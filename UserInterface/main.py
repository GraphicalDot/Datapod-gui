#!/usr/bin/env python3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.properties import StringProperty
from kivy.clock import Clock
import time
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from Application.userpage import UserPage
from user_registration import UserRegistration
from forgot_password import ForgotPassword
from kivy.storage.jsonstore import JsonStore
import hashlib
import six
import os
import sys
import requests
from SettingsModule.settings import api_server
from SettingsModule import global_variables
#from DecentralizeFileSystem.ipfs_decentralize_filesystem import IPFS
from alert import Alert
from kivy.config import Config
from LoggingModule.logging import feynlog
#https://www.colorcombos.com/color-schemes/192/ColorCombo192.html
from kivy.core.window import Window



class LoginPage(Screen):
    def do_login(self, loginText, passwordText):

            
        app = App.get_running_app()
        print (app.get_application_config())

        app.username = loginText
        feynlog.info("This is the password text %s"%passwordText)
        app.password = hashlib.sha1(passwordText.encode("utf-8")).hexdigest()


        if app.username == "" or app.password == "":
            Alert(title='Feynmen error message', text='username and password cannot be left blank')
            return             

        ##This iwll check if the vm has runing ipfs connection or not, 
        ##if its running global_variables.ipfs_node_id is not None
    
        try:
            r = requests.post("%slogin"%api_server, data={"username": app.username, "password": app.password, "ipfs_node_id": global_variables.ipfs_node_id})
            global_variables.app_token = r.json()["data"]["token"]

        except Exception as e:
            feynlog.debug(str(e))
            Alert(title='Feynmen error message', text="Remote server id not responding")

        if not r.json()["success"]:
            feynlog.error("The user doesnt exists")
            content = Button(text='Close me!')
            popup = Popup(content=content, auto_dismiss=False)

            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)

            # open the popup
            popup.open()
        
            popup.open()
            
        try:
            r.json()["data"]["user"]
        except Exception as e:
            feynlog.debug(e)
            Alert(title='Feynmen error message', text=r.json()["message"])

        global_variables.username = app.username
        global_variables.password = app.password  
        global_variables.user_id = r.json()["data"]["user"]["user_id"]

        _class = IPFS()
        _class.check_filesystem()


        #feynlog.debug("This is the ipfs config file present on the node %s"%global_variables.ipfs_config)
        #feynlog.debug("This is the ipfs config file deleivered from the central server %s"%r.json()["data"]["user"]["ipfs_config"])


        


        if not r.json()["data"]["user"]["ipfs_config"]: #first time user
            _class.new_user()
        else:
            _class.repeated_user(r.json()["data"]["user"])

       ##Now we will get all the files that were stored by this user
        r = requests.get("http://localhost:8888/storage", params={"user_id": global_variables.user_id})    
        self.manager.add_widget(UserPage(name='User'))
        

        feynlog.debug(r.json()["data"])
        self.manager.get_screen('User').data = r.json()["data"]

        self.manager.get_screen('User').encryption_public_key = global_variables.encryption_public_key
        self.manager.get_screen('User').ipfs_node_id = global_variables.ipfs_node_id
        self.manager.get_screen('User').passphrase = global_variables.passphrase


 

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'User'

    def do_registration(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'UserRegistration'    

    def do_forgot_password(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'ForgotPassword'    

    def resetForm(self):
        self.ids['username'].text = ""
        self.ids['password'].text = ""


class MainApp(App):
    username = StringProperty(None)
    password = StringProperty(None)
    
    def build(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        manager = ScreenManager()
        manager.add_widget(LoginPage(name='Login'))
        #manager.add_widget(UserPage(name='User'))
        manager.add_widget(UserRegistration(name='UserRegistration'))
        manager.add_widget(ForgotPassword(name='ForgotPassword'))
        self.title = "Decentralize computation framework"
        return manager
  


def main():
    Config.set('graphics', 'width', '1000')
    Config.set('graphics', 'height', '600')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.write()
    Window.borderless = False
    app = MainApp()
    app.run()


if __name__ == "__main__":
    #feynlogger.debug("This is the password text %s"%"passwordText")
    #feynlogger.info("This is the password text %s"%"passwordText")
    #feynlogger.error("This is the password text %s"%"passwordText")
    #feynlogger.warning("This is the password text %s"%"passwordText")
    main()    


