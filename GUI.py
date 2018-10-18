#!/usr/bin/env python4
from tkinter import *
from euroJackpot import euroJackpotWebScrap
from tkinter import messagebox



class GUIforEuroJackpotWeb:

    # Constructor for the GUI class
    # Creates the Graphic User Interface with Labels, Entries and Buttons
    def __init__(self):
        #Creates the main window for Graphic User Interface
        self.window = Tk()

        self.nrFrom = StringVar()
        self.nrTo = StringVar()

        #Creates Entries and Button by calling in the methods
        self.theEntries()
        self.theButton()

        #Creates an 'euroJackpot' object
        self.newWebScrap = euroJackpotWebScrap()

        #Declares and assigns the CurrentMaximum(Current number of euroJackpot games)
        self.currentMaximum = self.newWebScrap.currentMax()

        #Initialises the Labels of the Grahpic user interface
        label1 = Label(self.window, text="Current minimum: 1")
        label1.grid(row=0, column=0)
        label2 = Label(self.window, text="From:")
        label2.grid(row=1, column=0)
        label3 = Label(self.window, text="To:")
        label3.grid(row=1, column=2)
        label4 = Label(self.window, text="Current maximum:")
        label4.grid(row=0, column=2)
        label5 = Label(self.window, text=self.currentMaximum)
        label5.grid(row=0, column=3)
        label6 = Label(self.window, text='Current Status:')
        label6.grid(row=3, column=0)
        label7 = Label(self.window, text='Waiting for input')
        label7.grid(row=3, column=1)
        # Main loop for Graphic user interface to keep it renewed
        self.window.mainloop()

    # A method that helps to initialise the Entries into the Graphic User Interface
    def theEntries(self):
        # Initialises the Entry, which is going to be the first euroJacktop game
        # of which the user wants to gather the data
        entryFrom = Entry(self.window, textvariable=self.nrFrom)
        entryFrom.grid(row=1, column=1)

        # Initialises the Entry, which is going to be the last euroJacktop game
        # of which the user wants to gather the data
        entryTo = Entry(self.window, textvariable=self.nrTo)
        entryTo.grid(row=1, column=3)

    # A method that help to initialise the Buttons into the Graphic User Interface
    def theButton(self):
        button1 = Button(self.window, text="Run", command=self.buttonExecute)
        button1.grid(row=3, column=3)

    # A method that works after the button in the GUI is pressed. Works as a coordinating method
    def buttonExecute(self):
        check = self.GUIchecks()
        if check == True:
            textNrFrom = self.nrFrom.get()
            textNrTo = self.nrTo.get()
            self.newWebScrap.coord(textNrFrom, textNrTo)
            messagebox.showinfo("Title", "The information has been gathered successfully")

    # A method that runs the checks to see if the information that has been entered by the user
    # are within the scope of the program
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
