"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for,
    Response,
)
from io import StringIO
from scrapper import scrape_remoteok, scrape_stackoverflow, scrape_wework
import csv

app = Flask("Final")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    term = request.args.get("term").lower()

    if term in db:
        jobs = db[term]
    else:
        wework_remotely_jobs = scrape_wework(term)
        remote_ok_jobs = scrape_remoteok(term)
        stack_overflow_jobs = scrape_stackoverflow(term)

        jobs = wework_remotely_jobs + remote_ok_jobs + stack_overflow_jobs
        db[term] = jobs

    return render_template("result.html", jobs=jobs, term=term)


#
# @app.route("/export")
# def export():
#     term = request.args.get("term").lower()
#     output = StringIO()
#     output.write("Link,Title,Company\n")
#
#     for job in db[term]:
#         for idx, val in enumerate(job.values()):
#             output.write(str(val))
#
#             if idx < (len(job) - 1):
#                 output.write(",")
#
#         output.write("\n")
#
#     response = Response(
#         output.getvalue(), mimetype="text/csv", content_type="application/octet-stream",
#     )
#     response.headers["Content-Disposition"] = f"attachment; filename={term}.csv"
#
#     return response
#
#     # https://frhyme.github.io/python-libs/file_download_with_flask/
#
#     # term = request.args.get("term").lower()
#     # with open(f"{term}.csv", mode="w", encoding="utf-8-sig") as job_file:
#     #     writer = csv.writer(job_file)
#     #     writer.writerow(["Link", "Company", "Title"])
#     #     for job in db[term]:
#     #         writer.writerow(list(job.values()))
#     #
#     # return send_file(
#     #     job_file,
#     #     mimetype="text/csv",
#     #     as_attachment=True,
#     #     attachment_filename=f"{term}.csv",
#     # )


@app.route("/export")
def export():
    term = request.args.get("term").lower()
    try:
        output = StringIO()
        output.write("Link,Title,Company\n")

        for job in db[term]:
            for i, value in enumerate(job.values()):
                output.write(str(value))

                if i < (len(job) - 1):
                    output.write(",")

            output.write("\n")

        response = Response(
            output.getvalue(),
            mimetype="text/csv",
            content_type="application/octet-stream",
        )

        response.headers["Content-Disposition"] = f"attachment; filename={term}.csv"

        return response
    except Exception:
        return redirect(url_for("home"))


app.run(host="0.0.0.0", debug=True, port=7000)
