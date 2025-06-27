import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

class GitHubDataFetcher:
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub API client
        
        Args:
            token: GitHub personal access token (optional but recommended for higher rate limits)
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_user_profile(self, username: str) -> Dict:
        """Get basic user profile information"""
        url = f"{self.base_url}/users/{username}"
        response = self.session.get(url)
        
        if response.status_code == 404:
            return {"error": "User not found"}
        elif response.status_code != 200:
            return {"error": f"API Error: {response.status_code}"}
        
        return response.json()
    
    def get_user_repos(self, username: str, per_page: int = 100) -> List[Dict]:
        """Get user's public repositories"""
        url = f"{self.base_url}/users/{username}/repos"
        params = {
            "per_page": per_page,
            "sort": "updated",
            "type": "owner"
        }
        
        response = self.session.get(url, params=params)
        
        if response.status_code != 200:
            return []
        
        return response.json()
    
    def get_user_activity(self, username: str) -> Dict:
        """Get user's recent activity events"""
        url = f"{self.base_url}/users/{username}/events/public"
        response = self.session.get(url)
        
        if response.status_code != 200:
            return {"events": []}
        
        return {"events": response.json()}
    
    def get_repo_languages(self, username: str, repo_name: str) -> Dict:
        """Get programming languages used in a repository"""
        url = f"{self.base_url}/repos/{username}/{repo_name}/languages"
        response = self.session.get(url)
        
        if response.status_code != 200:
            return {}
        
        return response.json()
    
    def calculate_social_metrics(self, username: str) -> Dict:
        """
        Calculate social stock metrics for a GitHub user
        """
        # Get basic profile
        profile = self.get_user_profile(username)
        if "error" in profile:
            return profile
        
        # Get repositories
        repos = self.get_user_repos(username)
        
        # Get recent activity
        activity = self.get_user_activity(username)
        
        # Calculate metrics
        metrics = {
            "username": username,
            "profile_data": {
                "followers": profile.get("followers", 0),
                "following": profile.get("following", 0),
                "public_repos": profile.get("public_repos", 0),
                "account_age_days": self._calculate_account_age(profile.get("created_at")),
                "has_bio": bool(profile.get("bio")),
                "has_company": bool(profile.get("company")),
                "has_location": bool(profile.get("location")),
                "has_website": bool(profile.get("blog")),
                "verified": profile.get("site_admin", False)
            },
            "repository_metrics": self._analyze_repositories(repos),
            "activity_metrics": self._analyze_activity(activity["events"]),
            "calculated_scores": {}
        }
        
        # Calculate final scores
        metrics["calculated_scores"] = self._calculate_scores(metrics)
        
        return metrics
    
    def _calculate_account_age(self, created_at: str) -> int:
        """Calculate account age in days"""
        if not created_at:
            return 0
        
        created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        return (datetime.now(created_date.tzinfo) - created_date).days
    
    def _analyze_repositories(self, repos: List[Dict]) -> Dict:
        """Analyze repository data for scoring"""
        if not repos:
            return {
                "total_stars": 0,
                "total_forks": 0,
                "avg_stars_per_repo": 0,
                "languages": {},
                "recent_activity": False,
                "repo_count": 0
            }
        
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos)
        
        # Language analysis
        languages = {}
        for repo in repos:
            if repo.get("language"):
                lang = repo["language"]
                languages[lang] = languages.get(lang, 0) + 1
        
        # Check for recent activity (last 30 days)
        recent_activity = False
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for repo in repos:
            if repo.get("updated_at"):
                updated_date = datetime.fromisoformat(repo["updated_at"].replace('Z', '+00:00'))
                if updated_date > cutoff_date.replace(tzinfo=updated_date.tzinfo):
                    recent_activity = True
                    break
        
        return {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "avg_stars_per_repo": total_stars / len(repos) if repos else 0,
            "languages": languages,
            "recent_activity": recent_activity,
            "repo_count": len(repos)
        }
    
    def _analyze_activity(self, events: List[Dict]) -> Dict:
        """Analyze recent activity events"""
        if not events:
            return {
                "recent_commits": 0,
                "recent_prs": 0,
                "recent_issues": 0,
                "activity_score": 0
            }
        
        # Count different types of activities
        commits = sum(1 for event in events if event.get("type") == "PushEvent")
        prs = sum(1 for event in events if event.get("type") == "PullRequestEvent")
        issues = sum(1 for event in events if event.get("type") == "IssuesEvent")
        
        return {
            "recent_commits": commits,
            "recent_prs": prs,
            "recent_issues": issues,
            "activity_score": commits * 1 + prs * 2 + issues * 1.5
        }
    
    def _calculate_scores(self, metrics: Dict) -> Dict:
        """Calculate final S3 scores based on metrics"""
        profile = metrics["profile_data"]
        repos = metrics["repository_metrics"]
        activity = metrics["activity_metrics"]
        
        # Influence Score (0-100)
        influence_score = min(100, (
            profile["followers"] * 0.3 +
            repos["total_stars"] * 0.4 +
            repos["total_forks"] * 0.2 +
            profile["public_repos"] * 0.1
        ))
        
        # Activity Score (0-100)
        activity_score = min(100, (
            activity["activity_score"] * 2 +
            (20 if repos["recent_activity"] else 0) +
            (10 if profile["account_age_days"] > 365 else 0)
        ))
        
        # Profile Completeness Score (0-100)
        completeness_score = (
            (20 if profile["has_bio"] else 0) +
            (15 if profile["has_company"] else 0) +
            (15 if profile["has_location"] else 0) +
            (15 if profile["has_website"] else 0) +
            (10 if profile["followers"] > 0 else 0) +
            (10 if profile["public_repos"] > 0 else 0) +
            (15 if len(repos["languages"]) > 0 else 0)
        )
        
        # Overall S3 Score (weighted average)
        s3_score = (
            influence_score * 0.4 +
            activity_score * 0.35 +
            completeness_score * 0.25
        )
        
        return {
            "influence_score": round(influence_score, 2),
            "activity_score": round(activity_score, 2),
            "completeness_score": round(completeness_score, 2),
            "s3_score": round(s3_score, 2),
            "rating": self._get_rating(s3_score)
        }
    
    def _get_rating(self, score: float) -> str:
        """Convert numerical score to rating"""
        if score >= 80:
            return "🚀 Sigma Dev"
        elif score >= 60:
            return "💪 Chad Coder"
        elif score >= 40:
            return "📈 Rising Star"
        elif score >= 20:
            return "🌱 Newbie"
        else:
            return "👻 Ghost Profile"

# Example usage
if __name__ == "__main__":
    # Initialize without token (rate limited) or with token
    github_fetcher = GitHubDataFetcher()  # Add your token here
    
    # Get comprehensive data for a user
    username = "lothnic"  # Replace with actual username
    user_data = github_fetcher.calculate_social_metrics(username)
    
    print(json.dumps(user_data, indent=2))
    
    # Quick access to S3 score
    if "calculated_scores" in user_data:
        s3_score = user_data["calculated_scores"]["s3_score"]
        rating = user_data["calculated_scores"]["rating"]
        print(f"\n{username}'s S3 Score: {s3_score}/100 - {rating}")