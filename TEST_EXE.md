# 🧪 Hướng dẫn Test Executable

## ✅ Kích thước 70MB là BÌNH THƯỜNG!

### 📊 So sánh kích thước:

- **Python interpreter**: ~15-20MB
- **tkinter (GUI)**: ~5-10MB
- **ffmpeg-python**: ~2-5MB
- **psutil**: ~1-2MB
- **FFmpeg binaries**: ~30-40MB
- **PyInstaller overhead**: ~5-10MB
- **Tổng**: **~60-90MB** → **70MB là hợp lý!**

---

## 🧪 Cách Test Executable:

### Bước 1: Chạy thử GUI

```bash
# Double-click vào file exe hoặc chạy từ terminal
dist/MKVProcessor.exe
```

**Kiểm tra:**
- ✅ GUI có mở được không?
- ✅ Có hiển thị "FFmpeg: OK" không?
- ✅ Có hiển thị "RAM: OK" không?

---

### Bước 2: Test xử lý file

1. **Chọn thư mục** có file MKV test
2. **Nhấn "Bắt đầu xử lý"**
3. **Xem log** có lỗi gì không

**Nếu thành công:**
- ✅ Không có lỗi import
- ✅ Xử lý file được
- ✅ Tạo file output

**Nếu lỗi:**
- ❌ Lỗi import → Cần sửa build
- ❌ Lỗi FFmpeg → Cần kiểm tra bundle FFmpeg
- ❌ Lỗi khác → Xem log chi tiết

---

### Bước 3: Test import (nếu cần)

Nếu muốn test chi tiết hơn, chạy:

```bash
python test_exe.py
```

Script này sẽ kiểm tra:
- ✅ Import được ffmpeg không?
- ✅ Import được psutil không?
- ✅ Import được script không?
- ✅ Import được ffmpeg_helper không?

---

## ⚠️ Nếu vẫn lỗi import:

### Lỗi: "No module named 'ffmpeg'"

**Nguyên nhân:** PyInstaller không bundle đúng package

**Giải pháp:**
1. Kiểm tra `requirements.txt` có `ffmpeg-python` không
2. Chạy lại: `pip install -r requirements.txt`
3. Build lại: `python build_complete.py`

### Lỗi: "No module named 'psutil'"

**Nguyên nhân:** Tương tự như trên

**Giải pháp:**
1. Kiểm tra `requirements.txt` có `psutil` không
2. Chạy lại: `pip install -r requirements.txt`
3. Build lại: `python build_complete.py`

---

## 💡 Tips:

1. **Kích thước không quan trọng** - Quan trọng là chạy được!
2. **70MB là hợp lý** - Không phải quá nhẹ hay quá nặng
3. **Test thực tế** - Chạy thử với file MKV thật
4. **Nếu chạy được** → Build thành công! ✅

---

## ✅ Kết luận:

**70MB là hợp lý cho một executable Python!**

- ✅ Python interpreter: ~20MB
- ✅ Dependencies: ~10MB
- ✅ FFmpeg: ~30MB
- ✅ Overhead: ~10MB
- ✅ **Tổng: ~70MB** → **Bình thường!**

**Quan trọng:** Test xem có chạy được không, không phải kích thước!

---

**🎉 Nếu executable chạy được → Build thành công!**

