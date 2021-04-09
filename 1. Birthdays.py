import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Insert new birthday data into birthdays database
        # ---------------------------------------

        # Check if new birthday data was submitted
        if request.form.get("name"):

            # Access data submitted via the form
            name = request.form.get("name")
            month = request.form.get("month")
            day = request.form.get("day")

            # Add the user's entry into the database
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        # Modify data in birthdays database
        # ---------------------------------

        # Check if modified birthday data was submitted
        if request.form.get("mod_name"):

            # Access data submitted via the form
            mod_name = request.form.get("mod_name")
            mod_month = request.form.get("mod_month")
            mod_day = request.form.get("mod_day")

            # Update the user's entry in the database
            db.execute("UPDATE birthdays SET month = ?, day = ? WHERE name = ?", mod_month, mod_day, mod_name)

        # Delete data from birthday database
        # -----------------------------------

        # Check if deleted birthday data was submitted
        if request.form.get("delete_name"):

            # Access data submitted via the form
            delete_name = request.form.get("delete_name")

            # Delete the user's entry from the database
            db.execute("DELETE FROM birthdays WHERE name = ?", delete_name)

        # Re-render the index page with changes included
        return redirect("/")

    else:

        # Display the birthday entries in the database on index.html

        # Query the birthdays.db database for all birthdays
        birthdays = db.execute("SELECT * FROM birthdays")

        # Pass all data to index.html
        return render_template("index.html", birthdays=birthdays)
