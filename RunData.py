# use conda activate rundataenv
import csv
import os
import pandas as pd
from pathlib import Path


class RunLog():

    completeName = ''
    fileName = ''
    SAVE_PATH = '/Users/tony/Documents/PersonalPython/RunningLog Project/'
    COLUMNS = ['Date', 'Year', 'Month', 'Day',
               'Distance', 'Hours', 'Minutes', 'Seconds', 'Notes']
    fileCounter = 0
    overallStats = {}

    def __init__(self):

        if self.fileCounter == 0:
            self.fileName = 'log' + '0'
        else:
            self.fileName = 'log' + self.fileCounter
        self.fileCounter += 1

        self.completeName = os.path.join(self.SAVE_PATH, self.fileName)

        path = Path(self.completeName)
        if path.is_file():
            self.log = pd.read_csv(path)
        else:
            self.log = pd.DataFrame(columns=self.COLUMNS)

    def addRun(self, date, year, month, day, distance, hours, minutes, seconds, notes):

        entryDict = {'Date': date, 'Year': year, 'Month': month,
                     'Day': day, 'Distance': distance, 'Hours': hours,
                     'Minutes': minutes, 'Seconds': seconds, 'Notes': notes}

        self.log = self.log.append(entryDict, ignore_index=True)

        print(self.log)

    def saveToFile(self):
        self.log.to_csv(self.completeName, index=False)

    def getGraphData(self):
        graph1d = self.log.loc[:20, ['Date', 'Distance']]
        return graph1d

    def setOverallStats(self):
        dfOverallTotals = self.log.loc[:20, [
            'Distance', 'Hours', 'Minutes', 'Seconds']]
        print(dfOverallTotals)
        sum = dfOverallTotals.sum()
        print(sum)

    # with open(COMPLETE_NAME, "w", newline='') as log:
    #     writer = csv.DictWriter(log, fieldnames=FIELDS)
    #     writer.writeheader()
    #     print("test")
