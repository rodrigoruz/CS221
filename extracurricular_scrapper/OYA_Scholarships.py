# pip install bs4
encoding='utf-8'
# TODO:
    # Acortar descripcion
    # Links:
        #

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

URL_BASE = "https://oyaop.com/opportunities/scholarships-and-fellowships/"
Fecha_Final = "-"
premio="-"
remuneracion ="-"
costo="-"
Requisitos = "-"
Calificacion = "-"
Vacantes = "-"
Semestre = "-"
Carreras = "-"
selected_url = "-"
MAX_PAGES = 130
counter = 0
rows = []

# All in same directory
DRIVER_PATH = 'chromedriver.exe'

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

#Categoria / Tipo de Oportunidad
categoria = int(input("Elige el tipo de oportunidad...1:Evento, 2:Beca, 3:Pasantia, elige el #: "))
if categoria == 1:
    categoria = "Evento"
elif categoria == 2:
    categoria = "Beca"
elif categoria == 3:
    categoria = "Pasantia"
else:
    print("Invalid input!")
    import sys
    sys.exit()

# Nivel Educativo
nivel = int(input("Elige el Nivel Educativo...1:Preparatoria, 2:Universidad, 3:Posgrado, 4:Todos elige el #: "))
if nivel == 1:
    nivel = "Preparatoria"
elif nivel == 2:
    nivel = "Universidad"
elif nivel == 3:
    nivel = "Posgrado"
elif nivel == 4:
    nivel = "Todos"
else:
    print("Invalid input!")
    import sys
    sys.exit()

idiomas = int(input("Elige el Idioma...1:Español, 2:Inglés, 3:- elige el #: "))
if idiomas == 1:
    idiomas = "Español"
elif idiomas == 2:
    idiomas = "Inglés"
elif idiomas == 3:
    idiomas = "-"
else:
    print("Invalid input!")
    import sys
    sys.exit()

for i in range(1, MAX_PAGES):

    # Construyo la URL
    if i > 1:
        url = "%spage/%d/" % (URL_BASE, i)
    else:
        url = URL_BASE

    # Realizamos la peticion a la web
    req = requests.get(url)
    # Comprobamos que la peticion nos devuelve un Status Code = 200
    statusCode = req.status_code
    if statusCode == 200:

        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")

        # Obtenemos todos los divs donde estan las entradas
        entradas = html.find_all('div', {'class': 'col-12 col-sm-6 col-lg-4 py-3'})
        links = html.find_all('div', {'class': 'single_archive_specifics'})

        print(len(entradas))  # Print number of objects found
        print(len(links))  # Print number of objects found
        # Recorremos todas las entradas para extraer el titulo
        for j, entrada in enumerate(links):
            counter += 1
            if (j != 5) and (j != 11):
                ## Con el metodo "getText()" nos devuelve el HTML y el titulo de la oportunidad
                titulo = entrada.find('h5', {'class': 'col-12 py-2 single_archive_title'}).getText()
                links2 = entrada.find_all('a')
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
                URL = str(links5)  # Este es el URL de cada oportunidad
                req = requests.get(URL)  # Realizamos la peticion a la web
                status_code = req.status_code  # Comprobamos que la peticion nos devuelve un Status Code = 200
                if status_code == 200:
                    html = BeautifulSoup(req.text,
                                         "html.parser")  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
                    entradas = html.find_all('div', {
                        'class': 'col-md-9 col-12 ml-0 main pl-0 pr-0 pr-sm-3'})  # Obtenemos todos los divs donde estan las entradas
                    # Recorremos todas las entradas para extraer el titulo, autor y fecha
                    for i, entrada in enumerate(entradas):
                        ## Con el metodo "getText()" no nos devuelve el HTML
                        titulo = entrada.find('h1', {'col-12 px-0 my-0'}).getText()
                        try:
                            tags = entrada.find('div', {'class': 'tag_list'}).getText()
                        except:
                            tags = "-"
                        try:
                            tags = entrada.find('div', {'class': 'tag_list'}).getText()
                        except:
                            tags = "-"
                        try:
                            deadline = entrada.find('tr', {'class': 'opportunity_deadline'}).getText()
                        except:
                            deadline = "-"
                        try:
                            location = entrada.find('span', {'class': 'pl-1'}).getText()
                        except:
                            location = "-"
                        ## Extraer link del HTML
                        official_link = entrada.find('a', {'class': 'px-3 py-2'})
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
                        description = entrada.find('div', {
                            'class': 'description py-3'}).getText()  # description = entrada.find('p').getText()

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

                        Requisitos = entrada.find('div', {
                            'class': 'description py-3'}).getText()  # description = entrada.find('p').getText()
                        try:
                            split_string = Requisitos.split("Eligibility", 1)
                            Requisitos = split_string[1]
                        except:
                            pass
                        try:
                            split_string = Requisitos.split("Rules", 1)
                            Requisitos = split_string[1]
                        except:
                            pass
                        try:
                            split_string = Requisitos.split("Qualifications", 1)
                            Requisitos = split_string[1]
                        except:
                            pass
                        try:
                            split_string = Requisitos.split("Requirements", 1)
                            Requisitos = split_string[1]
                        except:
                            pass
                        try:
                            split_string = Requisitos.split("Criteria", 1)
                            Requisitos = split_string[1]
                        except:
                            pass
                        try:
                            split_string = Requisitos.split("Elegibilities", 1)
                            Requisitos = split_string[1]
                        except:
                            pass
                        try:
                            split_string = Requisitos.split("Also, visit", 1)
                            Requisitos = split_string[0]
                        except:
                            pass

                print(counter, "-", titulo, deadline, tags,location, official_link_4)
                # Generate Dataframe
                rows.append([titulo, categoria, tags,nivel, sofi,description,location,deadline,Fecha_Final,Requisitos,selected_url,official_link_4,Carreras,idiomas,Semestre,Vacantes,Calificacion,premio,remuneracion,costo])
                df = pd.DataFrame(rows, columns=["Titulo","Tipo","Tags","Nivel Educativo","Categoria","Descripcion","Ubicacion","Fecha Inicio", "Fecha Final","Requisitos","Url de IMAGEN","Url (PAGINA WEB)","Carreras","Idiomas","Semestre","Vacantes","Calificacion","Premio","Remuneracion","Costo"])  # print(df)
                df.to_csv('OYA_Scholarships.csv', encoding='utf-8-sig') #The encoding allows for writing special characters
                #df.to_csv('OYA.csv')
                # else:
                #   print(status_code)

    else:
        # Si ya no existe la pagina y me da un 400
        print("Status Code %d", statusCode, "Link:")
        break


