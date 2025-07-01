import requests
import time
import os
from dotenv import load_dotenv, find_dotenv

username = 'lothnic'

load_dotenv(find_dotenv())
GITHUB_TOKEN = os.getenv('GIT_TOKEN')

def make_github_request(url):
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 403:
        print(f"Error 403: Rate limit exceeded or forbidden. Headers: {response.headers}")
        if 'X-RateLimit-Remaining' in response.headers:
            remaining = response.headers['X-RateLimit-Remaining']
            reset_time = response.headers.get('X-RateLimit-Reset', 'unknown')
            print(f"Rate limit remaining: {remaining}, resets at: {reset_time}")
    
    return response

# GH = (commit_score + lang_diversity + stars_score + profile_score)

# Scale each out of:
# commit_score = min(commits_last_year / 1000 * 10, 10)
# lang_diversity = min(unique_langs / 5 * 5, 5)
# stars_score = min(total_stars / 50 * 10, 10)
# profile_score = 5 if bio and profile picture else 0

def get_user_data(username):
    url = f'https://api.github.com/users/{username}'

    response = make_github_request(url)
    
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        username = data['login']
        followers = data['followers']
        following = data['following']
        public_repos = data['public_repos']
        
        print(f"Name: {name}")
        print(f"Username: {username}")
        print(f"Followers: {followers}")
        print(f"Following: {following}")
        print(f"Public Repos: {public_repos}")
    else:
        print(f'Error: {response.status_code}')
        if response.status_code == 403:
            print("This is likely a rate limit issue. Consider adding a GitHub token.")

def get_repo_data(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = make_github_request(url)
    
    if response.status_code != 200:
        print(f'Error getting repos: {response.status_code}')
        if response.status_code == 403:
            print("Rate limit exceeded. Try again later or add a GitHub token.")
        return
    
    data = response.json()
    total_commits = 0
    
    for repo in data:
        name = repo['name']
        
        # Get actual commit count for this repo (only commits by this user)
        commits_url = f'https://api.github.com/repos/{username}/{name}/commits?author={username}'
        commits_response = make_github_request(commits_url)
        
        if commits_response.status_code == 200:
            number_of_commits = len(commits_response.json())
        else:
            print(f"Could not get commits for {name}: {commits_response.status_code}")
            number_of_commits = 0
            if commits_response.status_code == 403:
                print("Rate limit hit while getting commits. Consider adding delays or a token.")
        
        total_commits += number_of_commits
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        language = repo['language']
        created_at = repo['created_at']
        updated_at = repo['updated_at']
        
        print(f"Repo Name: {name}")
        print(f"Stars: {stars}")
        print(f"Number of Commits: {number_of_commits}")
        print(f"Forks: {forks}")
        print(f"Language: {language}")
        print(f"Created At: {created_at}")
        print(f"Updated At: {updated_at}")
        print('-' * 40)
        
        # Add small delay to avoid hitting rate limits too quickly
        time.sleep(0.5)
    
    print(f'Total Commits: {total_commits}')

get_repo_data('lothnic')