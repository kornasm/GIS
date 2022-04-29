# script listing all players in fbref.com and saving it to file

from lxml import html
import lxml, lxml.html
import requests
import csv
import time

baseurl = 'https://fbref.com/en/players/'

a = 97
z = 123
filename = 'players'

with open(filename , 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['id', 'name'])        

for firstletter in range(a, z):
    char1 = chr(firstletter)
    for secondletter in range(a, z):
        char2 = chr(secondletter)
        print(char1 + char2)
        time.sleep(10) # added to avoid being blocked by fbref server
        url = baseurl + char1 + char2 + '/'

        page = requests.get(url)

        tree = html.fromstring(page.content)
        print('status code  ' + str(page.status_code))

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