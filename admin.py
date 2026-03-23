import streamlit as st
from database import get_courses, get_all_students, add_course, delete_course, get_enrollment_details
import pandas as pd
import plotly.express as px
from collections import Counter

def admin_dashboard(user):

    st.title("📊 Admin Dashboard")

    menu = st.sidebar.radio("📂 Menu", [
        "📈 Overview", "📚 Courses", "👨‍🎓 Students", "📋 Enrollments"
    ])

    data = get_enrollment_details()
    courses = get_courses()
    students = get_all_students()

    # ---------- OVERVIEW ----------
    if "Overview" in menu:

        total_revenue = sum([d['price'] for d in data]) if data else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Courses", len(courses))
        c2.metric("Students", len(students))
        c3.metric("Enrollments", len(data))
        c4.metric("Revenue", f"₹{total_revenue}")

        if data:
            df = pd.DataFrame(data)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔥 Top Courses")
                course_count = Counter(df['course_name'])
                chart_df = pd.DataFrame({
                    "Course": list(course_count.keys()),
                    "Enrollments": list(course_count.values())
                })

                fig = px.bar(chart_df, x="Course", y="Enrollments", color="Enrollments")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📈 Progress")
                fig = px.line(df, y="progress")
                st.plotly_chart(fig, use_container_width=True)

    # ---------- COURSES ----------
    elif "Courses" in menu:

        st.subheader("➕ Add Course")

        with st.form("form"):
            name = st.text_input("Course Name")
            desc = st.text_area("Description")
            price = st.number_input("Price")
            seats = st.number_input("Seats")
            submit = st.form_submit_button("Add")

        if submit:
            add_course(name, desc, price, seats)
            st.success("Added!")
            st.rerun()

        st.subheader("📚 Course List")

        for c in courses:
            col1, col2 = st.columns([4,1])
            col1.write(f"{c['course_name']} - ₹{c['price']}")
            if col2.button("❌", key=c['id']):
                delete_course(c['id'])
                st.rerun()

    # ---------- STUDENTS ----------
    elif "Students" in menu:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)

    # ---------- ENROLLMENTS ----------
    elif "Enrollments" in menu:
        if data:
            df = pd.DataFrame(data)

            fig = px.pie(df, names="course_name", values="price", title="Revenue Distribution")
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df)