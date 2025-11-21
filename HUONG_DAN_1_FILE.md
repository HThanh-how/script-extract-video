# 📦 Hướng dẫn: Chỉ 1 File EXE Duy Nhất

## ✨ Mục tiêu: 1 FILE DUY NHẤT - Không cần gì khác!

Sau khi build, bạn sẽ có **CHỈ 1 FILE .EXE**:
- ✅ Tất cả Python code đã bundle
- ✅ Tất cả dependencies đã bundle  
- ✅ FFmpeg đã bundle (extract tự động khi chạy)
- ✅ Không cần file nào khác!

---

## 🔨 Build

```bash
python build_complete.py
```

**Kết quả:** `dist/MKVProcessor.exe` (chỉ 1 file!)

---

## 🚀 Sử dụng

### Cho người dùng:

1. **Tải file** `MKVProcessor.exe`
2. **Double-click** để chạy
3. **XONG!** Không cần cài gì!

**Đúng như bạn muốn - chỉ 1 file, nhấn là chạy!**

---

## 📊 So sánh

| | Trước | Bây giờ |
|---|---|---|
| Số file | Nhiều file + thư mục | **1 file duy nhất** |
| FFmpeg | Thư mục riêng | **Bundle trong exe** |
| Dependencies | Nhiều file | **Bundle trong exe** |
| Dễ chia sẻ | ❌ | ✅ |

---

## 💡 Cách hoạt động

1. **Khi chạy exe:**
   - PyInstaller extract tất cả vào thư mục tạm `_MEIPASS`
   - FFmpeg được extract tự động
   - Code chạy từ thư mục tạm
   - Khi đóng, thư mục tạm tự động xóa

2. **Người dùng không thấy:**
   - Không thấy thư mục tạm
   - Không cần quan tâm gì
   - Chỉ cần chạy file exe

---

## ✅ Lợi ích

1. **Chỉ 1 file** - Dễ chia sẻ
2. **Không cần cài đặt** - Double-click là chạy
3. **Tự động extract** - FFmpeg extract tự động
4. **Tự động dọn dẹp** - Thư mục tạm tự xóa

---

## 🎯 Kết quả

```
dist/
└── MKVProcessor.exe    ← CHỈ CẦN FILE NÀY!
```

**Kích thước:** ~100-150MB (bao gồm tất cả)

---

**🎉 Vậy là xong! Bạn có 1 file duy nhất, chỉ cần tải và chạy!**

