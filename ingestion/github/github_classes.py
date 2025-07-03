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


    def get_more_data(self):
        url = f"https://api.github.com/users/{self.username}/repos"
        response = self.make_github_request(url)
        
        if response.status_code == 200:
            data = response.json()
            for repo in data:
                name = repo['name']
                primary_language = repo['language'] 
                
                # Get languages for this repo
                languages_url = f'https://api.github.com/repos/{self.username}/{name}/languages'
                languages_response = self.make_github_request(languages_url)
                
                if languages_response.status_code == 200:
                    languages_data = languages_response.json()
                    all_languages = list(languages_data.keys())
                else:
                    all_languages = [primary_language] if primary_language else []

                self.unique_langs.update(all_languages)

                # Get commits for this repo (fixed: use 'name' not 'self.name')
                commit_url = f'https://api.github.com/repos/{self.username}/{name}/commits?author={self.username}'
                commit_response = self.make_github_request(commit_url)
                
                # Fixed: use 'commit_response' not 'commits_response'
                if commit_response.status_code == 200:
                    number_of_commits = len(commit_response.json())
                    self.total_commits += number_of_commits
                else:
                    print(f"Could not get commits for {name}: {commit_response.status_code}")
                    number_of_commits = 0
                
                # Add stars collection
                self.total_stars += repo['stargazers_count']
                
                print(f"Repo: {name}, Commits: {number_of_commits}, Stars: {repo['stargazers_count']}")
        else:
            print(f'Error getting repositories: {response.status_code}')


lothnic = GitHubUser('lothnic')
lothnic.get_user_data()
lothnic.get_more_data()

print(f"Name: {lothnic.name}")
print(f"Username: {lothnic.username}")
print(f"Followers: {lothnic.followers}")
print(f"Following: {lothnic.following}")
print(f"Public Repos: {lothnic.public_repos}")
print(f"Bio: {lothnic.bio}")
print(f"Profile Picture: {lothnic.profile_picture}")
print(f"Distinct Languages: {list(set(lothnic.unique_langs))}")
print(f"Total Distinct Languages: {len(lothnic.unique_langs)}")
print(f'Total Commits: {lothnic.total_commits}')
