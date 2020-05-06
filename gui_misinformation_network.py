import wx
from twitter_misinformation import *


class MisinformationDetector(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        tekst = 'Misinformation Detector'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, tekst, (wx.VERTICAL, 10)).SetFont(font)
        
        self.lblname = wx.StaticText(self, -1, "Enter Tweet:", pos=(wx.VERTICAL, 60))
        self.tweet = wx.TextCtrl(self,5, "",wx.Point(20,85), wx.Size(295,110), \
                wx.TE_MULTILINE | wx.TE_RICH2)
            
        self.btn1 = wx.Button(self, -1, "Check", (130, 220))
        self.Bind(wx.EVT_BUTTON, self.Oker, self.btn1)
        
        self.btn = wx.Button(self, -1, "Go back", (wx.VERTICAL, 220))
        
    def Oker(self, event):
        tweet = self.tweet.GetValue()
        
        btn = event.GetEventObject()
        btn.Disable()
        
        wait = wx.BusyInfo("Please wait, working...")
        prediction = check_tweet(tweet)
        
        if prediction:
            message = 'Tweet is a misinformation'
        else:
            message = 'Tweet is normal'
        
        del wait
        dlg = wx.MessageDialog(self, message, style=wx.OK|wx.CENTRE|wx.ICON_NONE)
        dlg.SetOKLabel('OK')
        dlg.ShowModal()
        btn.Enable()
        