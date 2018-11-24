#!/usr/bin/env python4
import csv
import requests
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import date

#A program designet to use web scarping of page from perlas EuroJackpot statistics with beautifulsoup and requests
class VikingLotoScrap:

    # Constructor of the euroJackpot class
    def __init__(self):
        # Declaration of a variable that will contain the webpage from which the information is going to be pulled out
        # The XXXX in the webPageEuroJackpot must be replaced with the first game number from which the user wants to
        # gather data from
        # The YYYY in the webPageEuroJackpot must be replaced with the last game number that the user wants to
        # gather data
        self.webVikingLotoPost = "https://perlas.lt/lt/statistic/vikinglotto?tab=archive&Filter%5BdrawFrom%5D=" \
                                  "XXXX&Filter%5BdrawTo%5D=YYYY"
        self.webVikingLotoPre = "https://perlas.lt/lt/statistic/vikingloto?tab=archive&Filter%5BdrawFrom%5D=" \
                                "XXXX&Filter%5BdrawTo%5D=YYYY"
        self.date = date(2004, 8, 18)
        self.fileLocation = ''
        self.gameNr = 597

    def currentGameNr(self):
        self.setGameNr(self.gameNr +1)
        return int(self.gameNr -1)

    def setGameNr(self, newGameNr):
        self.gameNr = newGameNr


    def setFileLocation(self, location):
        self.fileLocation = location +'.csv'

    def getFileLocation(self):
        return self.fileLocation

    # Method that changes the initial webpage by including the correct beginning and the end of the required data
    def setPage(self, nrFrom, nrTo):
        self.webVikingLotoPost = self.webVikingLotoPost.replace('XXXX', nrFrom)
        self.webVikingLotoPost = self.webVikingLotoPost.replace('YYYY', nrTo)
        self.webVikingLotoPre = self.webVikingLotoPre.replace('XXXX', nrFrom)
        self.webVikingLotoPre = self.webVikingLotoPre.replace('YYYY', nrTo)

    # Method that is responsible for gathering data from the website
    # options for gathering data are 'numbers' - initial numbers of the game, 'gameNr'- the number of the game,
    # 'bonusNr' - the bonus number of the game
    def requesting(self, requesting, page):
        webPageOpen = requests.get(page)
        webData = webPageOpen.text
        soup = BeautifulSoup(webData, 'html.parser')

        if requesting == 'numbers':
            return soup.findAll('li', 'number ')

#     if requesting == 'gameNr':
#        return soup.findAll('p', 'lead')

        if requesting == 'bonusNr':
            return soup.findAll('li', 'number bonus-number')

        if requesting == 'auksinisNr':
            return soup.findAll('li', 'number success-number')

    # Method that adjusts the date to match the date for the first requested game by the user
    def adjustDate(self, firstGame):
        self.date = self.date + ((timedelta(days=7)) * (firstGame-self.gameNr))

    # Method that returns date and changes the current date by 7 days
    def addDate(self):
        theDate = self.date.strftime("%Y/%m/%d")
        self.date = self.date + (timedelta(days=7))
        return theDate

    # Method that tests if the file myData.csv is currently not open
    # returns False if the file is currently opened
    def testTextFile(self):
        try:
            with open(self.fileLocation, 'w', newline='') as csvFile:
                csvFile.close
                return True
        except IOError:
            return False

    #  Method that uses other methods from this class to write the data into myFile.csv
    def writeNumbersPre(self,writeType,numbersFrom, numbersTo):
        # Variables that hold all the data from the website
        if (int(numbersTo) > 1262):
            numbTo = 1262
        else:
            numbTo = int(numbersTo)

        if (int(numbersFrom) > 597):
            self.setGameNr(int(numbersFrom))
        else:
            self.setGameNr(597)

        numbers = self.requesting('numbers', self.webVikingLotoPre)
        bonusNr = self.requesting('bonusNr', self.webVikingLotoPre)
        auksinisNr = self.requesting('auksinisNr', self.webVikingLotoPre)
        with open(self.fileLocation, writeType, newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=';')
            while (self.gameNr <= numbTo):
                fullOne = []
                fullOne.append(self.currentGameNr())
                fullOne.append(self.addDate())
                numberOfNumbers = 0
                # tempList is storing the numbers that belong to the current game
                tempList = []
                while numberOfNumbers < 6:
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
                fullOne.insert(2,auksinisNr.pop().string)
                writer.writerow(fullOne)
        csvFile.close


    #  Method that uses other methods from this class to write the data into myFile.csv
    def writeNumbersPost(self, writeType,numbersFrom, numbersTo):
        # Variables that hold all the data from the website

        if (int(numbersFrom) > 1263):
            self.setGameNr(int(numbersFrom))
        else:
            self.setGameNr(1263)
        numbers = self.requesting('numbers', self.webVikingLotoPost)
        bonusNr = self.requesting('bonusNr', self.webVikingLotoPost)
        with open(self.fileLocation, writeType, newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=';')
            while (int(self.gameNr) <= int(numbersTo)):
                fullOne = []
                fullOne.append(self.currentGameNr())
                fullOne.append(self.addDate())
                numberOfNumbers = 0
                # tempList is storing the numbers that belong to the current game
                tempList = []
                while numberOfNumbers < 6:
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
                writer.writerow(fullOne)
        csvFile.close

    # Method that checks what is the last game of Euro Jackpot
    def currentMax(self):
        webPageOpen = requests.get('https://perlas.lt/lt/statistic/vikinglotto#archive')
        webData = webPageOpen.text
        soup = BeautifulSoup(webData, 'html.parser')
        return soup.find('p', 'lead').string[13:]

    # Coordinating method to be called by other classes
    def coord(self, numbersFrom, numbersTo):
        self.setPage(numbersFrom, numbersTo)
        self.adjustDate(int(numbersFrom))
        if((int(numbersFrom)) < 1262):
            if((int(numbersTo)) < 1263):
                self.writeNumbersPre('w', numbersFrom, numbersTo)
            else:
                self.writeNumbersPre('w', numbersFrom, numbersTo)
                self.writeNumbersPost('a' , numbersFrom, numbersTo)
        else:
            self.writeNumbersPost('w', numbersTo)
