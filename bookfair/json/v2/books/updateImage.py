#!/usr/bin/env python3
import sys
import json
from json import dumps
import requests
from pathlib import Path
import os


from openpyxl import load_workbook
json_file= sys.argv[1]
folder = sys.argv[2]

books = []
with open(json_file, 'r') as f:
  books = json.load(f)


for book in books:
  if book['images'] is not None:
    updatedImages  = []
    for img in book['images']:
      res = img.split('/')
      last = folder+res[len(res)-1]
      updatedImages.append(last)
      #Download image
      path = str(Path.cwd())+"/"+last

      if not os.path.isfile(path):
        img_data = requests.get(img).content
        with open(path, 'wb') as handler:
          handler.write(img_data)

    book['images'] = updatedImages

  print(books)
  # convert into json
json_data = dumps(books)
print(json_data)


out_file  = open (json_file, "w")
out_file.write(json_data)
out_file.close()



