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

# we get about 0.01 per commit

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

        print(f"Token loaded successfully: {token[:3]}...")

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
                # Filter commits only made by this user)
                user_commits = repo.get_commits(author=self._user)
                user_commit_count = user_commits.totalCount
                
                self.total_stars += repo.stargazers_count
                self.total_commits += user_commit_count
                
                # Getting all languages used in the repository
                try:
                    languages = repo.get_languages()
                    for language in languages.keys():
                        self.unique_langs.add(language)
                except Exception as lang_error:
                    if repo.language:
                        self.unique_langs.add(repo.language)
                    print(f"Could not get languages for {repo.name}: {lang_error}")

            except Exception as e:
                print(f"Error fetching repo {repo.name} for {self.username}: {e}")
                continue
                
    def cal_score(self):
        self.fetch_repos()
        
        self.commit_score = min(self.total_commits / 1000 * 10, 10)
        self.lang_diversity = min(len(self.unique_langs) / 5 * 5, 5)
        self.stars_score = min(self.total_stars / 50 * 10, 10)
        self.profile_score = 5 if self.bio and self.profile_picture else 0
        
        gh_score = self.commit_score + self.lang_diversity + self.stars_score + self.profile_score
        return gh_score
        
def score_github_user(username: str):
    user = GithubUser(username)
    score = user.cal_score()

    # Return detailed breakdown
    return round(score, 2)
    #, {
    #     "Commits Last Year": user.total_commits,
    #     "Unique Languages": len(user.unique_langs),
    #     "Total Stars": user.total_stars,
    #     "Bio Present": bool(user.bio),
    #     "Profile Picture": bool(user.profile_picture),
    #     "Commit Score": round(user.commit_score, 2),
    #     "Lang Diversity Score": round(user.lang_diversity, 2),
    #     "Stars Score": round(user.stars_score, 2),
    #     "Profile Score": round(user.profile_score, 2)
    # }
