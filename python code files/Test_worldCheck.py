# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:10:24 2018

@author: Administrator
"""

import unittest
#from selenium import webdriver
#import time
#from bs4 import BeautifulSoup
import WorldCheck
import MessageManager
from datetime import date

class Test_worldCheck(unittest.TestCase):

    def test_worldCheck(self):
        
         
        baseDir = 'C:/Users/Administrator/Documents/Individual Agreements/'
        
        
        
        G = MessageManager.gmail('2018/10/22','credentials_gmail1')
        #ID = '1668cdc8f9dada84'
        ID ='1668da875689cf28' #input not valid
        ID = '166944d8763e33bb'
        mess = MessageManager.emailMessage(ID,G)
        mess.downloadAttachment()
        
        FullName =  mess.getFullName()
        
        
        print(FullName)
        
        
        
        username = 'TVmarkets'
        password = 'Tv431smt!'
        address = 'https://app.accelus.com/#accelus/fsp/case/539728a9-5215-4dd3-9728-e964c12af110/view/worldcheck'
        wc = WorldCheck.worldCheck(address, username, password)
        wc.Process(baseDir+FullName+'/',mess,FullName)
        
        print(wc.getResult())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()