#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import csv
from datetime import timedelta
from datetime import date

#Web Scarping with beautifulsoup and requests
class EuroJackpotWebScrap:
    

    def __init__(self):
        self.webPageEuroJackpot = "https://perku.perlas.lt/lt/statistic/eurojackpot?tab=archive&Filter%5BdrawFrom%5D=XXXX&Filter%5BdrawTo%5D=YYYY"
        self.date = date(2013, 2, 1)
        
    def setPage (self, nrFrom, nrTo):
        self.webPageEuroJackpot = self.webPageEuroJackpot.replace('XXXX', nrFrom)
        self.webPageEuroJackpot = self.webPageEuroJackpot.replace('YYYY', nrTo)

    
    def requesting(self, requesting, page):
        webPageOpen = requests.get(page)
        webData = webPageOpen.text
        soup = BeautifulSoup(webData, 'html.parser')
        
        if (requesting == 'numbers'):
            return soup.findAll('li','number ')
        
        if(requesting == 'gameNr'):
            return soup.findAll('p', 'lead')

        if (requesting == 'bonusNr'):
            return soup.findAll('li' , 'number bonus-number')
        

    def adjustDate (self, firstGame):
        self.date = self.date + ((timedelta (days = 7))* (firstGame-1))

        
        
    def addDate(self):
        theDate = self.date.strftime("%Y/%m/%d")
        self.date = self.date + (timedelta (days = 7))
        return theDate
    
    
    def testTextFile(self):
        try:
            with open('myData.csv', 'w', newline= '') as csvFile:
                writer = csv.writer(csvFile, delimiter = ',')
                csvFile.close
                return True
        except IOError:
            return False
    
    def writeNumbers(self, numberRange):
        numbers = self.requesting('numbers', self.webPageEuroJackpot)
        gameNr = self.requesting('gameNr', self.webPageEuroJackpot)
        bonusNr = self.requesting('bonusNr', self.webPageEuroJackpot)            
        with open('myData.csv', 'w', newline= '') as csvFile:
            writer = csv.writer(csvFile, delimiter = ',')
            while(len(gameNr) > 0):
                fullOne= []
                fullOne.append(gameNr.pop().string[13:])
                fullOne.append(self.addDate())
                numberOfNumbers = 0
                while (numberOfNumbers < 5):
                    fullOne.insert(2, numbers.pop().string)
                    numberOfNumbers += 1
                fullOne.append(bonusNr.pop().string)
                fullOne.insert(7, bonusNr.pop().string)
                writer.writerow(fullOne)
        csvFile.close
   
    
    def currentMax (self):
        webPageOpen = requests.get('https://perku.perlas.lt/lt/statistic/eurojackpot?tab=archive')
        webData = webPageOpen.text
        soup = BeautifulSoup(webData, 'html.parser')
        return soup.find('p', 'lead').string[13:]
    
    
    def coord(self, numbersFrom, numbersTo):

        self.setPage(numbersFrom, numbersTo)
        self.adjustDate(int(numbersFrom))
        self.writeNumbers(numbersTo)
        
  






