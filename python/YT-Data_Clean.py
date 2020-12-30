import sqlite3
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import xlrd
from collections import Counter
from matplotlib import pyplot as plt
import collections
import emoji
from matplotlib.font_manager import FontProperties


# Displaying function which filters datframes and outputs Data Visuals
# Data visuals demonstrate stats on popular comments on target videoID on original 100 comments
def displayVisuals100():
    #INPUT
    file = pd.ExcelFile("YOUR PATH/Data/comments.xlsx")
    df = pd.read_excel("YOUR PATH/comments.xlsx")

    #Filter data for visual #1
    filter1 = df[(df.LIKES >= 1)]
    filter1 = filter1.sort_values(by=['LIKES'])

    # Subplot2grid utilized to display comment popularty
    plt.figure(figsize=(13,18))
    ax1 = plt.subplot2grid((15,1), (0,0), rowspan=5, colspan=1)
    ax1.tick_params(labelrotation=90)
    ax1.title.set_text('YouTube CommentThread Popularity')
    ax1.set(ylabel='Frequency [Likes]')
    ax1.bar(filter1.AUTHOR, filter1.LIKES, label='Comment Likes', color='steelblue')
    plt.margins(x=0)
    plt.grid(True)  
    plt.legend() 

    # Filtering for visual #2
    cols = [1,4,3]
    df2 = pd.read_excel(file, sheet_name='Comments', usecols= cols)
    df2 = df2[['AUTHOR', 'AUTHOR CHANNEL','LIKES']]
    # Filtering by ASC LIKES 
    filter2 = df2[(df.LIKES >= 1)]
    filter2 = filter2.sort_values(by=['LIKES'], ascending=False).head(10)
    filter3 = filter2.drop(columns=['LIKES'])

    # Top 10 Table
    ax2 = plt.subplot2grid((15,1), (10,0), rowspan=5, colspan=1)
    colors = ['steelblue','steelblue']
    ax2.axis('tight')
    ax2.axis('off')
    table = ax2.table(cellText=filter3.values,colLabels=filter3.columns,
                    loc="center", label='Top 10', 
                    cellLoc='center', colWidths= [.5, .6],
                    colColours=colors)
    # Table customization
    cell1 = 1
    while cell1 < 11:
        table[(cell1,1)].set_facecolor("white")
        cell1 +=1
     
    cell2 = 1
    while cell2 < 11:
        table[(cell2,0)].set_facecolor("white")
        cell2+=1

    # Display Table    
    ax2.set_title('Top 10 Authors')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2) 
    plt.savefig('YOUR PATH/popularity_100.png')

# This function contains two options to retrieve comments
# First option uses SQL to retrieve comments with specific KEYWORDS
# Second option retrieves all commentThreads (copy) to avoid altering original Data
def keywordSearch():
    # INPUT
    file = "/YOUR PATH/comments.xlsx"
    # OUTPUT
    output = pd.ExcelWriter("YOUR PATH/comments_filtered.xlsx", engine='xlsxwriter')

    # Creating sql engine to use SQL/reading Excel sheets
    engine = create_engine('sqlite://', echo=False)
    df = pd.read_excel(file, sheet_name='Comments')

    # Creating Table to extract data
    df.to_sql('Comments', engine, if_exists='replace', index=False)

    
    # [OPTION 1] Query1 - Using SQL to create new file with only comments containing desired keywords
    q1 = engine.execute("Select AUTHOR, COMMENT, LIKES, [AUTHOR CHANNEL], DATE \
                        FROM Comments \
                        WHERE COMMENT LIKE '%biden%' \
                        OR COMMENT LIKE '%covid%' \
                        OR COMMENT LIKE '%vaccine%' \
                        OR COMMENT LIKE '%trump%' \
                        OR COMMENT LIKE '%stimulus%' \
                        OR COMMENT LIKE '%Fraud%' \
                        ")
    '''
    # [OPTION 2] Making copy of original excel sheet
    q1 = engine.execute(" Select AUTHOR, COMMENT, LIKES, [AUTHOR CHANNEL] \
                        FROM Comments \
                        ")'''
    # Transfer Data
    data1 = pd.DataFrame(q1, columns = ['AUTHOR', 'COMMENT', 'LIKES', 'AUTHOR CHANNEL', 'DATE'])
    data1.to_excel(output, sheet_name='Comments')
    output.save()

# Function containing multiple Algorithms to parse/clean commentThread() Data
# Results are transferred to excel sheets using Dataframes (Data is overwritten by popularKeywords() to avoid redundancy)
def parseWords():
    # INPUT
    file = "YOUR PATH/comments_filtered.xlsx" 
    # OUTPUT
    output = pd.ExcelWriter("YOUR PATH/word_occurence.xlsx", engine='xlsxwriter')

    # Special Characters to be removed
    bad_chars = [';', ':', '!', "*", '.', ',', '"', '?']

    # Retrieve comments for keyword frequencies
    cols = [2]
    df = pd.read_excel(file, sheet_name='Comments', usecols= cols)

    #Convert [COMMENT] column to list
    comList = df['COMMENT'].to_list()

    # Temp Data placements
    wordlist = []
    newString = ''

    # Iterate and seperate words(by list)
    for line in comList:
        line = line.split(' ') 
        for word in line:
            words = word.split(' ')
            wordlist.append(words)

    # Converting words into strings
    for x in wordlist:
        newString += " "
        for word in x:
           newString += word

    # Remove undesired chars from newString
    for x in bad_chars:
        for y in newString:
            newString = newString.replace(x, ' ')

    # Replace list with newString
    wordlist = newString.split()
   
    # Counter Dictionary
    x = Counter(map(str.lower, wordlist))

    # Dataframe
    data1 = pd.DataFrame.from_dict(x, orient= 'index')
    data1.columns = ['FREQUENCY']
    data1.to_excel(output, sheet_name='OCCURENCE')

    output.save()

    
# Final filtering process on target sheets with commentThread Data
# Overwrite word_occurence.xlsx Data to avoid redundancy.    
def popularKeywords():
    # INPUT FILES
    file1 = "/YOUR PATH/word_occurence.xlsx"
    file2 = pd.ExcelFile("/YOUR PATH/comments_filtered.xlsx")
    # OUTPUT FILES
    output = pd.ExcelWriter("YOUR PATH/word_occurence.xlsx", engine='xlsxwriter')

    df1 = pd.read_excel(file1, sheet_name='OCCURENCE')
    df2 = pd.read_excel(file2, sheet_name='Comments')

    # Filtering Data in Dataframe(word occurences)
    filter1 = df1[(df1.FREQUENCY >= 2)]
    filter1 = filter1.sort_values(by=['FREQUENCY'])
    filter1.columns = ['KEYWORD', 'FREQUENCY']
    filter1.to_excel(output, sheet_name='OCCURENCE', index=False)

    # Filtering Data for comment data
    cols = [2,3]
    df2 = pd.read_excel(file2, sheet_name='Comments', usecols= cols)
    df2 = df2[['COMMENT','LIKES']]

    filter2 = df2[(df2.LIKES >= 1)]
    filter2 = filter2.sort_values(by=['LIKES'], ascending=False).head(10)
    filter3 = filter2.drop(columns=['LIKES'])

    # Subplot2grid utilized to display word frequency on keyword search
    plt.figure(figsize=(14,12))
    ax1 = plt.subplot2grid((14,1), (0,0), rowspan=6, colspan=1)
    ax1.bar(filter1.KEYWORD, filter1.FREQUENCY, label='Word #', color='red')
    ax1.tick_params(labelrotation=90)
    ax1.title.set_text('Word Popularity')
    ax1.set(ylabel='Frequency')
    plt.margins(x=0)
    plt.grid(True) 

    # Data Visual (Comment Table)
    ax2 = plt.subplot2grid((14,1), (8,0), rowspan=7, colspan=1)
    colors = ['red','red']
    ax2.axis('tight')
    ax2.axis('off')
    table = ax2.table(cellText=filter3.values,colLabels=filter3.columns,
                    loc="center", label='Top 10', 
                    cellLoc='center',
                    colColours=colors)
    # Display Table    
    ax2.set_title('Top Comments')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1.3, 2.5) 
    plt.savefig('YOUR PATH/filtered_comments.png')
    
    output.save() 

def main():
    # Invoke all methods
    keywordSearch()
    parseWords()
    popularKeywords()
    displayVisuals100()

    print('-----------Comment Analysis Complete----------')

main()
