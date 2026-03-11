from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import json
from tester.runner import run_qos
from storage import init_db, save_run, list_runs
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
init_db()

@app.get("/")
def consignes():
     return render_template('consignes.html')

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


@app.route("/health")
def health():
    runs = list_runs(1)

    if not runs:
        return {"status": "unknown"}

    last = runs[0]

    return {
        "status": "ok" if last["availability"] > 0.9 else "degraded",
        "availability": last["availability"],
        "error_rate": last["error_rate"],
        "avg_latency_ms": last["avg_latency_ms"],
        "p95_latency_ms": last["p95_latency_ms"]
    }

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True) 
