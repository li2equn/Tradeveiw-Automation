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
#         labels = G.getService().users().labels().list(userId='me').execute().get('labels', [])
#         for label in labels:
#             print(label['name']+ " "+label['id'])
# =============================================================================
        GS = GoogleSheet.googleSheet()
        for i in GS.ReadProcessedID():
        #ID = '166c584b592ae544'
            mess = MessageManager.emailMessage(i,G)
            mess.MarkAsRead()
# =============================================================================
#         print(mess._content)
#         mess.downloadAttachment()
#         print(mess.getLastName())
#         print(mess.getFirstName())
#         print(mess.getFolderName())
#         print(mess.getNationality())
#         print(mess.getPlatform())
#         print(mess.getCountryName())
#         print(mess.getID())
#         
#         print(mess.getSubject())
#         #print(mess._content)
#         print(mess.getTradingKnowledge())
# =============================================================================
        
        #print(mess.AddressScreenShot())
        
        #mess.NameScreenShot()
        
    def atest_messageManager_corporate(self):
        G = MessageManager.gmail('2018/10/28','credentials_gmail1')
        print('There are '+str(len(G._messages))+' unread individual/corporate agreement')
        print(G.getAllIDs())
        ID = '166c5a9b72db9110'
        mess = MessageManager.emailMessage(ID,G)
# =============================================================================
#         mess.downloadAttachment()
#         print(mess.getLastName())
#         print(mess.getFirstName())
#         print(mess.getFolderName())
#         print(mess.getNationality())
#         print(mess.getPlatform())
#         print(mess.getCountryName())
#         print(mess.getID())
#         
#         print(mess.getSubject())
# =============================================================================
        print(mess._content)
        
        #print(mess.AddressScreenShot())
        
        #mess.NameScreenShot()
        
    
    
# =============================================================================
#         G2 = MessageManager.gmail('2018/10/28','credentials_gmail_operation')
#         print('There are '+str(len(G2._messages))+' unread individual agreement')
#         print(G2.getAllMessages())
#         ID = G2.getAllIDs()[0]
#         mess2 = MessageManager.emailMessage(ID,G2)
#         mess2.downloadAttachment()
#         print(mess2.getLastName())
#         print(mess2.getFirstName())
#         print(mess2.getFolderName())
#         print(mess2.getNationality())
#         print(mess2.getPlatform())
#         print(mess2.getCountryName())
#         print(mess2.getID())
#         
#         print(mess2.getSubject())
#         
#         print(mess2.AddressScreenShot())
#         
#         #mess.NameScreenShot()
#         mess.MarkAsRead()
# =============================================================================
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()