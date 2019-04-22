import wx
from pathlib import Path

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(300, 250))
        self.dir = Path.cwd().parent
        print (self.dir)




        #toolbar1.AddTool(wx.ID_ANY,  wx.Image(finance_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap())




        main_panel = wx.Panel(self)

        panel1 = wx.Panel(main_panel,-1, style=wx.SUNKEN_BORDER)
        panel2 = wx.Panel(main_panel,-1, style=wx.SUNKEN_BORDER)

        panel1.SetBackgroundColour("BLUE")
        panel2.SetBackgroundColour("RED")
        toolbar1 = wx.ToolBar(panel1, wx.TB_VERTICAL)
        home_path = str(self.dir.joinpath('home.png'))
        travel_path = str(self.dir.joinpath('travel.png'))
        finance_path = str(self.dir.joinpath('finance.png'))
        exit_path = str(self.dir.joinpath('exit.png'))
        #wx.StaticBitmap(self, -1, wx.Bitmap("path/image.png", wx.BITMAP_TYPE_ANY)
        toolbar1.SetToolBitmapSize((24, 24))
        
        toolbar1.AddTool(wx.ID_ANY, wx.Image(finance_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        toolbar1.AddTool(wx.ID_ANY,  wx.Image(finance_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
       
        toolbar1.Realize()


        #panel1.Add(toolbar1)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        #mainsizer.AddStretchSpacer()

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(panel1, 2, wx.EXPAND)
        box.Add(panel2, 1, wx.EXPAND)
        mainsizer.Add(box, 1, wx.EXPAND)

        main_panel.SetSizer(mainsizer)
        self.Layout()    

app = wx.App()
frame = MyFrame(None, -1, "Sizer Test")
frame.Show()
app.MainLoop()