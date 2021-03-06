import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time
from filter_words import filter_words


job_array = []

def indeed(job_title, filterwords, location="netherlands"):
    indeed_load_all_jobs(job_title, filterwords, location)
    df = create_dataframe(job_array)
    print(f"Indeed | {job_title} : -------- Done")
    return df

def indeed_load_jobs(job_title, location="netherlands", start=0):
    baseURL = "https://www.indeed.nl/jobs?"
    params = {"q": job_title, "l": location, "sort": "date", "start": start, 'fromage': 3}
    url = baseURL + urllib.parse.urlencode(params)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    jobs = soup.find(id="resultsCol")

    return jobs

def indeed_extract_jobs(jobs):
    job_elements = jobs.find_all('div', class_ = 'jobsearch-SerpJobCard')

    return job_elements

def indeed_extract_title(job_element):
    title_element = job_element.find("h2", class_ = "title") 

    return title_element.text.strip() if title_element else None

def indeed_extract_location(job_element):
    location_element = job_element.find("span", class_ = "location")

    if not location_element:
        location_element = job_element.find("div", class_ = "location")
    return location_element.text.strip() if location_element else None

def indeed_extract_company(job_element):
    company_element = job_element.find("span", class_ = "company")

    return company_element.text.strip() if company_element else None

def indeed_extract_date(job_element):
    date_element = job_element.find("span", class_ = "date")

    return date_element.text.strip() if date_element else None

def indeed_extract_url(job_element):
    url_element = job_element.find("a")["href"]
    baseURL = "https://indeed.nl"
    return baseURL + url_element

def indeed_extract_all_elements(job_element):
    title = indeed_extract_title(job_element)
    location = indeed_extract_location(job_element)
    company = indeed_extract_company(job_element)
    date = indeed_extract_date(job_element)
    url = indeed_extract_url(job_element)
    return [title, location, company, date, url]

def iterate_jobs(job_elements, filterwords):
    for i, job in enumerate(job_elements):     
        row = indeed_extract_all_elements(job)
        if filter_words(row[0],  filterwords):
            continue
        job_array.append(row)

def create_dataframe(data):
    df = pd.DataFrame(data, columns=["Title", "Location", "Company", "Date", "url"])
    return df

def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor

def indeed_load_all_jobs(job_title, filterwords, location):
    index = 0
    spinner = spinning_cursor()
    while True:
        jobs = indeed_load_jobs(job_title, location, start=index)
        job_elements = indeed_extract_jobs(jobs)
        iterate_jobs(job_elements, filterwords)
        index += 10
        time.sleep(0.5)
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\b')

        if len(job_elements) != 15:
            break
