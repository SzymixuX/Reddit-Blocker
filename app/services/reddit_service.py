import requests


def get_subreddit_info(subreddit_name: str):

    url = f"https://www.reddit.com/r/{subreddit_name}/about.json"

    headers = {
        "User-Agent": "RedditBlocker/0.1 by local-development-project",
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        headers=headers
    )
    return {
        "status": response.status_code
    }