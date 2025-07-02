from github import Github
from github import Auth
import os
from dotenv import load_dotenv

# GH = (commit_score + lang_diversity + stars_score + profile_score)

# Scale each out of:
# commit_score = min(commits_last_year / 1000 * 10, 10)
# lang_diversity = min(unique_langs / 5 * 5, 5)
# stars_score = min(total_stars / 50 * 10, 10)
# profile_score = 5 if bio and profile picture else 0


class GithubUser:
    def __init__(self,username):
        self.username = username
        self._client = None
        self._user = None
        self.unique_langs = set()
        self.total_commits = 0
        self.total_stars = 0
        self.bio = ''
        self.profile_picture = ''
        self.name = ''
        self.followers = 0
        self.following = 0
        self.public_repos = 0
        self.load_client()
    
    def load_client(self):
        load_dotenv()
        token = os.getenv("GIT_TOKEN")
        if not token:
            raise ValueError("GIT_TOKEN not found in .env")

        print(f"✅ Token loaded successfully: {token[:3]}...")  # Obfuscated for safety

        self._auth = Auth.Token(token)
        self._client = Github(auth=self._auth)
    
    def fetch_profile(self):
        try:
            self._user = self._client.get_user(self.username)
            self.name = self._user.name or 'N/A'
            self.followers = self._user.followers
            self.following = self._user.following
            self.public_repos = self._user.public_repos
            self.bio = self._user.bio or ''
            self.profile_picture = self._user.avatar_url or ''
        except e as Exception:
            print(f"Error fetching profile for {self.username}: {e}")
            self._user = None

    def fetch_repos(self):
        if not self._user:
            self.fetch_profile() 
        for repo in self._user.get_repos():
            try:
                print(repo.name)
                print(repo.stargazers_count)
                print(repo.language)
                
                # Filter commits by author (only commits made by this user)
                user_commits = repo.get_commits(author=self._user)
                user_commit_count = user_commits.totalCount
                
                print(f"User commits: {user_commit_count}")
                self.total_stars += repo.stargazers_count
                self.total_commits += user_commit_count
                print(20*'-')
            except Exception as e:
                print(f"Error fetching repo {repo.name} for {self.username}: {e}")
                continue


user1 = GithubUser('lothnic')
user1.fetch_repos()
print(user1.total_commits)
print(user1.total_stars)