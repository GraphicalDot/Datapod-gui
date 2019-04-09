#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import uuid
from kivy.properties import StringProperty, NumericProperty
from functools import partial


Builder.load_string("""
<PlayerRecord>:
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]

    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            pos: self.pos
            size: self.size

<TableHeader>
    size_hint_y: None
    height: '30dp'
    width: '100dp'

    canvas.before:
        Color:
            rgb: 0.5, 0.5, 0.5
        Rectangle:
            pos: self.pos
            size: self.size


<MTable>:
    
    cols: 4
    size_hint_y: None
    height: self.minimum_height
    spacing: '1dp'
""")


class TableHeader(Label):
    pass


class PlayerRecord(Label):
    pass


class MTable(GridLayout):

    def __init__(self, data, **kwargs):
        super(MTable, self).__init__(**kwargs)

        self.data = data
        self.display_scores()

    def fetch_data_from_database(self):
        self.data = [
            {'name': 'name', 'score': 'score', 'car': 'car'},
            {'name': 'przyczajony', 'score': '1337', 'car': 'Fiat 126p'},
            {'name': 'Krusader Jake', 'score': '777', 'car': 'Ford'},
            {'name': 'dummy', 'score': '10', 'car': 'none'},
            {'name': 'Last', 'score': '880', 'car': 'none'}
        ]

    def display_scores(self):
        self.clear_widgets()
        for i in range(len(self.data)):
            if i < 1:
                row = self.create_header()
            else:
                row = self.create_player_info(i)
            for item in row:
                self.add_widget(item)

    def create_header(self):
        keys = ["File name", "File size", "Ipfs hash"]
        first_column = TableHeader(text=keys[0])
        second_column = TableHeader(text=keys[1])
        third_column = TableHeader(text=keys[2])
        
        fourth_column = TableHeader(text="action")
        return [first_column, second_column, third_column, fourth_column]

    def create_player_info(self, i):
        first_column = PlayerRecord(text=self.data[i]['file_name'])
        second_column = PlayerRecord(text=self.data[i]['file_size'])
        third_column = PlayerRecord(text=self.data[i]['ipfs_hash'])
        fourth_column = Button(text="edit")
        fourth_column.bind(on_press=partial(self.on_enter, self.data[i]))
        return [first_column, second_column, third_column, fourth_column]

    def on_enter(self, *args):
        print (args[0])

class MyPaintApp(App):

    data =    [
            {'name': 'name', 'score': 'score', 'car': 'car'},
            {'name': 'przyczajony', 'score': '1337', 'car': 'Fiat 126p'},
            {'name': 'Krusader Jake', 'score': '777', 'car': 'Ford'},
    ]
    def build(self):
        return MTable(self.data, cols=4)

if __name__ == '__main__':
    pass
    #MyPaintApp().run()