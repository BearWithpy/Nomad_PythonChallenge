import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
comment_db = {}
app = Flask("DayNine")


@app.route("/")
def hello():
    mode = request.args.get("mode", default="Popular")

    if mode not in db.keys():
        if mode == "Popular":
            response = requests.get(popular)
        elif mode == "New":
            response = requests.get(new)

        news = response.json()["hits"]
        db[mode] = news

    else:
        news = db[mode]

    return render_template("index.html", mode=mode, news=news)


@app.route("/<int:info_id>")
def detail(info_id):
    if id not in db.keys():
        detail_url = make_detail_url(info_id)
        response = requests.get(detail_url)
        info = response.json()
        comment_db[info_id] = info

    else:
        info = comment_db[id]

    return render_template("detail.html", info_id=info_id, info=info)


app.run(host="0.0.0.0", port=7000)
