import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}
"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django",
]

app = Flask("DayEleven")


@app.route("/")
def check():
    return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():
    subs = list(request.args)
    result = []

    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/top/?t=month"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", {"class": "Post"})

        for post in posts:
            title = post.find("h3").get_text()
            url = post.find("a", {"class": "_3jOxDPIQ0KaOWpzvSQo-1s"}).get("href")
            upvote = post.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).get_text()
            if upvote == "•":
                continue
            if "k" in upvote:
                upvote = int(eval(upvote.replace("k", "")) * 1000)

            info = {"title": title, "url": url, "upvote": int(upvote), "sub": sub}
            result.append(info)

        result.sort(key=lambda x: x["upvote"], reverse=True)

    return render_template("read.html", subs=subs, result=result)


app.run(host="0.0.0.0", port=7000)
