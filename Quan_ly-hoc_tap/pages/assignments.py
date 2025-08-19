import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Nhập điểm môn học", page_icon="📝", layout="wide")

# Kiểm tra đăng nhập
if "login" not in st.session_state or st.session_state.login is False:
    st.session_state["login"] = None
if st.session_state["login"] is None:
    st.switch_page("main.py")
    st.stop()

username = st.session_state.username

# Kết nối database
db = sqlite3.connect("Database/users.db")
cursor = db.cursor()

cursor.execute("""
    SELECT subject FROM subjects 
    WHERE username = ? AND isdone = 0
""", (username,))
undone_subjects = [row[0] for row in cursor.fetchall()]

st.title("📝 Nhập điểm cho môn học")

if not undone_subjects:
    st.success("🎉 Bạn đã hoàn thành tất cả các môn học!")
else:
    with st.form(key="Nhập điểm môn học"):
        subject_choice = st.selectbox("📘 Chọn môn học", undone_subjects)

        diem_giua_ky = st.number_input("Điểm giữa kỳ", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
        diem_cuoi_ky = st.number_input("Điểm cuối kỳ", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
        diem_khac = st.number_input("Điểm khác", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")

        if st.form_submit_button("✅ Lưu kết quả"):
            if diem_giua_ky == 0.0 and diem_cuoi_ky == 0.0 and diem_khac == 0.0:
                st.warning("⚠️ Vui lòng nhập ít nhất một điểm.")
            else:
                diem_tb = round((diem_giua_ky + diem_cuoi_ky + diem_khac) / 3, 2)

                gpa_mon = round((diem_tb / 10) * 4, 2)

                end_time = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
                cursor.execute("""
                    UPDATE subjects 
                    SET isdone = 1, 
                        note = COALESCE(note, '') || ' | GPA: ' || ?, 
                        end_date = ? 
                    WHERE username = ? AND subject = ?
                """, (gpa_mon, end_time, username, subject_choice))
                db.commit()

                cursor.execute("SELECT gpa, total_subjects, done_subjects FROM general WHERE username = ?", (username,))
                row = cursor.fetchone()

                if row:
                    old_gpa, total_sub, done_sub = row
                    new_done = done_sub + 1
                    new_gpa = round(((old_gpa * done_sub) + gpa_mon) / new_done, 2)

                    cursor.execute("""
                        UPDATE general 
                        SET done_subjects = ?, gpa = ? 
                        WHERE username = ?
                    """, (new_done, new_gpa, username))
                    db.commit()

                st.success(f"✅ Đã lưu điểm cho môn {subject_choice} (GPA: {gpa_mon})")
                st.rerun()

# Lịch sử môn học
col11, col12 = st.columns([1, 1])
with col11:
    if st.button("🔙Quay lại"):
        st.switch_page("pages/subjects.py")


with st.expander("📜 Xem lịch sử môn học"):
    cursor.execute("""
        SELECT subject, note, isdone, start_date, end_date 
        FROM subjects 
        WHERE username = ?
    """, (username,))
    all_subjects = cursor.fetchall()

    if not all_subjects:
        st.info("📭 Bạn chưa có môn học nào.")
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