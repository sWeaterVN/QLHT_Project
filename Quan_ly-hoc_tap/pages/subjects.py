import streamlit as st
from datetime import datetime
import sqlite3


st.set_page_config(page_title="Quản Lý Học Tập", page_icon="🎓", layout="wide")

if "login" not in st.session_state or st.session_state.login == False:
    st.session_state["login"] = None  
if st.session_state["login"] is None:
    st.switch_page("main.py")
    st.stop()

# Kết nối database
conn = sqlite3.connect("Database/users.db")
cursor = conn.cursor()

# Giao diện
col11, col21, col31 = st.columns([6, 1, 1])
with col11:
    st.title("🎓 Website Quản Lý Học Tập")
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

cursor.execute("SELECT total_subjects, done_subjects, gpa FROM general WHERE username = ?", (username,))
row = cursor.fetchone()
total, done, gpa = row if row else (0, 0, 0.0)

# Hiển thị danh sách môn học
cursor.execute("SELECT subject FROM subjects WHERE username = ? AND isdone = 0", (username,))
undone_subjects = cursor.fetchall()

st.markdown("#### 📚 Môn học đang theo học")
if not undone_subjects:
    cursor.execute("SELECT COUNT(*) FROM subjects WHERE username = ?", (username,))
    total_subjects = cursor.fetchone()[0]



    if total_subjects == 0:
        st.cursor("📝 Bạn chưa có môn học nào.")
        
    else:
        st.success("🎉 Bạn đã hoàn thành tất cả các môn học!")
else:
    for subject in undone_subjects:
        with st.expander(f"📘 {subject[0]}"):
            cursor.execute(
                "SELECT note, isdone FROM subjects WHERE username = ? AND subject = ?",
                (username, subject[0])
            )
            row = cursor.fetchone()

            if row:
                note, isdone = row
                st.markdown(f"**Ghi chú:** {note if note else '_Không có_'}")
                st.markdown(f"**Trạng thái:** {'✅ Đã hoàn thành' if isdone else '❌ Chưa hoàn thành'}")
            else:
                st.warning("Không tìm thấy thông tin môn học.")

# Thêm môn học
col11, col12, col13 = st.columns([2, 1, 1])
with col11:
    with st.expander("➕ Thêm môn học"):
        with st.form(key="form_them_mon", clear_on_submit=True):
            new_subject = st.text_input("📘 Tên môn học")
            new_note = st.text_area("📝 Ghi chú")
            submit_subject = st.form_submit_button("✅ Thêm vào danh sách")

            if submit_subject:
                if new_subject.strip() == "":
                    st.warning("⚠️ Vui lòng nhập tên môn học.")
                else:
                    start_time = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
                    
                    username = st.session_state.username
                    cursor.execute("""
                        INSERT INTO subjects (username, subject, note, isdone, start_date)
                        VALUES (?, ?, ?, 0, ?)
                    """, (username, new_subject.strip(), new_note, start_time))

                    conn.commit()

                    cursor.execute("""
                        UPDATE general 
                        SET total_subjects = total_subjects + 1 
                        WHERE username = ?
                    """, (username,))
                    conn.commit()

                    st.success(f"✅ Đã thêm môn học: {new_subject}")
with col12:
    if(st.button("✅ Hoàn thành môn học")):
        st.switch_page("pages/assignments.py")
with col13:
    if(st.button("🏠 Quay lại trang chủ")):
        st.switch_page("pages/home.py")

st.subheader("📅 " + datetime.now().strftime("%A, %d/%m/%Y"))
st.markdown("#### 📈 Dữ liệu cá nhân")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Số môn học", total)
with col2:
    st.metric("Môn đã hoàn thành", done)
with col3:
    st.metric("GPA hiện tại", round(gpa, 2))


with st.expander("📜 Xem lịch sử môn học"):
    cursor.execute("""
        SELECT subject, note, isdone, start_date, end_date 
        FROM subjects 
        WHERE username = ?
    """, (username,))
    all_subjects = cursor.fetchall()

    if not all_subjects:
        st.cursor("📭 Bạn chưa có môn học nào.")
    else:
        st.subheader("📚 Lịch sử môn học")
        for idx, (subject, note, isdone, start_date, end_date) in enumerate(all_subjects, start=1):
            status = "✅ Hoàn thành" if isdone else "❌ Chưa hoàn thành"
            st.subheader(f"{idx}) 📘 {subject}")
            st.write(f"📝 Ghi chú: {note if note else '_Không có_'}")
            st.write(f"📅 Bắt đầu: {start_date if start_date else '_Không rõ_'}")
            if isdone:
                st.write(f"🏁 Hoàn thành: {end_date if end_date else '_Chưa hoàn thành_'}")
            st.write(f"📊 Trạng thái: {status}")
            st.markdown("---")

st.markdown("---")

