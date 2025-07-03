import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('CLIENT_ID'),
    client_secret = os.getenv('CLIENT_SECRET'),
    user_agent = 'SocialStockScore'
)

username = str(input("Enter Reddit username: "))

def fetch_user_data(username):
    reddit_user = reddit.redditor(username)

    comments = []
    for comment in reddit_user.comments.new(limit=50):
        comments.append({
            'id': comment.id,
            'body': comment.body,
            'created_utc': comment.created_utc,
            'score': comment.score
        })

    posts = []
    for post in reddit_user.submissions.new(limit=50):
        posts.append({
            'id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'created_utc': post.created_utc,
            'score': post.score
        })

    return comments, posts

def subreddit_diversity(username):
    reddit_user = reddit.redditor(username)
    subreddits = set()

    for comment in reddit_user.comments.new(limit=50):
        subreddits.add(comment.subreddit.display_name)

    for post in reddit_user.submissions.new(limit=50):
        subreddits.add(post.subreddit.display_name)

    return len(subreddits)

def total_karma(username):
    reddit_user = reddit.redditor(username)
    return reddit_user.comment_karma + reddit_user.link_karma

def cal_score(username, comments, posts):
    score = 0

    karma = total_karma(username)
    score += min(karma/1000 * 8, 8) #karma score

    diversity = subreddit_diversity(username)
    score += min(diversity/10 * 4, 4) #subreddits diversity score

    avg_length = sum(len(c['body']) for c in comments) / len(comments)
    if avg_length > 100: score += 4
    elif avg_length > 50: score += 2 #comment length score

    toxic_words = ["r*pe", "hate", "cringe", "simp", "incel", "sigma", "elon"]
    toxic_count = sum(any(word in c['body'].lower() for word in toxic_words) for c in comments)
    score -= min(toxic_count, 5) #profanity score

    return round(score, 2)

final_score = cal_score(username, *fetch_user_data(username))
print(f"Reddit user {username} has a score of {final_score}/20")
