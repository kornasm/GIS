# script listing all players in fbref.com and saving it to file

from lxml import html
import requests
import csv
import time

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

baseurl = 'https://fbref.com/en/players/'

a = 97
z = 123
filename = 'Players.csv'

with open(filename , 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['id', 'name'])        

for firstletter in range(a, z):
    char1 = chr(firstletter)
    for secondletter in range(a, z):
        char2 = chr(secondletter)
        print(char1 + char2)
        url = baseurl + char1 + char2 + '/'
        page = my_http_get(url)
        tree = html.fromstring(page.content)

        playerids = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@class="section_wrapper"]/div[@class="section_content"]/p/a//@href') # id
        playernames = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@class="section_wrapper"]/div[@class="section_content"]/p/a//text()') # name

        if(len(playerids) > 0):
            playernames.pop(-1) # empty record with the same path
            playerids.pop(-1)

        for i in range(0,len(playerids)):
            playerlink = str(playerids[i]).split('/')
            playerids[i] = playerlink[3]

        players = list(zip(playerids, playernames))

        with open(filename , 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(players)

        print('no players  ' + str(len(playerids)))
        print('')