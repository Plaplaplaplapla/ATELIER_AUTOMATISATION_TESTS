from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)

@app.route("/run")
def run():
    result = run_qos(10)
    save_run(result)
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    runs = list_runs(20)
    last_run = runs[0] if runs else None
    return render_template("dashboard.html", runs=runs, last_run=last_run)

@app.get("/")
def consignes():
     return render_template('consignes.html')

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True) 
