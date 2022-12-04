#Yes
# URL = "http://www.hackalist.org/"
#URL ="https://mlh.io/seasons/2021/events"

# pip install bs4
encoding='utf-8'

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import time
import sys
import random
import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib

URL_BASE = "https://oyaop.com/jobs/academic-job/"
final_date = "-"
prize="-"
compensation ="-"
cost="-"
requisites = "-"
grade = "-"
vacancies = "-"
semester = "-"
majors = "-"
selected_url = "-"
MAX_PAGES = 6
counter = 0
rows = []

# All in same directory
DRIVER_PATH = '/Users/rodrigoruz/CS221/extracurricular_scrapper/chromedriver.exe'

#Sofi
print("Choose Discipline...1:Anthropology, 2:Archeology, 3:Scenic Arts, 4: Visual Arts, 5:Biology, 6:Aerospace")
print("7:Natural Science, 8:Political Science, 9:Computer Science, 10:Economics, 11:Education, 12:Entrepreneurship, 13:Statistics, 14:Philosophy")
print("15:Physics, 16:Geography, 17:History, 18:Engineering and Technology, 19:Language and Literature, 20:Law, 21:Mathematics, 22:Marketing")
print("23:Medicine and Health, 24:Business, 25:Psychology, 26:Chemistry, 27:Sociology, 28:Theology, 29:Social Work, 30:Sales. Choose a #: ")
sofi = int(input())
if sofi == 1:
    sofi = "Anthropology"
elif sofi == 2:
    sofi = "Archeology"
elif sofi == 3:
    sofi = "Scenic Arts"
elif sofi == 4:
    sofi = "Visual Arts"
elif sofi == 5:
    sofi = "Biology"
elif sofi == 6:
    sofi = "Aerospace"
elif sofi == 7:
    sofi = "Natural Science"
elif sofi == 8:
    sofi = "Political Science"
elif sofi == 9:
    sofi = "Computer Science"
elif sofi == 10:
    sofi = "Economics"
elif sofi == 11:
    sofi = "Education"
elif sofi == 12:
    sofi = "Entrepreneurship"
elif sofi == 13:
    sofi = "Statistics"
elif sofi == 14:
    sofi = "Philosophy"
elif sofi == 15:
    sofi = "Physics"
elif sofi == 16:
    sofi = "Geography"
elif sofi == 17:
    sofi = "History"
elif sofi == 18:
    sofi = "Engineering and Technology"
elif sofi == 19:
    sofi = "Language and Literature"
elif sofi == 20:
    sofi = "Law"
elif sofi == 21:
    sofi = "Mathematics"
elif sofi == 22:
    sofi = "Marketing"
elif sofi == 23:
    sofi = "Medicine and Health"
elif sofi == 24:
    sofi = "Business"
elif sofi == 25:
    sofi = "Psychology"
elif sofi == 26:
    sofi = "Chemistry"
elif sofi == 27:
    sofi = "Sociology"
elif sofi == 28:
    sofi = "Theology"
elif sofi == 29:
    sofi = "Social Work"
elif sofi == 30:
    sofi = "Sales"
else:
    print("Invalid input!")
    import sys
    sys.exit()

#type / Tipo de Oportunidad
type = "Pasantia"

# academic_level Educativo
academic_level = int(input("Choose an Education Level...1:High School, 2:University, 3:Graduate School, 4:All. Choose a #: "))
if academic_level == 1:
    academic_level = "High School"
elif academic_level == 2:
    academic_level = "University"
elif academic_level == 3:
    academic_level = "Graduate School"
elif academic_level == 4:
    academic_level = "All"
else:
    print("Invalid input!")
    import sys
    sys.exit()

languages = int(input("Choose a Language...1:Spanish, 2:English, 3:- Choose a #: "))
if languages == 1:
    languages = "Spanish"
elif languages == 2:
    languages = "English"
elif languages == 3:
    languages = "-"
else:
    print("Invalid input!")
    import sys
    sys.exit()

for i in range(1, MAX_PAGES): # Iterate through the number of pages in the website

    # Build the URL
    if i > 1:
        url = "%spage/%d/" % (URL_BASE, i)
    else:
        url = URL_BASE

    # Make a web request
    req = requests.get(url)
    # Confirm the request status code = 200
    statusCode = req.status_code
    if statusCode == 200:

        # Pass the HTML content of the web to get a BeautifulSoup() object
        html = BeautifulSoup(req.text, "html.parser")

        # Obtain all divs with input
        records = html.find_all('div', {'class': 'col-12 col-sm-6 col-lg-4 py-3'})
        links = html.find_all('div', {'class': 'single_archive_specifics'})

        print(len(records))  # Print number of objects found
        print(len(links))  # Print number of objects found
        # Iterate through records to extract title
        for j, record in enumerate(links):
            counter += 1
            if (j != 5) and (j != 11):
                ## Use "getText()" method to return HTML and opportunity title
                title = record.find('h5', {'class': 'col-12 py-2 single_archive_title'}).getText()
                links2 = record.find_all('a')
                ## This takes the URL of the opportunity and extracts it from html (retreiving whats between "")
                import re

                links3 = str(links2)  # type(links3) convert to string
                string = links3
                match = re.findall('href.+"><', string, flags=re.IGNORECASE)
                if match:
                    links4 = match[0]
                string = links4
                match = re.findall('http.+/', string, flags=re.IGNORECASE)
                if match:
                    links5 = match[0]
                # PRINT THIS TO SEE OYA Opportunity Link print("\n", links5)
                ## Now that we have the link of each opportunity, we go ahead and scrap it
                URL = str(links5)  # This is the URL for each opportunity
                req = requests.get(URL)  # Make request to web
                status_code = req.status_code  # Confirm that request returns Status Code = 200
                if status_code == 200:
                    html = BeautifulSoup(req.text,
                                         "html.parser")  # Pass web HTML content to a BeautifulSoup() object
                    records = html.find_all('div', {
                        'class': 'col-md-9 col-12 ml-0 main pl-0 pr-0 pr-sm-3'})  # Obtain all divs in the records
                    # Iterate through all records to extract title, author and date
                    for i, record in enumerate(records):
                        ## Use "getText()" to return HTML
                        title = record.find('h1', {'col-12 px-0 my-0'}).getText()
                        deadline = record.find('tr', {'class': 'opportunity_deadline'}).getText()
                        tags = record.find('div', {'class': 'tag_list'}).getText()

                        try:
                            location = record.find('span', {'class': 'pl-1'}).getText()
                        except:
                            location = "-"
                        ## Extraer link del HTML
                        official_link = record.find('a', {'class': 'px-3 py-2'})
                        string = str(official_link)
                        match = re.findall('href.+" target', string, flags=re.IGNORECASE)
                        if match:
                            official_link_2 = match[0]
                        string = official_link_2
                        match = re.findall('http.+"', string, flags=re.IGNORECASE)
                        if match:
                            official_link_3 = match[0]
                        official_link_4 = official_link_3[:-1];
                        # print("Description:",description,"\n") #Uncomment to print description
                        description = record.find('div', {
                            'class': 'description py-3'}).getText()  # description = record.find('p').getText()

                        try:
                            split_string = description.split("Eligibility", 1)
                            description = split_string[0]
                        except:
                            pass
                        try:
                            split_string = description.split("Requirements", 1)
                            description = split_string[0]
                        except:
                            pass
                        try:
                            split_string = description.split("Qualifications", 1)
                            description = split_string[0]
                        except:
                            pass
                        try:
                            split_string = description.split("Rules", 1)
                            description = split_string[0]
                        except:
                            pass
                        try:
                            split_string = description.split("Elegibilities", 1)
                            description = split_string[0]
                        except:
                            pass
                        try:
                            split_string = description.split("Criteria", 1)
                            description = split_string[0]
                        except:
                            pass
                        split_string = description.split("Details", 1)
                        description = split_string[1]

                        requisites = record.find('div', {
                            'class': 'description py-3'}).getText()  # description = record.find('p').getText()
                        try:
                            split_string = requisites.split("Eligibility", 1)
                            requisites = split_string[1]
                        except:
                            pass
                        try:
                            split_string = requisites.split("Rules", 1)
                            requisites = split_string[1]
                        except:
                            pass
                        try:
                            split_string = requisites.split("Qualifications", 1)
                            requisites = split_string[1]
                        except:
                            pass
                        try:
                            split_string = requisites.split("Requirements", 1)
                            requisites = split_string[1]
                        except:
                            pass
                        try:
                            split_string = requisites.split("Criteria", 1)
                            requisites = split_string[1]
                        except:
                            pass
                        try:
                            split_string = requisites.split("Elegibilities", 1)
                            requisites = split_string[1]
                        except:
                            pass
                        try:
                            split_string = requisites.split("Also, visit", 1)
                            requisites = split_string[0]
                        except:
                            pass

                print(counter, "-", title,deadline, tags,location, official_link_4)
                # Generate Dataframe
                rows.append([title, type, tags,academic_level, sofi,description,location,deadline,final_date,requisites,selected_url,official_link_4,majors,languages,semester,vacancies,grade,prize,compensation,cost])
                df = pd.DataFrame(rows, columns=["title","Tipo","tags","academic level","discipline","description","location","deadline", "final_date","requisites","Image URL","Url","majors","languages","semester","vacancies","grade","prize","compensation","cost"])  # print(df)
                df.to_csv('OYA_AcademicJobs.csv', encoding='utf-8-sig') #The encoding allows for writing special characters
                #df.to_csv('OYA.csv')
                # else:
                #   print(status_code)

    else:
        # If page doesnt exist, return error code 400
        print("Status Code %d", statusCode, "Link:")
        break
