# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 12:25:08 2018

@author: Administrator
"""

import DriveManager
import unittest
import time
class Test_driveManager(unittest.TestCase):

    def test_driveManager(self):
        
        DM = DriveManager.driveManager()   
# =============================================================================
        print('get foldre ID')
        print(DM.getFolderID('MT5 Accounts'))
        
        print('get file id')
        print(DM.getFileID(' 323523>>Xin Liu>>ID translation'))
        
        print('get all folders in mt4 account')
        print(DM.getAllFolders('MT4 accounts'))
        
        print('get all files in the folder')
        print(DM.getAllFiles('705046 KAZUTAKA ARITOMI'))
        
        print('create folder')
        DM.CreateFolder('test')
        
        time.sleep(5)
        print('check existence of created folder')
        print(DM.CheckFolderExistence('test'))
        #DM.UploadFile('test','C:/Users/Intern/Desktop/','tradeview_logo.png')
        print('create the same folder')
        DM.CreateFolder('test')
# =============================================================================
        DM.CopyRiskMatrix('Munemichi Ishikawa')
        
        
if __name__ == "__main__":
    
    unittest.main()
