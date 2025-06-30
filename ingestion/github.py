import requests

username = 'lothnic'

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
    total_commits = 0
    if response.status_code == 200:
        for repo in data:
            name = repo['name']
            
            # Get actual commit count for this repo (only commits by this user)
            commits_url = f'https://api.github.com/repos/{username}/{name}/commits?author={username}'
            commits_response = requests.get(commits_url)
            
            if commits_response.status_code == 200:
                number_of_commits = len(commits_response.json())
            else:
                number_of_commits = 0  # If we can't access commits (private repo, etc.)
            
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
        print(f'Total Commits: {total_commits}')
    else:
        print(f'Error: {response.status_code}')

get_repo_data('lothnic')