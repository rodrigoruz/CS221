


from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import numpy as np

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=chrome_options)

def scrap_links()->list:
    """scrapes all links to jobs from Amazon's careers site

    Returns:
        _type_: list of all links
    """   
    links=[]
    url_start="https://www.amazon.jobs/en/search?offset="
    url_end="&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=applied%20scientist&city=&country=&region=&county=&query_options=&"
    for i in range(1000): #only first 1k tabs are accessible 
        if i%50==0: #progress check
            print(i)
        driver = webdriver.Chrome('chromedriver',options=chrome_options) #connecting to chrome 
        driver.get(url_start+str(10*i)+url_end) #getting the site we want, the offset at the site is always multiplication of 10
        ls=driver.find_elements(By.CLASS_NAME,"job-tile") #look for element by class name
        for l in ls:
            links.append(l.find_element(By.CSS_SELECTOR,"a").get_attribute('href')) #job link is always in href attribute of this element
        driver.quit() #ending connection, because it was causing problems when I've tried to iterate over all with one connection
    return links

def job_scraper(link_ls:list)->pd.DataFrame:
    """Scrapers all source code from provided URLs

    Args:
        link_ls (list): list of URLs

    Returns:
        pd.DataFrame: dataframe with 2 columns : URL and Source code
    """    
    raw_data=[]
    urls=[]
    for l in link_ls: #iterate over all links
        urls.append(l)
        raw_data.append(str(requests.get(l).content))
    
    return pd.DataFrame(list(zip(urls, raw_data)),columns =['url', 'raw_data'])
