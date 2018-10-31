# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:10:24 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class worldCheck(object):
    def __init__(self, address, username, password):
        self._username = username
        self._password = password
        self._address = address
        
        
    def Process(self,filepath,emailobject,FullName):
        #the emailobject must have getFullNmae(), getCountryName(), getPlaceBirth(),
        #getNationality(), getBirthD, getBirthM, getBirthY
        
        
        options = webdriver.ChromeOptions()

        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": filepath , "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        
        
        self._driver = webdriver.Chrome(chrome_options=options)
        wait = WebDriverWait(self._driver, 60)
    
        # Optional argument, if not specified will search path.
        self._driver.get(self._address)
        self._driver.maximize_window()
        wait.until(EC.element_to_be_clickable((By.NAME, 'SignIn')))
        self._driver.find_element_by_name('Username').send_keys(self._username)
        self._driver.find_element_by_name('Password').send_keys(self._password)
        self._driver.find_element_by_name('SignIn').click()
        wait.until(EC.element_to_be_clickable((By.ID, 'dijit_form_DropDownButton_1')))
        #WebDriverWait(self._driver, 120).until(EC.presence_of_element_located((By.ID, 'dijit__WidgetsInTemplateMixin_2')))
        
        self._driver.find_element_by_id('dijit_form_DropDownButton_1').click()
        self._driver.find_element_by_id('dijit_MenuItem_3_text').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="accelus_components_application_IframeView_0"]/iframe')))
        
        frame = self._driver.find_element_by_xpath('//*[@id="accelus_components_application_IframeView_0"]/iframe')
        self._driver.switch_to.frame(frame)
        
        wait.until(EC.element_to_be_clickable((By.ID, 'dijit_form_Button_1_label')))
        
        self._driver.find_element_by_xpath('//*[@id="indium_view_form_ValidationTextBox_0"]').send_keys(emailobject.getFullName())
        self._driver.find_element_by_xpath('//*[@id="dijit_form_FilteringSelect_3"]').send_keys(emailobject.getCountryName())
        self._driver.find_element_by_xpath('//*[@id="dijit_form_FilteringSelect_4"]').send_keys(emailobject.getPlaceBirth())
        self._driver.find_element_by_xpath('//*[@id="dijit_form_FilteringSelect_5"]').send_keys(emailobject.getNationality())
        self._driver.find_element_by_xpath('//*[@id="dijit_form_FilteringSelect_0"]').send_keys(emailobject.getBirthD())
        self._driver.find_element_by_xpath('//*[@id="dijit_form_FilteringSelect_1"]').send_keys(emailobject.getBirthM())
        self._driver.find_element_by_xpath('//*[@id="dijit_form_FilteringSelect_2"]').send_keys(emailobject.getBirthY())
        
        
        self._driver.find_element_by_xpath('//*[@id="dijit_form_Button_1_label"]').click()
        try:
            self._driver.find_element_by_id("dijit__MasterTooltip_0")
            print('Invalid input')
            self._result = False
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type = 'checkbox']")))
        
            self._driver.find_element_by_xpath("//input[@type = 'checkbox']").click()
            self._driver.find_element_by_xpath('//*[@title="Export"]').click()
            self._driver.find_element_by_xpath('//*[@id="dijit_form_RadioButton_6"]').click()
                
                
            self._driver.find_element_by_xpath('//*[@id="dijit_form_Button_6"]').click()
            self._result = True
        
        
        time.sleep(2)
        self._driver.quit()
        
        
        for filename in os.listdir(filepath):
            extension = os.path.splitext(filename)[1]
            if 'Case' in filename:
                if not os.path.exists( filepath+FullName+'-WorldCheck'+extension ):
                    os.rename(filepath+filename,filepath+FullName+'-WorldCheck'+extension)
                    print('world check change name')
                else:
                    print('File '+os.path.basename(filepath+FullName+'-WorldCheck'+extension+' exists.'))
                
    def getResult(self):
        return self._result