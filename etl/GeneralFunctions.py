# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata
# Daniel Steinemann
# Angel Angel

from typing import Optional

def getGroupIds() -> dict:
    """From a Google Sheet gets data from groups, this is part of another module in this project
    This is a javaScript project on a Node.js (API as a gateway in Gsheets)
    https://docs.google.com/spreadsheets/d/123rWmGspi0CG6VMvIkUkVEL6j9vNmEp7S6TQDkR6hNs/edit#gid=0

    Returns:
        (dict)
    """
    import requests
    
    jira_reference = {}

    for i in requests.get('https://jira-res-app-q5uprh6tba-uc.a.run.app/groupsids').json()['data']['data'][1:]:
        lst =list(i.values())
        jira_reference[lst[0]] = lst[1]
    
    return jira_reference

def decoratorGetUserName(function):
    def wrapper():
        from os import environ
        return environ.get('USERNAME')
    return wrapper
#@decoratorGetUserName
def getUserName()->str:
    """Returns the email provided by your ServiceNow user this is needed to execute locally when deployed the decorator
       needs to be activated.  
    
    Arguments:
        None
    Returns: 
        (str)
    """
    return '' # Add your own creds if running locally

def decoratorGetPassword(function):
    def wrapper():
        from os import environ
        return environ.get('PASSWORD')
    return wrapper
#@decoratorGetPassword
def getPassword()->str:
    """Returns the password provided by your ServiceNow user this is needed to execute locally when deployed the decorator
       needs to be activated. 
    
    Arguments:
        None
    Returns: 
        (str)
    """
    return '' # Add your own creds if running locally

def decoratorGetPath(function):
    def wrapper(file_name:str):
        from pathlib import Path
        return Path('/tmp', file_name)
    return wrapper
#@decoratorGetPath
def getPath(file_name:str):
    """Getting the local Path, deactivate decorator for local testing
    Arguments:
        file_name {str} -- my_file.csv
    Returns:
        Path
    """
    from os import getcwd
    from pathlib import Path
    return Path(getcwd(), file_name)

def convertToCSV(df, group_id)->str:
    """Convers a pandas DataFrame to a CSV
    
    Arguments:
        df (DataFrame): Pandas Dataframe
        group_id (str): Group id from API Google Sheet
    Returns: 
        str: file_full_path
    """
    from csv import QUOTE_ALL
    import datetime
    from datetime import date
    
    file_name = '{id}_{year}_{month}_{day}.csv'.format(id=group_id, year=date.today().year, month=date.today().month, day=date.today().day)
    file_full_path = getPath(file_name)

    df.to_csv(file_full_path, header=True, index=False, sep=',', quoting=QUOTE_ALL, escapechar = ' ')

    return file_full_path

def send_to_bucket(file_full_path:str)->None:
    """Uploads an object/file to a GCP bucket Example: app-script-data-extraction-output/tsheets/myfile.csv
    Arguments:
        file_full_path (str): String for the the file full path
    Returns: 
        None
    """
    from google.cloud import storage
    from os.path import basename

    file_name = basename(file_full_path) 

    dictionary = {'bucketName': 'app-dataengineering',
                  'destination_blob_name': f'jira_servicenow/{file_name}',
                  'source_file_name': f'{file_full_path}'}
    storage_client = storage.Client()
    storage_client.get_bucket(dictionary['bucketName']).blob(dictionary['destination_blob_name'])\
        .upload_from_filename(dictionary['source_file_name'])


