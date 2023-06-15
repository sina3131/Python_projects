from bs4 import BeautifulSoup
from urllib.parse import urlparse
from settings import *


with open ("blacklist.txt") as f:
    bad_domain_list = set(f.read().split("\n")) # we use set here because searching become faster due to ani duplicate property of set

def get_page_content(row):
    soup = BeautifulSoup(row["html"])
    text = soup.get_text()
    return text
    
def tracker_urls(row):
    soup = BeautifulSoup(row["html"])
    scripts = soup.find_all("script", {"src": True}) # this part will find things such as google analytics js etc
    src = [s.get("src") for s in scripts]
    
    links = soup.find_all("href", {"href": True}) # finding href from the page
    href = [l.get("href") for l in links]

    all_domains = [urlparse(s) for s in src + href] # here we will remove uncesseray parts 
    # for exmaple https://www.googleadmin.com/script.js will be googleadmin.com
    
    bad_domain = [a for a in all_domains if a in bad_domain_list ]
    return len (bad_domain)
    
    

class Filter():
    # initilazing the class by passing a list or df of results and it will be stored as part of the class
    def __init__(self, results):
        self.filterd = results.copy()
        
    # First we create a content filter first we will apply get page content which on our self.filterd. 
    # Nexg we will count how many words appear on the page using lambda function
    # Then we will divide that by the median to see if the page has more or less than the mdeian
    # Then we create sort of punishment for the page with too little text and rank them very low if they have few words.
    def content_filter(self):
        page_content = self.filterd.apply(get_page_content, axis= 1)
        word_count = page_content.apply(lambda x: len(x.split(" ")))
        word_count /= word_count.median()
        
        word_count[word_count <= .5] = RESULT_COUNT
        word_count[word_count != RESULT_COUNT] = 0
        self.filterd["rank"] += word_count
        
    def filter(self):
        self.content_filter()
        self.filter_tracker()
        self.filterd["rank"] = self.filterd["rank"].round()
        return self.filterd
    
    
    # if the tracker count is bigger than the median then we will put it in very low rank thus penalizing those types of web pages
    def filter_tracker(self):
        tracker_count = self.filterd.apply(tracker_urls, axis= 1)
        tracker_count[tracker_count > tracker_count.median()] = RESULT_COUNT * 2
        self.filterd["rank"] += tracker_count