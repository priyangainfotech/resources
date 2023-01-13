#!/usr/bin/env python3

import sys
from json import dumps
import json
import os
from pathlib import Path



currPath = str(Path.cwd())

summary = []

def isAvailable(book):
    for idx, preBook in enumerate(summary):
        if preBook['title'] == book['title']:
            print("Found Duplication: "+ book['title'])
            return idx, preBook
    return None

def writeJson(path, content):
    out_file = open(path, "w")
    out_file.write(dumps(content))
    out_file.close()

def readJson(path):
    if  os.path.isfile(path):
        with open (path , 'r') as f:
            return json.load(f)
    

def updateBooks(stallInfo, eventInfo):
    #print(stallInfo)
    book_file = stallInfo['books_list']
    if book_file is not None:
        books = readJson(currPath+"/"+book_file)
        if books is not None:
            for book in books:
                stalls = []
                existBookWithIndex = isAvailable(book=book)
                if  existBookWithIndex is None:
                    stalls.append(stallInfo)
                    book.update({"stalls": stalls})
                    summary.append(book)
                else:
                    prevBook = existBookWithIndex[1]
                    stalls = stalls+prevBook['stalls']
                    stalls.append(stallInfo)
                    prevBook['stalls'] = stalls
                    summary[existBookWithIndex[0]] = prevBook 

    

def loadFairDetail(fairInfo):
    print("Processing the fair file")
    stall_file = fairInfo['book_list']
    if  stall_file is not None:
        stalls = readJson(currPath+"/"+stall_file)
        if stalls is not None:
            for stall in stalls:
                updateBooks( stallInfo=stall, eventInfo=fairInfo)




def loadEvents():
    with os.scandir(currPath) as it:
        for entry in it:
            if entry.name.endswith(".json") and entry.is_file():
                #print(entry.name, entry.path)
                events = readJson(entry.path)['events']
                for event in events:
                    print("********** START *********")
                    loadFairDetail(event)
                    print("********* END **********")
                    


loadEvents()
writeJson("wholeBooks.json", summary)