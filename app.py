import streamlit as st
from database import login_user, register_user
from admin import admin_dashboard
from student import student_dashboard

st.set_page_config(page_title="Course App", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

if "dashboard" not in st.session_state:
    st.session_state.dashboard = None

# ---------- AUTH ----------
if st.session_state.user is None:

    st.title("🚀 Course Management System")

    menu = st.radio("", ["Login", "Register"], horizontal=True)

    if menu == "Login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if email == "" or password == "":
                st.warning("Please fill all fields")
            else:
                user = login_user(email, password)

                if user:
                    st.session_state.user = user
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")

    else:
        st.subheader("Register")

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            if name == "" or email == "" or password == "":
                st.warning("All fields required")
            else:
                success = register_user(name, email, password)

                if success:
                    st.success("Account created! Now login.")
                else:
                    st.error("⚠ Email already exists")

# ---------- DASHBOARD ----------
else:

    user = st.session_state.user

    st.sidebar.write(f"👤 {user['name']} ({user['role']})")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.dashboard = None
        st.rerun()

    if st.session_state.dashboard is None:

        st.title("Select Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Student Dashboard"):
                if user['role'] == "admin":
                    st.error("Admin cannot open student dashboard")
                else:
                    st.session_state.dashboard = "student"
                    st.rerun()

        with col2:
            if st.button("Admin Dashboard"):
                if user['role'] != "admin":
                    st.error("Only Admin allowed")
                else:
                    st.session_state.dashboard = "admin"
                    st.rerun()

    else:

        if st.session_state.dashboard == "student":
            if st.sidebar.button("Back"):
                st.session_state.dashboard = None
                st.rerun()
            student_dashboard(user)

        elif st.session_state.dashboard == "admin":
            if st.sidebar.button("Back"):
                st.session_state.dashboard = None
                st.rerun()
            admin_dashboard(user)