# 🔧 Sửa Lỗi Import "No module named 'ffmpeg'"

## ❌ Vấn đề:

Khi chạy executable, gặp lỗi:
```
[ERROR] Lỗi import dependencies: No module named 'ffmpeg'
```

## 🔍 Nguyên nhân:

PyInstaller không bundle được package `ffmpeg-python` vì:
1. Package name là `ffmpeg-python` nhưng import là `ffmpeg`
2. PyInstaller không tự động phát hiện package này
3. Cần import trực tiếp trong code để PyInstaller bundle

## ✅ Giải pháp đã áp dụng:

### 1. Import ffmpeg ngay từ đầu trong `gui.py`

```python
# Import ngay từ đầu để PyInstaller bundle
try:
    import ffmpeg  # type: ignore
    import psutil  # type: ignore
except ImportError:
    pass
```

### 2. Thêm hidden imports trong `build_complete.py`

```python
hidden_imports = [
    "ffmpeg", "ffmpeg._run", "ffmpeg._probe", "ffmpeg.nodes",
    "ffmpeg._ffmpeg", "ffmpeg._utils", "ffmpeg._filters",
    "psutil", "psutil._common", "psutil._pswindows",
    ...
]
```

### 3. Sử dụng collect-submodules

```python
pyinstaller_args.extend(["--collect-submodules", "ffmpeg"])
pyinstaller_args.extend(["--collect-submodules", "psutil"])
```

### 4. Tạo hook files

- `hook-ffmpeg.py` - Đảm bảo bundle đầy đủ ffmpeg
- `hook-psutil.py` - Đảm bảo bundle đầy đủ psutil

---

## 🚀 Cách build lại:

### Bước 1: Kiểm tra dependencies

```bash
python check_build_requirements.py
```

Hoặc cài đặt thủ công:

```bash
pip install -r requirements.txt
```

### Bước 2: Build lại

```bash
python build_complete.py
```

### Bước 3: Test executable

```bash
dist/MKVProcessor.exe
```

---

## ⚠️ Lưu ý:

1. **Phải cài đặt dependencies trước khi build:**
   ```bash
   pip install ffmpeg-python psutil pyinstaller
   ```

2. **Import phải ở top-level:**
   - PyInstaller chỉ bundle những gì được import trực tiếp
   - Import trong function/thread có thể không được bundle

3. **Kiểm tra kích thước file:**
   - Nếu < 50MB → Có thể thiếu dependencies
   - Nếu > 80MB → Có thể đã bundle đầy đủ

---

## 🐛 Nếu vẫn lỗi:

### Kiểm tra package có được cài đặt đúng không:

```bash
python -c "import ffmpeg; print(ffmpeg.__file__)"
python -c "import psutil; print(psutil.__file__)"
```

### Kiểm tra PyInstaller có bundle đúng không:

1. Xem file `.spec` được tạo
2. Kiểm tra `hiddenimports` có chứa `ffmpeg` không
3. Xem log build có warnings gì không

### Thử build với spec file:

```bash
pyinstaller MKVProcessor.spec
```

---

## ✅ Kết quả mong đợi:

Sau khi build lại:
- ✅ Executable chạy được
- ✅ Không còn lỗi "No module named 'ffmpeg'"
- ✅ GUI hiển thị "FFmpeg: OK"
- ✅ Xử lý file được

---

**💡 Tip:** Nếu vẫn lỗi, gửi log build và log chạy executable để debug tiếp.

