from lxml import html
import requests
import csv
from os.path import exists
import time
import sys

# function printing additional info about request
def my_http_get(url):
    print('')
    print('REQUEST  ' + url)
    time.sleep(7) # added to avoid being blocked by fbref server
    start = time.time()
    result = requests.get(url)
    elapsed = time.time() - start
    print('request time  ' + str(elapsed))
    print('status code   ' + str(result.status_code))

    if(result.status_code != 200):
        print('last request failed')
        quit()
    return result

baseurl = 'https://fbref.com'
currenturl = ''
filename = ''

if len(sys.argv) <= 1:
    print('python3 matchesScraper.py [link to current season matches list of a scraped league]')
    print('e.g. python3 matchesScraper.py https://fbref.com/en/comps/36/schedule/Ekstraklasa-Scores-and-Fixtures')
    quit()
else:
    currenturl = sys.argv[1]
    splittedUrl = sys.argv[1].split('/')
    leagueName = splittedUrl[-1]
    filename = leagueName + 'Edges.csv'

if exists(filename) == False:
    with open(filename , 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['#id1', 'id2']) 

prevseasonexist = True

while prevseasonexist == True:
    page = my_http_get(currenturl)
    tree = html.fromstring(page.content)

    matches = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div/div//table/tbody/tr/td[@data-stat="match_report"]/a/@href')
    matches = [item for item in matches if 'matches' in item] # delete records with matches that has not yet taken place

    print('no matches  ' + str(len(matches)))

    for match in matches:
        matchurl = baseurl + match
        matchdetails = my_http_get(matchurl)
        matchhtml = html.fromstring(matchdetails.content)

        teams = matchhtml.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@class="table_wrapper tabbed"]')
        playersid1 = teams[0].xpath('div/table/tbody/tr/th/@data-append-csv')
        playersid2 = teams[1].xpath('div/table/tbody/tr/th/@data-append-csv')

        with open(filename , 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['# ' + str(matchurl)])

            for i in range(len(playersid1)):
                for j in range(i + 1, len(playersid1)):
                    csvwriter.writerow([playersid1[i], playersid1[j]])
            
            for i in range(len(playersid2)):
                for j in range(i + 1, len(playersid2)):
                    csvwriter.writerow([playersid2[i], playersid2[j]])

    # log info to file about scraped season
    with open('seasonsParsed', 'a') as file:
        file.write(currenturl)

    if len(matches) == 0:
        break # fbref haven't uploaded all the data yet.
              # if there is no data about this season, there probably won't be any data about the previous one either
              # if an internal server error occured it will be easy to figure out where to continue

    # get link to previous season
    prevseason = tree.xpath('/html/body/div[@id="wrap"]/div[@id="info"]/div[@id="meta"]/div/div[@class="prevnext"]/a[@class="button2 prev"]/@href')

    if len(prevseason) == 0:
        prevseasonexist = False

    prevseasonurl = str(prevseason[0])
    currenturl = baseurl + prevseasonurl
    print(currenturl)
    print('')