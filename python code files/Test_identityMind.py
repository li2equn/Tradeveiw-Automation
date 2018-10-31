# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:04:25 2018

@author: Administrator
"""

import unittest
#from selenium import webdriver
#import time
#from bs4 import BeautifulSoup
import IdentityMind
#import FileManager
import MessageManager


class Test_identityMind(unittest.TestCase):

    def test_identityMind(self):
       baseDir = 'C:/Users/Administrator/Documents/Individual Agreements/'
        
        
        
       G = MessageManager.gmail('2018/10/22','credentials_gmail1')
       ID = "166a1dad771c9b8d"
       mess = MessageManager.emailMessage(ID,G)
       mess.downloadAttachment()
        
       FullName =  mess.getFullName()
        
        
       print(FullName)
       print(mess.getEmailAddress())
       username = 'bsadgrove@tvmarkets.com'
       password = 'Tr3ad$eViEw18'
       address = 'https://edna.identitymind.com/merchantedna'
       
       im = IdentityMind.identityMind(address, username, password)
       im.Process(baseDir+FullName+'/',mess.getEmailAddress(),FullName)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()