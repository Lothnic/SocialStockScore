from linkedin_api import Linkedin
from dotenv import load_dotenv
import re
import os
import pprint
from playwright.sync_api import sync_playwright
import time
import json
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
# Authenticate using any Linkedin user account credentials
email = os.getenv('LINKEDIN_ID')
password = os.getenv('LINKEDIN_PASS')
api = Linkedin(email, password)

def cal_score(username):
    linkedin_score = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()

        try:
            print("Navigating to LinkedIn login...")
            page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            
            if "feed" in page.url:
                print("Already logged in!")
            else:
                page.fill("input#username", email)
                page.fill("input#password", password)
                page.click("button[type='submit']")
                
                page.wait_for_load_state("networkidle")
                time.sleep(3)
                
                if "challenge" in page.url or "checkpoint" in page.url:
                    print("Login challenge detected. Please complete manually.")
                    input("Press Enter after completing the challenge...")

            print(f"Navigating to profile: {username}")
            page.goto(f"https://www.linkedin.com/in/{username}/", wait_until="networkidle")
            time.sleep(3)

            connection_selectors = [
                "span:has-text('connections')",
                "span:has-text('connection')", 
                "[data-test-id='connections']",
                ".pv-top-card--list-bullet li:has-text('connection')",
                ".pv-top-card-v2-ctas .pv-top-card-v2-ctas__actions button:has-text('Connect')",
                "section.pv-top-card span:has-text('connection')"
            ]
            
            connection_text = None
            net_connections = 0
            
            for selector in connection_selectors:
                try:
                    print(f"Trying selector: {selector}")
                    element = page.wait_for_selector(selector, timeout=5000)
                    if element:
                        connection_text = element.text_content()
                        print(f"Found connection text: {connection_text}")
                        break
                except Exception as e:
                    print(f"Selector {selector} failed: {e}")
                    continue
            
            if not connection_text:
                print("No connection element found, searching page content...")
                content = page.content()
                
                connection_patterns = [
                    r'(\d+[\+,]*)\s*connections?',
                    r'(\d+[\+,]*)\s*followers?',
                    r'Connect with (\d+[\+,]*)'
                ]
                
                for pattern in connection_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        connection_text = matches[0]
                        print(f"Found via regex: {connection_text}")
                        break
            
            if connection_text:
                numbers_only = re.findall(r'\d+', connection_text.replace(',', ''))
                if numbers_only:
                    net_connections = int(numbers_only[0])
                    print(f"Extracted connections: {net_connections}")
                else:
                    print("Could not extract number from connection text")
            else:
                print("No connection information found")
                page.screenshot(path=f"linkedin_debug_{username}.png")
                
        except Exception as e:
            print(f"Error during scraping: {e}")
            page.screenshot(path=f"linkedin_error_{username}.png")
            
        finally:
            browser.close()
  
        connection = net_connections
        if(connection >= 500):
            linkedin_score += 5
        elif(connection >= 100):
            linkedin_score += 3
        elif(connection >= 25):
            linkedin_score += 1


    try:
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
                print(f"Average post length: {avg_length} characters, Score: +2")
            elif avg_length > 500:
                linkedin_score += 3
            elif avg_length <= 250:
                linkedin_score += 5
                print(f"Average post length: {avg_length} characters, Score: +5")
    
    except Exception as e:
        print(f"Error with LinkedIn API: {e}")

    print(f"Total LinkedIn Score: {linkedin_score}")
    return linkedin_score