
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file", type = argparse.FileType('r', encoding='utf-8-sig'))
args = parser.parse_args()
fullString = args.file.readlines()


subString = "====="
coordStart = []
coordEnd = []

for text in fullString:
    if "=====" in text:
        fullString.insert(0,text)
        break

for i,text in enumerate(fullString):
    if "\n" == text:
        fullString.pop(i)

for i,x in enumerate(fullString):
    if subString in x:
        coordStart.append(i)

coordStart.pop(len(coordStart)-1)

for x in coordStart:
    coordEnd.append(x+4)

coords = tuple(zip(coordStart, coordEnd))
collection = dict([])
bookname = []

for pair in coords:

    start = pair[0]
    end = pair[1]
    
    note = fullString[start+1:end]
    bookname.append(note[0])
    
bookname = set(bookname)

goodUnicode = []
badUnicode = []

for entry in bookname:
    if "\ufeff" in entry:
        badUnicode.append(entry)
    else:
        goodUnicode.append(entry)

correction = []
error = []

badUnicode = set(badUnicode)
goodUnicode = set(goodUnicode)

for correctName in goodUnicode:
    for badName in badUnicode:
        if correctName in badName:
            correction.append(correctName)
            error.append(badName)

collection = []

for pair in coords:

    start = pair[0]
    end = pair[1]
    
    note = fullString[start+1:end]

    for content in note:
        title = note[0]

        if title in error:
            index = error.index(title)
            note[0] = correction[index]

    seperator = ', '
    text = seperator.join(note[1:3])
    text = text.replace("\n","")
    title = note[0]

    title = title[0:-2]
    title = title.replace(" ","").replace("\ufeff","").replace(".","_")
   

    joint = (title,text)

    collection.append(joint)

final = {}


for item in collection:
    final[item[0]]=[]
   
    
for key in final:
    notelist = []
    for item in collection:
        if key == item[0]:
            notelist.append(item)
    final[key].append(notelist)
    


print(final.keys())

for key in final:
    firstterm = key
    firstterm = firstterm+'.txt'
    output = json.dumps(final[key], indent=0, sort_keys=True)
    output = output.replace("[","").replace("]","")
    print(firstterm)
    f = open(firstterm, 'w')
    f.write(output)
	
