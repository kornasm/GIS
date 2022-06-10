# script listing all players in fbref.com and saving it to file

from lxml import html
import lxml, lxml.html
import requests
from collections import Counter
import csv
from os.path import exists
import time
import sys

# function printing additional info about request
def my_http_get(url):
    print('')
    start = time.time()
    print('REQUEST  ' + url)
    result = requests.get(url)
    elapsed = time.time() - start
    print('request time  ' + str(elapsed))
    print('status code   ' + str(result.status_code))
    return result

baseurl = 'https://fbref.com'
localurl = 'http://0.0.0.0:8000'

if len(sys.argv) <= 1:
    print('Run this script with link to current season of a league you want to scrape')
    print('eg: python3 https://fbref.com/en/comps/36/schedule/Ekstraklasa-Scores-and-Fixtures')
    quit()
else:
    currenturl = sys.argv[1]
    splittedUrl = sys.argv[1].split('/')
    leagueName = splittedUrl[7]
    leagueName = leagueName.split('-')
    leagueName = leagueName[0]
    filename = leagueName + 'Edges'

#currenturl = baseurl + '/en/comps/36/schedule/Ekstraklasa-Scores-and-Fixtures'

#https://fbref.com/en/comps/36/10747/schedule/2020-2021-Ekstraklasa-Scores-and-Fixtures

filename = 'edges'

if exists(filename) == False:
    with open(filename , 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['id1', 'id2']) 

prevseasonexist = True

while prevseasonexist == True:
    print('loop iteration')
    #page = requests.get(currenturl + '/SeasonOverview.html')
    page = my_http_get(currenturl)
    tree = html.fromstring(page.content)
    #print(type(tree))
    # get links to all matches
    #terms = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div/div/div/table/tbody/')
    #print(terms)
    #teams = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div/div/div/table/tbody/tr/td[@class="left "]/a/@href')
    #print(teams)

    matches = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div/div//table/tbody/tr/td[@data-stat="match_report"]/a/@href')

    matches = [item for item in matches if 'matches' in item] # delete records with matches that has not yet taken place

    print('no matches  ' + str(len(matches)))
    #print(*matches, sep="\n")
    if len(matches) == 0:
        break

    for match in matches:
        matchurl = baseurl + match
        print(matchurl)
        time.sleep(5)
        matchdetails = requests.get(matchurl)
        matchdetails = my_http_get(matchurl)
        matchhtml = html.fromstring(matchdetails.content)

        teams = matchhtml.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@class="table_wrapper tabbed"]')
        playersid1 = teams[0].xpath('div/table/tbody/tr/th/@data-append-csv')
        playersid2 = teams[1].xpath('div/table/tbody/tr/th/@data-append-csv')
        print(playersid1)
        print(playersid2)

        with open(filename , 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['# ' + str(matchurl)])

            for i in range(len(playersid1)):
                for j in range(i + 1, len(playersid1)):
                    #print(str(i) + '  ' + str(j))
                    csvwriter.writerow([playersid1[i], playersid1[j]])
            
            for i in range(len(playersid2)):
                for j in range(i + 1, len(playersid2)):
                    #print(str(i) + '  ' + str(j))
                    csvwriter.writerow([playersid2[i], playersid2[j]])

    # save info to file about parsed season
    with open('seasonsParsed', 'a') as file:
        file.write(currenturl)

    # get link to previous season
    prevseason = tree.xpath('/html/body/div[@id="wrap"]/div[@id="info"]/div[@id="meta"]/div/div[@class="prevnext"]/a[@class="button2 prev"]/@href')

    if len(prevseason) == 0:
        prevseasonexist = False
    else:

        print('prev season:', end='  ')
    


    prevseasonurl = str(prevseason[0])
    currenturl = baseurl + prevseasonurl
    print(currenturl)
    print('')

    time.sleep(5)




