#!/usr/bin/python
# coding: utf-8


"""
Test module to be ran with pytest.
Tests that hosts.py returns correct values

Start the tests with something like this:
py.test -xs test_hosts.py -k getData
"""


import os
import feedparser
import requests
import pytest
import random
import datetime
from bs4 import BeautifulSoup
import hashlib
import arrow

import hosts

LENGTH_SAMPLE = 1


def test_getJournals():

    """Function to get the informations about all the journals of
    a company. Returns the names, the URLs, the abbreviations, and also
    a boolean to set the download of the graphical abstracts"""

    print("\n")
    print("Starting test getJournals")

    rsc = hosts.getJournals("rsc")
    acs = hosts.getJournals("acs")
    wiley = hosts.getJournals("wiley")
    npg = hosts.getJournals("npg")
    science = hosts.getJournals("science")
    nas = hosts.getJournals("nas")
    elsevier = hosts.getJournals("elsevier")
    thieme = hosts.getJournals("thieme")
    beil = hosts.getJournals("beilstein")
    npg2 = hosts.getJournals("npg2")

    # TODO: tester le type de chaque variable ds le tuple
    assert type(rsc) == tuple
    assert type(acs) == tuple
    assert type(wiley) == tuple
    assert type(npg) == tuple
    assert type(science) == tuple
    assert type(nas) == tuple
    assert type(elsevier) == tuple
    assert type(thieme) == tuple
    assert type(beil) == tuple
    assert type(npg2) == tuple

    total = rsc + acs + wiley + npg + science + nas + elsevier + thieme + beil + npg2

    for publisher in total:
        for chain in publisher:
            assert type(chain) == str


@pytest.fixture()
def journalsUrls():

    """Returns a combined list of urls.
    All the journals of all the companies.
    Specific to the tests, fixture"""

    rsc_urls = hosts.getJournals("rsc")[2]
    acs_urls = hosts.getJournals("acs")[2]
    wiley_urls = hosts.getJournals("wiley")[2]
    npg_urls = hosts.getJournals("npg")[2]
    science_urls = hosts.getJournals("science")[2]
    nas_urls = hosts.getJournals("nas")[2]
    elsevier_urls = hosts.getJournals("elsevier")[2]
    thieme_urls = hosts.getJournals("thieme")[2]
    beil_urls = hosts.getJournals("beilstein")[2]
    npg2_urls = hosts.getJournals("npg2")[2]

    urls = rsc_urls + acs_urls + wiley_urls + npg_urls + science_urls + \
           nas_urls + elsevier_urls + thieme_urls + beil_urls + npg2_urls

    return urls


def test_getData(journalsUrls):

    """Tests the function getData. For each journal of each company,
    tests LENGTH_SAMPLE entries"""

    print("\n")
    print("Starting test getData")

    # Returns a list of the urls of the feed pages
    list_urls_feed = journalsUrls

    # Get the names of the journals, per company
    rsc = hosts.getJournals("rsc")[0]
    acs = hosts.getJournals("acs")[0]
    wiley = hosts.getJournals("wiley")[0]
    npg = hosts.getJournals("npg")[0]
    science = hosts.getJournals("science")[0]
    nas = hosts.getJournals("nas")[0]
    elsevier = hosts.getJournals("elsevier")[0]
    thieme = hosts.getJournals("thieme")[0]
    beil = hosts.getJournals("beilstein")[0]
    npg2 = hosts.getJournals("npg2")[0]

    # # Bypass all companies but one
    # list_urls_feed = hosts.getJournals("rsc")[2]

    # All the journals are tested
    for site in list_urls_feed:

        print("Site {} of {}".format(list_urls_feed.index(site) + 1,
                                     len(list_urls_feed)))

        feed = feedparser.parse(site)
        journal = feed['feed']['title']

        if journal in rsc:
            company = 'rsc'
        elif journal in acs:
            company = 'acs'
        elif journal in wiley:
            company = 'wiley'
        elif journal in npg:
            company = 'npg'
        elif journal in science:
            company = 'science'
        elif journal in nas:
            company = 'nas'
        elif journal in elsevier:
            company = 'elsevier'
        elif journal in thieme:
            company = 'thieme'
        elif journal in beil:
            company = 'beilstein'
        elif journal in npg2:
            company = 'npg2'


        print("\n")
        print(journal)

        if len(feed.entries) < LENGTH_SAMPLE:
            samples = feed.entries
        else:
            samples = random.sample(feed.entries, LENGTH_SAMPLE)

        # Tests LENGTH_SAMPLE entries for a journal, not all of them
        for entry in samples:

            if journal in science + elsevier + beil:
                title, date, authors, abstract, graphical_abstract, url, topic_simple = hosts.getData(company, journal, entry)
            else:
                url = getattr(entry, 'feedburner_origlink', entry.link)

                try:
                    response = requests.get(url, timeout=10)
                    title, date, authors, abstract, graphical_abstract, url, topic_simple = hosts.getData(company, journal, entry, response)
                except requests.exceptions.ReadTimeout:
                    print("A ReadTimeout occured, continue to next entry")

            print(title)
            print(url)
            print(graphical_abstract)
            print(date)
            print("\n")

            # TODO: faire des tests plus poussés sur ces variables
            # tester par ex si graphical_abstract est une url valide
            # tester si abstract n'est pas vide
            # tester si author n'est pas vide
            assert type(abstract) == str
            assert type(url) == str
            assert type(graphical_abstract) == str
            assert type(arrow.get(date)) == arrow.arrow.Arrow


def test_getDoi(journalsUrls):

    """Tests if the function getDoi gets the DOI correctly"""

    print("\n")
    print("Starting test getDoi")

    rsc = hosts.getJournals("rsc")[0]
    acs = hosts.getJournals("acs")[0]
    wiley = hosts.getJournals("wiley")[0]
    npg = hosts.getJournals("npg")[0]
    science = hosts.getJournals("science")[0]
    nas = hosts.getJournals("nas")[0]
    elsevier = hosts.getJournals("elsevier")[0]
    thieme = hosts.getJournals("thieme")[0]
    beil = hosts.getJournals("beilstein")[0]
    npg2 = hosts.getJournals("npg2")[0]

    list_sites = journalsUrls

    for site in list_sites:
        feed = feedparser.parse(site)
        journal = feed['feed']['title']

        if journal in rsc:
            company = 'rsc'
        elif journal in acs:
            company = 'acs'
        elif journal in wiley:
            company = 'wiley'
        elif journal in npg:
            company = 'npg'
        elif journal in science:
            company = 'science'
        elif journal in nas:
            company = 'nas'
        elif journal in elsevier:
            company = 'elsevier'
        elif journal in thieme:
            company = 'thieme'
        elif journal in beil:
            company = 'beilstein'
        elif journal in npg2:
            company = 'npg2'

        print("{}: {}".format(site, len(feed.entries)))

        if len(feed.entries) < LENGTH_SAMPLE:
            samples = feed.entries
        else:
            samples = random.sample(feed.entries, LENGTH_SAMPLE)

        # Tests 3 entries for a journal, not all of them
        # for entry in random.sample(feed.entries, 3):
        for entry in samples:

            doi = hosts.getDoi(company, journal, entry)
            print(doi)

            assert type(doi) == str


def test_dlRssPages(journalsUrls):

    """Dl all the RSS pages  of the journals, and store them
    in directories named after the journal. I'll run comparisons
    on the pages to determine the refresh rate of each journal"""

    print("\n")
    print("Starting test dlRssPages")

    # Returns a list of the urls of the feed pages
    list_sites = journalsUrls

    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
               'Connection': 'close'}

    print(list_sites)

    for url_feed in list_sites:

        print("Site {} of {}".format(list_sites.index(url_feed) + 1, len(list_sites)))
        feed = feedparser.parse(url_feed)

        try:
            journal = feed['feed']['title']
        except KeyError:
            print("Abort for {}".format(url_feed))

        # Get the RSS page and store it. I'll run some comparisons on them
        content = requests.get(url_feed, timeout=120, headers=headers, verify=False)
        if content.status_code is requests.codes.ok:
            soup = BeautifulSoup(content.text)

            filename = "./debug_journals/" + str(journal) + "/" + str(datetime.datetime.today().date())
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w') as file:
                for line in soup.prettify():
                    file.write(line)
        else:
            print("Dl of {} not OK: {}".format(journal, content.status_code))


def test_analyzeRssPages():

    """Tests all the RSS pages stored in debug_journals.
    For each journal, print the date when the RSS page changed"""

    for directory in os.walk("./debug_journals/"):

        print(directory[0])

        list_dates = []
        list_md5 = []

        for fichier in directory[2]:

            # Read each file and generate a md5 sum
            with open(directory[0] + "/" + fichier, 'rb') as file:
                m = hashlib.md5(file.read()).hexdigest()

            if m not in list_md5:
                list_md5.append(m)
                list_dates.append(fichier)

        print(sorted(list_dates))
