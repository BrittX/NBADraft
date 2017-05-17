from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
import time
import sys
# Globals
start_time = time.time()
rnd = []
pick = []
player = []
position = []
team = []
school = []
# urls with wikitable sortable
picky_urls = ["2003_NBA_draft", "1996_NBA_draft", "1995_NBA_draft",
"1994_NBA_draft", "1993_NBA_draft"]
# split into two tables/both sortable sortable
super_picky = ["1992_NBA_draft", "1990_NBA_draft", "1989_NBA_draft", "2004_NBA_draft", "2002_NBA_draft", "2001_NBA_draft"]
# sortable sortable but need to get [0] and [1]
# omg_why = ["1987_NBA_draft"]

def getPicky(endingUrl, saveToCsv, year):
    html = urlopen("https://en.wikipedia.org/wiki/"+endingUrl)
    bsObj = BeautifulSoup(html, "lxml")
    pass


# Get HTML table and write to CSV file
def getTable(endingUrl, saveToCsv, year):
    print(endingUrl)
    html = urlopen("https://en.wikipedia.org/wiki/"+endingUrl)
    bsObj = BeautifulSoup(html, "lxml")
    # Get the table of draft pics
    if endingUrl in picky_urls:
        try:
            table = bsObj.findAll("table", {"class": "wikitable sortable"})[0]
            rows = table.findAll("tr")
        except:
            print("Something wrong with file ", endingUrl)
            sys.exit()
    else:
        try:
            table = bsObj.findAll("table", {"class": "wikitable sortable sortable"})[0]
            rows = table.findAll("tr")
        except:
            print("Something wrong with file ", endingUrl)
            sys.exit()

    for row in rows:
        # print(row)
        cells = row.findAll("td")
        # print("These are cells: ", cells)
        if len(cells) == 7:
            rnd.append(cells[0].find(text=True))
            pick.append(cells[1].findAll(text=True))
            player.append(cells[2].find(text=True))
            # print(player)
            position.append(cells[3].findAll(text=True))
            team.append(cells[5].find(text=True))
            school.append(cells[6].find(text=True))
        # Some pages don't have position or round
        elif len(cells) == 5:
            # rnd.append(cells[0].find(text=True))
            pick.append(cells[0].findAll(text=True))
            player.append(cells[1].find(text=True))
            team.append(cells[3].find(text=True))
            school.append(cells[4].find(text=True))
    writeCSV(saveToCsv, year, rnd, pick, player, position, team, school)
    # Reset cells
    rnd[:] = []
    pick[:] = []
    player[:] = []
    position[:] = []
    team[:] = []
    school[:] = []
        # print("\nThis is a row", row.get_text())
        # for cell in row.findAll(['td', 'th']):
            # print("\nThis is a cell: ", cell.get_text())

    print("We just finished ", endingUrl)

'''
Function to write to a CSV file
'''
def writeCSV(csvFile, year, rnd, picks, players, positions, team, prevTeam):
    with open(csvFile, 'a') as saveToCsv:
        fw = csv.writer(saveToCsv, quoting=csv.QUOTE_MINIMAL)
        for num in range(len(rnd)):
            # write each player on own row
            fw.writerow([year, rnd[num], picks[num][0], players[num], positions[num][0], team[num], prevTeam[num]])

# Function to write that initial header row
def writeHeader(csvFile):
    with open(csvFile, 'wt') as saveToCsv:
        fw = csv.writer(saveToCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fw.writerow(['Year', 'Round', 'Pick', 'Player', 'Position', 'NBA Team', 'Prev Team'])
    # print("We just finished ", endingUrl)

# Decrement the year and call getTable
def decrementYear(endingUrl):
    # Split and get the year out
    splt = endingUrl.split("_", 1)
    # Decrement the year
    year = int(splt[0]) - 1
    # Make it a regular string again
    newUrl = str(year) + "_" + splt[1]
    return newUrl

def main():
    startingYear = "2007_NBA_draft"
    year = 2007
    # startingYear = "2004_NBA_draft"
    # year = 2004
    saveDraft = "draft.csv"
    # Write the header
    writeHeader(saveDraft)
    stop = False
    # getTable(startingYear, saveDraft, year)
    # Make a call to get table

    while not stop:
        if startingYear == "1988_NBA_draft": stop = True
        if startingYear in super_picky:
            year-=1
            startingYear = decrementYear(startingYear)
            continue
        getTable(startingYear, saveDraft, year)
        year -=1
        startingYear = decrementYear(startingYear)

    print("Program finished in {} seconds".format(round(time.time() - start_time, 2)))

if __name__ == '__main__':
    main()
