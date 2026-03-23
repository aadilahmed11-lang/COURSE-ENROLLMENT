import streamlit as st
from database import get_courses, enroll_course

def student_dashboard(user):

    st.title("🎓 Student Dashboard")

    courses = get_courses()
    selected = []

    search = st.text_input("🔍 Search Courses")

    cols = st.columns(3)

    i = 0
    for c in courses:
        if search.lower() in c['course_name'].lower():

            with cols[i % 3]:
                st.markdown(f"""
                <div style='
                    background:#1c1f26;
                    padding:20px;
                    border-radius:15px;
                    transition:0.3s;
                '>
                    <h4>{c['course_name']}</h4>
                    <p>{c['description']}</p>
                    <b>₹{c['price']}</b>
                </div>
                """, unsafe_allow_html=True)

                if st.checkbox("Select", key=c['id']):
                    selected.append(c['id'])

            i += 1

    st.divider()

    if st.button("🚀 Enroll Now"):
        for cid in selected:
            enroll_course(user['id'], cid)
        st.success("Enrolled Successfully!")