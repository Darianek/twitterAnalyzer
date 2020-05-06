import wx
from user_bot_detector_ann import ann_predict
import user_bot_detector_tweets as ubdt
from user_bot_detector_decision_trees import random_forest_predict
from user_bot_detector_xgboost import xgboost_predict

from twitter_get_user import get_sinlge_user


class BotDetector(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        tekst = 'Bot Detector'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, tekst, (wx.VERTICAL, 10)).SetFont(font)

        self.screen_name = ''

        self.cb1 = wx.CheckBox(self, label='Single user:', pos=(0, 55))
        self.screen_name1 = wx.TextCtrl(self, -1, '', pos=(106, 50))
        self.cb2 = wx.CheckBox(self, label='Bots in network:', pos = (0, 95))
        self.screen_name2 = wx.TextCtrl(self, -1, '', pos=(134, 90))
        
        self.btn1 = wx.Button(self, -1, "Decision Trees", (wx.VERTICAL, 130))
        self.Bind(wx.EVT_BUTTON, self.Oker, self.btn1)

        self.btn2 = wx.Button(self, -1, "ANN", (121, 130))
        self.Bind(wx.EVT_BUTTON, self.Oker, self.btn2)
        
        self.btn3 = wx.Button(self, -1, "xgboost", (207, 130))
        self.Bind(wx.EVT_BUTTON, self.Oker, self.btn3)
        
        self.btn4 = wx.Button(self, -1, "Tweets", (7, 168))
        self.Bind(wx.EVT_BUTTON, self.Oker, self.btn4)

        self.btn = wx.Button(self, -1, "Go back", (wx.VERTICAL, 220))
        
    def Oker(self, event):
        
        cb = event.GetEventObject() 
        if self.cb1.GetValue():
            screen_name = self.screen_name1.GetValue()
        if self.cb2.GetValue():
            screen_name = self.screen_name2.GetValue()
            
        option = cb.GetLabel()
        
        btn = event.GetEventObject()
        btn.Disable()
        
        access_file = 'access/access10.txt'
        
        wait = wx.BusyInfo("Please wait, working...")
        
        to_predict = get_sinlge_user(screen_name, access_file)
        
        Z = [to_predict['Followers Count'], to_predict['Friends Count'], 
         to_predict['Listed count'], to_predict['Favourites count'],
         to_predict['Status count'], int(to_predict['Verified']), int(to_predict['Default profile']),
         int(to_predict['Default profile image'])]
               
        prediction = True
        
        if option == 'ANN':
            prediction = ann_predict(Z)
            ubdt.users_collection.update_one({"Label": screen_name}, {"$set": {"Bot": {"ANN": prediction}}})
        elif option == 'Random Forest':
            prediction = random_forest_predict(Z)
            ubdt.users_collection.update_one({"Label": screen_name}, {"$set": {"Bot": {"Random Forest": prediction}}})
        elif option == 'xgboost':
            prediction = xgboost_predict(Z)
            ubdt.users_collection.update_one({"Label": screen_name}, {"$set": {"Bot": {"xgboost": prediction}}})
        elif option == 'Tweets':
            prediction = ubdt.check_by_tweets(screen_name, access_file)
            ubdt.users_collection.update_one({"Label": screen_name}, {"$set": {"Bot": {"Tweets": prediction}}})
    
        if prediction:
            message = 'User is bot'
        else:
            message = 'User is normal'
        
        del wait
        dlg = wx.MessageDialog(self, message, style=wx.OK|wx.CENTRE|wx.ICON_NONE)
        dlg.SetOKLabel('OK')
        dlg.ShowModal()
        btn.Enable()
                    