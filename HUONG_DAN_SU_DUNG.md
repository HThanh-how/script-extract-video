# 📦 Hướng dẫn Sử dụng Package Sau Khi Build

## 🎯 Sau khi build xong, bạn sẽ có:

### 📁 Thư mục output:
```
dist/
└── MKVProcessor_Portable_win_x64/    ← Đây là package bạn cần!
    ├── MKVProcessor.exe              ← ⭐ CHẠY FILE NÀY!
    ├── ffmpeg_bin/                    ← FFmpeg đã bundle
    │   ├── ffmpeg.exe
    │   └── ffprobe.exe
    └── README.txt                     ← Hướng dẫn
```

---

## 🚀 Cách sử dụng:

### Bước 1: Tìm thư mục package

Sau khi chạy `python build_complete.py`, package sẽ ở:
```
dist/MKVProcessor_Portable_[OS]_[ARCH]/
```

Ví dụ:
- Windows x64: `dist/MKVProcessor_Portable_win_x64/`
- macOS Intel: `dist/MKVProcessor_Portable_mac_x64/`
- macOS Apple Silicon: `dist/MKVProcessor_Portable_mac_arm64/`
- Linux x64: `dist/MKVProcessor_Portable_linux_x64/`

### Bước 2: Copy thư mục package

**Copy TOÀN BỘ thư mục** `MKVProcessor_Portable_*` ra nơi bạn muốn:
- Desktop
- USB
- Thư mục bất kỳ

**QUAN TRỌNG:** Phải copy CẢ THƯ MỤC, không chỉ file .exe!

### Bước 3: Chạy ứng dụng

#### Windows:
```
1. Mở thư mục MKVProcessor_Portable_win_x64
2. Double-click MKVProcessor.exe
3. XONG!
```

#### macOS:
```
1. Mở thư mục MKVProcessor_Portable_mac_*
2. Double-click MKVProcessor.app
3. XONG!
```

#### Linux:
```
1. Mở terminal trong thư mục MKVProcessor_Portable_linux_*
2. Chạy: ./MKVProcessor
3. Hoặc: chmod +x MKVProcessor && ./MKVProcessor
4. XONG!
```

---

## ✅ Kiểm tra package đúng:

Package đúng phải có:
- ✅ File executable (`.exe` / `.app` / không extension)
- ✅ Thư mục `ffmpeg_bin/` với FFmpeg bên trong
- ✅ File `README.txt`

**Nếu thiếu `ffmpeg_bin/` → Package không hoàn chỉnh!**

---

## 📤 Chia sẻ cho người khác:

### Cách 1: Nén thành ZIP
```
1. Right-click thư mục MKVProcessor_Portable_*
2. Send to → Compressed (zipped) folder
3. Chia sẻ file ZIP
```

### Cách 2: Upload lên cloud
- Google Drive
- Dropbox
- OneDrive
- Bất kỳ cloud storage nào

### Cách 3: GitHub Release (nếu dùng GitHub Actions)
- Tự động có sẵn trong Release
- Người dùng chỉ cần tải về

---

## 🎯 Sử dụng ứng dụng:

1. **Mở ứng dụng** → Giao diện GUI hiện ra
2. **Chọn thư mục** → Click "Chọn thư mục..." và chọn thư mục chứa file MKV
3. **Kiểm tra** → Xem trạng thái FFmpeg, RAM, số file MKV
4. **Bắt đầu** → Click "🚀 Bắt đầu xử lý"
5. **Xem tiến trình** → Theo dõi trong cửa sổ log
6. **Hoàn thành** → File đã được xử lý!

---

## 📂 Kết quả sau khi xử lý:

Trong thư mục bạn chọn sẽ có:

```
thư-mục-của-bạn/
├── video.mkv                    ← File gốc (đã đổi tên)
├── Lồng Tiếng - Thuyết Minh/    ← Video với audio tiếng Việt
│   └── 4K_VIE_DTS_2023_video.mkv
├── Original/                    ← Video với audio gốc
│   └── 4K_ENG_DTS_2023_video.mkv
└── Subtitles/                   ← Subtitle đã trích xuất
    ├── video_vie.srt
    └── processed_files.log
```

---

## ❓ FAQ:

**Q: Có thể xóa thư mục `ffmpeg_bin/` không?**  
A: ❌ KHÔNG! Ứng dụng cần FFmpeg để chạy.

**Q: Có thể di chuyển file .exe ra ngoài không?**  
A: ❌ KHÔNG! Phải giữ nguyên cấu trúc thư mục.

**Q: Package lớn bao nhiêu?**  
A: Khoảng 100-150MB (bao gồm Python + FFmpeg + dependencies).

**Q: Có cần cài Python không?**  
A: ❌ KHÔNG! Đã bundle sẵn trong executable.

**Q: Có cần cài FFmpeg không?**  
A: ❌ KHÔNG! Đã bundle trong thư mục `ffmpeg_bin/`.

---

## 💡 Tips:

1. **Giữ nguyên cấu trúc** - Đừng tách rời các file
2. **Copy cả thư mục** - Không chỉ copy file .exe
3. **Kiểm tra trước** - Đảm bảo có đủ file trước khi chia sẻ
4. **Test trên máy khác** - Đảm bảo package hoạt động

---

**🎉 Vậy là xong! Bạn đã có một app hoàn chỉnh, chỉ cần copy và chạy!**

