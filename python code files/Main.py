# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:30:00 2018

@author: Administrator
"""

import FileManager
import MessageManager
import IndividualAgreement
import DriveManager
import GoogleSheet


def main():
    baseDir = 'C:/Users/Administrator/Documents/Individual Agreements/'
        
    filemanager = FileManager.fileManager(baseDir)
    Drive = DriveManager.driveManager()
    GS = GoogleSheet.googleSheet()
    ProcessedID = GS.ReadProcessedID()

    while True:
        ###########################################################################
        Gmail = MessageManager.gmail('2018/10/28','credentials_gmail1')
        ###########################################################################
        UnreadID = Gmail.getAllIDs()
        Process = set(UnreadID)-set(ProcessedID)
        
        for I in Process:
            print(I)
            mess = MessageManager.emailMessage(I,Gmail)
            try:
                ia = IndividualAgreement.individualAgreement( Gmail, filemanager, Drive,I)
                li= ia.ReportResult()
            except:
                try:
                    ia = IndividualAgreement.individualAgreement( Gmail, filemanager, Drive,I)
                    li= ia.ReportResult()
                except:
                    li = [I,mess.getSubject(),mess.getFullName(),mess.getEmailAddress(),mess.getCountryName(), None, None, None,None,None,mess.getPlatform()]
                    print('failed')
            print(li)
            GS.updateInformation([li])
            ProcessedID.append(I)

    
    
if __name__ == '__main__':
    main()