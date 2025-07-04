import requests

# GH = (commit_score + lang_diversity + stars_score + profile_score)

# Scale each out of:
# commit_score = min(commits_last_year / 1000 * 10, 10)
# lang_diversity = min(unique_langs / 5 * 5, 5)
# stars_score = min(total_stars / 50 * 10, 10)
# profile_score = 5 if bio and profile picture else 0

def get_user_data(username):
    url = f'https://api.github.com/users/{username}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
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

def get_repo_data(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    data = response.json()

    print(data)

get_repo_data(lothnic)