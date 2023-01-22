#!/usr/bin/env python3

import sys
from json import dumps
import json
import os
from pathlib import Path


currPath = str(Path.cwd())

books = []

with os.scandir(currPath) as it:
    for entry in it:
        if entry.name.endswith(".json") and entry.is_file():
            #print(entry.name, entry.path)
            with open(entry.name, 'r') as f:
                prevBooks = json.load(f)
                books = books+prevBooks


out_file  = open ("wholeBooks.json", "w")
out_file.write(dumps(books))
out_file.close()