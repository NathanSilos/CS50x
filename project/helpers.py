import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime

def login_required(f):
    #"""
    #Decorate routes to require login.

    #https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    #"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def calculate_hours(report):
    # Declaring variables
    organized_report = {}
    days = []

    # Separate each day in a dictionary
    for day in report:
        actual_day = day['date']
        organized_report[actual_day] = []
        if actual_day not in days:
            days.append(actual_day)

    # Including hours per day
    for day in report:
        actual_day = day['date']
        organized_report[actual_day].append(day['hour'])

    # Working with hours
    for day in days:
        hours = organized_report[day]
        FMT = '%H:%M:%S'

        # Calculate the different between hours
        first_period = datetime.strptime(hours[1], FMT) - datetime.strptime(hours[0], FMT)
        if len(hours) == 4:
            second_period = datetime.strptime(hours[3], FMT) - datetime.strptime(hours[2], FMT)
            timeList = [str(first_period), str(second_period)]
        else:
            timeList = [str(first_period)]

        # Calculate the sum between differents hours
        totalSecs = 0
        for tm in timeList:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        organized_report[day] = "%d:%02d:%02d" % (hr, min, sec)

    return organized_report