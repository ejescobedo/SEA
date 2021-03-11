#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string

#theme
sg.theme('LightGrey1')


#tool View
contentTool = []
headingsTool = ['Name of Tool', 'Description of Tool', 'Remove']
for i in range(15):
    contentTool.append([sg.Text('Name of Tool 0000'), sg.Text('Description of Tool'), sg.Button('Remove', button_color=('white','red'))])

toolCol = [[sg.Text('Name of Tool ▲ ▼', text_color= 'black', background_color= 'lightgrey'), sg.Text('Description of Tool', text_color= 'black', background_color= 'lightgrey'), sg.Text('Remove', text_color= 'black', background_color= 'lightgrey')],
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
        #[sg.Text('Tool Specification', font=('none 16'),size=(20,1))],
        [sg.Text('Tool Name', size=(20,1)), sg.InputText('')],
        [sg.Text('Tool Description', size=(20,1)), sg.InputText('')],
        [sg.Text('Tool Path', size=(20,1)), sg.InputText(''), sg.Button('Browse')],
        [sg.Text('Option and Argument', size=(20,1)), sg.InputText('')],
        [sg.Text('Output Data Specification', size=(20,1)), sg.InputText(''), sg.Button('Add')],
        [sg.Text('OR',font=('None 16'), size=(20,1))],
        [sg.Text('Tool Specification File', pad=((5,5),(20,5)),size=(20,1)), sg.InputText(''), sg.Button('Browse')]
        ]
toolListCol = [
            #Run Table
            #[sg.Text('Tool List', font=('none 16'))],
            [sg.Column(toolCol, scrollable=True)]]
toolDepCol = [
            #[sg.Text('Tool Dependency', font=('none 16'),size=(20,1))],
            [sg.Text('Dependent Data', size=(15,1)), sg.InputCombo(['X', 'Y'], size=(15, 1)), sg.Text('Operator', size=(0,0)), sg.InputCombo(['X', 'Y'], size=(15, 1)), sg.Text('Value', size=(0,0)), sg.InputText(''),sg.Button('Remove')],
            [sg.Text('Dependency Expression', size=(20,1)), sg.InputText('')],
            [sg.Button('Add')]
            ]

#run View
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
        #[sg.Text('Configuration of the Selected Run',font=('none 16'),size=(30,1))],
        [sg.Text('Run Name', size=(20,1)), sg.InputText('')],
        [sg.Text('Run Description', size=(20,1)), sg.InputText('')],
        [sg.Text('Whitelisted IP Target', size=(20,1)), sg.InputText('')],
        [sg.Text('Blacklisted IP Target', size=(20,1)), sg.InputText('')],
        [sg.Text('Scan Type', size=(20,1)), sg.InputCombo(['Scan Type', 'filler'], size=(20, 1)),sg.Button('Add')],
        [sg.Text('OR',font=('None 16'))],
        [sg.Text('Run Configuration File', size=(20,1)), sg.Button('Browse')],
        [sg.Button('Save', pad=((5,5),(30,5)), button_color=('black','white')), sg.Button('Cancel',button_color=('white','black'), pad=((5,5),(30,5)))]
        ]
xmlCol = [
        #[sg.Text('XML Report', font=('none 16'),size=(20,1))],
        [sg.Text('Report Name', size=(15,1)), sg.InputText('')],
        [sg.Text('Report Description', size=(15,1)), sg.InputText('')],
        [sg.Text('Run', size=(15,1)), sg.InputCombo(['X', 'Y'], size=(15, 1)),sg.Button('Add')],
        [sg.Text('OR', font=('None 16'), size=(15,1))],
        [sg.Text('Run', size=(15,1)), sg.InputCombo(['Run X', 'Run Y'], size=(15, 1)),sg.Text('Scan'), sg.InputCombo(['Scan X', 'Scan Y'], size=(15, 1)),sg.Button('Remove', button_color=('white', 'red')), sg.Button('Add')],
        [sg.Button('Generate', pad=((5,5),(30,5)), button_color=('black','white')), sg.Button('Cancel', button_color=('white','black'), pad=((5,5),(30,5)))]
        ]

tab1_layout =  [[sg.T('Output of Scan X',size=(220,20))]]
tab2_layout =  [[sg.T('Output of Scan Y',size=(210,20))]]


outputTabCol = [
            [sg.TabGroup([[sg.Tab('Scan X', tab1_layout), sg.Tab('Scan Y', tab2_layout)]])]
            ]


scanFrame = [
            [sg.Frame('Scan', scanCol)]
            ]

runFrame = [
            [sg.Frame('Run', runCol)]
            ]
xmlFrame = [
            [sg.Frame('XML Report', xmlCol, pad=((3,370),(0,0)))]
            ]
runConfigFrame = [
            [sg.Frame('Configuration of the Selected Run', runConfigCol)]
            ]
toolListFrame = [
            [sg.Frame('Tool', toolListCol)]
            ]
specColFrame = [
            [sg.Frame('Tool Specification', specCol)]
            ]
toolDepColFrame = [
            [sg.Frame('Tool Dependency', toolDepCol)]
            ]
outputFrame = [
            [sg.Frame('Output', outputTabCol)]
            ]


run_tab_layout =  [

                #[sg.Text('Scan List', font=('none 16'),size=(20,1), pad=((0,620),(0,0))), sg.Text('Run List', font=('none 16'),size=(20,1))],
                #[sg.Column(NewSpinner)],
                [sg.Column(scanFrame, scrollable=(True), vertical_alignment=('Top')), sg.Column(runFrame, scrollable=(True))],
                #[sg.Column(runConfigCol, pad=((0,20),(10,0))), sg.Column(xmlCol, pad=((0,0),(0,0)))],
                [sg.Column(xmlFrame, vertical_alignment=('Top')), sg.Column(runConfigFrame, vertical_alignment=('Top'))],
                #scan result table in tabs
                [sg.Column(outputFrame)]
                #[sg.TabGroup([[sg.Tab('Scan X', tab1_layout), sg.Tab('Scan Y', tab2_layout)]])]
                ]
tool_tab_layout =  [
                [sg.Column(toolListFrame), sg.Column(specColFrame, vertical_alignment='top')],
                [sg.Column(toolDepColFrame)]

                ]


#window layout
layout = [
        [sg.TabGroup([[sg.Tab('Run', run_tab_layout, font=('none 24')), sg.Tab('Tool', tool_tab_layout)]])]

        ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Run', layout)

#event loop
event, values = window.read()
