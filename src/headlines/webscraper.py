from bs4 import BeautifulSoup
from typing import List
import requests
# CODE MUST BE RUN FROM USA OR AMERICAN VPN SO PROPER HTML WILL BE OBTAINED BY REQUESTS


def get_full_name(last_name):
    """
    * gets full name of person from just their last name using Google and Wikipedia
    * Search must be launched from American Network/VPN or results will not be able to be parsed properly
    * will be used to tag ArticleHeadline objects with their proper names if their names are not currently in database
    * very slow function call, so will be avoided as much as possible by storing results in database with list of famous people
    """
    searchURL = f"https://www.google.com/search?q={last_name}"
    html = requests.get(searchURL).text
    name_parser = BeautifulSoup(html, 'html5lib')
    possible_hits = name_parser.find_all('div', class_="BNeawe UPmit AP7Wnd")
    for hit in possible_hits:
        if hit.text.startswith("https://en.wikipedia.org › wiki ›"):
            return hit.text.split("›")[-1].replace("_", " ")
    raise RuntimeError("No name was found")


def get_FOX_headlines() -> List[str]:
    """ :return all headlines from fox"""
    url_fox = "https://www.foxnews.com"
    html_fox = requests.get(url_fox).text
    headlines_parser = BeautifulSoup(html_fox, 'html5lib')
    article_marker = ['title', 'title-color-default']
    return [headline.find_children('a')[0].string.strip() for headline in headlines_parser.find_all('h2') if headline['class'] in article_marker]


def get_MSNBC_headlines() -> List[str]:
    """ :return all headlines from MSNBC"""
    urlMSNBC = "https://www.msnbc.com"
    htmlMSNBC = requests.get(urlMSNBC).text
    headlines_parser = BeautifulSoup(htmlMSNBC, 'html5lib')
    spanMarker = "tease-card__headline"
    headlines = [headline.text.strip() for headline in headlines_parser.find_all('span', class_=spanMarker)]
    h3Marker = "related-content__headline"
    headlines.extend(
        [headline.find_children('a')[0].text.strip() for headline in headlines_parser.find_all('h3') if headline['class'] == h3Marker])
    h2Marker = "a-la-carte__headline"
    headlines.extend([headline.text.strip() for headline in headlines_parser.find_all('h2', class_=h2Marker)])
    return headlines


def get_ABC_headlines() -> List[str]:
    """ :return all headlines from ABC"""
    urlABC = "https://abcnews.go.com"
    htmlABC = requests.get(urlABC).text
    headlines_parser = BeautifulSoup(htmlABC, 'html5lib')
    first_marker = 'headlines-li-div'
    all_headlines = [headline.find_children('h1')[0].find_children('a')[0].string.strip() for headline in
                     headlines_parser.find_all('div') if has_class_marker(headline, first_marker)]
    second_marker = "caption-wrapper"
    all_headlines.extend([headline.find_children('a')[0].string.strip() for headline in
                         headlines_parser.find_all('div') if has_class_marker(headline, second_marker)])
    return all_headlines


def has_class_marker(headline, marker) -> bool:
    try:
        return headline['class'] == marker
    except KeyError:
        return False
