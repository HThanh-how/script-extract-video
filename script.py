import os
import sys
import subprocess
import platform

# Thiết lập và kích hoạt virtual environment, cài đặt các package cần thiết
if __name__ == '__main__' and not os.environ.get('VENV_ACTIVE'):
    venv_dir = os.path.join(os.getcwd(), 'venv')
    if not os.path.isdir(venv_dir):
        print('Tạo môi trường ảo trong venv...')
        try:
            # Kiểm tra nếu venv module được hỗ trợ
            try:
                import venv
                has_venv = True
            except ImportError:
                has_venv = False
            
            if has_venv:
                # Sử dụng venv module trực tiếp
                import venv
                venv.create(venv_dir, with_pip=True)
                print('Đã tạo môi trường ảo bằng venv module')
            else:
                # Sử dụng virtualenv nếu venv không khả dụng
                try:
                    # Kiểm tra nếu virtualenv đã được cài đặt
                    subprocess.check_call([sys.executable, '-m', 'pip', 'show', 'virtualenv'], 
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print('Đang cài đặt virtualenv...')
                    try:
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'virtualenv'])
                    except subprocess.CalledProcessError:
                        print('Không thể cài đặt virtualenv. Thử sử dụng --break-system-packages...')
                        try:
                            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'virtualenv', '--break-system-packages'])
                        except subprocess.CalledProcessError:
                            print('Không thể cài đặt virtualenv. Vui lòng cài đặt thủ công.')
                            sys.exit(1)
                
                # Tạo môi trường ảo với virtualenv
                print('Tạo môi trường ảo bằng virtualenv...')
                subprocess.check_call([sys.executable, '-m', 'virtualenv', venv_dir])
        except Exception as e:
            print(f'Lỗi khi tạo môi trường ảo: {e}')
            print('Cố gắng cài đặt các thư viện trực tiếp...')
            
            # Cố gắng cài đặt các gói trực tiếp nếu không thể tạo venv
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ffmpeg-python', 'psutil'])
                # Import và chạy script trực tiếp
                try:
                    import ffmpeg
                    import psutil
                    print('Đã cài đặt các gói cần thiết trực tiếp.')
                    # Thiết lập biến môi trường để tránh lặp
                    os.environ['VENV_ACTIVE'] = '1'
                    # Tiếp tục chạy script
                except ImportError as imp_err:
                    print(f'Vẫn không thể import các gói cần thiết: {imp_err}')
                    sys.exit(1)
            except subprocess.CalledProcessError:
                print('Thử cài đặt với --break-system-packages...')
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ffmpeg-python', 'psutil', '--break-system-packages'])
                    # Import và chạy script trực tiếp
                    try:
                        import ffmpeg
                        import psutil
                        print('Đã cài đặt các gói cần thiết trực tiếp với --break-system-packages.')
                        # Thiết lập biến môi trường để tránh lặp
                        os.environ['VENV_ACTIVE'] = '1'
                        # Tiếp tục chạy script
                    except ImportError as imp_err:
                        print(f'Vẫn không thể import các gói cần thiết: {imp_err}')
                        sys.exit(1)
                except subprocess.CalledProcessError:
                    print('Không thể cài đặt các gói cần thiết.')
                    print('Vui lòng thử cài đặt thủ công:')
                    print(f'{sys.executable} -m pip install ffmpeg-python psutil --user')
                    sys.exit(1)
    else:
        # Nếu venv đã tồn tại
        print(f'Môi trường ảo {venv_dir} đã tồn tại.')
    
    # Xác định đường dẫn python và pip trong môi trường ảo
    is_windows = platform.system() == 'Windows'
    bin_dir = 'Scripts' if is_windows else 'bin'
    venv_python = os.path.join(venv_dir, bin_dir, 'python' + ('.exe' if is_windows else ''))
    venv_pip = os.path.join(venv_dir, bin_dir, 'pip' + ('.exe' if is_windows else ''))
    
    if not os.path.exists(venv_python):
        print(f'Không tìm thấy Python trong môi trường ảo: {venv_python}')
        print(f'Các tệp có trong thư mục: {os.listdir(os.path.join(venv_dir, bin_dir))}')
        sys.exit(1)
    
    try:
        print('Nâng cấp pip...')
        subprocess.check_call([venv_pip, 'install', '--upgrade', 'pip'])
        print('Cài đặt thư viện cần thiết...')
        subprocess.check_call([venv_pip, 'install', 'ffmpeg-python', 'psutil'])
        
        # Kiểm tra ffmpeg trên hệ thống
        ffmpeg_installed = False
        try:
            # Kiểm tra lệnh ffmpeg có sẵn không
            subprocess.check_call(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            ffmpeg_installed = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Kiểm tra ffmpeg qua snap
            try:
                subprocess.check_call(['snap', 'info', 'ffmpeg'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print('Phát hiện snap. Đang cài đặt ffmpeg thông qua snap...')
                subprocess.check_call(['snap', 'install', 'ffmpeg'])
                ffmpeg_installed = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print('CẢNH BÁO: FFmpeg chưa được cài đặt trên hệ thống.')
                print('Script này yêu cầu FFmpeg để xử lý video.')
                print('Vui lòng cài đặt FFmpeg thủ công:')
                print('- Trên Ubuntu: sudo apt install -y ffmpeg')
                print('- Sử dụng snap: sudo snap install ffmpeg')
                print('- Trên macOS: brew install ffmpeg')
                print('- Tải từ trang chủ: https://ffmpeg.org/download.html')
        
        if not ffmpeg_installed:
            print('\nCẢNH BÁO: Script có thể không hoạt động đúng nếu không có FFmpeg!')
            response = input("Bạn có muốn tiếp tục mà không có FFmpeg không? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
        
        # Thiết lập biến môi trường để tránh lặp
        new_env = os.environ.copy()
        new_env['VENV_ACTIVE'] = '1'
        print('Khởi động lại script với virtual environment...')
        os.execve(venv_python, [venv_python] + sys.argv, new_env)
    except Exception as e:
        print(f'Lỗi khi cài đặt các thư viện: {e}')
        print('Vui lòng thử chạy thủ công:')
        print(f'{venv_pip} install --upgrade pip')
        print(f'{venv_pip} install ffmpeg-python psutil')
        sys.exit(1)

# Import sau khi đã chắc chắn chạy trong venv
try:
    import ffmpeg
    import psutil
except ImportError as e:
    print(f"Lỗi khi import thư viện cần thiết: {e}")
    print("Vui lòng chắc chắn các thư viện đã được cài đặt đúng cách.")
    sys.exit(1)

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
            
            # Kiểm tra xem có đủ RAM để xử lý trong bộ nhớ không
            file_size = get_file_size_gb(file_path)
            available_ram = check_available_ram()
            use_ram = available_ram > (file_size + 5)  # Cần nhiều hơn kích thước file + 5GB
            
            if use_ram:
                print(f"Đủ RAM để xử lý file trong bộ nhớ ({available_ram:.2f}GB > {file_size + 5:.2f}GB)")
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
                    
                    result = subprocess.run(cmd, capture_output=True)
                    
                    if result.returncode == 0 and os.path.exists(temp_output_path):
                        print(f"Video được tạo tạm thời trong RAM: {temp_output_path}")
                        # Chuyển từ RAM sang ổ đĩa
                        shutil.copy2(temp_output_path, final_output_path)
                        print(f"Video đã được sao chép từ RAM sang ổ đĩa: {final_output_path}")
                        
                        # Rename file gốc sau khi xử lý thành công
                        new_source_path = os.path.join(os.path.dirname(file_path), sanitize_filename(source_name))
                        os.rename(file_path, new_source_path)
                        print(f"Renamed source file to: {source_name}")
                        
                        # Ghi log
                        log_processed_file(log_file, original_filename, os.path.basename(new_source_path))
                        return True
                    else:
                        print(f"Failed to process {file_path} in RAM.")
                        if result.stderr:
                            stderr_text = result.stderr.decode('utf-8', errors='replace')
                            print(f"Error: {stderr_text}")
                        return False
            else:
                print(f"Không đủ RAM để xử lý trong bộ nhớ ({available_ram:.2f}GB < {file_size + 5:.2f}GB). Xử lý trực tiếp trên ổ đĩa.")
                # Xử lý tách audio trực tiếp trên ổ đĩa
                cmd = [
                    'ffmpeg',
                    '-i', file_path,
                    '-map', '0:v',
                    '-map', f'0:{selected_track[0]}',
                    '-c', 'copy',
                    '-y',
                    final_output_path
                ]

                result = subprocess.run(cmd, capture_output=True)

                if result.returncode == 0 and os.path.exists(final_output_path):
                    print(f"Video saved to {final_output_path}.")
                    
                    # Rename file gốc sau khi xử lý thành công
                    new_source_path = os.path.join(os.path.dirname(file_path), sanitize_filename(source_name))
                    os.rename(file_path, new_source_path)
                    print(f"Renamed source file to: {source_name}")
                    
                    # Ghi log
                    log_processed_file(log_file, original_filename, os.path.basename(new_source_path))
                    return True
                else:
                    print(f"Failed to process {file_path}.")
                    if result.stderr:
                        stderr_text = result.stderr.decode('utf-8', errors='replace')
                        print(f"Error: {stderr_text}")
                    return False
        else:
            print(f"No audio found in {file_path}")
            return False
            
    except Exception as e:
        print(f"Exception while processing {file_path}: {e}")
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
            print(f"Skipping subtitle extraction: format {codec} is not supported (must be text-based).")
            return False
            
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Rút gọn tên file nếu quá dài
        if len(base_name) > 100:
            base_name = base_name[:100]
        
        # Đặt tên file subtitle giữ nguyên tên gốc và thêm mã ngôn ngữ
        sub_filename = sanitize_filename(f"{base_name}_{language}.srt")
        final_output_path = os.path.join(sub_root_folder, sub_filename)
        
        print(f"Xử lý subtitle trong bộ nhớ RAM...")
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
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(temp_output_path):
                print(f"Subtitle được trích xuất tạm thời trong RAM: {temp_output_path}")
                # Chuyển từ RAM sang ổ đĩa
                shutil.copy2(temp_output_path, final_output_path)
                print(f"Subtitle đã được sao chép từ RAM sang ổ đĩa: {final_output_path}")
                
                # Ghi vào log
                log_processed_file(log_file, os.path.basename(file_path), sub_filename)
                return True
            else:
                print("Lỗi khi trích xuất subtitle trong RAM")
                if result.stderr:
                    stderr_text = result.stderr.decode('utf-8', errors='replace')
                    print(f"Error: {stderr_text}")
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
            # Linux với /dev/shm (RAM disk)
            temp_dir = tempfile.mkdtemp(dir='/dev/shm')
        else:
            # macOS hoặc Windows (sử dụng tempfile thông thường)
            temp_dir = tempfile.mkdtemp()
        
        try:
            print(f"Tạo thư mục tạm trong RAM: {temp_dir}")
            yield temp_dir
        finally:
            try:
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

    create_folder(vn_folder)
    create_folder(original_folder)
    create_folder(os.path.join(".", "Subtitles"))

    # Kiểm tra và hiển thị thông tin về RAM
    available_ram = check_available_ram()
    print(f"Hệ thống có {available_ram:.2f} GB RAM khả dụng")
    print(f"Các file lớn hơn {available_ram - 5:.2f} GB sẽ được xử lý trực tiếp trên ổ đĩa")
    print(f"Các file nhỏ hơn sẽ được xử lý trong RAM để tăng tốc độ")
    print(f"Tất cả subtitle sẽ được xử lý trong RAM bất kể kích thước file")

    # Đọc danh sách file đã xử lý
    processed_files, processed_signatures = read_processed_files(log_file)

    try:
        mkv_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".mkv")]
        if not mkv_files:
            print("No MKV files found in the folder.")
            return

        for mkv_file in mkv_files:
            file_path = os.path.join(input_folder, mkv_file)
            print(f"Processing file: {file_path}")
            
            # Hiển thị kích thước file
            file_size = get_file_size_gb(file_path)
            print(f"Kích thước file: {file_size:.2f} GB")

            # Kiểm tra file đã xử lý bằng tên và signature
            file_signature = get_file_signature(file_path)
            if mkv_file in processed_files:
                print(f"File {mkv_file} was processed as {processed_files[mkv_file]['new_name']} on {processed_files[mkv_file]['time']}. Skipping.")
                continue
            elif file_signature and file_signature in processed_signatures:
                print(f"File {mkv_file} has same content as processed file {processed_signatures[file_signature]['new_name']}. Skipping.")
                continue

            # Đọc thông tin file một lần duy nhất
            try:
                probe_data = ffmpeg.probe(file_path)
                audio_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'audio']
                subtitle_streams = [stream for stream in probe_data['streams'] if stream['codec_type'] == 'subtitle']
            except Exception as e:
                print(f"Error probing file {file_path}: {e}")
                # Nếu không thể đọc thông tin file, vẫn thử rename đơn giản
                try:
                    new_path = rename_simple(file_path)
                    log_processed_file(log_file, mkv_file, os.path.basename(new_path))
                except Exception as rename_err:
                    print(f"Failed to rename: {rename_err}")
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
                print(f"Phát hiện {len(vie_subtitle_streams)} subtitle tiếng Việt. Bắt đầu trích xuất trong RAM...")
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
                    print("Phát hiện audio tiếng Việt. Bắt đầu xử lý...")
                    # Tìm audio track tiếng Việt có nhiều kênh nhất
                    vie_audio_tracks = [(i, stream.get('channels', 0), 'vie', 
                                      stream.get('tags', {}).get('title', 'VIE'))
                                      for i, stream in enumerate(audio_streams)
                                      if stream.get('tags', {}).get('language', 'und') == 'vie']
                    if vie_audio_tracks:
                        # Sắp xếp theo số kênh giảm dần
                        vie_audio_tracks.sort(key=lambda x: x[1], reverse=True)
                        selected_track = vie_audio_tracks[0]
                        extract_video_with_audio(file_path, vn_folder, original_folder, log_file, probe_data)
                        processed = True  # Đánh dấu file đã được xử lý
                except Exception as e:
                    print(f"Error processing audio: {e}")

            # Nếu không có cả subtitle và audio tiếng Việt HOẶC xử lý audio thất bại
            if (not has_vie_subtitle and not has_vie_audio) or not processed:
                print(f"No Vietnamese subtitle and audio found or processing failed. Renaming file...")
                try:
                    new_path = rename_simple(file_path)
                    log_processed_file(log_file, mkv_file, os.path.basename(new_path))
                except Exception as rename_err:
                    print(f"Failed to rename: {rename_err}")

    except Exception as e:
        print(f"Error accessing input folder '{input_folder}': {e}")

if __name__ == "__main__":
    main()