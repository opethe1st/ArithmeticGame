"""This is where the GUI of the Arithmetic game is going to be. It is going to use methods from the GameLogic file.
specifically the generateExpression and evaluateExpression methods"""

import GameLogic
import wx
import time as t

class ArithmeticGame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,pos=(400,300),title = "Arithmetic Game")
        self.run()

    def startPage(self,panel):
        panel = panel
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel,label="\tShall\n\tWe \n\tBegin?\n")
        self.sizer.Add(label)

        startStop = wx.Panel(panel)
        ynsizer = wx.BoxSizer(wx.HORIZONTAL)
        yes = wx.Button(startStop,label="yes")
        self.Bind(wx.EVT_BUTTON,self.onYes,yes)
        no = wx.Button(startStop,label= "no")
        #self.Bind(wx.EVT_BUTTON,exit(0),no)
        ynsizer.Add(yes)
        ynsizer.Add(no)
        startStop.SetSizer(ynsizer)

        self.sizer.Add(startStop)

        panel.SetSizer(self.sizer)
        MainSizer.Add(panel)
        self.SetSizer(MainSizer)
        self.SetSize((300,100))
        self.Show()

    def newQuestion(self,panel,numOfTimes):
        """A method to display Questions"""
        if numOfTimes>=4:
            return
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        panel = panel
        expr,self.CorrectAns = GameLogic.generateQuestion(1,1)
        self.question = wx.StaticText(panel,label="Solve\n %s"%expr)
        self.sizer.Add(self.question)

        self.inputAns = wx.TextCtrl(panel,style = wx.TE_PROCESS_ENTER)
        self.sizer.Add(self.inputAns)
        self.Bind(wx.EVT_TEXT_ENTER,self.correctAns,self.inputAns)

        self.answer = wx.TextCtrl(panel,style = wx.TE_READONLY,size=(150,25) )
        self.answer.SetValue("Answer Now!")
        self.sizer.Add(self.answer)

        self.next = wx.Button(panel,label="Next")
        self.sizer.Add(self.next)
        self.Bind(wx.EVT_BUTTON,self.newQ,self.next)

        panel.SetSizer(self.sizer)
        MainSizer.Add(panel)

        self.SetSizerAndFit(MainSizer)
        self.SetSize((300,100))
        self.Show()

    def resultPage():
        pass

    def update(self,e):
        self.panel.Destroy()
        self.Layout()
        self.panel = wx.Panel(self)
        self.newQuestion(self.panel,0)


    def onYes(self,e):
        self.panel.Destroy()
        self.Layout()
        self.panel = wx.Panel(self)
        self.newQuestion(self.panel,0)

    def correctAns(self,e):
        ans = self.inputAns.GetLineText(0)
        if GameLogic.checkAnswer(ans,self.CorrectAns):
            self.answer.SetValue("The answer is correct")
        else:
            self.answer.SetValue("The answer is wrong")

    def newQ(self,e):
        self.panel.Destroy()
        self.Layout()
        self.panel = wx.Panel(self)
        self.newQuestion(self.panel,0)

    def run(self):
        self.panel = wx.Panel(self)
        self.startPage(self.panel)


app = wx.App(False)
ArithmeticGame(None)
app.MainLoop()
