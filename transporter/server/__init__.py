from flask import Flask, render_template
from http_basic_auth import requires_auth
from transporter import manager
from transporter.classes.manager import LogFile, JobFile

app = Flask(__name__, static_folder='public', static_url_path='/public')

@app.route("/")
@requires_auth
def index():
    return render_template('index.html', jobs=manager.all_jobs(), logs=manager.all_logs())


@app.route("/jobs/<path:project_path>")
@requires_auth
def show_job(project_path):
    job = JobFile(project_path)
    return render_template('show_job.html', job=job)


@app.route("/logs/<path:project_path>")
@requires_auth
def show_log(project_path):
    log = LogFile(project_path)

    return render_template('show_log.html', log=log)