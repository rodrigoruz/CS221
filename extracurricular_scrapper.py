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
MAX_PAGES = 6
counter = 0
rows = []

# All in same directory
DRIVER_PATH = '/Users/rodrigoruz/Dook/data-science-base/scrapper/crawlers/chromedriver.exe'

# Methods for Image Scrapping
def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 3):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    # search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    search_url = 'https://www.google.com/search?tbm=isch&q=' + query + "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:m"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0
    while (image_count < max_links_to_fetch) & (
            error_clicks < 30):  # error clicks to stop when there are no more results to show by Google Images. You can tune the number
        scroll_to_end(wd)

        print('Starting search for Images')

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:max_links_to_fetch]:
            # try to click every thumbnail such that we can get the real image behind it
            print("Total Errors till now:", error_clicks)
            try:
                print('Trying to Click the Image')
                img.click()
                time.sleep(sleep_between_interactions)
                print('Image Click Successful!')
            except Exception:
                error_clicks = error_clicks + 1
                print('ERROR: Unable to Click the Image')
                if (results_start < number_results):
                    continue
                else:
                    break

            results_start = results_start + 1

            # extract image urls
            print('Extracting of Image URLs')
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            print('Current Total Image Count:', image_count)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                image_urls="-"
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path: str, file_name: str, url: str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path, file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

#Sofi
print("Choose Area of Interest...1:Antropología, 2:Arqueología, 3:Artes Escénicas, 4: Artes Visuales, 5:Biología, 6:Ciencias Espaciales")
print("7:Ciencias Naturales, 8:Ciencias Políticas, 9:Computación, 10:Economía, 11:Educación, 12:Emprendimiento, 13:Estadística, 14:Filosofía")
print("15:Física, 16:Geografía, 17:Historia, 18:Ingeniería y Tecnología, 19:Lenguaje y Literatura, 20:Leyes, 21:Matemáticas, 22:Marketing")
print("23:Medicina y Salud, 24:Negocios, 25:Psicología, 26:Química, 27:Sociología, 28:Teología, 29:Trabajo Social, 30:Ventas elige el #: ")
sofi = int(input())
if sofi == 1:
    sofi = "Antropología"
elif sofi == 2:
    sofi = "Arqueología"
elif sofi == 3:
    sofi = "Artes Escénicas"
elif sofi == 4:
    sofi = "Artes Visuales"
elif sofi == 5:
    sofi = "Biología"
elif sofi == 6:
    sofi = "Ciencias Espaciales"
elif sofi == 7:
    sofi = "Ciencias Naturales"
elif sofi == 8:
    sofi = "Ciencias Políticas"
elif sofi == 9:
    sofi = "Computación"
elif sofi == 10:
    sofi = "Economía"
elif sofi == 11:
    sofi = "Educación"
elif sofi == 12:
    sofi = "Emprendimiento"
elif sofi == 13:
    sofi = "Estadística"
elif sofi == 14:
    sofi = "Filosofía"
elif sofi == 15:
    sofi = "Física"
elif sofi == 16:
    sofi = "Geografía"
elif sofi == 17:
    sofi = "Historia"
elif sofi == 18:
    sofi = "Ingeniería y Tecnología"
elif sofi == 19:
    sofi = "Lenguaje y Literatura"
elif sofi == 20:
    sofi = "Leyes"
elif sofi == 21:
    sofi = "Matemáticas"
elif sofi == 22:
    sofi = "Marketing"
elif sofi == 23:
    sofi = "Medicina y Salud"
elif sofi == 24:
    sofi = "Negocios"
elif sofi == 25:
    sofi = "Psicología"
elif sofi == 26:
    sofi = "Química"
elif sofi == 27:
    sofi = "Sociología"
elif sofi == 28:
    sofi = "Teología"
elif sofi == 29:
    sofi = "Trabajo Social"
elif sofi == 30:
    sofi = "Ventas"
else:
    print("Invalid input!")
    import sys
    sys.exit()

#Categoria / Tipo de Oportunidad
categoria = "Pasantia"

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
                        deadline = entrada.find('tr', {'class': 'opportunity_deadline'}).getText()

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
                        ## URL Imagen
                        # taking user input
                        print(titulo)
                        if __name__ == '__main__':
                            queryinput = input("Ingresa un image query: ")
                            wd = webdriver.Chrome(executable_path=DRIVER_PATH)
                            queries = [queryinput]  # change your set of queries here
                            for query in queries:
                                wd.get('https://google.com')
                                search_box = wd.find_element_by_css_selector('input.gLFyf')
                                search_box.send_keys(query)
                                links = fetch_image_urls(query, 1, wd)  # 1 denotes no. of images you want to download
                                images_path = 'dataset/'
                                for i in links:
                                    persist_image(images_path, query, i)
                            wd.quit()
                            selected_url=str(links)
                            selected_url = selected_url[2:-2]

                print(counter, "-", titulo, deadline, location, official_link_4)
                # Generate Dataframe
                rows.append([titulo, categoria, nivel, sofi,description,location,deadline,Fecha_Final,Requisitos,selected_url,official_link_4,Carreras,idiomas,Semestre,Vacantes,Calificacion,premio,remuneracion,costo])
                df = pd.DataFrame(rows, columns=["Titulo","Tipo","Nivel Educativo","Categoria","Descripcion","Ubicacion","Fecha Inicio", "Fecha Final","Requisitos","Url de IMAGEN","Url (PAGINA WEB)","Carreras","Idiomas","Semestre","Vacantes","Calificacion","Premio","Remuneracion","Costo"])  # print(df)
                df.to_csv('OYA_AcademicJobs.csv', encoding='utf-8-sig') #The encoding allows for writing special characters
                #df.to_csv('OYA.csv')
                # else:
                #   print(status_code)

    else:
        # Si ya no existe la pagina y me da un 400
        print("Status Code %d", statusCode, "Link:")
        break
