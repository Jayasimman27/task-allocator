import streamlit as st
import requests

st.title("AI Task Generator & Planner")

text = st.text_area("Describe your tasks for today:")

if st.button("Generate"):
    res = requests.post(
        "http://localhost:8000/generate",
        json={"text": text}
    ).json()

    st.subheader("Generated Tasks:")

    for t in res["tasks"]:
        st.write(f"### • {t['task']}")
        st.write("Priority:", t["priority"])
        st.write("Category:", t["category"])
        st.write("Time:", t["estimated_minutes"], "min")
        st.write("---")
