"""
GUI Application cho MKV Video Processing Toolkit
Sử dụng tkinter (built-in Python) - không cần cài thêm
"""
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import queue
import os
import sys
from pathlib import Path

# Kiểm tra xem đang chạy từ executable (PyInstaller) hay source code
IS_EXECUTABLE = getattr(sys, 'frozen', False)

# QUAN TRỌNG: Import ffmpeg và psutil NGAY TỪ ĐẦU để PyInstaller bundle
# PyInstaller chỉ bundle những gì được import trực tiếp trong code
try:
    import ffmpeg  # type: ignore  # PyInstaller sẽ bundle package này
    import psutil  # type: ignore  # PyInstaller sẽ bundle package này
except ImportError:
    # Nếu không import được, sẽ xử lý sau
    pass

# Import các hàm từ script.py
process_main = None
check_ffmpeg_available = None
check_available_ram = None
get_file_size_gb = None
read_processed_files = None
create_folder = None
import_success = False

try:
    # Import từ script
    from script import (
        main as process_main,
        check_ffmpeg_available,
        check_available_ram,
        get_file_size_gb,
        read_processed_files,
        create_folder
    )
    import_success = True
except ImportError as e:
    # Nếu không import được
    import_error = str(e)
    # Chỉ in lỗi nếu đang chạy từ source code (không phải executable)
    if not IS_EXECUTABLE:
        print(f"Lỗi import: {import_error}")
    # Nếu chạy từ executable, thử thêm path
    elif hasattr(sys, '_MEIPASS'):
        try:
            sys.path.insert(0, sys._MEIPASS)
            # Thử import lại
            import ffmpeg  # type: ignore
            import psutil  # type: ignore
            from script import (
                main as process_main,
                check_ffmpeg_available,
                check_available_ram,
                get_file_size_gb,
                read_processed_files,
                create_folder
            )
            import_success = True
        except Exception as ex:
            print(f"Lỗi import trong executable: {ex}")
            pass


class MKVProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 MKV Video Processing Toolkit")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Queue để giao tiếp giữa thread xử lý và GUI
        self.log_queue = queue.Queue()
        
        # Biến trạng thái
        self.is_processing = False
        self.current_folder = tk.StringVar(value=".")
        
        self.setup_ui()
        self.check_dependencies()
        self.process_log_queue()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame, 
            text="🎬 MKV Video Processing Toolkit",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Tự động tách audio, trích xuất subtitle và đổi tên file video",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Folder selection
        folder_frame = ttk.LabelFrame(self.root, text="📁 Thư mục xử lý", padding="10")
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        
        folder_entry = ttk.Entry(folder_frame, textvariable=self.current_folder, width=60)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(
            folder_frame,
            text="Chọn thư mục...",
            command=self.browse_folder
        )
        browse_btn.pack(side=tk.LEFT)
        
        # System info
        info_frame = ttk.LabelFrame(self.root, text="ℹ️ Thông tin hệ thống", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.ffmpeg_status = ttk.Label(info_frame, text="FFmpeg: Đang kiểm tra...", foreground="orange")
        self.ffmpeg_status.pack(anchor=tk.W)
        
        self.ram_status = ttk.Label(info_frame, text="RAM: Đang kiểm tra...", foreground="orange")
        self.ram_status.pack(anchor=tk.W)
        
        self.folder_status = ttk.Label(info_frame, text="Thư mục: Chưa chọn", foreground="orange")
        self.folder_status.pack(anchor=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        self.process_btn = ttk.Button(
            control_frame,
            text="🚀 Bắt đầu xử lý",
            command=self.start_processing,
            state=tk.NORMAL
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            control_frame,
            text="⏹ Dừng",
            command=self.stop_processing,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="📊 Xem log đã xử lý",
            command=self.view_processed_log
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="❌ Đóng",
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Log output
        log_frame = ttk.LabelFrame(self.root, text="📝 Nhật ký xử lý", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Sẵn sàng",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def log(self, message, level="INFO"):
        """Thêm message vào log queue"""
        self.log_queue.put((message, level))
        
    def write_log(self, message, level="INFO"):
        """Ghi log vào text widget"""
        self.log_text.insert(tk.END, f"[{level}] {message}\n")
        self.log_text.see(tk.END)
        
        # Màu sắc theo level
        if level == "ERROR":
            self.status_bar.config(text=f"❌ Lỗi: {message[:50]}", foreground="red")
        elif level == "SUCCESS":
            self.status_bar.config(text=f"✅ {message[:50]}", foreground="green")
        elif level == "WARNING":
            self.status_bar.config(text=f"⚠️ {message[:50]}", foreground="orange")
        else:
            self.status_bar.config(text=message[:80], foreground="black")
            
    def process_log_queue(self):
        """Xử lý queue log từ thread xử lý"""
        try:
            while True:
                message, level = self.log_queue.get_nowait()
                self.write_log(message, level)
        except queue.Empty:
            pass
        finally:
            # Lên lịch kiểm tra lại sau 100ms
            self.root.after(100, self.process_log_queue)
            
    def check_dependencies(self):
        """Kiểm tra dependencies"""
        def check():
            # Kiểm tra FFmpeg
            if check_ffmpeg_available:
                try:
                    if check_ffmpeg_available():
                        self.root.after(0, lambda: self.ffmpeg_status.config(
                            text="FFmpeg: ✅ Đã cài đặt",
                            foreground="green"
                        ))
                        self.log("FFmpeg đã được cài đặt", "SUCCESS")
                    else:
                        self.root.after(0, lambda: self.ffmpeg_status.config(
                            text="FFmpeg: ❌ Chưa cài đặt",
                            foreground="red"
                        ))
                        self.log("FFmpeg chưa được cài đặt. Vui lòng cài đặt FFmpeg.", "ERROR")
                except Exception as e:
                    self.root.after(0, lambda: self.ffmpeg_status.config(
                        text="FFmpeg: ⚠️ Lỗi kiểm tra",
                        foreground="orange"
                    ))
                    self.log(f"Lỗi kiểm tra FFmpeg: {str(e)}", "WARNING")
            else:
                # Chỉ hiển thị warning nếu đang chạy từ source code
                if not IS_EXECUTABLE:
                    self.root.after(0, lambda: self.ffmpeg_status.config(
                        text="FFmpeg: ⚠️ Không thể kiểm tra (thiếu dependencies)",
                        foreground="orange"
                    ))
                    self.log("Thiếu thư viện Python. Chạy: pip install -r requirements.txt", "WARNING")
                else:
                    # Nếu chạy từ executable, thử kiểm tra FFmpeg trực tiếp
                    try:
                        import subprocess
                        result = subprocess.run(['ffmpeg', '-version'], 
                                               capture_output=True, 
                                               check=True)
                        self.root.after(0, lambda: self.ffmpeg_status.config(
                            text="FFmpeg: ✅ Đã cài đặt",
                            foreground="green"
                        ))
                        self.log("FFmpeg đã được cài đặt", "SUCCESS")
                    except:
                        # Kiểm tra FFmpeg local trong package
                        from ffmpeg_helper import check_ffmpeg_available as check_local
                        if check_local():
                            self.root.after(0, lambda: self.ffmpeg_status.config(
                                text="FFmpeg: ✅ Đã bundle",
                                foreground="green"
                            ))
                            self.log("FFmpeg đã được bundle trong package", "SUCCESS")
                        else:
                            self.root.after(0, lambda: self.ffmpeg_status.config(
                                text="FFmpeg: ❌ Chưa cài đặt",
                                foreground="red"
                            ))
                            self.log("FFmpeg chưa được cài đặt", "ERROR")
            
            # Kiểm tra RAM
            if check_available_ram:
                try:
                    ram = check_available_ram()
                    self.root.after(0, lambda r=ram: self.ram_status.config(
                        text=f"RAM: ✅ {r:.2f} GB khả dụng",
                        foreground="green"
                    ))
                except Exception as e:
                    self.root.after(0, lambda: self.ram_status.config(
                        text="RAM: ⚠️ Không thể kiểm tra",
                        foreground="orange"
                    ))
            else:
                # Chỉ hiển thị warning nếu đang chạy từ source code
                if not IS_EXECUTABLE:
                    self.root.after(0, lambda: self.ram_status.config(
                        text="RAM: ⚠️ Không thể kiểm tra (thiếu dependencies)",
                        foreground="orange"
                    ))
                else:
                    # Nếu chạy từ executable, thử import psutil trực tiếp
                    try:
                        import psutil
                        memory = psutil.virtual_memory()
                        ram_gb = memory.available / (1024 ** 3)
                        self.root.after(0, lambda r=ram_gb: self.ram_status.config(
                            text=f"RAM: ✅ {r:.2f} GB khả dụng",
                            foreground="green"
                        ))
                    except:
                        self.root.after(0, lambda: self.ram_status.config(
                            text="RAM: ⚠️ Không thể kiểm tra",
                            foreground="orange"
                        ))
            
            # Kiểm tra thư mục
            self.update_folder_status()
            
        threading.Thread(target=check, daemon=True).start()
        
    def browse_folder(self):
        """Chọn thư mục để xử lý"""
        folder = filedialog.askdirectory(
            title="Chọn thư mục chứa file MKV",
            initialdir=self.current_folder.get()
        )
        if folder:
            self.current_folder.set(folder)
            self.update_folder_status()
            
    def update_folder_status(self):
        """Cập nhật trạng thái thư mục"""
        folder = self.current_folder.get()
        if not folder or not os.path.exists(folder):
            self.folder_status.config(
                text="Thư mục: ❌ Không hợp lệ",
                foreground="red"
            )
            return
            
        # Đếm file MKV
        try:
            mkv_files = [f for f in os.listdir(folder) if f.lower().endswith('.mkv')]
            count = len(mkv_files)
            if count > 0:
                self.folder_status.config(
                    text=f"Thư mục: ✅ {count} file MKV tìm thấy",
                    foreground="green"
                )
                self.log(f"Tìm thấy {count} file MKV trong thư mục", "INFO")
            else:
                self.folder_status.config(
                    text="Thư mục: ⚠️ Không có file MKV",
                    foreground="orange"
                )
        except Exception as e:
            self.folder_status.config(
                text=f"Thư mục: ❌ Lỗi: {str(e)}",
                foreground="red"
            )
            
    def start_processing(self):
        """Bắt đầu xử lý trong thread riêng"""
        if self.is_processing:
            messagebox.showwarning("Cảnh báo", "Đang xử lý, vui lòng đợi...")
            return
            
        folder = self.current_folder.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục hợp lệ!")
            return
            
        # Kiểm tra FFmpeg
        ffmpeg_ok = False
        if check_ffmpeg_available:
            ffmpeg_ok = check_ffmpeg_available()
        elif IS_EXECUTABLE:
            # Nếu chạy từ executable, thử kiểm tra trực tiếp
            try:
                from ffmpeg_helper import check_ffmpeg_available as check_local
                ffmpeg_ok = check_local()
            except:
                try:
                    import subprocess
                    subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, check=True)
                    ffmpeg_ok = True
                except:
                    ffmpeg_ok = False
        
        if not ffmpeg_ok:
            response = messagebox.askyesno(
                "Cảnh báo",
                "FFmpeg chưa được cài đặt. Bạn có muốn tiếp tục không?\n"
                "(Có thể gặp lỗi trong quá trình xử lý)"
            )
            if not response:
                return
                
        # Xác nhận
        mkv_files = [f for f in os.listdir(folder) if f.lower().endswith('.mkv')]
        if not mkv_files:
            messagebox.showwarning("Cảnh báo", "Không tìm thấy file MKV nào trong thư mục!")
            return
            
        response = messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn xử lý {len(mkv_files)} file MKV trong thư mục này?\n\n"
            f"Thư mục: {folder}"
        )
        if not response:
            return
            
        # Bắt đầu xử lý
        self.is_processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        self.log(f"Bắt đầu xử lý {len(mkv_files)} file MKV...", "INFO")
        
        # Chạy trong thread riêng
        def process():
            try:
                # Thử import lại script.py trong thread này (có thể cần thiết khi chạy từ executable)
                process_main_func = process_main
                
                if not process_main_func:
                    # Thử import lại
                    try:
                        if IS_EXECUTABLE:
                            # Khi chạy từ executable, script.py có thể ở trong _MEIPASS
                            if hasattr(sys, '_MEIPASS'):
                                # Thêm _MEIPASS vào path
                                sys.path.insert(0, sys._MEIPASS)
                            
                            # Đảm bảo import được ffmpeg và psutil trước
                            try:
                                import ffmpeg  # type: ignore
                                import psutil  # type: ignore
                            except ImportError as e:
                                self.log(f"Lỗi import dependencies: {str(e)}", "ERROR")
                                self.log("Vui lòng build lại với: python build_complete.py", "ERROR")
                                return
                        
                        from script import main as process_main_func
                        self.log("Đã import script.py thành công", "INFO")
                    except ImportError as import_err:
                        self.log(f"Lỗi import script.py: {str(import_err)}", "ERROR")
                        import traceback
                        self.log(traceback.format_exc(), "ERROR")
                        self.log("Vui lòng đảm bảo script.py và dependencies có trong package", "ERROR")
                        return
                
                if process_main_func:
                    # Redirect stdout/stderr để capture log
                    import io
                    
                    old_stdout = sys.stdout
                    old_stderr = sys.stderr
                    
                    try:
                        # Tạo StringIO để capture output
                        log_capture = io.StringIO()
                        sys.stdout = log_capture
                        sys.stderr = log_capture
                        
                        # Chạy xử lý với thư mục đã chọn
                        process_main_func(folder)
                        
                        # Lấy output
                        output = log_capture.getvalue()
                        for line in output.split('\n'):
                            if line.strip():
                                self.log(line, "INFO")
                                
                    finally:
                        sys.stdout = old_stdout
                        sys.stderr = old_stderr
                else:
                    self.log("Không thể import script.py. Vui lòng kiểm tra lại.", "ERROR")
                    
            except Exception as e:
                self.log(f"Lỗi khi xử lý: {str(e)}", "ERROR")
                import traceback
                self.log(traceback.format_exc(), "ERROR")
            finally:
                # Khôi phục UI
                self.root.after(0, self.processing_finished)
                
        threading.Thread(target=process, daemon=True).start()
        
    def stop_processing(self):
        """Dừng xử lý (chỉ có thể dừng bằng cách đóng ứng dụng)"""
        if self.is_processing:
            response = messagebox.askyesno(
                "Xác nhận",
                "Bạn có chắc muốn dừng xử lý?\n"
                "(Quá trình hiện tại sẽ hoàn thành file đang xử lý)"
            )
            if response:
                self.is_processing = False
                self.log("Người dùng yêu cầu dừng xử lý...", "WARNING")
                
    def processing_finished(self):
        """Gọi khi xử lý hoàn tất"""
        self.is_processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.log("Hoàn thành xử lý!", "SUCCESS")
        messagebox.showinfo("Hoàn thành", "Đã xử lý xong tất cả file!")
        
    def view_processed_log(self):
        """Xem log các file đã xử lý"""
        folder = self.current_folder.get()
        if not folder:
            folder = "."
            
        log_file = os.path.join(folder, "Subtitles", "processed_files.log")
        
        if not os.path.exists(log_file):
            messagebox.showinfo("Thông tin", "Chưa có file log nào được tạo.")
            return
            
        # Mở file log trong cửa sổ mới
        log_window = tk.Toplevel(self.root)
        log_window.title("📊 Log các file đã xử lý")
        log_window.geometry("800x600")
        
        text_widget = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert(1.0, content)
        except Exception as e:
            text_widget.insert(1.0, f"Lỗi khi đọc file log: {str(e)}")


def main():
    """Hàm main để chạy GUI"""
    root = tk.Tk()
    app = MKVProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

