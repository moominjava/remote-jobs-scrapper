import requests
from bs4 import BeautifulSoup


def extract_job(html):
  title = html.find("span", {"class": "title"}).text
  company = html.find("span", {"class": "company"}).text
  job_id = html.find("a", recursive=False)["href"]
  return {
    'title': title, 
    'company': company, 
    "link": f"https://weworkremotely.com{job_id}"
  }


def extract_jobs(URL):
  jobs = []
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.find("article").find_all("li")
  del results[-1]
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs


def get_jobs(word):
  URL = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(URL)
  return jobs
