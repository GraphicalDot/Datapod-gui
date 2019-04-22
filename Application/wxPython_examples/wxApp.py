
#!/usr/bin/python

# menu1.py

import wx


class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)


class MyMenu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(900, 500))
        panel = wx.Panel(self, -1)
        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        _help = wx.Menu()
        file.Append(101, '&Open', 'Open a new document')
        file.Append(102, '&Save', 'Save the document')
        file.AppendSeparator()
        _quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application', wx.ITEM_NORMAL)
        #quit.SetBitmap(wx.Image('stock_exit-16.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        file.Append(_quit)

        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(_help, '&Help')


        submenu = wx.Menu()
        submenu.Append(301, 'radio item1', kind=wx.ITEM_RADIO)
        submenu.Append(302, 'radio item2', kind=wx.ITEM_RADIO)
        submenu.Append(302, 'radio item3', kind=wx.ITEM_RADIO)


        edit.Append(203, 'submenu', submenu)

        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        self.Centre()
    
    def OnInit(self):
        print ("App started")
        dia = MyDialog(None, -1, "simpledialog.py")
        dia.ShowModal()
        dia.Destroy()
        return True

class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, 'menu1.py')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()