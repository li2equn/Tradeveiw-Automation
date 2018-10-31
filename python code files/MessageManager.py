# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 12:52:49 2018

@author: Administrator
"""

from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import time
import os
from selenium import webdriver
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# If modifying these scopes, delete the file token.json.
class gmail(object):
    def __init__(self, StartDate
                 , credentials
                 #, EndDate
                 ):
        #StartDate should be a datetime.date object
        #self._StartDate = StartDate
        self._SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
        store = file.Storage('token_gmail'+credentials+'.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials+'.json', self._SCOPES)
            creds = tools.run_flow(flow, store)
        self._service = build('gmail', 'v1', http=creds.authorize(Http()))
        # Call the Gmail API
        self._response =self._service.users().messages().list(userId='me',q = '{subject: "Individual Agreement" subject: "Corporate Agreement"} -subject:Fwd:  -subject:RE:  has:attachment is:unread after:'+StartDate
                                           #+' before:'+EndDate
                                               ).execute()
        self._messages = []
        if 'messages' in self._response:
            self._messages.extend(self._response['messages'])

        while 'nextPageToken' in self._response:
            page_token = self._response['nextPageToken']
            self._response = self._service.users().messages().list(userId='me',q = 'subject: Individual Agreement -subject:Fwd: -subject:RE:  has:attachment is:unread after:'+StartDate+' before:'+EndDate,
                                         pageToken=page_token).execute()
            self._messages.extend(self._response['messages'])
    #print(messages)
    def getService(self):
        return self._service
    
    def getAllIDs(self):
        messID = list(map(lambda x: x['id'], self._messages))
        return messID
    
    def getAllMessages(self):
        messID = list(map(lambda x: x['id'], self._messages))
        mess = list(map(lambda x: self.getService().users().messages().get(userId='me', id=x).execute(),messID))
        messSub = list(map(lambda y: list(filter(lambda x: x['name'] == 'Subject',y['payload']['headers']))[0]['value'], mess))
# =============================================================================
#         messName = list(map(lambda y: dict((item.text.split(': ')[0], item.text.split(': ')[1]) for item in BeautifulSoup(base64.urlsafe_b64decode(y['payload']['parts'][0]['body']['data'].encode('UTF-8')),'lxml').find_all('p'))['First Name']+' '+dict((item.text.split(': ')[0], item.text.split(': ')[1]) for item in BeautifulSoup(base64.urlsafe_b64decode(y['payload']['parts'][0]['body']['data'].encode('UTF-8')),'lxml').find_all('p'))['Last Name'],mess))
#         messEmail = list(map(lambda y: dict((item.text.split(': ')[0], item.text.split(': ')[1]) for item in BeautifulSoup(base64.urlsafe_b64decode(y['payload']['parts'][0]['body']['data'].encode('UTF-8')),'lxml').find_all('p'))['Email'],mess))
# =============================================================================
        return dict(zip(messID,messSub))
        #return list(map(lambda x: (messID[x],messSub[x],messName[x]), range(len(messID))))
    def getID(self,Sub):
        return self.getAllMessages()[Sub]
    

class emailMessage(object):
    def __init__(self, ID,gmail):
        self._id = ID
        self._message = gmail.getService().users().messages().get(userId='me', id=self._id).execute()
        self._content = dict((item.text.split(': ')[0], item.text.split(': ')[1:]) for item in BeautifulSoup(base64.urlsafe_b64decode(self._message['payload']['parts'][0]['body']['data'].encode('UTF-8')),'lxml').find_all('p'))
        self._gmail = gmail
        self._subject = list(filter(lambda x: x['name'] == 'Subject',self._message['payload']['headers']))[0]['value']
    def getSubject(self):
        return self._subject
    def getID(self):
        return self._id
    def getFirstName(self):
        return self._content['First Name'][0]
    def getLastName(self):
        return self._content['Last Name'][0]
    def getFullName(self):
        return self.getFirstName()+' '+self.getLastName()
    def getCountryName(self):
        return self._content['Country'][0]
    def getEmailAddress(self):
        return self._content['Email'][0]
    def getIBNum(self):
        return self._content['IB#'][0]
    def getManagementAccount(self):
        return self._content['Management of account'][0]
    def getFolderName(self):
        
        if 'Individual' in self.getSubject():
            return self._content['Folder (individual_documents)'][0]
        else:
            return self._content['Folder (corporate_documents)'][0]
    def getPhone(self):
        return self._content['Home Phone'][0]
    def getNationality(self):
        return self._content['Nationality'][0]
    def getPlaceBirth(self):
        return self._content['Place of Birth'][0]
    def getCity(self):
        return self._content['City'][0]
    def getTradingKnowledge(self):
        knowledgelist =[
                self._content['On-Exchange Securities'][1][1],
                self._content["Leverage FX, CFD's and Precious Metals"][1][1],
                self._content['Commodities'][1][1],
                self._content['Futures'][1][1],
                self._content['Options'][1][1],
                self._content['Mutual Funds'][1][1]
                ]
        if len(set(knowledgelist)) == 1:
            return 'N'
        elif 'M' in knowledgelist:
            return 10
        else:
            return max(list(map(lambda y: int(y),list(filter(lambda x: x.isdigit(),knowledgelist)))))
        
    def getBirthD(self):
        return time.strptime(self._content['Day of Birth'][0],'%d / %b / %Y').tm_mday
    
    def getBirthM(self):
        return time.strptime(self._content['Day of Birth'][0],'%d / %b / %Y').tm_mon
    
    def getBirthY(self):
        return time.strptime(self._content['Day of Birth'][0],'%d / %b / %Y').tm_year
    def getFullAddress(self):
        return self._content['Country'][0]+' '+self._content['Province'][0]+' '+self._content['City'][0]+' '+self._content['Address'][0]+' '+self._content['Address2'][0]
    def getPlatform(self):
        if 'MT4' in self._content['Platform'][0] and self.getCountryName() == 'Japan':
            return 'MT4 accounts JAPAN'
        elif 'MT4' in self._content['Platform'][0] and self.getCountryName() != 'Japan':
            return 'MT4 accounts'
        elif 'MT5' in self._content['Platform'][0] and self.getCountryName() == 'Japan':
            return 'MT5 Accounts JAPAN'
        elif 'MT5' in self._content['Platform'][0] and self.getCountryName() != 'Japan':
            return 'MT5 Accounts'
        elif 'cTrader' in self._content['Platform'][0] and self.getCountryName() == 'Japan':
            return 'cTrader - Currenex JAPAN'
        elif 'cTrader' in self._content['Platform'][0] and self.getCountryName() != 'Japan':
            return 'cTrader - Currenex'
        elif 'Currenex' in self._content['Platform'][0] and self.getCountryName() == 'Japan':
            return 'cTrader - Currenex JAPAN'
        elif 'Currenex' in self._content['Platform'][0] and self.getCountryName() != 'Japan':
            return 'cTrader - Currenex'
        elif 'Equities' in self._content['Platform'][0] :
            return 'Equities'
        else:
            return self._content['Platform'][0]
    def getFileFolder(self):
        filefolder = 'C:/Users/Administrator/Documents/Individual Agreements/'+self.getFullName()+'/'
        if not os.path.exists( filefolder ):
            os.makedirs(filefolder)
        return filefolder
    def downloadAttachment(self):
        for part in self._message['payload']['parts'][1:]:
            att_id=part['body']['attachmentId']
            att=self._gmail.getService().users().messages().attachments().get(userId='me', messageId=self._id,id=att_id).execute()
            data=att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            
            filepath = self.getFileFolder()+part['filename']
            if not os.path.exists( filepath ):
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                    f.close()
            else:
                print('File '+part['filename']+' exists.')
        
    def MarkAsRead(self):
        self._gmail.getService().users().messages().modify(userId='me', id=self._id,
                                                        body={"addLabelIds": ['Label_1078048674160145953'],
                                                                "removeLabelIds": ['UNREAD']}).execute()
        
    
        
# =============================================================================
#         label_ids = message['labelIds']
#         
#         print ('Message ID: %s - With Label IDs %s' % (self._id, label_ids))
#         return message
# =============================================================================
    
    def AddressScreenShot(self):
        
        addressDriver = webdriver.Chrome()
        wait = WebDriverWait(addressDriver, 60)
        addressDriver.get('https://www.google.com/maps')
        addressDriver.maximize_window()
        wait.until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
        addressDriver.find_element_by_id('searchboxinput').send_keys(self.getFullAddress())
        wait.until(EC.element_to_be_clickable((By.ID, 'searchbox-searchbutton')))
        addressDriver.find_element_by_id('searchbox-searchbutton').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[3]/button')))
        page = addressDriver.page_source
        time.sleep(5)
        pic = pyautogui.screenshot()
        # Save the image
        
        pic.save(self.getFileFolder()+self.getFullName()+'-AddressScreenshot.png') 
        
        addressDriver.quit()
        try:
            BeautifulSoup(page,'lxml').findall(text='Directions')
            return True
        except:
            return False
        
        
        
        
    def NameScreenShot(self):
        
        nameDriver = webdriver.Chrome()
        wait = WebDriverWait(nameDriver, 60)
        nameDriver.get('https://www.google.com')
        nameDriver.maximize_window()
        wait.until(EC.presence_of_element_located((By.NAME, 'q')))
        nameDriver.find_element_by_name('q').send_keys(self.getFullName()+' '+self.getCountryName())
        #wait.until(EC.element_to_be_clickable((By.NAME, 'btnK')))import org.openqa.selenium.Keys
        nameDriver.find_element_by_name('q').send_keys(Keys.ENTER)
#        nameDriver.find_element_by_name('btnK').click()
 #       wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[3]/button')))
        time.sleep(5)
        pic = pyautogui.screenshot()
        # Save the image
        
        pic.save(self.getFileFolder()+self.getFullName()+'-NameScreenshot.png') 
        nameDriver.quit()