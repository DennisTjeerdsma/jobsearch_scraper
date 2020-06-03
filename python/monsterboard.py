from bs4 import BeautifulSoup
import urllib
import requests
from filter_words import filter_words
import time
import sys
import pandas as pd 

job_array = []


def monsterboard(job_title, filterwords, location="netherlands"):
    load_all_jobs(job_title, filterwords, location)
    df = create_dataframe(job_array)
    print(f"Monsterboard | {job_title} : -------- Done")
    return df

def monsterboard_load_jobs(job_title, location="netherlands", page=1):
    params = {'q': job_title, 'where': location, 'cy': 'nl', 'tm': 3, "page": page}
    baseURL = "https://www.monsterboard.nl/vacatures/zoeken/Fulltime_8?"
    url = baseURL + urllib.parse.urlencode(params)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    jobs = soup.find("div", {'id':"SearchResults"})
    return jobs

def extract_title(job_element):
    title_element = job_element.find("h2", {'class' : "title"})
    return title_element.text.strip() if title_element else None


def extract_location(job_element):
    location_element = job_element.find("div", {'class' : "location"})
    return location_element.text.strip() if location_element else None

def extract_jobs(jobs):
    job_elements = jobs.find_all("section", {"class": "card-content"})
    return job_elements

def extract_company(job_element):
    company_element = job_element.find("a", class_ = "name")

    return company_element.text.strip() if company_element else None

def extract_date(job_element):
    date_element = job_element.find("time")

    return date_element.text.strip() if date_element else None

def extract_url(job_element):
    try: 
        url_element = job_element.a.get('href')
    except:
        url_element = None

    return url_element if url_element else None

def extract_all_elements(job_element):
    title = extract_title(job_element)
    location = extract_location(job_element)
    company = extract_company(job_element)
    date = extract_date(job_element)
    url = extract_url(job_element)
    return [title, location, company, date, url]

def iterate_jobs(job_elements, filterwords):
    for i, job in enumerate(job_elements):     
        row = extract_all_elements(job)
        
        if not row[0]:
            continue
        elif filter_words(row[0],  filterwords):
            continue
        else:
            job_array.append(row)

def create_dataframe(data):
    df = pd.DataFrame(data, columns=["Title", "Location", "Company", "Date", "url"])
    return df
        
def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor

def load_all_jobs(job_title, filterwords, location):
    index = 1
    spinner = spinning_cursor()
    while True:
        jobs = monsterboard_load_jobs(job_title, location, page=index)
        job_elements = extract_jobs(jobs)
        iterate_jobs(job_elements, filterwords)
        index += 1
        time.sleep(0.5)
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\b')

        if len(job_elements) != 20:
            break

