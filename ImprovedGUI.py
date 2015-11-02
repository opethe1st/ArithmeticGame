"""I am starting from scratch. I will pay more attention to designing on paper first before
coding. Take Ideas from GameGUI.py and sound ideas from WxPython in Action."""
import GameLogic
import wx


class MyApp(wx.App):
    def OnInit():
        """Create the Arithmetica frame."""
        Arithmetica(None)
        return True

class Arithmetica(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,None,id = -1,title = "Arithmetica")
