'''
Script to get the stats of each player in draft.csv
'''
import requests
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
url = "https://google.com/search?q="
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
stats = "stats.csv"
sites = "urls.txt"


# Function to write to a CSV file

def writeCSV(csvFile, name, gp, gs, minutes, ppg, fga, fgm, fgp, thpa, thpm, thp, fta, ftm, ftp,
reb, dreb, oreb, assist, turnover, steals, blcks, fouls):
    with open(csvFile, 'a') as saveToCsv:
        fw = csv.writer(saveToCsv, quoting=csv.QUOTE_MINIMAL)
        # write each player on own row
        fw.writerow([name, gp, gs, minutes, ppg, fga, fgm, fgp, thpa, thpm, thp,
        fta, ftm, ftp, reb, dreb, oreb, assist, turnover, steals, blcks, fouls])

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
df = pd.read_csv("draft.csv", encoding="ISO-8859-1")
names = df['Player']
'''
# Make list to store urls to check
urls = [[] for _ in range(len(names))]
# Search for each player
for i, name in enumerate(names):
    # Check if already written first last
    if "," not in name:
        n = name.split(" ")
        if len(n) > 1:
            newname = n[0] + "+" + n[1]
    else: # written last, first
        newname = name.replace(" ", "")
        newname = newname.split(",")
        if len(newname) > 1:
            newname = newname[1] + "+" + newname[0]
    newname = newname + "+realgm" + "+summary" # to guarantee we'll get the stats page

    r = requests.get(url+newname, headers)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.find_all('h3', attrs ={'class': 'r'}, limit=1):
        splt = item.a['href'][7:]
        urls[i].append(splt.split("&")[0])
    print(urls[i])

# Just to see how long it takes to do the above
print("Program finished in {} seconds".format(round(time.time() - start_time, 2)))
'''
i = 0
# Open and store the html
websites = open(sites)

while 1:
    site = websites.readline()
    if not site: break
    # site.
    html = urlopen(site)
    bsObj = BeautifulSoup(html, "lxml")
    # Get first table
    try:
        header = bsObj.findAll("h2")[2]
        if header.get_text() == 'NBA Regular Season Stats - Totals':
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

                    # Write stats to the csv file
                    writeCSV(stats, names[i], played[0], started[0], minutes[0], points[0], fgattempt[0], fgmade[0], fgpercent[0],
                    three_attempt[0], three_made[0], three_percent[0], free_attempt[0],free_made[0], free_percent[0], allboards[0],
                    dboards[0], oboards[0], assists[0], turnovers[0], steals[0], blocks[0], fouls[0])

        # No statistics available (didn't play in league)
        else:
            writeCSV(stats, names[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    except IndexError:
        writeCSV(stats, names[i], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # Reset statistics
    played[:] = []
    started[:] = []
    minutes[:] = []
    fgmade[:] = []
    fgattempt[:] = []
    fgpercent[:] = []
    three_made[:] = []
    three_attempt[:] = []
    three_percent[:] = []
    free_made[:] = []
    free_attempt[:] = []
    free_percent[:] = []
    oboards[:] = []
    dboards[:] = []
    allboards[:] = []
    assists[:] = []
    steals[:] = []
    blocks[:] = []
    fouls[:] = []
    turnovers[:] = []
    points[:] = []
    i+= 1 #to increment the name we're on


print("Program finished in {} seconds".format(round(time.time() - start_time, 2)))
