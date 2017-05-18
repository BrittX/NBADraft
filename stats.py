'''
Script to get the stats of each player in draft.csv
'''
from google import search
import csv
import pandas as pd
from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
import time
# Globals
start_time = time.time()
played = []
started = []
minutes = []
fgmade = []
fgattempt = []
fgpercent
three_made = []
three_attempt = []
three_percent. = []
free_made. = []
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
stats = "stats.csv"

'''
Function to write to a CSV file
'''
def writeCSV(csvFile, name, gp, gs, minutes, ppg, fga, fgm, fgp, thpa, thpm, thp, fta, ftm, ftp,
reb, dreb, oreb, assist, turnover, steals, blcks, fouls):
    with open(csvFile, 'a') as saveToCsv:
        fw = csv.writer(saveToCsv, quoting=csv.QUOTE_MINIMAL)
            # write each player on own row
            fw.writerow([name, gp, gs, minutes, ppg, fga, fgp, thpa, thpm, thp, fta, ftm,
            ftp, reb, dreb, oreb, assist, turnover, steals, blcks, fouls)

# Function to write that initial header row
def writeHeader(csvFile):
    with open(csvFile, 'wt') as saveToCsv:
        fw = csv.writer(saveToCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fw.writerow(['Player', 'Games Played', 'Games Started', 'Minutes', 'Points Per Game', 'FGA', 'FGM',
        'FG%', '3PA', '3PM', '3P%', 'FTA', 'FTM', 'FT%', 'Rebounds', 'DBoards', 'OBoards', 'Assists', 'Turnovers',
        'Steals', 'Blocks', 'Fouls'])


# Write the initial header
writeHeader(stats)

# Read and store each name in csv file
df = pd.read_csv("draft.csv")
names = df['Player']
# Make list to store urls to check
urls = [[] for _ in range(len(names))]
# Search for each player
for i, name in enumerate(names):
    for url in search(name + 'realgm', stop=3):
        urls[i].append(url)

# Only take first results of each url
for url in urls:
    del url[1:]
print(urls)

print("Program finished in {} seconds".format(round(time.time() - start_time, 2)))

# Open and store the html
for site in url:
    html = urlopen(site)
    bsObj = BeautifulSoup(html, "lxml")
    # Get first table
    table = bsObj.findAll("table", {"class": "tablesaw compact"})[0]
    rows = table.findAll("tr", {"class": "career per_game"})

    for row in rows:
        cells = row.findAll("td")
        # Store stats
        if len(cells) == 22:
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
            points.append(cells[21].find(text=True))

            writeCSV(stats, name[i], played[0], started[0], minutes[0], points[0], fgattempt[0], fgmade[0], fgpercent[0], three_attempt[0], three_made[0], three_percent[0], free_attempt[0],
            free_made[0], free_percent[0], allboards[0], dboards[0], oboards[0], assists[0], turnovers[0], steals[0], blocks[0], fouls[0]):

print("Program finished in {} seconds".format(round(time.time() - start_time, 2)))
