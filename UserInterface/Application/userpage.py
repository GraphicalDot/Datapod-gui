
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from faker import Faker
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListItemButton, ListItemLabel, \
CompositeListItem, ListView
from kivy.properties import ObjectProperty
from Application.table import MTable
from os.path import sep, expanduser, isdir, dirname
from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.popup import Popup
import subprocess
#from DecentralizeFileSystem.ipfs_decentralize_filesystem import IPFS
from LoggingModule.logging import logger_log
from SettingsModule import global_variables
import os
import requests
from kivy.garden.navigationdrawer import NavigationDrawer




from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.app import App
from kivy.lang import Builder

from kivymd.navigationdrawer import NavigationDrawerIconButton
from kivymd.theming import ThemeManager
from kivymd.toast import toast


fake = Faker()


data =  [{"file_name": fake.file_name(), "stored_on": fake.date(), "location": fake.sha1() } for i in range(50)]


#f = MTable(data, cols=4)





class UserPage(Screen):
    ##IPFSListButton now you can access it in .kv file by referring as root.IPFSListButton
    data_items = ObjectProperty([])
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    ipfs_node_id = StringProperty("")
    encryption_public_key = StringProperty("")
    passphrase= StringProperty("")
    file = 'Enter zip path or select it'
    data = ObjectProperty(None)
    #tab_1=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UserPage, self).__init__(**kwargs)
        #self.tab_1.bind(minimum_height=self.layout_content.setter('height'))
        #Clock.schedule_interval(self.update, 0)
        """
        if self.data:
            f = MTable(self.data, cols=4)
            self.ids.tab_1.add_widget(f)
        logger_log.debug("This is the data we are looking at %s"%self.data)
        Clock.schedule_interval(self.update, 1)
        """

    def on_start(self):
        for i in range(15):
            self.main_widget.ids.nav_drawer.add_widget(
                NavigationDrawerIconButton(
                    icon='checkbox-blank-circle', text="Item menu %d" % i,
                    on_release=lambda x, y=i: self.callback(x, y)))


    def update(self,*args):
            self.ids.tab_1.clear_widgets()
            f = MTable(self.data, cols=4)
            self.ids.tab_1.add_widget(f)
            
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Login'
        self.manager.get_screen('Login').resetForm()

    def on_cancel(self):

        self.go_to_login()
    


if __name__== "__main__":
    pass
    