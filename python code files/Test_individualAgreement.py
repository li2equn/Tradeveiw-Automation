# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:14:18 2018

@author: Administrator
"""

import unittest
#from selenium import webdriver
#import time
#from bs4 import BeautifulSoup
import FileManager
import MessageManager

import IndividualAgreement
import DriveManager


class Test_IndividualAgreement(unittest.TestCase):

    def test_individualAgreement(self):
        baseDir = 'C:/Users/Administrator/Documents/Individual Agreements/'
        
        filemanager = FileManager.fileManager(baseDir)
        G = MessageManager.gmail('2018/10/22','credentials_gmail1')
        Drive = DriveManager.driveManager()
        ID = '166cc3673644d500'
        ia = IndividualAgreement.individualAgreement( G, filemanager, Drive,ID)
        print(ia.ReportResult())


       
        
if __name__ == "__main__":
    unittest.main()