"""
Data Collection Script for IMDb Movie Data
Sử dụng OMDb API để thu thập dữ liệu phim
"""

import requests
import pandas as pd
import time
import os
from typing import List, Dict

class MovieDataCollector:
    """Class để thu thập dữ liệu phim từ OMDb API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"
        
    def search_movies(self, query: str, year: str = None) -> List[Dict]:
        """Tìm kiếm phim theo từ khóa"""
        params = {
            'apikey': self.api_key,
            's': query,
            'type': 'movie'
        }
        if year:
            params['y'] = year
            
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return data.get('Search', [])
                else:
                    # API trả về lỗi
                    error = data.get('Error', 'Unknown error')
                    if 'Invalid API key' in error:
                        print(f"\n❌ API key không hợp lệ! Vui lòng kiểm tra lại.")
                        print(f"💡 Đảm bảo bạn đã click link kích hoạt trong email!")
                        return None  # Signal to stop
                    # Không tìm thấy phim thì bỏ qua
                    return []
        except Exception as e:
            print(f"  ⚠️ Lỗi khi tìm kiếm '{query}': {e}")
        return []
    
    def get_movie_details(self, imdb_id: str) -> Dict:
        """Lấy thông tin chi tiết của một phim"""
        params = {
            'apikey': self.api_key,
            'i': imdb_id,
            'plot': 'full'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return data
        except Exception as e:
            print(f"  ⚠️ Lỗi khi lấy chi tiết phim {imdb_id}: {e}")
        return {}
    
    def collect_popular_movies(self, queries: List[str], save_path: str = 'data/raw_movies.csv'):
        """
        Thu thập dữ liệu từ danh sách các từ khóa phổ biến
        
        Args:
            queries: Danh sách các từ khóa tìm kiếm
            save_path: Đường dẫn lưu file
        """
        all_movies = []
        seen_ids = set()
        
        print(f"🎬 Bắt đầu thu thập dữ liệu từ {len(queries)} từ khóa...")
        
        for i, query in enumerate(queries, 1):
            print(f"📍 [{i}/{len(queries)}] Tìm kiếm: {query}")
            movies = self.search_movies(query)
            
            # Kiểm tra nếu API key không hợp lệ
            if movies is None:
                print("\n❌ Dừng thu thập do API key không hợp lệ!")
                print("💡 Vui lòng:")
                print("   1. Kiểm tra email và click link kích hoạt")
                print("   2. Đợi vài phút để API key được kích hoạt")
                print("   3. Chạy lại script này")
                return pd.DataFrame()
            
            for movie in movies:
                imdb_id = movie.get('imdbID')
                if imdb_id and imdb_id not in seen_ids:
                    print(f"  ⏳ Lấy chi tiết: {movie.get('Title', 'N/A')}")
                    details = self.get_movie_details(imdb_id)
                    if details:
                        all_movies.append(details)
                        seen_ids.add(imdb_id)
                    time.sleep(0.2)  # Tránh rate limit
        
        # Chuyển sang DataFrame
        df = pd.DataFrame(all_movies)
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Lưu file
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        print(f"\n✅ Đã lưu {len(df)} phim vào {save_path}")
        
        return df


def create_sample_dataset():
    """
    Tạo dataset mẫu từ dữ liệu có sẵn (không cần API key)
    Phù hợp cho việc demo và test
    """
    print("🎬 Tạo dataset mẫu IMDb...")
    
    # Dữ liệu mẫu từ các phim nổi tiếng
    sample_data = {
        'Title': [
            'The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 
            'Pulp Fiction', 'Forrest Gump', 'Inception', 'Fight Club',
            'The Matrix', 'Goodfellas', 'The Lord of the Rings: The Return of the King',
            'Star Wars: Episode V', 'Interstellar', 'The Silence of the Lambs',
            'Saving Private Ryan', 'The Green Mile', 'The Prestige',
            'The Departed', 'Gladiator', 'The Lion King', 'Back to the Future',
            'Avengers: Endgame', 'Spider-Man: No Way Home', 'Avatar',
            'Titanic', 'Jurassic Park', 'The Avengers', 'Black Panther',
            'Frozen', 'Toy Story', 'Finding Nemo', 'Inside Out',
            'Parasite', 'Joker', 'Get Out', 'Moonlight', 'Whiplash'
        ],
        'Year': [
            1994, 1972, 2008, 1994, 1994, 2010, 1999, 1999, 1990, 2003,
            1980, 2014, 1991, 1998, 1999, 2006, 2006, 2000, 1994, 1985,
            2019, 2021, 2009, 1997, 1993, 2012, 2018, 2013, 1995, 2003, 2015,
            2019, 2019, 2017, 2016, 2014
        ],
        'Rating': [
            9.3, 9.2, 9.0, 8.9, 8.8, 8.8, 8.8, 8.7, 8.7, 9.0,
            8.7, 8.6, 8.6, 8.6, 8.6, 8.5, 8.5, 8.5, 8.5, 8.5,
            8.4, 8.2, 7.9, 7.9, 8.2, 8.0, 7.3, 7.4, 8.3, 8.2, 8.1,
            8.5, 8.4, 7.7, 7.4, 8.5
        ],
        'Genre': [
            'Drama', 'Crime, Drama', 'Action, Crime, Drama', 'Crime, Drama',
            'Drama, Romance', 'Action, Sci-Fi, Thriller', 'Drama',
            'Action, Sci-Fi', 'Crime, Drama', 'Action, Adventure, Drama',
            'Action, Adventure, Fantasy', 'Adventure, Drama, Sci-Fi', 'Crime, Drama, Thriller',
            'Drama, War', 'Crime, Drama, Fantasy', 'Drama, Mystery, Thriller',
            'Crime, Drama, Thriller', 'Action, Adventure, Drama', 'Animation, Adventure, Drama',
            'Adventure, Comedy, Sci-Fi', 'Action, Adventure, Drama', 'Action, Adventure, Fantasy',
            'Action, Adventure, Fantasy', 'Drama, Romance', 'Action, Adventure, Sci-Fi',
            'Action, Adventure, Sci-Fi', 'Action, Adventure, Sci-Fi', 'Animation, Adventure, Comedy',
            'Animation, Adventure, Comedy', 'Animation, Adventure, Comedy', 'Animation, Adventure, Comedy',
            'Drama, Thriller', 'Crime, Drama, Thriller', 'Horror, Mystery, Thriller',
            'Drama', 'Drama, Music'
        ],
        'Director': [
            'Frank Darabont', 'Francis Ford Coppola', 'Christopher Nolan',
            'Quentin Tarantino', 'Robert Zemeckis', 'Christopher Nolan', 'David Fincher',
            'Lana Wachowski, Lilly Wachowski', 'Martin Scorsese', 'Peter Jackson',
            'Irvin Kershner', 'Christopher Nolan', 'Jonathan Demme',
            'Steven Spielberg', 'Frank Darabont', 'Christopher Nolan',
            'Martin Scorsese', 'Ridley Scott', 'Roger Allers, Rob Minkoff', 'Robert Zemeckis',
            'Anthony Russo, Joe Russo', 'Jon Watts', 'James Cameron',
            'James Cameron', 'Steven Spielberg', 'Joss Whedon', 'Ryan Coogler',
            'Chris Buck, Jennifer Lee', 'John Lasseter', 'Andrew Stanton', 'Pete Docter',
            'Bong Joon Ho', 'Todd Phillips', 'Jordan Peele', 'Barry Jenkins', 'Damien Chazelle'
        ],
        'Runtime': [
            142, 175, 152, 154, 142, 148, 139, 136, 145, 201,
            124, 169, 118, 169, 189, 130, 151, 155, 88, 116,
            181, 148, 162, 194, 127, 143, 134, 102, 81, 100, 95,
            132, 122, 104, 111, 106
        ],
        'Country': [
            'USA', 'USA', 'USA, UK', 'USA', 'USA', 'USA, UK', 'USA',
            'USA', 'USA', 'New Zealand, USA', 'USA', 'USA, UK', 'USA',
            'USA', 'USA', 'USA, UK', 'USA, Hong Kong', 'USA, UK', 'USA', 'USA',
            'USA', 'USA', 'USA, UK', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA',
            'South Korea', 'USA, Canada', 'USA, Japan', 'USA', 'USA'
        ],
        'BoxOffice': [
            28341469, 134966411, 534858444, 107928762, 330252182, 292576195, 37030102,
            171479930, 46836394, 377845905, 290475067, 188020017, 130742922,
            216540909, 136801374, 53089891, 132384315, 187705427, 422783777, 210609762,
            858373000, 814115070, 760507625, 659363944, 402453882, 623357910, 700059566,
            400953009, 373554033, 380843261, 356461711, 53369749, 335451311, 176040665,
            27854625, 13092000
        ],
        'Language': [
            'English', 'English, Italian, Latin', 'English, Mandarin',
            'English, Spanish, French', 'English', 'English, Japanese, French', 'English',
            'English', 'English, Italian', 'English, Quenya, Old English, Sindarin',
            'English', 'English', 'English, Latin', 'English, French, German, Czech',
            'English', 'English', 'English, Cantonese', 'English', 'English, Swahili, Xhosa, Zulu',
            'English', 'English, Japanese', 'English, Tagalog, Spanish', 'English, Spanish',
            'English, Swedish, Italian, French', 'English, Spanish', 'English, Russian, Hindi',
            'English, Xhosa', 'English, Norwegian', 'English', 'English', 'English',
            'Korean, English, German, French', 'English', 'English', 'English', 'English'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Tạo thư mục data nếu chưa tồn tại
    os.makedirs('data', exist_ok=True)
    
    # Lưu file
    save_path = 'data/raw_movies.csv'
    df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"✅ Đã tạo dataset mẫu với {len(df)} phim tại {save_path}")
    
    return df


def main():
    """Main function để chạy data collection"""
    
    # Đọc API key từ file .env
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OMDB_API_KEY')
    
    if api_key and api_key != 'your_api_key_here':
        # Sử dụng API thật
        print("🔑 Sử dụng OMDb API để thu thập dữ liệu...")
        print(f"🎯 Mục tiêu: Thu thập 100+ phim từ nhiều thể loại\n")
        collector = MovieDataCollector(api_key)
        
        # Danh sách các từ khóa phổ biến mở rộng
        popular_queries = [
            # Franchises lớn
            'Star Wars', 'Marvel', 'Avengers', 'Iron Man', 'Captain America',
            'Batman', 'Superman', 'Spider-Man', 'Wonder Woman', 'Aquaman',
            'Lord of the Rings', 'Hobbit', 'Harry Potter',
            'James Bond', 'Mission Impossible', 'Fast Furious',
            'Jurassic', 'Transformers', 'Pirates Caribbean',
            
            # Directors nổi tiếng
            'Nolan', 'Spielberg', 'Tarantino', 'Scorsese', 'Cameron',
            'Fincher', 'Coen', 'Anderson', 'Villeneuve', 'Kubrick',
            
            # Classics
            'Godfather', 'Pulp Fiction', 'Forrest Gump', 'Shawshank',
            'Fight Club', 'Matrix', 'Inception', 'Interstellar',
            'Titanic', 'Avatar', 'Gladiator', 'Braveheart',
            
            # Animation
            'Toy Story', 'Finding Nemo', 'Frozen', 'Lion King',
            'Up', 'Inside Out', 'Coco', 'Moana', 'Zootopia',
            
            # Horror/Thriller
            'Exorcist', 'Shining', 'Silence Lambs', 'Psycho',
            'Alien', 'Terminator', 'Predator', 'Jaws',
            
            # Comedy/Drama
            'Forrest', 'Life Beautiful', 'Green Mile', 'Prestige',
            'Departed', 'Usual Suspects', 'Good Will', 'American'
        ]
        
        df = collector.collect_popular_movies(popular_queries)
    else:
        # Sử dụng dataset mẫu
        print("⚠️ Không tìm thấy API key. Sử dụng dataset mẫu...")
        print("💡 Để sử dụng API thật: Lấy key từ https://www.omdbapi.com/apikey.aspx")
        print("   Sau đó tạo file .env với nội dung: OMDB_API_KEY=your_key")
        df = create_sample_dataset()
    
    print(f"\n📊 Thông tin dataset:")
    print(f"   - Số lượng phim: {len(df)}")
    print(f"   - Số cột: {len(df.columns)}")
    print(f"   - Các cột: {', '.join(df.columns.tolist())}")


if __name__ == '__main__':
    main()
