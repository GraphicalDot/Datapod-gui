
import wx
import wx.grid as gridlib
from pathlib import Path
class RightPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------


    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.images_dir = Path(__file__).parent.joinpath("images")
        """
        box = wx.BoxSizer(wx.VERTICAL)
        m_text = wx.StaticText(self, -1, "Hello World!")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)
        """
        #panel2 = wx.Panel(splitter, -1) 
            


        box = wx.BoxSizer(wx.VERTICAL) 
        
        #self.text = wx.TextCtrl(self,style = wx.TE_MULTILINE) 
        #b.Add(self.text, 1, wx.EXPAND) 
        
        #self.SetSizerAndFit(b)
        tb = wx.ToolBar(self, wx.ID_ANY, style=wx.VERTICAL|wx.TB_NODIVIDER|wx.TB_TEXT)
        tb.SetToolBitmapSize((9, 9))
        #tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        #tb.AddTool(-1, wx.Image('images/home.png'), 'Previous')
        home = tb.AddTool(wx.ID_ANY, "Home", wx.Bitmap(str(self.images_dir.joinpath("travel.png"))))
        self.Bind(wx.EVT_MENU, self.on_home, home)
        tb.AddSeparator()

        tb.AddTool(wx.ID_ANY, "settings", wx.Bitmap(str(self.images_dir.joinpath("home.png"))))
        tb.AddSeparator()


        tb.AddTool(wx.ID_ANY, "travel", wx.Bitmap(str(self.images_dir.joinpath("travel.png"))))
        tb.AddSeparator()

        tb.AddTool(wx.ID_ANY, "finance", wx.Bitmap(str(self.images_dir.joinpath("finance.png"))))
        tb.AddSeparator()


        # tb.AddTool(-1, wx.Image('images/settings.png'), 'Up one directory')
        # tb.AddSeparator()
        # tb.AddTool(-1, wx.Image('images/travel.png'), 'Home')
        # tb.AddSeparator()
        # tb.AddTool(-1, wx.Image('images/finance.png'), 'Refresh')
        # tb.AddSeparator()
        tb.Realize()
        tb.Fit()

        box.Add(tb, border=5)

        self.SetSizer(box)
        box.Layout()

    def on_home(self, event):
        print ("On Home clicked")