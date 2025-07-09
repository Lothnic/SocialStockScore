from playwright.sync_api import sync_playwright
import time
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('LINKEDIN_ID')
PASSWORD = os.getenv("LINKEDIN_PASS")

def scrape_connections(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to False if you want to watch it work
        context = browser.new_context()
        page = context.new_page()

        # --- STEP 1: LOGIN ---
        page.goto("https://www.linkedin.com/login")
        page.fill("input#username", EMAIL)
        page.fill("input#password", PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_load_state("load")
        time.sleep(5)

        # --- STEP 2: OPEN profile ---
        page.goto(f"https://www.linkedin.com/in/{username}")
        page.wait_for_selector("span:has-text('connections')", timeout=10000)

        content = page.content()

        connection_text = page.locator("span:has-text('connections')").first.text_content()

        numbers_only = re.findall(r'\d+', connection_text.replace(',', ''))
        
        browser.close()

        net_connections = int(numbers_only[0])
        return net_connections

