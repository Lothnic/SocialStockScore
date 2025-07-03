import praw

reddit = praw.Reddit(
    client_id = 'EaREKYz5-PxQ3isphK-ngA',
    client_secret = '1qVFcDbcCSFC16_B6kpiDECrjzIU-Q',
    user_agent = 'SocialStockScore'
)

username = 'wrongdoerbubbly'


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

fetch_profile = fetch_user_data(username)
print(f"Comments: {fetch_profile[0]}")
print(f"Posts: {fetch_profile[1]}")