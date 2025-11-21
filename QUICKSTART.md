# 🚀 Hướng dẫn nhanh

## Cách 1: Sử dụng Package Hoàn Chỉnh (Dễ nhất) ⭐⭐⭐

### Bước 1: Build package (chỉ cần làm 1 lần)
```bash
# Build package HOÀN CHỈNH (bao gồm FFmpeg)
python build_complete.py
```

Script sẽ tự động:
- ✅ Tải FFmpeg (Windows) hoặc hướng dẫn (Mac/Linux)
- ✅ Build executable
- ✅ Bundle tất cả vào 1 package

### Bước 2: Lấy package
Package ở trong: `dist/MKVProcessor_Portable_[OS]_[ARCH]/`

### Bước 3: Chạy!
- Giải nén thư mục package
- Double-click `MKVProcessor.exe` (Windows) hoặc `MKVProcessor.app` (Mac)
- **XONG! Không cần cài gì cả!**

**💡 Đây chính là cách bạn muốn - như app tải từ mạng, chỉ cần nhấn là chạy!**

---

## Cách 2: Chạy từ Source Code

### Bước 1: Setup (chỉ cần 1 lần)
```bash
python setup.py
```

### Bước 2: Chạy GUI
```bash
python gui.py
```

**Xong!**

---

## So sánh 2 cách

| | Executable | Source Code |
|---|---|---|
| Cần Python? | ❌ | ✅ |
| Cần pip install? | ❌ | ✅ |
| Dễ phân phối? | ✅ | ❌ |
| Dễ debug? | ❌ | ✅ |
| Khuyến nghị cho | Người dùng cuối | Developer |

---

## ⚡ Quick Commands

```bash
# ⭐ BUILD PACKAGE HOÀN CHỈNH (KHUYẾN NGHỊ)
python build_complete.py

# Setup để chạy từ source
python setup.py

# Chạy GUI từ source
python gui.py

# Build executable đơn giản (không bundle FFmpeg)
python build.py

# Chạy command line
python script.py
```

---

## ❓ FAQ

**Q: Tôi không có Python, làm sao?**  
A: Bạn chỉ cần Python để BUILD (1 lần). Sau khi build xong, package không cần Python!

**Q: FFmpeg là gì? Có cần cài không?**  
A: Tool xử lý video. KHÔNG CẦN CÀI! Script tự động bundle vào package.

**Q: Tôi dùng Mac/Linux, có khác không?**  
A: Không! Build script tự động detect OS. Chỉ cần build trên OS tương ứng.

**Q: Package lớn bao nhiêu?**  
A: Khoảng 100-150MB (đã bao gồm Python + FFmpeg + tất cả dependencies).

**Q: Có thể chia sẻ cho người khác không?**  
A: CÓ! Chỉ cần copy thư mục package. Họ giải nén và chạy - không cần cài gì!

---

**💡 Tip:** 
- **Build 1 lần** với `build_complete.py`
- **Dùng mãi mãi** - package không cần cập nhật
- **Chia sẻ dễ dàng** - như app thông thường!

