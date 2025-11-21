# 🎬 IMDb Movie Data Storytelling

Ứng dụng web phân tích và trực quan hóa dữ liệu phim IMDb với **1000+ phim**.

## 🌐 Demo Online

**Link ứng dụng:** `[Sẽ được cập nhật sau khi deploy]`

## ✨ Tính Năng

- 📊 **Phân tích thống kê** - Histogram, Boxplot, Violin plot
- 📈 **Xu hướng thời gian** - Phim theo năm, rating theo thập kỷ, doanh thu
- 🔍 **Phân tích sâu** - Scatter plot, heatmap tương quan, treemap
- 🏆 **Top Movies** - Top 20 phim rating cao nhất và doanh thu cao nhất
- 💡 **Insights** - Phát hiện chính và storytelling
- 🎛️ **Bộ lọc** - Lọc theo năm, thể loại, quốc gia, rating

## 📂 Cấu Trúc Project

```
├── app.py                      # Streamlit web app chính
├── data_collection.py          # Thu thập dữ liệu từ OMDb API
├── data_preprocessing.py       # Tiền xử lý và làm sạch dữ liệu
├── data_analysis.py            # Tạo biểu đồ phân tích
├── download_large_dataset.py   # Tải dataset 1000 phim
├── run_all.py                  # Chạy toàn bộ pipeline
├── requirements.txt            # Dependencies
├── data/
│   ├── raw_movies.csv         # Dữ liệu thô
│   └── processed_movies.csv   # Dữ liệu đã xử lý
└── visualizations/            # Các biểu đồ HTML
```

## 🚀 Chạy Local

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
```bash
streamlit run app.py
```

Hoặc chạy toàn bộ pipeline:
```bash
python run_all.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## 📊 Dữ Liệu

- **Nguồn:** IMDb Top 1000 Movies Dataset
- **Số lượng:** 1000 phim
- **Khoảng thời gian:** 2006-2016
- **Các cột:** Title, Year, Genre, Director, Rating, Runtime, Revenue, Metascore, v.v.

## 🛠️ Công Nghệ

- **Python 3.13**
- **Streamlit** - Web framework
- **Pandas** - Xử lý dữ liệu
- **Plotly** - Trực quan hóa tương tác
- **Matplotlib & Seaborn** - Biểu đồ
- **WordCloud** - Word cloud

## 📈 Phân Tích Chính

- Phân bố rating của các phim
- Xu hướng sản xuất phim theo thời gian
- Mối quan hệ giữa runtime và rating
- Top phim theo rating và doanh thu
- Phân tích theo thể loại và quốc gia

## 👨‍💻 Tác Giả

**Đoàn Quang Minh** - B22DCVT336

## 📝 License

Dự án giữa kỳ môn Phân tích dữ liệu

---

⭐ **Nếu thấy hữu ích, hãy cho project một ngôi sao!**
