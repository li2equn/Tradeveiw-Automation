# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:27:50 2018

@author: Administrator
"""

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import itertools
# =============================================================================
# from apiclient.http import MediaFileUpload
# from sys import exit
# =============================================================================

# =============================================================================
# from __future__ import print_function
# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
# =============================================================================


class googleSheet(object):
    def __init__(self,SPREADSHEET_ID = '1lXvOe2_-jx3TGeZ4WeBgQpXE0g4Cae2uwyTGowi2Fr8'):
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        store = file.Storage('token_googleSheet.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials_googleSheet.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self._service = build('sheets', 'v4', http=creds.authorize(Http()))
        self._SPREADSHEET_ID = SPREADSHEET_ID
        
        
    def updateInformation(self,values):
        
        body = {
            'values': values
        }
        range_name = 'A:L'
        result = self._service.spreadsheets().values().append(
            spreadsheetId=self._SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW',
            body=body).execute()
        #
        print('{0} cells appended.'.format(result \
                                               .get('updates') \
                                               .get('updatedCells')));
    def ReadProcessedID(self):
        range_name = 'A2:A192000'
        
        request = self._service.spreadsheets().values().get(spreadsheetId=self._SPREADSHEET_ID, range=range_name, valueRenderOption='FORMATTED_VALUE', dateTimeRenderOption='FORMATTED_STRING')
        response = request.execute()
        
        # TODO: Change code below to process the `response` dict:
        l_of_l = response['values']
        all_IDs = list(itertools.chain.from_iterable(l_of_l))
        return all_IDs