"""
Data Preprocessing Script for IMDb Movie Data
Chuẩn hóa kiểu dữ liệu, xử lý missing values, tạo features mới
"""

import pandas as pd
import numpy as np
import re
import os


class MovieDataPreprocessor:
    """Class để tiền xử lý dữ liệu phim"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def clean_year(self):
        """Chuẩn hóa cột Year"""
        if 'Year' in self.df.columns:
            # Chuyển về dạng số, xử lý các giá trị không hợp lệ
            self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce')
            # Lọc các năm hợp lý (1900-2025)
            self.df['Year'] = self.df['Year'].apply(
                lambda x: x if 1900 <= x <= 2025 else np.nan
            )
            print(f"✅ Đã chuẩn hóa cột Year")
        return self
    
    def clean_rating(self):
        """Chuẩn hóa cột Rating (imdbRating)"""
        rating_cols = ['imdbRating', 'Rating']
        
        for col in rating_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                # Rating từ 0-10
                self.df[col] = self.df[col].apply(
                    lambda x: x if 0 <= x <= 10 else np.nan
                )
                print(f"✅ Đã chuẩn hóa cột {col}")
        
        # Rename để thống nhất
        if 'imdbRating' in self.df.columns:
            self.df.rename(columns={'imdbRating': 'Rating'}, inplace=True)
            
        return self
    
    def clean_runtime(self):
        """Chuẩn hóa cột Runtime (phút)"""
        if 'Runtime' in self.df.columns:
            # Xử lý string dạng "142 min" -> 142
            if self.df['Runtime'].dtype == 'object':
                self.df['Runtime'] = self.df['Runtime'].apply(
                    lambda x: re.findall(r'\d+', str(x))[0] if pd.notna(x) and re.findall(r'\d+', str(x)) else np.nan
                )
            self.df['Runtime'] = pd.to_numeric(self.df['Runtime'], errors='coerce')
            print(f"✅ Đã chuẩn hóa cột Runtime")
        return self
    
    def clean_box_office(self):
        """Chuẩn hóa cột BoxOffice (USD)"""
        if 'BoxOffice' in self.df.columns:
            # Xử lý string dạng "$123,456,789" -> 123456789
            if self.df['BoxOffice'].dtype == 'object':
                self.df['BoxOffice'] = self.df['BoxOffice'].apply(
                    lambda x: re.sub(r'[^\d]', '', str(x)) if pd.notna(x) else np.nan
                )
            self.df['BoxOffice'] = pd.to_numeric(self.df['BoxOffice'], errors='coerce')
            print(f"✅ Đã chuẩn hóa cột BoxOffice")
        return self
    
    def clean_budget(self):
        """Chuẩn hóa cột Budget"""
        if 'Budget' in self.df.columns:
            if self.df['Budget'].dtype == 'object':
                self.df['Budget'] = self.df['Budget'].apply(
                    lambda x: re.sub(r'[^\d]', '', str(x)) if pd.notna(x) else np.nan
                )
            self.df['Budget'] = pd.to_numeric(self.df['Budget'], errors='coerce')
            print(f"✅ Đã chuẩn hóa cột Budget")
        return self
    
    def split_genres(self):
        """Tách cột Genre thành list"""
        if 'Genre' in self.df.columns:
            # Tách theo dấu phẩy
            self.df['Genres_List'] = self.df['Genre'].apply(
                lambda x: [g.strip() for g in str(x).split(',')] if pd.notna(x) else []
            )
            # Lấy genre đầu tiên làm primary genre
            self.df['Primary_Genre'] = self.df['Genres_List'].apply(
                lambda x: x[0] if len(x) > 0 else 'Unknown'
            )
            # Đếm số genre
            self.df['Genre_Count'] = self.df['Genres_List'].apply(len)
            print(f"✅ Đã tách cột Genre")
        return self
    
    def extract_country(self):
        """Lấy quốc gia chính"""
        if 'Country' in self.df.columns:
            # Lấy quốc gia đầu tiên
            self.df['Primary_Country'] = self.df['Country'].apply(
                lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Unknown'
            )
            print(f"✅ Đã trích xuất quốc gia chính")
        return self
    
    def create_decade(self):
        """Tạo cột Decade (thập kỷ)"""
        if 'Year' in self.df.columns:
            self.df['Decade'] = (self.df['Year'] // 10 * 10).astype('Int64')
            print(f"✅ Đã tạo cột Decade")
        return self
    
    def create_roi(self):
        """Tạo cột ROI (Return on Investment)"""
        if 'BoxOffice' in self.df.columns and 'Budget' in self.df.columns:
            self.df['ROI'] = (
                (self.df['BoxOffice'] - self.df['Budget']) / self.df['Budget'] * 100
            ).round(2)
            self.df['ROI'] = self.df['ROI'].replace([np.inf, -np.inf], np.nan)
            print(f"✅ Đã tạo cột ROI")
        return self
    
    def create_profit(self):
        """Tạo cột Profit"""
        if 'BoxOffice' in self.df.columns and 'Budget' in self.df.columns:
            self.df['Profit'] = self.df['BoxOffice'] - self.df['Budget']
            print(f"✅ Đã tạo cột Profit")
        return self
    
    def categorize_rating(self):
        """Phân loại Rating thành các nhóm"""
        if 'Rating' in self.df.columns:
            self.df['Rating_Category'] = pd.cut(
                self.df['Rating'],
                bins=[0, 5, 7, 8, 10],
                labels=['Poor', 'Average', 'Good', 'Excellent']
            )
            print(f"✅ Đã phân loại Rating")
        return self
    
    def categorize_runtime(self):
        """Phân loại Runtime"""
        if 'Runtime' in self.df.columns:
            self.df['Runtime_Category'] = pd.cut(
                self.df['Runtime'],
                bins=[0, 90, 120, 150, 300],
                labels=['Short', 'Medium', 'Long', 'Very Long']
            )
            print(f"✅ Đã phân loại Runtime")
        return self
    
    def handle_missing_values(self):
        """Xử lý missing values"""
        print("\n📊 Xử lý missing values:")
        
        # Điền giá trị cho các cột số
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                # Điền median cho numeric
                self.df[col].fillna(self.df[col].median(), inplace=True)
                print(f"  - {col}: Điền {missing_count} giá trị bằng median")
        
        # Điền giá trị cho các cột string
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                self.df[col].fillna('Unknown', inplace=True)
                print(f"  - {col}: Điền {missing_count} giá trị bằng 'Unknown'")
        
        return self
    
    def remove_duplicates(self):
        """Loại bỏ các bản ghi trùng lặp"""
        initial_count = len(self.df)
        
        # Xóa trùng dựa trên Title và Year
        if 'Title' in self.df.columns and 'Year' in self.df.columns:
            self.df.drop_duplicates(subset=['Title', 'Year'], keep='first', inplace=True)
        else:
            self.df.drop_duplicates(inplace=True)
        
        removed_count = initial_count - len(self.df)
        if removed_count > 0:
            print(f"✅ Đã loại bỏ {removed_count} bản ghi trùng lặp")
        return self
    
    def get_processed_data(self):
        """Trả về DataFrame đã xử lý"""
        return self.df
    
    def save_processed_data(self, output_path: str = 'data/processed_movies.csv'):
        """Lưu dữ liệu đã xử lý"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n💾 Đã lưu dữ liệu đã xử lý vào {output_path}")
        print(f"   - Số lượng phim: {len(self.df)}")
        print(f"   - Số cột: {len(self.df.columns)}")
        return self


def preprocess_movie_data(input_path: str = 'data/raw_movies.csv', 
                         output_path: str = 'data/processed_movies.csv'):
    """
    Function chính để xử lý dữ liệu phim
    
    Args:
        input_path: Đường dẫn file input
        output_path: Đường dẫn file output
    """
    print("🔧 BẮT ĐẦU TIỀN XỬ LÝ DỮ LIỆU\n")
    
    # Đọc dữ liệu
    df = pd.read_csv(input_path, encoding='utf-8-sig')
    print(f"📂 Đã đọc {len(df)} phim từ {input_path}\n")
    
    # Chuẩn hóa tên cột để thống nhất
    column_mapping = {
        'Runtime (Minutes)': 'Runtime',
        'Revenue (Millions)': 'BoxOffice',
        'Rank': 'ID'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # Chuyển BoxOffice từ triệu sang đơn vị bình thường
    if 'BoxOffice' in df.columns:
        df['BoxOffice'] = df['BoxOffice'] * 1_000_000
    
    print("✅ Đã chuẩn hóa tên cột\n")
    
    # Khởi tạo preprocessor
    preprocessor = MovieDataPreprocessor(df)
    
    # Thực hiện các bước xử lý
    processed_df = (preprocessor
                    .remove_duplicates()
                    .clean_year()
                    .clean_rating()
                    .clean_runtime()
                    .clean_box_office()
                    .clean_budget()
                    .split_genres()
                    .extract_country()
                    .create_decade()
                    .create_roi()
                    .create_profit()
                    .categorize_rating()
                    .categorize_runtime()
                    .handle_missing_values()
                    .save_processed_data(output_path)
                    .get_processed_data())
    
    # Hiển thị thông tin
    print(f"\n📈 THỐNG KÊ DỮ LIỆU SAU XỬ LÝ:")
    print(f"   - Số phim: {len(processed_df)}")
    print(f"   - Năm từ: {processed_df['Year'].min():.0f} đến {processed_df['Year'].max():.0f}")
    print(f"   - Rating trung bình: {processed_df['Rating'].mean():.2f}")
    
    if 'Runtime' in processed_df.columns:
        print(f"   - Runtime trung bình: {processed_df['Runtime'].mean():.0f} phút")
    
    if 'BoxOffice' in processed_df.columns:
        print(f"   - BoxOffice trung bình: ${processed_df['BoxOffice'].mean():,.0f}")
    
    print(f"\n✅ HOÀN THÀNH TIỀN XỬ LÝ DỮ LIỆU!")
    
    return processed_df


def main():
    """Main function"""
    # Kiểm tra file input
    input_path = 'data/raw_movies.csv'
    
    if not os.path.exists(input_path):
        print(f"❌ Không tìm thấy file {input_path}")
        print(f"💡 Vui lòng chạy data_collection.py trước")
        return
    
    # Xử lý dữ liệu
    preprocess_movie_data(input_path)


if __name__ == '__main__':
    main()
