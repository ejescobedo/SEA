#!/usr/bin/env python
import PySimpleGUI as sg
import os
import random
import string
import pymongo
from bson import ObjectId

# Custom theme
table_text_color = 'white'
table_background_color = '#282A2B'
table_alternate_row_color = '#1D1F21'
header_color = '#2A2C2E'
header_t_color = 'white'
titles = '#51A0D5'
titles2 = '#51A0D5'
relief = 'ridge'
title_location = 'nw'
border_width = 0
tab_border_width = 0
selected_row_colors = ('white','#51A0D5')

buttondefault = ('white', '#2A2C2E')
yellowbutton = ('white', '#E5B302')
buttondefault2 = ('white', '#51A0D5')

dark_theme = {'BACKGROUND': '#282A2B',
                'TEXT': 'white',
                'INPUT': '#656565',
                'TEXT_INPUT': 'white',
                'SCROLL': 'red',
                'BUTTON': ('white', '#2A2C2E'),
                'PROGRESS': ('white', '#333945'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

light_theme = {'BACKGROUND': '#323232',
                'TEXT': 'black',
                'INPUT': '#FFFFFF',
                'TEXT_INPUT': 'black',
                'SCROLL': 'red',
                'BUTTON': ('black', '#AACCF3'),
                'PROGRESS': ('white', '#333945'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}


# Add theme to dict
#sg.theme_add_new('Light', light_theme)
sg.theme_add_new('Dark', dark_theme)

#theme
sg.theme('Dark')

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
collectionScan = database['Scan List']
collectionRun = database['Run List']



data = []
headingsTool = ['Name of Tool', 'Description of Tool']
headingsScan = ['Scan', 'Name of Scan', 'Execution Number','Start Time', 'End Time', 'Scanned IPs', 'Sucessful Execution/Failure', 'Control']
headingsRun = ['Name of Run', 'Description of Run', 'Result with Timestemp', 'Control']

headingsTool2 = ['dumb', 'yes']

def makeToolConfigurationTable(num_cols):
    data = []
    i = 0
    information = get_multiple_data(collection)
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Name of Tool"), element.get("Description of Tool")]
        i += 1
    return data

def makeScanTable():
    num_cols = 9
    data = []
    i = 0
    information = get_multiple_data(collectionScan)
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Scan"), element.get("Name of Scan"), element.get("Execution Number"),
                   element.get("Start Time"), element.get("End Time"), element.get("Scanned IPs"),
                   element.get("Sucessful Execution/Failure"), element.get("Control")]
        i += 1
    return data

def makeRunTable():
    num_cols = 5
    data = []
    i = 0
    information = get_multiple_data(collectionRun)
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Name of Run"), element.get("Description of Run"), element.get("Result with Timestamp"),
                   element.get("Control")]
        i += 1
    return data

# ------ Make the Table Data ------
dataToolConfiguration = makeToolConfigurationTable(num_cols=3)
dataScan = makeScanTable()
dataRun = makeRunTable()

toolListCol = [
        [sg.Table(values=dataToolConfiguration[:][:], headings=headingsTool, max_col_width=500,
                                background_color=table_background_color,
                                auto_size_columns=False,
                                def_col_width = 90,
                                display_row_numbers=True,
                                justification='left',
                                num_rows=7,
                                pad=((0,0),(15,10)),
                                header_text_color = header_t_color,
                                selected_row_colors = selected_row_colors,
                                header_background_color = header_color,
                                text_color = table_text_color,
                                alternating_row_color=table_alternate_row_color,
                                key='-TABLE-',
                                row_height=25, enable_events= True,
                                tooltip='This is a table')],
        [sg.Button("Remove Configuration", button_color=(buttondefault), key='-removeConfig-'), sg.Button("Load Configuration", button_color=(buttondefault), key='-loadConfig-')]
        ]


specCol = [
        #[sg.Text('Tool Specification', font=('none 16'),size=(20,1))],
        [sg.Text('Tool Name', font=('None 12'),pad=((5,5),(30,5)), size=(20,1)), sg.InputText('', font=('None 12'),pad=((5,5),(30,5)), key='-spec1-')],
        [sg.Text('Tool Description', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key='-spec2-')],
        [sg.Text('Tool Path', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key='-spec3-'), sg.FileBrowse('Browse', button_color=(buttondefault), key= '-toolPathBrowse-')],
        [sg.Text('Option and Argument', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key='-spec4-')],
        [sg.Text('Output Data Specification', font=('None 12'),size=(20,1)), sg.InputText('',font=('None 12'),key='-spec5-')],
        [sg.Text('OR',font=('None 16'), size=(20,1))],
        [sg.Text('Tool Specification File', font=('None 12'),pad=((5,5),(20,5)),size=(20,1)), sg.InputText('', font=('None 12'),key= '-toolSpecificationFile-'), sg.FileBrowse('Browse', key= '-toolSpecificationFileBrowse')],
        [sg.Button('Add', button_color=(buttondefault), key='-addSpec-'), sg.Button('Update Configuration', button_color=(buttondefault),key='-updateConfig-')]
        ]


toolDepCol = [
            #[sg.Text('Tool Dependency', font=('none 16'),size=(20,1))],
            [sg.Text('Dependent Data', font=('None 12'),pad=((5,5),(30,5)),size=(15,1)), sg.InputCombo(['X', 'Y'], font=('None 12'),pad=((5,5),(30,5)),key='-toolData1-',size=(15, 1)), sg.Text('Operator', font=('None 12'),pad=((5,5),(30,5)),size=(0,0)), sg.InputCombo(['X', 'Y'], font=('None 12'),pad=((5,5),(30,5)),key='-toolData2-',size=(15, 1)), sg.Text('Value', font=('None 12'),pad=((5,5),(30,5)), size=(0,0)), sg.InputText('',font=('None 12'),pad=((5,5),(30,5)),key='-toolData3-')],
            [sg.Text('Dependency Expression', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key='-toolData4-')],
            [sg.Button('Add', button_color=(buttondefault),key= '-addConfig-'), sg.Button('Remove', button_color=(buttondefault),key='-removeDependency-')]
            ]

#run View
contentRun = []
contentScan = []

for i in range(15):
    contentScan.append([sg.Text('Scan'), sg.Text('Name of Scan 0000'), sg.Text('Execution Number 0000'), sg.Text('Start Time 0000'), sg.Text('End Time 0000'), sg.Text('Scanned IPs'), sg.Text('Sucessful Execution/Failure'), sg.Button('Start'), sg.Button('Pause'), sg.Button('Stop') ])



scanCol = [
    [sg.Table(values=dataScan[:][:], headings=headingsScan, max_col_width=500,
              background_color=table_background_color,
              auto_size_columns=False,
              def_col_width=10,
              pad=((0,0),(15,10)),
              display_row_numbers=True,
              header_text_color = header_t_color,
              header_background_color = header_color,
              justification='left',
              selected_row_colors = selected_row_colors,
              num_rows=7,
              text_color = table_text_color,
              alternating_row_color=table_alternate_row_color,
              key='-SCANTABLE-',
              row_height=25, enable_events=True,
              tooltip='This is a table')],
    [sg.Button('Start', button_color=(buttondefault)), sg.Button('Pause', button_color=(buttondefault)), sg.Button('Stop', button_color=(buttondefault))]
    ]



for i in range(15):
    contentRun.append([sg.Text('Name of Run 0000'), sg.Text('Description of Run'), sg.Text('Result with Timestamp'), sg.Button('Start'), sg.Button('Pause'), sg.Button('Stop') ])

runCol = [
    [sg.Table(values=dataRun[:][:], headings=headingsRun, max_col_width=500,
              background_color= table_background_color,
              auto_size_columns=False,
              def_col_width=25,
              display_row_numbers=True,
              pad=((0,0),(15,0)),
              header_text_color = header_t_color,
              header_background_color = header_color,
              text_color = table_text_color,
              justification='left',
              selected_row_colors = selected_row_colors,
              num_rows=7,
              alternating_row_color=table_alternate_row_color,
              key='-RUNTABLE-',
              row_height=25, enable_events=True,
              tooltip='This is a table')]]
runConfigCol = [
        #[sg.Text('Configuration of the Selected Run',font=('none 16'),size=(30,1))],
        [sg.Text('Run Name', font=('None 12'),pad=((5,5),(30,3)), size=(20,1)), sg.InputText('',font=('None 12'), pad=((5,5),(30,3)),key= '-runName-')],
        [sg.Text('Run Description', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key= '-runDescription-')],
        [sg.Text('Whitelisted IP Target', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key= '-whitelist-')],
        [sg.Text('Blacklisted IP Target', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key= '-blacklist-')],
        [sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.InputCombo(['Scan Type', 'filler'], font=('None 12'),size=(20, 1), key= '-scanType-')],
        [sg.Text('OR',font=('None 16'))],
        [sg.Text('Run Configuration File', font=('None 12'),pad=((5,5),(0,0)),size=(20,1)), sg.InputText('', font=('None 12'),key= '-runConfigurationFile-'),
         sg.FileBrowse('Browse',key= '-runConfigurationFileBrowse')],    ##Added!
        [sg.Button('Save', pad=((5,5),(10,0)), key= '-saveRunConfiguration-', button_color=(buttondefault)), sg.Button('Cancel', key= '-cancelRunConfiguration-',button_color=(buttondefault), pad=((5,5),(10,0)))]
        ]
xmlCol = [
        #[sg.Text('XML Report', font=('none 16'),size=(20,1))],
        [sg.Text('Report Name', font=('None 12'),pad=((5,5),(30,5)),size=(15,1)), sg.InputText('',font=('None 12'),size=(15,1),pad=((5,5),(30,5)))],
        [sg.Text('Report Description', font=('None 12'),size=(15,1)), sg.InputText('',font=('None 12'),size=(15,1))],
        [sg.Text('Run', font=('None 12'),size=(15,1)), sg.InputCombo(['X', 'Y'], font=('None 12'),size=(15, 1)),sg.Button('Add')],
        [sg.Text('OR', font=('None 16'), size=(15,1))],
        [sg.Text('Run', font=('None 12'),size=(15,1)), sg.InputCombo(['Run X', 'Run Y'], font=('None 12'),size=(15, 1)),sg.Text('Scan',font=('None 12'),), sg.InputCombo(['Scan X', 'Scan Y'],font=('None 12'), size=(15, 1)),sg.Button('Remove', button_color=(buttondefault)), sg.Button('Add')],
        [sg.Button('Generate',pad=((5,5),(30,5)), button_color=(buttondefault)), sg.Button('Cancel', button_color=(buttondefault), pad=((5,5),(30,5)))]
        ]

helpView = [
        [sg.Text('Scan List - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('Run List - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('XML Report - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('Configuration of the Selected Run - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('Output - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('Tool List - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('The Tool List displays a list of the already configured underlying tools.')],
        [sg.Text('You have the option to select a tool from the list and either select Remove to remove the configuration or select Load Configuration to auto populate the tools configuration into the tool specification area below.')],
        [sg.Text('Tool Specificitation - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('The Tool Specification allows you to add or update a custom tool configuration to the tool list.')],
        [sg.Text('Tool Dependency - How to Use', font='None 14', pad=((5,0),(15,0)))],
        [sg.Text('The Tool Dependency allows you to add or remove the dependencies between different tools.')],
        [sg.Text('......')],
        [sg.Button('Dark Mode')]
        # Tool dependency help
        # Run help

        # Created by

        ]

tab1_layout =  [[sg.T('Output of Scan X', size=(220,10))]]
tab2_layout =  [[sg.T('Output of Scan Y', size=(210,10))]]



outputTabCol = [
            [sg.TabGroup([[sg.Tab('Scan X', tab1_layout,pad=((0,0),(30,0))), sg.Tab('Scan Y', tab2_layout, pad=((0,0),(30,0)))]], tab_location = 'topleft',pad=((0,0),(0,0)))]
            ]


scanFrame = [
            [sg.Frame('Scan', scanCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]

runFrame = [
            [sg.Frame('Run', runCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
xmlFrame = [
            [sg.Frame('XML Report', xmlCol, title_color = titles, pad=((5,40),(0,0)), title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
runConfigFrame = [
            [sg.Frame('Configuration of the Selected Run', runConfigCol, pad=((5,5),(0,5)), title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]

specColFrame = [
            [sg.Frame('Tool Specification', specCol, pad=((5,5),(20,0)), title_color = titles,title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
toolDepColFrame = [
            [sg.Frame('Tool Dependency', toolDepCol, pad=((5,5),(20,0)), title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
outputFrame = [
            [sg.Frame('Output', outputTabCol, title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]


run_tab_layout =  [
                [sg.Column(scanFrame, vertical_alignment=('Top')), sg.Column(runFrame, vertical_alignment=('Top'))],
                [sg.Column(xmlFrame, vertical_alignment=('Top')), sg.Column(runConfigFrame, vertical_alignment=('Top'))],
                [sg.Column(outputFrame)]
                ]

tool_tab_layout =  [
                [sg.Frame('Tool List', toolListCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width, font='none 20')],
                [sg.Column(specColFrame, vertical_alignment='top')],
                [sg.Column(toolDepColFrame)]]

help_tab_layout =  [
                [sg.Frame('Help', helpView, title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')],
                ]


#window layout
layout = [
        [sg.TabGroup([[sg.Tab('Run', run_tab_layout, font=('none 24')), sg.Tab('Tool', tool_tab_layout), sg.Tab('Help', help_tab_layout)]],title_color='white',border_width=tab_border_width)]

        ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Home', layout)

#event loop


while True:
    event, values = window.read()
    #print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
        
    if event == '-addSpec-':
        if ((values['-spec1-'] != "") and (values['-spec2-'] != "") and (values['-spec3-'] != "")  and (values['-spec4-'] != "") and values['-spec5-'] != ""):
            data = data = {"Name of Tool": values['-spec1-'], "Description of Tool": values['-spec2-'], "Path of Tool": values['-spec3-']
                           , "Option and Argument of Tool": values['-spec4-'], "Output Data Specification of Tool"
                           : values['-spec5-']}
            collection.insert_one(data)
            data = makeToolConfigurationTable(3)
            window.FindElement('-TABLE-').Update(values=data)

            window['-spec1-'].update('')
            window['-spec2-'].update('')
            window['-spec3-'].update('')
            window['-spec4-'].update('')
            window['-spec5-'].update('')
        elif values['-toolSpecificationFile-'] != "":
            f = open(values['-toolSpecificationFile-'], "r")
            print(f.read())
            window['-toolSpecificationFile-'].update('')
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
        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')


    if event == "-removeConfig-":
        tableElement = window['-TABLE-'].get()

        tableRow = values['-TABLE-']
        tableRow = tableRow[0]
        rowClicked = tableElement[tableRow]
        print(rowClicked[0])

        confirm = sg.popup_yes_no('Are you sure you want to remove the selected configuration?', title='Remove')

        
        if confirm == "Yes":
            print('ok')
            tool = rowClicked[0]
            remove_tool_list(rowClicked[0])
            data = makeToolConfigurationTable(3)
            window.FindElement('-TABLE-').Update(values=data)
    

    if event == "-removeDependency-":
        confirm = sg.popup_yes_no('Are you sure you want to remove the selected dependency?', title='Remove')

        if confirm == "Yes":
            if (values['-toolData1-'] != ""):
                remove_depedency(values['-toolData1-'])
                window['-toolData1-'].update("")

    if event == "-saveRunConfiguration-":
        if ((values['-runName-'] != "") and (values['-runDescription-'] != "") and (values['-whitelist-'] != "") and (values['-blacklist-'] != "") and (values['-scanType-'] != "")):
            collection = database['Run List']
            data = data = {"Dependent Data": values['-toolData1-'], "Operator": values['-toolData2-'],
                           "Value": values['-toolData3-']
                , "Dependency Expression": values['-toolData4-']}
            data = {"Name of Run": values['-runName-'], "Description of Run": values['-runDescription-'],
                    "Whitelisted IP Target": values['-whitelist-'], "Blacklisted IP Target": values['-blacklist-'],
                    "Scan Type": values['-scanType-'], "Control": "None", "Result with Timestamp": "TBI"}
            collection.insert_one(data)
            window['-runName-'].update('')
            window['-runDescription-'].update('')
            window['-whitelist-'].update('')
            window['-blacklist-'].update('')
            window['-scanType-'].update('')

            data = makeRunTable()
            window.FindElement('-RUNTABLE-').Update(values=data)

        elif values['-runConfigurationFile-'] != "":
            f = open(values['-runConfigurationFile-'], "r")
            print(f.read())
            window['-runConfigurationFile-'].update('')

        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')
    
    if event  == "-cancelRunConfiguration-":
        window['-runName-'].update('')
        window['-runDescription-'].update('')
        window['-whitelist-'].update('')
        window['-blacklist-'].update('')
        window['-scanType-'].update('')

    if event == "-loadConfig-":
        target = []

        tableElement = window['-TABLE-'].get()

        tableRow = values['-TABLE-']
        tableRow = tableRow[0]
        rowClicked = tableElement[tableRow]
        
        tool = rowClicked[0]

        collection = database['Tool List']
        information = get_multiple_data(collection)
        for element in information:
            if element.get("Name of Tool") == tool:
                target = element
                window['-spec1-'].update(element.get("Name of Tool"))
                window['-spec2-'].update(element.get("Description of Tool"))
                window['-spec3-'].update(element.get("Path of Tool"))
                window['-spec4-'].update(element.get("Option and Argument of Tool"))
                window['-spec5-'].update(element.get("Output Data Specification of Tool"))
    
    if event == "-updateConfig-":
        
        confirm = sg.popup_yes_no('Are you sure you want to update the selected configuration?', title='Update')
        
        if confirm == "Yes":
            remove_tool_list(values["-spec1-"])
            if ((values['-spec1-'] != "") and (values['-spec2-'] != "") and (values['-spec3-'] != "") and (
                    values['-spec4-'] != "") and values['-spec5-'] != ""):
                data = data = {"Name of Tool": values['-spec1-'], "Description of Tool": values['-spec2-'],
                                "Path of Tool": values['-spec3-']
                    , "Option and Argument of Tool": values['-spec4-'], "Output Data Specification of Tool"
                    : values['-spec5-']}
                collection.insert_one(data)
                data = makeToolConfigurationTable(3)
                
                window.FindElement('-TABLE-').Update(values=data)

                window['-spec1-'].update('')
                window['-spec2-'].update('')
                window['-spec3-'].update('')
                window['-spec4-'].update('')
                window['-spec5-'].update('')
            else:
                sg.popup(title="Missing input", custom_text='Please check the missing parameters')