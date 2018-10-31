# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:14:18 2018

@author: Administrator
"""

import MessageManager
import Au10tix
import WorldCheck
import IdentityMind
import os

import threading
import time

from queue import Queue
from threading import Thread

from pprint import pprint
import GoogleSheet

from googleapiclient import discovery


HighRiskCountry = ['Afghanistan','Angola','Algeria','Bangladesh','Bolivia','Burkina Faso','Burundi','Cambodia','Cameroon','Central African Repulic'
                   ,'Chad','Colombia','Egypt','Eritrea','Ethiopia','Gambia','Guinea','Guinea Bissau','Haiti','India','Indonesia'
                   ,'Israel','Kenya','Laos','Lesotho','Liberia','Madagascar','Mali','Mozambique','Myanmar','Nepal','Niger','Nigeria'
                   ,'Pakistan','Palestinian Territory','Panama','Paraguay','Philippines','Sao Tome and Principe','Saudi Arabia'
                   ,'Sierra Leone','Sri Lanka','South Sudan','Tajikistan','Tanzania','Tunisia','Turkey','Ukraine','Uganda','Vanuatu'
                   ,'Venezueia','Zambia']


class individualAgreement(object):
    def __init__(self, Gmail, filemanager,Drive,ID):
        self._Drive = Drive
        self._ID = ID
        self._baseDir = filemanager.getbaseDir()
        #Get the email infomation
        self._message = MessageManager.emailMessage(self._ID,Gmail)
        #Download All the attachment
        self._message.downloadAttachment()
        #Format attachment Name
        self._filemanager = filemanager
        filemanager.FormatName(self._message.getFullName())
        
        self._message.AddressScreenShot()
        self._message.NameScreenShot()
        
        
        self._FullName = self._message.getFullName()
        self._emailAddress = self._message.getEmailAddress()
        self._Country = self._message.getCountryName()
        self._Sub = self._message.getSubject()
        
        
        
        #self._receivedDate = self._message.get
        #Au10tix
        bosusername = 'W.Chung@tvmarkets.com'
        bospassword = '83@h#k#0i65@'
        bosaddress = 'https://www.au10tixportalusa.com/VanillaRest/'        
        self._filepath = filemanager.getbaseDir() +self._FullName+'/'
        filename = filemanager.getIDfilename(self._FullName)
        
        
        
        #world check
        wcusername = 'TVmarkets'
        wcpassword = 'Tv431smt!'
        wcaddress = 'https://app.accelus.com/#accelus/fsp/case/539728a9-5215-4dd3-9728-e964c12af110/view/worldcheck'
        
        
        #IdentityMind
        imusername = 'bsadgrove@tvmarkets.com'
        impassword = 'Tr3ad$eViEw18'
        imaddress = 'https://edna.identitymind.com/merchantedna'
        
        if not filename:
            print('No ID')
            self._AUresult = None
        else:
            b = Au10tix.au10tix(bosaddress, bosusername, bospassword)
            b.Process(self._filepath,filename)
            self._AUresult = b.getResult()
        
        
        if not os.path.exists( self._filepath+self._FullName+'-'+'IdentityMind.pdf'):
            im = IdentityMind.identityMind(imaddress, imusername, impassword)
            try:
                im.Process(self._filepath,self._emailAddress,self._FullName)
            except:
                print('No Identity Mind')
        
        
        #WorldCheck
        if not os.path.exists( self._filepath+self._FullName+'-WorldCheck.pdf'):
            
            wc = WorldCheck.worldCheck(wcaddress, wcusername, wcpassword)
            wc.Process(self._baseDir+self._FullName+'/',self._message,self._FullName)
            self._WCresult = wc.getResult()
        


        
        
        
        Drive.CreateFolder(self._FullName,self._message.getPlatform())
        self.RiskMatrix()
        
        
        
        
        #upload to google Drive
        self._platform = self._message.getPlatform()
        
        
        
        
        self._attach = filemanager.getAttachments(self._FullName)
        
        
        
        for filename in self._attach:
            Drive.UploadFile(self._FullName,self._filepath,filename)
            
        
        
        if self._FullName+'-ID' in self._attach:
            self._IDphotp = True
        else:
            self._IDphoto = False
            
        if self._FullName+'-ProofAddress' in self._attach:
            self._POA = True
        else:
            self._POA = False
            
        if self._FullName+'-IdentityMind' in self._attach:
            self._IdentityMind = True
        else:
            self._IdentityMind = False
            
        if self._FullName+'-WorldCheck' in self._attach:
            self._WorldCheck = True
        else:
            self._WorldCheck = False
            
        self._idfilename = self._filemanager.getIDfilename(self._FullName)
        self._addressfilename=self._filemanager.getAddressfilename(self._FullName)
        self._imfilename = self._filemanager.getIMfilename(self._FullName)
        self._wcfilename = self._filemanager.getWCfilename(self._FullName)
        
        
        self._message.MarkAsRead()
            
        filemanager.removeFolder(self._FullName)
        
            
    def ReportResult(self):
        return [self._ID,self._Sub,self._FullName, self._emailAddress, self._Country,self._idfilename , self._addressfilename, self._AUresult , self._imfilename,self._wcfilename,self._platform]
    
    def RiskMatrix(self):
        self._Drive.CopyRiskMatrix(self._FullName)
        RiskMatrixID = self._Drive.getFileID(self._FullName+" RiskMatrix")
        
        self._RiskMatrix = GoogleSheet.googleSheet(RiskMatrixID)
        
        self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='A4',valueInputOption='RAW', body={'values': [[self._FullName]]}).execute()
        self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B26',valueInputOption='RAW', body={'values': [[time.strftime("%Y-%m-%d", time.gmtime())]]}).execute()
        #RiskMatrix['A4'] = self._FullName
        if self._Country in HighRiskCountry:
            #RiskMatrix['B7'] = 3
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B7',valueInputOption='RAW', body={'values': [[3]]}).execute()
        
           
        else:
            #RiskMatrix['B7'] = 1
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B7',valueInputOption='RAW',body={'values': [[1]]}).execute()
        
            
        
        if 'Corporate' in self._message.getSubject():
            #RiskMatrix['B8'] = 1
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B8',valueInputOption='RAW', body={'values': [[1]]}).execute()
        
            
        else:
            #RiskMatrix['B8'] = 3
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B8',valueInputOption='RAW', body={'values': [[3]]}).execute()
        
            
        if self._message.getManagementAccount() == 'Third party manager':
            #RiskMatrix['B9'] = 5
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B9',valueInputOption='RAW', body={'values': [[5]]}).execute()
        
            
        else:
            #RiskMatrix['B9'] = 1
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B9',valueInputOption='RAW', body={'values': [[1]]}).execute()
        
        if self._message.getTradingKnowledge() == 'N':
            
            #RiskMatrix['B12']=5
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B12',valueInputOption='RAW', body={'values': [[5]]}).execute()
        
        elif self._message.getTradingKnowledge() == 0:
            
            #RiskMatrix['B12'] = 3
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B12', valueInputOption='RAW',body={'values': [[3]]}).execute()
        
        elif self._message.getTradingKnowledge() == 2:
            #RiskMatrix['B12'] = 2
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B12',valueInputOption='RAW', body={'values': [[2]]}).execute()
        
            
        else:
            #RiskMatrix['B12'] = 1
            self._RiskMatrix._service.spreadsheets().values().update(spreadsheetId=RiskMatrixID,range ='B12', valueInputOption='RAW',body={'values': [[1]]}).execute()
        
            
    