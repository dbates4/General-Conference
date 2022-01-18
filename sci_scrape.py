# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 22:55:15 2022

Scrapes the scripture citation index

@author: Dylan
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random as rand


save_path = 'C:/Users/dylan/Datasets/lds/genconftext/'
sci_gc_link = 'https://scriptures.byu.edu/#:t'

# last talk is at t2177
for i in range(2):
    page_id = i + 1
    page_link = sci_gc_link + str(page_id)
    
    # Run in headless mode so it doesn't open a window
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    
    # Create driver object and open page
    DRIVER_PATH = 'C:/Users/Dylan/Projects/chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(page_link)
    
    # Grab relevant text
    title = driver.find_element_by_class_name('gctitle').text
    speaker = driver.find_element_by_class_name('gcspeaker').text
    bib = driver.find_element_by_class_name('gcbib').text
    calling = driver.find_element_by_class_name('gcspkpos').text
    body = driver.find_element_by_class_name('gcbody').text
    
    # Create and write to text file
    file = open(save_path+'t'+page_id, 'w+')
    file.write('TITLE:'+'\n'+title+'\n')
    file.write('SPEAKER:'+'\n'+speaker.split(' ',1)[1]+'\n')
    file.write('SPEAKER TITLE:'+'\n'+speaker.split(' ')[0]+'\n')
    file.write('SPEAKER CALLING:'+'\n'+calling+'\n')
    file.write('TEXT:'+'\n'+body+'\n')
    file.close()
    
    # Close the driver object
    driver.quit()
    
    # sleep a bit out of respect
    time.sleep(rand.randint(5,10))
    




