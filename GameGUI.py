"""This is where the GUI of the Arithmetic game is going to be. It is going to use methods from the GameLogic file.
specifically the generateExpression and evaluateExpression methods"""

import GameLogic
import wx
import time as t

class ArithmeticGame(wx.Frame):
    """This is the main frame """
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,pos=(400,300),title = "'rithmetik")
        self.times = 5
        self.NUMROUNDS = self.times
        self.numCorrectAns = 0
        self.CorrectAns = None
        self.RunBefore = False
        #question = None
        #self.inputAns = None

        self.size = (350,200)
        self.nest = 1
        self.answer = None
        self.run()

    def startPage(self,panel):
        """This the start page"""
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel,label="Shall We Begin?")
        font = wx.Font(17,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        label.SetFont(font)

        startStop = wx.Panel(panel)
        ynsizer = wx.BoxSizer(wx.HORIZONTAL)
        yes = wx.Button(startStop,label="yes")
        self.Bind(wx.EVT_BUTTON,self.newQ,yes)
        no = wx.Button(startStop,label= "no")
        self.Bind(wx.EVT_BUTTON,self.resultPage,no)
        ynsizer.Add(yes)
        ynsizer.Add(no)
        startStop.SetSizer(ynsizer)
        
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(label,0,wx.ALIGN_CENTER)
        panelSizer.Add(startStop,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(1)

        panel.SetSizer(panelSizer)

        FrameSizer.Add(panel)

        self.SetSizerAndFit(FrameSizer)
        self.Show()

    def newQuestion(self,panel):
        """A method to display the Questions page"""
        self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)

        expr,self.CorrectAns = GameLogic.generateQuestion(1,self.nest)

        question = wx.StaticText(panel,label="%s = \n"%expr)
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        question.SetFont(font)

        #inp = wx.Panel(panel)
        self.inputAns = wx.TextCtrl(panel,style = wx.TE_PROCESS_ENTER,size=(30,20))
        self.Bind(wx.EVT_TEXT_ENTER,self.correctAns,self.inputAns)

        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(question,0,wx.ALIGN_CENTER)
        panelSizer.Add(self.inputAns,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(1)

        panel.SetSizer(panelSizer)
        FrameSizer.Add(panel)
        self.SetSizerAndFit(FrameSizer)
        self.Layout()
        self.Show()

    def correctPage(self,panel):
        self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        CorrectMessage = wx.StaticText(panel,label = "Correct!")
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(CorrectMessage,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(1)
        CorrectMessage.SetFont(font)

        panel.SetSizer(panelSizer)
        FrameSizer.Add(panel)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()

    def wrongPage(self,panel,ans):
        self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        CorrectMessage = wx.StaticText(panel,label = "Wrong!\nThe correct answer is %s"%ans)
        font = wx.Font(15,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(CorrectMessage,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer(1)
        CorrectMessage.SetFont(font)

        panel.SetSizer(panelSizer)
        FrameSizer.Add(panel)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()


    def resultPage(self,panel):
        self.Layout()
        FrameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        Result = wx.StaticText(panel,label="You got %d/%d correct "%(self.numCorrectAns,self.NUMROUNDS))
        panelSizer.AddStretchSpacer()
        panelSizer.Add(Result,0,wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer()
        #panel.SetSizerAndFit(panelSizer)
        panel.SetSizer(panelSizer)
        FrameSizer.Add(panel,0,wx.ALIGN_CENTER)
        self.SetSizer(FrameSizer)
        self.Layout()
        self.Show()


    def newQ(self,e):
        if not self.RunBefore:
            self.RunBefore=True
        self.panel.Destroy()

        self.panel = wx.Panel(self,size=self.size)
        if self.times>0:
            self.newQuestion(self.panel)
            self.times-=1
        else:
            self.resultPage(self.panel)

    def correctAns(self,e):
        ans = self.inputAns.GetLineText(0)
        if GameLogic.checkAnswer(ans,self.CorrectAns):
            #self.answer.SetValue("The answer is correct")
            self.numCorrectAns+=1
            self.panel.Destroy()
            self.panel = wx.Panel(self,size=self.size)
            self.correctPage(self.panel)
            self.timer = wx.Timer(self)
            self.timer.Start(1500)
            self.Bind(wx.EVT_TIMER,self.update,self.timer)

        else:
            self.panel.Destroy()
            self.panel = wx.Panel(self,size=self.size)
            self.wrongPage(self.panel,self.CorrectAns)
            self.timer = wx.Timer(self)
            self.timer.Start(1500)
            self.Bind(wx.EVT_TIMER,self.update,self.timer)
            pass
            #self.answer.SetValue("The answer is wrong. The correct Answer is %s"%self.CorrectAns)
        #self.next.Enable()

    def update(self,e):
        if self.timer.IsRunning():
            self.timer.Stop()
            self.panel.Destroy()
            self.panel = wx.Panel(self,size=self.size)
            self.newQuestion(self.panel)
            self.times-=1

        if self.times==0:
            self.panel.Destroy()
            self.panel = wx.Panel(self,size=self.size)
            self.resultPage(self.panel)



    def run(self):
        self.panel = wx.Panel(self,size=self.size)
        self.startPage(self.panel)


app = wx.App(False)
ArithmeticGame(None)
app.MainLoop()
