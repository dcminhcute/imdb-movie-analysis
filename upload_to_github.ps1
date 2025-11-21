# Script tự động upload lên GitHub
# Chỉnh sửa YOUR_USERNAME thành username GitHub của bạn

# Bước 1: Add tất cả file
git add .

# Bước 2: Commit
git commit -m "Initial commit - IMDb Movie Analysis with 1000 movies"

# Bước 3: Đổi tên branch
git branch -M main

# Bước 4: Thêm remote GitHub (⚠️ SỬA YOUR_USERNAME)
git remote add origin https://github.com/dcminhcute/imdb-movie-analysis.git

# Bước 5: Push lên GitHub
git push -u origin main

Write-Host "`n✅ Upload thành công!" -ForegroundColor Green
Write-Host "🌐 Tiếp theo: Truy cập https://share.streamlit.io/ để deploy" -ForegroundColor Yellow
