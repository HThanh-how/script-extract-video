"""
Script build để đóng gói ứng dụng thành executable
Hỗ trợ Windows, macOS, và Linux
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def get_platform_spec():
    """Lấy thông tin platform"""
    system = platform.system()
    machine = platform.machine()
    
    if system == "Windows":
        return "win", "exe"
    elif system == "Darwin":
        return "mac", "app" if machine == "arm64" else "app"
    elif system == "Linux":
        return "linux", "bin"
    else:
        return "unknown", "bin"


def check_pyinstaller():
    """Kiểm tra PyInstaller đã được cài đặt chưa"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_dependencies():
    """Cài đặt dependencies"""
    print("📦 Đang cài đặt dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Đã cài đặt dependencies thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt dependencies: {e}")
        return False


def build_executable():
    """Build executable với PyInstaller"""
    platform_name, ext = get_platform_spec()
    
    print(f"\n🔨 Bắt đầu build cho {platform_name}...")
    print(f"   Output format: {ext}\n")
    
    # Tên file output
    output_name = "MKVProcessor"
    
    # Tùy chọn PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--name", output_name,
        "--onefile",  # Đóng gói thành 1 file duy nhất
        "--windowed",  # Không hiện console (cho GUI)
        "--icon=NONE",  # Có thể thêm icon sau
        "--add-data", "script.py;." if platform_name == "win" else "script.py:.",
        "gui.py"
    ]
    
    # Thêm hidden imports nếu cần
    hidden_imports = [
        "ffmpeg",
        "psutil",
        "tkinter",
        "tkinter.ttk",
        "tkinter.filedialog",
        "tkinter.scrolledtext",
        "tkinter.messagebox"
    ]
    
    for imp in hidden_imports:
        pyinstaller_args.extend(["--hidden-import", imp])
    
    # Windows specific
    if platform_name == "win":
        pyinstaller_args.append("--console")  # Giữ console để debug
    
    # macOS specific
    if platform_name == "mac":
        pyinstaller_args.extend([
            "--osx-bundle-identifier", "com.mkvprocessor.app"
        ])
    
    try:
        print(f"Chạy lệnh: {' '.join(pyinstaller_args)}")
        subprocess.check_call(pyinstaller_args)
        print("\n✅ Build thành công!")
        
        # Hiển thị vị trí file output
        dist_path = Path("dist") / output_name
        if platform_name == "win":
            dist_path = dist_path.with_suffix(".exe")
        elif platform_name == "mac":
            dist_path = dist_path.with_suffix(".app")
        
        if dist_path.exists():
            size_mb = dist_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 File output: {dist_path.absolute()}")
            print(f"   Kích thước: {size_mb:.2f} MB")
            print(f"\n💡 Lưu ý: Để tạo package hoàn chỉnh (bao gồm FFmpeg), chạy:")
            print(f"   python build_complete.py")
        else:
            print(f"⚠️ Không tìm thấy file output tại {dist_path}")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Lỗi khi build: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Không tìm thấy PyInstaller. Vui lòng cài đặt:")
        print("   pip install pyinstaller")
        return False


def create_portable_package():
    """Tạo package portable với FFmpeg"""
    platform_name, ext = get_platform_spec()
    
    print("\n📦 Tạo package portable...")
    
    package_name = f"MKVProcessor_{platform_name}_{platform.machine()}"
    package_dir = Path("dist") / package_name
    
    # Tạo thư mục package
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    exe_name = "MKVProcessor"
    if platform_name == "win":
        exe_name += ".exe"
    elif platform_name == "mac":
        exe_name += ".app"
    
    exe_path = Path("dist") / exe_name
    if exe_path.exists():
        if platform_name == "mac":
            shutil.copytree(exe_path, package_dir / exe_name, dirs_exist_ok=True)
        else:
            shutil.copy2(exe_path, package_dir / exe_name)
        print(f"✅ Đã copy executable vào {package_dir}")
    else:
        print(f"⚠️ Không tìm thấy executable tại {exe_path}")
    
    # Tạo README cho package
    readme_content = f"""# MKV Processor Portable Package

## Hướng dẫn sử dụng

1. Giải nén package này
2. Chạy file {exe_name}
3. Chọn thư mục chứa file MKV và bắt đầu xử lý

## Yêu cầu

- FFmpeg cần được cài đặt trên hệ thống
- Windows: Tải từ https://ffmpeg.org/download.html
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg` hoặc `sudo dnf install ffmpeg`

## Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. FFmpeg đã được cài đặt và có trong PATH
2. Đủ dung lượng ổ đĩa để xử lý video
3. Đủ RAM (khuyến nghị >= 4GB)

Platform: {platform_name}
Architecture: {platform.machine()}
"""
    
    readme_path = package_dir / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ Đã tạo package tại: {package_dir.absolute()}")
    print(f"   Kích thước: {get_folder_size(package_dir) / (1024*1024):.2f} MB")


def get_folder_size(path):
    """Tính kích thước thư mục"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total += os.path.getsize(filepath)
    return total


def main():
    """Hàm main"""
    print("=" * 60)
    print("🔨 MKV Processor Build Script")
    print("=" * 60)
    
    # Kiểm tra platform
    platform_name, ext = get_platform_spec()
    print(f"\n🖥️  Platform: {platform_name}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Output format: {ext}\n")
    
    # Kiểm tra PyInstaller
    if not check_pyinstaller():
        print("⚠️ PyInstaller chưa được cài đặt.")
        response = input("Bạn có muốn cài đặt dependencies không? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                print("❌ Không thể cài đặt dependencies. Thoát.")
                return
        else:
            print("❌ Cần PyInstaller để build. Thoát.")
            return
    
    # Build
    if build_executable():
        # Tạo package portable
        response = input("\nBạn có muốn tạo package portable không? (y/n): ")
        if response.lower() == 'y':
            create_portable_package()
    
    print("\n" + "=" * 60)
    print("✅ Hoàn thành!")
    print("=" * 60)


if __name__ == "__main__":
    main()

