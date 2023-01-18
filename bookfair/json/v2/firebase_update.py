#!/usr/bin/env python3

import sys
from json import dumps
import json
import os
from pathlib import Path


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials.
cred = credentials.Certificate("../cred.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firebase has been connected")



currPath = str(Path.cwd())

summary = []

def writeJson(path, content):
    out_file = open(path, "w")
    out_file.write(dumps(content))
    out_file.close()

def readJson(path):
    if  os.path.isfile(path):
        with open (path , 'r') as f:
            return json.load(f)
    

def updateBooks(stallInfo, fairInfo):
    #print(stallInfo)
    book_file = stallInfo['books_list']
    if book_file is not None:
        books = readJson(currPath+"/"+book_file)
        if books is not None:
            for book in books:
                detail = {}
                detail.update ({"book":book})
                detail.update({"stall":stallInfo})
                detail.update({"fair":fairInfo})
                summary.append(detail)

    


def loadFairDetail(fairInfo):
    print("Processing the fair file")
    stall_file = fairInfo['book_list']
    if  stall_file is not None:
        stalls = readJson(currPath+"/"+stall_file)
        if stalls is not None:
            for stall in stalls:
                updateBooks(stall, fairInfo)




def loadEvents():
    with os.scandir(currPath) as it:
        for entry in it:
            if entry.name.endswith(".json") and entry.is_file():
                #print(entry.name, entry.path)
                events = readJson(entry.path)['events']
                for event in events:
                    print("********** START *********")
                    addDocument("events", event)
                    loadFairDetail(event)
                    print("********* END **********")
                    

def addDocument(collectionName, collections):
    document = db.collection(collectionName).add(collections)
    print(document[1].id)
    return document[1].id


loadEvents()
writeJson("wholeBooks.json", summary)