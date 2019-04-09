
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.storage.jsonstore import JsonStore
import hashlib

store = JsonStore('feynmen.json')
class ForgotPassword(Screen):

    def on_submit(self, old_password, password, repeat_password):
        """
        Make an api request with the change in password
        After succeful registration reset the form 

        if password != repeat_password:
            raise StandardError("Passwords dont match")

        if store.exists("credentials"):
            username = store["credentials"].get('username')
            password = store["credentials"].get('password')

        else:
            #TODO show popup
            pass


        if hashlib.sha3_256(password.encode("utf-8")).hexdigest() != old_password:
            raise StandardError("")

        store.put("credentials", password=hashlib.sha3_256(password.encode("utf-8")).hexdigest())
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Login'
        self.manager.get_screen('Login').resetForm()
        return         
        """
        pass

    def on_cancel(self):

        self.go_to_login()


    def go_to_login(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'Login'
        self.manager.get_screen('Login').resetForm()
        return        