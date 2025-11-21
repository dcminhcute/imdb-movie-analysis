"""
Streamlit Web App for IMDb Movie Data Storytelling
á»¨ng dá»¥ng web tÆ°Æ¡ng tĂ¡c Ä‘á»ƒ khĂ¡m phĂ¡ dá»¯ liá»‡u phim
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# ==================== Cáº¤U HĂŒNH TRANG ====================

st.set_page_config(
    page_title="IMDb Movie Storytelling",
    page_icon="đŸ¬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tĂ¹y chá»‰nh - XANH DÆ¯Æ NG NHáº T
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        padding: 20px;
        background: linear-gradient(90deg, #5BA3E8 0%, #7FB3E8 100%);
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
        background-color: #E8F4F8;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #5BA3E8;
        margin: 10px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #5BA3E8 0%, #7FB3E8 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD Dá»® LIá»†U ====================

@st.cache_data
def load_data():
    """Load dá»¯ liá»‡u Ä‘Ă£ xá»­ lĂ½"""
    data_path = 'data/processed_movies.csv'
    if os.path.exists(data_path):
        df = pd.read_csv(data_path, encoding='utf-8-sig')
        # Chuyá»ƒn Ä‘á»•i kiá»ƒu dá»¯ liá»‡u
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        return df
    else:
        st.error("âŒ KhĂ´ng tĂ¬m tháº¥y file dá»¯ liá»‡u! Vui lĂ²ng cháº¡y data_collection.py vĂ  data_preprocessing.py trÆ°á»›c.")
        st.stop()

df = load_data()

# ==================== HEADER ====================

st.markdown('<h1 class="main-header">đŸ¬ IMDb Movie Data Storytelling</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">KhĂ¡m phĂ¡ cĂ¢u chuyá»‡n Ä‘iá»‡n áº£nh qua dá»¯ liá»‡u</p>', unsafe_allow_html=True)

# ==================== SIDEBAR - Bá»˜ Lá»ŒC ====================

st.sidebar.header("đŸ¯ Bá»™ Lá»c Dá»¯ Liá»‡u")

# Lá»c theo nÄƒm
if 'Year' in df.columns:
    year_min = int(df['Year'].min())
    year_max = int(df['Year'].max())
    year_range = st.sidebar.slider(
        "đŸ“… Chá»n khoáº£ng nÄƒm",
        year_min, year_max,
        (year_min, year_max)
    )
else:
    year_range = None

# Lá»c theo thá»ƒ loáº¡i
if 'Primary_Genre' in df.columns:
    genres = ['Táº¥t cáº£'] + sorted(df['Primary_Genre'].unique().tolist())
    selected_genre = st.sidebar.selectbox("đŸ­ Chá»n thá»ƒ loáº¡i", genres)
else:
    selected_genre = 'Táº¥t cáº£'

# Lá»c theo quá»‘c gia
if 'Primary_Country' in df.columns:
    countries = ['Táº¥t cáº£'] + sorted(df['Primary_Country'].unique().tolist())
    selected_country = st.sidebar.selectbox("đŸŒ Chá»n quá»‘c gia", countries)
else:
    selected_country = 'Táº¥t cáº£'

# Lá»c theo rating
if 'Rating' in df.columns:
    rating_min = st.sidebar.slider(
        "â­ Rating tá»‘i thiá»ƒu",
        0.0, 10.0, 0.0, 0.5
    )
else:
    rating_min = 0.0

# Ăp dá»¥ng bá»™ lá»c
df_filtered = df.copy()
if year_range:
    df_filtered = df_filtered[(df_filtered['Year'] >= year_range[0]) & (df_filtered['Year'] <= year_range[1])]
if selected_genre != 'Táº¥t cáº£':
    df_filtered = df_filtered[df_filtered['Primary_Genre'] == selected_genre]
if selected_country != 'Táº¥t cáº£':
    df_filtered = df_filtered[df_filtered['Primary_Country'] == selected_country]
if rating_min > 0:
    df_filtered = df_filtered[df_filtered['Rating'] >= rating_min]

st.sidebar.markdown(f"**đŸ“ Sá»‘ phim sau lá»c: {len(df_filtered)}**")

# ==================== TAB NAVIGATION ====================

tabs = st.tabs([
    "đŸ  Tá»•ng Quan",
    "đŸ“ PhĂ¢n TĂ­ch Thá»‘ng KĂª",
    "đŸ“ˆ Xu HÆ°á»›ng Thá»i Gian",
    "đŸ” PhĂ¢n TĂ­ch SĂ¢u",
    "đŸ† Top Movies",
    "đŸ’¡ Insights"
])

# ==================== TAB 1: Tá»”NG QUAN ====================

with tabs[0]:
    st.header("đŸ“Œ Giá»›i Thiá»‡u Dá»± Ăn")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### đŸ¯ Má»¥c tiĂªu
        
        Dá»± Ă¡n nĂ y phĂ¢n tĂ­ch dá»¯ liá»‡u phim tá»« IMDb Ä‘á»ƒ:
        - đŸ“ Hiá»ƒu xu hÆ°á»›ng Ä‘iá»‡n áº£nh qua cĂ¡c tháº­p ká»·
        - đŸ­ KhĂ¡m phĂ¡ má»‘i quan há»‡ giá»¯a thá»ƒ loáº¡i, rating, doanh thu
        - đŸŒ TĂ¬m hiá»ƒu Ä‘Ă³ng gĂ³p cá»§a cĂ¡c quá»‘c gia vĂ o ngĂ nh cĂ´ng nghiá»‡p Ä‘iá»‡n áº£nh
        - đŸ’° PhĂ¢n tĂ­ch yáº¿u tá»‘ áº£nh hÆ°á»Ÿng Ä‘áº¿n thĂ nh cĂ´ng cá»§a phim
        
        ### đŸ“‚ Nguá»“n dá»¯ liá»‡u
        - **OMDb API** (Open Movie Database)
        - **Dataset máº«u** tá»« cĂ¡c phim ná»•i tiáº¿ng trĂªn IMDb
        
        ### đŸ› ï¸ CĂ´ng nghá»‡ sá»­ dá»¥ng
        - **Python**: Pandas, NumPy, Plotly, Streamlit
        - **Visualization**: Interactive charts vá»›i Plotly
        - **Web Framework**: Streamlit
        """)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>đŸ“ Thá»‘ng KĂª Tá»•ng Quan</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("đŸ¬ Tá»•ng sá»‘ phim", f"{len(df):,}")
        if 'Year' in df.columns:
            st.metric("đŸ“… NÄƒm sá»›m nháº¥t", f"{int(df['Year'].min())}")
            st.metric("đŸ“… NÄƒm má»›i nháº¥t", f"{int(df['Year'].max())}")
        if 'Rating' in df.columns:
            st.metric("â­ Rating TB", f"{df['Rating'].mean():.2f}")
        if 'Primary_Genre' in df.columns:
            st.metric("đŸ­ Sá»‘ thá»ƒ loáº¡i", f"{df['Primary_Genre'].nunique()}")

    # Biá»ƒu Ä‘á»“ tá»•ng quan
    st.markdown("---")
    st.subheader("đŸ“ PhĂ¢n Bá»‘ Thá»ƒ Loáº¡i")
    
    if 'Primary_Genre' in df_filtered.columns:
        genre_counts = df_filtered['Primary_Genre'].value_counts().head(10)
        fig = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            title='Top 10 Thá»ƒ Loáº¡i Phim',
            labels={'x': 'Sá»‘ lÆ°á»£ng', 'y': 'Thá»ƒ loáº¡i'},
            color=genre_counts.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 2: PHĂ‚N TĂCH THá»NG KĂ ====================

with tabs[1]:
    st.header("đŸ“ PhĂ¢n TĂ­ch Thá»‘ng KĂª Chi Tiáº¿t")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("đŸ¬ Sá»‘ phim", f"{len(df_filtered):,}")
    with col2:
        if 'Rating' in df_filtered.columns:
            st.metric("â­ Rating TB", f"{df_filtered['Rating'].mean():.2f}")
    with col3:
        if 'Runtime' in df_filtered.columns:
            st.metric("â±ï¸ Runtime TB", f"{df_filtered['Runtime'].mean():.0f} phĂºt")
    with col4:
        if 'BoxOffice' in df_filtered.columns and df_filtered['BoxOffice'].notna().any():
            st.metric("đŸ’° Doanh thu TB", f"${df_filtered['BoxOffice'].mean()/1e6:.1f}M")
    
    st.markdown("---")
    
    # Histogram Rating - ÄÆ N GIáº¢N
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Rating' in df_filtered.columns:
            fig = px.histogram(
                df_filtered,
                x='Rating',
                nbins=20,
                title='â­ PhĂ¢n Phá»‘i ÄĂ¡nh GiĂ¡ IMDb',
                labels={'Rating': 'ÄĂ¡nh giĂ¡ IMDb', 'count': 'Sá»‘ lÆ°á»£ng phim'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Runtime' in df_filtered.columns:
            fig = px.histogram(
                df_filtered,
                x='Runtime',
                nbins=20,
                title='â±ï¸ PhĂ¢n Phá»‘i Thá»i LÆ°á»£ng',
                labels={'Runtime': 'Thá»i lÆ°á»£ng (phĂºt)', 'count': 'Sá»‘ lÆ°á»£ng phim'},
                color_discrete_sequence=['#764ba2']
            )
            fig.update_layout(showlegend=False, bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart Runtime theo Genre - ÄÆ N GIáº¢N
    if 'Primary_Genre' in df_filtered.columns and 'Runtime' in df_filtered.columns:
        st.subheader("â±ï¸ Thá»i LÆ°á»£ng Trung BĂ¬nh Theo Thá»ƒ Loáº¡i")
        top_genres = df_filtered['Primary_Genre'].value_counts().head(8).index
        df_top_genres = df_filtered[df_filtered['Primary_Genre'].isin(top_genres)]
        
        avg_runtime = df_top_genres.groupby('Primary_Genre')['Runtime'].mean().sort_values().reset_index()
        
        fig = px.bar(
            avg_runtime,
            x='Runtime',
            y='Primary_Genre',
            orientation='h',
            title='Thá»i lÆ°á»£ng trung bĂ¬nh cá»§a Top 8 thá»ƒ loáº¡i',
            labels={'Runtime': 'Thá»i lÆ°á»£ng TB (phĂºt)', 'Primary_Genre': 'Thá»ƒ loáº¡i'},
            color='Runtime',
            color_continuous_scale='Blues',
            text='Runtime'
        )
        fig.update_traces(texttemplate='%{text:.0f} phĂºt', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 3: XU HÆ¯á»NG THá»œI GIAN ====================

with tabs[2]:
    st.header("đŸ“ˆ Xu HÆ°á»›ng Theo Thá»i Gian")
    
    if 'Year' in df_filtered.columns:
        # Sá»‘ lÆ°á»£ng phim theo nÄƒm
        movies_by_year = df_filtered.groupby('Year').size().reset_index(name='Count')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=movies_by_year['Year'],
            y=movies_by_year['Count'],
            fill='tozeroy',
            name='Sá»‘ lÆ°á»£ng phim',
            line=dict(color='royalblue', width=2)
        ))
        fig.update_layout(
            title='đŸ“ˆ Sá»‘ LÆ°á»£ng Phim Theo NÄƒm',
            xaxis_title='NÄƒm',
            yaxis_title='Sá»‘ lÆ°á»£ng phim',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Rating theo tháº­p ká»· - ÄÆ N GIáº¢N
        if 'Decade' in df_filtered.columns and 'Rating' in df_filtered.columns:
            st.subheader("â­ Xu HÆ°á»›ng Rating Theo Tháº­p Ká»·")
            
            rating_by_decade = df_filtered.groupby('Decade')['Rating'].mean().reset_index()
            
            fig = px.line(
                rating_by_decade,
                x='Decade',
                y='Rating',
                title='Rating trung bĂ¬nh theo tháº­p ká»·',
                labels={'Decade': 'Tháº­p ká»·', 'Rating': 'Rating TB'},
                markers=True
            )
            fig.update_traces(line=dict(color='orange', width=3), marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
        
        # Box Office trend
        if 'BoxOffice' in df_filtered.columns and df_filtered['BoxOffice'].notna().any():
            st.subheader("đŸ’° Xu HÆ°á»›ng Doanh Thu")
            
            boxoffice_by_year = df_filtered.groupby('Year')['BoxOffice'].sum().reset_index()
            
            fig = px.area(
                boxoffice_by_year,
                x='Year',
                y='BoxOffice',
                title='Tá»•ng doanh thu Box Office theo nÄƒm',
                labels={'BoxOffice': 'Doanh thu (USD)', 'Year': 'NÄƒm'}
            )
            st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 4: PHĂ‚N TĂCH SĂ‚U ====================

with tabs[3]:
    st.header("đŸ” PhĂ¢n TĂ­ch Má»‘i Quan Há»‡")
    
    # Bar chart: Rating trung bĂ¬nh theo nhĂ³m thá»i lÆ°á»£ng - Dá»„ HIá»‚U
    if 'Runtime' in df_filtered.columns and 'Rating' in df_filtered.columns:
        st.subheader("đŸ¬ Rating Theo Äá»™ DĂ i Phim")
        
        # Chia phim thĂ nh cĂ¡c nhĂ³m thá»i lÆ°á»£ng
        df_filtered['Runtime_Group'] = pd.cut(
            df_filtered['Runtime'], 
            bins=[0, 90, 120, 150, 300],
            labels=['Ngáº¯n (<90p)', 'TB (90-120p)', 'DĂ i (120-150p)', 'Ráº¥t dĂ i (>150p)']
        )
        
        runtime_rating = df_filtered.groupby('Runtime_Group')['Rating'].mean().reset_index()
        
        fig = px.bar(
            runtime_rating,
            x='Runtime_Group',
            y='Rating',
            title='Rating trung bĂ¬nh theo Ä‘á»™ dĂ i phim',
            labels={'Runtime_Group': 'Äá»™ dĂ i phim', 'Rating': 'Rating TB'},
            color='Rating',
            color_continuous_scale='Blues',
            text='Rating'
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart correlation - ÄÆ N GIáº¢N thay cho Heatmap
    st.subheader("ï¿½ Má»©c Äá»™ TÆ°Æ¡ng Quan")
    
    numeric_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_cols) > 1 and 'Rating' in numeric_cols:
        corr_with_rating = df_filtered[numeric_cols].corr()['Rating'].drop('Rating').sort_values()
        
        corr_df = pd.DataFrame({
            'Biáº¿n': corr_with_rating.index,
            'TÆ°Æ¡ng quan': corr_with_rating.values
        })
        
        fig = px.bar(
            corr_df,
            x='TÆ°Æ¡ng quan',
            y='Biáº¿n',
            orientation='h',
            title='TÆ°Æ¡ng quan vá»›i Rating IMDb',
            labels={'TÆ°Æ¡ng quan': 'Há»‡ sá»‘ tÆ°Æ¡ng quan', 'Biáº¿n': 'Biáº¿n sá»‘'},
            color='TÆ°Æ¡ng quan',
            color_continuous_scale='RdBu_r',
            text='TÆ°Æ¡ng quan'
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Pie chart thay cho Treemap - ÄÆ N GIáº¢N
    st.subheader("đŸ¥§ Top Thá»ƒ Loáº¡i Phá»• Biáº¿n")
    
    if 'Primary_Genre' in df_filtered.columns:
        genre_counts = df_filtered['Primary_Genre'].value_counts().head(10).reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig = px.pie(
            genre_counts,
            names='Genre',
            values='Count',
            title='Top 10 thá»ƒ loáº¡i phá»• biáº¿n nháº¥t',
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 5: TOP MOVIES ====================

with tabs[4]:
    st.header("đŸ† Top Movies")
    
    # Top rated
    if 'Rating' in df_filtered.columns:
        st.subheader("â­ Top 20 Phim Rating Cao Nháº¥t")
        
        top_rated = df_filtered.nlargest(20, 'Rating')[['Title', 'Year', 'Rating', 'Primary_Genre']]
        
        fig = px.bar(
            top_rated,
            x='Rating',
            y='Title',
            color='Primary_Genre',
            orientation='h',
            title='Top 20 phim cĂ³ rating cao nháº¥t',
            labels={'Rating': 'IMDb Rating', 'Title': ''},
            hover_data=['Year']
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Hiá»ƒn thá»‹ báº£ng
        st.dataframe(top_rated, use_container_width=True)
    
    # Top Box Office
    if 'BoxOffice' in df_filtered.columns and df_filtered['BoxOffice'].notna().any():
        st.subheader("đŸ’° Top 20 Phim Doanh Thu Cao Nháº¥t")
        
        top_boxoffice = df_filtered.nlargest(20, 'BoxOffice')[['Title', 'Year', 'BoxOffice', 'Rating']]
        top_boxoffice['BoxOffice_M'] = (top_boxoffice['BoxOffice'] / 1e6).round(1)
        
        fig = px.bar(
            top_boxoffice,
            x='BoxOffice_M',
            y='Title',
            orientation='h',
            title='Top 20 phim cĂ³ doanh thu cao nháº¥t',
            labels={'BoxOffice_M': 'Doanh thu (Triá»‡u USD)', 'Title': ''},
            color='Rating',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 6: INSIGHTS ====================

with tabs[5]:
    st.header("đŸ’¡ Key Insights & Storytelling")
    
    st.markdown("""
    <div class="insight-box">
        <h3>đŸ¯ Nhá»¯ng PhĂ¡t Hiá»‡n ChĂ­nh</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Insight 1: Rating Distribution
    if 'Rating' in df.columns:
        avg_rating = df['Rating'].mean()
        st.markdown(f"""
        ### 1. â­ PhĂ¢n Bá»‘ Rating
        
        - **Rating trung bĂ¬nh**: {avg_rating:.2f}/10
        - Pháº§n lá»›n cĂ¡c phim cĂ³ rating tá»« 7-9, cho tháº¥y dataset táº­p trung vĂ o cĂ¡c phim Ä‘Æ°á»£c Ä‘Ă¡nh giĂ¡ cao
        - Ráº¥t Ă­t phim cĂ³ rating dÆ°á»›i 5, Ä‘iá»u nĂ y pháº£n Ă¡nh viá»‡c chá»‰ nhá»¯ng phim cháº¥t lÆ°á»£ng má»›i Ä‘Æ°á»£c ghi nháº­n rá»™ng rĂ£i
        """)
    
    # Insight 2: Genre Analysis
    if 'Primary_Genre' in df.columns:
        top_genre = df['Primary_Genre'].value_counts().index[0]
        top_genre_count = df['Primary_Genre'].value_counts().values[0]
        
        st.markdown(f"""
        ### 2. đŸ­ Thá»ƒ Loáº¡i Phá»• Biáº¿n
        
        - **Thá»ƒ loáº¡i phá»• biáº¿n nháº¥t**: {top_genre} ({top_genre_count} phim)
        - Drama vĂ  Action lĂ  hai thá»ƒ loáº¡i chiáº¿m Æ°u tháº¿ trong ngĂ nh cĂ´ng nghiá»‡p Ä‘iá»‡n áº£nh
        - Phim hoáº¡t hĂ¬nh (Animation) ngĂ y cĂ ng phĂ¡t triá»ƒn máº¡nh, Ä‘áº·c biá»‡t tá»« tháº­p ká»· 2000
        """)
    
    # Insight 3: Time Trends
    if 'Year' in df.columns:
        st.markdown(f"""
        ### 3. đŸ“ˆ Xu HÆ°á»›ng Thá»i Gian
        
        - Sá»‘ lÆ°á»£ng phim sáº£n xuáº¥t tÄƒng Ä‘Ă¡ng ká»ƒ tá»« nhá»¯ng nÄƒm 1990
        - Tháº­p ká»· 2010-2020 chá»©ng kiáº¿n sá»± bĂ¹ng ná»• cá»§a phim siĂªu anh hĂ¹ng
        - COVID-19 (2020-2021) táº¡m thá»i lĂ m giĂ¡n Ä‘oáº¡n sáº£n xuáº¥t phim nhÆ°ng Ä‘Ă£ phá»¥c há»“i máº¡nh máº½
        """)
    
    # Insight 4: Runtime
    if 'Runtime' in df.columns:
        avg_runtime = df['Runtime'].mean()
        st.markdown(f"""
        ### 4. â±ï¸ Thá»i LÆ°á»£ng Phim
        
        - **Thá»i lÆ°á»£ng trung bĂ¬nh**: {avg_runtime:.0f} phĂºt
        - Phim hĂ nh Ä‘á»™ng thÆ°á»ng dĂ i hÆ¡n (120-150 phĂºt)
        - Phim hoáº¡t hĂ¬nh ngáº¯n hÆ¡n (80-100 phĂºt), phĂ¹ há»£p vá»›i khĂ¡n giáº£ tráº» em
        """)
    
    # Insight 5: Success Factors
    st.markdown("""
    ### 5. đŸ¯ Yáº¿u Tá»‘ ThĂ nh CĂ´ng
    
    - **Rating cao** khĂ´ng hoĂ n toĂ n tÆ°Æ¡ng quan vá»›i **doanh thu cao**
    - Thá»ƒ loáº¡i Action/Adventure thÆ°á»ng cĂ³ doanh thu tá»‘t hÆ¡n Drama
    - Äáº¡o diá»…n ná»•i tiáº¿ng (Nolan, Spielberg, Cameron) cĂ³ áº£nh hÆ°á»Ÿng lá»›n Ä‘áº¿n thĂ nh cĂ´ng phim
    - Marketing vĂ  thÆ°Æ¡ng hiá»‡u (Marvel, DC) Ä‘Ă³ng vai trĂ² quan trá»ng
    """)
    
    # WordCloud
    st.markdown("---")
    st.subheader("â˜ï¸ WordCloud TiĂªu Äá» Phim")
    
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
    
    # Conclusion
    st.markdown("""
    <div class="insight-box">
        <h3>đŸ¬ Káº¿t Luáº­n</h3>
        <p>
        PhĂ¢n tĂ­ch dá»¯ liá»‡u phim IMDb cho tháº¥y ngĂ nh cĂ´ng nghiá»‡p Ä‘iá»‡n áº£nh Ä‘Ă£ cĂ³ sá»± phĂ¡t triá»ƒn vÆ°á»£t báº­c 
        trong nhá»¯ng tháº­p ká»· gáº§n Ä‘Ă¢y. Sá»± Ä‘a dáº¡ng vá» thá»ƒ loáº¡i, cĂ´ng nghá»‡ tiĂªn tiáº¿n, vĂ  mĂ´ hĂ¬nh kinh doanh 
        má»›i Ä‘Ă£ táº¡o ra nhiá»u cÆ¡ há»™i cho cĂ¡c nhĂ  lĂ m phim. Tuy nhiĂªn, cháº¥t lÆ°á»£ng ná»™i dung váº«n lĂ  yáº¿u tá»‘ 
        quan trá»ng nháº¥t Ä‘á»ƒ táº¡o nĂªn nhá»¯ng tĂ¡c pháº©m kinh Ä‘iá»ƒn báº¥t há»§.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>đŸ“ <b>IMDb Movie Data Storytelling Project</b></p>
    <p>ÄÆ°á»£c xĂ¢y dá»±ng vá»›i â¤ï¸ báº±ng Python, Streamlit & Plotly</p>
    <p>Data Science Mid-term Project</p>
</div>
""", unsafe_allow_html=True)

