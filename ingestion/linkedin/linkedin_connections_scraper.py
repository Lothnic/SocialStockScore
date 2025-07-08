from playwright.sync_api import sync_playwright
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = "thehorizondude@gmail.com"
PASSWORD = os.getenv("LINKEDIN_PASS")



def scrape_connections(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to False if you want to watch it work
        context = browser.new_context()
        page = context.new_page()

        # --- STEP 1: LOGIN ---
        print("[+] Logging into LinkedIn...")
        page.goto("https://www.linkedin.com/login")
        page.fill("input#username", EMAIL)
        page.fill("input#password", PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        time.sleep(3)

        # --- STEP 2: OPEN profile ---
        print("[+] Navigating to user's page...")
        page.goto(f"https://www.linkedin.com/in/{username}")
        time.sleep(2)

        content = page.content()

        connection_text = page.locator("span:has-text('connections')").first.text_content()

        net_connections = connection_text.split()[0].replace(',', '')
        
        browser.close()
        print(f"[+] Total connections: {net_connections}")
        return int(net_connections)

