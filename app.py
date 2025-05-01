from flask import Flask, render_template, request, redirect, url_for, session
import json
from dotenv import load_dotenv
import os

load_dotenv()



from analytics import (
    get_device_stats,
    get_custom_page_views,
    get_top_product_page_views,
    get_total_website_users,
   
    get_last_search_terms
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
USERNAME = os.getenv("DASHBOARD_USERNAME")
PASSWORD = os.getenv("DASHBOARD_PASSWORD")
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    results = {}
    start_date = end_date = None

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Load config.json
        with open("config.json") as f:
            config = json.load(f)

        # Inject date range into config for analytics.py functions
        config["date_range"] = {
            "start_date": start_date,
            "end_date": end_date
        }
    
        # Call analytics functions
        results = {
            "start_date": start_date,
            "end_date": end_date,
            "total_visitors": get_total_website_users(config),
            "device_stats": get_device_stats(config),
            "page_views": get_custom_page_views(config),
            "top_product_pages": [
            {
                "name": path.split("/")[2].replace("-", " ").title(),
                "views": views
            }
            for path, views in get_top_product_page_views(config)
],

             
            "last_search_terms": get_last_search_terms(config)
        }

    return render_template(
    "dashboard.html",
    results=results,

    start_date=start_date,
    end_date=end_date
)

if __name__ == "__main__":
    app.run(debug=True)
