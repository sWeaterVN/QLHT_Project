import streamlit as st
import sqlite3

st.set_page_config(page_title="Đăng ký", layout="centered")
st.title("🆕 Đăng ký tài khoản mới")

# Kết nối database
conn = sqlite3.connect("Database/users.db")
cursor = conn.cursor()

# Giao diện đăng ký
with st.form(key = "Register"):
    username = st.text_input("👤 Username")
    name = st.text_input("👤 Full name")
    password = st.text_input("🔑 Password", type="password")

    submitted = st.form_submit_button("Tạo tài khoản")
    if submitted:
        if username and password and name:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                st.error("⚠️ Tên tài khoản đã tồn tại!")
            else:
                cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, password, name))
                conn.commit()
                st.success("✅ Tạo tài khoản thành công!")
                # tạo tài khoản thành công

                gen_conn = sqlite3.connect("Database/users.db")
                gen_cursor = gen_conn.cursor()
                gen_cursor.execute("INSERT OR IGNORE INTO general (username) VALUES (?)", (username,))
                gen_conn.commit()

        else:
            st.error("⚠️ Vui lòng điền đầy đủ thông tin.")

st.markdown("---")
if st.button("🔙 Đã có tài khoản? Đăng nhập"):
    st.switch_page("pages/login.py")
