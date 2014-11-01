#!/usr/bin/python
# -*-coding:Utf-8 -*

import sys
import os
import feedparser
from bs4 import BeautifulSoup
import requests
from io import open as iopen
import arrow

#Personal modules
sys.path.append('/home/djipey/informatique/python/batbelt')
import batbelt


#urls = ["http://onlinelibrary.wiley.com/rss/journal/10.1002/%28ISSN%291521-3773",
        #"http://feeds.feedburner.com/acs/jacsat"
       #]

def getData(journal, entry):

    """Get the data. Starts from the data contained in the RSS flux, and if necessary,
    parse the website for supplementary infos. Download the graphical abstract"""

    #This function is called like this in parse.py:
    #title, date, authors, abstract, graphical_abstract = hosts.getData(journal, entry)

    #List of the journals
    rsc = [
           "RSC - New J. Chem. latest articles",
           "RSC - Chem. Sci. latest articles"
          ]

    #Dictionnary journal/journal abbreviation
    rsc_abb = {
               "RSC - New J. Chem. latest articles": "New J. Chem.",
               "RSC - Chem. Sci. latest articles": "Chem. Sci."
              }


    #If the journal is edited by the RSC
    if journal in rsc:

        title = entry.title
        date = arrow.get(entry.updated).format('YYYY-MM-DD')
        journal_abb = rsc_abb[journal]
        url = entry.feedburner_origlink

        abstract = None
        graphical_abstract = None

        soup = BeautifulSoup(entry.summary)

        r = soup.find_all("div")

        doi = getDoi(journal, entry)

        author = None

        graphical_abstract = r[0].img
        if graphical_abstract is not None:
            graphical_abstract = r[0].img['src']
            response, graphical_abstract = downloadPic(graphical_abstract)

        else:
            graphical_abstract = "Empty"

        try:
            #Dl of the article website page
            #page = requests.get(entry.feedburner_origlink, timeout=20)
            page = requests.get(url, timeout=20)

            #If the dl went wrong, print an error
            if page.status_code is not requests.codes.ok:
                print("{0}, bad return code: {1}".format(journal_abb, page.status_code))

            #Get the abstract
            soup = BeautifulSoup(page.text)
            r = soup.find_all("meta", attrs={"name": "citation_abstract"})
            if r:
                abstract = r[0]['content']

            r = soup.find_all("meta", attrs={"name": "citation_author"})
            if r:
                author = [ tag['content'] for tag in r ]
                author = ",".join(author)

        except requests.exceptions.Timeout:
            print("getData, {0}, timeout".format(journal_abb))
        except Exception as e:
            print("encore")
            print(e)


    if journal == "Angewandte Chemie International Edition":

        journal_abb = "Angew. Chem. Int. Ed. Engl."
        title = entry.title
        date = arrow.get(entry.updated).format('YYYY-MM-DD')

        author = entry.author.split(", ")
        author = ",".join(author)

        url = entry.prism_url

        graphical_abstract = None

        abstract = None

        soup = BeautifulSoup(entry.summary)
        r = soup.find_all("a", attrs={"class": "figZoom"})

        if r:
            response, graphical_abstract = downloadPic(r[0]['href'])
            r[0].replaceWith("")
            abstract = soup.renderContents().decode()


    if journal == "Journal of the American Chemical Society: Latest Articles (ACS Publications)":

        journal_abb = "J. Am. Chem. Soc."
        title = entry.title.replace("\n", " ")
        abstract = None
        date = arrow.get(entry.updated).format('YYYY-MM-DD')

        author = entry.author.split(" and ")
        author = author[0] + ", " + author[1]
        author = author.split(", ")
        author = ",".join(author)

        url = entry.feedburner_origlink

        graphical_abstract = None

        try:
            #Dl of the article website page
            page = requests.get(url, timeout=20)

            #If the dl went wrong, print an error
            if page.status_code is not requests.codes.ok:
                print("getData, JACS, bad return code: {0}".format(page.status_code))

            #Get the abstract
            soup = BeautifulSoup(page.text)
            r = soup.find_all("p", attrs={"class": "articleBody_abstractText"})
            if r:
                abstract = r[0].text

        except requests.exceptions.Timeout:
            print("getData, JACS, timeout")
        except Exception as e:
            print("encore")
            print(e)

        soup = BeautifulSoup(entry.summary)
        r = soup.find_all("img", alt="TOC Graphic")
        if r:
            response, graphical_abstract = downloadPic(r[0]['src'])

    return title, journal_abb, date, author, abstract, graphical_abstract, url


def getDoi(journal, entry):

    """Get the DOI number of a post, to save time"""

    rsc = [
           "RSC - New J. Chem. latest articles",
           "RSC - Chem. Sci. latest articles"
          ]

    if journal in rsc:
        soup = BeautifulSoup(entry.summary)
        r = soup.find_all("div")
        try:
            doi = r[0].text.split("DOI: ")[1].split(",")[0]
        except IndexError:
            doi = r[1].text.split("DOI:")[1].split(",")[0]

    if journal == "Angewandte Chemie International Edition":
        doi = entry.prism_doi

    if journal == "Journal of the American Chemical Society: Latest Articles (ACS Publications)":
        doi = entry.id.split("dx.doi.org/")[1]

    return doi


def downloadPic(url):

    """The parameter is a list. The function will be able to evolve"""

    #On essaie de récupérer chaque page correspondant
    #à chaque url, ac un timeout
    try:
        #On utilise un user-agent de browser,
        #ds le cas où les hébergeurs bloquent les bots
        headers = {'User-agent': 'Mozilla/5.0'}

        #On rajoute l'url de base comme referer,
        #car certains sites bloquent l'accès direct aux images
        headers["Referer"]= url

        page = requests.get(url, timeout=20, headers=headers)

        #Si la page a bien été récupérée
        if page.status_code == requests.codes.ok:

            path = "./graphical_abstracts/"

            #On enregistre la page
            with iopen(path + batbelt.simpleChar(url), 'wb') as file:
                file.write(page.content)
                #l.debug("image ok")

                #On sort True si on matche une des possibilités
                #de l'url
                return True, batbelt.simpleChar(url)

        elif page.status_code != requests.codes.ok:
            print("Bad return code: {0}".format(page.status_code))
            return "wrongPage", None

    except requests.exceptions.Timeout:
        print("downloadPic, timeout")
        return "timeOut", None
    except Exception as e:
        print("toujours")
        print(e)



if __name__ == "__main__":

    #urls_test = ["ang.xml",
                 #"jacs.xml"
                #]
    #urls_test = ["jacs.xml"]
    #urls_test = ["http://feeds.rsc.org/rss/nj"]
    #urls_test = ["njc.xml"]
    urls_test = ["http://feeds.rsc.org/rss/sc"]

    for site in urls_test:

        feed = feedparser.parse(site)

        #print(feed)

        #Name of the journal
        journal = feed['feed']['title'] 

        print(journal)

        for entry in feed.entries:
            getData(journal, entry)
            #break

        print("\n\n")

