# YouTube Comment Analysis: Project Overview
Repo for YouTube comment Analysis using YouTube API


- CommentThread resource is used to retrieve Youtube comment data with various attributes on target video.
- List by videoID function is used as main API function with desired parameters.
- Comments are analyzed based on a limited value of 100.
- Target videoID's can be filtered by SQL functionality [optional].
- Main purpose of this project is to isolate comments & word usage to log popular words or trending strings per videoID.
- Emoji frequency is also logged on target videoID.
 
 # Code & Resources 
 #### Python Version: 3.7
 #### YouTube data API : https://developers.google.com/youtube/v3/docs/commentThreads/list
 #### Packages: pandas, sqlite3, collections, emoji
  
 # YouTube Data API:
  - Various attributes are pulled by iterating through nested dictionary located in API response.
  - YouTube parsing function is used to pull [comments, author, author channel, likes, dates] from comment thread.
  - YouTube commentThreads() API function called with specific parameters to satisfy project goals.
  - *API key required to use YouTube Data API functionality.*
  
# SQL: Keyword functionality [Optional Feature]
  - Optional SQL functionality which queries.
  - Format consists of **[COMMENT LIKE '%KEYWORD%]**
    - This SQL query may conatin multiple Keywords an filter commentThread response further.
  - Default SQL query retrieves all attributes/columns from **comments.xlsx** containing target video data.
  
# Data Cleaning & Filtering: Parsing comments Algorithm
  - Array data Structures utilized to manipulate and organize commentThreads
  - Occurences logged for commentThreads while omitting special characters **[';', ':', '!', "*", '.', ',', '" "', '?']**.
  - Comment emojis along with frequencies are logged using **UNICODE_EMOJI**.
  
# Excel & Dataframes: Data Storage/Results
  - **word_occurence.xlsx** contains all cleaned/parsed comment data, leaving original data unchanged in **comments.xlsx**.
  - **word_occurence.xlsx** is overitten by popularKeywords() with new sheet containing FREQUENCY condition.


## Demonstration of data visuals by comparing touchdowns and sacks

