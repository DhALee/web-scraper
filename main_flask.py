from flask import Flask, render_template, request, redirect
from scraper

app = Flask("web-scrapper")

# "@" is decorator which takes a function right under itself
@app.route("/") # "/" means root
def home():
    return render_template("index.html")

@app.route("/<username>") # "<>" is placeholder
def contact(username):
    return f"Hello {username}, how are you today?"

@app.route("/career")
def report():
    career = request.args.get("career")
    if career:
        career = career.lower() # in case when user type in capital words
    else:
        return redirect("/") # when input comes nothing go back to root page
    return render_template("career.html", search=career)

app.run(host="0.0.0.0")