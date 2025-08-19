import streamlit as st
import sqlite3

st.set_page_config(page_title="Đăng nhập", layout="centered")
st.title("🔐 Đăng nhập")

# Kết nối database
conn = sqlite3.connect("Database/users.db")
cursor = conn.cursor()

if "login" not in st.session_state:
    st.session_state.login = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Giao diện đăng nhập
with st.form(key = "Login"):

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    submitted = st.form_submit_button("Đăng Nhập")

    if submitted:
        if username and password:
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            if result:
                st.session_state.login = True
                st.session_state.username = username
                st.success("✅ Đăng nhập thành công!")
                st.switch_page("main.py")
            else:
                st.error("❌ Sai tài khoản hoặc mật khẩu.")
        else:
            st.error("⚠️ Vui lòng điền đầy đủ thông tin.")

# Liên kết sang trang đăng ký
st.markdown("---")
if st.button("👉 Chưa có tài khoản? Đăng ký ngay"):
    st.switch_page("pages/register.py")
