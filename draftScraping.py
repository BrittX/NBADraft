'''
Prompt user for NBA draft years to scrape as well as a csv file where the results
will be stored. Works for years [1975, Current Year - 1]

'''

from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
import time
import sys
import datetime
import requests

# Globals
start_time = time.time()
today = datetime.datetime.now()
rnd = []
pick = []
player = []
position = []
team = []
school = []
url = "https://basketball.realgm.com/nba/draft/past_drafts/"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

# urls with wikitable sortable
saveToCsv = 'draft.csv'


# Function to get draft info from basketball.realgm
def getPicky(year, saveToCsv):
    # Get web page of that draft year
    r = requests.get(url+str(year), headers)
    bsObj = BeautifulSoup(r.text, "html.parser")

    # Find all instances of the table we're looking for
    table = bsObj.findAll("table", {"class": "tablesaw"})
    # Set our our rows to be equal to each tables' row
    numTables = len(table)
    # Setting the rows from each table in a list
    rows = [[] for _ in range(numTables)]
    for t in range(numTables):
        rows[t] = table[t].findAll("tr")
    # Get each row for the specific player
    for tableNum in range(numTables):
        for row in rows[tableNum]:
            cells = row.findAll("td")
            # We're looking at the actual picks in the draft
            if len(cells) == 12:
                rnd.append(tableNum+1)
                pick.append(cells[0].find(text=True))
                player.append(cells[1].find(text=True))
                team.append(cells[2].find(text=True))
                position.append(cells[4].find(text=True))
                school.append(cells[9].find(text=True))
            # These people went undrafted
            if len(cells) == 9:
                rnd.append(0) # Set round/pick equal to zero for undrafted
                pick.append(0)
                player.append(cells[0].find(text=True))
                team.append("None")
                position.append(cells[1].find(text=True))
                school.append(cells[6].find(text=True))
        # Write to our csv file (probably use pandas next time)
        writeCSV(saveToCsv, year, rnd, pick, player, position, team, school)
        # Reset everything
        rnd[:] = []
        pick[:] = []
        player[:] = []
        position[:] = []
        team[:] = []
        school[:] = []
    print("We just finished ", year)
    # except Exception as e:
        # print(e)
        # sys.exit()
'''
Function to write to a CSV file
'''
def writeCSV(csvFile, year, rnd, picks, players, positions, team, prevTeam):
    with open(csvFile, 'a') as saveToCsv:
        fw = csv.writer(saveToCsv, quoting=csv.QUOTE_MINIMAL)
        for num in range(len(rnd)):
            # write each player on own row
            fw.writerow([year, rnd[num], picks[num], players[num], positions[num], team[num], prevTeam[num]])

# Function to write that initial header row
def writeHeader(csvFile):
    with open(csvFile, 'wt') as saveToCsv:
        fw = csv.writer(saveToCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        fw.writerow(['Year', 'Round', 'Pick', 'Player', 'Position', 'NBA Team', 'Prev Team', 'Games Played', 'Games Started', 'Minutes', 'Points Per Game', 'FGA', 'FGM',
        'FG%', '3PA', '3PM', '3P%', 'FTA', 'FTM', 'FT%', 'Rebounds', 'DBoards', 'OBoards', 'Assists', 'Turnovers',
        'Steals', 'Blocks', 'Fouls'])

# Initial greeting
def greet():
    print("Welcome to my draft scraping program!")

# Get the years the user wants to get draft info for
def getYears():
    try:
        print("\nPlease choose a year to start scraping: ")
        begin = int(input(">>> "))

        print("\nPlease choose an ending year")
        end = int(input(">>> "))
    except ValueError:
        print("Please choose an integer value")
        getYears()
    # Make sure begin is less than current year - 1, and that end is [1975-begin)
    if begin >= (today.year - 1) or (end > begin or end < 1975):
        print("Please choose a begin date before the year {} and an end date before 1975".format(today.year))
        getYears()
    return begin, end

# Ask for the name of the csv file the user would like to save results to
def getCSVName():
    try:
        print("\nPlease enter the name of a csv file you'd like to write to")
        csvFile = input(">>> ")
    except Exception as e:
        print(e)
        getCSVName()
    if csvFile.endswith(".csv"): return csvFile
    else:
        print("Your file name needs to end in .csv")
        getCSVName()


def main():
    # Greet user
    greet()
    # Get begin/end date in years
    years = getYears()
    startYear, endYear = years
    draftFileName = getCSVName()
    # Write the header
    writeHeader(draftFileName)
    stop = False
    # Get the tables of the specified years
    while not stop:
        if startYear == endYear: stop = True
        getPicky(startYear, draftFileName)
        startYear -= 1 # decrement year

    print("Program finished in {} seconds".format(round(time.time() - start_time, 2)))

if __name__ == '__main__':
    main()
