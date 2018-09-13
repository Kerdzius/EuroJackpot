#!/usr/bin/env python4
from tkinter import *
from tkinter import ttk
from euroJackpot import euroJackpotWebScrap
from tkinter import messagebox
from time import sleep


class GUIforEuroJackpotWeb:

    def __init__(self):
        self.window = Tk()

        self.nrFrom = StringVar()
        self.nrTo = StringVar()

        self.theEntries()
        self.theButton()

        self.newWebScrap = euroJackpotWebScrap()
        self.currentMaximum = self.newWebScrap.currentMax()

        li1 = Label(self.window, text="Current minimum: 1")
        li1.grid(row=0, column=0)
        li2 = Label(self.window, text="From:")
        li2.grid(row=1, column=0)
        li3 = Label(self.window, text="To:")
        li3.grid(row=1, column=2)
        li4 = Label(self.window, text="Current maximum:")
        li4.grid(row=0, column=2)
        li5 = Label(self.window, text=self.currentMaximum)
        li5.grid(row=0, column=3)
        li6 = Label(self.window, text='Current Status:')
        li6.grid(row=3, column=0)
        li7 = Label(self.window, text='Waiting for input')
        li7.grid(row=3, column=1)

        self.window.mainloop()

    def theEntries(self):
        entryFrom = Entry(self.window, textvariable=self.nrFrom)
        entryFrom.grid(row=1, column=1)

        entryTo = Entry(self.window, textvariable=self.nrTo)
        entryTo.grid(row=1, column=3)

    def theButton(self):
        b1 = Button(self.window, text="Run", command=self.buttonExecute)
        b1.grid(row=3, column=3)

    def buttonExecute(self):
        check = self.GUIchecks()
        if check == True:
            textNrFrom = self.nrFrom.get()
            textNrTo = self.nrTo.get()
            self.newWebScrap.coord(textNrFrom, textNrTo)
            messagebox.showinfo("Title", "The information has been gathered successfully")

    def GUIchecks(self):
        GUIReturn = False
        try:
            textNrFrom = self.nrFrom.get()
            textNrTo = self.nrTo.get()
            if int(textNrFrom) < 1:
                messagebox.showinfo("Title", "The entered number in the"
                                             " field \"From:\" is less than the first recorded draw")
            else:
                if int(textNrFrom) > int(self.currentMaximum):
                    messagebox.showinfo("Title", "The entered number in the field \"From:\" is "
                                                 "higher than the last recorded draw")
                else:
                    if int(textNrTo) > int(self.currentMaximum):
                        messagebox.showinfo("Title", "The entered number in the field \"To:\" is"
                                                     " higher than the last recorded draw")
                    else:
                        if int(textNrFrom) > int(textNrTo):
                            messagebox.showinfo("Title", "The entered number in the field \"From:\" is"
                                                         " higher than a number in the field \"To:\"")
                        else:
                            if self.newWebScrap.testTextFile() == False:
                                messagebox.showinfo("Title", "The file \"myData.csv\" is currently open."
                                                             " Please Close it before continuing ")
                            else:
                                GUIReturn = True

        except ValueError:
            messagebox.showinfo("Error", "Not a number has been entered!")
        return GUIReturn


a = GUIforEuroJackpotWeb()
