# 📁 Hướng dẫn Chọn Thư Mục

## ✅ Ứng dụng đã hỗ trợ chọn thư mục!

Bạn có thể chọn **BẤT KỲ THƯ MỤC NÀO** để xử lý file MKV.

---

## 🖥️ Cách sử dụng trong GUI:

### Bước 1: Mở ứng dụng
- Chạy `MKVProcessor.exe` (hoặc `.app` / không extension trên Linux)

### Bước 2: Chọn thư mục
1. Click nút **"Chọn thư mục..."**
2. Chọn thư mục chứa file MKV bạn muốn xử lý
3. Ứng dụng sẽ tự động:
   - Hiển thị số file MKV tìm thấy
   - Kiểm tra trạng thái thư mục

### Bước 3: Xử lý
- Click **"🚀 Bắt đầu xử lý"**
- Ứng dụng sẽ xử lý tất cả file MKV trong thư mục đã chọn

---

## 💻 Cách sử dụng từ Command Line:

### Windows:
```cmd
MKVProcessor.exe "D:\Videos\MyMovies"
```

### macOS/Linux:
```bash
./MKVProcessor "/path/to/videos"
```

### Python (nếu chạy từ source):
```bash
python script.py "D:\Videos\MyMovies"
```

---

## 📂 Kết quả sẽ được tạo trong thư mục đã chọn:

```
Thư mục bạn chọn/
├── video1.mkv                    ← File gốc (đã đổi tên)
├── video2.mkv
├── Lồng Tiếng - Thuyết Minh/    ← Video với audio tiếng Việt
│   ├── 4K_VIE_DTS_2023_video1.mkv
│   └── 4K_VIE_DTS_2023_video2.mkv
├── Original/                    ← Video với audio gốc
│   ├── 4K_ENG_DTS_2023_video1.mkv
│   └── 4K_ENG_DTS_2023_video2.mkv
└── Subtitles/                   ← Subtitle đã trích xuất
    ├── video1_vie.srt
    ├── video2_vie.srt
    └── processed_files.log
```

---

## ✅ Lợi ích:

1. **Xử lý nhiều thư mục** - Không cần copy file vào thư mục ứng dụng
2. **Giữ nguyên cấu trúc** - File được xử lý tại chỗ
3. **Dễ quản lý** - Mỗi thư mục có log riêng
4. **Linh hoạt** - Chọn bất kỳ thư mục nào

---

## 💡 Tips:

1. **Xử lý từng thư mục một** - Chọn thư mục → Xử lý → Chọn thư mục khác
2. **Kiểm tra trước** - Xem số file MKV trước khi xử lý
3. **Backup quan trọng** - Nên backup trước khi xử lý số lượng lớn

---

## ❓ FAQ:

**Q: Có thể xử lý nhiều thư mục cùng lúc không?**  
A: Không, nhưng bạn có thể xử lý từng thư mục một rất nhanh.

**Q: File output ở đâu?**  
A: Trong chính thư mục bạn chọn, không phải thư mục ứng dụng.

**Q: Có thể chạy từ bất kỳ đâu không?**  
A: Có! Bạn có thể:
- Chạy ứng dụng từ Desktop
- Chạy từ USB
- Chạy từ bất kỳ thư mục nào
- Chọn thư mục khác để xử lý

**Q: Thư mục ứng dụng có cần ở đâu không?**  
A: Không! Bạn có thể đặt package ở bất kỳ đâu, chọn thư mục khác để xử lý.

---

**🎉 Vậy là bạn có thể chọn bất kỳ thư mục nào để xử lý!**

