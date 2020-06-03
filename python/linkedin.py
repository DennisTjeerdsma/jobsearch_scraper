import urllib
from bs4 import BeautifulSoup
import pandas as pd 
from filter_words import filter_words
import requests

job_array = []

def linkedIn_load_posts(job_title, location="netherlands", index=0):
    urlVars = {'keywords': job_title, 'location': location, 'sort':"DD", 'f_TPR': "r604800", 'start': index}
    baseURL = "https://www.linkedin.com/jobs/search/?"
    url = baseURL + urllib.parse.urlencode(urlVars)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    jobs = soup.find("ul", {"class" :"jobs-search-results__list artdeco-list"})
    return jobs

if __name__ == "__main__":
    jobs = linkedIn_load_posts("Process engineer")
    print(jobs)