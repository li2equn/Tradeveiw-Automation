# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:08:13 2018

@author: Administrator
"""

import unittest

import MessageManager
import GoogleSheet



class Test_MessageManager(unittest.TestCase):

    def test_messageManager_individual(self):
        G = MessageManager.gmail('2018/10/25','credentials_gmail1')
        print('There are '+str(len(G._messages))+' unread individual/corporate agreement')
        #print(G.getAllIDs())
        #print(G.getAllMessages()['166c584b592ae544'])
# =============================================================================
        labels = G.getService().users().labels().list(userId='me').execute().get('labels', [])
        for label in labels:
            print(label['name']+ " "+label['id'])
# =============================================================================
        GS = GoogleSheet.googleSheet()
        for i in GS.ReadProcessedID():
        #ID = '166c584b592ae544'
            mess = MessageManager.emailMessage(i,G)
            mess.MarkAsRead()
# =============================================================================
        print(mess._content)
        mess.downloadAttachment()
        print(mess.getLastName())
        print(mess.getFirstName())
        print(mess.getFolderName())
        print(mess.getNationality())
        print(mess.getPlatform())
        print(mess.getCountryName())
        print(mess.getID())
        
        print(mess.getSubject())
        #print(mess._content)
        print(mess.getTradingKnowledge())
# =============================================================================
        
        #print(mess.AddressScreenShot())
        
        #mess.NameScreenShot()
        
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
