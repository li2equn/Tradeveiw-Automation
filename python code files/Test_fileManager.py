# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:18:29 2018

@author: Administrator
"""

import unittest

import FileManager
import MessageManager



class Test_fileManager(unittest.TestCase):

    def test_fileManager(self):
        baseDir = 'C:/Users/Administrator/Documents/Individual Agreements/'
        
        fM = FileManager.fileManager(baseDir)
        
        G = MessageManager.gmail('2018/10/17','credentials_gmail1')
        ID = '1667d415f3ab66f5'
        mess = MessageManager.emailMessage(ID,G)
        mess.downloadAttachment()
        
        print('before format')
        print(fM.getAttachments(mess.getFullName()))
        
        fM.FormatName(mess.getFullName())
        
        print('after format')
        print(fM.getAttachments(mess.getFullName()))
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()