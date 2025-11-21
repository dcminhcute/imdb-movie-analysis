# Script thêm giải thích cho phần tương quan

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Tìm dòng cần sửa
for i, line in enumerate(lines):
    if 'Mức Độ Tương Quan' in line:
        # Thay đổi tiêu đề
        lines[i] = '    st.subheader("📊 Yếu Tố Nào Ảnh Hưởng Đến Rating?")\n'
        
        # Thêm giải thích ngay sau tiêu đề
        explanation = '''    
    st.markdown("""
    <div class="insight-box">
    <h4>💡 Hệ số tương quan là gì?</h4>
    <ul>
    <li><b>Từ 0.4 đến 1.0</b>: Liên quan MẠNH - Yếu tố này tăng → Rating tăng 📈</li>
    <li><b>Từ 0.1 đến 0.4</b>: Liên quan VỪA PHẢI - Có ảnh hưởng nhưng không nhiều</li>
    <li><b>Gần 0</b>: KHÔNG liên quan - Yếu tố này không ảnh hưởng gì đến Rating</li>
    <li><b>Số âm</b>: Liên quan NGƯỢC - Yếu tố này tăng → Rating giảm 📉</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
'''
        lines.insert(i+1, explanation)
        break

# Tìm dòng st.plotly_chart sau correlation chart và thêm kết luận
for i, line in enumerate(lines):
    if i > 380 and 'st.plotly_chart(fig, use_container_width=True)' in line and 'correlation' in ''.join(lines[max(0,i-20):i]).lower():
        conclusion = '''        
        # Giải thích kết quả cụ thể
        st.markdown("""
        <div class="insight-box">
        <h4>🔍 Kết luận từ biểu đồ:</h4>
        <p><b>⭐ Metascore (0.41)</b> - MẠNH NHẤT: Phim được giới phê bình đánh giá cao → Khán giả cũng cho rating cao!</p>
        <p><b>💰 BoxOffice (0.21)</b> - VỪA PHẢI: Phim bán vé tốt thường có rating cao hơn một chút.</p>
        <p><b>⏱️ Runtime (0.15)</b> - YẾU: Thời lượng phim gần như không ảnh hưởng đến rating.</p>
        <p><b>📅 Năm/Thập kỷ</b> - RẤT YẾU: Thời gian phát hành không quan trọng với rating.</p>
        </div>
        """, unsafe_allow_html=True)
'''
        lines.insert(i+1, conclusion)
        break

# Ghi lại file
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Đã thêm giải thích cho phần tương quan!")
