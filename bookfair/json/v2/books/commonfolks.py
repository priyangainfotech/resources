#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import requests
from json import dumps

url= sys.argv[1]
json_file = sys.argv[2]


books = []

def readAtt(soupInst, tag, className, child):
    instant = soupInst.find(tag, className)
    if instant is not None:
       return instant.find(child, recursive=False).text
    return None

def readUrl(endPoint):
    page = requests.get(endPoint)
    print("******** Parsing************")
    print(endPoint)
    soup = BeautifulSoup(page.content, 'html.parser')
    itemDivs = soup.find_all("div", {"class": "item"})

    for tag in itemDivs:
        children = tag.findChildren()
        book = {}
        for child in children:
            attr = child.attrs
            if child.name == 'div' and 'data-src' in attr:
                book.update ({"images":[attr['data-src']] })
            if child.name == "a":
                book.update ({'url': attr['href'] })
                book.update ({'title':child.text})

            if child.name == 'font':
                if('class' in attr and 'price' in attr['class']):
                    book.update ({'price':child.text})
            
        if len(book) != 0:
            print(book)
            detailPage = requests.get(book['url'])
            detalSoup = BeautifulSoup(detailPage.content, 'html.parser')
            author = readAtt(detalSoup, "h6", {"class": "author"}, 'a')
            if author is not None:
                 book.update({'author':author})

            language = detalSoup.find("h6", {"class": "language"}).find("a", recursive=False)
            book.update({'language':language.text})
            
            publishedon = detalSoup.find("h6", {"class": "publishedon"}).find("a", recursive=False)

            book.update({'publishedon':publishedon.text})
            
            isbn = detalSoup.find("h6", {"class": "isbn"})
            if isbn is not None:
                book.update({'isbn':isbn.text})

            books.append(book)

    #Go to next page
    #page by option
    pages = soup.find("span", {"class": "pageby"}).findAll("a", recursive=False)
    for page in pages:
        pageChild = page.findChildren()
        for child in pageChild:
            if child.name == 'font' and 'nextpage' in child.attrs['class']:
                nextPage = page.attrs['href']
                print("======= Navigating to next page ==============")
                readUrl(nextPage)
                break

    print(books)

readUrl(url)

out_file  = open (json_file, "w")
out_file.write(dumps(books))
out_file.close()