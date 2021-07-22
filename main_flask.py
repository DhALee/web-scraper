from flask import Flask, render_template, request, redirect, send_file
from scraper_flask import get_jobs
from save import save_to_file

app = Flask("job-scraper")
# db should be out of router
db = {}  # fake database that store jobs to save searching time when user find same career that others searched before

# "@" is decorator which takes a function right under itself


@app.route("/")  # "/" means root
def index():
    return render_template("index.html")


@app.route("/<username>")  # "<>" is placeholder
def contact(username):
    return f"Hello {username}, how are you today?"


@app.route("/result")
def result():
    career = request.args.get("career")
    if career:
        career = career.lower()  # in case when user type in capital words
        existing_jobs = db.get(career)
        if existing_jobs:  # if db has career, return that data
            jobs = existing_jobs
        else:
            jobs = get_jobs(career)
            db[career] = jobs
    else:
        return redirect("/")  # when input comes nothing go back to root page

    # keyword "search" which could be any other words send variable "career" into result.html
    return render_template("result.html", result_num=len(jobs), search=career, jobs=jobs)


@app.route("/export")
def export():
    try:
        career = request.args.get("career")
        if not career:
            raise Exception()
        career = career.lower()
        jobs = db.get(career)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")


app.run(host="0.0.0.0", debug=True)
