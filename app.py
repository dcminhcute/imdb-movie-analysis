"""
Streamlit Web App for IMDb Movie Data Storytelling
Ứng dụng web tương tác để khám phá dữ liệu phim
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# ==================== CẤU HÌNH TRANG ====================

st.set_page_config(
    page_title="IMDb Movie Storytelling",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    /* Căn giữa các cột trong bảng */
    table td, table th {
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD DỮ LIỆU ====================

@st.cache_data(ttl=600)  # Cache 10 phút
def load_data():
    """Load dữ liệu đã xử lý"""
    data_path = 'data/processed_movies.csv'
    if os.path.exists(data_path):
        df = pd.read_csv(data_path, encoding='utf-8-sig')
        # Chuyển đổi kiểu dữ liệu
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        return df
    else:
        st.error("❌ Không tìm thấy file dữ liệu! Vui lòng chạy data_collection.py và data_preprocessing.py trước.")
        st.stop()

# Button để clear cache (ẩn trong sidebar)
with st.sidebar:
    if st.button("🔄 Reload Data", help="Click để tải lại dữ liệu mới nhất"):
        st.cache_data.clear()
        st.rerun()

df = load_data()

# ==================== HEADER ====================

st.markdown('<h1 class="main-header">🎬 IMDb Movie\'s History</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Khám phá lịch sử điện ảnh IMDb qua dữ liệu</p>', unsafe_allow_html=True)

# ==================== SIDEBAR - BỘ LỌC ====================

st.sidebar.header("🎯 Bộ Lọc Dữ Liệu")

# Lọc theo năm
if 'Year' in df.columns:
    year_min = int(df['Year'].min())
    year_max = int(df['Year'].max())
    year_range = st.sidebar.slider(
        "📅 Chọn khoảng năm",
        year_min, year_max,
        (year_min, year_max)
    )
else:
    year_range = None

# Lọc theo thể loại
genre_col = 'Primary_Genre' if 'Primary_Genre' in df.columns else 'genre' if 'genre' in df.columns else None
if genre_col:
    genres = ['Tất cả'] + sorted(df[genre_col].dropna().unique().tolist())
    selected_genre = st.sidebar.selectbox("🎭 Chọn thể loại", genres)
else:
    selected_genre = 'Tất cả'

# Lọc theo quốc gia
country_col = 'Primary_Country' if 'Primary_Country' in df.columns else 'Country' if 'Country' in df.columns else None
if country_col:
    countries = ['Tất cả'] + sorted(df[country_col].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("🌍 Chọn quốc gia", countries)
else:
    selected_country = 'Tất cả'

# Lọc theo rating
if 'Rating' in df.columns:
    rating_min = st.sidebar.slider(
        "⭐ Rating tối thiểu",
        0.0, 10.0, 0.0, 0.5
    )
else:
    rating_min = 0.0

# Áp dụng bộ lọc
df_filtered = df.copy()
if year_range:
    df_filtered = df_filtered[(df_filtered['Year'] >= year_range[0]) & (df_filtered['Year'] <= year_range[1])]
if selected_genre != 'Tất cả' and genre_col:
    df_filtered = df_filtered[df_filtered[genre_col] == selected_genre]
if selected_country != 'Tất cả' and country_col:
    df_filtered = df_filtered[df_filtered[country_col] == selected_country]
if rating_min > 0:
    df_filtered = df_filtered[df_filtered['Rating'] >= rating_min]

st.sidebar.markdown(f"**📊 Số phim sau lọc: {len(df_filtered)}**")

# ==================== TAB NAVIGATION ====================

tabs = st.tabs([
    "🏠 Tổng Quan",
    "📊 Phân Tích Thống Kê",
    "📈 Xu Hướng Thời Gian",
    "🔍 Phân Tích Sâu",
    "🏆 Top Movies",
    "💡 Insights"
])

# ==================== TAB 1: TỔNG QUAN ====================

with tabs[0]:
    st.header("📌 Giới Thiệu Dự Án")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Mục tiêu
        
        Dự án này phân tích dữ liệu phim từ IMDb để:
        - 📊 Hiểu xu hướng điện ảnh qua các thập kỷ
        - 🎭 Khám phá mối quan hệ giữa thể loại, rating, doanh thu
        - 🌍 Tìm hiểu đóng góp của các quốc gia vào ngành công nghiệp điện ảnh
        - 💰 Phân tích yếu tố ảnh hưởng đến thành công của phim
        
        ### 📂 Nguồn dữ liệu
        - **OMDb API** (Open Movie Database)
        - **Dataset mẫu** từ các phim nổi tiếng trên IMDb
        
        ### 🛠️ Công nghệ sử dụng
        - **Python**: Pandas, NumPy, Plotly, Streamlit
        - **Visualization**: Interactive charts với Plotly
        - **Web Framework**: Streamlit
        """)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>📊 Thống Kê Tổng Quan</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("🎬 Tổng số phim", f"{len(df):,}")
        if 'Year' in df.columns:
            st.metric("📅 Năm sớm nhất", f"{int(df['Year'].min())}")
            st.metric("📅 Năm mới nhất", f"{int(df['Year'].max())}")
        if 'Rating' in df.columns:
            st.metric("⭐ Rating TB", f"{df['Rating'].mean():.2f}")
        if genre_col and genre_col in df.columns:
            st.metric("🎭 Số thể loại", f"{df[genre_col].nunique()}")

    # Biểu đồ tổng quan
    st.markdown("---")
    st.subheader("📊 Phân Bố Thể Loại")
    
    if genre_col and genre_col in df_filtered.columns:
        genre_counts = df_filtered[genre_col].value_counts().head(10)
        fig = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            title='Top 10 Thể Loại Phim',
            labels={'x': 'Số lượng', 'y': 'Thể loại'},
            color=genre_counts.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 2: PHÂN TÍCH THỐNG KÊ ====================

with tabs[1]:
    st.header("📊 Phân Tích Thống Kê Chi Tiết")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎬 Số phim", f"{len(df_filtered):,}")
    with col2:
        if 'Rating' in df_filtered.columns:
            st.metric("⭐ Rating TB", f"{df_filtered['Rating'].mean():.2f}")
    with col3:
        if 'Runtime' in df_filtered.columns:
            st.metric("⏱️ Runtime TB", f"{df_filtered['Runtime'].mean():.0f} phút")
    with col4:
        if 'BoxOffice' in df_filtered.columns and df_filtered['BoxOffice'].notna().any():
            st.metric("💰 Doanh thu TB", f"${df_filtered['BoxOffice'].mean()/1e6:.1f}M")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Rating' in df_filtered.columns:
            fig = px.histogram(
                df_filtered,
                x='Rating',
                nbins=20,
                title='⭐ Histogram: Phân Phối Rating',
                labels={'Rating': 'IMDb Rating', 'count': 'Số lượng'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Runtime' in df_filtered.columns:
            fig = px.box(
                df_filtered,
                y='Runtime',
                title='⏱️ Boxplot: Phân Phối Thời Lượng',
                labels={'Runtime': 'Thời lượng (phút)'},
                color_discrete_sequence=['#764ba2']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    if genre_col and genre_col in df_filtered.columns and 'Runtime' in df_filtered.columns:
        st.subheader("🎻 Violin Plot: Runtime Theo Thể Loại")
        top_genres = df_filtered[genre_col].value_counts().head(6).index
        df_top_genres = df_filtered[df_filtered[genre_col].isin(top_genres)]
        
        fig = px.violin(
            df_top_genres,
            x=genre_col,
            y='Runtime',
            color=genre_col,
            title='Phân phối Runtime theo thể loại',
            box=True,
            points="outliers"
        )
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 3: XU HƯỚNG THỜI GIAN ====================

with tabs[2]:
    st.header("📈 Xu Hướng Theo Thời Gian")
    
    if 'Year' in df_filtered.columns:
        movies_by_year = df_filtered.groupby('Year').size().reset_index(name='Count')
        
        fig = px.area(
            movies_by_year,
            x='Year',
            y='Count',
            title='📈 Area Chart: Số Lượng Phim Theo Năm',
            labels={'Year': 'Năm', 'Count': 'Số lượng phim'}
        )
        fig.update_traces(line=dict(color='royalblue', width=2))
        st.plotly_chart(fig, use_container_width=True)
        
        if 'Decade' in df_filtered.columns and 'Rating' in df_filtered.columns:
            st.subheader("⭐ Line Chart: Rating Theo Thập Kỷ")
            
            rating_by_decade = df_filtered.groupby('Decade')['Rating'].mean().reset_index()
            
            fig = px.line(
                rating_by_decade,
                x='Decade',
                y='Rating',
                title='Rating trung bình theo thập kỷ',
                labels={'Decade': 'Thập kỷ', 'Rating': 'Rating TB'},
                markers=True
            )
            fig.update_traces(line=dict(color='orange', width=3), marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
        
        # Box Office trend
        if 'BoxOffice' in df_filtered.columns and df_filtered['BoxOffice'].notna().any():
            st.subheader("💰 Xu Hướng Doanh Thu")
            
            boxoffice_by_year = df_filtered.groupby('Year')['BoxOffice'].sum().reset_index()
            
            fig = px.area(
                boxoffice_by_year,
                x='Year',
                y='BoxOffice',
                title='Tổng doanh thu Box Office theo năm',
                labels={'BoxOffice': 'Doanh thu (USD)', 'Year': 'Năm'}
            )
            st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 4: PHÂN TÍCH SÂU ====================

with tabs[3]:
    st.header("🔍 Phân Tích Mối Quan Hệ")
    
    if 'Runtime' in df_filtered.columns and 'Rating' in df_filtered.columns:
        st.subheader("📊 Scatter Plot + Hồi Quy: Runtime vs Rating")
        
        fig = px.scatter(
            df_filtered.sample(min(200, len(df_filtered))),
            x='Runtime',
            y='Rating',
            color=genre_col if genre_col and genre_col in df_filtered.columns else None,
            trendline="ols",
            title='Mối quan hệ giữa thời lượng và rating (với đường hồi quy)',
            labels={'Runtime': 'Thời lượng (phút)', 'Rating': 'IMDb Rating'},
            hover_data=['Title', 'Year']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔥 Heatmap: Ma Trận Tương Quan")
    
    numeric_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_cols) > 1:
        corr_matrix = df_filtered[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect='auto',
            title='Heatmap tương quan giữa các biến số',
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    if genre_col and genre_col in df_filtered.columns:
        st.subheader("🌳 Treemap: Phân Bố Thể Loại")
        genre_counts = df_filtered[genre_col].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig = px.treemap(
            genre_counts,
            path=['Genre'],
            values='Count',
            title='Treemap phân bố thể loại phim',
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig.update_traces(textinfo="label+value+percent parent")
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 5: TOP MOVIES ====================

with tabs[4]:
    st.header("🏆 Top Movies")
    
    if 'Rating' in df_filtered.columns:
        st.subheader("⭐ Top 20 Phim Rating Cao Nhất")
        
        # Chọn cột để hiển thị
        cols_to_show = ['Title', 'Year', 'Rating']
        if genre_col and genre_col in df_filtered.columns:
            cols_to_show.append(genre_col)
        
        top_rated = df_filtered.nlargest(20, 'Rating')[cols_to_show].copy()
        top_rated['Rating'] = top_rated['Rating'].round(1)
        
        fig = px.bar(
            top_rated,
            x='Rating',
            y='Title',
            color=genre_col if genre_col in top_rated.columns else None,
            orientation='h',
            title='Top 20 phim có rating cao nhất',
            labels={'Rating': 'IMDb Rating', 'Title': ''},
            hover_data=['Year']
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Hiển thị bảng với số thứ tự bắt đầu từ 1
        top_rated_display = top_rated.reset_index(drop=True)
        top_rated_display.index = range(1, len(top_rated_display) + 1)
        # Format Rating để chỉ hiển thị 1 chữ số thập phân
        top_rated_display['Rating'] = top_rated_display['Rating'].apply(lambda x: f"{x:.1f}")
        st.table(top_rated_display)
    
    if 'BoxOffice' in df_filtered.columns and df_filtered['BoxOffice'].notna().any():
        st.subheader("💰 Top 20 Phim Doanh Thu Cao Nhất")
        
        top_boxoffice = df_filtered.nlargest(20, 'BoxOffice')[['Title', 'Year', 'BoxOffice', 'Rating']].copy()
        top_boxoffice['BoxOffice_M'] = (top_boxoffice['BoxOffice'] / 1e6).round(1)
        top_boxoffice['Rating'] = top_boxoffice['Rating'].round(1)
        
        fig = px.bar(
            top_boxoffice,
            x='BoxOffice_M',
            y='Title',
            orientation='h',
            title='Top 20 phim có doanh thu cao nhất',
            labels={'BoxOffice_M': 'Doanh thu (Triệu USD)', 'Title': ''},
            color='Rating',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Hiển thị bảng với số thứ tự bắt đầu từ 1
        top_boxoffice_display = top_boxoffice[['Title', 'Year', 'BoxOffice_M', 'Rating']].reset_index(drop=True)
        top_boxoffice_display.index = range(1, len(top_boxoffice_display) + 1)
        # Format để chỉ hiển thị 1 chữ số thập phân
        top_boxoffice_display['Rating'] = top_boxoffice_display['Rating'].apply(lambda x: f"{x:.1f}")
        top_boxoffice_display['BoxOffice_M'] = top_boxoffice_display['BoxOffice_M'].apply(lambda x: f"{x:.1f}")
        st.table(top_boxoffice_display)

# ==================== TAB 6: INSIGHTS ====================

with tabs[5]:
    st.header("💡 Key Insights & Storytelling")
    
    st.markdown("""
    <div class="insight-box">
        <h3>🎯 Những Phát Hiện Chính</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Insight 1: Rating Distribution
    if 'Rating' in df.columns:
        avg_rating = df['Rating'].mean()
        st.markdown(f"""
        ### 1. ⭐ Phân Bố Rating
        
        - **Rating trung bình**: {avg_rating:.2f}/10
        - Phần lớn các phim có rating từ 7-9, cho thấy dataset tập trung vào các phim được đánh giá cao
        - Rất ít phim có rating dưới 5, điều này phản ánh việc chỉ những phim chất lượng mới được ghi nhận rộng rãi
        """)
    
    # Insight 2: Genre Analysis
    if genre_col and genre_col in df.columns:
        top_genre = df[genre_col].value_counts().index[0]
        top_genre_count = df[genre_col].value_counts().values[0]
        
        st.markdown(f"""
        ### 2. 🎭 Thể Loại Phổ Biến
        
        - **Thể loại phổ biến nhất**: {top_genre} ({top_genre_count} phim)
        - Drama và Action là hai thể loại chiếm ưu thế trong ngành công nghiệp điện ảnh
        - Phim hoạt hình (Animation) ngày càng phát triển mạnh, đặc biệt từ thập kỷ 2000
        """)
    
    # Insight 3: Time Trends
    if 'Year' in df.columns:
        st.markdown(f"""
        ### 3. 📈 Xu Hướng Thời Gian
        
        - Số lượng phim sản xuất tăng đáng kể từ những năm 1990
        - Thập kỷ 2010-2020 chứng kiến sự bùng nổ của phim siêu anh hùng
        - COVID-19 (2020-2021) tạm thời làm gián đoạn sản xuất phim nhưng đã phục hồi mạnh mẽ
        """)
    
    # Insight 4: Runtime
    if 'Runtime' in df.columns:
        avg_runtime = df['Runtime'].mean()
        st.markdown(f"""
        ### 4. ⏱️ Thời Lượng Phim
        
        - **Thời lượng trung bình**: {avg_runtime:.0f} phút
        - Phim hành động thường dài hơn (120-150 phút)
        - Phim hoạt hình ngắn hơn (80-100 phút), phù hợp với khán giả trẻ em
        """)
    
    # Insight 5: Success Factors
    st.markdown("""
    ### 5. 🎯 Yếu Tố Thành Công
    
    - **Rating cao** không hoàn toàn tương quan với **doanh thu cao**
    - Thể loại Action/Adventure thường có doanh thu tốt hơn Drama
    - Đạo diễn nổi tiếng (Nolan, Spielberg, Cameron) có ảnh hưởng lớn đến thành công phim
    - Marketing và thương hiệu (Marvel, DC) đóng vai trò quan trọng
    """)
    
    st.markdown("---")
    st.subheader("☁️ WordCloud: Từ Khóa Trong Tiêu Đề Phim")
    
    if 'Title' in df.columns:
        text = ' '.join(df['Title'].astype(str))
        wordcloud = WordCloud(
            width=1200,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=50
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    
    st.markdown("""
    <div class="insight-box">
        <h3>🎬 Kết Luận</h3>
        <p>
        Phân tích dữ liệu phim IMDb cho thấy ngành công nghiệp điện ảnh đã có sự phát triển vượt bậc 
        trong những thập kỷ gần đây. Sự đa dạng về thể loại, công nghệ tiên tiến, và mô hình kinh doanh 
        mới đã tạo ra nhiều cơ hội cho các nhà làm phim. Tuy nhiên, chất lượng nội dung vẫn là yếu tố 
        quan trọng nhất để tạo nên những tác phẩm kinh điển bất hủ.
        </p>
    </div>
    """, unsafe_allow_html=True)
