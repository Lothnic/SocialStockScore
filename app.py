import streamlit as st
import random
from ingestion.github.github_final import score_github_user

st.title("Social Credit Score Calculator")
st.write("This app calculates your social credit score based on your activity on varoius social media platforms.")
st.write("Please Enter your github username below")

github_username = st.text_input("GitHub Username")
# linkedin_username = st.text_input("LinkedIn Username")
# reddit_username = st.text_input("Reddit Username")


if github_username and st.button("Calculate GitHub Score"):
    with st.spinner("Calculating your GitHub social credit score..."):
        social_credit_score, details = score_github_user(github_username)
        st.write(f"Your GitHub social credit score is: {social_credit_score}")
    
    