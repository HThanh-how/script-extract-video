# 🎬 MKV Video Processing Toolkit - GUI Version

## ✨ Tính năng mới

### 🖥️ Giao diện đồ họa (GUI)
- **Không cần command line** - Sử dụng giao diện trực quan, dễ dàng
- **Chọn thư mục bằng chuột** - Không cần gõ đường dẫn
- **Hiển thị tiến trình real-time** - Xem log xử lý trực tiếp
- **Kiểm tra dependencies tự động** - Hiển thị trạng thái FFmpeg, RAM

### 📦 Đóng gói thành Executable
- **Một file duy nhất** - Không cần cài Python
- **Hỗ trợ đa nền tảng** - Windows (.exe), macOS (.app), Linux (.bin)
- **Tự động phát hiện OS** - Build script tự động detect platform

## 🚀 Cài đặt nhanh

### Cách 1: Sử dụng Executable (Khuyến nghị)

1. **Tải executable** từ releases (hoặc tự build)
2. **Cài đặt FFmpeg** (chỉ cần 1 lần):
   - Windows: Chạy `download_ffmpeg.py` hoặc tải từ https://ffmpeg.org
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
3. **Chạy file executable** - Không cần cài gì thêm!

### Cách 2: Chạy từ source code

```bash
# 1. Clone repository
git clone <repo-url>
cd script-extract-video

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy GUI
python gui.py
```

## 🔨 Build Executable

### Tự động build cho platform hiện tại:

```bash
python build.py
```

Script sẽ:
- ✅ Tự động detect OS (Windows/macOS/Linux)
- ✅ Cài đặt PyInstaller nếu chưa có
- ✅ Build executable với tất cả dependencies
- ✅ Tạo package portable (tùy chọn)

### Build thủ công:

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build
pyinstaller --name MKVProcessor --onefile --windowed gui.py
```

File output sẽ ở trong thư mục `dist/`

## 📖 Hướng dẫn sử dụng GUI

### 1. Mở ứng dụng
- Chạy `MKVProcessor.exe` (Windows) hoặc `MKVProcessor.app` (macOS) hoặc `MKVProcessor` (Linux)
- Hoặc chạy `python gui.py` nếu dùng source code

### 2. Chọn thư mục
- Click nút **"Chọn thư mục..."**
- Chọn thư mục chứa file MKV cần xử lý
- Ứng dụng sẽ tự động đếm số file MKV

### 3. Kiểm tra hệ thống
- Xem trạng thái **FFmpeg**: Phải có ✅ (xanh)
- Xem trạng thái **RAM**: Đảm bảo đủ RAM
- Xem trạng thái **Thư mục**: Phải có file MKV

### 4. Bắt đầu xử lý
- Click nút **"🚀 Bắt đầu xử lý"**
- Xác nhận số file sẽ xử lý
- Xem tiến trình trong cửa sổ log

### 5. Xem kết quả
- File đã xử lý sẽ được:
  - Tách audio vào thư mục `Lồng Tiếng - Thuyết Minh` hoặc `Original`
  - Trích xuất subtitle vào thư mục `Subtitles`
  - Đổi tên file gốc theo format chuẩn

## 🛠️ Cài đặt FFmpeg tự động

### Windows:
```bash
python download_ffmpeg.py
```

Script sẽ tự động:
- Tải FFmpeg từ nguồn chính thức
- Giải nén vào thư mục `ffmpeg_bin`
- Hướng dẫn thêm vào PATH

### macOS/Linux:
```bash
python download_ffmpeg.py
```

Script sẽ hướng dẫn hoặc tự động cài qua Homebrew/apt/dnf

## 📁 Cấu trúc thư mục sau khi xử lý

```
thư-mục-của-bạn/
├── video.mkv                    # File gốc (đã đổi tên)
├── Lồng Tiếng - Thuyết Minh/    # Video với audio tiếng Việt
│   └── 4K_VIE_DTS_2023_video.mkv
├── Original/                    # Video với audio gốc
│   └── 4K_ENG_DTS_2023_video.mkv
└── Subtitles/                   # Subtitle đã trích xuất
    ├── video_vie.srt
    └── processed_files.log      # Log các file đã xử lý
```

## ⚙️ Yêu cầu hệ thống

### Tối thiểu:
- **RAM**: 4GB (khuyến nghị 8GB+)
- **Ổ đĩa**: Dung lượng trống >= 2x kích thước file video lớn nhất
- **FFmpeg**: Phiên bản mới nhất

### Hỗ trợ:
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, Fedora, etc.)

## 🐛 Xử lý lỗi

### Lỗi: "FFmpeg chưa được cài đặt"
**Giải pháp:**
1. Chạy `python download_ffmpeg.py` để tự động tải
2. Hoặc cài thủ công từ https://ffmpeg.org
3. Đảm bảo FFmpeg có trong PATH

### Lỗi: "Không tìm thấy file MKV"
**Giải pháp:**
- Kiểm tra lại thư mục đã chọn
- Đảm bảo file có extension `.mkv`

### Lỗi: "Không đủ dung lượng ổ đĩa"
**Giải pháp:**
- Xóa file không cần thiết
- Cần ít nhất 2x kích thước file video lớn nhất

### Lỗi: "Thiếu thư viện Python"
**Giải pháp:**
```bash
pip install -r requirements.txt
```

## 📝 So sánh: Command Line vs GUI

| Tính năng | Command Line | GUI |
|-----------|-------------|-----|
| Dễ sử dụng | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Hiển thị tiến trình | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Chọn thư mục | ⭐ | ⭐⭐⭐⭐⭐ |
| Kiểm tra dependencies | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Phù hợp người mới | ❌ | ✅ |

## 🎯 Lợi ích của Executable

1. **Không cần cài Python** - Chạy trực tiếp
2. **Không cần cài dependencies** - Đã đóng gói sẵn
3. **Dễ phân phối** - Chỉ cần 1 file
4. **Tự động detect OS** - Không cần setup khác nhau

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra log trong cửa sổ GUI
2. Xem file `Subtitles/processed_files.log`
3. Đảm bảo FFmpeg đã được cài đặt đúng

## 🔄 Cập nhật

Để cập nhật:
1. Tải version mới
2. Thay thế file executable cũ
3. Không cần cài đặt lại

---

**Made with ❤️ for easy video processing**

