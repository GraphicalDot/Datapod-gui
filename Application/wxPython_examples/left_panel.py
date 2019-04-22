

import wx
import wx.grid as gridlib
from pathlib import Path
########################################################################
class LeftPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        languages = ['C', 'C++', 'Java', 'Python', 'Perl',
            'JavaScript', 'PHP' ,'VB.NET' ,'C#'] 
        lst = wx.ListBox(self, size = (100,300), choices = languages, style = wx.LB_SINGLE) 
            
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        hbox1.Add(lst,1) 
        #self.Bind(wx.EVT_LISTBOX, self.onListBox, lst) 

        self.SetSizer(hbox1) 


    def onListBox(self, event): 
        self.text.AppendText( "Current selection: " + 
        event.GetEventObject().GetStringSelection() +"\n")
        self.Centre()

  
 