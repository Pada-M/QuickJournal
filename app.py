from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, JournalEntry

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///journal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        mood = request.form.get("mood")
        new_entry = JournalEntry(title=title, content=content, mood=mood)
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")  # Print the actual error!
        return "Error saving journal entry."
    else:
        entries = JournalEntry.query.order_by(JournalEntry.date_created.desc()).all()
        return render_template("index.html", entries=entries)


if __name__ == "__main__":
    app.run(debug=True)
