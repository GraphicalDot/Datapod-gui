import wx #For graphics' interface
import os #For operating system compatibility

class TextPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)

        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE) #Text area with multiline

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.control, 1, wx.EXPAND)
        self.SetSizer(sizer)

class GraphicsPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.BLACK)


class TopPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        text = TextPanel(self)
        main_sizer.Add(text, 1, wx.EXPAND)

        graphics = GraphicsPanel(self)
        main_sizer.Add(graphics, 1, wx.EXPAND)

        self.SetSizer(main_sizer)


class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):

        #SETUP
        wx.Frame.__init__(self, parent, wx.ID_ANY, title = "MyTitle", size = (550,300))
        self.dirname=''

        self.top_panel = TopPanel(self)

        #CREATE
        self.create_status_bar()
        self.create_menu_bar()


# FUNCTIONS
# ------------------------------------------------------------------------------
    def create_status_bar(self):
        self.CreateStatusBar() #A Statusbar at the bottom of the window


    def create_menu_bar(self):

    # File Menu
        filemenu= wx.Menu()

        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open file to edit")
        filemenu.AppendSeparator()
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", "Save the file")
        menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As", "Save the file with a new name")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate communication and close window")

    #The Menu Bar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") #Adding the "File" menu to the 'menuBar'
        self.SetMenuBar(menuBar)  #Adding the 'menuBar' to the Frame content

    #Event binding
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)

# EVENTS
# ------------------------------------------------------------------------------
    def OnExit(self, event):
        self.Close(True) #Close the frame


    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.panelA.control.SetValue(f.read())
            f.close()
        dlg.Destroy()


    def OnSave(self, event):
        f = open(os.path.join(self.dirname, self.filename), 'w')
        f.write(self.panelA.control.GetValue())
        f.close()


    def OnSaveAs(self, event):
        file_choices = "TXT (*.txt)|*.txt"
        dlg = wx.FileDialog(self, message = "Save file as...", defaultDir = os.getcwd(), defaultFile = self.filename, wildcard = file_choices, style = wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            f = open(os.path.join(dlg.GetDirectory(), dlg.GetFilename()), 'w')
            f.write(self.panelA.control.GetValue())
            f.close()


# RUN!
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.PySimpleApp(False)
    app.frame = MainWindow(None, wx.ID_ANY, "tSock - Adaptation Technologies")
    app.frame.Show()
    app.MainLoop()