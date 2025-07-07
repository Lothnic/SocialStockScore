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

username = str(input("Enter LinkedIn username: "))

# profile = api.get_profile(username)
# print(json.dumps(profile['headline'], indent=2, ensure_ascii=False))

# posts = api.get_profile_posts(username)

# for i in range(len(posts)):
#     post = posts[i]
#     pprint.pprint(json.dumps(post['commentary']['text']['text'], indent=2, ensure_ascii=False))

connections = api.get_profile_connections(username)
print(f"Total connections: {len(connections)}")
