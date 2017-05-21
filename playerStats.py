'''
Script to get the stats of each player in draft.csv
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
gSearch = "https://google.com/search?q="
# So we don't look like the robot we are
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# headers = {'user-agent': 'my internets'}
urlTxtFile = 'draft.txt'

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

# Get the urls to seach the stats of each player
def getUrls(playerNames):
    # Make list to store urls to check
    urls = [[] for _ in range(len(playerNames))]
    for i, name in enumerate(playerNames):
        if i == len(playerNames)/2: print("we're halfway there")
        term = name.replace(" ", "+")
        # Update teh search term so it's "'player name' player profile realgm"
        term = term + "+player+profile+realgm"

        # Concat with search url and add our headers
        r = requests.get(gSearch+term, headers)
        soup = BeautifulSoup(r.text, "html.parser")
        # Search for the link to the first result
        for item in soup.find_all('h3', attrs ={'class': 'r'}, limit=1):
            splt = item.a['href'][7:]
            # Get rid of the trailing letters to store just the url
            urls[i].append(splt.split("&")[0])
            print(urls[i])
    # Write urls to txt file so user doesn't have to scrape each time
    urlFile = getUrlFile()
    storeUrls = writeUrls(urls, urlFile)
    return storeUrls

# Write the urls to the text file
def writeUrls(statSites, urlFile):
    try:
        uF = open(urlFile, 'w+')
        for site in statSites:
            print(site)
            for actualSite in site:
                print(actualSite)
                uF.write(actualSite)
                uF.write('\n')
        uF.close()
        return urlFile
    except Exception as e:
        print(e)
        # Get new url file
        newFile = getUrlFile()
        writeUrls(statSites, newFile)


# Prompt user for text file to store corresponding urls for each player
def getUrlFile():
    try:
        print("Please enter a text file to store the urls for the stats")
        textFile = input(">>> ")
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()
    # Make sure it's a .txt file
    if textFile.endswith(".txt"): return textFile
    else:
        print("Please enter a file ending in .txt")
        writeUrls()

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
    print(websites)
    player_stats = {}
    i = 0 # For indexing player name
    while 1:
        site = websites.readline()
        if not site: break
        html = urlopen(site)
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
#Function to determine if we need to scrape to get the urls or
# user already has them stored
def scrape_stat_urls():
    print("\n Please choose one of the options below: ")

    print("\n1. I don't have a text file for all the urls")
    print("2. I already have the urls ready to go")
    try:
        selection = int(input(">>> "))
    except ValueError:
        print("Please choose one of the options above")
        scrape_stat_urls()
    if selection in range(1,3): return selection
    else:
        print("Please choose either option 1 or option 2")
        scrape_stat_urls()
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
    choice = scrape_stat_urls()
    if choice == 1:
        # Get the urls
        urlTxtFile = getUrls(players)
        # Just to see how long it takes to do the above
        print("Program stored the urls in {} seconds".format(round(time.time() - start_time, 2)))
    elif choice == 2:
        urlTxtFile = getUrlTextFile()
    # Now we'll go ahead and actually scrape through each site and get the stats
    getStats(urlTxtFile, players, draftFile)
    print("Program stored the urls in {} seconds".format(round(time.time() - start_time, 2)))

if __name__ == '__main__':
    main()
