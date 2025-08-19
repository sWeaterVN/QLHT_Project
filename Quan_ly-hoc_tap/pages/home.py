import streamlit as st
from datetime import datetime
import sqlite3

# Sidebar điều hướng
st.sidebar.title("📚 Điều hướng")
page = st.sidebar.radio("Chọn chức năng", [
    "🏠 Trang chủ",
    "📋 Môn học",
    "📝 Bài tập",
    "📊 Điểm số",
    "🗓️ Lịch học",
    "🗒️ Ghi chú"
])

# Chuyển trang nếu không phải Trang chủ
if page == "📋 Môn học":
    st.switch_page("pages/subjects.py")
    st.stop()
elif page == "📝 Bài tập":
    st.switch_page("pages/assignments.py")
    
elif page == "📊 Điểm số":
    st.switch_page("pages/grades.py")
    st.stop()
elif page == "🗓️ Lịch học":
    st.switch_page("pages/schedule.py")
    st.stop()
elif page == "🗒️ Ghi chú":
    st.switch_page("pages/notes.py")
    st.stop()

# Nếu là Trang chủ, render nội dung

st.set_page_config(page_title="Quản Lý Học Tập", page_icon="🎓", layout="wide")

if "login" not in st.session_state or st.session_state.login == False:
    st.session_state["login"] = None  
if st.session_state["login"] is None:
    st.switch_page("main.py")
    st.stop()

# Kết nối database
conn = sqlite3.connect("Database/users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        username TEXT PRIMARY KEY,
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
# Giao diện
col1, col2, col3 = st.columns([6, 1, 1])
with col1:
    st.title("🎓 Website Quản Lý Học Tập")
with col2:
    username = st.session_state.username
    cursor.execute("SELECT name FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    name = row[0]
    st.write(f"Xin chào, {name}")
with col3:
    if st.button("🔐 Đăng xuất"):
        st.session_state.login = False
        st.switch_page("pages/login.py")
        st.stop()

cursor.execute("SELECT total_subjects, done_subjects, gpa FROM general WHERE username = ?", (username,))
row = cursor.fetchone()
total, done, gpa = row if row else (0, 0, 0.0)


st.subheader("📅 " + datetime.now().strftime("%A, %d/%m/%Y"))
st.markdown("#### 📈 Dữ liệu cá nhân")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Số môn học", total)
with col2:
    st.metric("Môn đã hoàn thành", done)
with col3:
    st.metric("GPA hiện tại", round(gpa, 2))

st.markdown("---")

# Hiển thị danh sách môn học
cursor.execute("SELECT subject FROM subjects WHERE username = ? AND isdone = 0", (username,))
undone_subjects = cursor.fetchall()

st.markdown("#### 📚 Môn học đang theo học")
if not undone_subjects:
    cursor.execute("SELECT COUNT(*) FROM subjects WHERE username = ?", (username,))
    total_subjects = cursor.fetchone()[0]

    if total_subjects == 0:
        st.cursor("📝 Bạn chưa có môn học nào. Hãy thêm môn học tại mục **📋 Môn học**")
        
    else:
        st.success("🎉 Bạn đã hoàn thành tất cả các môn học!")
else:
    col21, col22, col23 = st.columns([3, 2, 3])
    i = 0
    for subject in undone_subjects:
        i+=1
        with col21:
            st.write(f"{i} | 📘 {subject[0]}")
        with col22:
            st.warning("Chưa hoàn thành")
if st.button("Chuyển đến **📋 Môn học**"):
    st.switch_page("pages/subjects.py")
    st.stop
