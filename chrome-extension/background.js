chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (message.type === "CHECK_SUBREDDIT") {

        fetch(`http://127.0.0.1:8000/check/${message.subreddit}`)
            .then(response => response.json())
            .then(data => {
                sendResponse(data);
            })
            .catch(error => {
                sendResponse({
                    blocked: false,
                    reason: "backend_error",
                    error: error.toString()
                });
            });

        return true;
    }


    if (message.type === "ADD_SUBREDDIT") {

        fetch("http://127.0.0.1:8000/subreddits", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(message.subreddit)
        })
            .then(response => response.json())
            .then(data => {
                sendResponse(data);
            })
            .catch(error => {
                sendResponse({
                    message: "backend_error",
                    error: error.toString()
                });
            });

        return true;
    }

});