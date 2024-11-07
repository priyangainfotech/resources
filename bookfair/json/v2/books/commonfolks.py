#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import requests
from json import dumps
from pathlib import Path
import os
import json

url= sys.argv[1]
json_file = sys.argv[2]


prevBooks = []
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        prevBooks = json.load(f)

books = []
jsonPath = Path(json_file).stem
folderPath = "/images/"+jsonPath
imageFolder = str(Path.cwd())+folderPath

isExist = os.path.exists(imageFolder)
if not isExist:
    os.makedirs(imageFolder)
    print("Created "+imageFolder)


def isAvailable(book):

    url = book['url']
    for pre in prevBooks:
        if pre['url'] == url:
            return True
        
    return False


def downloadImage(img):
    res = img.split('/')
    path = imageFolder+"/"+res[len(res)-1]
   
    if not os.path.isfile(path):
        img_data = requests.get(img).content
        with open(path, 'wb') as handler:
         handler.write(img_data)

    return "https://raw.githubusercontent.com/piappstudio/resources/main/bookfair/json/v2/books"+folderPath+"/"+res[len(res)-1]

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
                imgPath = downloadImage(attr['data-src'])
                book.update ({"images":[imgPath] })
                
            if child.name == "a":
                book.update ({'url': attr['href'] })
                book.update ({'title':child.text})

            if child.name == 'font':
                if('class' in attr and 'price' in attr['class']):
                    book.update ({'price':child.text})
            
        if isAvailable(book):
            print("********** Skip details page *************")
            break
        if len(book) != 0:
            print(book)
            detailPage = requests.get(book['url'])
            detalSoup = BeautifulSoup(detailPage.content, 'html.parser')
            author = readAtt(detalSoup, "h6", {"class": "author"}, 'a')
            if author is not None:
                 book.update({'author':author})

            language =  readAtt(detalSoup, "h6", {"class": "language"}, 'a')
            if language is not None:
                book.update({'language':language})
            
            
            publishedon = readAtt(detalSoup, "h6", {"class": "publishedon"}, 'a')
            if publishedon is not None:
                book.update({'publishedon':publishedon})
            
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

try:
    readUrl(url)
except Exception as e:
    print(e)
finally:
    out_file  = open (json_file, "w")
    out_file.write(dumps(books))
    out_file.close()