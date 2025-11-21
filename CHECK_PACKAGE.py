"""
Script kiểm tra package sau khi build có đầy đủ không
"""
import os
from pathlib import Path


def check_package(package_dir):
    """Kiểm tra package có đầy đủ không"""
    package_path = Path(package_dir)
    
    if not package_path.exists():
        print(f"❌ Không tìm thấy thư mục: {package_dir}")
        return False
    
    print(f"📦 Kiểm tra package: {package_path.absolute()}\n")
    
    # Kiểm tra executable
    exe_found = False
    exe_files = []
    
    # Windows
    exe_file = package_path / "MKVProcessor.exe"
    if exe_file.exists():
        exe_found = True
        exe_files.append("MKVProcessor.exe")
    
    # macOS
    app_dir = package_path / "MKVProcessor.app"
    if app_dir.exists():
        exe_found = True
        exe_files.append("MKVProcessor.app")
    
    # Linux
    exe_file = package_path / "MKVProcessor"
    if exe_file.exists():
        exe_found = True
        exe_files.append("MKVProcessor")
    
    if exe_found:
        print(f"✅ Executable: {', '.join(exe_files)}")
    else:
        print("❌ Không tìm thấy executable!")
        return False
    
    # Kiểm tra FFmpeg
    ffmpeg_dir = package_path / "ffmpeg_bin"
    if ffmpeg_dir.exists():
        ffmpeg_files = list(ffmpeg_dir.glob("ffmpeg*"))
        if ffmpeg_files:
            print(f"✅ FFmpeg: {len(ffmpeg_files)} file(s) tìm thấy")
            for f in ffmpeg_files:
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"   - {f.name} ({size_mb:.2f} MB)")
        else:
            print("⚠️ Thư mục ffmpeg_bin/ rỗng!")
    else:
        print("❌ Không tìm thấy thư mục ffmpeg_bin/")
        print("   ⚠️ Package không hoàn chỉnh - thiếu FFmpeg!")
        return False
    
    # Kiểm tra README
    readme_file = package_path / "README.txt"
    if readme_file.exists():
        print("✅ README.txt")
    else:
        print("⚠️ Không có README.txt (không bắt buộc)")
    
    # Tính kích thước
    total_size = sum(f.stat().st_size for f in package_path.rglob('*') if f.is_file())
    size_mb = total_size / (1024 * 1024)
    print(f"\n📊 Tổng kích thước: {size_mb:.2f} MB")
    
    print("\n" + "=" * 60)
    if exe_found and ffmpeg_dir.exists():
        print("✅ PACKAGE HOÀN CHỈNH - Sẵn sàng sử dụng!")
        print("\n💡 Cách sử dụng:")
        print(f"   1. Copy toàn bộ thư mục: {package_path.name}")
        print(f"   2. Chạy file executable trong thư mục đó")
        print(f"   3. XONG!")
    else:
        print("❌ PACKAGE KHÔNG HOÀN CHỈNH!")
        print("   Vui lòng build lại với: python build_complete.py")
    print("=" * 60)
    
    return exe_found and ffmpeg_dir.exists()


def main():
    """Hàm main"""
    import sys
    
    # Tìm package trong dist/
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ Không tìm thấy thư mục dist/")
        print("   Vui lòng chạy: python build_complete.py")
        return
    
    # Tìm tất cả package
    packages = list(dist_dir.glob("MKVProcessor_Portable_*"))
    
    if not packages:
        print("❌ Không tìm thấy package nào trong dist/")
        print("   Vui lòng chạy: python build_complete.py")
        return
    
    if len(packages) == 1:
        check_package(packages[0])
    else:
        print(f"Tìm thấy {len(packages)} package(s):\n")
        for i, pkg in enumerate(packages, 1):
            print(f"{i}. {pkg.name}")
        
        if len(sys.argv) > 1:
            # Kiểm tra package được chỉ định
            pkg_name = sys.argv[1]
            pkg_path = dist_dir / pkg_name
            if pkg_path.exists():
                check_package(pkg_path)
            else:
                print(f"\n❌ Không tìm thấy: {pkg_name}")
        else:
            # Kiểm tra tất cả
            print("\n" + "=" * 60)
            for pkg in packages:
                check_package(pkg)
                print()


if __name__ == "__main__":
    main()

