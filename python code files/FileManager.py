# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:18:17 2018

@author: Administrator
"""

import os
from os import access, R_OK
import shutil


class fileManager(object):
    def __init__(
        self, 
        baseDir
    ):
        '''
        Make sure baseDir has the proper structure. Save baseDir. 
        '''
        if not baseDir.endswith('/'):
            baseDir = baseDir + "/"
        if not os.path.exists( baseDir ):
            raise Exception( "%s does not exist" % baseDir )
        if( not access( baseDir, R_OK ) ):
            raise Exception( "You don't have access to directory %s" % baseDir )
        self._baseDir = baseDir
        

        
    def FormatName(self,emailname):
        for filename in os.listdir(self._baseDir+emailname):
            extension = os.path.splitext(filename)[1]
            if 'ndividual' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'Individual Agreement'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                     os.remove(self._baseDir+emailname+'/'+filename)
                     print('File '+emailname+'-'+'Individual Agreement'+extension+' exists.')
            if 'orporate' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'Corporate Agreement'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                     os.remove(self._baseDir+emailname+'/'+filename)
                     print('File '+emailname+'-'+'Corporate Agreement'+extension+' exists.')
            elif 'signature' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'Signature'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                     os.remove(self._baseDir+emailname+'/'+filename)
                     print('File '+emailname+'-'+'Signature'+extension+' exists.')
                
            elif 'ack' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'ID-Back'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'ID-Back'+extension+' exists.')
                
                
            elif 'ddress' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'ProofAddress'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'ProofAddress'+extension+' exists.')
                
                
                
            elif 'POA' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'POA'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'POA'+extension+' exists.')
                
                
                
            elif 'dentity'in filename and 'Mind' not in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'ID'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'ID'+extension+' exists.')
                
                
                
            elif 'icense' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'ID'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'ID'+extension+' exists.')
                
                
            elif 'assport' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'ID'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'ID'+extension+' exists.')
            
            elif 'ID' in filename:
                newfilepath = self._baseDir+emailname+'/'+emailname+'-'+'ID'+extension
                if not os.path.exists( newfilepath ):
                    os.rename(self._baseDir+emailname+'/'+filename,newfilepath)
                else:
                    os.remove(self._baseDir+emailname+'/'+filename)
                    print('File '+emailname+'-'+'ID'+extension+' exists.')
                
                
                
            else:
                print('Need to change name manully')
                print(filename)
            
    def getAllClient(self):
        return os.listdir(self._baseDir)
    

    def getAttachments(self,foldername): 
        if not os.path.exists(self._baseDir+foldername):
            raise Exception( "%s does not exist" % (self._baseDir+foldername) )
        else:
            return os.listdir(self._baseDir+foldername)
            
    def getbaseDir(self):
        return self._baseDir
    
    
    def getIDfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'ID.' in filename:
                return filename
        
        return False
    
    def getIndividualAgreementfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'ndividual' in filename:
                return filename
        return False
    def getSignaturefilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'ignature' in filename:
                return filename
        return False
    def getIDBackfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'ack' in filename:
                return filename
        return False
    def getAddressfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'ddress' in filename:
                return filename
        return False
    def getPOAfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'POA' in filename:
                return filename
        return False
    def getIMfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'Mind' in filename:
                return filename
        return False
    
    def getWCfilename(self,foldername):
        for filename in self.getAttachments(foldername):
            if 'Check' in filename:
                return filename
        return False
    def removeFolder(self,foldername):
        shutil.rmtree(self.getbaseDir()+foldername)