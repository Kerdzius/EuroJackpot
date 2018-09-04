#!/usr/bin/env python4
from tkinter import *
from tkinter import ttk
from EuroJackpot import EuroJackpotWebScrap
from tkinter import messagebox


class GUIforEuroJackpotWeb:
    
    def __init__(self):
        self.window = Tk()
        
        
        self.nrFrom = StringVar()
        self.nrTo = StringVar()
        
    
        self.theEntries()
        self.theButton()
        
        
        self.newWebScrap = EuroJackpotWebScrap()
        self.currentMaximum = self.newWebScrap.currentMax()
        self.theLabels()
        
        self.window.mainloop()
    
    def theLabels(self):
        li = Label(self.window, text = "Current minimum: 1")
        li.grid(row = 0, column = 0)
        li = Label(self.window, text = "From:")
        li.grid(row = 1, column = 0)
        li = Label(self.window, text = "To:")
        li.grid(row = 1, column = 2)
        li = Label(self.window, text = "Current maximum:")
        li.grid(row = 0, column = 2)
        li = Label(self.window, text = self.currentMaximum)
        li.grid(row = 0, column = 3)
        
    def theEntries(self):
        entryFrom = Entry (self.window, textvariable = self.nrFrom)
        entryFrom.grid(row = 1, column = 1)
              
        entryTo = Entry (self.window, textvariable = self.nrTo)
        entryTo.grid(row = 1, column = 3)
        
            
    def theButton(self):
        b1 = Button(self.window, text = "Run", command = self.buttonExecute)
        b1.grid(row = 3, column = 3)
        
        
    def buttonExecute(self):
        try:
            textNrFrom = self.nrFrom.get()
            textNrTo = self.nrTo.get()

            if (int(textNrFrom) < 1):
                messagebox.showinfo("Title", "The entered number in the field \"From:\" is less than the first recorded draw")    
            else:
                if (int(textNrFrom) > int(self.currentMaximum)):
                    messagebox.showinfo("Title", "The entered number in the field \"From:\" is higher than the last recorded draw")
                else:
                    if (int(textNrTo) > int(self.currentMaximum)):
                        messagebox.showinfo("Title", "The entered number in the field \"To:\" is higher than the last recorded draw")
                    else:
                        if(int(textNrFrom)> int(textNrTo)):
                            messagebox.showinfo("Title", "The entered number in the field \"From:\" is higher than a number in the field \"To:\"")
                        else:
                            if(self.newWebScrap.testTextFile() == False):
                                messagebox.showinfo("Title", "The file \"myData.csv\" is currently open. Please Close it before continuing ")
                            else:
                                self.newWebScrap.coord(textNrFrom, textNrTo)
                                messagebox.showinfo("Title", "The information has been gathered successfully")
                        
        except ValueError:
                messagebox.showinfo("Error", "Not a number has been entered!")
            


a = GUIforEuroJackpotWeb()
