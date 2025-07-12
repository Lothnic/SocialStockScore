import streamlit as st
import random
from ingestion.github.github_final import score_github_user
from ingestion.linkedin.first import cal_score
from ingestion.reddit.first import cal_score as reddit_cal_score, fetch_user_data

st.title("Social Credit Score Calculator")
st.write("This app calculates your social credit score based on your activity on varoius social media platforms.")
st.write("Please Enter your github username below")

github_username = st.text_input("GitHub Username")
linkedin_username = st.text_input("LinkedIn Username")
reddit_username = st.text_input("Reddit Username")


if st.button("Calculate Dev Score") and github_username and linkedin_username and reddit_username:
    with st.spinner("Calculating your Social credit score..."):
        social_credit_score = 0
        social_credit_score += score_github_user(github_username)
        social_credit_score += cal_score(linkedin_username)
        social_credit_score += reddit_cal_score(reddit_username, *fetch_user_data(reddit_username))
        st.write(f"Your Social credit score is: {round(social_credit_score,2)}/60")
    
    