#!/usr/bin/env python
# coding: utf-8

# In[70]:


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


# In[66]:


def scrap_links():
    links=[]
    url_start="https://www.amazon.jobs/en/search?offset="
    url_end="&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=applied%20scientist&city=&country=&region=&county=&query_options=&"
    for i in range(1000):
        if i%50==0:
            print(i)
        driver = webdriver.Chrome('chromedriver',options=chrome_options)
        driver.get(url_start+str(10*i)+url_end)
        ls=driver.find_elements(By.CLASS_NAME,"job-tile")
        for l in ls:
            links.append(l.find_element(By.CSS_SELECTOR,"a").get_attribute('href'))
        driver.quit()
    return links


# In[67]:


all_links=scrap_links()


# In[69]:


def job_scraper(link_ls):
    raw_data=[]
    urls=[]
    for l in link_ls:
        urls.append(l)
        raw_data.append(str(requests.get(l).content))
    
    return pd.DataFrame(list(zip(urls, raw_data)),columns =['url', 'raw_data'])


# In[75]:


df=job_scraper(all_links)


# In[ ]:




