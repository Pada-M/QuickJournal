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
    mood_icons = {
        "Happy": "😊 Happy",
        "Sad": "😢 Sad",
        "Angry": "😠 Angry",
        "Excited": "😄 Excited",
        "Calm": "😌 Calm",
        "": "No mood",
    }
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
        return render_template("index.html", entries=entries, mood_icons=mood_icons)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    entry = JournalEntry.query.get_or_404(id)
    if request.method == "POST":
        entry.title = request.form["title"]
        entry.content = request.form["content"]
        entry.mood = request.form.get("mood")
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error updating: {e}")
            return "There was a problem updating that entry."
    else:
        return render_template("edit.html", entry=entry)


@app.route("/delete/<int:id>")
def delete(id):
    entry_to_delete = JournalEntry.query.get_or_404(id)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error deleting: {e}")
        return "There was a problem deleting that entry."


if __name__ == "__main__":
    app.run(debug=True)
