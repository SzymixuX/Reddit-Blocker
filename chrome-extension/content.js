console.log("Reddit Blocker loaded");
document.documentElement.style.visibility = "hidden";
function getSubredditName() {
    const pathParts = window.location.pathname.split("/");

    if (pathParts.length >= 3 && pathParts[1].toLowerCase() === "r") {
        return pathParts[2].toLowerCase();
    }

    return null;
}

function detectNsfwFromPage() {
    const pageText = document.body.innerText.toLowerCase();

    console.log("PAGE TEXT SAMPLE:", pageText.slice(0, 1000));

    const nsfwSignals = [
        "nsfw",
        "adult content",
        "mature content",
        "over 18",
        "18+",
        "view community",
        "unreviewed content"
    ];

    return nsfwSignals.some(signal => pageText.includes(signal));
}

function redirectToBlockedPage(subredditName, reason) {
    window.location.href = chrome.runtime.getURL(
        `blocked.html?subreddit=${subredditName}&reason=${reason}`
    );
}

function checkSubreddit()
{
    const subredditName = getSubredditName();

    if (!subredditName) {
        console.log("No subreddit detected");
        return;
    }

    console.log("Detected subreddit:", subredditName);

    chrome.runtime.sendMessage(
        {
            type: "CHECK_SUBREDDIT",
            subreddit: subredditName
        },
        (data) => {
            console.log("Backend response:", JSON.stringify(data, null, 2));

            if (data && data.blocked === true) {
    redirectToBlockedPage(subredditName, data.reason);
    return;
}

    if (data && data.reason === "not_found")
    {
        const detectedNsfw = detectNsfwFromPage();

        console.log("Auto NSFW detection:", detectedNsfw);
            if (detectedNsfw)
            {

            chrome.runtime.sendMessage(
                {
                    type: "ADD_SUBREDDIT",
                    subreddit: {
                        name: subredditName,
                        is_nsfw: true,
                        category: "adult",
                        manual_blocked: false,
                        manual_allowed: false,
                        confidence: 0.7,
                        source: "extension_page_detection",
                        description: "Detected from Reddit page content"
                    }
                },
                (response) => {
                    console.log("Auto-added subreddit:", JSON.stringify(response, null, 2));
                    redirectToBlockedPage(subredditName, "auto_detected_nsfw");
                }
            );
                return;
            }
    }
    document.documentElement.style.visibility = "visible";
        }
    );
}
let lastUrl = location.href;

function runCheckWithDelay() {
    document.documentElement.style.visibility = "hidden";
    setTimeout(checkSubreddit, 500);
}

runCheckWithDelay();

setInterval(() => {
    if (location.href !== lastUrl) {
        lastUrl = location.href;
        console.log("URL changed:", lastUrl);
        runCheckWithDelay();
    }
}, 500);