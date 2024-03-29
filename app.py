import datetime, os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("DATABASE_URL"))
    app.db = client.microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
                (
                    entry["content"], 
                    entry["date"], 
                    datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
                )
                for entry in app.db.entries.find({})
            ]

        kwargs = {
            # 'entries': entries
            'entries': entries_with_date
        }
            
        return render_template("home.html", **kwargs, template_name="Jinja2")
    return app
