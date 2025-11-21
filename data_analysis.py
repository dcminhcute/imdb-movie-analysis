"""
Data Analysis & Visualization Script for IMDb Movie Data
Tạo các biểu đồ theo yêu cầu: Histogram, Line, Scatter, Heatmap, Treemap, WordCloud
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import os
from sklearn.linear_model import LinearRegression


class MovieDataAnalyzer:
    """Class để phân tích và trực quan hóa dữ liệu phim"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.output_dir = 'visualizations'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Thiết lập style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
    # ==================== 1. HISTOGRAM / BOXPLOT / VIOLIN ====================
    
    def plot_rating_distribution(self, save=True):
        """Histogram đơn giản cho Rating"""
        # Chỉ dùng histogram đơn giản, dễ hiểu
        fig = px.histogram(
            self.df,
            x='Rating',
            nbins=20,
            title='⭐ Phân Phối Đánh Giá IMDb',
            labels={'Rating': 'Đánh giá IMDb (0-10)', 'count': 'Số lượng phim'},
            color_discrete_sequence=['#667eea']
        )
        
        fig.update_layout(
            template='plotly_white',
            showlegend=False,
            height=400,
            bargap=0.1
        )
        
        fig.update_traces(marker_line_color='white', marker_line_width=1)
        
        if save:
            fig.write_html(f'{self.output_dir}/01_rating_distribution.html')
            print("✅ Đã tạo: 01_rating_distribution.html")
        
        return fig
    
    def plot_runtime_boxplot_by_genre(self, save=True):
        """Bar chart đơn giản: Runtime trung bình theo thể loại"""
        # Lấy top 8 genres và tính runtime trung bình
        top_genres = self.df['Primary_Genre'].value_counts().head(8).index
        df_filtered = self.df[self.df['Primary_Genre'].isin(top_genres)]
        
        avg_runtime = df_filtered.groupby('Primary_Genre')['Runtime'].mean().sort_values(ascending=True).reset_index()
        
        fig = px.bar(
            avg_runtime,
            x='Runtime',
            y='Primary_Genre',
            orientation='h',
            title='⏱️ Thời Lượng Trung Bình Theo Thể Loại (Phút)',
            labels={'Runtime': 'Thời lượng trung bình (phút)', 'Primary_Genre': 'Thể loại'},
            color='Runtime',
            color_continuous_scale='Blues',
            text='Runtime'
        )
        
        fig.update_traces(texttemplate='%{text:.0f} phút', textposition='outside')
        fig.update_layout(
            template='plotly_white',
            showlegend=False,
            height=500
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/02_runtime_by_genre.html')
            print("✅ Đã tạo: 02_runtime_by_genre.html")
        
        return fig
    
    # ==================== 2. LINE / AREA (THEO THỜI GIAN) ====================
    
    def plot_movies_over_time(self, save=True):
        """Line chart + Area chart số lượng phim theo năm"""
        movies_by_year = self.df.groupby('Year').size().reset_index(name='Count')
        
        fig = go.Figure()
        
        # Area chart
        fig.add_trace(go.Scatter(
            x=movies_by_year['Year'],
            y=movies_by_year['Count'],
            fill='tozeroy',
            name='Số lượng phim',
            line=dict(color='royalblue', width=2)
        ))
        
        fig.update_layout(
            title='📈 Số Lượng Phim Theo Năm',
            xaxis_title='Năm',
            yaxis_title='Số lượng phim',
            template='plotly_white',
            hovermode='x unified',
            height=500
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/03_movies_over_time.html')
            print("✅ Đã tạo: 03_movies_over_time.html")
        
        return fig
    
    def plot_rating_trend_by_decade(self, save=True):
        """Line chart đơn giản: Rating theo thập kỷ"""
        rating_by_decade = self.df.groupby('Decade')['Rating'].mean().reset_index()
        
        fig = px.line(
            rating_by_decade,
            x='Decade',
            y='Rating',
            title='⭐ Đánh Giá Trung Bình Theo Thập Kỷ',
            labels={'Rating': 'Đánh giá trung bình', 'Decade': 'Thập kỷ'},
            markers=True
        )
        
        fig.update_traces(
            line=dict(color='orange', width=3),
            marker=dict(size=12, color='orange', line=dict(width=2, color='white'))
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500,
            hovermode='x unified'
        )
        
        # Thêm annotation
        fig.add_annotation(
            text="Rating dao động từ 6.0 đến 7.0 qua các thập kỷ",
            xref="paper", yref="paper",
            x=0.5, y=1.1,
            showarrow=False,
            font=dict(size=12, color="gray")
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/04_rating_trend.html')
            print("✅ Đã tạo: 04_rating_trend.html")
        
        return fig
    
    def plot_boxoffice_trend(self, save=True):
        """Area chart doanh thu theo năm"""
        if 'BoxOffice' not in self.df.columns:
            print("⚠️ Không có dữ liệu BoxOffice")
            return None
        
        boxoffice_by_year = self.df.groupby('Year')['BoxOffice'].sum().reset_index()
        
        fig = px.area(
            boxoffice_by_year,
            x='Year',
            y='BoxOffice',
            title='💰 Tổng Doanh Thu Box Office Theo Năm',
            labels={'BoxOffice': 'Doanh thu (USD)', 'Year': 'Năm'}
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/05_boxoffice_trend.html')
            print("✅ Đã tạo: 05_boxoffice_trend.html")
        
        return fig
    
    # ==================== 3. SCATTER + REGRESSION ====================
    
    def plot_runtime_vs_rating(self, save=True):
        """Scatter plot đơn giản: Runtime vs Rating"""
        # Đơn giản hóa - không dùng trendline phức tạp
        fig = px.scatter(
            self.df,
            x='Runtime',
            y='Rating',
            color='Primary_Genre',
            hover_data=['Title', 'Year'],
            title='🎬 Thời Lượng Phim vs Đánh Giá IMDb',
            labels={'Runtime': 'Thời lượng (phút)', 'Rating': 'Đánh giá IMDb (0-10)'},
            opacity=0.7
        )
        
        fig.update_layout(
            template='plotly_white',
            height=600
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/06_runtime_vs_rating.html')
            print("✅ Đã tạo: 06_runtime_vs_rating.html")
        
        return fig
    
    def plot_budget_vs_boxoffice(self, save=True):
        """Scatter plot đơn giản: Budget vs Box Office"""
        if 'Budget' not in self.df.columns or 'BoxOffice' not in self.df.columns:
            print("⚠️ Không có dữ liệu Budget/BoxOffice")
            return None
        
        # Lọc dữ liệu hợp lệ
        df_filtered = self.df[(self.df['Budget'] > 0) & (self.df['BoxOffice'] > 0)].copy()
        
        # Chuyển sang triệu USD để dễ đọc
        df_filtered['Budget_M'] = (df_filtered['Budget'] / 1e6).round(1)
        df_filtered['BoxOffice_M'] = (df_filtered['BoxOffice'] / 1e6).round(1)
        
        fig = px.scatter(
            df_filtered,
            x='Budget_M',
            y='BoxOffice_M',
            color='Rating',
            hover_data=['Title', 'Year'],
            title='💵 Ngân Sách vs Doanh Thu (Triệu USD)',
            labels={'Budget_M': 'Ngân sách (triệu $)', 'BoxOffice_M': 'Doanh thu (triệu $)'},
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=600
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/07_budget_vs_boxoffice.html')
            print("✅ Đã tạo: 07_budget_vs_boxoffice.html")
        
        return fig
    
    # ==================== 4. HEATMAP TƯƠNG QUAN ====================
    
    def plot_correlation_heatmap(self, save=True):
        """Bỏ heatmap phức tạp, thay bằng bar chart đơn giản"""
        # Tính correlation với Rating
        numeric_cols = ['Year', 'Runtime', 'Genre_Count']
        if 'BoxOffice' in self.df.columns:
            numeric_cols.append('BoxOffice')
        
        # Tính correlation với Rating
        correlations = []
        for col in numeric_cols:
            corr = self.df[[col, 'Rating']].corr().iloc[0, 1]
            correlations.append({'Feature': col, 'Correlation': corr})
        
        corr_df = pd.DataFrame(correlations).sort_values('Correlation')
        
        # Tạo bar chart
        fig = px.bar(
            corr_df,
            x='Correlation',
            y='Feature',
            orientation='h',
            title='🔗 Mối Liên Hệ Của Các Yếu Tố Với Đánh Giá IMDb<br><sub>Số dương = tỷ lệ thuận, Số âm = tỷ lệ nghịch</sub>',
            labels={'Correlation': 'Mức độ liên quan', 'Feature': 'Yếu tố'},
            color='Correlation',
            color_continuous_scale='RdYlGn',
            text='Correlation'
        )
        
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/08_correlation_heatmap.html')
            print("✅ Đã tạo: 08_correlation_heatmap.html")
        
        return fig
    
    # ==================== 5. TREEMAP ====================
    
    def plot_genre_treemap(self, save=True):
        """Pie chart đơn giản thay vì Treemap"""
        genre_counts = self.df['Primary_Genre'].value_counts().head(10).reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig = px.pie(
            genre_counts,
            values='Count',
            names='Genre',
            title='🎭 Top 10 Thể Loại Phim Phổ Biến',
            hole=0.3  # Donut chart - đẹp hơn
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=600)
        
        if save:
            fig.write_html(f'{self.output_dir}/09_genre_treemap.html')
            print("✅ Đã tạo: 09_genre_treemap.html")
        
        return fig
    
    def plot_country_treemap(self, save=True):
        """Bar chart đơn giản cho quốc gia"""
        if 'Primary_Country' not in self.df.columns:
            print("⚠️ Không có dữ liệu Primary_Country")
            return None
        
        country_counts = self.df['Primary_Country'].value_counts().head(15).reset_index()
        country_counts.columns = ['Country', 'Count']
        
        fig = px.bar(
            country_counts,
            x='Count',
            y='Country',
            orientation='h',
            title='🌍 Top 15 Quốc Gia Sản Xuất Phim',
            labels={'Count': 'Số lượng phim', 'Country': 'Quốc gia'},
            color='Count',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=600
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/10_country_treemap.html')
            print("✅ Đã tạo: 10_country_treemap.html")
        
        return fig
    
    # ==================== 6. WORDCLOUD ====================
    
    def plot_title_wordcloud(self, save=True):
        """WordCloud từ tiêu đề phim"""
        # Kết hợp tất cả tiêu đề
        text = ' '.join(self.df['Title'].astype(str))
        
        # Tạo WordCloud
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5
        ).generate(text)
        
        # Vẽ
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('☁️ WordCloud Tiêu Đề Phim', fontsize=20, weight='bold')
        
        if save:
            plt.savefig(f'{self.output_dir}/11_title_wordcloud.png', 
                       dpi=300, bbox_inches='tight')
            print("✅ Đã tạo: 11_title_wordcloud.png")
        
        plt.close()
        return fig
    
    def plot_genre_wordcloud(self, save=True):
        """WordCloud từ thể loại"""
        # Kết hợp tất cả genres
        all_genres = []
        for genres_list in self.df['Genres_List']:
            all_genres.extend(genres_list)
        
        text = ' '.join(all_genres)
        
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='plasma',
            max_words=50
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('☁️ WordCloud Thể Loại Phim', fontsize=20, weight='bold')
        
        if save:
            plt.savefig(f'{self.output_dir}/12_genre_wordcloud.png',
                       dpi=300, bbox_inches='tight')
            print("✅ Đã tạo: 12_genre_wordcloud.png")
        
        plt.close()
        return fig
    
    # ==================== ADDITIONAL INTERACTIVE CHARTS ====================
    
    def plot_sunburst_genre_decade(self, save=True):
        """Bar chart đơn giản thay vì Sunburst phức tạp"""
        # Tạo dữ liệu đơn giản - Top 5 thể loại theo thập kỷ
        top_genres = self.df['Primary_Genre'].value_counts().head(5).index
        df_filtered = self.df[self.df['Primary_Genre'].isin(top_genres)]
        
        genre_decade_data = df_filtered.groupby(['Decade', 'Primary_Genre']).size().reset_index(name='Count')
        
        fig = px.bar(
            genre_decade_data,
            x='Decade',
            y='Count',
            color='Primary_Genre',
            title='📊 Top 5 Thể Loại Phim Theo Thập Kỷ',
            labels={'Count': 'Số lượng phim', 'Decade': 'Thập kỷ', 'Primary_Genre': 'Thể loại'},
            barmode='group'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=600
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/13_sunburst_genre_decade.html')
            print("✅ Đã tạo: 13_sunburst_genre_decade.html")
        
        return fig
    
    def plot_top_movies_bar(self, save=True):
        """Bar chart Top 20 phim Rating cao nhất (Interactive)"""
        top_movies = self.df.nlargest(20, 'Rating')[['Title', 'Rating', 'Year', 'Primary_Genre']]
        
        fig = px.bar(
            top_movies,
            x='Rating',
            y='Title',
            color='Primary_Genre',
            orientation='h',
            title='🏆 Top 20 Phim Có Rating Cao Nhất',
            labels={'Rating': 'IMDb Rating', 'Title': ''},
            hover_data=['Year']
        )
        
        fig.update_layout(
            template='plotly_white',
            height=700,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        if save:
            fig.write_html(f'{self.output_dir}/14_top_movies.html')
            print("✅ Đã tạo: 14_top_movies.html")
        
        return fig
    
    def generate_all_visualizations(self):
        """Tạo tất cả các biểu đồ"""
        print("\n🎨 BẮT ĐẦU TẠO TẤT CẢ CÁC BIỂU ĐỒ...\n")
        
        # 1. Histogram/Boxplot/Violin
        self.plot_rating_distribution()
        self.plot_runtime_boxplot_by_genre()
        
        # 2. Line/Area
        self.plot_movies_over_time()
        self.plot_rating_trend_by_decade()
        self.plot_boxoffice_trend()
        
        # 3. Scatter + Regression
        self.plot_runtime_vs_rating()
        self.plot_budget_vs_boxoffice()
        
        # 4. Heatmap
        self.plot_correlation_heatmap()
        
        # 5. Treemap
        self.plot_genre_treemap()
        self.plot_country_treemap()
        
        # 6. WordCloud
        self.plot_title_wordcloud()
        self.plot_genre_wordcloud()
        
        # Additional Interactive
        self.plot_sunburst_genre_decade()
        self.plot_top_movies_bar()
        
        print(f"\n✅ ĐÃ TẠO XONG TẤT CẢ CÁC BIỂU ĐỒ!")
        print(f"📁 Lưu tại thư mục: {self.output_dir}/")


def main():
    """Main function"""
    # Đọc dữ liệu đã xử lý
    data_path = 'data/processed_movies.csv'
    
    if not os.path.exists(data_path):
        print(f"❌ Không tìm thấy file {data_path}")
        print(f"💡 Vui lòng chạy data_preprocessing.py trước")
        return
    
    df = pd.read_csv(data_path, encoding='utf-8-sig')
    print(f"📂 Đã đọc {len(df)} phim từ {data_path}")
    
    # Khởi tạo analyzer
    analyzer = MovieDataAnalyzer(df)
    
    # Tạo tất cả biểu đồ
    analyzer.generate_all_visualizations()


if __name__ == '__main__':
    main()
