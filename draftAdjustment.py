'''
File to adjust the inputs of the stats so everything entered is either a 1 or -1
'''
import csv
from sys import exit
import pandas as pd
import time

# To track how long this program takes
start_time = time.time()
# For testing purposes
# stats_file = "draftInfo.csv"

# Greet user and get that csv file
def greet():
    print("Hello and welcome to my draft adjustment file")

    print("\nPlease enter a csv file to adjust")
    try:
        csv_file = input(">>> ")
    except KeyboardInterrupt:
        print("Goodbye!")
        exit()
    if csv_file.endswith(".csv"): return csv_file
    else:
        print("Please enter a csv file")
        greet()

# Get name of text file to output our inputs to
def inputsFile():
    print("\nPlease enter a text file to save the inputs to")
    try:
        in_file = input(">>> ")
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()
    if in_file.endswith(".txt"): return in_file
    else:
        print("Please enter a .txt file")
        inputsFile()

# Function to open csv file and store each row
def readCSV(csv_file):
    df = pd.read_csv(csv_file)
    df.head()
    # Remove the player name, year, nba team, pos and prev team
    df = df.drop(["Player", "Year", "NBA Team", "Position", "Prev Team"], axis=1)
    df.head()
    df.set_index('Round', inplace='True')
    df.head()


    return df

# Function to read each row of data and adjust values to 1 or -1
def adjust(csv_data, results):
    # print(len(csv_data))
    adjustments = [[] for _ in range(len(csv_data))]
    # On each row it prints each stat in the header
    for i, row in enumerate(csv_data.itertuples()):
        for j in range(len(row)):
            # Round
            if j == 0:
                if row[j] == 1: adjustments[i].append(1)
                elif row[j] != 1: adjustments[i].append(-1)
            # Pick
            elif j == 1:
                if row[j] in range(1, 11): adjustments[i].append(1)
                elif row[j] >= 11 or row[j] == 0: adjustments.append(-1)
            # Games Played
            elif j == 2:
                if row[j] >= 410: adjustments[i].append(1)
                elif row[j] < 410: adjustments[i].append(-1)
            # Games Started
            elif j == 3:
                if row[j] >= 205: adjustments[i].append(1)
                elif row[j] < 205: adjustments[i].append(-1)
            # Minutes
            elif j == 4:
                if row[j] >= 30: adjustments[i].append(1)
                elif row[j] < 30: adjustments[i].append(-1)
            # PPG
            elif j == 5:
                if row[j] >= 25: adjustments[i].append(1)
                elif row[j] < 25: adjustments[i].append(-1)
            # FGA
            elif j == 6:
                if row[j] >= 10: adjustments[i].append(1)
                elif row[j] < 10: adjustments[i].append(-1)
            # FGM
            elif j == 7:
                if row[j] >= 5: adjustments[i].append(1)
                elif row[j] < 5: adjustments[i].append(-1)
            # FG%
            elif j == 8:
                if row[j] >= .47: adjustments[i].append(1)
                elif row[j] < .47: adjustments[i].append(-1)
            # 3PA
            elif j == 9:
                if row[j] >= 2: adjustments[i].append(1)
                elif row[j] < 2: adjustments[i].append(-1)
            # 3PM
            elif j == 10:
                if row[j] >= 1: adjustments[i].append(1)
                elif row[j] < 1: adjustments[i].append(-1)
            # 3P%
            elif j == 11:
                if row[j] >= .5: adjustments[i].append(1)
                elif row[j] < .5: adjustments[i].append(-1)
            # FTA
            elif j == 12:
                if row[j] >= 2.5: adjustments[i].append(1)
                elif row[j] < 2.5: adjustments[i].append(-1)
            # FTM
            elif j == 13:
                if row[j] >= 1.25: adjustments[i].append(1)
                elif row[j] < 1.25: adjustments[i].append(-1)
            # FT%
            elif j == 14:
                if row[j] >= .75: adjustments[i].append(1)
                elif row[j] < .75: adjustments[i].append(-1)
            # Rebounds
            elif j == 15:
                if row[j] >= 8: adjustments[i].append(1)
                elif row[j] < 8: adjustments[i].append(-1)
            # DBoards
            elif j == 16:
                if row[j] >= 6: adjustments[i].append(1)
                elif row[j] < 6: adjustments[i].append(-1)
            # OBoards
            elif j == 17:
                if row[j] >= 2: adjustments[i].append(1)
                elif row[j] < 2: adjustments[i].append(-1)
            # Assists
            elif j == 18:
                if row[j] >= 5: adjustments[i].append(1)
                elif row[j] < 5: adjustments[i].append(-1)
            # Turnovers
            elif j == 19:
                if row[j] <= 2.5: adjustments[i].append(1)
                elif row[j] > 2.5: adjustments[i].append(-1)
            # Steals
            elif j == 20:
                if row[j] >= 2.5: adjustments[i].append(1)
                elif row[j] < 2.5: adjustments[i].append(-1)
            # Blocks
            elif j == 21:
                if row[j] >= 1.5: adjustments[i].append(1)
                elif row[j] < 1.5: adjustments[i].append(-1)
            # Fouls
            elif j == 22:
                if row[j] <= 2: adjustments[i].append(1)
                elif row[j] > 2: adjustments[i].append(-1)
    # To cut off the extra values at the end
    return adjustments[:len(csv_data)]

    # print(adjustments)
    # Write results to text file
    # writeResults(results, adjustments)

# Function to write results of adjust to text file
def writeResults(res_file, adj_inputs):
    try:
        with open(res_file, 'a') as rf:
            # Get number of inputs and their length
            l = len(adj_inputs)
            ins_in_line = len(adj_inputs[0])
            # Write num inputs and length
            rf.write(str(l))
            rf.write('\n')
            rf.write(str(ins_in_line))
            rf.write('\n')
            rf.write('\n')
            # Write the inputs on a separate line
            for line in adj_inputs:
                # print("This is a line ", line)
                for data in line:
                    rf.write(str(data))
                rf.write('\n')
    except Exception as e:
        print(e)
        exit()
    return res_file

def main():
    # Greet
    stats_file = greet()
    # Get name of txt file to save inputs to
    inp_file = inputsFile()
    # open and read each row
    data = readCSV(stats_file)
    # Go through each row and adjust values
    adj = adjust(data, inp_file)
    # Write to file
    writeResults(inp_file, adj)
    print("File has been written to and we're done!")
    print("\nProgram finished in {} seconds".format(round(time.time() - start_time, 2)))
if __name__ == '__main__':
    main()
