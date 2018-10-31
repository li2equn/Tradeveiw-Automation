# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:27:51 2018

@author: Administrator
"""


import unittest

import GoogleSheet


class Test_GoogleSheet(unittest.TestCase):

    def test_googlesheet(self):
        
        values = [
          ['166cae07e4b68791', 'Individual Agreement - IB# 1604 - 1541001342-KZvmU', 'Toshifumi Nakata', 'towelieeeee1000@gmail.com', 'Japan', 'Toshifumi Nakata-ID.jpg', 'Toshifumi Nakata-AddressScreenshot.png', 'Passed', 'Toshifumi Nakata-IdentityMind.pdf', 'Toshifumi Nakata-WorldCheck.pdf', 'MT4 accounts JAPAN']
           
            ]
        
        
        
        GS = GoogleSheet.googleSheet()
        
        GS.updateInformation(values)
        print(GS.ReadProcessedID())
        
        
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()