# 🚀 Hướng Dẫn Triển Khai Lên Streamlit Cloud

## Bước 1: Tạo GitHub Repository

1. Truy cập: https://github.com/new
2. Tạo repository mới (ví dụ: `imdb-movie-analysis`)
3. Chọn **Public**
4. **Không** chọn "Add a README file"

## Bước 2: Upload Code Lên GitHub

Mở terminal trong thư mục project và chạy:

```bash
git init
git add .
git commit -m "Initial commit - IMDb Movie Analysis"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/imdb-movie-analysis.git
git push -u origin main
```

**Thay `YOUR_USERNAME` bằng username GitHub của bạn**

## Bước 3: Triển Khai Lên Streamlit Cloud

1. Truy cập: https://share.streamlit.io/
2. Đăng nhập bằng GitHub
3. Click **"New app"**
4. Chọn:
   - **Repository:** `YOUR_USERNAME/imdb-movie-analysis`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy"**

## ⏱️ Thời Gian

- Upload GitHub: 2-5 phút
- Deploy Streamlit: 3-5 phút
- **Tổng:** Khoảng 10 phút

## 🔗 Kết Quả

Bạn sẽ nhận được link dạng:
```
https://YOUR_USERNAME-imdb-movie-analysis-app-xxxxx.streamlit.app
```

Link này có thể chia sẻ cho giảng viên!

## 📌 Lưu Ý

- Repository phải là **Public**
- File `requirements.txt` phải có đầy đủ thư viện
- File `data/processed_movies.csv` phải được commit
- Streamlit Cloud miễn phí cho 1 app

## 🆘 Nếu Gặp Lỗi

1. Kiểm tra file `requirements.txt`
2. Xem logs trên Streamlit Cloud
3. Đảm bảo file `processed_movies.csv` tồn tại

## 📧 Liên Hệ

Nếu cần hỗ trợ, liên hệ qua GitHub Issues của repository.
