"""
Run All Pipeline - Chạy toàn bộ quy trình
Tự động chạy: Thu thập → Xử lý → Phân tích → Web App
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {description} - HOÀN THÀNH!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - LỖI!")
        print(f"Error: {e}")
        return False

def main():
    """Main function"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   🎬 IMDb Movie Data Storytelling Pipeline 🎬        ║
    ║                                                       ║
    ║   Tự động chạy toàn bộ quy trình:                    ║
    ║   1. Thu thập dữ liệu                                ║
    ║   2. Tiền xử lý                                      ║
    ║   3. Tạo biểu đồ phân tích                           ║
    ║   4. Khởi động web app                               ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Kiểm tra Python
    python_cmd = sys.executable
    print(f"📍 Python: {python_cmd}")
    print(f"📍 Working Directory: {os.getcwd()}\n")
    
    # Bước 1: Thu thập dữ liệu
    if not run_command(f'"{python_cmd}" data_collection.py', 
                      "Bước 1/4: Thu thập dữ liệu"):
        print("\n⚠️ Dừng pipeline do lỗi ở bước 1")
        return
    
    # Bước 2: Tiền xử lý
    if not run_command(f'"{python_cmd}" data_preprocessing.py',
                      "Bước 2/4: Tiền xử lý dữ liệu"):
        print("\n⚠️ Dừng pipeline do lỗi ở bước 2")
        return
    
    # Bước 3: Tạo biểu đồ
    if not run_command(f'"{python_cmd}" data_analysis.py',
                      "Bước 3/4: Tạo biểu đồ phân tích"):
        print("\n⚠️ Dừng pipeline do lỗi ở bước 3")
        return
    
    # Bước 4: Web app
    print(f"\n{'='*60}")
    print(f"🌐 Bước 4/4: Khởi động Web Application")
    print(f"{'='*60}\n")
    print("🚀 Đang khởi động Streamlit...")
    print("📍 Mở trình duyệt tại: http://localhost:8501")
    print("⚠️ Nhấn Ctrl+C để dừng server\n")
    
    # Chạy Streamlit (blocking)
    subprocess.run(['streamlit', 'run', 'app.py'])

if __name__ == '__main__':
    main()
