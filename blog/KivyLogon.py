import kivy 
kivy.require('1.0.5') 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.button import Button 
from kivy.app import App 
from kivy.lang import Builder 
from kivy.uix.widget import Widget 
from kivy.properties import ObjectProperty, StringProperty 
Builder.load_file('sample_kivy.kv') 

class loginView(Widget): 
    status=ObjectProperty(None) 
    def validate(self,username,password): 
        if username == password: 
            print(username,password)
            self.clear_widgets() 
        else: 
            self.status.text="Login failed" 
class afterLogin(Widget): 
    def dumb(self): 
        l = BoxLayout(cols="2") 
        btn = Button(text="ad") 
        l.add_widget(btn) 
        print("flag")
class mainClass(App): 
    def build(self): 
        return loginView() 

if __name__ == '__main__': 
    mainClass().run() 