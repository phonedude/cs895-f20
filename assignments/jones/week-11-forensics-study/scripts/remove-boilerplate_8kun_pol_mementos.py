import sys
import os
from bs4 import BeautifulSoup

inputdir = sys.argv[1]

#inputfile = sys.argv[1]

for inputfile in os.listdir(inputdir):

    if inputfile[-5:] != '.html':
        print("skipping {} because it is not html".format(inputfile))
        continue

    outputfile = inputfile + '.noboilerplate.txt'
    
    if os.path.exists(outputfile):
        print("skipping {} because it already exists".format(inputfile))
        continue
    
    with open(inputdir + '/' + inputfile) as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html5lib')
    
    text = soup.get_text(" ", strip=True)
    
    with open(inputdir + '/' + outputfile, 'w') as f:
        f.write(text)
