# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 12:25:08 2018

@author: Administrator
"""

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

class driveManager(object):
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('token_drive.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials_drive.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self._service = build('drive', 'v3', http=creds.authorize(Http()))
    
    def getFileID(self, FileName):
        results = self._service.files().list(q="name = '"+FileName+"' and mimeType != 'application/vnd.google-apps.folder'", fields="files(id, name,mimeType,description,parents,trashed)",pageSize = 1000,pageToken=None).execute()
        #fields="files(id, name,mimeType,description,parents)"
        items = results.get('files', [])
        return items[0]['id']
    def getFolderID(self, FolderName):
        results = self._service.files().list(q="name = '"+FolderName+"' and mimeType = 'application/vnd.google-apps.folder'", fields="files(id, name,mimeType,description,parents,trashed)",pageSize = 1000,pageToken=None).execute()
        #fields="files(id, name,mimeType,description,parents)"
        items = results.get('files', [])
        return items[0]['id']
    
    
    def getAllFolders(self, parentFolderName=None):
        if parentFolderName == None:
            parentFolderID = '0AHmsVRr7NBF3Uk9PVA'
        else:
            try:
                parentFolderID = self.getFolderID(parentFolderName)
            except:
                print('ParentFolderName does not exist')
                
        results = self._service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and parents in '"+parentFolderID+"' and trashed = False", fields="files(id, name,parents)",pageSize = 1000,pageToken=None).execute()
        return list(map(lambda x: x['name'], results.get('files', [])))
    
    def getAllFiles(self, parentFolderName=None):
        if parentFolderName == None:
            parentFolderID = '0AHmsVRr7NBF3Uk9PVA'
        else:
            try:
                parentFolderID = self.getFolderID(parentFolderName)
            except:
                print('ParentFolderName does not exist')
                print(parentFolderName)
                #exit
                return []
        results = self._service.files().list(q="mimeType != 'application/vnd.google-apps.folder' and parents in '"+parentFolderID+"' and trashed = False", fields="files(id, name,parents)",pageSize = 1000,pageToken=None).execute()
        return list(map(lambda x: x['name'], results.get('files', [])))
    
    def CheckFileExistence(self,filename,parentFolderName=None):
        if filename in self.getAllFiles(parentFolderName):
            return True
        else:
            return False
        
    def CheckFolderExistence(self,FolderName,parentFolderName=None):
        if FolderName in self.getAllFolders(parentFolderName):
            return True
        else:
            return False
    
    
    def UploadFile(self, FolderName, filepath, filename):
        if not self.CheckFileExistence(filename,FolderName):
            if FolderName != None:
                FolderID = self.getFolderID(FolderName)
                file_metadata = {'name': filename,
                         'parents':[FolderID]}
                media = MediaFileUpload(filepath+filename)
                self._service.files().create(body=file_metadata,media_body=media,fields='id').execute()
            else:
                file_metadata = {'name': filename}
                media = MediaFileUpload(filepath+filename)
                        #mimetype='image/png')
                self._service.files().create(body=file_metadata,media_body=media,fields='id').execute()
        else:
            print('Exist in Drive')
        
        
        
                
    def CreateFolder(self,FolderName,parentFolderName=None):
        if not self.CheckFolderExistence(FolderName,parentFolderName):
            if parentFolderName != None:
                try:
                    parentFolderID = self.getFolderID(parentFolderName)
                except:
                    self.CreateFolder(parentFolderName)
                    parentFolderID = self.getFolderID(parentFolderName)
                file_metadata = {'name':FolderName,'parents': [parentFolderID],'mimeType':'application/vnd.google-apps.folder'}
                self._service.files().create(body=file_metadata,fields='id').execute()
            else:
                file_metadata = {'name':FolderName,'mimeType': 'application/vnd.google-apps.folder'}
                self._service.files().create(body=file_metadata,fields='id').execute()
        else:
            print(FolderName +' exists')
        
        
    def CopyRiskMatrix(self, FullName):
        FolderID = self.getFolderID(FullName)
        #print(FolderID)
        copied_file = {'name': FullName+" RiskMatrix",
                       'parents':[FolderID]}
        filesource = self._service.files().copy(fileId="1JLlnHCEqlWi_WihVKBvjbTP5PlsR2RwlCH2q0oX1MQc", body=copied_file).execute()
        #print(filesource)
# =============================================================================
#         updated_file = self._service.files().update(
#         fileId=file_id,
#         body=file,
#         newRevision=new_revision,
#         media_body=media_body).execute()
# =============================================================================
