# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.image import Image
import pickle
import time
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
import requests
import hashlib
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from EncryptionModule.symmetric import generate_scrypt_key, aes_encrypt, aes_decrypt
from instagram_api import instagram_login, get_all_posts
from kivy.properties import ObjectProperty, ListProperty, StringProperty


import datetime






store = JsonStore('config.json')



class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)



class MainApp(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "Decentralize oil field"
    mnemonic = StringProperty()
    address = StringProperty()    
    passphrase = StringProperty()    
    repeat_passphrase = StringProperty()    
    enabled_mnemonic = BooleanProperty(True)
    enabled_address = BooleanProperty(True)
    

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        #Window.bind(on_close=self.on_stop)

    def stop(self, *largs):
        # Open the popup you want to open and declare callback if user pressed `Yes`
        # popup = ExitPopup(title=TEXT_ON_CLOSE_APPLICATION,
        #                   content=Button(text=TEXT_ON_CLOSE_APPLICATION_BUTTON_CLOSE),
        #                   size=(400, 400), size_hint=(None, None)
        #                   )
        # popup.bind(on_confirm=partial(self.close_app, *largs))
        # popup.open()
        return 

    def build(self):
        self.main_widget =Builder.load_file(
            os.path.join(os.path.dirname(__file__), "./latest.kv")
        )
        self.theme_cls.theme_style = 'Dark'

        # self.theme_cls.theme_style = 'Dark'

        # self.main_widget.ids.text_field_error.bind(
        #     on_text_validate=self.set_error_message,
        #     on_focus=self.set_error_message)
        self.bottom_navigation_remove_mobile(self.main_widget)
        return self.main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)

    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar(text="This is a snackbar!").show()
        elif snack_type == 'button':
            Snackbar(text="This is a snackbar", button_text="with a button!", button_callback=lambda *args: 2).show()
        elif snack_type == 'verylong':
            Snackbar(text="This is a very very very very very very very long snackbar!").show()

    def show_example_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="This is a dialog with a title and some text. "
                               "That's pretty awesome right!",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a test dialog",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def show_example_long_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Lorem ipsum dolor sit amet, consectetur "
                               "adipiscing elit, sed do eiusmod tempor "
                               "incididunt ut labore et dolore magna aliqua. "
                               "Ut enim ad minim veniam, quis nostrud "
                               "exercitation ullamco laboris nisi ut aliquip "
                               "ex ea commodo consequat. Duis aute irure "
                               "dolor in reprehenderit in voluptate velit "
                               "esse cillum dolore eu fugiat nulla pariatur. "
                               "Excepteur sint occaecat cupidatat non "
                               "proident, sunt in culpa qui officia deserunt "
                               "mollit anim id est laborum.",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a long test dialog",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def get_time_picker_data(self, instance, time):
        self.root.ids.time_picker_label.text = str(time)
        self.previous_time = time

    def show_example_time_picker(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(time=self.get_time_picker_data)
        if self.root.ids.time_picker_use_previous_time.active:
            try:
                self.time_dialog.set_time(self.previous_time)
            except AttributeError:
                pass
        self.time_dialog.open()

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        self.root.ids.date_picker_label.text = str(date_obj)

    def show_example_date_picker(self):
        if self.root.ids.date_picker_use_previous_date.active:
            pd = self.previous_date
            try:
                MDDatePicker(self.set_previous_date,
                             pd.year, pd.month, pd.day).open()
            except AttributeError:
                MDDatePicker(self.set_previous_date).open()
        else:
            MDDatePicker(self.set_previous_date).open()

    def show_example_bottom_sheet(self):
        bs = MDListBottomSheet()
        bs.add_item("Here's an item with text only", lambda x: x)
        bs.add_item("Here's an item with an icon", lambda x: x,
                    icon='clipboard-account')
        bs.add_item("Here's another!", lambda x: x, icon='nfc')
        bs.open()

    def show_example_grid_bottom_sheet(self):
        bs = MDGridBottomSheet()
        bs.add_item("Facebook", lambda x: x,
                    icon_src='./assets/facebook-box.png')
        bs.add_item("YouTube", lambda x: x,
                    icon_src='./assets/youtube-play.png')
        bs.add_item("Twitter", lambda x: x,
                    icon_src='./assets/twitter.png')
        bs.add_item("Da Cloud", lambda x: x,
                    icon_src='./assets/cloud-upload.png')
        bs.add_item("Camera", lambda x: x,
                    icon_src='./assets/camera.png')
        bs.open()

    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False

    def on_close(self):
        print ("Clicked on closing application")
        Window.close()
        return True



    def on_start(self):
        print(self.main_widget.ids.scr_mngr)
        if store.get("mnemonic"):
            self.main_widget.ids.login_box.remove_widget(self.main_widget.ids.button_mnemonic)
            self.main_widget.ids.login_box.remove_widget(self.main_widget.ids.button_save_mnemonic)
            #self.main_widget.ids.login_box.remove_widget(self.main_widget.ids.address)
            self.main_widget.ids.login_box.remove_widget(self.main_widget.ids.repeat_passphrase)

            self.main_widget.ids.login_box.remove_widget(self.main_widget.ids.mnemonic)
            
            #self.main_widget.ids.login_box.add_widget(self.main_widget.ids.repeat_passphrase)
        else:
            self.main_widget.ids.login_box.remove_widget(self.main_widget.ids.button_login)


        return 

    def on_instagram_login(self, username, password):
        __list = Factory.Lists()
        for i in range(30):
            __list.ids.scroll.add_widget(
                Factory.ListItemWithCheckbox(text='Item %d' % i))
        return 

        """
        try:
            instagram_object = instagram_login(username.text, password.text)
            max_id, posts = get_all_posts(instagram_object)
            print (posts)
            with open("instagram.data","wb") as f:
                pickle.dump(posts, f)
            store.put("instagram", max_id=max_id, time_zone=time.tzname, 
                last_fetch_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                last_fetch_local=datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
                 )
        except:
            Snackbar(text="Please check your instragram username and password again").show()
        """
        return 
        


    def on_show_mnemonic(self):
        """
        Show mnemonic after fetching it from local storage 
        """
        self.main_widget.ids.login_box.add_widget(self.main_widget.ids.mnemonic)



    def on_login(self, passphrase):
        encrypted = store.get("mnemonic")
        encrypted_mnemonic = encrypted["value"]
        salt = encrypted["salt"]

        
        scrypt_key, salt = generate_scrypt_key(passphrase.text, bytes.fromhex(salt))
        print (f"scrypt_key from password {scrypt_key.hex()} and salt is {salt.hex()}")

        print (f"Encrypted Mnemonic is {encrypted_mnemonic}")

        try:
            result = aes_decrypt(scrypt_key, bytes.fromhex(encrypted_mnemonic))
        except Exception as e:
            print ("Error ")
            print (e)
            Snackbar(text="Password entered is wrong").show()

        print (result)        
        store.put("password", value=passphrase.text)
        return 

    def on_save(self, passphrase, repeat_passphrase):
        if not self.mnemonic:
            Snackbar(text="PLease generate a New mnemonic").show()
            return 
        if passphrase.text != repeat_passphrase.text or not passphrase.text:
            Snackbar(text="Passphrases must match").show()
            return  

        if len(passphrase.text) <  8:
            Snackbar(text="Passphrases must be at least 8 characters long").show()
            return  


        scrypt_key, salt = generate_scrypt_key(passphrase.text)
        encrypted_mnemonic = aes_encrypt(scrypt_key, self.mnemonic)

        store.put("mnemonic", value=encrypted_mnemonic.hex(), salt=salt.hex())
        store.put("address", value=self.address)
        return

    def generate_mnemonic(self):
        """
        Make an api request with the data to confirm the user registraion
        After succesful registration reset the form 
        """
        #TODO form validation with cerberus
        #TODO Check if macid is available from the host or not
        #TODO check if ip address

        r = requests.get(f"http://{store.get('GO_API')}/get_mnemonic")
        mnemonic = r.json()["data"]["mnemonic"]
        zeroth_private_key = r.json()["data"]["zeroth_private_key"]
        zeroth_public_key = r.json()["data"]["zeroth_public_key"]

        master_private_key = r.json()["data"]["master_private_key"]
        master_public_key = r.json()["data"]["master_public_key"]

        self.mnemonic = mnemonic 
        self.address = hashlib.sha256(zeroth_public_key.encode()).hexdigest()
        return 

class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass

def main():

    Config.set('graphics', 'width', '1000')
    Config.set('graphics', 'height', '600')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.write()
    Window.borderless = True
    #Window.clearcolor = utils.rgba("#1E1F26")
    app = MainApp()
    app.run()


if __name__ == "__main__":
    #logger_logger.debug("This is the password text %s"%"passwordText")
    #logger_logger.info("This is the password text %s"%"passwordText")
    #logger_logger.error("This is the password text %s"%"passwordText")
    #logger_logger.warning("This is the password text %s"%"passwordText")
    from kivy.config import Config
    import os
    from kivy.core.window import Window
    main() 

