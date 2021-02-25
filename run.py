#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string

#theme
sg.theme('LightGrey1')


tab1_layout =  [[sg.T('Output of Scan X',size=(210,20), background_color=('lightgrey'))]]
tab2_layout =  [[sg.T('Output of Scan Y',size=(210,20), background_color=('lightgrey'))]]

contentRun = []
contentScan = []


for i in range(15):
    contentScan.append([sg.Text('Scan'), sg.Text('Name of Scan 0000'), sg.Text('Execution Number 0000'), sg.Text('Start Time 0000'), sg.Text('End Time 0000'), sg.Text('Scanned IPs'), sg.Text('Sucessful Execution/Failure'), sg.Button('Start'), sg.Button('Pause'), sg.Button('Stop') ])

scanCol = [
        #[sg.Text('Scan List', font=('none 16'),size=(20,1))],
        [sg.Text('Scan', text_color= 'black', background_color= 'lightgrey'), sg.Text('Name of Scan ▲ ▼', text_color= 'black', background_color= 'lightgrey'), sg.Text('Execution Number ▲ ▼', text_color= 'black', background_color= 'lightgrey'), sg.Text('Start Time ▲ ▼', text_color= 'black', background_color= 'lightgrey'), sg.Text('End Time ▲ ▼', text_color= 'black', background_color= 'lightgrey'), sg.Text('Scanned IPs', text_color= 'black', background_color= 'lightgrey'), sg.Text('Sucessful Execution/Failure', text_color= 'black', background_color= 'lightgrey'), sg.Text('Control', text_color= 'black', background_color= 'lightgrey')],
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


#Run
for i in range(15):
    contentRun.append([sg.Text('Name of Run 0000'), sg.Text('Description of Run'), sg.Text('Result with Timestamp'), sg.Button('Start'), sg.Button('Pause'), sg.Button('Stop') ])


runCol = [
            #[sg.Text('Run List', font=('none 16'),size=(20,1))],
            [sg.Text('Name of Run ▲ ▼', text_color= 'black', background_color= 'lightgrey'), sg.Text('Description of Run', text_color= 'black', background_color= 'lightgrey'), sg.Text('Result with Timestamp', text_color= 'black', background_color= 'lightgrey'), sg.Text('Control', text_color= 'black', background_color= 'lightgrey')],
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

runConfigCol = [
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
        [sg.Text('Scan List', font=('none 16'),size=(20,1), pad=((0,620),(0,0))), sg.Text('Run List', font=('none 16'),size=(20,1))],
        #[sg.Column(NewSpinner)],
        [sg.Column(scanCol,scrollable=True), sg.Column(runCol, scrollable=True)],
        [sg.Column(runConfigCol, pad=((0,20),(10,0))), sg.Column(xmlCol, pad=((0,0),(0,0)))],
        #scan result table in tabs
        [sg.TabGroup([[sg.Tab('Scan X', tab1_layout, background_color='lightgrey'), sg.Tab('Scan Y', tab2_layout, background_color=('lightgrey'))]])]

        ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Run', layout)

#event loop
event, values = window.read()
