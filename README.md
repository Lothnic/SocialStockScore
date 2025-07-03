# Whats next
- Completed Github scoring.
- Implement it with FastAPI and basic streamlit app.

# ~~REST APIS ~~ Library Used
Using PyGithub Library cause it provides easier auth and repo access.


- User data
https://api.github.com/users/{username}

- repos by username
https://api.github.com/users/{username}/repos

- commits by the author
https://api.github.com/repos/{username}/{name}/commits?author={username}

- for languages in a repo
https://api.github.com/repos/{username}/{name}/languages