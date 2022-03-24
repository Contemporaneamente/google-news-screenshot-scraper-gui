from fileinput import filename
from importlib.resources import path
import util
import os
import requests
import time
import pandas as pd
import fake_useragent as fua
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
from fpdf import FPDF
import datetime
#------COSTANTI------#
#impostazione del motore di ricerca
#lo script funziona bene su google e quindi è basato sulle 
#stringhe di ricerca di google
#posta dopo la query con la formula (pageNumber - 1)*10 indica la pagina dei risultati
#0 è la prima pagina
SEARCH_ENGINE = "https://www.google.com/search?q="
GOOGLE_PAGE_STRING = "&start="
GOOGLE_NEWS_STRING = "&tbm=nws"
#------COSTANTI------#

#------QUERY PROCESSING------#
#splitto le keywords in un array
def SplitKeywords(inputString):
    keywordsArray = inputString.split(" ")
    return keywordsArray
    
#funzione che costruisce la query
def MakeQueryString(inputString, numberOfPages): 

    #split della stringa di ricerca in parole singole
    queryWord = inputString
    parsedWords = queryWord.split(" ")

    #temporanee di iterazione
    count = 0
    queryString = ""

    #determinazione della prima parola della query
    for word in parsedWords:
        if count == 0:
            queryString = word
        else:
            queryString = queryString + "+" + word
        count += 1
    #valore in output
    
    computedQuery = SEARCH_ENGINE + queryString

    pagesLinks = []
    i = 1

    while i <= numberOfPages:
        queryWithPages = ""
        queryWithPages = computedQuery + GOOGLE_PAGE_STRING + str((i - 1)*10)
        pagesLinks.append(queryWithPages + GOOGLE_NEWS_STRING)
        i += 1

    return computedQuery, pagesLinks
#------QUERY PROCESSING------#

#------SCREENSHOT PARSING------#
def OpenBrowser(cQuery):
#scatto screenshot alle prime n pagine di google news definite nelle variabili
    #aggiungo l'opzione di non aprire effettivamente la finestra di chrome mentre funziona
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=OFF")

    #apro il browser
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(cQuery + GOOGLE_NEWS_STRING)

    #attendo che si carichi il popup
    print("Caricamento popup in corso")
    time.sleep(10)
    print("Popup caricato")

    #trovo il bottone infame bastardo 
    element = driver.find_elements_by_class_name("VfPpkd-RLmnJb")

    #action set da effettuare nella finestra di browser aperta
    action = webdriver.ActionChains(driver)
    action.move_to_element(to_element=element[3])
    action.click()
    action.perform()

    #setto la dimensione della finestra
    driver.set_window_size(1000, 3000)

    #attendo il caricamento della pagina
    time.sleep(3)
    return driver
#------GOOGLE SEARCH PARSING------#

#------SCREENSHOTS TIMEEEE------#
def TakeScreenshotForPage(wDriver, pLinks, inputString):
    i = 1

    for pageLink in pLinks:
        wDriver.get(pageLink)
        util.fullpage_screenshot(driver=wDriver, file=f'imgs/{inputString}{i}.png')
        print("Screenshot: ", str(i), "/", str(len(pLinks)))
        i += 1       
#------SCREENSHOTS TIMEEEE------#

#------CREAZIONE DEL PDF------#
def CreatePdf(mainArgument):
    pdf = FPDF("P", "mm", (400, 800))
    w,h = 0,0

    imgFiles = []

    #itero tutti i file nella cartella delle immagini
    for fileName in os.scandir("imgs"):
        if fileName.is_file():
            imgFiles.append(fileName.path)

    #creo una pagina con lo screenshot per ogni screenshot
    for imgFile in imgFiles:
        image = imgFile
        pdf.add_page()
        pdf.image(image,0,0,w,h)
        
    todayDate = datetime.date.today()
    todayDateString = todayDate.strftime("%A, %d %b %Y")
    
    pdf.output(f"{todayDateString}_{mainArgument}.pdf")
#------CREAZIONE DEL PDF------#



