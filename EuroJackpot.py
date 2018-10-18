#!/usr/bin/env python4
import csv
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import date

#A program designet to use web scarping of page from perlas EuroJackpot statistics with beautifulsoup and requests
class euroJackpotWebScrap:

    # Constructor of the euroJackpot class
    def __init__(self):
        # Declaration of a variable that will contain the webpage from which the information is going to be pulled out
        # The XXXX in the webPageEuroJackpot must be replaced with the first game number from which the user wants to
        # gather data from
        # The YYYY in the webPageEuroJackpot must be replaced with the last game number that the user wants to
        # gather data
        self.webPageEuroJackpot = "https://perku.perlas.lt/lt/statistic/eurojackpot?" \
                                  "tab=archive&Filter%5BdrawFrom%5D=XXXX&Filter%5BdrawTo%5D=YYYY"
        self.date = date(2013, 2, 1)

    # Method that changes the initial webpage by including the correct beginning and the end of the required data
    def setPage(self, nrFrom, nrTo):
        self.webPageEuroJackpot = self.webPageEuroJackpot.replace('XXXX', nrFrom)
        self.webPageEuroJackpot = self.webPageEuroJackpot.replace('YYYY', nrTo)

    # Method that is responsible for gathering data from the website
    # options for gathering data are 'numbers' - initial numbers of the game, 'gameNr'- the number of the game,
    # 'bonusNr' - the bonus number of the game
    def requesting(self, requesting, page):
        webPageOpen = requests.get(page)
        webData = webPageOpen.text
        soup = BeautifulSoup(webData, 'html.parser')

        if requesting == 'numbers':
            return soup.findAll('li', 'number ')

        if requesting == 'gameNr':
            return soup.findAll('p', 'lead')

        if requesting == 'bonusNr':
            return soup.findAll('li', 'number bonus-number')

    # Method that adjusts the date to match the date for the first requested game by the user
    def adjustDate(self, firstGame):
        self.date = self.date + ((timedelta(days=7)) * (firstGame-1))

    # Method that returns date and changes the current date by 7 days
    def addDate(self):
        theDate = self.date.strftime("%Y/%m/%d")
        self.date = self.date + (timedelta(days=7))
        return theDate

    # Method that tests if the file myData.csv is currently not open
    # returns False if the file is currently opened
    def testTextFile(self):
        try:
            with open('myData.csv', 'w', newline='') as csvFile:
                csvFile.close
                return True
        except IOError:
            return False

    #  Method that uses other methods from this class to write the data into myFile.csv
    def writeNumbers(self):
        # Variables that hold all the data from the website
        numbers = self.requesting('numbers', self.webPageEuroJackpot)
        gameNr = self.requesting('gameNr', self.webPageEuroJackpot)
        bonusNr = self.requesting('bonusNr', self.webPageEuroJackpot)
        with open('myData.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=';')
            while len(gameNr) > 0:
                fullOne = []
                fullOne.append(gameNr.pop().string[13:])
                fullOne.append(self.addDate())
                numberOfNumbers = 0
                # tempList is storing the numbers that belong to the current game
                tempList = []
                while numberOfNumbers < 5:
                    tempList.append(numbers.pop().string)
                    numberOfNumbers += 1
                # Sorted tempList
                tempListSorted = sorted(tempList)
                placesToSkip = 0
                for eachNumber in tempListSorted:
                    tempNr = int(eachNumber)
                    while placesToSkip < tempNr:
                        fullOne.append( ' ')
                        placesToSkip += 1
                    fullOne.append(eachNumber)
                    placesToSkip +=1
                fullOne.insert(2, bonusNr.pop().string)
                fullOne.insert(2, bonusNr.pop().string)
                writer.writerow(fullOne)
        csvFile.close

    # Method that checks what is the last game of Euro Jackpot
    def currentMax(self):
        webPageOpen = requests.get('https://perku.perlas.lt/lt/statistic/eurojackpot?tab=archive')
        webData = webPageOpen.text
        soup = BeautifulSoup(webData, 'html.parser')
        return soup.find('p', 'lead').string[13:]

    # Coordinating method to be called by other classes
    def coord(self, numbersFrom, numbersTo):
        self.setPage(numbersFrom, numbersTo)
        self.adjustDate(int(numbersFrom))
        self.writeNumbers()
