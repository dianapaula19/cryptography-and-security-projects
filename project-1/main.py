from kivymd.app import MDApp
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

from kivy.uix.popup import Popup

import util as u

from os.path import join, isdir

import os
import sys

class FileChoosePopup(Popup):
    load = ObjectProperty()
    
class DirectoryChoosePopup(Popup):
    load = ObjectProperty()
    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))

class MainLayout(AnchorLayout):
    
    dialog = ObjectProperty(None)
    file_path = StringProperty("")
    directory_path = StringProperty("")
    plaintext = StringProperty("")
    file_popup = ObjectProperty(None)
    directory_popup = ObjectProperty(None)
    caesar_key = StringProperty("")
    otp_key = StringProperty("")
    pressed_encrypt_button = BooleanProperty(False)
    pressed_decrypt_button = BooleanProperty(False)

    def open_choose_file_popup(self):
        self.file_popup = FileChoosePopup(load=self.load_file)
        self.file_popup.open()
        
    def open_choose_directory_popup(self):
        self.directory_popup = DirectoryChoosePopup(load=self.load_directory)
        self.directory_popup.open()

    def load_file(self, selection):
        self.file_path = str(selection[0])
        self.file_popup.dismiss()

        if self.file_path:
            self.ids.get_file.text = self.file_path
            try:
                file = open(self.file_path, "r")
                self.plaintext = file.read()
                file.close()
            except PermissionError:
                self.show_alert("You don't have permission to access this file")
    
    def reset(self):
        self.pressed_encrypt_button = False
        self.pressed_decrypt_button = False
        self.plaintext = ""
    
    def load_directory(self, selection):
        self.directory_path = str(selection[0])
        self.directory_popup.dismiss()
        print(self.directory_path)
        if self.directory_path:
            try:
                u.write_file(self.directory_path, self.plaintext, int(self.caesar_key), self.otp_key, self.pressed_decrypt_button)
                self.restart()
            except PermissionError:
                self.show_alert("You don't have permission to access this directory")
    
    def save_caesar_key(self, widget):
        if not widget.text.isnumeric() or (int(widget.text) < 0 or int(widget.text) > 26):
            self.show_alert("Please enter a number between 0 and 25!")
            self.caesar_key = ""
        else:
            self.caesar_key = widget.text
    
    def save_otp_key(self, widget):
        if len(widget.text) < len(self.plaintext):
            self.show_alert("Please enter a key longer than the plaintext!")
            self.otp_key = ""
        else:
            self.otp_key = widget.text
    
    def encrypt(self):
        self.pressed_encrypt_button = True
    
    def decrypt(self):
        self.pressed_decrypt_button = True
        
    def show_alert(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDFlatButton(
                        text="Dismiss",
                        on_release=self.close_dialog
                    ),
                ],
            )
        else:
            self.dialog.text = message
        self.dialog.open()
    
    def close_dialog(self, obj):
        self.dialog.dismiss()
    
    def restart(self):
        print(f'exec: {sys.executable} {["python"] + sys.argv}')
        os.execvp(sys.executable, ['python'] + sys.argv)
    

class MainApp(MDApp):
    def build(self):
        self.title = "Encryption Tool"
        return MainLayout()
        

if __name__ == "__main__":
    app = MainApp()
    app.run()