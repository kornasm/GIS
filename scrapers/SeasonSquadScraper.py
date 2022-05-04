from lxml import html
import lxml, lxml.html
import requests
import csv
from os.path import exists
import time
import sys

# function printing additional info about request
def my_http_get(url):
    print('')
    print('REQUEST  ' + url)
    time.sleep(3) # added to avoid being blocked by fbref server
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
localurl = 'http://0.0.0.0:8000'
currenturl = ''
filename = ''
minimum_matches = 0

if len(sys.argv) <= 1:
    print('Run this script with link to current season league table of a league you want to scrape')
    print('e.g. python3 matchesScraper.py https://fbref.com/en/comps/36/Ekstraklasa-Stats')
    quit()
else:
    currenturl = sys.argv[1]
    splittedUrl = sys.argv[1].split('/')
    leagueName = splittedUrl[-1]
    filename = leagueName + 'Edges.csv'
    if len(sys.argv) >= 3:
        minimum_matches = int(sys.argv[2])

if exists(filename) == False:
    with open(filename , 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['id1', 'id2'])

prevseasonexist = True

while prevseasonexist == True:
    page = my_http_get(currenturl)
    tree = html.fromstring(page.content)

    #teams = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div/div//table/tbody/tr/td[@data-stat="match_report"]/a/@href')
    teams = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div/div/div/table/tbody/tr/td[@class="left "]/a/@href')
    #mat = [item for item in matches if 'matches' in item] # delete records with matches that has not yet taken place
    print(*teams, sep="\n")
    print('no teams  ' + str(len(teams)))

    for team in teams:
        teamurl = baseurl + team
        matchdetails = my_http_get(teamurl)
        teamhtml = html.fromstring(matchdetails.content)

        playersid = teamhtml.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@id="all_stats_standard"]/div/table/tbody/tr/th[@class="left "]/@data-append-csv')
        players_matches = teamhtml.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@id="all_stats_standard"]/div/table/tbody/tr/td[@data-stat="games"]/text()')

        players_matches = [int(item) for item in players_matches]
        players = list(zip(playersid, players_matches))
        players = [item for item in players if item[1] > minimum_matches]
        players = [item[0] for item in players]

        with open(filename , 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['# ' + str(teamurl)])

            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                        csvwriter.writerow([players[i], players[j]])

    # log info to file about scraped season
    with open('seasonSquadsParsed', 'a') as file:
        file.write(currenturl)

    if len(teams) == 0:
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