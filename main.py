from flask import Flask, render_template, request, redirect, send_file
from exporter import save_to_file
from so import get_jobs as so_get_jobs
from rm import get_jobs as rm_get_jobs
from ww import get_jobs as ww_get_jobs
"""
https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs
"""

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/list")
def list():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = ww_get_jobs(word) + rm_get_jobs(word) + so_get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template("list.html", 
  searchingBy = word,
  resultsNumber = len(jobs),
  jobs = jobs)


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")



app.run(host="0.0.0.0")



