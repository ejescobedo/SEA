#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string


import pymongo
from bson import ObjectId

#theme
sg.theme('LightGrey1')

def remove_Tool(name):
    document = collection.delete_one({'Name of Tool': name})
    return document.acknowledged

def remove_depedency(name):
    collection = database['Tool Dependency']
    document = collection.delete_one({'Dependent Data': name})
    return document.acknowledged

def remove_tool_list(name):
    collection = database['Tool List']
    document = collection.delete_one({'Name of Tool': name})
    return document.acknowledged

def get_multiple_data(collection):
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)


##Database
connection = pymongo.MongoClient('localhost', 27017)
database = connection['mydb_01']
collection = database['Tool List']

#information = get_multiple_data(collection)


#adding data to collection
#Every time you run it it will create the data, even if it is the same information
#theme
sg.theme('LightGrey1')


data = []
headingsTool = ['Name of Tool', 'Description of Tool']
headingsTool2 = ['dumb', 'yes']

def make_table(num_cols):
    data = []
    i = 0
    information = get_multiple_data(collection)
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Name of Tool"), element.get("Description of Tool")]
        i += 1
    return data

# ------ Make the Table Data ------
data = make_table(num_cols=3)


toolCol = [
        [sg.Table(values=data[:][:], headings=headingsTool, max_col_width=500,
                                # background_color='light blue',
                                auto_size_columns=False,
                                col_widths = 90,
                                def_col_width = 90,
                                display_row_numbers=True,
                                justification='left',
                                num_rows=10,
                                alternating_row_color='#ededed',
                                key='-TABLE-',
                                row_height=25, enable_events= True,
                                tooltip='This is a table')]]

toolListCol = [
            #Run Table
            #[sg.Text('Tool List', font=('none 16'))],
            [sg.Column(toolCol, scrollable=True)],
            [sg.Text('Name of Tool', key='-toolConfigName-', size=(10,1)), sg.InputText('', key='-removeInput-'), sg.Button("Remove Configuration", button_color=('white', 'red'), key='-removeConfig-')]
            ]

specCol = [
        #[sg.Text('Tool Specification', font=('none 16'),size=(20,1))],
        [sg.Text('Tool Name', size=(20,1)), sg.InputText('', key='-spec1-')],
        [sg.Text('Tool Description', size=(20,1)), sg.InputText('', key='-spec2-')],
        [sg.Text('Tool Path', size=(20,1)), sg.InputText('', key='-spec3-'), sg.FileBrowse('Browse', key= '-toolPathBrowse-')],
        [sg.Text('Option and Argument', size=(20,1)), sg.InputText('', key='-spec4-')],
        [sg.Text('Output Data Specification', size=(20,1)), sg.InputText('',key='-spec5-'), sg.Button('Add', key='-addSpec-')],
        [sg.Text('OR',font=('None 16'), size=(20,1))],
        [sg.Text('Tool Specification File', pad=((5,5),(20,5)),size=(20,1)), sg.InputText(''), sg.FileBrowse('Browse', key= '-toolSpecificationFileBrowse')]
        ]


toolDepCol = [
            #[sg.Text('Tool Dependency', font=('none 16'),size=(20,1))],
            [sg.Text('Dependent Data', size=(15,1)), sg.InputCombo(['X', 'Y'], key='-toolData1-',size=(15, 1)), sg.Text('Operator', size=(0,0)), sg.InputCombo(['X', 'Y'], key='-toolData2-',size=(15, 1)), sg.Text('Value', size=(0,0)), sg.InputText('',key='-toolData3-')],
            [sg.Text('Dependency Expression', size=(20,1)), sg.InputText('', key='-toolData4-')],
            [sg.Button('Add', key= '-addConfig-'), sg.Button('Remove', button_color=('white', 'red'),key='-removeDependency-')]
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

tab1_layout =  [[sg.T('Output of Scan X',size=(220,15))]]
tab2_layout =  [[sg.T('Output of Scan Y',size=(210,15))]]



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
                [sg.Column(toolListFrame)],

                [sg.Column(specColFrame, vertical_alignment='top')],
                [sg.Column(toolDepColFrame)]]


#window layout
layout = [
        [sg.TabGroup([[sg.Tab('Run', run_tab_layout, font=('none 24')), sg.Tab('Tool', tool_tab_layout)]])]

        ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Run', layout)

#event loop


while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-addSpec-':
        print("Add clicked")
        if ((values['-spec1-'] != "") and (values['-spec2-'] != "") and (values['-spec3-'] != "")  and (values['-spec4-'] != "") and values['-spec5-'] != ""):
            data = data = {"Name of Tool": values['-spec1-'], "Description of Tool": values['-spec2-'], "Path of Tool": values['-spec3-']
                           , "Option and Argument of Tool": values['-spec4-'], "Output Data Specification of Tool"
                           : values['-spec5-']}
            collection.insert_one(data)
            data = make_table(3)
            window.FindElement('-TABLE-').Update(values=data)

            window['-spec1-'].update('')
            window['-spec2-'].update('')
            window['-spec3-'].update('')
            window['-spec4-'].update('')
            window['-spec5-'].update('')

            # for i in range (11, 16):
                # window[i].update("")
        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')

    if event == "-addConfig-":
        if ((values['-toolData1-'] != "") and (values['-toolData2-'] != "") and (values['-toolData3-'] != "") and (values['-toolData4-'] != "")):
            collection = database['Tool Dependency']
            data = data = {"Dependent Data": values['-toolData1-'], "Operator": values['-toolData2-'],
                           "Value": values['-toolData3-']
                , "Dependency Expression": values['-toolData4-']}
            collection.insert_one(data)
            window['-toolData1-'].update('')
            window['-toolData2-'].update('')
            window['-toolData3-'].update('')
            window['-toolData4-'].update('')

            # for i in range (17, 22):
            #     window[i].update("")
        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')
    if event == "-removeConfig-":
        #test = values['-removeInput-']
        #print(test)
        if (values["-removeInput-"] != ""):
            remove_tool_list(values["-removeInput-"])
            data = make_table(3)
            window.FindElement('-TABLE-').Update(values=data)
            window['-removeInput-'].update('')

    if event == "-removeDependency-":
        if (values['-toolData1-'] != ""):
            remove_depedency(values['-toolData1-'])
            window['-toolData1-'].update("")
