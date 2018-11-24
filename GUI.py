#!/usr/bin/env python4
from tkinter import *
from euroJackpot import euroJackpotWebScrap
from vikingLotto import VikingLotoScrap
from tkinter import messagebox
from tkinter import filedialog


class GUIforEuroJackpotWeb:

    # Constructor for the GUI class
    # Creates the Graphic User Interface with Labels, Entries and Buttons
    def __init__(self):
        #Creates the main window for Graphic User Interface
        self.window = Tk()


        self.nrFrom = StringVar()
        self.nrTo = StringVar()

        #Creates an 'euroJackpot' object
        self.newWebScrap = euroJackpotWebScrap()
        self.newVikingLotoScrap = VikingLotoScrap()



        self.selectedGame = ''

        #Creates Entries and Button by calling in the methods
        self.theEntries()
        self.theButton()



        #Declares and assigns the CurrentMaximum(Current number of euroJackpot games)
        self.currentMaximumEuro = self.newWebScrap.currentMax()
        self.currentMaximumViking = self.newVikingLotoScrap.currentMax()

        #Initialises the Labels of the Grahpic user interface
        self.label1 = Label(self.window, text="Current minimum: ")
        self.label1.grid(row=1, column=1)
        label2 = Label(self.window, text="From:")
        label2.grid(row=3, column=1)
        label3 = Label(self.window, text="To:")
        label3.grid(row=3, column=3)
        label4 = Label(self.window, text="Current maximum:")
        label4.grid(row=1, column=3)
        self.label5 = Label(self.window, text=self.currentMaximumEuro)
        self.label5.grid(row=1, column=4)
        label6 = Label(self.window, text='Current Status:')
        label6.grid(row=5, column=3)
        self.label7 = Label(self.window, text='Select Game')
        self.label7.grid(row=5, column=4)
        labelskip = Label(self.window, text=' ')
        labelskip.grid(row=6, column=2)
        labelskip2 = Label(self.window, text=' ')
        labelskip2.grid(row=2, column=2)
        labelskip3 = Label(self.window, text=' ')
        labelskip3.grid(row=4, column=2)
        labelskip3 = Label(self.window, text=' ')
        labelskip3.grid(row=6, column=2)
        labelskip4 = Label(self.window, text=' ')
        labelskip4.grid(row=7, column=6)
        labelskip4 = Label(self.window, text=' ')
        labelskip4.grid(row=7, column=0)



        self.window.update()
        self.fileLocation = ''
        self.fileLocation = filedialog.asksaveasfilename()
        self.newVikingLotoScrap.setFileLocation(self.fileLocation)
        self.newWebScrap.setFileLocation(self.fileLocation)


        # Main loop for Graphic user interface to keep it renewed
        self.window.mainloop()

    # A method that helps to initialise the Entries into the Graphic User Interface
    def theEntries(self):
        # Initialises the Entry, which is going to be the first euroJacktop game
        # of which the user wants to gather the data
        entryFrom = Entry(self.window, textvariable=self.nrFrom)
        entryFrom.grid(row=3, column=2)

        # Initialises the Entry, which is going to be the last euroJacktop game
        # of which the user wants to gather the data
        entryTo = Entry(self.window, textvariable=self.nrTo)
        entryTo.grid(row=3, column=4)

    # A method that help to initialise the Buttons into the Graphic User Interface
    def theButton(self):
        button1 = Button(self.window, text='Execute', command=self.buttonExecute)
        button1.grid(row=6, column=4)

        button2 = Button(self.window, text='Exit', command=self.buttonExecute1)
        button2.grid(row=6, column=5)


        button3 = Button(self.window, text='Viking Loto', command=self.buttonExecute3)
        button3.grid(row=0, column=1)

        button4 = Button(self.window, text='EuroJackpot', command=self.buttonExecute4)
        button4.grid(row=0, column=2)

    # A method that works after the button in the GUI is pressed. Works as a coordinating method
    def buttonExecute(self):
        check = self.GUIchecks()
        if check == True:
            if(self.selectedGame == 'EuroJackpot'):
                textNrFrom = self.nrFrom.get()
                textNrTo = self.nrTo.get()
                self.newWebScrap.coord(textNrFrom, textNrTo)
                messagebox.showinfo("Title", "The information has been gathered successfully")
            else:
                textNrFrom = self.nrFrom.get()
                textNrTo = self.nrTo.get()
                self.newVikingLotoScrap.coord(textNrFrom, textNrTo)
                messagebox.showinfo("Title", "The information has been gathered successfully")



    #Exit
    def buttonExecute1(self):
        self.window.destroy()


    #Viking Loto
    def buttonExecute3(self):
        self.label1.config(text="Current minimum: 597")
        self.label5.config(text=self.currentMaximumViking)
        self.label7.config(text= 'Waiting for input')
        self.window.update()
        self.selectedGame = 'Viking'

    #EuroJackpot
    def buttonExecute4(self):
        self.label1.config(text="Current minimum: 1")
        self.label5.config(text=self.currentMaximumEuro)
        self.label7.config(text= 'Waiting for input')
        self.window.update()
        self.selectedGame = 'EuroJackpot'

    # A method that runs the checks to see if the information that has been entered by the user
    # are within the scope of the program
    def GUIchecks(self):
        GUIReturn = False

        if (self.selectedGame == 'EuroJackpot'):
            currentMaximum = self.currentMaximumEuro
        else:
            if (self.selectedGame == 'Viking'):
                currentMaximum = self.currentMaximumViking
            else:
                messagebox.showinfo("title", "Select a game before proceding")
        if (self.fileLocation == ''):
            messagebox.showinfo("title", "Location has not been selected")

        try:
            textNrFrom = self.nrFrom.get()
            textNrTo = self.nrTo.get()
            if int(textNrFrom) < 1:
                messagebox.showinfo("Title", "The entered number in the"
                                             " field \"From:\" is less than the first recorded draw")
            else:
                if int(textNrFrom) > int(currentMaximum):
                    messagebox.showinfo("Title", "The entered number in the field \"From:\" is "
                                                 "higher than the last recorded draw")
                else:
                    if int(textNrTo) > int(currentMaximum):
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
