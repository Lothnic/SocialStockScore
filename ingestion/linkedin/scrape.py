from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = "thehorizondude@gmail.com"
password = os.getenv("LINKEDIN_PASS")  # Ensure you have set this in your .env file
actions.login(driver, email, password)
person = Person("https://www.linkedin.com/in/mayankjoshi0801", driver=driver)

print(person.name)