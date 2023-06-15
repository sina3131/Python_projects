from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBstorage
from urllib.parse import quote_plus
from datetime import datetime, timedelta

# Quote_plus fixes the space problem between words



# Resultucount/ 10 says that eage page contains 10 search result 
# could be adjusted depending on result count setting
def search_api(query, pages=int(RESULT_COUNT/10)):
    results = []
    # First record of each page example page 1=1 2=11 3=21 
    for i in range(0, pages):
        start = i * 10 + 1
        url = SEARCH_URL.format(
            key= SEARCH_KEY,
            cx = SEARCH_ID,
            query = quote_plus(query),
            start = start
        )
        response = requests.get(url)
        data = response.json()
        print(data)
        results += data["items"]
    res_dataframe = pd.DataFrame.from_dict(results)
    res_dataframe["rank"] = list(range(1, res_dataframe.shape[0] + 1 ))
    res_dataframe = res_dataframe[["link","rank","snippet","title"]]
    return res_dataframe
        
search_api("lego")


# Scraping the links and storing the content on a list.
def scrape_page(links):
    html = []
    for i in links:
        try:   
            data = requests.get(i, timeout=4)
            html.append(data.text)
        except RequestException:
            html.append("")
    return html

# this next function is our main search function
# we first connect to our db, then we check wether we already run a query
# or if the data already exist, if it does we change data type of created
# to datetime, if the result isn't in out db we use our search_api, and 
# scrape function to fetch the data, change the format and finally store it 
# in database


def search(query):
    start = DBstorage()
    columns = ["query", "rank","link","snippet","title","html","created"]
    stored_result = start.query_result(query)
    if stored_result.shape[0] > 0:
        stored_result["created"] = pd.to_datetime(stored_result["created"])
        return stored_result[columns]
    results = search_api(query)
    results["html"] = scrape_page(results["link"])
    results = results[results["html"].str.len()>0] .copy()
    
    results["query"] = query
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    results = results[columns]
    results.apply(lambda x: start.insert_values(x), axis=1)
    return results