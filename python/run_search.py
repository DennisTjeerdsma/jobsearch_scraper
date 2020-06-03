from indeed import indeed
from monsterboard import monsterboard
import pandas as pd
import sys
import time

def load_filterwords():
    f = open("filterwords.txt", 'r')
    filterwords = []
    for line in f.readlines():
        filterwords.append(line[:-1])
    return filterwords

if __name__ == "__main__":
    filterwords = load_filterwords()
    file_name = "job_list"
    complete_job_list_indeed = pd.DataFrame([], columns=["Title", "Location", "Company", "Date", "url"])
    complete_job_list_monsterboard = pd.DataFrame([], columns=["Title", "Location", "Company", "Date", "url"])

    searchwords = ["Process Engineer", "Chemical Engineer", "Control Engineer", "junior engineer", 'automation engineer', 'procestechnoloog', 'proces ingenieur', 'procesingenieur']
    
    print("Starting job scraper")
    print("--------------------------------------------------------------------")
    
    for word in searchwords:
        df_indeed = indeed(word, filterwords)
        df_monsterboard = monsterboard(word, filterwords)
        complete_job_list_indeed = complete_job_list_indeed.append(df_indeed)
        complete_job_list_monsterboard = complete_job_list_monsterboard.append(df_monsterboard)
        time.sleep(1)

    complete_job_list_indeed.drop_duplicates(subset="url", keep="first", inplace=True)
    complete_job_list_monsterboard.drop_duplicates(subset="url", keep="first", inplace=True)


    print(f"{len(complete_job_list_indeed)} jobs found and added to excel list {file_name} on sheet Indeed")
    print(f"{len(complete_job_list_monsterboard)} jobs found and added to excel list {file_name} on sheet Monsterboard")
    complete_job_list_indeed.to_excel(file_name + ".xlsx", index=False, sheet_name="Indeed")
    complete_job_list_monsterboard.to_excel(file_name + ".xlsx", index=False, sheet_name="Monsterboard")
