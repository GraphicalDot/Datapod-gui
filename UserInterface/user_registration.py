

#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooser, FileChooser
from kivy.uix.floatlayout import FloatLayout
from os.path import sep, expanduser, isdir, dirname
from kivy.garden.filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.popup import Popup
from alert import Alert
from SettingsModule.settings import api_server
import requests
import re
from LoggingModule.logging import logger_log
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
import os
import hashlib
from EncryptionModule.symmetric import generate_scrypt_key, aes_encrypt

##THe documentation for this function which were copied are present at https://kivy.org/docs/api-kivy.uix.filechooser.html
import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
def str_to_class(str):
    return getattr(sys.modules[__name__], str)

store = JsonStore('config.json')





class UserRegistration(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    mnemonic = StringProperty()
    address = StringProperty()
    file = 'enter zip path or select it'
    
    def open(self, textfield_id):
        self.popup = Popup(title='Test popup',
                  content=self.explorer(),
                  size_hint=(None, None), size=(600, 600))
        self.popup.open()
        self.textid = textfield_id
    def explorer(self):
        if platform == 'win':
            user_path = dirname(expanduser('~')) + sep + 'Documents'
        else:
            user_path = expanduser('~') + sep + 'Documents'
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
        self.popup.dismiss()

    def on_save(self, passphrase, repeat_passphrase):
        # if store.get("mnemonic"):
        #     print ("Mnemonic exists")
        #     print (store.get("mnemonic"))
        #     return 


        if passphrase.text != repeat_passphrase.text or not passphrase.text:
            Alert(title='Error message', text='Passphrases must match')
            return  

        if len(passphrase.text) <  8:
            Alert(title='Error message', text='Passphrases must be at least 8 characters long')
            return  

        if not self.mnemonic:
            Alert(title='Error message', text='PLease generate a New mnemonic')
            return 


        scrypt_key, salt = generate_scrypt_key(passphrase.text)
        encrypted_mnemonic = aes_encrypt(scrypt_key, self.mnemonic)

        store.put("mnemonic", value=encrypted_mnemonic.hex(), salt=salt.hex())

        print (store.get("mnemonic"))

        self.go_to_login()
        return

    def on_submit(self):
        """
        Make an api request with the data to confirm the user registraion
        After succesful registration reset the form 
        """
        #TODO form validation with cerberus
        #TODO Check if macid is available from the host or not
        #TODO check if ip address
        app = App.get_running_app()
        print (app.get_application_config())
        print (app.config)

        r = requests.get(f"http://{store.get('GO_API')}/get_mnemonic")
        mnemonic = r.json()["data"]["mnemonic"]
        zeroth_private_key = r.json()["data"]["zeroth_private_key"]
        zeroth_public_key = r.json()["data"]["zeroth_public_key"]


        master_private_key = r.json()["data"]["master_private_key"]
        master_public_key = r.json()["data"]["master_public_key"]



        self.mnemonic = mnemonic 
        self.address = hashlib.sha256(zeroth_public_key.encode()).hexdigest()

        """
        print (username, password, repeat_password, email, phone_number)
        if password != repeat_password:
            Alert(title='Feynmen error message', text='Password must match')
            return    

        if len(password) < 7:
            Alert(title='Feynmen error message', text='Password length must be greater then 7')
            return    

        if len(phone_number) < 10:
            Alert(title='Feynmen error message', text='Phone number must be valid')
            return    

        addressToVerify ='infoemailhippo.com'
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
        if match == None:
            feynlog.error('Bad Syntax for the Email id ')
            Alert(title='Feynmen error message', text='Please enter a valid email id')


        payload = {"username": username, "password": password, "email": email, "phone_number": phone_number}
        try:
            r = requests.post("%sregistration"%api_server, data=payload)
        except Exception as e:
            feynlog.debug(str(e))
            Alert(title='Feynmen error message', text="Remote server id not responding")
            
            
        
        feynlog.debug(r.json())
        Alert(title='Feynmen error message', text=r.json()["message"])
        
        self.go_to_login()
        """
        return        
    
    def on_cancel(self):

        self.go_to_login()


    def go_to_login(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Login'
        self.manager.get_screen('Login').resetForm()
        return        
        
    
   