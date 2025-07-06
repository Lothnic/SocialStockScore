from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import pprint

# Load environment variables from .env file
load_dotenv()
# Authenticate using any Linkedin user account credentials
password = os.getenv('LINKEDIN_PASS')
api = Linkedin('thehorizondude@gmail.com', password)

# GET a profile
# profile = api.get_profile('mayankjoshi0801')

posts = api.get_profile_posts('mayankjoshi0801')

pprint.pprint(posts)