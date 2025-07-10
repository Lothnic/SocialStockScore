from linkedin_api import Linkedin
from dotenv import load_dotenv
import re
import os
import pprint
from linkedin_connections_scraper import scrape_connections
import time
import json


# Load environment variables from .env file
load_dotenv()
# Authenticate using any Linkedin user account credentials
email = os.getenv('LINKEDIN_ID')
password = os.getenv('LINKEDIN_PASS')
api = Linkedin(email, password)

username = str(input("Enter LinkedIn username: "))

def cal_score(username):
    linkedin_score = 0

    connection = scrape_connections(username)
    if(connection>=500):
        linkedin_score += 5
    elif(connection>=100):
        linkedin_score += 3
    elif(connection>=25):
        linkedin_score += 1

    profile = api.get_profile(username)
    headline = json.dumps(profile['headline'], indent=2, ensure_ascii=False)

    buzzwords = [
    "enthusiast", "lifelong learner", "aspiring", "passionate",
    "motivated", "visionary", "self-taught", "seeking opportunity",
    "ninja", "hacker", "guru", "wizard"]

    count = sum(1 for word in buzzwords if word in headline.lower())
    linkedin_score -= min(count, 5)

    posts = api.get_profile_posts(username)

    avg_length = 0
    if len(posts) > 0:
        avg_length = sum(len(post['commentary']['text']['text']) for post in posts) / len(posts)
        if avg_length > 750:
            linkedin_score += 2
            print(f"Average post length: {avg_length} characters, Score: -3")
        elif avg_length > 500:
            linkedin_score += 3
        elif avg_length <= 250:
            linkedin_score += 5
            print(f"Average post length: {avg_length} characters, Score: +2")

    return linkedin_score
    

print(cal_score(username))

