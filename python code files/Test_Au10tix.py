# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:54:49 2018

@author: Administrator
"""

import unittest

import Au10tix
import FileManager
import MessageManager


class Test_Au10tix(unittest.TestCase):

    def test_au10tix(self):
        baseDir = 'C:/Users/Administrator/Documents/Individual Agreements/'
        
        fM = FileManager.fileManager(baseDir)
        G = MessageManager.gmail('2018/10/22','credentials_gmail1')
        ID = '166c529c709708d8'
        mess = MessageManager.emailMessage(ID,G)
        mess.downloadAttachment()
        
        
        FullName =  mess.getFullName()
        print(FullName)
        fM.FormatName(mess.getFullName())
        username = 'W.Chung@tvmarkets.com'
        password = '83@h#k#0i65@'
        address = 'https://www.au10tixportalusa.com/VanillaRest/'
        
        filepath = baseDir + FullName +'/'
        filename = fM.getIDfilename(FullName)
        b = Au10tix.au10tix( address, username, password)
        #b.Login()
        b.Process(filepath,filename)
        print(b.getResult())
        #print(b._downloadname)        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()