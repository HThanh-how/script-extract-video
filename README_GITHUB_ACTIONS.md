# 🚀 GitHub Actions - Tự động Build và Release

## ✨ Tính năng

GitHub Actions tự động:
- ✅ Build cho **6 platforms**: Windows (x64, x86), macOS (x64, arm64), Linux (x64, arm64)
- ✅ Tự động tải và bundle FFmpeg
- ✅ Tạo release khi push tag `v*`
- ✅ Upload artifacts cho tất cả platforms

---

## 📋 Cách sử dụng

### 1. Tạo Release

```bash
# Tạo tag và push
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions sẽ tự động:
1. Build cho tất cả platforms
2. Tạo release với tất cả artifacts
3. Upload files lên release

### 2. Manual Trigger

Vào **Actions** tab → **Build and Release** → **Run workflow**

---

## 📦 Artifacts được tạo

| Platform | Architecture | File |
|---|---|---|
| Windows | x64 | `MKVProcessor_Windows_x64.zip` |
| Windows | x86 | `MKVProcessor_Windows_x86.zip` |
| macOS | x64 (Intel) | `MKVProcessor_macOS_x64.zip` |
| macOS | arm64 (Apple Silicon) | `MKVProcessor_macOS_arm64.zip` |
| Linux | x64 | `MKVProcessor_Linux_x64.tar.gz` |
| Linux | arm64 | `MKVProcessor_Linux_arm64.tar.gz` |

---

## 🔧 Workflow Details

### Build Jobs

Mỗi job chạy độc lập:
1. **Checkout code**
2. **Setup Python 3.11**
3. **Install dependencies**
4. **Download/Install FFmpeg**
5. **Build executable**
6. **Create archive**
7. **Upload artifact**

### Release Job

Chạy sau khi tất cả build jobs thành công:
- Download tất cả artifacts
- Tạo GitHub Release
- Upload tất cả files lên release

---

## 🐛 Troubleshooting

### Build fails

1. Kiểm tra logs trong Actions tab
2. Đảm bảo `requirements.txt` đầy đủ
3. Kiểm tra FFmpeg download (Windows)

### Release không tạo

1. Đảm bảo tag bắt đầu bằng `v` (ví dụ: `v1.0.0`)
2. Kiểm tra tất cả build jobs đã thành công
3. Kiểm tra quyền tạo release trong repo settings

---

## 💡 Tips

1. **Test trước khi release**: Push tag với `-beta` để test
2. **Versioning**: Sử dụng semantic versioning (v1.0.0, v1.1.0, v2.0.0)
3. **Release notes**: GitHub tự động generate, có thể edit sau

---

## 📝 Example

```bash
# Tạo release v1.0.0
git tag v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# GitHub Actions sẽ tự động:
# 1. Build 6 packages
# 2. Tạo release
# 3. Upload tất cả files
```

---

**🎉 Sau khi workflow chạy xong, bạn sẽ có release với tất cả packages cho mọi platform!**

