"""
Script test executable để kiểm tra xem có thiếu dependencies không
"""
import sys
import os
from pathlib import Path


def test_imports():
    """Test xem có import được các module không"""
    print("=" * 60)
    print("🧪 Test Import Dependencies")
    print("=" * 60)
    
    # Test ffmpeg
    try:
        import ffmpeg
        print("✅ ffmpeg: OK")
        print(f"   Location: {ffmpeg.__file__}")
    except ImportError as e:
        print(f"❌ ffmpeg: FAILED - {e}")
        return False
    
    # Test psutil
    try:
        import psutil
        print("✅ psutil: OK")
        print(f"   Location: {psutil.__file__}")
    except ImportError as e:
        print(f"❌ psutil: FAILED - {e}")
        return False
    
    # Test script
    try:
        from script import main
        print("✅ script: OK")
    except ImportError as e:
        print(f"❌ script: FAILED - {e}")
        return False
    
    # Test ffmpeg_helper
    try:
        from ffmpeg_helper import check_ffmpeg_available
        print("✅ ffmpeg_helper: OK")
    except ImportError as e:
        print(f"❌ ffmpeg_helper: FAILED - {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TẤT CẢ IMPORTS THÀNH CÔNG!")
    print("=" * 60)
    return True


def check_exe_size():
    """Kiểm tra kích thước file exe"""
    exe_path = Path("dist/MKVProcessor.exe")
    if not exe_path.exists():
        print("❌ Không tìm thấy MKVProcessor.exe trong dist/")
        return
    
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"\n📦 Kích thước file exe: {size_mb:.2f} MB")
    
    if size_mb < 30:
        print("⚠️ File quá nhỏ - có thể thiếu dependencies")
    elif size_mb > 200:
        print("⚠️ File quá lớn - có thể bundle thừa")
    else:
        print("✅ Kích thước hợp lý (30-200MB)")


if __name__ == "__main__":
    print("\n🔍 Kiểm tra Executable...\n")
    
    # Kiểm tra kích thước
    check_exe_size()
    
    # Test imports (chỉ khi chạy từ source, không phải exe)
    if not getattr(sys, 'frozen', False):
        print("\n" + "=" * 60)
        print("📝 Test imports từ source code...")
        print("=" * 60)
        test_imports()
    else:
        print("\n✅ Đang chạy từ executable - imports đã được bundle")
        print("   Nếu chạy được GUI → Build thành công!")

