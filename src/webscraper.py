from bs4 import BeautifulSoup
import requests


"""
* Return all headlines from fox
"""
def get_fox_headlines() -> list:
    urlFox = "https://www.foxnews.com"
    htmlFox = requests.get(urlFox).text
    headlinesParser = BeautifulSoup(htmlFox, 'html5lib')
    articleMarker = ['title', 'title-color-default']
    return [headline.findChildren('a')[0].string for headline in headlinesParser.find_all('h2') if headline['class'] == articleMarker]

"""
* Return all headlines from MSNBC
"""
def get_MSNBC_headlines() -> list:
    urlMSNBC = "https://www.msnbc.com"
    htmlMSNBC = requests.get(urlMSNBC).text
    headlinesParser = BeautifulSoup(htmlMSNBC, 'html5lib')
    spanMarker = "tease-card__headline"
    headlines = [headline.text for headline in headlinesParser.find_all('span', class_=spanMarker)]
    h3Marker = "related-content__headline"
    headlines.extend(
        [headline.findChildren('a')[0].text for headline in headlinesParser.find_all('h3', class_=h3Marker)])
    h2Marker = "a-la-carte__headline"
    headlines.extend([headline.text for headline in headlinesParser.find_all('h2', class_=h2Marker)])

"""
* Return all headlines from ABC
"""
def get_ABC_headlines() -> list:
    urlABC = "https://abcnews.go.com"
    htmlABC = requests.get(urlABC).text
    headlinesParser = BeautifulSoup(htmlABC, 'html5lib')
    allHeadlines = [headline.findChildren('h1')[0].findChildren('a')[0].string for headline in
                    headlinesParser.find_all('div', class_="headlines-li-div")]
    allHeadlines.extend([headline.findChildren('a')[0].string.strip() for headline in
                         headlinesParser.find_all('div', class_="caption-wrapper")])
    return allHeadlines

