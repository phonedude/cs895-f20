import sys
from bs4 import BeautifulSoup
import re
import json
import os

inputdir = sys.argv[1]
outputdir = sys.argv[2]
failfile = "failfile.txt"

html_files = []

for filename in os.listdir(inputdir):

    if '.html' in filename:
        html_files.append(filename)

#html_files = [
#    "2015-04-21T16:38:12Z.html"
#]
        
for inputhtml in html_files:
    # inputhtml = sys.argv[1]

    print("working on file {}".format(inputhtml))

    if os.path.exists( outputdir + '/' + inputhtml + '.json' ):
        print("skipping already processed {}".format(inputhtml))
        continue

    if inputhtml[-5:] != '.html':
        continue

    with open(inputdir + '/' + inputhtml) as f:
        htmldata = f.read()
    
    all_data = []
    
    soup = BeautifulSoup(htmldata, 'html5lib')

    foundth = None
    headers = []

    for table in soup.find_all('table'):

        for th in table.find_all('th'):
            header = th.get_text()
            foundth = table

#            if header == 'ボード':
#                header = "Board"
#            elif header == 'ボードのタイトル':
#                header = "Title"
#            elif header == '１時間以内の投稿。':
#                header = "PPH"
#            elif header == "すべての投稿":
#                header = "Total Posts"
#            elif header == "ユニークIP":
#                header = "Unique IP"
#            elif header == "作成済み":
#                header = "Created"

            headers.append(header)

#    print("found headers: {}".format(headers))
    print("size of all_data: {}".format(len(all_data)))

    if foundth is not None:

        trs = foundth.find_all('tr')

#        print("found {} trs".format(len(trs)))

        for tr in trs:

            record_output = {}

#            print("tr: {}".format(tr))

            ths = tr.find_all('th')

            if len(ths) > 0:
                continue

            tds = tr.find_all('td')

            if len(tds) == 1:
                if tds[0].get_text().strip() == '':
                    continue
                else:
                    endphrase_found = []
                    for endphrase in [
                        "Displaying results",
                        "Click to load more."
                    ]:
                        if endphrase in tds[0].get_text().strip():
                            endphrase_found.append( True )
                            continue
                        else:
                            print("Failed to find end phrase")
                            print("td: {}".format(tds[0].get_text().strip()))
                            endphrase_found.append( False )

            if len(tds) != len(headers):

                if all(endphrase_found):
                    continue
                else:
                    print("found {} tds".format(len(tds)))
                    print("tr: {}".format(tr))
                    print("there are {} headers".format(len(headers)))
                    print("Failed to parse 8kun tables...")
                    with open(failfile, 'a') as f:
                        f.write(inputhtml + '\n')
                    #sys.exit(255)
        
            for i in range( 0, len(tds)):
                record_output[ headers[i] ] = tds[i].get_text()

            all_data.append(record_output) 

    if len(all_data) == 0:
        print("no records, failed to find any data for {}".format(inputhtml))
        with open(failfile, 'a') as f:
            f.write(inputhtml + '\n')
    
#    for tr in soup.find_all('tr'):
#
#        board_data = {}
#    
#        for td in tr.find_all('td'):
#        
#            for link in td.find_all('a'):
#        
#                linkurl = link['href']
#        
#                if "8ch.net/" in linkurl and "https://8ch.net/boards.html" not in linkurl:
#        
#                    if "boards.php?" in linkurl:
#                        tagname = re.sub("^.*://8ch.net/boards.php\?tags=(.*)$", "\\1", linkurl)
#                        board_data.setdefault('tags', []).append( tagname )
#                    else:
#                        board_name = re.sub("^.*://8ch.net/([^/]*)/", "\\1", linkurl) 
#                        board_data['board_name'] = board_name
#                        board_data["board_url"] = linkurl
#     
#        if board_data != {}:
#            #print("board data is now {}".format(board_data))
#            all_data.append( board_data )
       
    outputfilename = outputdir + '/' + os.path.basename(inputhtml) + '.json'
    print("saving data for {} boards".format(len(all_data)))
    print("output is at {}".format(outputfilename))

    with open(outputfilename, 'w') as g:
        json.dump(all_data, g, indent=4)
