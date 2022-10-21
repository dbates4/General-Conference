# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:33:36 2020

Scrape gen con text. Each talk will be saved to its own file.

@author: dylan
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time
import random as rand
import unicodedata

df = pd.DataFrame()
save_path = 'C:/Users/dylan/Datasets/lds/genconftext/'
root = 'https://www.churchofjesuschrist.org'

#Make list of all conference sessions links ----------------------------------
conference_path = root + '/general-conference/conferences?lang=eng'
s_req = Request(conference_path, headers={'User-Agent': 'Mozilla/5.0'})
s_url = urlopen(s_req).read()
s_bs = BeautifulSoup(s_url, "lxml")
s_list = s_bs.find_all("a",{"class":"portrait-jkaM1"})
session_links = []
for session in s_list:
    session_links.append(session['href'])
session_links = session_links[:-9] #Remove useless links
    #Find session links hidden in decade links
decade_links = [x for x in session_links if len(x.split('/')[3])>4] #Find decade links
session_links = [x for x in session_links if x not in decade_links] #Remove decade links from session_links
new_sessions = []
for decade in decade_links: #Loop through decade links and find sessions
    d_req = Request(root + decade, headers={'User-Agent': 'Mozilla/5.0'})
    d_url = urlopen(d_req).read()
    d_bs = BeautifulSoup(d_url, "lxml")
    d_list = d_bs.find_all("a",{"class":"portrait-jkaM1"})
    for session in d_list:
        new_sessions.append(session['href'])
session_links.extend(new_sessions)#Add new session to session_links
half = len(session_links)//2
session_links_a = session_links[:half]
session_links_b = session_links[half:]

talk_links = []
#Loop through conference sessions
for link in session_links_a:
    
    #For each session make list of talk links
    year = link.split('/')[3]
    month = link.split('/')[4][:2]
    session_path = root + link
    t_req = Request(session_path, headers={'User-Agent': 'Mozilla/5.0'})
    t_url = urlopen(t_req).read()
    t_bs = BeautifulSoup(t_url, "lxml")
    t_list = t_bs.find_all("a",{"class":"item-U_5Ca"})
    for talk in t_list:
        d = {'y':year,'m':month, 'l':talk['href']}
        talk_links.append(dict(d))
    time.sleep(rand.randint(5,15))

print("sleeping...")
time.sleep(120)
print('back to work')

#Loop through conference sessions
for link in session_links_b:
    
    #For each session make list of talk links
    year = link.split('/')[3]
    month = link.split('/')[4][:2]
    session_path = 'https://www.lds.org' + link
    t_req = Request(session_path, headers={'User-Agent': 'Mozilla/5.0'})
    t_url = urlopen(t_req).read()
    t_bs = BeautifulSoup(t_url, "lxml")
    t_list = t_bs.find_all("a",{"class":"item-U_5Ca"})
    for talk in t_list:
        d = {'y':year,'m':month, 'l':talk['href']}
        talk_links.append(dict(d))
    time.sleep(rand.randint(5,10))

print("sleeping...")
time.sleep(120)
print('back to work')


# Remove session links from talk_links
tsession_links = [x for x in talk_links if len(x['l'].split('/')[4])>2] #Find decade links
talk_links = [x for x in talk_links if x not in tsession_links] #Remove decade links from session_links

# Loop through talk links and do the following:
    # Grab full text
    # Grab author's name
    # Grab author's title
    # Grab talk title
    # Remove footnotes
    # Remove weird formatting
    # Grab summary
    # Remove summary from full text
id_num = 0
for talk in talk_links:
    
    # create ID number
    id_num += 1
    # create bs object
    talk_path = 'https://www.lds.org' + talk['l']
    req = Request(talk_path, headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req).read()
    bs = BeautifulSoup(url, "lxml")
    # remove footnotes from talk
    footnote_list = bs.find_all("sup",{"class":"marker"})
    for f in footnote_list:
        bs.find("sup",{"class":"marker"}).replace_with('')
    # grab text of talk and clean
    try:
        text = bs.find("div",{"class":"body-block"}).getText()
        text_clean = text.encode("ascii","ignore")
        text_clean = text_clean.decode()
    except:
        text = 'no text found'
    # grab summary and remove from text
    try:
        text_summary = bs.find("p",{"kicker":"kicker1"}).getText()
        text_summary = text_summary.encode("ascii","ignore")
        text_summary = text_summary.decode()
        bs.find("p",{"kicker":"kicker1"}).replace_with('')
    except:
        text_summary = 'no summary found'
    # get text title
    try:
        text_title = bs.find("h1",{"id":"title1"}).getText()
        text_title = text_title.encode("ascii","ignore")
        text_title = text_title.decode()
    except:
        text_title = 'no title found'
    # get and clean text author
    try:
        text_author = bs.find("p",{"class":"author-name"}).getText()
        text_author = text_author.lower().replace('by ','')
        text_author = text_author.lower().replace('presented ','')
        text_author = text_author.lower().replace('president ','')
        text_author = text_author.lower().replace('elder ','')
        text_author = text_author.lower().replace('sister ','')
        text_author = text_author.lower().replace('bishop ','')
        text_author = text_author.encode("ascii","ignore")
        text_author = text_author.decode()
    except:
        text_author = 'no author found'
    # get text author title
    try:
        text_author_title = bs.find("p",{"class":"author-role"}).getText()
        text_author_title = text_author_title.encode("ascii","ignore")
        text_author_title = text_author_title.decode()
    except:
        text_author_title = 'no author title found'

    # create and write to text file
    file = open(save_path+talk['y']+'_'+talk['m']+'_'+str(id_num)+'.txt', 'w+')
    file.write('TITLE:'+'\n'+text_title+'\n')
    file.write('AUTHOR:'+'\n'+text_author+'\n')
    file.write('AUTHOR TITLE:'+'\n'+text_author_title+'\n')
    file.write('TEXT SUMMARY:'+'\n'+text_summary+'\n')
    file.write('TEXT:'+'\n'+text_clean+'\n')
    file.close()
    
    # sleep a bit out of respect
    time.sleep(rand.randint(5,10))




