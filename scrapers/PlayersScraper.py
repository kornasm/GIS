# script listing all players in fbref.com and saving it to file

from lxml import html
import lxml, lxml.html
import requests

baseurl = 'https://fbref.com/en/players/'

for firstletter in range(97, 123):
    char1 = chr(firstletter)
    for secondletter in range(97, 123):
        char2 = chr(secondletter)
        url = baseurl + char1 + char2 + '/'
        page = requests.get(url)
        tree = html.fromstring(page.content)

        players = tree.xpath('/html/body/div[@id="wrap"]/div[@id="content"]/div[@class="section_wrapper"]/div[@class="section_content"]/p/a/@href')
        players.pop(-1) # empty record with the same path

        with open('players' , 'w') as file:
            for player in players:
                file.write(player)
                file.write("\n")