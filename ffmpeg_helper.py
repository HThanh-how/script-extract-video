"""
Helper để tìm và sử dụng FFmpeg - ưu tiên FFmpeg bundle local
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def get_bundle_dir():
    """Lấy thư mục chứa executable (khi chạy từ PyInstaller)"""
    if getattr(sys, 'frozen', False):
        # Chạy từ executable (PyInstaller)
        # PyInstaller tạo thư mục _MEIPASS tạm thời
        if hasattr(sys, '_MEIPASS'):
            # Khi chạy từ PyInstaller, data files được extract vào _MEIPASS
            return Path(sys._MEIPASS)
        else:
            # Fallback: thư mục chứa executable
            return Path(sys.executable).parent
    else:
        # Chạy từ source code
        return Path(__file__).parent


def find_ffmpeg_binary():
    """Tìm FFmpeg binary - ưu tiên bundle local"""
    bundle_dir = get_bundle_dir()
    system = platform.system()
    
    # Tên file FFmpeg theo OS
    if system == "Windows":
        ffmpeg_name = "ffmpeg.exe"
        ffprobe_name = "ffprobe.exe"
    else:
        ffmpeg_name = "ffmpeg"
        ffprobe_name = "ffprobe"
    
    # 1. Tìm trong thư mục bundle/ffmpeg_bin
    local_ffmpeg = bundle_dir / "ffmpeg_bin" / ffmpeg_name
    if local_ffmpeg.exists():
        return str(local_ffmpeg.absolute())
    
    # 2. Tìm trong thư mục bundle (cùng thư mục với exe)
    local_ffmpeg = bundle_dir / ffmpeg_name
    if local_ffmpeg.exists():
        return str(local_ffmpeg.absolute())
    
    # 3. Tìm trong PATH (system FFmpeg)
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            check=True
        )
        return 'ffmpeg'  # Sử dụng system FFmpeg
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return None


def find_ffprobe_binary():
    """Tìm FFprobe binary - ưu tiên bundle local"""
    bundle_dir = get_bundle_dir()
    system = platform.system()
    
    if system == "Windows":
        ffprobe_name = "ffprobe.exe"
    else:
        ffprobe_name = "ffprobe"
    
    # 1. Tìm trong thư mục bundle/ffmpeg_bin
    local_ffprobe = bundle_dir / "ffmpeg_bin" / ffprobe_name
    if local_ffprobe.exists():
        return str(local_ffprobe.absolute())
    
    # 2. Tìm trong thư mục bundle
    local_ffprobe = bundle_dir / ffprobe_name
    if local_ffprobe.exists():
        return str(local_ffprobe.absolute())
    
    # 3. Tìm trong PATH
    try:
        result = subprocess.run(
            ['ffprobe', '-version'],
            capture_output=True,
            check=True
        )
        return 'ffprobe'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return None


def check_ffmpeg_available():
    """Kiểm tra FFmpeg có sẵn - sử dụng local nếu có"""
    ffmpeg_path = find_ffmpeg_binary()
    if ffmpeg_path is None:
        return False
    
    try:
        subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_ffmpeg_command(cmd):
    """Thay thế 'ffmpeg' trong command bằng path thực tế"""
    ffmpeg_path = find_ffmpeg_binary()
    if ffmpeg_path is None:
        return cmd  # Fallback về command gốc
    
    # Thay thế 'ffmpeg' và 'ffprobe' trong command
    if isinstance(cmd, list):
        new_cmd = []
        for arg in cmd:
            if arg == 'ffmpeg':
                new_cmd.append(ffmpeg_path)
            elif arg == 'ffprobe':
                ffprobe_path = find_ffprobe_binary()
                if ffprobe_path:
                    new_cmd.append(ffprobe_path)
                else:
                    new_cmd.append(arg)
            else:
                new_cmd.append(arg)
        return new_cmd
    elif isinstance(cmd, str):
        return cmd.replace('ffmpeg', ffmpeg_path).replace('ffprobe', find_ffprobe_binary() or 'ffprobe')
    
    return cmd

