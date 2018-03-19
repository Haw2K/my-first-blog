from kivy.app import App
from kivy.uix.button import Button

from kivy.uix.boxlayout import BoxLayout

class BoxApp(App):
    def build(self):
        bl = BoxLayout(orientation='horizontal', padding = [50])

        bl.add_widget(Button(text='Button 1'))

        return bl

if __name__ == '__main__':
    BoxApp().run()