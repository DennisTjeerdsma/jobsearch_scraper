from indeed import indeed
import pandas as pd
import sys

def load_filterwords():
    f = open("filterwords.txt", 'r')
    filterwords = []
    for line in f.readlines():
        filterwords.append(line[:-1])
    return filterwords

if __name__ == "__main__":
    filterwords = load_filterwords()
    file_name = "job_list"
    complete_job_list = pd.DataFrame([], columns=["Title", "Location", "Company", "Date", "url"])
    searchwords = ["Process Engineer", "Chemical Engineer", "Control Engineer", "junior engineer", 'automation engineer', 'procestechnoloog', 'proces ingenieur', 'procesingenieur']

    for word in searchwords:
        df = indeed(word, filterwords)
        complete_job_list = complete_job_list.append(df)

    print(f"{len(complete_job_list)} jobs found and added to excel list {file_name}")
    complete_job_list.to_excel(file_name + ".xlsx", index=False)
