import wx

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_right = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        driveList=["D:/", "E:/"]

        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)

        label = wx.StaticText(self, -1, "Audio Source") # Add type/name of source
        label.SetFont(font)
        label.SetSize(label.GetBestSize())
        self.combo1 = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=driveList)
        self.listbox = wx.ListBox(self, 1, size=(380, 220))
        vbox_left.Add(label, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vbox_left.Add(self.combo1, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 15)
        vbox_left.Add(self.listbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)

        label = wx.StaticText(self, -1, "Local Disk") # Add disk name
        label.SetFont(font)
        label.SetSize(label.GetBestSize())
        self.combo2 = wx.ComboBox(self, style=wx.CB_DROPDOWN, choices=driveList)
        self.listbox = wx.ListBox(self, 0, size=(380, 220))
        vbox_right.Add(label, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5)
        vbox_right.Add(self.combo2, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 15)       
        vbox_right.Add(self.listbox, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)

        hbox.Add(vbox_left, 0, wx.EXPAND | wx.LEFT, 20)
        hbox.Add(vbox_right, 0, wx.EXPAND | wx.RIGHT, 20)
        self.SetSizer(hbox)
        self.Layout()

########################################################################
class MyFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title='Notebooks')
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        page_one = PageOne(notebook)
        notebook.AddPage(page_one, 'Page 1')

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(main_sizer)
        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()