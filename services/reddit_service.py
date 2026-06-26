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

    print("STATUS:", response.status_code)
    print("TEXT:", response.text[:300])

    return {
        "status": response.status_code
    }