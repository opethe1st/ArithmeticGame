#!/usr/bin/env python2

"""This is where the GUI of the Arithmetic game is going to be. It is going to use methods from the GameLogic file.
specifically the generateExpression and evaluateExpression methods"""

import GameLogic
import wx
import time as t

class MyApp(wx.App):
    def OnInit(self):
        return True

class ArithmeticGame(wx.Frame):
    """This is the main frame """
    def __init__(self,parent):
        """Initiaize variables plus run the program"""
        wx.Frame.__init__(self,parent,pos=(500,300),title = "'rithmetik",size=(500,300))
        self.count = 0                 #counter, number of times, the program has asked a question
        self.NUMROUNDS = 5             #Constant to hold the number of times the question is asked
        self.numCorrectAns = 0          #Initially the number of correct Answers is Zero
        self.CorrectAns = None          #Correct Answer to a given question. here so it can be shared by other methods
        self.RunBefore = False          #Flag to check if the program has been run before.Here so it can checked by other programs
        self.TotalScore = 0
        global size
        size = (500,300)           #Size of the panels.
        self.nest = 0                   #maximum number of possible nesting of expressions
        self.answer = None              #What the user put as the answer.
        self.TimeReq = 10                #Initial time required to answer a question.
        self.TimeOut = False

        self.panel = wx.Panel(self)
        #Create a Menu
        self.settingsMenu = wx.Menu()
        self.settingsId = 1000
        self.settingsMenu.Append(self.settingsId,"Settings","Adjust Program Settings")
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.settingsMenu,"Settings")
        self.Bind(wx.EVT_MENU,self.configure)
        self.SetMenuBar(self.menuBar)
        #main program
        self.run()                      #The equivalent of the main program.

    def configure(self,e):
        """Adjust the required time to answer a question. change the nesting."""
        config = wx.Dialog(self,0,title="Settings",size=(200,170))
        sizer = wx.BoxSizer(wx.VERTICAL)
        TimText = wx.StaticText(config, -1, "Select the time you need to answer a question",)
        times = ['5','10','20' ]

        lb = wx.Choice(config, -1, (85, 18),choices=times)
        sizer.Add(TimText,0)
        sizer.Add(lb, 1)

        NmText = wx.StaticText(config, -1, "Select the number of Rounds",)
        numrounds = ['3','5','7' ]

        lb2 = wx.Choice(config, -1, (105, 18),choices=numrounds)
        sizer.Add(NmText,0)
        sizer.Add(lb2, 1)

        box  = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(wx.Button(config,wx.ID_OK),0)
        box.Add(wx.Button(config,wx.ID_CANCEL),1)

        sizer.Add(box, 0)
        config.SetSizer(sizer)
        config.SetAutoLayout(True)
        sizer.Fit(config)

        r  = config.ShowModal()
        if r == wx.ID_OK:
            self.TimeReq = int(times[lb.GetSelection()])
            self.NUMROUNDS = int(numrounds[lb2.GetSelection()])


    def __startPage(self):
        """This the start page. Shall we Begin?yes or no"""
        self.settingsMenu.Enable(self.settingsId,True)
        self.numCorrectAns = 0
        self.count = 0
        FrameSizer = wx.BoxSizer(wx.VERTICAL)   #Sizer for the main frame
        self.panel.Destroy()
        self.panel = wx.Panel(self,size = size)
        panelSizer = wx.BoxSizer(wx.VERTICAL)   #sizer for the panel
        self.panel.SetBackgroundColour('White')
        #self.panel.Refresh()
        label = wx.StaticText(self.panel,label="Red Pill or Blue Pill?")
        font = wx.Font(17,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        label.SetFont(font)

        startStop = wx.Panel(self.panel,size = size)             #Panel to contain the yes and no buttons
        startStop.SetBackgroundColour('White')
        ynsizer = wx.BoxSizer(wx.HORIZONTAL)    #sizer for the panel
        yes = wx.Button(startStop,label="Blue")  #The yes button
        yes.SetBackgroundColour("LightBlue")
        self.Bind(wx.EVT_BUTTON,self.newPage,yes)  #bind the yes button to self.newPage
        no = wx.Button(startStop,label= "Red")
        no.SetBackgroundColour("Pink")
        self.Bind(wx.EVT_BUTTON,self.resPage,no) #Display the resultPage if the user selects No
        ynsizer.Add(yes)
        ynsizer.Add(no)
        startStop.SetSizer(ynsizer)

        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(label,0,wx.ALIGN_CENTER)
        panelSizer.Add(startStop,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(2)

        self.panel.SetSizer(panelSizer)

        #self.Layout()
        self.Show()

    def staPage(self,e):
        """Destroy the previous panel and create the StartPage. This can be in StartPage? Nah..because self,event"""
        self.__startPage()

    def __newQuestion(self,panel):
        """A method to display the Questions page"""
        #Can't change settings in the middle of a game
        self.settingsMenu.Enable(1000,False) #I fixed 1000 for some reason , earlier when I was setting up settingsMenu
        #FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetBackgroundColour('LightYellow')
        self.panel.Refresh()

        #The main use of GameLogic. Generates a Queston and Answer pair
        self.numdigit = 1
        expr,self.CorrectAns = GameLogic.generateQuestion(self.numdigit,self.nest)
        #print expr,self.CorrectAns
        question = wx.StaticText(panel,label="%s = \n"%expr)
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        question.SetFont(font)

        self.inputAns = wx.TextCtrl(panel,style = wx.TE_PROCESS_ENTER,size=(40,20))

        self.timer1 = wx.Timer(self)
        self.timer1.Start(self.TimeReq*1000,oneShot=True)
        self.Bind(wx.EVT_TIMER,self.timedOut,self.timer1)

        self.Bind(wx.EVT_TEXT_ENTER,self.correctAns,self.inputAns)

        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(question,0,wx.ALIGN_CENTER)
        panelSizer.Add(self.inputAns,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(2)
        panel.SetSizer(panelSizer)
        #FrameSizer.AddStretchSpacer(1)
        #FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        #FrameSizer.AddStretchSpacer(2)
        #self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()
        self.start = t.time()

    def isCorrectPage(self,panel,message,score=0):
        self.Layout()
        if message=="Correct!":
            self.panel.SetBackgroundColour('LightGreen')
            self.panel.Refresh()
        else:
            self.panel.SetBackgroundColour('Pink')
            self.panel.Refresh()
        #FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        CorrectMessage = wx.StaticText(panel,label = message)
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        CorrectMessage.SetFont(font)

        label = "The correct answer is %s. "%(self.CorrectAns)
        if score!=0:
            label += "You scored %d"%score
        CorrectAnswer = wx.StaticText(panel,label = label)
        font = wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        CorrectAnswer.SetFont(font)

        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(CorrectMessage,0,wx.ALIGN_CENTER)
        panelSizer.Add(CorrectAnswer,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(2)

        panel.SetSizer(panelSizer)
        #FrameSizer.AddStretchSpacer(1)
        #FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        #FrameSizer.AddStretchSpacer(2)
        #self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def __resultPage(self):
        self.timer1.Stop()
        self.Layout()
        #FrameSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.Destroy()
        self.panel = wx.Panel(self,size = size)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        Result = wx.StaticText(self.panel,label="You got %d/%d correct\nYour total score was %d "%(self.numCorrectAns,self.NUMROUNDS,self.TotalScore))
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        Result.SetFont(font)

        startStop = wx.Panel(self.panel,size = size)             #Panel to contain the yes and no buttons
        startStop.SetBackgroundColour("LightGray")
        ynsizer = wx.BoxSizer(wx.HORIZONTAL)    #sizer for the panel
        yes = wx.Button(startStop,label="Play")  #The yes button
        self.Bind(wx.EVT_BUTTON,self.staPage,yes)  #bind the yes button to self.newPage
        no = wx.Button(startStop,label= "Quit")
        self.Bind(wx.EVT_BUTTON,self.exit,no) #Display the resultPage if the user selects No
        ynsizer.Add(yes)
        ynsizer.Add(no)
        startStop.SetSizer(ynsizer)

        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(Result,0,wx.ALIGN_CENTER)
        panelSizer.Add(startStop,0, wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(2)
        self.panel.SetSizer(panelSizer)
        self.panel.SetBackgroundColour("LightGray")
        #FrameSizer.AddStretchSpacer(1)
        #FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        #FrameSizer.AddStretchSpacer(2)
        #self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def resPage(self,e):

        self.__resultPage()

    def newPage(self,e):
        #""
        if not self.RunBefore:
            self.RunBefore=True
        self.panel.Destroy()
        self.panel = wx.Panel(self,size = size)
        if self.count<self.NUMROUNDS:
            self.__newQuestion(self.panel)
            self.count+=1
        else:
            self.__resultPage()

    def timedOut(self,e):
        self.panel.Destroy()
        self.panel = wx.Panel(self,size = size)
        self.TimeOut = True
        timeout ="Time Out!"
        self.isCorrectPage(self.panel,timeout)
        self.timer = wx.Timer(self)
        self.timer.Start(2000)
        self.Bind(wx.EVT_TIMER,self.update,self.timer)

    def correctAns(self,e):
        self.elapsedTime = t.time()-self.start
        print self.elapsedTime
        self.timer1.Stop()
        ans = self.inputAns.GetLineText(0)
        self.panel.Destroy()
        self.panel = wx.Panel(self,size = size)
        if GameLogic.checkAnswer(ans,self.CorrectAns):
            isCorrect = "Correct!"
            self.isCorrectPage(self.panel,isCorrect,20-int(self.elapsedTime))
            self.TotalScore += 20-int(self.elapsedTime)
            self.numCorrectAns+=1
        else:
            isCorrect ="Wrong!"
            self.isCorrectPage(self.panel,isCorrect)
        self.timer = wx.Timer(self)
        self.timer.Start(2000)
        self.Bind(wx.EVT_TIMER,self.update,self.timer)


    def update(self,e):
        if self.timer.IsRunning():
            self.timer.Stop()
            self.panel.Destroy()
            self.panel = wx.Panel(self,size = size)
            self.__newQuestion(self.panel)
            self.count+=1

        if self.count>self.NUMROUNDS:

            self.__resultPage()

    def exit(self,e):
        self.Destroy()

    def run(self):
        #self.panel = wx.Panel(self,size = size)
        self.__startPage()
#NewPage is used just once I think. I should probably remove it

app = MyApp(False)
ArithmeticGame(None)
app.MainLoop()
