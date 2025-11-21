# 🚀 Hướng dẫn Sử dụng GitHub Actions

## ❓ Tại sao GitHub Actions không chạy?

Workflow chỉ chạy khi:
1. ✅ **Push tag** `v*` (ví dụ: `v1.0.0`)
2. ✅ **Push vào branch** `main` hoặc `master`
3. ✅ **Manual trigger** (chạy thủ công)
4. ✅ **Pull Request** vào main/master

---

## 🎯 Cách Trigger Workflow

### Cách 1: Push Tag (Tạo Release)

```bash
# 1. Commit và push code
git add .
git commit -m "Update code"
git push origin main

# 2. Tạo tag và push
git tag v1.0.0
git push origin v1.0.0
```

**→ GitHub Actions sẽ tự động chạy và tạo Release!**

### Cách 2: Push vào Main (Test Build)

```bash
# Chỉ cần push code
git add .
git commit -m "Test build"
git push origin main
```

**→ GitHub Actions sẽ chạy và build, nhưng KHÔNG tạo release**

### Cách 3: Manual Trigger (Chạy Thủ Công)

1. Vào GitHub repository
2. Click tab **"Actions"**
3. Chọn workflow **"Build and Release"**
4. Click **"Run workflow"** (bên phải)
5. Chọn branch và click **"Run workflow"**

**→ Workflow sẽ chạy ngay lập tức!**

---

## ✅ Kiểm tra Workflow đã chạy

1. Vào tab **"Actions"** trên GitHub
2. Xem danh sách workflows đã chạy
3. Click vào workflow để xem chi tiết
4. Xem logs của từng job

---

## 🐛 Troubleshooting

### Workflow không xuất hiện

**Nguyên nhân:**
- File `.github/workflows/build-release.yml` chưa được commit/push

**Giải pháp:**
```bash
git add .github/workflows/build-release.yml
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### Workflow chạy nhưng fail

**Kiểm tra:**
1. Xem logs trong Actions tab
2. Tìm job nào bị lỗi
3. Xem error message

**Lỗi thường gặp:**
- Thiếu dependencies → Kiểm tra `requirements.txt`
- FFmpeg download fail → Kiểm tra network
- Build fail → Kiểm tra `build_complete.py`

### Release không được tạo

**Nguyên nhân:**
- Chỉ tạo release khi push tag `v*`
- Push vào main KHÔNG tạo release (chỉ build)

**Giải pháp:**
```bash
# Tạo tag để trigger release
git tag v1.0.0
git push origin v1.0.0
```

---

## 📋 Checklist

Trước khi push:
- [ ] File `.github/workflows/build-release.yml` đã có
- [ ] File `build_complete.py` đã có
- [ ] File `requirements.txt` đã có
- [ ] File `script.py`, `gui.py` đã có
- [ ] File `ffmpeg_helper.py` đã có

Sau khi push:
- [ ] Vào tab Actions kiểm tra workflow đã chạy
- [ ] Xem logs nếu có lỗi
- [ ] Kiểm tra artifacts đã được tạo
- [ ] Nếu push tag, kiểm tra release đã được tạo

---

## 💡 Tips

1. **Test trước**: Push vào main để test build trước khi tạo release
2. **Versioning**: Dùng semantic versioning (v1.0.0, v1.1.0, v2.0.0)
3. **Manual trigger**: Dùng để test workflow mà không cần commit
4. **Xem logs**: Luôn xem logs để debug nếu có lỗi

---

## 🎯 Quick Start

```bash
# 1. Đảm bảo đã commit workflow file
git status

# 2. Nếu chưa, commit và push
git add .github/
git commit -m "Add GitHub Actions"
git push origin main

# 3. Tạo tag để trigger release
git tag v1.0.0 -m "First release"
git push origin v1.0.0

# 4. Vào GitHub → Actions → Xem workflow chạy
```

---

**🎉 Sau khi workflow chạy xong, bạn sẽ có release với tất cả packages!**

