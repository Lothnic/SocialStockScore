# linkedin_login_once.py
from playwright.sync_api import sync_playwright
import os

EMAIL = os.getenv("LINKEDIN_ID")
PASSWORD = os.getenv("LINKEDIN_PASS")

with sync_playwright() as p:
    user_data_dir = "./.linkedin_user_data"
    browser = p.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=False)
    page = browser.new_page()

    print("[+] Opening LinkedIn login page...")
    page.goto("https://www.linkedin.com/login")

    page.fill("input#username", EMAIL)
    page.fill("input#password", PASSWORD)
    page.click("button[type='submit']")

    input("[✓] Login manually if needed. Press ENTER once done and you're on feed/profile page.")
    browser.close()
