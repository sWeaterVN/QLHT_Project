import streamlit as st
import sqlite3

main_img = "https://i.ibb.co/KjPLQF1p/Website-Qu-n-l-h-c-t-p.png"
func_img = "https://i.ibb.co/TxYy7Sk0/Website-Qu-n-l-h-c-t-p-1.png"


conn = sqlite3.connect("Database/users.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        name TEXT   
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        username TEXT,
        subject TEXT,
        isdone INTEGER DEFAULT 0,
        note TEXT,
        start_date TEXT,
        end_date TEXT     
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS general (
        username TEXT PRIMARY KEY,
        gpa REAL DEFAULT 0,
        total_subjects INTEGER DEFAULT 0,
        done_subjects INTEGER DEFAULT 0
    )
""")
conn.commit()

st.set_page_config(page_title="Quản Lý Học Tập", page_icon="🎓", layout="wide")
if "login" not in st.session_state or st.session_state.login == False:
    st.session_state["login"] = None
    
    # Kết nối database
user_info = sqlite3.connect("Database/users.db")
cursor = user_info.cursor()

col11, col21, col31 = st.columns([6, 1, 1])
with col11:
    st.title("🎓 Website Quản Lý Học Tập")

# Kiểm tra trạng thái đăng nhập
col12, col22 = st.columns([1, 1])

# Sidebar điều hướng

col13, col23 = st.columns([1, 1])
with col13:
    st.markdown("""
        Xin chào! 👋 Đây là ứng dụng giúp bạn quản lý quá trình học tập một cách hiệu quả.

        ### 🔧 Tính năng chính:
        - **Quản lý môn học**: thêm, sửa, xóa các môn đang học.
        - **Theo dõi bài tập**: xem các bài tập còn hạn và sắp đến hạn.
        - **Tính điểm trung bình**: nhập điểm và xem biểu đồ học lực.
        - **Xem lịch học**: tổ chức thời gian học tập theo tuần.
        - **Ghi chú cá nhân**: lưu ý tưởng, nội dung quan trọng.
        """)
with col23:
    st.image(func_img)


st.image(main_img, use_container_width=True)
# Kiểm tra trạng thái đăng nhập
if not st.session_state.get("login"):
    st.warning("❗ Bạn chưa đăng nhập. Hãy nhấn nút 🔐 Đăng nhập ở góc phải để sử dụng ứng dụng.")
    with col31:
        if st.button("🔐 Đăng nhập"):
            st.switch_page("pages/login.py")
    st.stop()    
else:
    with col21:
        username = st.session_state.username
        cursor.execute("SELECT name FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        name = row[0]
        st.write(f"Xin chào, {name}")
    with col31:
        if st.button("🔐 Đăng xuất"):
            st.session_state.login = False
            st.switch_page("pages/login.py")
            st.stop()
    with col13:
        if st.button("🏠 Chuyển đến trang chủ"):
            st.switch_page("pages/home.py")


