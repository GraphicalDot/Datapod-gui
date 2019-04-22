

import wx
from left_panel import LeftPanel
from right_panel import RightPanel




#           box = wx.BoxSizer(wx.VERTICAL)
#            
#            m_text = wx.StaticText(panel, -1, "Hello World!")
#            m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
#            m_text.SetSize(m_text.GetBestSize())
#            box.Add(m_text, 0, wx.ALL, 10)
#           
#           m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
#           m_close.Bind(wx.EVT_BUTTON, self.OnClose)
#           box.Add(m_close, 0, wx.ALL, 10)
#        
#           panel.SetSizer(box)
#           panel.Layout()




########################################################################
class Application(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(900, 500))
        splitter = wx.SplitterWindow(self, -1) 
        
        
        """
        panel1 = wx.Panel(splitter, -1) 
        b = wx.BoxSizer(wx.HORIZONTAL) 
        
        self.text = wx.TextCtrl(panel1,style = wx.TE_MULTILINE) 
        b.Add(self.text, 1, wx.EXPAND) 
        
        panel1.SetSizerAndFit(b)
        """
        panel1 = LeftPanel(splitter)
        
        panel2 = RightPanel(splitter) 

        splitter.SetMinimumPaneSize(150)
        splitter.SplitVertically(panel2, panel1) 
        self.Centre() 
        self.Show(True)  
        
    

#----------------------------------------------------------------------
# Run the program
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = Application()
#     frame.Show()
#     app.MainLoop()

class MyApp(wx.App):
    def OnInit(self):
        frame = Application(None, -1, 'Nova')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()