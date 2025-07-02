from github import Github
from github import Auth
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("GIT_TOKEN")
auth = Auth.Token(access_token)

g = Github(auth=auth)

user = g.get_user('lothnic')

print(user.name)

g.close()