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
# jason
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

    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/top/?t=month"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", {"class": "Post"})

    print(posts)
    return render_template("read.html", subs=subs)


app.run(host="0.0.0.0")