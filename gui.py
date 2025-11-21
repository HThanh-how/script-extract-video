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
import json
import importlib
import importlib.util
from pathlib import Path

import requests

from config_manager import load_user_config, save_user_config

# Đảm bảo thư mục chứa script nằm trong sys.path
BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def load_script_module():
    try:
        import script  # type: ignore
        return script
    except ModuleNotFoundError:
        for candidate in ("script.py", "script.pyc"):
            script_file = BASE_DIR / candidate
            if script_file.exists():
                spec = importlib.util.spec_from_file_location("script", script_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)  # type: ignore[attr-defined]
                    sys.modules["script"] = module
                    return module
        raise

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
    script_module = load_script_module()
    process_main = getattr(script_module, "main", None)
    check_ffmpeg_available = getattr(script_module, "check_ffmpeg_available", None)
    check_available_ram = getattr(script_module, "check_available_ram", None)
    get_file_size_gb = getattr(script_module, "get_file_size_gb", None)
    read_processed_files = getattr(script_module, "read_processed_files", None)
    create_folder = getattr(script_module, "create_folder", None)
    import_success = all([
        process_main,
        check_ffmpeg_available,
        check_available_ram,
        get_file_size_gb,
        read_processed_files,
        create_folder,
    ])
except Exception as e:
    import_error = str(e)
    if not IS_EXECUTABLE:
        print(f"Lỗi import script: {import_error}")


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
        self.processing_error = False
        self.config = load_user_config()
        self.current_folder = tk.StringVar(value=self.config.get("input_folder", "."))
        self.auto_upload_var = tk.BooleanVar(value=self.config.get("auto_upload", False))
        self.repo_var = tk.StringVar(value=self.config.get("repo", "HThanh-how/Subtitles"))
        self.branch_var = tk.StringVar(value=self.config.get("branch", "main"))
        self.logs_dir_var = tk.StringVar(value=self.config.get("logs_dir", "logs"))
        self.subtitle_dir_var = tk.StringVar(value=self.config.get("subtitle_dir", "subtitles"))
        self.token_var = tk.StringVar(value=self.config.get("token", ""))
        self.show_token = tk.BooleanVar(value=False)
        
        self.setup_ui()
        self.check_dependencies()
        self.process_log_queue()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng hiện đại với tabs."""
        self.setup_styles()
        self.notebook = ttk.Notebook(self.root)
        self.processing_tab = ttk.Frame(self.notebook, padding="15")
        self.settings_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.processing_tab, text="📂 Xử lý")
        self.notebook.add(self.settings_tab, text="⚙️ Cài đặt")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.build_processing_tab(self.processing_tab)
        self.build_settings_tab(self.settings_tab)
        self.update_github_status()

        self.status_bar = ttk.Label(
            self.root,
            text="Sẵn sàng",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11))
        style.configure("Section.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure("StatusGood.TLabel", foreground="#1b873f")
        style.configure("StatusWarn.TLabel", foreground="#d99428")
        style.configure("StatusBad.TLabel", foreground="#c62828")

    def build_processing_tab(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X)

        ttk.Label(
            header_frame,
            text="🎬 MKV Video Processing Toolkit",
            style="Title.TLabel"
        ).pack(anchor=tk.W)
        ttk.Label(
            header_frame,
            text="Tự động tách audio, trích xuất subtitle, đổi tên & đồng bộ GitHub",
            style="Subtitle.TLabel"
        ).pack(anchor=tk.W, pady=(0, 10))

        folder_frame = ttk.LabelFrame(parent, text="📁 Thư mục xử lý", padding=10)
        folder_frame.pack(fill=tk.X, pady=5)

        folder_entry = ttk.Entry(folder_frame, textvariable=self.current_folder)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(folder_frame, text="Chọn...", command=self.browse_folder).pack(side=tk.LEFT)

        info_frame = ttk.LabelFrame(parent, text="🖥️ Trạng thái hệ thống", padding=10)
        info_frame.pack(fill=tk.X, pady=5)

        self.ffmpeg_status = ttk.Label(info_frame, text="FFmpeg: Đang kiểm tra...", style="StatusWarn.TLabel")
        self.ffmpeg_status.pack(anchor=tk.W)

        self.ram_status = ttk.Label(info_frame, text="RAM: Đang kiểm tra...", style="StatusWarn.TLabel")
        self.ram_status.pack(anchor=tk.W)

        self.folder_status = ttk.Label(info_frame, text="Thư mục: Chưa chọn", style="StatusWarn.TLabel")
        self.folder_status.pack(anchor=tk.W)

        self.github_status = ttk.Label(
            info_frame,
            text="GitHub: Chưa cấu hình",
            style="StatusWarn.TLabel"
        )
        self.github_status.pack(anchor=tk.W)

        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10)

        self.process_btn = ttk.Button(
            control_frame,
            text="🚀 Bắt đầu xử lý",
            command=self.start_processing
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
            text="📂 Mở thư mục logs",
            command=self.view_processed_log
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            control_frame,
            text="📋 Copy log",
            command=self.copy_log_text
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            control_frame,
            text="⚙️ Cài đặt",
            command=lambda: self.notebook.select(self.settings_tab)
        ).pack(side=tk.RIGHT, padx=5)

        self.progress = ttk.Progressbar(parent, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=5)

        log_frame = ttk.LabelFrame(parent, text="📝 Nhật ký xử lý", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=18,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def build_settings_tab(self, parent):
        ttk.Label(parent, text="Cài đặt đồng bộ & GitHub", style="Section.TLabel").pack(anchor=tk.W)
        ttk.Label(parent, text="Nhập token GitHub (fine-grained, chỉ repo Subtitles).", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(0, 10))

        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(
            form_frame,
            text="Bật tự động upload lên GitHub (Subtitles repo)",
            variable=self.auto_upload_var,
            command=self.on_setting_change
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Label(form_frame, text="Repository").grid(row=1, column=0, sticky="e", pady=2, padx=5)
        repo_entry = ttk.Entry(form_frame, textvariable=self.repo_var, width=40)
        repo_entry.grid(row=1, column=1, sticky="we", pady=2)

        ttk.Label(form_frame, text="Branch").grid(row=2, column=0, sticky="e", pady=2, padx=5)
        ttk.Entry(form_frame, textvariable=self.branch_var).grid(row=2, column=1, sticky="we", pady=2)

        ttk.Label(form_frame, text="Thư mục logs").grid(row=3, column=0, sticky="e", pady=2, padx=5)
        ttk.Entry(form_frame, textvariable=self.logs_dir_var).grid(row=3, column=1, sticky="we", pady=2)

        ttk.Label(form_frame, text="Thư mục subtitles").grid(row=4, column=0, sticky="e", pady=2, padx=5)
        ttk.Entry(form_frame, textvariable=self.subtitle_dir_var).grid(row=4, column=1, sticky="we", pady=2)

        ttk.Label(form_frame, text="GitHub Token").grid(row=5, column=0, sticky="ne", pady=2, padx=5)
        token_entry = ttk.Entry(form_frame, textvariable=self.token_var, show="•")
        token_entry.grid(row=5, column=1, sticky="we", pady=2)

        ttk.Checkbutton(
            form_frame,
            text="Hiển thị token",
            variable=self.show_token,
            command=lambda: token_entry.config(show="" if self.show_token.get() else "•")
        ).grid(row=6, column=1, sticky="w")

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="💾 Lưu cấu hình", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Kiểm tra kết nối", command=self.test_connection).pack(side=tk.LEFT, padx=5)

        self.settings_status = ttk.Label(parent, text="", style="Subtitle.TLabel")
        self.settings_status.pack(anchor=tk.W, pady=5)

    def collect_settings_from_ui(self):
        return {
            "auto_upload": self.auto_upload_var.get(),
            "repo": self.repo_var.get().strip(),
            "branch": self.branch_var.get().strip() or "main",
            "logs_dir": self.logs_dir_var.get().strip() or "logs",
            "subtitle_dir": self.subtitle_dir_var.get().strip() or "subtitles",
            "token": self.token_var.get().strip(),
            "input_folder": self.current_folder.get(),
        }

    def on_setting_change(self):
        self.update_github_status()

    def save_settings(self):
        data = self.collect_settings_from_ui()
        save_user_config(data)
        self.config.update(data)
        self.settings_status.config(text="✅ Đã lưu cấu hình!")
        self.update_github_status()

    def test_connection(self):
        data = self.collect_settings_from_ui()
        if not data["auto_upload"]:
            messagebox.showwarning("Thông tin", "Bạn chưa bật chế độ tự động upload.")
            return
        if not data["token"]:
            messagebox.showerror("Thiếu token", "Vui lòng nhập GitHub token.")
            return
        try:
            headers = {
                "Authorization": f"Bearer {data['token']}",
                "Accept": "application/vnd.github+json",
            }
            resp = requests.get(f"https://api.github.com/repos/{data['repo']}", headers=headers, timeout=10)
            if resp.status_code == 200:
                messagebox.showinfo("Thành công", "Kết nối GitHub thành công!")
                self.settings_status.config(text="✅ Kết nối GitHub thành công!", style="StatusGood.TLabel")
            else:
                messagebox.showerror("Lỗi", f"Không thể kết nối (mã {resp.status_code}). Kiểm tra repo/token.")
                self.settings_status.config(text=f"❌ Lỗi kết nối: {resp.status_code}", style="StatusBad.TLabel")
        except Exception as exc:
            messagebox.showerror("Lỗi", f"Không thể kết nối GitHub: {exc}")
            self.settings_status.config(text=f"❌ Lỗi kết nối: {exc}", style="StatusBad.TLabel")

    def update_github_status(self):
        if self.auto_upload_var.get() and self.token_var.get().strip():
            self.github_status.config(text="GitHub: ✅ Đồng bộ bật", style="StatusGood.TLabel")
        elif self.auto_upload_var.get():
            self.github_status.config(text="GitHub: ⚠️ Thiếu token", style="StatusWarn.TLabel")
        else:
            self.github_status.config(text="GitHub: 🔌 Đang tắt", style="StatusWarn.TLabel")
        
    def log(self, message, level="INFO"):
        """Thêm message vào log queue"""
        if level == "ERROR":
            self.processing_error = True
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
            self.root.after(0, self.update_github_status)
            
        threading.Thread(target=check, daemon=True).start()
        
    def browse_folder(self):
        """Chọn thư mục để xử lý"""
        folder = filedialog.askdirectory(
            title="Chọn thư mục chứa file MKV",
            initialdir=self.current_folder.get()
        )
        if folder:
            self.current_folder.set(folder)
            self.config["input_folder"] = folder
            save_user_config(self.collect_settings_from_ui())
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
        self.config["input_folder"] = folder
        save_user_config(self.collect_settings_from_ui())
            
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
        self.processing_error = False
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
                        script_module = load_script_module()
                        process_main_func = getattr(script_module, "main", None)
                        if not process_main_func:
                            raise ImportError("Không tìm thấy hàm main trong script.py")
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
        if self.processing_error:
            self.log("Quá trình kết thúc nhưng có lỗi. Xem log chi tiết.", "WARNING")
            messagebox.showwarning("Hoàn thành (có lỗi)", "Đã kết thúc nhưng xuất hiện lỗi. Vui lòng xem log để biết chi tiết.")
        else:
            self.log("Hoàn thành xử lý!", "SUCCESS")
            messagebox.showinfo("Hoàn thành", "Đã xử lý xong tất cả file!")
        
    def view_processed_log(self):
        """Mở thư mục logs và hiển thị file JSON mới nhất."""
        logs_dir = Path(self.logs_dir_var.get() or "logs")
        if not logs_dir.exists():
            messagebox.showinfo("Thông tin", f"Chưa có thư mục logs ({logs_dir}).")
            return

        json_files = sorted(logs_dir.glob("*.json"), reverse=True)
        if not json_files:
            messagebox.showinfo("Thông tin", f"Chưa có file log trong {logs_dir}.")
            return

        latest = json_files[0]
        log_window = tk.Toplevel(self.root)
        log_window.title(f"📊 Log: {latest.name}")
        log_window.geometry("900x600")

        text_widget = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        try:
            content = latest.read_text(encoding="utf-8")
            parsed = json.loads(content)
            text_widget.insert(1.0, json.dumps(parsed, ensure_ascii=False, indent=2))
        except Exception as e:
            text_widget.insert(1.0, f"Lỗi khi đọc log: {e}")

    def copy_log_text(self):
        """Copy toàn bộ log hiện tại vào clipboard"""
        content = self.log_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Thông tin", "Chưa có log để copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_bar.config(text="Đã copy log vào clipboard", foreground="#2563eb")


def main():
    """Hàm main để chạy GUI"""
    root = tk.Tk()
    app = MKVProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

