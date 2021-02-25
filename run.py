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
contentRun = []
contentScan = []
#Scan
#Run Col

for i in range(15):
    contentScan.append([sg.Text('Scan'), sg.Text('Name of Scan'), sg.Text('Execution Number'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Scanned IPs'), sg.Text('Sucessful Execution/Failure'), sg.Text('Control'),sg.Button('Start'), sg.Button('Pause'), sg.Button('Stop') ])

scanCol = [[sg.Text('Scan', text_color= 'blue', background_color= 'black'), sg.Text('Name of Scan', text_color= 'blue', background_color= 'black'), sg.Text('Execution Number', text_color= 'blue', background_color= 'black'), sg.Text('Start Time', text_color= 'blue', background_color= 'black'), sg.Text('End Time', text_color= 'blue', background_color= 'black'), sg.Text('Scanned IPs', text_color= 'blue', background_color= 'black'), sg.Text('Sucessful Execution/Failure', text_color= 'blue', background_color= 'black'), sg.Text('Control', text_color= 'blue', background_color= 'black')],
           contentScan[0],
           contentScan[1],
           contentScan[2],
           contentScan[3],
           contentScan[4],
           contentScan[5],
           contentScan[6],
           contentScan[7],
           contentScan[8],
           contentScan[9]]


#Run Spinners
NewSpinner = []
for i in range(4):
    NewSpinner.append([sg.Input("Scan", size=(3, 1), font='Any 12', justification='r', key='-SPIN-'),
                      sg.Column([[sg.Button('▲', size=(1, 1), font='Any 7', border_width=0,
                    button_color=(sg.theme_text_color(), sg.theme_background_color()), key='-UP-')],
                    [sg.Button('▼', size=(1, 1), font='Any 7', border_width=0,
                    button_color=(sg.theme_text_color(), sg.theme_background_color()), key='-DOWN-')]])])
#Run
for i in range(15):
    contentRun.append([sg.Text('Name of Run'), sg.Text('Description of Run'), sg.Text('Result with Timestamp'), sg.Button('Start'), sg.Button('Pause'), sg.Button('Stop') ])

#[sg.Text('Name of Run', text_color= 'blue', background_color= 'black'), sg.Text('Description of Run', text_color= 'blue', background_color= 'black'), sg.Text('Result with Timestamp', text_color= 'blue', background_color= 'black'), sg.Text('Control', text_color= 'blue', background_color= 'black')],

runColu = [[sg.Text('Name of Run', text_color= 'blue', background_color= 'black'), sg.Text('Description of Run', text_color= 'blue', background_color= 'black'), sg.Text('Result with Timestamp', text_color= 'blue', background_color= 'black'), sg.Text('Control', text_color= 'blue', background_color= 'black')],

           contentRun[0],
           contentRun[1],
           contentRun[2],
           contentRun[3],
           contentRun[4],
           contentRun[5],
           contentRun[6],
           contentRun[7],
           contentRun[8],
           contentRun[9]]





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
        [sg.Column(scanCol, scrollable=True), sg.Column(runColu, scrollable=True)],
        [sg.Column(runCol, pad=((0,20),(10,0))), sg.Column(xmlCol, pad=((0,0),(0,0)))],
         #                                                    )],
          #scan result table in tabs
          [sg.TabGroup([[sg.Tab('Scan X', tab1_layout, tooltip='tip'), sg.Tab('Scan Y', tab2_layout)]], tooltip='TIP2')]
          ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Run', layout, size=(1600, 1000))

#event loop
event, values = window.read()