import requests
from bs4 import BeautifulSoup


def extract_job(html):
  title = html.find("h2", {"itemprop": "title"}).text
  company = html.find("h3", {"itemprop": "name"}).text
  job_id = html.find("a", {"class": "preventLink"})["href"]
  return {
    'title': title, 
    'company': company, 
    "link": f"https://remoteok.io{job_id}"
  }


def extract_jobs(URL):
  jobs = []
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find_all("tr", {"class": "job"})
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs


def get_jobs(word):
  URL = f"https://remoteok.io/remote-dev+{word}-jobs"
  jobs = extract_jobs(URL)
  return jobs
