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
          ['1','dsafgsef','awetgae','ergaer']
            ]
        
        
        
        GS = GoogleSheet.googleSheet()
        
        GS.updateInformation(values)
        print(GS.ReadProcessedID())
        
        
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
