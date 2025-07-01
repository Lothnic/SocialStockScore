import requests
import json
import os
from dotenv import load_dotenv

# GH = (commit_score + lang_diversity + stars_score + profile_score)

# Scale each out of:
# commit_score = min(commits_last_year / 1000 * 10, 10)
# lang_diversity = min(unique_langs / 5 * 5, 5)
# stars_score = min(total_stars / 50 * 10, 10)
# profile_score = 5 if bio and profile picture else 0

class GitHubUser:
    def __init__(self,username):
        self.username = username
        self.unique_langs = set()
        self.total_commits = 0
        self.total_stars = 0
        self.profile_score = 0
        self.commit_score = 0
        self.lang_diversity = 0
        self.load_env()
    
    def load_env(self):
        load_dotenv()
        self.github_token = os.getenv('GITHUB_TOKEN')
    
    def make_github_request(self, url):
        headers = {}
        if self.github_token:
            headers['Authorization'] = f'Bearer {self.github_token}'
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 403:
            print(f"Error 403: Rate limit exceeded or forbidden. Headers: {response.headers}")
            if 'X-RateLimit-Remaining' in response.headers:
                remaining = response.headers['X-RateLimit-Remaining']
                reset_time = response.headers.get('X-RateLimit-Reset', 'unknown')
                print(f"Rate limit remaining: {remaining}, resets at: {reset_time}")
        
        return response
    
    def get_user_data(self):
        url = f"https://api.github.com/users/{self.username}"
        response = self.make_github_request(url)
        if response.status_code == 200:
            data = response.json()
            self.name = data.get('name', 'N/A')
            self.followers = data.get('followers', 0)
            self.following = data.get('following', 0)
            self.public_repos = data.get('public_repos', 0)
            self.bio = data.get('bio', '')
            self.profile_picture = data.get('avatar_url', '')
        else:
            print(f'Error: {response.status_code}')

lothnic = GitHubUser('lothnic')
lothnic.get_user_data()

print(f"Name: {lothnic.name}")
print(f"Username: {lothnic.username}")
print(f"Followers: {lothnic.followers}")
print(f"Following: {lothnic.following}")
print(f"Public Repos: {lothnic.public_repos}")
print(f"Bio: {lothnic.bio}")
print(f"Profile Picture: {lothnic.profile_picture}")