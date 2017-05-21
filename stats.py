'''
Script to get the stats of each player in draft.csv
Takes about an hour and 15 minutes to run
'''
import requests
import csv
from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
import time
import pandas as pd
import sys

# Globals
start_time = time.time()
# So we don't look like the robot we are
#headers = {'user-agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
# 'Totally not a robot', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html',
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'}#,
# 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0']}
# headers = {'user-agent': 'my internets'}
website = 'http://basketball.realgm.com/'

# Function to write to a CSV file MODIFY LATERZ
def writeStats(csvFile, player_stats):
    with open(csvFile, 'r') as f:
        lines = list(csv.reader(f))
    # Add the stats to the end of each player row
    for i, row in enumerate(lines[1:]):
        row[7:] = player_stats[i]
    # Over write with appending data
    with open(csvFile, 'w') as f:
        csv.writer(f).writerows(lines)

# Get names of players in draft file
def getPlayerNames():
    try:
        print("Please enter the name of the csv file we'll append the stats to ")
        csvFile = input(">>> ")
        # Open the csv file and store players' names
        df = pd.read_csv(csvFile)
        names = df['Player']
        return names, csvFile
    except Exception as e:
        print(e)
        getCSV()

# Go through each site that we got from getUrls
def getStats(urlFile, players, csvFile):
    played = []
    started = []
    minutes = []
    fgmade = []
    fgattempt = []
    fgpercent = []
    three_made = []
    three_attempt = []
    three_percent = []
    free_made = []
    free_attempt = []
    free_percent = []
    oboards = []
    dboards = []
    allboards = []
    assists = []
    steals = []
    blocks = []
    fouls = []
    turnovers = []
    points = []
    websites = open(urlFile)
    player_stats = {}
    i = 0 # For indexing player name
    while 1:
        site = websites.readline()
        if not site: break
        html = urlopen(website+site)
        # r = requests.get(site, headers)
        # print(r.text)
        bsObj = BeautifulSoup(html, "lxml")

        try:
            hdr = bsObj.findAll("h2")[2]
            # Each table is led by this string if there's NBA stats available
            if hdr.get_text() == 'NBA Regular Season Stats - Totals':
                table = bsObj.findAll("table", {"class": "tablesaw compact"})[0]
                rows = table.findAll("tr", {"class": "career per_game"})

                for row in rows:
                    cells = row.findAll("td")
                    # Store stats
                    if len(cells) == 23:
                        played.append(cells[2].find(text=True))
                        started.append(cells[3].find(text=True))
                        minutes.append(cells[4].find(text=True))
                        fgmade.append(cells[5].find(text=True))
                        fgattempt.append(cells[6].find(text=True))
                        fgpercent.append(cells[7].find(text=True))
                        three_made.append(cells[8].find(text=True))
                        three_attempt.append(cells[9].find(text=True))
                        three_percent.append(cells[10].find(text=True))
                        free_made.append(cells[11].find(text=True))
                        free_attempt.append(cells[12].find(text=True))
                        free_percent.append(cells[13].find(text=True))
                        oboards.append(cells[14].find(text=True))
                        dboards.append(cells[15].find(text=True))
                        allboards.append(cells[16].find(text=True))
                        assists.append(cells[17].find(text=True))
                        steals.append(cells[18].find(text=True))
                        blocks.append(cells[19].find(text=True))
                        fouls.append(cells[20].find(text=True))
                        turnovers.append(cells[21].find(text=True))
                        points.append(cells[22].find(text=True))

                        # Store in dictonary of player stats
                        player_stats[i] = [played[0], started[0], minutes[0], points[0], fgattempt[0], fgmade[0], fgpercent[0],
                        three_attempt[0], three_made[0], three_percent[0], free_attempt[0],free_made[0], free_percent[0], allboards[0],
                        dboards[0], oboards[0], assists[0], turnovers[0], steals[0], blocks[0], fouls[0]]

            # No statistics available
            else:
                player_stats[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Error occured so just zero out the stats
        except Exception as e:
            print(e)
            player_stats[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        print("We just finished i: ", i)
        i += 1
        # Reset statistics
        played = []
        started = []
        minutes = []
        fgmade = []
        fgattempt = []
        fgpercent = []
        three_made = []
        three_attempt = []
        three_percent = []
        free_made = []
        free_attempt = []
        free_percent = []
        oboards = []
        dboards = []
        allboards = []
        assists = []
        steals = []
        blocks = []
        fouls = []
        turnovers = []
        points = []

    # write to csvFile
    writeStats(csvFile, player_stats)

# Function to get the name of the url text file
def getUrlTextFile():
    print("\nPlease enter the name of the text file with your urls")
    try:
        urlFile = input(">>> ")
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()
    if urlFile.endswith(".txt"): return urlFile
    else:
        print("Please enter a text file")
        getUrlTextFile()

def main():
    print("Let's get everyones stats!")
    # Get name of players
    players, draftFile = getPlayerNames()
    urlTxtFile = getUrlTextFile()
    # Now we'll go ahead and actually scrape through each site and get the stats
    getStats(urlTxtFile, players, draftFile)
    print("Program stored the urls in {} seconds".format(round(time.time() - start_time, 2)))

if __name__ == '__main__':
    main()
