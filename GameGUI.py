"""This is where the GUI of the Arithmetic game is going to be. It is going to use methods from the GameLogic file.
specifically the generateExpression and evaluateExpression methods"""

import GameLogic
import wx
import time as t

class ArithmeticGame(wx.Frame):
    """This is the main frame """
    def __init__(self,parent):
        """Initiaize variables plus run the program"""
        wx.Frame.__init__(self,parent,pos=(400,300),title = "'rithmetik",size=(350,200))
        self.count = 0                 #counter, number of times, the program has asked a question
        self.NUMROUNDS = 3              #Constant to hold the number of times
        self.numCorrectAns = 0          #Initially the number of correct Answers is Zero
        self.CorrectAns = None          #Correct Answer to a given question. here so it can be shared by other methods
        self.RunBefore = False          #Flag to check if the program has been run before.Here so it can checked by other programs
        self.size = (350,200)           #Size of the panels.
        self.nest = 1                   #maximum number of possible nesting of expressions
        self.answer = None              #What the user put as the answer.

        self.run()                      #The equivalent of the main program.

    def __startPage(self,panel):
        """This the start page. Shall we Begin?yes or no"""
        FrameSizer = wx.BoxSizer(wx.VERTICAL)   #Sizer for the main frame
        panelSizer = wx.BoxSizer(wx.VERTICAL)   #sizer for the panel

        label = wx.StaticText(panel,label="Shall We Begin?")
        font = wx.Font(17,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        label.SetFont(font)

        startStop = wx.Panel(panel)             #Panel to contain the yes and no buttons
        ynsizer = wx.BoxSizer(wx.HORIZONTAL)    #sizer for the panel
        yes = wx.Button(startStop,label="yes")  #The yes button
        self.Bind(wx.EVT_BUTTON,self.newPage,yes)  #bind the yes button to self.newPage
        no = wx.Button(startStop,label= "no")
        self.Bind(wx.EVT_BUTTON,self.resPage,no) #Display the resultPage if the user selects No
        ynsizer.Add(yes)
        ynsizer.Add(no)
        startStop.SetSizer(ynsizer)

        panelSizer.Add(label,0,wx.ALIGN_CENTER)
        panelSizer.Add(startStop,0,wx.ALIGN_CENTER)

        panel.SetSizer(panelSizer)

        FrameSizer.AddStretchSpacer(1)
        FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        FrameSizer.AddStretchSpacer(2)

        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def staPage(self,e):
        """Destroy the previous panel and create the StartPage. This can be in StartPage? Nah..because self,event"""
        self.panel.Destroy()
        self.panel = wx.Panel(self,size=self.size)
        self.__startPage(self.panel)

    def __newQuestion(self,panel):
        """A method to display the Questions page"""
        #self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)

        expr,self.CorrectAns = GameLogic.generateQuestion(1,self.nest)

        question = wx.StaticText(panel,label="%s = \n"%expr)
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        question.SetFont(font)

        #inp = wx.Panel(panel)
        self.inputAns = wx.TextCtrl(panel,style = wx.TE_PROCESS_ENTER,size=(30,20))
        self.Bind(wx.EVT_TEXT_ENTER,self.correctAns,self.inputAns)

        panelSizer.Add(question,0,wx.ALIGN_CENTER)
        panelSizer.Add(self.inputAns,0,wx.ALIGN_CENTER)

        panel.SetSizer(panelSizer)
        FrameSizer.AddStretchSpacer(1)
        FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        FrameSizer.AddStretchSpacer(2)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def isCorrectPage(self,panel,message):
        self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        CorrectMessage = wx.StaticText(panel,label = message)
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        CorrectMessage.SetFont(font)

        panelSizer.Add(CorrectMessage,0,wx.ALIGN_CENTER)

        panel.SetSizer(panelSizer)
        FrameSizer.AddStretchSpacer(1)
        FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        FrameSizer.AddStretchSpacer(2)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def __resultPage(self,panel):

        self.count = 0
        self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        Result = wx.StaticText(panel,label="You got %d/%d correct "%(self.numCorrectAns,self.NUMROUNDS))

        startStop = wx.Panel(panel)             #Panel to contain the yes and no buttons
        ynsizer = wx.BoxSizer(wx.HORIZONTAL)    #sizer for the panel
        yes = wx.Button(startStop,label="Play")  #The yes button
        self.Bind(wx.EVT_BUTTON,self.staPage,yes)  #bind the yes button to self.newPage
        no = wx.Button(startStop,label= "Quit")
        self.Bind(wx.EVT_BUTTON,self.exit,no) #Display the resultPage if the user selects No
        ynsizer.Add(yes)
        ynsizer.Add(no)
        startStop.SetSizer(ynsizer)

        panelSizer.Add(Result,0,wx.ALIGN_CENTER)
        panelSizer.Add(startStop)

        panel.SetSizer(panelSizer)
        FrameSizer.AddStretchSpacer(1)
        FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        FrameSizer.AddStretchSpacer(2)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def resPage(self,e):
        self.panel.Destroy()
        self.panel = wx.Panel(self,size=self.size)
        self.__resultPage(self.panel)

    def newPage(self,e):
        ""
        if not self.RunBefore:
            self.RunBefore=True
        self.panel.Destroy()
        self.panel = wx.Panel(self,size=self.size)
        if self.count<self.NUMROUNDS:
            self.__newQuestion(self.panel)
            self.count+=1
        else:
            self.__resultPage(self.panel)

    def correctAns(self,e):
        ans = self.inputAns.GetLineText(0)
        self.panel.Destroy()
        self.panel = wx.Panel(self,size=self.size)
        if GameLogic.checkAnswer(ans,self.CorrectAns):
            isCorrect = "Correct!"
            self.numCorrectAns+=1
        else:
            isCorrect ="Wrong!"
        self.isCorrectPage(self.panel,isCorrect)
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER,self.update,self.timer)


    def update(self,e):
        if self.timer.IsRunning():
            self.timer.Stop()
            self.panel.Destroy()
            self.panel = wx.Panel(self,size=self.size)
            self.__newQuestion(self.panel)
            self.count+=1

        if self.count>self.NUMROUNDS:
            self.panel.Destroy()
            self.panel = wx.Panel(self,size=self.size)
            self.__resultPage(self.panel)

    def exit(self,e):
        self.Destroy()

    def run(self):
        self.panel = wx.Panel(self,size=self.size)
        self.__startPage(self.panel)
#NewPage is used just once I think. I should probably remove it

app = wx.App(False)
ArithmeticGame(None)
app.MainLoop()
