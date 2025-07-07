from linkedin_api import Linkedin
from dotenv import load_dotenv
import os
import pprint
import json


# Load environment variables from .env file
load_dotenv()
# Authenticate using any Linkedin user account credentials
password = os.getenv('LINKEDIN_PASS')
api = Linkedin('thehorizondude@gmail.com', password)

# GET a profile
profile = api.get_profile('mayankjoshi0801')
print(json.dumps(profile['headline'], indent=2, ensure_ascii=False))



# posts = api.get_profile_posts('mayankjoshi0801')

# for i in range(len(posts)):
#     post = posts[i]
#     pprint.pprint(json.dumps(post['commentary']['text']['text'], indent=2, ensure_ascii=False))