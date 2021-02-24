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

tab1_layout =  [[sg.T('Output of Scan X',size=(190,20))]]
tab2_layout =  [[sg.T('Output of Scan Y',size=(190,20))]]

headingsRun = ['Name of Run', 'Description of Run', 'Result with Timestamp', 'Control']
headingsScan = ['Scan', 'Name of Scan', 'Execution Number', 'Start Time', 'End Time', 'Scanned IPs', 'Succesful Execution/Failure', 'Control']

scanCol = [
        [sg.Table(values=data2[1:][:], headings=headingsScan, max_col_width=25,
                            # background_color='light blue',
                            auto_size_columns=True,
                            display_row_numbers=False,
                            justification='right',
                            num_rows=10,
                            alternating_row_color='lightgrey',
                            key='-TABLE2',
                            row_height=20,
                            tooltip='This is a table')]]

runCol = [
        [sg.Text('Configuration of the Selected Run',font=('none 16'),size=(30,1))],
        [sg.Text('Run Name', size=(20,1)), sg.InputText('')],
        [sg.Text('Run Description', size=(20,1)), sg.InputText('')],
        [sg.Text('Whitelisted IP Target', size=(20,1)), sg.InputText('')],
        [sg.Text('Blacklisted IP Target', size=(20,1)), sg.InputText('')],
        [sg.Text('Scan Type', size=(20,1)), sg.InputCombo(['Scan Type', 'filler'], size=(20, 1)),sg.Button('Add')],
        [sg.Text('OR')],
        [sg.Text('Run Configuration File', size=(20,1)), sg.Button('Browse')],
        [sg.Button('Save'), sg.Button('Cancel')]
        ]

xmlCol = [
        [sg.Text('XML Report', font=('none 16'),size=(20,1))],
        [sg.Text('Report Name', size=(15,1)), sg.InputText('')],
        [sg.Text('Report Description', size=(15,1)), sg.InputText('')],
        [sg.Text('Run', size=(15,1)), sg.InputCombo(['X', 'Y'], size=(15, 1)),sg.Button('Add')],
        [sg.Text('OR', size=(15,1))],
        [sg.Text('Run', size=(15,1)), sg.InputCombo(['Run X', 'Run Y'], size=(15, 1)),sg.Text('Scan'), sg.InputCombo(['Scan X', 'Scan Y'], size=(15, 1)),sg.Button('Remove')],
        [sg.Button('Add')],
        [sg.Button('Generate'), sg.Button('Cancel')]
        ]

#window layout
layout = [
        #Run Table
        [sg.Text('Run List', font=('none 16'),size=(20,1))],
        [sg.Table(values=data[1:][:], headings=headingsRun, max_col_width=25,
                    # background_color='light blue',
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification='right',
                    num_rows=10,
                    #pad=((0,20),(0,0)),
                    alternating_row_color='lightgrey',
                    key='-TABLE1',
                    row_height=20,
                    tooltip='This is a table'), sg.Column(scanCol)
             ],
          [sg.Column(runCol, pad=((0,20),(10,0))), sg.Column(xmlCol, pad=((0,0),(0,0)))],
          #scan result table in tabs
          [sg.TabGroup([[sg.Tab('Scan X', tab1_layout, tooltip='tip'), sg.Tab('Scan Y', tab2_layout)]], tooltip='TIP2')]
          ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Run', layout)

#event loop
event, values = window.read()
