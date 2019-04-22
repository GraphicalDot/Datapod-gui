
import wx
import wx.lib.agw.flatmenu as FM

class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "FlatMenu Demo")

        self.CreateMenu()

        panel = wx.Panel(self, -1)
        btn = wx.Button(panel, -1, "Hello", (15, 12), (100, 120))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.menubar, 0, wx.EXPAND)
        main_sizer.Add(panel, 1, wx.EXPAND)

        self.SetSizer(main_sizer)
        main_sizer.Layout()


    def CreateMenu(self):

        self.menubar = FM.FlatMenuBar(self, -1)

        f_menu = FM.FlatMenu()
        e_menu = FM.FlatMenu()
        v_menu = FM.FlatMenu()
        t_menu = FM.FlatMenu()
        w_menu = FM.FlatMenu()

        # Append the menu items to the menus
        f_menu.Append(-1, "Simple   Ctrl+N", "Text", None)
        e_menu.Append(-1, "FlatMenu", "Text", None)
        v_menu.Append(-1, "Example", "Text", None)
        t_menu.Append(-1, "Hello", "Text", None)
        w_menu.Append(-1, "World", "Text", None)

        # Append menus to the menubar
        self.menubar.Append(f_menu, "&File")
        self.menubar.Append(e_menu, "&Edit")
        self.menubar.Append(v_menu, "&View")
        self.menubar.Append(t_menu, "&Options")
        self.menubar.Append(w_menu, "&Help")


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()