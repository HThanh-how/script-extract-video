import os
import sys
import subprocess
import platform
import re
import datetime
import tempfile
import io
import shutil
from contextlib import contextmanager

# Kiểm tra và hướng dẫn cài đặt các package cần thiết
if __name__ == '__main__':
    try:
        # Thử import các module cần thiết
        try:
            import ffmpeg
            import psutil
            # Nếu import thành công, tiếp tục chạy script
            print("Đã tìm thấy các thư viện cần thiết.")
        except ImportError as e:
            # Nếu không import được, hiển thị hướng dẫn cài đặt
            print(f"\n{'='*50}")
            print("HƯỚNG DẪN CÀI ĐẶT THƯ VIỆN".center(50))
            print(f"{'='*50}")
            print(f"\nKhông thể tìm thấy thư viện: {e}")
            print("\nVui lòng cài đặt các thư viện cần thiết bằng một trong các cách sau:")
            
            # Hướng dẫn cài đặt trên hệ thống Linux
            if platform.system() == "Linux":
                print("\n--- CHO UBUNTU/DEBIAN ---")
                print("1. Cài đặt python3-pip và ffmpeg:")
                print("   sudo apt update")
                print("   sudo apt install -y python3-pip ffmpeg")
                print("\n2. Cài đặt các thư viện Python:")
                print("   python3 -m pip install ffmpeg-python psutil --user")
                
                print("\n--- CHO FEDORA/RHEL ---")
                print("1. Cài đặt python3-pip và ffmpeg:")
                print("   sudo dnf install -y python3-pip ffmpeg")
                print("\n2. Cài đặt các thư viện Python:")
                print("   python3 -m pip install ffmpeg-python psutil --user")
                
                print("\n--- SỬ DỤNG SNAP (NẾU CÓ) ---")
                print("1. Cài đặt ffmpeg qua snap:")
                print("   sudo snap install ffmpeg")
            
            # Hướng dẫn cài đặt trên MacOS
            elif platform.system() == "Darwin":
                print("\n--- CHO MACOS ---")
                print("1. Cài đặt Homebrew (nếu chưa có):")
                print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                print("\n2. Cài đặt ffmpeg:")
                print("   brew install ffmpeg")
                print("\n3. Cài đặt các thư viện Python:")
                print("   pip3 install ffmpeg-python psutil")
            
            # Hướng dẫn cài đặt trên Windows
            elif platform.system() == "Windows":
                print("\n--- CHO WINDOWS ---")
                print("1. Tải và cài đặt FFmpeg từ trang chủ:")
                print("   https://ffmpeg.org/download.html")
                print("\n2. Thêm đường dẫn FFmpeg vào biến môi trường PATH")
                print("\n3. Cài đặt các thư viện Python:")
                print("   pip install ffmpeg-python psutil")
            
            # Hướng dẫn chung
            print("\n--- CÁCH NHANH NHẤT (TẤT CẢ HỆ ĐIỀU HÀNH) ---")
            print("Sử dụng môi trường ảo (khuyến nghị):")
            print("1. Tạo môi trường ảo:")
            print("   python3 -m venv venv")
            print("\n2. Kích hoạt môi trường ảo:")
            print("   - Linux/MacOS: source venv/bin/activate")
            print("   - Windows: venv\\Scripts\\activate")
            print("\n3. Cài đặt các thư viện:")
            print("   pip install ffmpeg-python psutil")
            print("\n4. Chạy script trong môi trường ảo:")
            print("   python script.py")
            
            print(f"\n{'='*50}")
            print("LƯU Ý: Script này cần FFmpeg để xử lý video.")
            print("Vui lòng đảm bảo FFmpeg đã được cài đặt và có sẵn trong PATH")
            
            sys.exit(1)
            
        # Kiểm tra FFmpeg đã được cài đặt chưa
        try:
            subprocess.check_call(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Đã tìm thấy FFmpeg trên hệ thống.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("\nCẢNH BÁO: Không tìm thấy FFmpeg trên hệ thống!")
            print("Script này yêu cầu FFmpeg để xử lý video.")
            
            print("\nHướng dẫn cài đặt FFmpeg:")
            if platform.system() == "Linux":
                print("- Ubuntu/Debian: sudo add-apt-repository universe && sudo apt update && sudo apt install -y ffmpeg")
                print("- Fedora/RHEL: sudo dnf install -y ffmpeg")
                print("- Sử dụng snap: sudo snap install ffmpeg")
            elif platform.system() == "Darwin":
                print("- macOS: brew install ffmpeg")
            elif platform.system() == "Windows":
                print("- Windows: Tải từ https://ffmpeg.org/download.html và thêm vào PATH")
            
            response = input("\nBạn có muốn tiếp tục mà không có FFmpeg không? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
                
        # Nếu mọi thứ đã sẵn sàng, tiếp tục thực hiện script
        print("\nMọi thư viện đã sẵn sàng. Bắt đầu xử lý...")
        
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)

# Import các thư viện cần thiết
import ffmpeg
import psutil

import re
import datetime
import tempfile
import io
import shutil
from contextlib import contextmanager

def create_folder(folder_name):
    """Tạo folder nếu chưa tồn tại."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def log_processed_file(log_file, old_name, new_name):
    """Ghi lại log file đã được xử lý với tên cũ và mới."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(".", old_name)
    signature = get_file_signature(file_path) if os.path.exists(file_path) else ""
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"{old_name}|{new_name}|{current_time}|{signature}\n")

def read_processed_files(log_file):
    """Đọc danh sách các file đã xử lý từ log."""
    processed_files = {}
    processed_signatures = {}
    if os.path.exists(log_file):
        with open(log_file, "r", encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    old_name = parts[0]
                    new_name = parts[1]
                    time_processed = parts[2] if len(parts) > 2 else ""
                    signature = parts[3] if len(parts) > 3 else ""
                    
                    info = {"new_name": new_name, "time": time_processed, "signature": signature}
                    processed_files[old_name] = info
                    processed_files[new_name] = info
                    if signature:
                        processed_signatures[signature] = info
    return processed_files, processed_signatures

def sanitize_filename(name):
    """Loại bỏ các ký tự không hợp lệ trong tên tệp để tránh lỗi FFmpeg."""
    # Thay thế các ký tự không hợp lệ bằng dấu gạch dưới
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '_', name)

def get_video_resolution_label(file_path):
    """Lấy tên độ phân giải video (FHD, 4K, 2K, HD)."""
    try:
        probe = ffmpeg.probe(file_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream and 'width' in video_stream and 'height' in video_stream:
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            # 8k
            if width >= 7680 or height >= 4320:
                return "8K"
            # 4k
            elif width >= 3840 or height >= 2160:  # Bao gồm cả 3840x1608
                return "4K"
            # 2k
            elif width >= 2560 or height >= 1440:
                return "2K"
            # FHD
            elif width >= 1920 or height >= 1080:
                return "FHD"
            # HD
            elif width >= 1280 or height >= 720:
                return "HD"
            # 480p
            elif width >= 720 or height >= 480:
                return "480p"
            else:
                return f"{width}p"
    except Exception as e:
        print(f"Error getting resolution for {file_path}: {e}")
    return "unknown_resolution"

def get_movie_year(file_path):
    """Lấy năm của phim từ metadata."""
    try:
        probe = ffmpeg.probe(file_path)
        format_tags = probe.get("format", {}).get("tags", {})
        year = format_tags.get("year", "")
        return year.strip()
    except Exception as e:
        print(f"Error getting year for {file_path}: {e}")
    return ""

def get_language_abbreviation(language_code):
    """Trả về tên viết tắt của ngôn ngữ dựa trên mã ngôn ngữ."""
    language_map = {
        'eng': 'ENG',  # Tiếng Anh
        'vie': 'VIE',  # Tiếng Việt
        'und': 'UNK',  # Không xác định (Undefined)
        'chi': 'CHI',  # Tiếng Trung
        'zho': 'CHI',  # Tiếng Trung (mã khác)
        'jpn': 'JPN',  # Tiếng Nhật
        'kor': 'KOR',  # Tiếng Hàn
        'fra': 'FRA',  # Tiếng Pháp
        'deu': 'DEU',  # Tiếng Đức
        'spa': 'SPA',  # Tiếng Tây Ban Nha
        'ita': 'ITA',  # Tiếng Ý
        'rus': 'RUS',  # Tiếng Nga
        'tha': 'THA',  # Tiếng Thái
        'ind': 'IND',  # Tiếng Indonesia
        'msa': 'MSA',  # Tiếng Malaysia
        'ara': 'ARA',  # Tiếng Ả Rập
        'hin': 'HIN',  # Tiếng Hindi
        'por': 'POR',  # Tiếng Bồ Đào Nha
        'nld': 'NLD',  # Tiếng Hà Lan
        'pol': 'POL',  # Tiếng Ba Lan
        'tur': 'TUR',  # Tiếng Thổ Nhĩ Kỳ
        'swe': 'SWE',  # Tiếng Thụy Điển
        'nor': 'NOR',  # Tiếng Na Uy
        'dan': 'DAN',  # Tiếng Đan Mạch
        'fin': 'FIN',  # Tiếng Phần Lan
        'ukr': 'UKR',  # Tiếng Ukraine
        'ces': 'CES',  # Tiếng Séc
        'hun': 'HUN',  # Tiếng Hungary
        'ron': 'RON',  # Tiếng Romania
        'bul': 'BUL',  # Tiếng Bulgaria
        'hrv': 'HRV',  # Tiếng Croatia
        'srp': 'SRP',  # Tiếng Serbia
        'slv': 'SLV',  # Tiếng Slovenia
        'ell': 'ELL',  # Tiếng Hy Lạp
        'heb': 'HEB',  # Tiếng Do Thái
        'kat': 'KAT',  # Tiếng Georgia
        'lat': 'LAT',  # Tiếng Latin
        'vie-Nom': 'NOM',  # Chữ Nôm
        'cmn': 'CMN',  # Tiếng Trung (Phổ thông)
        'yue': 'YUE',  # Tiếng Quảng Đông
        'nan': 'NAN',  # Tiếng Mân Nam
        'khm': 'KHM',  # Tiếng Khmer
        'lao': 'LAO',  # Tiếng Lào
        'mya': 'MYA',  # Tiếng Miến Điện
        'ben': 'BEN',  # Tiếng Bengal
        'tam': 'TAM',  # Tiếng Tamil
        'tel': 'TEL',  # Tiếng Telugu
        'mal': 'MAL',  # Tiếng Malayalam
        'kan': 'KAN',  # Tiếng Kannada
        'mar': 'MAR',  # Tiếng Marathi
        'pan': 'PAN',  # Tiếng Punjab
        'guj': 'GUJ',  # Tiếng Gujarat
        'ori': 'ORI',  # Tiếng Oriya
        'asm': 'ASM',  # Tiếng Assam
        'urd': 'URD',  # Tiếng Urdu
        'fas': 'FAS',  # Tiếng Ba Tư
        'pus': 'PUS',  # Tiếng Pashto
        'kur': 'KUR',  # Tiếng Kurdish
    }
    return language_map.get(language_code, language_code.upper()[:3])

def rename_simple(file_path):
    """Đổi tên file đơn giản cho trường hợp không có audio để tách."""
    try:
        resolution_label = get_video_resolution_label(file_path)
        probe = ffmpeg.probe(file_path)
        # Lấy ngôn ngữ từ audio stream đầu tiên
        audio_stream = next((stream for stream in probe['streams'] 
                           if stream['codec_type'] == 'audio'), None)
        language = 'und'  # mặc định là undefined
        audio_title = ''
        if audio_stream:
            language = audio_stream.get('tags', {}).get('language', 'und')
            audio_title = audio_stream.get('tags', {}).get('title', '')
        
        language_abbr = get_language_abbreviation(language)
        # Chỉ thêm audio_title nếu khác với language_abbr và không rỗng
        if audio_title and audio_title != language_abbr:
            lang_part = f"{language_abbr}_{audio_title}"
        else:
            lang_part = language_abbr
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        new_name = f"{resolution_label}_{lang_part}_{base_name}.mkv"
        new_name = sanitize_filename(new_name)
        
        dir_path = os.path.dirname(file_path)
        new_path = os.path.join(dir_path, new_name)
        
        os.rename(file_path, new_path)
        print(f"Simple renamed file to: {new_name}")
        return new_path
    except Exception as e:
        print(f"Error simple renaming file {file_path}: {e}")
        return file_path

def extract_video_with_audio(file_path, vn_folder, original_folder, log_file, probe_data):
    """Tách video với audio theo yêu cầu."""
    try:
        audio_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'audio']
        
        if not audio_streams:
            print(f"No audio found in {file_path}. Performing simple rename.")
            new_path = rename_simple(file_path)
            log_processed_file(log_file, os.path.basename(file_path), os.path.basename(new_path))
            return

        # Lấy thông tin audio đầu tiên để xác định trường hợp
        first_audio = audio_streams[0]
        first_audio_language = first_audio.get('tags', {}).get('language', 'und')

        # Tạo danh sách audio tracks với thông tin cần thiết
        audio_tracks = []
        for stream in audio_streams:
            index = stream.get('index', -1)
            channels = stream.get('channels', 0)
            language = stream.get('tags', {}).get('language', 'und')
            title = stream.get('tags', {}).get('title', get_language_abbreviation(language))
            audio_tracks.append((index, channels, language, title))

        # Sắp xếp theo số kênh giảm dần
        audio_tracks.sort(key=lambda x: x[1], reverse=True)
        
        vietnamese_tracks = [track for track in audio_tracks if track[2] == 'vie']
        non_vietnamese_tracks = [track for track in audio_tracks if track[2] != 'vie']

        if first_audio_language == 'vie':
            # Trường hợp 1: Audio đầu tiên là tiếng Việt
            if non_vietnamese_tracks:
                # Chọn audio không phải tiếng Việt có nhiều kênh nhất
                selected_track = non_vietnamese_tracks[0]
                process_video(file_path, original_folder, selected_track, log_file, probe_data)
        else:
            # Trường hợp 2: Audio đầu tiên không phải tiếng Việt
            if vietnamese_tracks:
                # Chọn audio tiếng Việt có nhiều kênh nhất
                selected_track = vietnamese_tracks[0]
                process_video(file_path, vn_folder, selected_track, log_file, probe_data)

    except Exception as e:
        print(f"Exception while processing {file_path}: {e}")

def rename_file(file_path, audio_info, is_output=False):
    """Đổi tên file theo format yêu cầu."""
    try:
        resolution_label = get_video_resolution_label(file_path)
        year = get_movie_year(file_path)
        language = audio_info[2]  # Mã ngôn ngữ
        audio_title = audio_info[3]  # Tiêu đề audio
        
        # Lấy tên gốc của file
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Format chung cho cả file gốc và output:
        # resolution_label + language_abbr + audio_title + year + base_name
        language_abbr = get_language_abbreviation(language)
        new_name = f"{resolution_label}_{language_abbr}_{audio_title}"
        
        if year:
            new_name += f"_{year}"
        new_name += f"_{base_name}.mkv"
        
        new_name = sanitize_filename(new_name)
        
        # Tạo đường dẫn mới
        dir_path = os.path.dirname(file_path)
        new_path = os.path.join(dir_path, new_name)
        
        # Đổi tên file
        os.rename(file_path, new_path)
        print(f"Renamed file to: {new_name}")
        return new_path
    except Exception as e:
        print(f"Error renaming file {file_path}: {e}")
        return file_path

def process_video(file_path, output_folder, selected_track, log_file, probe_data):
    """Xử lý video với track audio đã chọn và trích xuất subtitle."""
    try:
        original_filename = os.path.basename(file_path)
        
        # Lấy thông tin cơ bản
        resolution_label = get_video_resolution_label(file_path)
        year = get_movie_year(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Lấy thông tin audio đầu tiên
        first_audio = next((stream for stream in probe_data['streams'] 
                          if stream['codec_type'] == 'audio'), None)
        
        if first_audio:
            first_audio_lang = first_audio.get('tags', {}).get('language', 'und')
            first_audio_title = first_audio.get('tags', {}).get('title', '')
            # Sử dụng title chỉ khi khác với language abbreviation
            first_audio_display = get_language_abbreviation(first_audio_lang)
            if first_audio_title and first_audio_title != first_audio_display:
                first_audio_display += f"_{first_audio_title}"
            
            # Logic tương tự cho selected track
            selected_lang_abbr = get_language_abbreviation(selected_track[2])
            selected_title = selected_track[3]
            selected_display = selected_lang_abbr
            if selected_title and selected_title != selected_lang_abbr:
                selected_display += f"_{selected_title}"
            
            # Format tên file
            if first_audio_lang == 'vie':
                source_name = f"{resolution_label}_{first_audio_display}"
                output_name = f"{resolution_label}_{selected_display}"
            else:
                source_name = f"{resolution_label}_{first_audio_display}"
                output_name = f"{resolution_label}_{selected_display}"
            
            # Thêm năm và tên gốc
            if year:
                source_name += f"_{year}"
                output_name += f"_{year}"
            source_name += f"_{base_name}.mkv"
            output_name += f"_{base_name}.mkv"
            
            # Đường dẫn output cuối cùng
            final_output_path = os.path.join(output_folder, sanitize_filename(output_name))
            
            # Kiểm tra trường hợp file đích đã tồn tại
            if os.path.exists(final_output_path):
                print(f"File đích đã tồn tại: {final_output_path}. Bỏ qua.")
                return True
            
            # Kiểm tra không gian trống trên đĩa
            try:
                output_dir = os.path.dirname(final_output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                disk_usage = shutil.disk_usage(output_dir)
                free_space_gb = disk_usage.free / (1024**3)
                print(f"Dung lượng trống trên ổ đĩa: {free_space_gb:.2f} GB")
                
                if free_space_gb < 2:  # Cần ít nhất 2GB không gian trống để an toàn
                    print(f"CẢNH BÁO: Quá ít dung lượng trống trên ổ đĩa. Cần ít nhất 2GB")
                    return False
            except Exception as disk_err:
                print(f"Lỗi khi kiểm tra dung lượng ổ đĩa: {disk_err}")
            
            # Kiểm tra RAM khả dụng
            file_size = get_file_size_gb(file_path)
            available_ram = check_available_ram()
            
            # Ưu tiên xử lý trong RAM nếu có đủ RAM
            ram_required = file_size * 2  # Cần ít nhất 200% kích thước file
            try_ram_first = available_ram > ram_required
            
            if try_ram_first:
                print(f"Đủ RAM để xử lý file ({available_ram:.2f}GB > {ram_required:.2f}GB). Thử xử lý trong RAM...")
                
                # Xử lý trong RAM
                ram_success = False
                try:
                    with temp_directory_in_memory(use_ram=True) as temp_dir:
                        # Đường dẫn tạm thời trong RAM
                        temp_output_path = os.path.join(temp_dir, sanitize_filename(output_name))
                        
                        # Xử lý tách audio trong RAM
                        cmd = [
                            'ffmpeg',
                            '-i', file_path,
                            '-map', '0:v',
                            '-map', f'0:{selected_track[0]}',
                            '-c', 'copy',
                            '-y',
                            temp_output_path
                        ]
                        
                        print(f"Đang chạy lệnh trong RAM: {' '.join(cmd)}")
                        result = subprocess.run(cmd, capture_output=True)
                        
                        if result.returncode == 0 and os.path.exists(temp_output_path):
                            print(f"Xử lý trong RAM thành công. Di chuyển file tới: {final_output_path}")
                            # Chuyển từ RAM sang ổ đĩa
                            shutil.copy2(temp_output_path, final_output_path)
                            ram_success = True
                except Exception as ram_error:
                    print(f"Lỗi khi xử lý trong RAM: {ram_error}")
                    
                # Nếu xử lý trong RAM thành công
                if ram_success and os.path.exists(final_output_path):
                    print(f"Video đã được lưu tới: {final_output_path}")
                    
                    # Rename file gốc sau khi xử lý thành công
                    new_source_path = os.path.join(os.path.dirname(file_path), sanitize_filename(source_name))
                    os.rename(file_path, new_source_path)
                    print(f"Đã đổi tên file gốc thành: {source_name}")
                    
                    # Ghi log
                    log_processed_file(log_file, original_filename, os.path.basename(new_source_path))
                    return True
                else:
                    print("Xử lý trong RAM thất bại. Chuyển sang xử lý trực tiếp trên ổ đĩa...")
            else:
                print(f"Không đủ RAM để xử lý ({available_ram:.2f}GB < {ram_required:.2f}GB). Xử lý trực tiếp trên ổ đĩa.")
            
            # Nếu không đủ RAM hoặc xử lý trong RAM thất bại, xử lý trực tiếp trên ổ đĩa
            print("Xử lý video trực tiếp trên ổ đĩa...")
            cmd = [
                'ffmpeg',
                '-i', file_path,
                '-map', '0:v',
                '-map', f'0:{selected_track[0]}',
                '-c', 'copy',
                '-y',
                final_output_path
            ]
            
            print(f"Đang chạy lệnh trên ổ đĩa: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(final_output_path):
                print(f"Video đã được lưu thành công tới: {final_output_path}")
                
                # Rename file gốc sau khi xử lý thành công
                new_source_path = os.path.join(os.path.dirname(file_path), sanitize_filename(source_name))
                os.rename(file_path, new_source_path)
                print(f"Đã đổi tên file gốc thành: {source_name}")
                
                # Ghi log
                log_processed_file(log_file, original_filename, os.path.basename(new_source_path))
                return True
            else:
                print(f"Xử lý thất bại: {file_path}")
                if result.stderr:
                    stderr_text = result.stderr.decode('utf-8', errors='replace')
                    print(f"Lỗi: {stderr_text}")
                return False
        else:
            print(f"Không tìm thấy audio trong {file_path}")
            return False
            
    except Exception as e:
        print(f"Lỗi khi xử lý {file_path}: {e}")
        return False

def extract_subtitle(file_path, subtitle_info, log_file, probe_data):
    """Trích xuất subtitle tiếng Việt từ file video."""
    try:
        # Tạo thư mục ./Subtitles nếu chưa tồn tại
        sub_root_folder = os.path.join(".", "Subtitles")
        create_folder(sub_root_folder)
        
        index, language, title, codec = subtitle_info
        
        # Chỉ xử lý subtitle và định dạng text-based
        text_based_codecs = ['srt', 'ass', 'ssa', 'subrip']
        if codec.lower() not in text_based_codecs:
            print(f"Bỏ qua subtitle: định dạng {codec} không được hỗ trợ (chỉ hỗ trợ text-based)")
            return False
            
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Rút gọn tên file nếu quá dài
        if len(base_name) > 100:
            base_name = base_name[:100]
        
        # Đặt tên file subtitle giữ nguyên tên gốc và thêm mã ngôn ngữ
        sub_filename = sanitize_filename(f"{base_name}_{language}.srt")
        final_output_path = os.path.join(sub_root_folder, sub_filename)
        
        # Kiểm tra nếu subtitle đã tồn tại
        if os.path.exists(final_output_path):
            print(f"Subtitle đã tồn tại: {final_output_path}. Bỏ qua.")
            return True
        
        # Kiểm tra RAM khả dụng - subtitle thường nhỏ nên yêu cầu ít RAM hơn
        available_ram = check_available_ram()
        print(f"Xử lý subtitle với {available_ram:.2f} GB RAM khả dụng")
        
        # Ưu tiên xử lý trong RAM nếu có đủ RAM (>= 0.5GB)
        try_ram_first = available_ram >= 0.5
        
        if try_ram_first:
            print(f"Thử trích xuất subtitle trong RAM...")
            
            # Xử lý trong RAM
            ram_success = False
            try:
                with temp_directory_in_memory(use_ram=True) as temp_dir:
                    # Đường dẫn tạm thời trong RAM
                    temp_output_path = os.path.join(temp_dir, sub_filename)
                    
                    # Lệnh ffmpeg để trích xuất subtitle vào RAM
                    cmd = [
                        'ffmpeg',
                        '-i', file_path,
                        '-map', f'0:{index}',
                        '-c:s', 'srt',
                        '-y',
                        temp_output_path
                    ]
                    
                    print(f"Đang chạy lệnh trong RAM: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True)
                    
                    if result.returncode == 0 and os.path.exists(temp_output_path):
                        print(f"Trích xuất trong RAM thành công. Di chuyển file tới: {final_output_path}")
                        # Chuyển từ RAM sang ổ đĩa
                        shutil.copy2(temp_output_path, final_output_path)
                        ram_success = True
            except Exception as ram_error:
                print(f"Lỗi khi xử lý trong RAM: {ram_error}")
                
            # Nếu xử lý trong RAM thành công
            if ram_success and os.path.exists(final_output_path):
                print(f"Subtitle đã được lưu thành công tới: {final_output_path}")
                
                # Ghi vào log
                log_processed_file(log_file, os.path.basename(file_path), sub_filename)
                return True
            else:
                print("Xử lý trong RAM thất bại. Chuyển sang xử lý trực tiếp trên ổ đĩa...")
        else:
            print(f"Không đủ RAM để xử lý. Xử lý trực tiếp trên ổ đĩa.")
        
        # Xử lý trực tiếp vào thư mục đích nếu không thể xử lý trong RAM
        print(f"Trích xuất subtitle trực tiếp vào: {final_output_path}")
        
        # Lệnh ffmpeg để trích xuất subtitle
        cmd = [
            'ffmpeg',
            '-i', file_path,
            '-map', f'0:{index}',
            '-c:s', 'srt',
            '-y',
            final_output_path
        ]
        
        print(f"Đang chạy lệnh trên ổ đĩa: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True)
        
        if result.returncode == 0 and os.path.exists(final_output_path):
            print(f"Subtitle đã được trích xuất thành công: {final_output_path}")
            
            # Ghi vào log
            log_processed_file(log_file, os.path.basename(file_path), sub_filename)
            return True
        else:
            print("Lỗi khi trích xuất subtitle trực tiếp")
            if result.stderr:
                stderr_text = result.stderr.decode('utf-8', errors='replace')
                print(f"Lỗi: {stderr_text}")
            
            # Thử phương pháp khác nếu cách trên thất bại
            print("Thử phương pháp thay thế để trích xuất subtitle...")
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_output_path = os.path.join(temp_dir, sub_filename)
                
                alt_cmd = [
                    'ffmpeg',
                    '-i', file_path,
                    '-map', f'0:{index}',
                    '-f', 'srt',
                    '-y',
                    temp_output_path
                ]
                
                print(f"Đang chạy lệnh thay thế: {' '.join(alt_cmd)}")
                alt_result = subprocess.run(alt_cmd, capture_output=True)
                
                if alt_result.returncode == 0 and os.path.exists(temp_output_path):
                    print(f"Subtitle được trích xuất tạm thời: {temp_output_path}")
                    # Di chuyển tới đường dẫn cuối cùng
                    shutil.move(temp_output_path, final_output_path)
                    print(f"Subtitle đã được di chuyển tới: {final_output_path}")
                    
                    # Ghi vào log
                    log_processed_file(log_file, os.path.basename(file_path), sub_filename)
                    return True
                else:
                    print("Không thể trích xuất subtitle bằng cả hai phương pháp")
                    if alt_result.stderr:
                        stderr_text = alt_result.stderr.decode('utf-8', errors='replace')
                        print(f"Lỗi: {stderr_text}")
                    return False
    except Exception as e:
        print(f"Lỗi khi trích xuất subtitle: {e}")
        return False

def get_subtitle_info(file_path):
    """Lấy thông tin về các track subtitle trong file video."""
    try:
        probe = ffmpeg.probe(file_path)
        subtitle_tracks = []
        for stream in probe['streams']:
            if stream['codec_type'] == 'subtitle':
                index = stream.get('index', -1)
                language = stream.get('tags', {}).get('language', 'und')
                title = stream.get('tags', {}).get('title', '')
                codec = stream.get('codec_name', '')
                
                # Thêm thông tin về codec_type vào log
                print(f"Found subtitle track: index={index}, language={language}, codec={codec}")
                
                # Thêm vào danh sách các subtitle cần xử lý
                subtitle_tracks.append((index, language, title, codec))
        return subtitle_tracks
    except Exception as e:
        print(f"Lỗi khi lấy thông tin subtitle từ {file_path}: {e}")
        return []

def get_file_signature(file_path):
    """Lấy chữ ký của file (size và duration) để nhận diện file trùng."""
    try:
        file_size = os.path.getsize(file_path)
        probe = ffmpeg.probe(file_path)
        duration = probe.get('format', {}).get('duration', '0')
        return f"{file_size}_{duration}"
    except Exception as e:
        print(f"Error getting file signature: {e}")
        return None

def check_ffmpeg_available():
    """Kiểm tra FFmpeg có sẵn trong hệ thống"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: FFmpeg is not installed or not found in PATH")
        return False

def check_available_ram():
    """Kiểm tra lượng RAM còn trống trong hệ thống."""
    try:
        memory = psutil.virtual_memory()
        free_memory_gb = memory.available / (1024 ** 3)  # Convert to GB
        print(f"RAM khả dụng: {free_memory_gb:.2f} GB")
        return free_memory_gb
    except Exception as e:
        print(f"Lỗi khi kiểm tra RAM: {e}")
        return 0

def get_file_size_gb(file_path):
    """Lấy kích thước file theo GB."""
    try:
        file_size = os.path.getsize(file_path)
        file_size_gb = file_size / (1024 ** 3)  # Convert to GB
        print(f"Kích thước file: {file_size_gb:.2f} GB")
        return file_size_gb
    except Exception as e:
        print(f"Lỗi khi lấy kích thước file: {e}")
        return 0

@contextmanager
def temp_directory_in_memory(use_ram=True):
    """Tạo thư mục tạm trong RAM hoặc trên đĩa tùy thuộc vào tham số use_ram."""
    if use_ram:
        # Tạo thư mục tạm trong /dev/shm nếu có (Linux) hoặc sử dụng tempfile (macOS, Windows)
        if os.path.exists('/dev/shm') and os.access('/dev/shm', os.W_OK):
            # Kiểm tra không gian trống trong /dev/shm
            try:
                shm_usage = shutil.disk_usage('/dev/shm')
                shm_free_gb = shm_usage.free / (1024**3)
                print(f"Dung lượng trống trong /dev/shm: {shm_free_gb:.2f} GB")
                
                # Nếu có ít nhất 1GB không gian trống thì dùng /dev/shm
                if shm_free_gb >= 1:
                    temp_dir = tempfile.mkdtemp(dir='/dev/shm')
                    print(f"Sử dụng RAM disk (/dev/shm) để tạo thư mục tạm: {temp_dir}")
                else:
                    print(f"Không đủ dung lượng trong /dev/shm (chỉ còn {shm_free_gb:.2f} GB). Sử dụng ổ đĩa thay thế.")
                    temp_dir = tempfile.mkdtemp()
            except Exception as e:
                print(f"Lỗi khi kiểm tra /dev/shm: {e}. Sử dụng ổ đĩa thay thế.")
                temp_dir = tempfile.mkdtemp()
        else:
            # macOS: thử sử dụng /private/tmp (thường nằm trong RAM)
            if os.path.exists('/private/tmp') and os.access('/private/tmp', os.W_OK) and platform.system() == 'Darwin':
                temp_dir = tempfile.mkdtemp(dir='/private/tmp')
                print(f"Sử dụng /private/tmp trên macOS để tạo thư mục tạm: {temp_dir}")
            else:
                # Sử dụng tempfile thông thường (trên ổ đĩa)
                temp_dir = tempfile.mkdtemp()
                print(f"Sử dụng thư mục tạm trên ổ đĩa: {temp_dir}")
        
        try:
            yield temp_dir
        finally:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    print(f"Đã xóa thư mục tạm: {temp_dir}")
            except Exception as e:
                print(f"Lỗi khi xóa thư mục tạm: {e}")
    else:
        # Sử dụng tempfile thông thường (trên đĩa)
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Tạo thư mục tạm trên đĩa: {temp_dir}")
            yield temp_dir

def main():
    if not check_ffmpeg_available():
        return
    input_folder = "."  # Folder hiện tại
    vn_folder = "Lồng Tiếng - Thuyết Minh"
    original_folder = "Original"
    log_file = os.path.join(".", "Subtitles", "processed_files.log")

    # Tạo các thư mục cần thiết
    create_folder(vn_folder)
    create_folder(original_folder)
    create_folder(os.path.join(".", "Subtitles"))

    # Kiểm tra dung lượng ổ đĩa
    try:
        disk_usage = shutil.disk_usage(".")
        total_gb = disk_usage.total / (1024**3)
        free_gb = disk_usage.free / (1024**3)
        used_gb = disk_usage.used / (1024**3)
        percent_free = (free_gb / total_gb) * 100
        
        print(f"=== THÔNG TIN HỆ THỐNG ===")
        print(f"Ổ đĩa:")
        print(f"  Tổng dung lượng: {total_gb:.2f} GB")
        print(f"  Đã sử dụng: {used_gb:.2f} GB")
        print(f"  Còn trống: {free_gb:.2f} GB ({percent_free:.1f}%)")
        
        if percent_free < 10:
            print("\nCẢNH BÁO: Ổ đĩa của bạn còn rất ít dung lượng trống. Có thể gặp lỗi khi xử lý file lớn.")
    except Exception as e:
        print(f"Không thể kiểm tra dung lượng ổ đĩa: {e}")

    # Kiểm tra và hiển thị thông tin về RAM
    available_ram = check_available_ram()
    print(f"\nRAM khả dụng: {available_ram:.2f} GB")
    
    # Kiểm tra không gian trong /dev/shm nếu có
    if os.path.exists('/dev/shm'):
        try:
            shm_usage = shutil.disk_usage('/dev/shm')
            shm_free_gb = shm_usage.free / (1024**3)
            shm_total_gb = shm_usage.total / (1024**3)
            print(f"RAM disk (/dev/shm): {shm_total_gb:.2f} GB, còn trống: {shm_free_gb:.2f} GB")
        except Exception as e:
            print(f"Không thể kiểm tra /dev/shm: {e}")
    
    # Cập nhật thông tin chiến lược xử lý
    print(f"\n=== CHIẾN LƯỢC XỬ LÝ ===")
    print(f"1. Ưu tiên xử lý trong RAM để tối ưu tốc độ")
    print(f"2. Nếu có đủ RAM (200% kích thước file), sẽ xử lý trong RAM")
    print(f"3. Nếu xử lý trong RAM thất bại, sẽ tự động chuyển sang xử lý trên ổ đĩa")
    print(f"4. Trích xuất subtitle trực tiếp vào thư mục đích")
    print(f"======================\n")

    # Đọc danh sách file đã xử lý
    processed_files, processed_signatures = read_processed_files(log_file)

    try:
        mkv_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".mkv")]
        if not mkv_files:
            print("Không tìm thấy file MKV nào trong thư mục hiện tại.")
            return

        for mkv_file in mkv_files:
            file_path = os.path.join(input_folder, mkv_file)
            print(f"\n===== ĐANG XỬ LÝ FILE: {file_path} =====")
            
            # Hiển thị kích thước file
            file_size = get_file_size_gb(file_path)
            
            # Kiểm tra file đã xử lý bằng tên và signature
            file_signature = get_file_signature(file_path)
            if mkv_file in processed_files:
                print(f"File {mkv_file} đã được xử lý thành {processed_files[mkv_file]['new_name']} vào {processed_files[mkv_file]['time']}. Bỏ qua.")
                continue
            elif file_signature and file_signature in processed_signatures:
                print(f"File {mkv_file} có cùng nội dung với file đã xử lý {processed_signatures[file_signature]['new_name']}. Bỏ qua.")
                continue

            # Kiểm tra dung lượng trống trước khi xử lý
            try:
                disk_usage = shutil.disk_usage(".")
                free_gb = disk_usage.free / (1024**3)
                if free_gb < file_size * 1.5:
                    print(f"CẢNH BÁO: Không đủ dung lượng trống trên ổ đĩa để xử lý an toàn. Cần ít nhất {file_size * 1.5:.2f} GB, hiện có {free_gb:.2f} GB")
                    response = input("Bạn có muốn tiếp tục mặc dù có thể gặp lỗi? (y/n): ")
                    if response.lower() != 'y':
                        print("Bỏ qua file này.")
                        continue
            except Exception as e:
                print(f"Không thể kiểm tra dung lượng ổ đĩa: {e}")

            # Đọc thông tin file một lần duy nhất
            try:
                probe_data = ffmpeg.probe(file_path)
                audio_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'audio']
                subtitle_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'subtitle']
                
                # In thông tin streams để người dùng biết
                print("\nThông tin streams:")
                print("- Video streams:")
                for i, stream in enumerate([s for s in probe_data['streams'] if s['codec_type'] == 'video']):
                    width = stream.get('width', 'N/A')
                    height = stream.get('height', 'N/A')
                    codec = stream.get('codec_name', 'N/A')
                    print(f"  Stream #{i}: {codec}, {width}x{height}")
                
                print("- Audio streams:")
                for i, stream in enumerate(audio_streams):
                    lang = stream.get('tags', {}).get('language', 'und')
                    title = stream.get('tags', {}).get('title', '')
                    channels = stream.get('channels', 'N/A')
                    codec = stream.get('codec_name', 'N/A')
                    lang_display = f"{get_language_abbreviation(lang)}"
                    if title:
                        lang_display += f" - {title}"
                    print(f"  Stream #{stream.get('index', i)}: {codec}, {channels} channels, {lang_display}")
                
                print("- Subtitle streams:")
                for i, stream in enumerate(subtitle_streams):
                    lang = stream.get('tags', {}).get('language', 'und')
                    title = stream.get('tags', {}).get('title', '')
                    codec = stream.get('codec_name', 'N/A')
                    lang_display = f"{get_language_abbreviation(lang)}"
                    if title:
                        lang_display += f" - {title}"
                    print(f"  Stream #{stream.get('index', i)}: {codec}, {lang_display}")
                
            except Exception as e:
                print(f"Lỗi khi đọc thông tin file {file_path}: {e}")
                # Nếu không thể đọc thông tin file, vẫn thử rename đơn giản
                try:
                    new_path = rename_simple(file_path)
                    log_processed_file(log_file, mkv_file, os.path.basename(new_path))
                except Exception as rename_err:
                    print(f"Không thể đổi tên: {rename_err}")
                continue 

            # Kiểm tra subtitle và audio tiếng Việt
            has_vie_subtitle = any(stream.get('tags', {}).get('language', 'und') == 'vie' 
                                 for stream in subtitle_streams)
            has_vie_audio = any(stream.get('tags', {}).get('language', 'und') == 'vie' 
                               for stream in audio_streams)

            processed = False  # Flag để đánh dấu file đã được xử lý

            # Xử lý subtitle tiếng Việt
            vie_subtitle_streams = [stream for stream in subtitle_streams
                                    if stream.get('tags', {}).get('language', 'und') == 'vie']
            if vie_subtitle_streams:
                print(f"\nPhát hiện {len(vie_subtitle_streams)} subtitle tiếng Việt. Bắt đầu trích xuất...")
                for stream in vie_subtitle_streams:
                    subtitle_info = (
                        stream['index'],
                        'vie',
                        stream.get('tags', {}).get('title', ''),
                        stream.get('codec_name', '')
                    )
                    extract_subtitle(file_path, subtitle_info, log_file, probe_data)

            # Xử lý video nếu có audio tiếng Việt
            if has_vie_audio:
                try:
                    print("\nPhát hiện audio tiếng Việt. Bắt đầu xử lý...")
                    # Tìm audio track tiếng Việt có nhiều kênh nhất
                    vie_audio_tracks = [(stream.get('index', i), stream.get('channels', 0), 'vie', 
                                      stream.get('tags', {}).get('title', 'VIE'))
                                      for i, stream in enumerate(audio_streams)
                                      if stream.get('tags', {}).get('language', 'und') == 'vie']
                    if vie_audio_tracks:
                        # Sắp xếp theo số kênh giảm dần
                        vie_audio_tracks.sort(key=lambda x: x[1], reverse=True)
                        selected_track = vie_audio_tracks[0]
                        print(f"Chọn track audio tiếng Việt index={selected_track[0]} với {selected_track[1]} kênh")
                        extract_video_with_audio(file_path, vn_folder, original_folder, log_file, probe_data)
                        processed = True  # Đánh dấu file đã được xử lý
                except Exception as e:
                    print(f"Lỗi khi xử lý audio: {e}")

            # Nếu không có cả subtitle và audio tiếng Việt HOẶC xử lý audio thất bại
            if (not has_vie_subtitle and not has_vie_audio) or not processed:
                print(f"\nKhông tìm thấy subtitle hoặc audio tiếng Việt hoặc xử lý thất bại. Chỉ đổi tên file...")
                try:
                    new_path = rename_simple(file_path)
                    log_processed_file(log_file, mkv_file, os.path.basename(new_path))
                except Exception as rename_err:
                    print(f"Không thể đổi tên: {rename_err}")

    except Exception as e:
        print(f"Lỗi khi truy cập thư mục '{input_folder}': {e}")

if __name__ == "__main__":
    main()