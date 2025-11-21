# ⚠️ Giải thích Warnings khi Build

## Các Warnings bạn thấy:

```
WARNING: collect_data_files - skipping data collection for module 'ffmpeg' as it is not a package.
WARNING: collect_dynamic_libs - skipping library collection for module 'ffmpeg' as it is not a package.
WARNING: collect_data_files - skipping data collection for module 'psutil' as it is not a package.
WARNING: collect_dynamic_libs - skipping library collection for module 'psutil' as it is not a package.
```

## ✅ Đây là BÌNH THƯỜNG!

### Tại sao có warnings?

1. **PyInstaller không nhận ra package** - Một số package có cấu trúc đặc biệt
2. **Nhưng vẫn bundle được** - Qua `--hidden-import`, code vẫn được bundle
3. **Không ảnh hưởng chức năng** - Executable vẫn chạy bình thường

---

## 🔍 Kiểm tra Build có thành công không?

Sau khi build xong, kiểm tra:

1. **File exe có được tạo không?**
   ```
   dist/MKVProcessor.exe
   ```

2. **Kích thước file hợp lý không?**
   - Nếu < 10MB → Có thể thiếu dependencies
   - Nếu > 50MB → Có thể đã bundle đầy đủ

3. **Chạy thử có lỗi không?**
   - Nếu chạy được → Build thành công!
   - Nếu lỗi import → Cần sửa thêm

---

## 💡 Nếu vẫn lỗi import sau khi build:

### Cách 1: Kiểm tra package name

```bash
# Kiểm tra package thực tế
python -c "import ffmpeg; print(ffmpeg.__file__)"
python -c "import psutil; print(psutil.__file__)"
```

### Cách 2: Thêm vào spec file

Nếu build thất bại, có thể chỉnh sửa file `.spec`:

```python
# Trong MKVProcessor.spec
a = Analysis(
    ...
    hiddenimports=['ffmpeg', 'psutil', ...],
    # Thêm vào đây
)
```

### Cách 3: Test import trong executable

Chạy exe và xem log để biết module nào thiếu.

---

## ✅ Kết luận:

**Warnings này KHÔNG PHẢI LỖI!**

- ✅ Build vẫn tiếp tục
- ✅ Executable vẫn được tạo
- ✅ Code vẫn được bundle qua hidden-import
- ✅ Chỉ cần test xem có chạy được không

**Nếu executable chạy được → Bỏ qua warnings!**

---

**💡 Tip:** Nếu muốn tắt warnings, có thể redirect output, nhưng không cần thiết.

