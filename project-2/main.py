from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

from kivy.uix.popup import Popup

from os.path import join, isdir


import os
import sys

from bbs import BBS

P = 30000000091
Q = 40000000003
seed = 5231783971

class DirectoryChoosePopup(Popup):
    load = ObjectProperty()
    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))

class MainLayout(AnchorLayout):
    
    dialog = ObjectProperty(None)
    
    file_size = StringProperty("")
    directory_path = StringProperty("")
    directory_popup = ObjectProperty(None)
    
    def open_choose_directory_popup(self):
        self.directory_popup = DirectoryChoosePopup(load=self.load_directory)
        self.directory_popup.open()
    
    def load_directory(self, selection):
        self.directory_path = str(selection[0])
        self.directory_popup.dismiss()
        print(self.directory_path)
        if self.directory_path:
            try:
                b = BBS(P, Q, seed)
                b.generate_binary_file(int(self.file_size), self.directory_path)
                self.show_alert("The file was generated succesfully!!! :)")
            except Exception as e:
                self.show_alert(":( An error occured:" + str(e))
            
            self.restart()
    
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
        
    def save_file_size(self, widget):
        if not widget.text.isnumeric() or int(widget.text) == 0:
            self.show_alert("Please enter a number larger than zero!")
            self.file_size = ""
        else:
            self.file_size = widget.text
            
    def restart(self):
        print(f'exec: {sys.executable} {["python"] + sys.argv}')
        os.execvp(sys.executable, ['python'] + sys.argv)
            
            
class MainApp(MDApp):
    def build(self):
        self.title = "Cryptographically-secure pseudorandom number generator: BBS"
        return MainLayout()
        

if __name__ == "__main__":
    app = MainApp()
    app.run()
    
    
    
        