import os
import googleapiclient.discovery
import googleapiclient.errors
import json
import pandas as pd
import xlsxwriter
import time
import MySQLdb as sql_db

# API KEY
api_key = 'AIzaSyBzDwpMmJY5ZJ_UdRKsiF5oB8E7gGMoVZs'

# Target Video
VIDEO = "Jq7AexEUFHM"

# key/column List
comment = []
author = []
authorChannel = []
likes = []
dates = []

# Cleaning/Parsing JSON data converted into dictionary data structure
# Collecting target values from youtube video metadata
def parseYTComments(response):
    for x in response['items']:
        #add comment to list
        comment.append(x['snippet']['topLevelComment']['snippet']['textOriginal'])
        #add user name to list
        author.append(x['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        #add user channel to list
        authorChannel.append(x['snippet']['topLevelComment']['snippet']['authorChannelUrl'])
        #add # of likes per comment
        likes.append(x['snippet']['topLevelComment']['snippet']['likeCount'])
        #add dates
        dates.append(x['snippet']['topLevelComment']['snippet']['publishedAt'])

# Dumping collected attributes into excel sheet for further filtering.
def transferToExcel(col1, col2, col3, col4, col5):
    dataToExcel = pd.ExcelWriter("C:/Users/melen/desktop/PORTFOLIO/YouTube_Project/Data/comments.xlsx", engine='xlsxwriter')
    data = pd.DataFrame({'AUTHOR': col1,'COMMENT': col2,'LIKES':col3,'AUTHOR CHANNEL': col4, 'DATE': col5})
    data.to_excel(dataToExcel, sheet_name='Comments')
    dataToExcel.save()
    
def main():
    
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    #Variables
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    #API Function/100 comments
    request = youtube.commentThreads().list(part="snippet", videoId = VIDEO, maxResults=100, 
                order='relevance')
    response = request.execute()

    # Invoke parsing on JSON response
    parseYTComments(response)
    # Invoke dataframe
    transferToExcel(author, comment, likes, authorChannel, dates)

    print('-----------Comments Retrieved----------')

# Invoke main()
if __name__ == "__main__":
    main()



