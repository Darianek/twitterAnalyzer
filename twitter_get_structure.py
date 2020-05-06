import tweepy
import math
import wx
from time import strftime

from twitter_users_stats import get_stats
from twitter_get_user import *
  
from threading import Thread

from wx.lib.pubsub import pub

########################################################################
class TestThread(Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self, screen_name, deepth):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.screen_name = screen_name
        self.deepth = deepth
        self.start()    # start the thread

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        
        access_files = ['access/access1.txt', 'access/access2.txt', 'access/access3.txt', 'access/access4.txt', 'access/access5.txt',
              'access/access6.txt', 'access/access7.txt', 'access/access8.txt', 'access/access9.txt']
        safety = 0
        access = access_files[safety]
                
        names = []
        edges = set()
        names.append(self.screen_name)
        print('STARTING: ' + self.screen_name + ' at ' + strftime("%Y-%m-%d %H:%M:%S"))
        for i in range(0, self.deepth):
            for counter, name in enumerate(names):
                
                check = graph_collection.count_documents({"_id": name})
                
                if check == 1:
                    print('Already in database!')
                    print(str(math.ceil(counter)/len(names)*100) + '% ' + name + ' DONE' + ' at ' + strftime("%Y-%m-%d %H:%M:%S"))
                    wx.CallAfter(pub.sendMessage, "update", msg='')                
                else:
                    try:   
                        get_user(name, access)
                        print(str(math.ceil(counter)/len(names)*100) + '% ' + name + ' DONE' + ' at ' + strftime("%Y-%m-%d %H:%M:%S"))
                        wx.CallAfter(pub.sendMessage, "update", msg='')
                    except tweepy.TweepError:
                        print('CHANGING ACCESS FILE TO ' + access_files[safety] + '!')
                        if safety == 9:
                            safety = 0
                        else:
                            safety += 1
                        access = access_files[safety]
                        get_user(name, access) 
                        print(str(math.ceil(counter)/len(names)*100) + '% ' + name + ' DONE' + ' at ' + strftime("%Y-%m-%d %H:%M:%S"))
                        wx.CallAfter(pub.sendMessage, "update", msg='')
                        
                data = graph_collection.find_one({"_id": name})[name]
                source = data['Source']
                target = data['Target']
                direction = data['Direction']
                
                for counter, x in enumerate(source):
                    text = source[counter] + ',' + target[counter] + ',' + direction[counter]
                    edges.add(text)
                
            names = users_collection.find_one({"Label": name}, {"Connections": 1})["Connections"]
        
########################################################################
class MyProgressDialog(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, screen_name, deepth):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Progress")
        self.count = 0
        self.deepth = deepth
        access_file = 'access/access10.txt'
        
        if deepth == 1:
            self.length = 1
        else:
            self.length = get_number(screen_name, access_file)            

        self.progress = wx.Gauge(self, range=self.length)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)

        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update")

    #----------------------------------------------------------------------
    def updateProgress(self, msg):
        """"""
        print(msg)
        self.count += 1

        if self.count >= self.length:
            self.Destroy()

        self.progress.SetValue(self.count)
