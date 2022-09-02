from importlib.resources import path
import pandas as pd
import fake_useragent as fua
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import cochrane_string

#------COSTANTI------#
#impostazione del motore di ricerca
#lo script funziona bene su google e quindi è basato sulle 
#stringhe di ricerca di google

SEARCH_GOOGLE = "https://www.google.com/search?q="
SEARCH_PUBMED = "https://pubmed.ncbi.nlm.nih.gov/?term="
SEARCH_COCHRANE = cochrane_string.COCHRANE_STRING
SEARCH_APA = "https://www.apa.org/search?query="


PUBMED = "https://pubmed.ncbi.nlm.nih.gov"
#posta dopo la query con la formula (pageNumber - 1)*10 indica la pagina dei risultati
GOOGLE_PAGE_STRING = "&start="
PUBMED_PAGE_STRING = "&page="
APA_PAGE_STRING = "&page="
#------COSTANTI------#

#------VARIABILI------#
totalString = input("Inserisci l'argomento di ricerca: ")
numberOfPages = 3

googleSearch = 0
pubmedSearch = 1
cochraneSearch = 0
apaSearch = 0
#------VARIABILI------#

#------QUERY PROCESSING------#

pagesLinks = []
pagesLinksPubmed = []
pagesLinksCochrane = []
pagesLinksApa = []

#funzione che costruisce la query
def MakeQueryString(inputString):  

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
    return queryString

if googleSearch:
    #------GOOGLE QUERY------#
    computedQuery = SEARCH_GOOGLE + MakeQueryString(totalString)
    i = 1
    while i <= numberOfPages:
        queryWithPages = ""
        queryWithPages = computedQuery + GOOGLE_PAGE_STRING + str((i - 1)*10)
        i += 1

elif pubmedSearch:
    #------PUBMED QUERY------#
    computedQuery = SEARCH_PUBMED + MakeQueryString(totalString)
    i = 1 
    while i <= numberOfPages:
        queryWithPages = ""
        queryWithPages = computedQuery + PUBMED_PAGE_STRING + str(i)
        print(queryWithPages)
        pagesLinksPubmed.append(queryWithPages)
        i += 1

elif apaSearch == 1:
    #------APA QUERY------#
    computedQuery = SEARCH_APA + MakeQueryString(totalString)
    i = 1 
    while i <= numberOfPages:
        queryWithPages = ""
        queryWithPages = computedQuery + PUBMED_PAGE_STRING + str(i)
        print(queryWithPages)
        pagesLinksApa.append(queryWithPages)
        i += 1

elif cochraneSearch == 1:
    #------COCHRANE QUERY------#
    computedQuery = SEARCH_COCHRANE + MakeQueryString(totalString)
    pagesLinksCochrane.append(computedQuery)


i = 1
#------QUERY PROCESSING------#

#------GOOGLE SEARCH PARSING------#
#per estrarre i primi 10 link da una ricerca google

#aggiungo l'opzione di non aprire effettivamente la finestra di chrome mentre funziona
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

foundLinks = []
foundTitles = []
foundCits = []
foundDois = []
foundDates = []
i = 1

#apro il browser
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

#------GOOGLE------#
if googleSearch == 1:
    for pageLink in pagesLinks:
        progress = "step " + str(i) + " su " + str(len(pagesLinks) - 1)
        print(progress)

        #apro la pagina di ricerca sul browser selezionato
        driver.get(pageLink)

        #ricerca dei link con la classe del div sotto definita
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.find_all("div", class_="yuRUbf")

        for link in links:
            foundLinks.append(link.a.get("href"))

        for link in links:
            foundTitles.append(link.find("h3").contents)
        i += 1

#------PUBMED------#        
elif pubmedSearch == 1:
    for pageLink in pagesLinksPubmed:
        progress = "step " + str(i) + " su " + str(len(pagesLinksPubmed))
        print(progress)

        #apro la pagina di ricerca sul browser selezionato
        driver.get(pageLink)

        #ricerca dei link con la classe del div sotto definita
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.find_all("div", class_="docsum-content")

        for link in links:
            foundLinks.append(PUBMED + link.a.get("href"))

        for link in links:
            foundTitles.append(link.find("a").text)

        i += 1
    i = 1
    for foundLink in foundLinks:
        progress = "step " + str(i) + " su " + str(len(foundLinks))
        print(progress)
        driver.get(foundLink)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        foundCits.append(soup.find("span", class_="cit").text)
        if(hasattr(soup.find("span", class_="citation-doi"), "text")):
            foundDois.append(soup.find("span", class_="citation-doi").text)
        else:
            foundDois.append("")
        if(hasattr(soup.find("span", class_="secondary-date"), "text")):
            foundDates.append(soup.find("span", class_="secondary-date").text)
        else:
            foundDates.append("")
        i += 1

#------APA------#
elif apaSearch == 1:
    for pageLink in pagesLinksApa:
        progress = "step " + str(i) + " su " + str(len(pagesLinksApa))
        print(progress)

        #apro la pagina di ricerca sul browser selezionato
        driver.get(pageLink)

        #ricerca dei link con la classe del div sotto definita
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.save_screenshot("screenshot.png")
        links = soup.find_all("ul")

        print(links)

        i += 1
    i = 1

#------COCHRANE------#  
elif cochraneSearch == 1:
    for pageLink in pagesLinksCochrane:
        progress = "step " + str(i) + " su " + str(len(pagesLinksCochrane))
        print(progress)

        #apro la pagina di ricerca sul browser selezionato
        driver.get(pageLink)

        #ricerca dei link con la classe del div sotto definita
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.find_all("h3", class_="result-title")
        i += 1
        for link in links:
            foundLinks.append(link)
            foundTitles.append(link)
            foundDois.append(link)
            foundCits.append(link)
            foundDates.append(link)



#print(foundLinks)
#print(foundTitles)
#------GOOGLE SEARCH PARSING------#

#------DATA OUTPUT------#

dataObtained = {"Titoli": foundTitles, "Links": foundLinks, "Cit": foundCits, "DOI": foundDois, "Date": foundDates}
#dataObtained = {"Titoli": foundTitles, "Links": foundLinks}
totalDataFrame = pd.DataFrame(data=dataObtained)
#
totalDataFrame.to_csv(f"{totalString}.csv")
#print(totalDataFrame)