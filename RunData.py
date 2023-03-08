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
               'Distance', 'Hours', 'Minutes', 'Seconds', 'WeekDay', 'Notes']
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
            self.log = pd.read_csv(path, index_col=False)
        else:
            self.log = pd.DataFrame(columns=self.COLUMNS)

    def addRun(self, date, year, month, day, distance, hours, minutes, seconds, weekDay, notes):

        entryDict = {'Date': date, 'Year': year, 'Month': month,
                     'Day': day, 'Distance': distance, 'Hours': hours,
                     'Minutes': minutes, 'Seconds': seconds, 'WeekDay': weekDay, 'Notes': notes}
        for i in range(10):
            self.log = self.log.append(
                entryDict, ignore_index=True)

        print(self.log)

    def saveToFile(self):
        self.log.to_csv(self.completeName, index=False)

    def getGraphData(self, graphType):
        if self.log.empty:
            return None
        if graphType == 'day':
            self.log['Date'] = pd.to_datetime(self.log['Date'])
            df = self.log.groupby(self.log['Date'])
            print(df)
            df['WeekDay'] = df['Date'].dt.day_name()
            df.sort_values(by='Date')
            print(df)
            graph1d = df.loc[-7:, ['WeekDay', 'Distance']]
            return None

    def setOverallStats(self):
        if self.log.empty:
            return
        dfOverallTotals = self.log.loc[:10, [
            'Distance', 'Hours', 'Minutes', 'Seconds']]
        print(dfOverallTotals)
        sum = dfOverallTotals.sum()
        print(sum)

    # with open(COMPLETE_NAME, "w", newline='') as log:
    #     writer = csv.DictWriter(log, fieldnames=FIELDS)
    #     writer.writeheader()
    #     print("test")
