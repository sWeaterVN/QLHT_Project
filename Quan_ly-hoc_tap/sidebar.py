import streamlit as st

def sidebar():
    st.sidebar.title("📚 Điều hướng")
    page = st.sidebar.radio("Chọn chức năng", [
        "🏠 Trang chủ",
        "📋 Môn học",
        "📝 Bài tập",
        "📊 Điểm số",
        "🗓️ Lịch học",
        "🗒️ Ghi chú"
    ])

    if page == "🏠 Trang chủ":
        st.switch_page("pages/home.py")
        st.stop()
    elif page == "📋 Môn học":
        st.switch_page("pages/subjects.py")
        st.stop()
    elif page == "📝 Bài tập":
        st.switch_page("pages/assignments.py")
        st.stop()
    elif page == "📊 Điểm số":
        st.switch_page("pages/grades.py")
        st.stop()
    elif page == "🗓️ Lịch học":
        st.switch_page("pages/schedule.py")
        st.stop()
    elif page == "🗒️ Ghi chú":
        st.switch_page("pages/notes.py")
        st.stop()
