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

#Make list of all conference sessions links
conference_path = 'https://www.lds.org/general-conference/conferences?lang=eng'
s_req = Request(conference_path, headers={'User-Agent': 'Mozilla/5.0'})
s_url = urlopen(s_req).read()
s_bs = BeautifulSoup(s_url, "lxml")
s_list = s_bs.find_all("a",{"class":"year-line__link"})
session_links = []
for session in s_list:
    session_links.append(session['href'])
session_links[:] = [x for x in session_links if x != ''] #Remove missing values from session_links
half = len(session_links)//2
session_links_a = session_links[:half]
session_links_b = session_links[half:]

talk_links = []
#Loop through conference sessions
for link in session_links_a:
    
    #For each session make list of talk links
    year = link.split('/')[2]
    month = link.split('/')[3][:2]
    session_path = 'https://www.lds.org' + link
    t_req = Request(session_path, headers={'User-Agent': 'Mozilla/5.0'})
    t_url = urlopen(t_req).read()
    t_bs = BeautifulSoup(t_url, "lxml")
    t_list = t_bs.find_all("a",{"class":"lumen-tile__link"})
    for talk in t_list:
        d = {'y':year,'m':month, 'l':talk['href']}
        talk_links.append(dict(d))
    time.sleep(rand.randint(5,10))

print("sleeping...")
time.sleep(120)
print('back to work')

#Loop through conference sessions
for link in session_links_b:
    
    #For each session make list of talk links
    year = link.split('/')[2]
    month = link.split('/')[3][:2]
    session_path = 'https://www.lds.org' + link
    t_req = Request(session_path, headers={'User-Agent': 'Mozilla/5.0'})
    t_url = urlopen(t_req).read()
    t_bs = BeautifulSoup(t_url, "lxml")
    t_list = t_bs.find_all("a",{"class":"lumen-tile__link"})
    for talk in t_list:
        d = {'y':year,'m':month, 'l':talk['href']}
        talk_links.append(dict(d))
    time.sleep(rand.randint(5,10))

print("sleeping...")
time.sleep(120)
print('back to work')

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
for talk in talk_links[:2]:
    
    # create ID number
    id_num += 1
    # create bs object
    talk_path = 'https://www.lds.org' + talk['l']
    req = Request(talk_path, headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req).read()
    bs = BeautifulSoup(url, "lxml")
    # grab text of talk and clean
    text = bs.find("div",{"class":"body-block"}).get_text()
    text_clean = unicodedata.normalize("NFKD", text).rstrip().lstrip().replace(u'\ufeff','')
    # grab summary and remove from text
    try:
        text_summary = bs.find("p",{"kicker":"kicker1"}).get_text()
        bs.find("p",{"kicker":"kicker1"}).replace_with('')
    except:
        text_summary = 'no summary found'
    # remove footnotes from talk (use find and replace)
    
    # get text title
    text_title = bs.find("h1",{"id":"title1"}).get_text()
    # get and clean text author
    text_author = bs.find("p",{"class":"author-name"}).get_text()
    text_author = text_author.lower().replace('by ','')
    text_author = text_author.lower().replace('presented ','')
    text_author = text_author.lower().replace('president ','')
    text_author = text_author.lower().replace('elder ','')
    text_author = text_author.lower().replace('sister ','')
    text_author = text_author.lower().replace('bishop ','')
    # get text author title
    text_author_title = bs.find("p",{"class":"author-role"}).get_text()

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




