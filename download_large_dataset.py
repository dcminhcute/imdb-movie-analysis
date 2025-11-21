"""
Download Large IMDb Dataset
Tải dataset lớn hơn (1000+ phim) từ nguồn công khai
"""

import pandas as pd
import requests
import os

def download_imdb_dataset():
    """
    Tải dataset IMDb từ GitHub (IMDb Top 1000)
    Nguồn: Công khai, không cần API key
    """
    print("🎬 Đang tải IMDb Top 1000 Movies Dataset...")
    print("📍 Nguồn: GitHub Public Dataset\n")
    
    # Danh sách các URL dataset công khai (thử lần lượt)
    urls = [
        # Dataset mới nhất có phim đến 2024
        "https://raw.githubusercontent.com/danielgrijalva/movie-stats/master/movies.csv",
        # Dataset dự phòng
        "https://raw.githubusercontent.com/LearnDataSci/articles/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv",
    ]
    
    # Thử từng URL cho đến khi thành công
    df = None
    for url in urls:
        print(f"🔄 Đang thử: {url}")
        url = url  # Gán URL hiện tại
    
    # Thử tải từng URL
    for idx, url in enumerate(urls, 1):
        try:
            print(f"\n🔄 [{idx}/{len(urls)}] Đang thử tải từ URL...")
            print("⏳ Đang tải... (có thể mất vài giây)")
            df = pd.read_csv(url)
            
            print(f"✅ Đã tải thành công {len(df)} phim!")
            
            # Hiển thị thông tin
            print(f"\n📊 Thông tin dataset:")
            print(f"   - Số lượng phim: {len(df)}")
            print(f"   - Số cột: {len(df.columns)}")
            print(f"   - Các cột: {', '.join(df.columns.tolist())}")
            break  # Thành công thì thoát vòng lặp
            
        except Exception as e:
            print(f"❌ Lỗi với URL {idx}: {e}")
            if idx < len(urls):
                print("🔄 Thử URL tiếp theo...")
            continue
    
    if df is None:
        raise Exception("Không thể tải dataset từ bất kỳ URL nào")
    
    try:
        
        # Chuẩn hóa tên cột để phù hợp với code hiện tại
        column_mapping = {
            # Mapping cho dataset mới
            'name': 'Title',
            'year': 'Year',
            'score': 'Rating',
            'votes': 'imdbVotes',
            'gross': 'BoxOffice',
            'runtime': 'Runtime',
            'country': 'Country',
            'company': 'Production',
            'director': 'Director',
            'writer': 'Writer',
            'star': 'Actors',
            # Mapping cho dataset cũ
            'Series_Title': 'Title',
            'Released_Year': 'Year',
            'IMDB_Rating': 'Rating',
            'Overview': 'Plot',
            'Meta_score': 'Metascore',
            'No_of_Votes': 'imdbVotes',
            'Gross': 'BoxOffice',
            'Runtime (Minutes)': 'Runtime'
        }
        
        # Đổi tên cột nếu tồn tại
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        # Tạo thư mục data nếu chưa có
        os.makedirs('data', exist_ok=True)
        
        # Lưu file
        output_path = 'data/raw_movies.csv'
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"\n💾 Đã lưu tại: {output_path}")
        # Kiểm tra năm phim
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
            year_min = df['Year'].min()
            year_max = df['Year'].max()
            print(f"   - Khoảng năm: {year_min:.0f} - {year_max:.0f}")
        
        print(f"\n🎯 Bước tiếp theo:")
        print(f"   1. Chạy: python data_preprocessing.py")
        print(f"   2. Chạy: python data_analysis.py")
        print(f"   3. Chạy: streamlit run app.py")
        
        return df
        
    except Exception as e:
        print(f"\n❌ Lỗi khi xử lý dataset: {e}")
        print(f"\n💡 Giải pháp thay thế:")
        print(f"   1. Kiểm tra kết nối internet")
        print(f"   2. Hoặc tải thủ công từ:")
        print(f"      https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows")
        print(f"   3. Sau đó đặt file vào thư mục 'data/raw_movies.csv'")
        return None


def download_alternative_dataset():
    """
    Dataset dự phòng - Tạo dataset mở rộng từ dữ liệu mẫu
    """
    print("\n🎬 Tạo dataset mở rộng (Phương án dự phòng)...")
    
    # Danh sách phim mở rộng
    movies_data = []
    
    # Top movies từ nhiều thập kỷ và thể loại khác nhau
    movie_list = [
        # 1970s Classics
        ("The Godfather", 1972, 9.2, "Crime, Drama", "Francis Ford Coppola", 175, "USA", 134821952, "English, Italian, Latin"),
        ("Star Wars", 1977, 8.6, "Action, Adventure, Fantasy", "George Lucas", 121, "USA", 322740140, "English"),
        ("Alien", 1979, 8.5, "Horror, Sci-Fi", "Ridley Scott", 117, "USA, UK", 78900000, "English"),
        
        # 1980s Blockbusters
        ("The Shining", 1980, 8.4, "Drama, Horror", "Stanley Kubrick", 146, "USA, UK", 44017374, "English"),
        ("E.T. the Extra-Terrestrial", 1982, 7.9, "Family, Sci-Fi", "Steven Spielberg", 115, "USA", 435110554, "English"),
        ("Back to the Future", 1985, 8.5, "Adventure, Comedy, Sci-Fi", "Robert Zemeckis", 116, "USA", 210609762, "English"),
        ("Die Hard", 1988, 8.2, "Action, Thriller", "John McTiernan", 132, "USA", 83008852, "English"),
        
        # 1990s Masterpieces  
        ("The Shawshank Redemption", 1994, 9.3, "Drama", "Frank Darabont", 142, "USA", 28341469, "English"),
        ("Pulp Fiction", 1994, 8.9, "Crime, Drama", "Quentin Tarantino", 154, "USA", 107928762, "English"),
        ("Forrest Gump", 1994, 8.8, "Drama, Romance", "Robert Zemeckis", 142, "USA", 330252182, "English"),
        ("The Lion King", 1994, 8.5, "Animation, Adventure, Drama", "Roger Allers, Rob Minkoff", 88, "USA", 422783777, "English"),
        ("The Silence of the Lambs", 1991, 8.6, "Crime, Drama, Thriller", "Jonathan Demme", 118, "USA", 130742922, "English"),
        ("Goodfellas", 1990, 8.7, "Crime, Drama", "Martin Scorsese", 145, "USA", 46836394, "English"),
        ("Jurassic Park", 1993, 8.2, "Action, Adventure, Sci-Fi", "Steven Spielberg", 127, "USA", 402453882, "English"),
        ("Schindler's List", 1993, 9.0, "Biography, Drama, History", "Steven Spielberg", 195, "USA", 96898818, "English, Hebrew, German"),
        ("Toy Story", 1995, 8.3, "Animation, Adventure, Comedy", "John Lasseter", 81, "USA", 373554033, "English"),
        ("The Matrix", 1999, 8.7, "Action, Sci-Fi", "Lana Wachowski, Lilly Wachowski", 136, "USA", 171479930, "English"),
        ("Saving Private Ryan", 1998, 8.6, "Drama, War", "Steven Spielberg", 169, "USA", 216540909, "English"),
        ("The Green Mile", 1999, 8.6, "Crime, Drama, Fantasy", "Frank Darabont", 189, "USA", 136801374, "English"),
        ("Fight Club", 1999, 8.8, "Drama", "David Fincher", 139, "USA", 37030102, "English"),
        
        # 2000s Cinema
        ("Gladiator", 2000, 8.5, "Action, Adventure, Drama", "Ridley Scott", 155, "USA, UK", 187705427, "English"),
        ("The Lord of the Rings: The Fellowship", 2001, 8.8, "Action, Adventure, Drama", "Peter Jackson", 178, "New Zealand, USA", 315544750, "English"),
        ("The Lord of the Rings: The Return of the King", 2003, 9.0, "Action, Adventure, Drama", "Peter Jackson", 201, "New Zealand, USA", 377845905, "English"),
        ("Finding Nemo", 2003, 8.2, "Animation, Adventure, Comedy", "Andrew Stanton", 100, "USA", 380843261, "English"),
        ("The Prestige", 2006, 8.5, "Drama, Mystery, Thriller", "Christopher Nolan", 130, "USA, UK", 53089891, "English"),
        ("The Departed", 2006, 8.5, "Crime, Drama, Thriller", "Martin Scorsese", 151, "USA, Hong Kong", 132384315, "English"),
        ("The Dark Knight", 2008, 9.0, "Action, Crime, Drama", "Christopher Nolan", 152, "USA, UK", 534858444, "English"),
        ("WALL-E", 2008, 8.4, "Animation, Adventure, Family", "Andrew Stanton", 98, "USA", 223808164, "English"),
        ("Up", 2009, 8.3, "Animation, Adventure, Comedy", "Pete Docter", 96, "USA", 293004164, "English"),
        ("Avatar", 2009, 7.9, "Action, Adventure, Fantasy", "James Cameron", 162, "USA, UK", 760507625, "English"),
        
        # 2010s Modern Classics
        ("Inception", 2010, 8.8, "Action, Sci-Fi, Thriller", "Christopher Nolan", 148, "USA, UK", 292576195, "English"),
        ("Toy Story 3", 2010, 8.3, "Animation, Adventure, Comedy", "Lee Unkrich", 103, "USA", 415004880, "English"),
        ("The Avengers", 2012, 8.0, "Action, Adventure, Sci-Fi", "Joss Whedon", 143, "USA", 623357910, "English"),
        ("Frozen", 2013, 7.4, "Animation, Adventure, Comedy", "Chris Buck, Jennifer Lee", 102, "USA", 400953009, "English"),
        ("Interstellar", 2014, 8.6, "Adventure, Drama, Sci-Fi", "Christopher Nolan", 169, "USA, UK", 188020017, "English"),
        ("Whiplash", 2014, 8.5, "Drama, Music", "Damien Chazelle", 106, "USA", 13092000, "English"),
        ("Inside Out", 2015, 8.1, "Animation, Adventure, Comedy", "Pete Docter", 95, "USA", 356461711, "English"),
        ("Zootopia", 2016, 8.0, "Animation, Adventure, Comedy", "Byron Howard, Rich Moore", 108, "USA", 341268248, "English"),
        ("Moonlight", 2016, 7.4, "Drama", "Barry Jenkins", 111, "USA", 27854625, "English"),
        ("La La Land", 2016, 8.0, "Comedy, Drama, Music", "Damien Chazelle", 128, "USA", 151101803, "English"),
        ("Coco", 2017, 8.4, "Animation, Adventure, Family", "Lee Unkrich", 105, "USA", 209726015, "English"),
        ("Get Out", 2017, 7.7, "Horror, Mystery, Thriller", "Jordan Peele", 104, "USA", 176040665, "English"),
        ("Black Panther", 2018, 7.3, "Action, Adventure, Sci-Fi", "Ryan Coogler", 134, "USA", 700059566, "English"),
        ("Avengers: Infinity War", 2018, 8.4, "Action, Adventure, Sci-Fi", "Anthony Russo, Joe Russo", 149, "USA", 678815482, "English"),
        
        # 2019-2020s Recent Hits
        ("Avengers: Endgame", 2019, 8.4, "Action, Adventure, Drama", "Anthony Russo, Joe Russo", 181, "USA", 858373000, "English"),
        ("Joker", 2019, 8.4, "Crime, Drama, Thriller", "Todd Phillips", 122, "USA, Canada", 335451311, "English"),
        ("Parasite", 2019, 8.5, "Drama, Thriller", "Bong Joon Ho", 132, "South Korea", 53369749, "Korean, English"),
        ("1917", 2019, 8.2, "Drama, War", "Sam Mendes", 119, "USA, UK", 159227644, "English"),
        ("Spider-Man: No Way Home", 2021, 8.2, "Action, Adventure, Fantasy", "Jon Watts", 148, "USA", 814115070, "English"),
        ("Dune", 2021, 8.0, "Action, Adventure, Drama", "Denis Villeneuve", 155, "USA, Canada", 108327830, "English"),
        ("Top Gun: Maverick", 2022, 8.3, "Action, Drama", "Joseph Kosinski", 130, "USA", 718732821, "English"),
        ("Everything Everywhere All at Once", 2022, 7.8, "Action, Adventure, Comedy", "Dan Kwan, Daniel Scheinert", 139, "USA", 70281644, "English"),
    ]
    
    # Tạo DataFrame
    df = pd.DataFrame(movie_list, columns=[
        'Title', 'Year', 'Rating', 'Genre', 'Director', 'Runtime', 
        'Country', 'BoxOffice', 'Language'
    ])
    
    print(f"✅ Đã tạo dataset với {len(df)} phim")
    
    # Lưu file
    os.makedirs('data', exist_ok=True)
    output_path = 'data/raw_movies.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"💾 Đã lưu tại: {output_path}")
    
    return df


def main():
    """Main function"""
    print("="*60)
    print("  📥 TẢI DATASET IMDB LỚN (1000+ PHIM)")
    print("="*60)
    
    # Thử tải dataset lớn
    df = download_imdb_dataset()
    
    # Nếu thất bại, dùng dataset dự phòng
    if df is None:
        df = download_alternative_dataset()
    
    if df is not None:
        print(f"\n🎉 THÀNH CÔNG!")
        print(f"\n📋 Preview 5 phim đầu tiên:")
        print(df.head().to_string())


if __name__ == '__main__':
    main()
