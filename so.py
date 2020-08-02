import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "s-pagination"})
  if pages != None:
    get_pages = pages.find_all("a")
    last_page = get_pages[-2].get_text(strip=True)
  else:
    last_page = 0
  return int(last_page)


def extract_job(html):
  title = html.find("h2").find("a")["title"]
  company, location = html.find("h3").find_all(
      "span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip("-").strip("\n")
  job_id = html['data-jobid']
  return {
    'title': title, 
    'company': company, 
    "link": f"https://stackoverflow.com/jobs/{job_id}"
  }


def extract_jobs(last_page, URL):
  jobs = []
  if last_page == 0:
    print(f"Scrappint SO: Page :{last_page}")
    result = requests.get(f"{URL}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  else:
    for page in range(last_page):
      print(f"Scrappint SO: Page :{page}")
      result = requests.get(f"{URL}&pg={page+1}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("div", {"class": "-job"})
      for result in results:
        job = extract_job(result)
        jobs.append(job)
  return jobs


def get_jobs(word):
  URL = f"https://stackoverflow.com/jobs?r=true&q={word}"
  last_page = get_last_page(URL)
  jobs = extract_jobs(last_page, URL)
  return jobs
