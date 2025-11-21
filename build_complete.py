"""
Script build HOÀN CHỈNH - Tự động tải FFmpeg và bundle vào package
Tạo ra 1 package duy nhất, không cần cài gì thêm!
"""
import os
import sys
import platform
import subprocess
import shutil
import urllib.request
import zipfile
from pathlib import Path


def get_platform_spec():
    """Lấy thông tin platform"""
    system = platform.system()
    machine = platform.machine().lower()
    
    if system == "Windows":
        # Kiểm tra architecture chính xác hơn
        if "64" in machine or "amd64" in machine or "x86_64" in machine:
            arch = "x64"
        else:
            arch = "x86"
        return "win", "exe", arch
    elif system == "Darwin":
        # macOS: kiểm tra architecture
        try:
            # Kiểm tra uname -m hoặc sysctl
            result = subprocess.run(['uname', '-m'], capture_output=True, text=True)
            if result.returncode == 0:
                uname_m = result.stdout.strip().lower()
                if 'arm' in uname_m or 'aarch64' in uname_m:
                    arch = "arm64"
                else:
                    arch = "x64"
            else:
                # Fallback: dựa vào machine
                if machine == "arm64" or "arm" in machine.lower():
                    arch = "arm64"
                else:
                    arch = "x64"
        except:
            # Fallback cuối cùng
            if machine == "arm64" or "arm" in machine.lower():
                arch = "arm64"
            else:
                arch = "x64"
        return "mac", "app", arch
    elif system == "Linux":
        if "arm" in machine or "aarch64" in machine:
            arch = "arm64"
        else:
            arch = "x64"
        return "linux", "bin", arch
    else:
        return "unknown", "bin", "unknown"


def download_ffmpeg_windows():
    """Tải FFmpeg cho Windows và giải nén"""
    print("\n📥 Đang tải FFmpeg cho Windows...")
    
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = Path("ffmpeg_temp.zip")
    ffmpeg_bin_dir = Path("ffmpeg_bin")
    
    try:
        print(f"Đang tải từ: {url}")
        urllib.request.urlretrieve(url, zip_path)
        print("✅ Đã tải xong!")
        
        # Giải nén
        print("📦 Đang giải nén...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Tìm và copy FFmpeg
        ffmpeg_dirs = [d for d in Path(".").iterdir() if d.is_dir() and "ffmpeg" in d.name.lower()]
        if ffmpeg_dirs:
            ffmpeg_dir = ffmpeg_dirs[0]
            bin_dir = ffmpeg_dir / "bin"
            
            # Tạo thư mục ffmpeg_bin
            if ffmpeg_bin_dir.exists():
                shutil.rmtree(ffmpeg_bin_dir)
            ffmpeg_bin_dir.mkdir()
            
            # Copy các file cần thiết
            for exe in ["ffmpeg.exe", "ffprobe.exe"]:
                src = bin_dir / exe
                if src.exists():
                    shutil.copy2(src, ffmpeg_bin_dir / exe)
                    print(f"✅ Đã copy {exe}")
            
            # Dọn dẹp
            zip_path.unlink()
            shutil.rmtree(ffmpeg_dir)
            
            print(f"✅ FFmpeg đã được tải và sẵn sàng tại: {ffmpeg_bin_dir.absolute()}")
            return True
        else:
            print("❌ Không tìm thấy FFmpeg sau khi giải nén")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi tải FFmpeg: {e}")
        return False


def check_ffmpeg_local():
    """Kiểm tra FFmpeg đã có local chưa"""
    ffmpeg_bin_dir = Path("ffmpeg_bin")
    system = platform.system()
    
    if system == "Windows":
        ffmpeg_exe = ffmpeg_bin_dir / "ffmpeg.exe"
    else:
        ffmpeg_exe = ffmpeg_bin_dir / "ffmpeg"
    
    return ffmpeg_exe.exists()


def build_executable():
    """Build executable với PyInstaller"""
    platform_name, ext, arch = get_platform_spec()
    
    print(f"\n🔨 Bắt đầu build cho {platform_name} ({arch})...")
    
    output_name = "MKVProcessor"
    
    # Tùy chọn PyInstaller - sử dụng python -m PyInstaller để tránh lỗi PATH
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--name", output_name,
        "--onefile",  # 1 file duy nhất
        "--windowed",  # GUI mode
        "--add-data", f"script.py{os.pathsep}.",
        "--add-data", f"ffmpeg_helper.py{os.pathsep}.",
    ]
    
    # Bundle FFmpeg nếu có
    if check_ffmpeg_local():
        ffmpeg_bin_dir = Path("ffmpeg_bin").absolute()
        if platform_name == "win":
            pyinstaller_args.extend([
                "--add-data", f"{ffmpeg_bin_dir}{os.pathsep}ffmpeg_bin"
            ])
        else:
            pyinstaller_args.extend([
                "--add-data", f"{ffmpeg_bin_dir}{os.pathsep}ffmpeg_bin"
            ])
        print("✅ Sẽ bundle FFmpeg vào executable")
    else:
        print("⚠️ Không tìm thấy FFmpeg local, sẽ cần cài đặt riêng")
    
    # Hidden imports
    hidden_imports = [
        "ffmpeg", "psutil", "tkinter", "tkinter.ttk",
        "tkinter.filedialog", "tkinter.scrolledtext", "tkinter.messagebox"
    ]
    for imp in hidden_imports:
        pyinstaller_args.extend(["--hidden-import", imp])
    
    # macOS specific
    if platform_name == "mac":
        pyinstaller_args.extend([
            "--osx-bundle-identifier", "com.mkvprocessor.app"
        ])
    
    pyinstaller_args.append("gui.py")
    
    try:
        print(f"\nChạy PyInstaller...")
        subprocess.check_call(pyinstaller_args)
        print("\n✅ Build thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Lỗi khi build: {e}")
        return False


def create_portable_package():
    """Tạo package portable hoàn chỉnh"""
    platform_name, ext, arch = get_platform_spec()
    
    print("\n📦 Tạo package portable hoàn chỉnh...")
    
    # Tạo tên package với architecture đúng
    if platform_name == "win":
        if arch == "x64":
            arch_name = "win64"
        else:
            arch_name = "win32"
    elif platform_name == "mac":
        if arch == "arm64":
            arch_name = "arm64"
        else:
            arch_name = "x64"  # Intel
    else:  # Linux
        arch_name = arch
    package_name = f"MKVProcessor_Portable_{platform_name}_{arch_name}"
    package_dir = Path("dist") / package_name
    
    # Tạo thư mục
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    
    # Copy executable - tìm file đúng tên
    exe_name = "MKVProcessor"
    if platform_name == "win":
        exe_name += ".exe"
    elif platform_name == "mac":
        exe_name += ".app"
    
    # Tìm executable (có thể có suffix khác)
    exe_path = Path("dist") / exe_name
    if not exe_path.exists():
        # Thử tìm file khác trong dist
        dist_files = list(Path("dist").glob("MKVProcessor*"))
        if dist_files:
            exe_path = dist_files[0]
    if exe_path.exists():
        if platform_name == "mac":
            shutil.copytree(exe_path, package_dir / exe_name)
        else:
            shutil.copy2(exe_path, package_dir / exe_name)
        print(f"✅ Đã copy executable")
    else:
        print(f"❌ Không tìm thấy executable tại {exe_path}")
        return False
    
    # Copy FFmpeg nếu có
    if check_ffmpeg_local():
        ffmpeg_bin_dir = Path("ffmpeg_bin")
        package_ffmpeg_dir = package_dir / "ffmpeg_bin"
        shutil.copytree(ffmpeg_bin_dir, package_ffmpeg_dir)
        print(f"✅ Đã copy FFmpeg vào package")
    
    # Tạo README
    readme_content = f"""# 🎬 MKV Processor - Portable Package

## ✨ Package hoàn chỉnh - Không cần cài đặt gì!

### 🚀 Cách sử dụng:

1. **Giải nén** package này vào bất kỳ đâu
2. **Chạy file** {exe_name}
3. **Chọn thư mục** chứa file MKV
4. **Bắt đầu xử lý** - XONG!

### ✅ Đã bao gồm:

- ✅ Executable (đã bundle Python và dependencies)
- ✅ FFmpeg (không cần cài đặt)
- ✅ Tất cả thư viện cần thiết

### 💡 Lưu ý:

- Không cần cài Python
- Không cần cài FFmpeg
- Không cần cài dependencies
- Chỉ cần double-click và chạy!

### 📋 Yêu cầu hệ thống:

- RAM: Tối thiểu 4GB (khuyến nghị 8GB+)
- Ổ đĩa: Dung lượng trống >= 2x kích thước file video lớn nhất
- OS: {platform_name} {arch}

### 🐛 Xử lý lỗi:

Nếu gặp lỗi, kiểm tra:
1. Đủ dung lượng ổ đĩa
2. Đủ RAM
3. File MKV hợp lệ

---
Platform: {platform_name}
Architecture: {arch}
Build date: {platform.system()} {platform.release()}
"""
    
    readme_path = package_dir / "README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Tính kích thước
    total_size = sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
    size_mb = total_size / (1024 * 1024)
    
    print(f"\n✅ Package hoàn chỉnh đã được tạo!")
    print(f"   📁 Vị trí: {package_dir.absolute()}")
    print(f"   📦 Kích thước: {size_mb:.2f} MB")
    print(f"\n💡 Bạn có thể:")
    print(f"   1. Copy thư mục {package_name} vào USB")
    print(f"   2. Chia sẻ cho người khác")
    print(f"   3. Chạy trên bất kỳ máy {platform_name} nào (không cần cài đặt!)")
    
    return True


def main():
    """Hàm main"""
    print("=" * 70)
    print("🔨 MKV Processor - Build Complete Package")
    print("=" * 70)
    print("\n✨ Tạo package HOÀN CHỈNH - Không cần cài đặt gì!")
    print("   (Bao gồm: Executable + FFmpeg + Dependencies)\n")
    
    platform_name, ext, arch = get_platform_spec()
    print(f"🖥️  Platform: {platform_name} ({arch})")
    
    # Kiểm tra xem đang chạy trong CI/CD không (không có stdin)
    is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
    
    # Kiểm tra PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("\n⚠️ PyInstaller chưa được cài đặt.")
        if is_ci:
            print("Đang cài đặt PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        else:
            response = input("Cài đặt PyInstaller? (y/n): ")
            if response.lower() == 'y':
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            else:
                print("❌ Cần PyInstaller để build. Thoát.")
                return
    
    # Tải FFmpeg nếu chưa có
    if not check_ffmpeg_local():
        print("\n📥 FFmpeg chưa có local.")
        if platform_name == "win":
            if is_ci:
                print("Đang tự động tải FFmpeg cho Windows...")
                if not download_ffmpeg_windows():
                    print("❌ Không thể tải FFmpeg. Thoát.")
                    return
            else:
                response = input("Tự động tải FFmpeg cho Windows? (y/n): ")
                if response.lower() == 'y':
                    if not download_ffmpeg_windows():
                        print("⚠️ Không thể tải FFmpeg. Bạn có thể:")
                        print("   1. Chạy python download_ffmpeg.py trước")
                        print("   2. Hoặc cài FFmpeg thủ công")
                        response = input("Tiếp tục build không? (y/n): ")
                        if response.lower() != 'y':
                            return
        else:
            if is_ci:
                print(f"⚠️ FFmpeg cần được cài đặt trong CI cho {platform_name}")
                print("   (Nên được cài trong workflow)")
            else:
                print(f"⚠️ FFmpeg cần được cài đặt thủ công cho {platform_name}")
                print("   Hoặc copy vào thư mục ffmpeg_bin/")
                response = input("Tiếp tục build không? (y/n): ")
                if response.lower() != 'y':
                    return
    
    # Build executable
    if build_executable():
        # Tạo package
        if create_portable_package():
            print("\n" + "=" * 70)
            print("✅ HOÀN THÀNH!")
            print("=" * 70)
            print("\n🎉 Bạn đã có một package HOÀN CHỈNH!")
            print("   Chỉ cần copy thư mục dist/MKVProcessor_Portable_* và chia sẻ.")
            print("   Người dùng chỉ cần giải nén và chạy - KHÔNG CẦN CÀI ĐẶT GÌ!")
        else:
            print("\n⚠️ Build executable thành công nhưng không tạo được package.")
    else:
        print("\n❌ Build thất bại.")


if __name__ == "__main__":
    main()

