# 🧪 Hướng dẫn Test Executable sau khi Build

## 🚀 Cách Test Tự Động

Sau khi build xong, chạy script test:

```bash
python test_build.py
```

Script này sẽ:
- ✅ Kiểm tra file executable có tồn tại không
- ✅ Kiểm tra kích thước file (có hợp lý không)
- ✅ Kiểm tra FFmpeg có được bundle không
- ✅ Test chạy executable (xem có lỗi khởi động không)
- ✅ Hướng dẫn test GUI thủ công

---

## 🖥️ Cách Test Thủ Công (Quan trọng!)

### Bước 1: Chạy Executable

```bash
# Windows
dist/MKVProcessor.exe

# Mac
dist/MKVProcessor.app

# Linux
dist/MKVProcessor
```

### Bước 2: Kiểm tra GUI

Khi GUI mở, kiểm tra:

1. **GUI có mở được không?**
   - ✅ Cửa sổ GUI hiển thị
   - ✅ Không có lỗi popup

2. **Thông tin hệ thống:**
   - ✅ Hiển thị "FFmpeg: ✅ OK"
   - ✅ Hiển thị "RAM: ✅ OK" (hoặc cảnh báo nếu thiếu RAM)

3. **Chức năng cơ bản:**
   - ✅ Có thể chọn thư mục (nút "Chọn thư mục...")
   - ✅ Hiển thị đường dẫn thư mục đã chọn
   - ✅ Có nút "Bắt đầu xử lý"

### Bước 3: Test Xử lý File

1. **Chuẩn bị:**
   - Tạo thư mục test với 1-2 file MKV nhỏ
   - Đảm bảo có đủ dung lượng ổ đĩa

2. **Chạy xử lý:**
   - Chọn thư mục test
   - Nhấn "Bắt đầu xử lý"
   - Xem log trong cửa sổ

3. **Kiểm tra kết quả:**
   - ✅ Không có lỗi import
   - ✅ Xử lý file thành công
   - ✅ Tạo file output (audio, subtitle)
   - ✅ Đổi tên file video

---

## ❌ Các Lỗi Thường Gặp

### Lỗi 1: "No module named 'ffmpeg'"

**Nguyên nhân:** PyInstaller không bundle được `ffmpeg-python`

**Giải pháp:**
1. Kiểm tra đã cài `ffmpeg-python` chưa:
   ```bash
   pip install ffmpeg-python
   ```
2. Build lại:
   ```bash
   python build_complete.py
   ```

### Lỗi 2: "FFmpeg: ❌ NOT FOUND"

**Nguyên nhân:** FFmpeg không được bundle hoặc không tìm thấy

**Giải pháp:**
1. Kiểm tra thư mục `ffmpeg_bin/` có tồn tại không
2. Kiểm tra có file `ffmpeg.exe` (Windows) hoặc `ffmpeg` (Mac/Linux) không
3. Build lại với FFmpeg đầy đủ

### Lỗi 3: GUI không mở

**Nguyên nhân:** 
- Lỗi import
- Thiếu dependencies
- Lỗi khởi tạo GUI

**Giải pháp:**
1. Chạy từ terminal để xem lỗi:
   ```bash
   dist/MKVProcessor.exe
   ```
2. Kiểm tra log lỗi
3. Build lại nếu cần

### Lỗi 4: File quá nhỏ (< 30MB)

**Nguyên nhân:** Thiếu dependencies

**Giải pháp:**
1. Kiểm tra dependencies đã cài đầy đủ chưa
2. Build lại với `--collect-submodules`

---

## ✅ Checklist Test Hoàn Chỉnh

- [ ] File executable tồn tại
- [ ] Kích thước file hợp lý (30-200MB)
- [ ] GUI mở được
- [ ] Hiển thị "FFmpeg: ✅ OK"
- [ ] Hiển thị "RAM: ✅ OK"
- [ ] Có thể chọn thư mục
- [ ] Có thể bắt đầu xử lý
- [ ] Xử lý file thành công (không lỗi import)
- [ ] Tạo file output đúng
- [ ] Đổi tên file video đúng

---

## 💡 Tips

1. **Test trên máy khác:**
   - Copy file exe sang máy khác (không có Python)
   - Test xem có chạy được không

2. **Test với file thật:**
   - Dùng file MKV thật để test
   - Kiểm tra kết quả output

3. **Kiểm tra log:**
   - Xem log trong GUI
   - Kiểm tra file `processed_files.log`

---

## 🎉 Kết Quả Mong Đợi

Sau khi test thành công:
- ✅ Executable chạy được trên máy không có Python
- ✅ Không cần cài đặt gì
- ✅ Xử lý file MKV thành công
- ✅ Tạo output đúng

**→ Build thành công! 🎉**

