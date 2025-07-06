import streamlit as st


st.title("Social Credit Score Calculator")
st.write("This app calculates your social credit score based on your activity on varoius social media platforms.")
st.write("Please enter your github username below")
github_username = st.text_input("GitHub Username")
if github_username:
    st.write(f"Calculating social credit score for {github_username}...")

    
    
    st.write(f"Your social credit score is: {social_credit_score}")