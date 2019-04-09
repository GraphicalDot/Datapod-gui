
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
from LoggingModule.logging import feynlog
from SettingsModule import global_variables
import os
import requests


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
        if self.data:
            f = MTable(self.data, cols=4)
            self.ids.tab_1.add_widget(f)
        feynlog.debug("This is the data we are looking at %s"%self.data)
        Clock.schedule_interval(self.update, 1)


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
    
    def add(self, *args):
        self.ids['VIEWlist'].adapter.data.append('txt')


    def go_to_login(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Login'
        self.manager.get_screen('Login').resetForm()
        return  

    def open(self, textfield_id):
        self.popup = Popup(title='Test popup',
                  content=self.explorer(),
                   background = 'atlas://data/images/defaulttheme/button_pressed',
                  size_hint=(None, None), size=(1000, 600))
        self.popup.open()
        self.textid = textfield_id
    
    def explorer(self):
        if platform == 'win':
            user_path = dirname(expanduser('~'))
        else:
            user_path = expanduser('~') 
        browser = FileBrowser(select_string='Select',
                          favorites=[(user_path, 'Documents')])
        browser.bind(
                on_success=self._fbrowser_success,
                on_canceled=self._fbrowser_canceled)
        return browser

    def _fbrowser_canceled(self, instance):
        print ('cancelled, Close self.')
        self.popup.dismiss()

    def _fbrowser_success(self, instance):
        print(instance.selection[0])
        self.file = instance.selection[0]

        f = self.ids[self.textid]
        f.text = self.file
        feynlog.debug("This is the dile name %s"%f.text)
        self.popup.dismiss()

    def save_on_filesystem(self):
        f = self.ids[self.textid]
        file_path = f.text

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
    
        filesystem = IPFS()
        filesystem.store_data(file_path, file_name, file_size)
        
        ##Instead use some key value database pair
        r = requests.get("http://localhost:8888/storage", params={"user_id": global_variables.user_id})    
        feynlog.debug(r.json()["data"])
        self.data = r.json()["data"]

        self.update()

if __name__== "__main__":
    pass
    