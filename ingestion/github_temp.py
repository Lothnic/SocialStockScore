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
            primary_language = repo['language']  # This is the primary language (single string)
            
            # Get all languages used in this repo
            languages_url = f'https://api.github.com/repos/{username}/{name}/languages'
            languages_response = requests.get(languages_url)
            
            if languages_response.status_code == 200:
                languages_data = languages_response.json()
                all_languages = list(languages_data.keys())  # Get all language names
            else:
                all_languages = [primary_language] if primary_language else []
            
            print(f"Repo Name: {name}")
            print(f"Primary Language: {primary_language}")
            print(f"All Languages: {', '.join(all_languages) if all_languages else 'None'}")
            print('-' * 40)
    else:
        print(f'Error: {response.status_code}')

get_repo_data('lothnic')