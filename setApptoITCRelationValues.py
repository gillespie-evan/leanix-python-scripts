#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 09:41:06 2019

@author: evangillespie
"""

# INIT - Authorization/API Token
# Step 1 Load CSV into a dataframe - need Factsheet IDs
# Step 2 Retrieve ITC to Application information
# Step 3 Add cost to the correct ITCtoAppliction Relation

import json 
import requests 
import pandas as pd
from pandas.io.json import json_normalize


# Import csv as a pandas dataframe object
df = pd.read_csv('data.csv')

#remove top header row that contains "friendly" labels
df = df.iloc[1:, :]

api_token = 'INSERT API TOKEN'
auth_url = 'https://us.leanix.net/services/mtm/v1/oauth2/token' 
request_url = 'https://us.leanix.net/services/pathfinder/v1/graphql' 

# Get the bearer token - see https://dev.leanix.net/v4.0/docs/authentication

response = requests.post(auth_url, auth=('apitoken', api_token),
                         data={'grant_type': 'client_credentials'})
response.raise_for_status() 
access_token = response.json()['access_token']
auth_header = 'Bearer ' + access_token
header = {'Authorization': auth_header}

def call(query):
  data = {"query" : query}
  json_data = json.dumps(data)
  response = requests.post(url=request_url, headers=header, data=json_data)
  response.raise_for_status()
  return response.json()

# Get the relationship IDs

def getRelations():
  query = """
  {
  allFactSheets(factSheetType: ITComponent) {
    edges {
      node {
        ... on ITComponent {
          id
          name
          relITComponentToApplication {
            edges {
              node {
                id
                factSheet{
                  id
                  name
                }
                costTotalAnnual
              }
            }
          }
        }
      }
    }
  }
}
  """
  response = call(query)
  df = pd.DataFrame.from_dict(response['data']['allFactSheets']['edges'])
  dfX = pd.DataFrame.from_records(response['data']['allFactSheets']['edges'])
  for index, row in dfX.iterrows():
      print(index, " : ",row, "\n")
      print("ITC ID:" + row['node']['id'])
      print(row['node']['relITComponentToApplication'])
      print("\n")
  
"""  
  apps = {}
  for row in response['data']['allFactSheets']['edges']:
    appId = appNode['node']['id']
    apps[appId] = {}
    for relationNode in appNode['node']['relApplicationToITComponent']['edges']:
      relationId = relationNode['node']['id']
      itcId = relationNode['node']['factSheet']['id']
      apps[appId][itcId] = relationId
  return apps
"""
