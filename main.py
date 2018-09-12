#! /usr/bin/python3

import re
from urllib import request, parse
import time
from bs4 import BeautifulSoup
import time
import datetime
import json
from discord_hooks import Webhook #Credit: https://github.com/kyb3r/dhooks

VERSION = 1.2
BLACKLIST_LOCATION = "/home/liam/application_data/atom/discord/alexandria/blacklist.txt"
WEBHOOK_URL_LIST_LOCAtion = "/home/liam/application_data/atom/discord/alexandria/webhooks.txt"

WEBHOOK_URL_LIST = []
f=open(WEBHOOK_URL_LIST_LOCATION,'r')
while True:
    line = f.readline()
    if not x: break
    WEBHOOK_URL_LIST.append(line)

def main():
    print("Script version ", VERSION ," started. The time is " + str(datetime.datetime.now()))
    successful_iterations = 0
    articles = 0
    iterations = 0
    failures = 0

    while(True):
        try:
            #Setup
            print("\nIteration: " , iterations)
            print("Iterations since last failure: " , successful_iterations)
            print("Total failures: ",failures)
            print("Articles posted since load: ",articles)
            print("");
            url = "https://www.minecraftforum.net"
            page = request.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')

            #description
            description_list = []
            for cup in soup.find_all('div', {'class':'post-excerpt-description'} ):
                description_list.append(cup.text.replace("\n",""))

            #url
            url_list = []
            for cup in soup.find_all('h2', {'class':'post-excerpt-title'} ):
                url_list.append(cup.find('a')['href'])

            #image
            image_list = []
            for cup in soup.find_all('a', {'class':'post-excerpt-link'} ):
                image_list.append(cup.find('img')['src'])

            #title
            title_list = []
            for cup in soup.find_all('h2', {'class':'post-excerpt-title'} ):
                title_list.append(cup.text.replace("\n",""))

            #Handle file interactions
            file = open(BLACKLIST_LOCATION,"r")
            saved_url_list = file.read()
            file.close()

            for i in range(len(url_list)):
                url = url_list[i]
                image = image_list[i]
                title = title_list[i].lstrip()
                description = description_list[i].lstrip()

                if url not in saved_url_list:
                    print("New article found!")

                    #Writing to file
                    titles = open(BLACKLIST_LOCATION,"a")
                    titles.write(url + "\n")
                    titles.close()

                    #Post
                    for i in range(len(WEBHOOK_URL_LIST)):
                        webhook_url = webhook_url[i]
                        embed = Webhook(webhook_url,color=0xff0000)

                        embed.set_author(name=title)
                        embed.set_desc(description)
                        embed.set_thumbnail(image)
                        embed.add_field(name='Link:',value='[' + title + '](' + url + ')')
                        embed.set_footer(ts=True)

                        embed.post()
                        time.sleep(1)
                    time.sleep(15)
            successful_iterations+=1
            time.sleep(300)
        except Exception as e:
            successful_iterations = 0
            failers+=1
            print("Exception! Retrying in in 10 minutes...")
            print(e)
            time.sleep(600)
        iterations+=1
main()
