import os

from cs50 import SQL

from datetime import datetime, date
import time
import io
import csv
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, calculate_hours

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#db = SQL("sqlite:///final.db")
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Libary to use SQLite database
db = SQL("sqlite:///final.db")

@app.route("/", methods=['POST', 'GET'])
@login_required
def index():
    if request.method == "GET":
        # Create tables if not exists in data base
        db.execute("CREATE TABLE IF NOT EXISTS 'user' ('id_usuario' integer PRIMARY KEY NOT NULL, 'nome' text NOT NULL, 'email' text NOT NULL, 'setor' text NOT NULL,'centroCusto' text NOT NULL,'admissao' DATA NOT NULL, 'gestor' text NOT NULL, 'horarioEntrada' time NOT NULL, 'horarioSaida' time NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS 'login' ('id' integer PRIMARY KEY NOT NULL,'username' text NOT NULL, 'hash' text NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS 'control' ('controlId' integer PRIMARY KEY NOT NULL, 'user_id' integer NOT NULL, 'action_id' integer NOT NULL, 'date' text, 'hour' text)")
        db.execute("CREATE TABLE IF NOT EXISTS 'action' ('id' integer PRIMARY KEY NOT NULL, 'name' text NOT NULL)")

        verification = db.execute("SELECT * FROM control where user_id = ? ", session["user_id"])

        # Take the username from database
        name = db.execute("SELECT username FROM login WHERE id = ?", session["user_id"])

        if len(verification) != 0:
            # Take today's date
            today = date.today()

            # Take the current day hours
            day = db.execute("SELECT action_id, date, hour FROM control WHERE user_id = ? AND date = ?", session["user_id"], today)

            # Calculating total worked hours in day
            total_hours_day = calculate_hours(day)

            # Today's month
            currentMonth = datetime.now().month
            currentYear = datetime.now().year

            inicial_date =  str(currentYear) + "-0" + str(currentMonth)  + "-01"
            final_date = str(currentYear) + "-0" + str(currentMonth)  + "-31"

            # Take the current month hours
            month = db.execute("SELECT action_id, date, hour FROM control WHERE user_id = ? AND date BETWEEN ? and ?", session["user_id"], inicial_date, final_date)

             # Calculating total worked hours in a month
            month_hours = calculate_hours(month)
            total_hours_month = ""

            for hour in month_hours:
                month_hours[hour]
                totalSecs = 0
                timeParts = [int(s) for s in month_hours[hour].split(':')]
                totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
            totalSecs, sec = divmod(totalSecs, 60)
            hr, min = divmod(totalSecs, 60)
            total_hours_month = "%d:%02d" % (hr, min)

            return render_template("index.html", name=name, total_month=total_hours_month, total_day=total_hours_day)

        return render_template("index.html", name=name)

    if request.method == "POST":

        if request.form['submit'] == 'entry':

            #Get user name
            name = db.execute("SELECT username FROM login WHERE id = ?", session["user_id"])

            # Select registers from controler
            check_entry = db.execute("SELECT * FROM control WHERE user_id = ? AND action_id = 1 AND date = date()", session["user_id"])
            check_exit = db.execute("SELECT * FROM control WHERE user_id = ? AND action_id = 2 AND date = date()", session["user_id"])

            if len(check_entry) == 0:

                # Insert entry in database
                db.execute("INSERT INTO control (user_id, action_id, date, hour) VALUES (?, 1, date(), time('now','-3 hours'))", session["user_id"])

                flash("Parabéns seu horário de entrada foi registrado!")
                return render_template("index.html", name=name)

            elif len(check_entry) == 1 and len(check_exit) == 0:

                # Check if already registred and entry whitout and exit
                flash("Você já registrou sua entrada, clique em saída para registrar o almoço!")
                return render_template("index.html", name=name)

            elif len(check_entry) == 1 and len(check_exit) == 1:

                # Insert second entry in database
                db.execute("INSERT INTO control (user_id, action_id, date, hour) VALUES (?, 1, date(), time('now','-3 hours'))", session["user_id"])
                flash("Bom início de segundo turmo!!")
                return render_template("index.html", name=name)

            elif len(check_entry) == 2 and len(check_exit) == 1:

                flash("Você já registrou sua volta do almoço, clique em sair para encerrar o turno!!")
                return render_template("index.html", name=name)

            else:

                flash("Você já possui dois registros hoje! Vá descansar.")
                return render_template("index.html", name=name)

        if request.form['submit'] == 'exit':

            # Get username
            name = db.execute("SELECT username FROM login WHERE id = ?", session["user_id"])

             # Select registers from controler
            check_exit = db.execute("SELECT * FROM control WHERE user_id = ? AND action_id = 2 AND date = date()", session["user_id"])
            check_entry = db.execute("SELECT * FROM control WHERE user_id = ? AND action_id = 1 AND date = date()", session["user_id"])

            if len(check_exit) == 0 and len(check_entry) == 1:

                # Insert entry in database
                db.execute("INSERT INTO control (user_id, action_id, date, hour) VALUES (?, 2, date(), time('now','-3 hours'))", session["user_id"])

                flash("Parabéns seu horário de saída para o almoço foi registrado!")
                return render_template("index.html", name=name)

            elif len(check_exit) == 1 and len(check_entry) == 1:

                flash("Você já registrou sua volta do almoço, clique em entrada para registrar a volta do almoço!")
                return render_template("index.html", name=name)

            elif len(check_exit) == 1 and len(check_entry) == 2:

                # Insert second entry in database
                db.execute("INSERT INTO control (user_id, action_id, date, hour) VALUES (?, 2, date(), time('now','-3 hours'))", session["user_id"])
                flash("Bom descanso, até amanhã!!")
                return render_template("index.html", name=name)

            else:
                flash("Você já possui dois registros hoje! Vá descansar.")
                return render_template("index.html", name=name)

        return apology("Sorry", 400)

@app.route("/report", methods=['POST', 'GET'])
@login_required
def report():
    if request.method == "POST":

        if not request.form.get("inicial_date"):
            return apology("Must provide a Inicial Date!", 403)
        if not request.form.get("final_date"):
            return apology("Must provide a Final Date!", 403)

        inicial_date = request.form.get("inicial_date")
        final_date = request.form.get("final_date")

        # Take hours between what user inputs
        report = db.execute("SELECT action_id, date, hour FROM control WHERE user_id = ? AND date BETWEEN ? and ?", session["user_id"], inicial_date, final_date)

        # Take users information
        userinformation = db.execute("SELECT nome, email, setor, centroCusto, admissao, gestor FROM user WHERE id_usuario = ?", session["user_id"])

        organized_report = calculate_hours(report)

        return render_template("generated.html", report=organized_report, userinformation=userinformation, inicial_date=inicial_date, final_date=final_date)
    else:
        # Take the username from database
        name = db.execute("SELECT username FROM login WHERE id = ?", session["user_id"])
        return render_template("report.html", name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

      # Ensure username was submitted
      if not request.form.get("username"):
          return apology("must provide username", 403)

      # Ensure password was submitted
      elif not request.form.get("password"):
          return apology("must provide password", 403)

      # Query database for username
      rows = db.execute("SELECT * FROM login WHERE username = ?", request.form.get("username"))

      # Ensure username exists and password is correct
      if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
          return apology("invalid username and/or password", 403)

      # Remember which user has logged in
      session["user_id"] = rows[0]["id"]

      # Redirect user to home page
      return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":

        # Verification of fields
        for campo in range(8):
            if not request.form.get(str(campo)):
                return apology("Must fill all the fields!", 403)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide a Username", 403)
        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Must provide a Password", 403)
        # Ensure password match confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Must passaword and confirmation match", 403)

        # Checking if username is already in use
        user = db.execute("SELECT username FROM login WHERE username = ?", request.form.get("username"))

        # Error message
        if user != []:
            return apology("Must provide a different username", 403)

        # Transforming datas to include in database
        hashed_password = generate_password_hash(request.form.get("password"))
        user = request.form.get("username")

        # Include user in login table
        db.execute("INSERT INTO login (username, hash) VALUES (?,?)", user, hashed_password)

        # Transforming strings text in uppercases
        name = (request.form.get("0")).upper()
        sector = (request.form.get("2")).upper()
        costcenter = (request.form.get("3")).upper()
        boss = (request.form.get("5")).upper()

        # Include new worker
        db.execute("INSERT INTO user (nome, email, setor, centroCusto, admissao, gestor, horarioEntrada, horarioSaida) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", name, request.form.get("1"), sector, costcenter, request.form.get("4"), boss, request.form.get("6"), request.form.get("7"))

        # Message registrated concluded
        flash("Registrado!")

        return render_template("login.html")

    else:
        return render_template("register.html")
