#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string

#theme
sg.theme('LightGrey1')

#stuff for table - will get this from DB
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for __ in range(num_cols)]
    for i in range(1, num_rows):
        data[i] = [word(), *[number() for i in range(num_cols - 1)]]
    return data

#making the table
data = make_table(num_rows=15, num_cols=4)
data2 = make_table(num_rows=15, num_cols=8)

headingsTool = ['Name of Tool', 'Description of Tool', 'Remove']

contentTool = []
for i in range(15):
    contentTool.append([sg.Text('Name of Tool'), sg.Text('Description of Tool'), sg.Button('Remove')])

toolCol = [[sg.Text('Name of Tool', text_color= 'black', background_color= 'lightgrey'), sg.Text('Description of Tool', text_color= 'black', background_color= 'lightgrey'), sg.Text('Remove', text_color= 'black', background_color= 'lightgrey')],
           contentTool[0],
           contentTool[1],
           contentTool[2],
           contentTool[3],
           contentTool[4],
           contentTool[5],
           contentTool[6],
           contentTool[7],
           contentTool[8],
           contentTool[9]]


specCol = [
        [sg.Text('Tool Specification', font=('none 16'),size=(20,1))],
        [sg.Text('Tool Name', size=(20,1)), sg.InputText('')],
        [sg.Text('Tool Description', size=(20,1)), sg.InputText('')],
        [sg.Text('Tool Path', size=(20,1)), sg.InputText(''), sg.Button('Browse')],
        [sg.Text('Option and Argument', size=(20,1)), sg.InputText('')],
        [sg.Text('Output Data Specification', size=(20,1)), sg.InputText(''), sg.Button('Add')],
        [sg.Text('OR', size=(20,1))],
        [sg.Text('Tool Specification File', size=(20,1)), sg.InputText(''), sg.Button('Browse')]
        ]
toolListCol = [
            #Run Table
            [sg.Text('Tool List', font=('none 16'))],
            [sg.Column(toolCol, scrollable=True)]]

#window layout
layout = [
            [sg.Column(toolListCol), sg.Column(specCol, vertical_alignment='top')],
            [sg.Text('Tool Dependency', font=('none 16'),size=(20,1))],
            [sg.Text('Dependent Data', size=(15,1)), sg.InputCombo(['X', 'Y'], size=(15, 1)), sg.Text('Operator', size=(0,0)), sg.InputCombo(['X', 'Y'], size=(15, 1)), sg.Text('Value', size=(0,0)), sg.InputText(''),sg.Button('Remove')],
            [sg.Text('Dependency Expression', size=(20,1)), sg.InputText('')],
            [sg.Button('Add')]

        ]


#create window
window = sg.Window('SEA Tool Version 1.0 - Tool', layout)

#event loop
event, values = window.read()
