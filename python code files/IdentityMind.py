# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:04:25 2018

@author: Administrator
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class identityMind(object):
    def __init__(self, address, username, password):
        self._username = username
        self._password = password
        self._address = address
        
        
    def Process(self,filepath,emailaddress,FullName):
        
        options = webdriver.ChromeOptions()

        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": filepath , "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        
        
        self._driver = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(self._driver, 60)
    
          # Optional argument, if not specified will search path.
        self._driver.get(self._address)
        self._driver.maximize_window()
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/table/tbody/tr[5]/td[2]/a[1]')))
        
        #log in to the Identity Mind
        self._driver.find_element_by_name('j_username').send_keys(self._username)
        self._driver.find_element_by_name('j_password').send_keys(self._password)
        self._driver.find_element_by_xpath('/html/body/form/table/tbody/tr[5]/td[2]/a[1]').click()
        
        #wait first page to load 
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="kyc"]/span')))
        
        #click KYC
        self._driver.find_element_by_xpath('//*[@id="kyc"]/span').click()
        
        #Click reset filter
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Reset Filter"]')))
        self._driver.find_element_by_xpath('//*[text()="Reset Filter"]').click()

        
        #Click 1-year
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'id-1y-')]/span/span")))
        self._driver.find_element_by_xpath("//*[contains(@id, 'id-1y-')]/span/span").click()
        #send email address as name
        self._driver.find_element_by_xpath('//*[@id="applicationFilter.applicantName"]').send_keys(emailaddress)
        #Click Apply filter
        self._driver.find_element_by_xpath('//*[text()="Apply Filter"]').click()
        
        # Wait to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='merchantedna-621220954']/div/div[1]")))

        wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@id='merchantedna-621220954']/div/div[1]")))
        time.sleep(2)
        try:
            self._driver.find_element_by_xpath("//*[text() = 'Print to PDF']").click()
        except:
        #wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='applicationView.table']/div[2]/div[1]/table/tbody/tr/td[2]/div")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[text()='"+emailaddress+"'])[1]")))
            try:
                self._driver.find_element_by_xpath("(//*[text()='Accepted'])[1]").click()
            except:
                self._driver.find_element_by_xpath("//*[@id='applicationView.table']/div[2]/div[1]/table/tbody/tr[1]/td[4]/div").click()

            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='merchantedna-621220954']/div/div[1]")))
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@id='merchantedna-621220954']/div/div[1]")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text() = 'Print to PDF']")))
        self._driver.find_element_by_xpath("//*[text() = 'Print to PDF']").click()        
        while not any(map(lambda x: x.startswith('Application'), os.listdir(filepath))):
            time.sleep(1)
        self._driver.quit()
        
        for filename in os.listdir(filepath):
            extension = os.path.splitext(filename)[1]
            if 'Application' in filename:
                if not os.path.exists( filepath+FullName+'-'+'IdentityMind'+extension ):
                    os.rename(filepath+filename,filepath+FullName+'-'+'IdentityMind'+extension)
                else:
                    print('File '+os.path.basename(os.path.dirname(filepath))+'-IdentityMind.pdf'+' exists.')
                
                print('change name')