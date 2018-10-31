# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:38:22 2018

@author: Administrator
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os

class au10tix(object):
    def __init__(self, address, username, password):
        self._username = username
        self._password = password
        self._address = address
        
        
    def Process(self,filepath,name):
        
        options = webdriver.ChromeOptions()

        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": filepath , "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        
        
        self._driver = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(self._driver, 60)
          # Optional argument, if not specified will search path.
        self._driver.get('https://www.au10tixportalusa.com/VanillaRest/')
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/div[2]/form/button')))
        ##log in
        self._driver.find_element_by_name('j_username').send_keys(self._username)
        self._driver.find_element_by_name('j_password').send_keys(self._password)
        self._driver.find_element_by_xpath('/html/body/div/article/div[2]/form/button').click()
        
        ##upload
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/ng-view/div/section/div/section/a')))
        self._driver.find_element_by_xpath('/html/body/div/article/ng-view/div/section/div/section/a').click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="addFilesOneSide"]/div/div/div[2]/div/div[1]/div/div/div[2]/div/input')))
        
        self._driver.find_element_by_xpath('//*[@id="addFilesOneSide"]/div/div/div[2]/div/div[1]/div/div/div[2]/div/input').send_keys(filepath+name)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="addFilesOneSide"]/div/div/div[3]/button[2]')))
        self._driver.find_element_by_xpath('//*[@id="addFilesOneSide"]/div/div/div[3]/button[2]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainTable"]/table/tbody/tr[1]/td[1]/div/label')))
        self._driver.find_element_by_xpath('//*[@id="mainTable"]/table/tbody/tr/td[3]').click()
        handles = self._driver.window_handles
        self._driver.switch_to.window(handles[1])
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/article/ng-view/div/section[1]/div/span')))
        self._this_page = self._driver.page_source
        time.sleep(1)
        #wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/article/ng-view/div/section[2]/div[2]')))

        try:
            self._driver.find_element_by_xpath('/html/body/div/article/ng-view/div/section[2]/div[2]').click()
            #WebDriverWait(self._driver, 60).until(lambda x: x.find_element_by_xpath('/html/body/div/article/ng-view/div/section[2]/div[2]')).click()
            
            self._driver.find_element_by_xpath('/html/body/div/article/ng-view/div/section[2]/div[2]/div/ul/li/a').click()
            
            self._result = BeautifulSoup(self._this_page,'lxml').find('span', class_ = 'ng-binding').text
            

            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='PDF']")))
            #print(str(BeautifulSoup(self._this_page,'lxml').find(text='PDF').parent))
            self._downloadname = re.findall(r"\d/(.+).pdf", str(BeautifulSoup(self._this_page,'lxml').find(text='PDF').parent))[0]
            #self._downloadname = re.findall(r"\d/(.+).pdf", pdf_url)[0]
            #old = max([f for f in os.listdir(filepath)], key=os.path.getctime)
            
            
            old = filepath+self._downloadname+ '.pdf'
            #print(old)
            while not os.path.exists(old):
                time.sleep(1)
                
            newfilepath = filepath+os.path.basename(os.path.dirname(filepath))+'-Au10tix.pdf'
            if not os.path.exists( newfilepath ):
                os.rename(old,newfilepath )
            else:
                print('File '+os.path.basename(os.path.dirname(filepath))+'-Au10tix.pdf'+' exists.')
        except:
            self._result = 'aborted'
            print('Processing Request Rejected')
        
        self._driver.quit()
        
    def getResult(self):
        return self._result
