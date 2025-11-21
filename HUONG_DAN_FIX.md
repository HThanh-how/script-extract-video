# 🔧 Hướng dẫn Fix Lỗi Build

## ❌ Lỗi: FileNotFoundError - PyInstaller

### Nguyên nhân:
PyInstaller không có trong PATH hoặc không được tìm thấy.

### ✅ Giải pháp:

Script đã được sửa để dùng `python -m PyInstaller` thay vì chỉ `pyinstaller`.

Nếu vẫn lỗi, thử:

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Hoặc
python -m pip install pyinstaller

# Kiểm tra
python -m PyInstaller --version
```

---

## 🔄 Chạy lại Build

```bash
python build_complete.py
```

Script sẽ:
1. ✅ Tự động detect CI/CD mode (không hỏi input)
2. ✅ Tự động cài PyInstaller nếu thiếu
3. ✅ Tự động tải FFmpeg (Windows)
4. ✅ Build với đúng architecture

---

## 🐛 Các lỗi khác

### Lỗi: "Cannot find ffmpeg_bin"
- Đảm bảo đã chạy `python download_ffmpeg.py` trước
- Hoặc copy FFmpeg vào thư mục `ffmpeg_bin/`

### Lỗi: "Import error"
```bash
pip install -r requirements.txt
```

### Lỗi: "Permission denied"
- Windows: Chạy PowerShell/CMD với quyền Admin
- Linux/Mac: Dùng `sudo` nếu cần

---

## ✅ Test Build

Sau khi fix, test lại:

```bash
# 1. Clean
rm -rf dist build *.spec

# 2. Build
python build_complete.py

# 3. Kiểm tra
ls -la dist/
```

---

**💡 Tip:** Nếu vẫn lỗi, kiểm tra logs chi tiết trong output của script.

