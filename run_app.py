"""
File launcher để chạy Streamlit app bằng nút ▶️ trong PyCharm
Chỉ cần nhấn Run (▶️) vào file này là app sẽ tự động mở!
"""

import os
import sys

# Chạy streamlit với app.py
if __name__ == "__main__":
    os.system("streamlit run app.py")
