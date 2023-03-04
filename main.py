import hashlib
from webbrowser import open_new

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

import qrcode

Window.clearcolor = (242/255, 226/255, 249/255, 1)


class codeQRcreator(App):
    url = ""

    def create_QR_code(self, text):
        img = qrcode.make(text)
        filename_binary = f'{text}'.encode('utf-8')
        filename_hash = hashlib.md5(filename_binary).hexdigest()
        img.save(f"QRcode-{filename_hash}.png")
        self.image.source = f"QRcode-{filename_hash}.png"

    def build(self):
        self.icon = "codeQRcreator-icon.png"
        self.screen = Screen()
        self.image = AsyncImage(
            source=self.url,
            size_hint_x=0.4,
            size_hint_y=0.4,
            pos_hint={"center_x": .5, "center_y": .75},
            color=(242/255, 226/255, 249/255, 1)
        )
        self.screen.add_widget(self.image)
        self.textinput = TextInput(
            hint_text="Enter your text ",
            hint_text_color=(0, 0.25, 0.35, 1),
            foreground_color=(0.45, 0.005, 0.35, 1),
            font_size=18,
            background_color=(222/255, 206/255, 229/255, 0.25),            size_hint_x=0.8,
            size_hint_y=0.1,
            pos_hint={"center_x": .5, "center_y": .45},
        )
        self.screen.add_widget(self.textinput)
        self.button = Button(
            text="create",
            background_color=(0, 1.0, 1.0, 1),
            size_hint_x=0.15,
            size_hint_y=0.075,
            pos_hint={"center_x": .5, "center_y": .3},
            on_press=self.getdata
        )
        self.screen.add_widget(self.button)
        self.bookmark = Button(
            text="made by - dshaw0004",
            background_color=(0, 0, 0, 0),
            color=(0.0, 0.0, 1, 1),
            size_hint_x=0.2,
            size_hint_y=0.1,
            pos_hint={"center_x": 0.8, "center_y": .05},
            on_press=lambda e: open_new(url="https://github.com/dshaw0004")
        )
        self.screen.add_widget(self.bookmark)
        return self.screen

    def getdata(self, *args):
        input_text = self.textinput.text
        self.create_QR_code(text=input_text)


codeQRcreator().run()
