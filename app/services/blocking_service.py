from app.repositories import subreddit_repository


def check_subreddit(subreddit_name: str):
    row = subreddit_repository.get_by_name(subreddit_name)

    if row is None:
        return {
            "subreddit": subreddit_name,
            "blocked": False,
            "reason": "not_found"
        }

    subreddit = subreddit_repository.row_to_subreddit_response(row)

    if subreddit["is_nsfw"]:
        return {
            "subreddit": subreddit["name"],
            "blocked": True,
            "reason": "nsfw"
        }

    if subreddit["manual_blocked"]:
        return {
            "subreddit": subreddit["name"],
            "blocked": True,
            "reason": "manual_blocked"
        }

    return {
        "subreddit": subreddit["name"],
        "blocked": False,
        "reason": "allowed"
    }