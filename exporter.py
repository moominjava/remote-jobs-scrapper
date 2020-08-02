import csv

def save_to_file(jobs):
  file = open("Remote-Jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Apply"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return
