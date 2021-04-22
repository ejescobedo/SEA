#!/usr/bin/env python
import PySimpleGUI as sg
import os
import sys
import subprocess
import random
import string
import pymongo
from bson import ObjectId
from datetime import datetime

theme = 'dark'
azure = '#ECF0F1'
whitelistIPS = ''
toolList = []
scans = []
#toolList = updateToolListDropdown(toolList)
#toolList2 = [1,2,3,4,5]

dark_theme = {'BACKGROUND': '#282A2B',
                'TEXT': 'white',
                'INPUT': '#656565',
                'TEXT_INPUT': 'white',
                'SCROLL': 'grey',
                'BUTTON': ('white', '#2A2C2E'),
                'PROGRESS': ('white', '#333945'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

light_theme = {'BACKGROUND': '#D0D3D4',
                'TEXT': 'black',
                'INPUT': '#FDFDFD',
                'TEXT_INPUT': 'black',
                'SCROLL': 'grey',
                'BUTTON': ('white', '#34495E'),
                'PROGRESS': ('white', '#333945'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

light_alt = {'BACKGROUND': '#CED6DC',
                'TEXT': 'black',
                'INPUT': '#FDFDFD',
                'TEXT_INPUT': 'black',
                'SCROLL': 'grey',
                'BUTTON': ('white', '#34495E'),
                'PROGRESS': ('white', '#333945'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}


if theme == 'dark':
    table_text_color = 'white'
    table_background_color = '#282A2B'
    table_alternate_row_color = '#1D1F21'
    header_color = '#2A2C2E'
    header_t_color = 'white'
    title_color = 'white'
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

    sg.theme_add_new('Dark', dark_theme)
    sg.theme('Dark')
    
if theme == 'light':
   
    table_text_color = 'black'
    table_background_color = 'white'
    table_alternate_row_color = '#ECF0F1'
    header_color = 'white'
    header_t_color = 'black'
    title_color = 'black'
    titles = '#34495E'
    titles2 = '#51A0D5'
    relief = 'ridge'
    title_location = 'nw'
    border_width = 0
    tab_border_width = 0
    selected_row_colors = ('white','#51A0D5')
    buttondefault = ('white', '#34495E')
    yellowbutton = ('white', '#E5B302')
    buttondefault2 = ('white', '#51A0D5')

    sg.theme_add_new('Light', light_theme)
    sg.theme('Light')

if theme == 'light_alt':
    
    table_text_color = 'black'
    table_background_color = 'white'
    table_alternate_row_color = '#ECF0F1'
    header_color = 'white'
    header_t_color = 'black'
    titles = '#34495E'
    titles2 = '#51A0D5'
    relief = 'ridge'
    title_location = 'nw'
    border_width = 0
    tab_border_width = 0
    selected_row_colors = ('white','#51A0D5')
    buttondefault = ('white', '#7B7D7D')
    yellowbutton = ('white', '#E5B302')
    buttondefault2 = ('white', '#51A0D5')

    sg.theme_add_new('Light', light_alt)
    sg.theme('Light')

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
collectionScan = database['Scan']
collectionEmptyScan = database['Scan List']
collectionRun = database['Run List']



data = []
headingsTool = ['Name of Tool', 'Description of Tool']
headingsScan = ['Scan', 'Name of Scan', 'Execution Number','Start Time', 'End Time', 'Scanned IPs', 'Sucessful Execution/Failure', 'Run']
headingsRun = ['Name of Run', 'Description of Run', 'Result with Timestemp', 'Control']

headingsTool2 = ['dumb', 'yes']

import subprocess
import sys
import PySimpleGUI as sg

"""
    Demo Program - Realtime output of a shell command in the window
        Shows how you can run a long-running subprocess and have the output
        be displayed in realtime in the window.
"""



def runCommand(cmd, timeout=None, window=None):
    nop = None
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)

        if event == 'Stop':
            break;
        window.refresh() if window else nop        # yes, a 1-line if, so shoot me

        # if event == 'Pause':
        #     read -p "$*"
    retval = p.wait(timeout)
    
    if event == 'Stop':
        print ('STOP')
    return (retval, output)


def makeToolConfigurationTable(num_cols):
    data = []
    i = 0
    information = get_multiple_data(collection)
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Name of Tool"), element.get("Description of Tool")]
        i += 1
    return data


def updateToolListDropdown(toolList):
    toolList = []
    for x in collection.find():
            #print(x['Name of Tool'])
            toolList.append(x['Name of Tool'])
    #print(toolList)
    return toolList


def makeScanTable():
    num_cols = 9
    data = []
    i = 0
    information = get_multiple_data(collectionEmptyScan)
    
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Scan"), element.get("Name of Scan"), element.get("Execution Number"),
                   element.get("Start Time"), element.get("End Time"), element.get("Scanned IPs"),
                   element.get("Sucessful Execution/Failure"), element.get("Run Name"), element.get("_id")]
        i += 1
    return data

def makeScanTable2(runName, length):
    num_cols = 9
    data = []
    i = 0
    information = get_multiple_data(collectionScan)
    data = [[j for j in range(num_cols)] for i in range(length)]
    for element in information:
        if element.get("Run Name") == runName:
            data[i] = [element.get("Scan"), element.get("Name of Scan"), element.get("Execution Number"),
                    element.get("Start Time"), element.get("End Time"), element.get("Scanned IPs"),
                    element.get("Sucessful Execution/Failure"), element.get("Run Name"), element.get("_id")]
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
                   element.get("Control"), element.get("Whitelisted IP Target")]
        i += 1
    return data

def readTextFile():
    f = open("hello.txt", "r")
    return f.read()

def getStartTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time



def updateScanTable():
    
    
    #this is the table element with values
    tableElement = window['-RUNTABLE-'].get()
    
    #this is the table row where user clicked
    tableRow = values['-RUNTABLE-']
    #getting the row from the array because it was in an array
    tableRow = tableRow[0]
    
    #getting the tableElement that corresponds with the table row
    tableElementRow = tableElement[tableRow]

    #0 element is the name,     
    nameOfRun = tableElementRow[0]
    
    ipsOfRun = tableElementRow[4]
    
    

    
    #getting name of run from run table
    query = {"Run Name": nameOfRun}

        
    mydoc = collectionScan.find(query)
    #print(mydoc)

    length = 0
    
    for x in mydoc:
        length = length + 1

        
    data3 = makeScanTable2(nameOfRun, length)

    #get ip from database
    query2 = {"Name of Run": nameOfRun}
    mydoc2 = collectionRun.find(query2)

    global whitelistIPS
    
    for x2 in mydoc2:
        
        #print(x2['Whitelisted IP Target'])
        whitelistIPS = x2['Whitelisted IP Target']

    

    window.FindElement('-SCANTABLE-').Update(values=data3)    
        
    #window.FindElement('-SCANTABLE-').Update(values=list(mydoc))

def updateScanTable2():
    
    #print('hello')
    
    tableElement = window['-SCANTABLE-'].get()
    
    tableRow = values['-SCANTABLE-']
    
    tableRow = tableRow[0]
    
    nameOfRun = tableElement[tableRow]

    #print(nameOfRun)
        
    nameOfRun = nameOfRun[7]

    #print(nameOfRun)
        
    query = {"Run Name": nameOfRun}
        #select * from scan where name == value

        
    mydoc = collectionScan.find(query)
        
        #print(mydoc)

    length = 0
    for x in mydoc:
        length = length + 1

        
    data3 = makeScanTable2(nameOfRun, length)
    
    #get ip from database
    
    # query2 = {"Name of Run": nameOfRun}
    # mydoc2 = collectionRun.find(query2)

    # for x2 in mydoc2:
    #     whitelistIPS = x2['Whitelisted IP Target']   
    #     print('ipppppppp') 
    
    window.FindElement('-SCANTABLE-').Update(values=data3)    
        
    #window.FindElement('-SCANTABLE-').Update(values=list(mydoc))


toolList = updateToolListDropdown(toolList)

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
        [sg.Text('Dependent Data', font=('None 12'),pad=((5,5),(30,5)),size=(20,1)), sg.InputCombo(['X', 'Y'], font=('None 12'),pad=((5,5),(30,5)),key='-toolData1-',size=(20, 1)), sg.Text('Operator', font=('None 12'),pad=((5,5),(30,5)),size=(0,0)), sg.InputCombo(['X', 'Y'], font=('None 12'),pad=((5,5),(30,5)),key='-toolData2-',size=(20, 1)), sg.Text('Value', font=('None 12'),pad=((5,5),(30,5)), size=(0,0)), sg.InputText('',font=('None 12'),pad=((5,5),(30,5)),key='-toolData3-')],
        [sg.Text('Dependency Expression', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key='-toolData4-')],
        [sg.Text('OR',font=('None 16'), size=(20,1))],
        [sg.Text('Tool Specification File', font=('None 12'),pad=((5,5),(20,5)),size=(20,1)), sg.InputText('', font=('None 12'),key= '-toolSpecificationFile-'), sg.FileBrowse('Browse', key= '-toolSpecificationFileBrowse')],
        [sg.Button('Add', pad=((5,5),(10,50)), button_color=(buttondefault), key='-addSpec-'), sg.Button('Update Configuration', pad=((5,5),(10,50)), button_color=(buttondefault),key='-updateConfig-')]
        ]

''''
toolDepCol = [
            #[sg.Text('Tool Dependency', font=('none 16'),size=(20,1))],
            [sg.Text('Dependent Data', font=('None 12'),pad=((5,5),(30,5)),size=(15,1)), sg.InputCombo(['X', 'Y'], font=('None 12'),pad=((5,5),(30,5)),key='-toolData1-',size=(15, 1)), sg.Text('Operator', font=('None 12'),pad=((5,5),(30,5)),size=(0,0)), sg.InputCombo(['X', 'Y'], font=('None 12'),pad=((5,5),(30,5)),key='-toolData2-',size=(15, 1)), sg.Text('Value', font=('None 12'),pad=((5,5),(30,5)), size=(0,0)), sg.InputText('',font=('None 12'),pad=((5,5),(30,5)),key='-toolData3-')],
            [sg.Text('Dependency Expression', font=('None 12'),size=(20,1)), sg.InputText('', font=('None 12'),key='-toolData4-')],
            [sg.Button('Add', button_color=(buttondefault),key= '-addConfig-'), sg.Button('Remove', button_color=(buttondefault),key='-removeDependency-')]
            ]
'''''
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
              pad=((0,0),(15,10)),
              header_text_color = header_t_color,
              header_background_color = header_color,
              text_color = table_text_color,
              justification='left',
              selected_row_colors = selected_row_colors,
              num_rows=7,
              alternating_row_color=table_alternate_row_color,
              key='-RUNTABLE-',
              row_height=25, enable_events=True,
              tooltip='This is a table')],
    [sg.Button('Load Run', button_color=(buttondefault))]]

runConfigCol = [
        #[sg.Text('Configuration of the Selected Run',font=('none 16'),size=(30,1))],
        [sg.Text('Run Name', font=('None 12'),pad=((5,5),(30,3)), size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'), pad=((5,5),(30,3)),key= '-runName-')],
        [sg.Text('Run Description', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-runDescription-')],
        [sg.Text('Whitelisted IP Target', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-whitelist-')],
        [sg.Text('Blacklisted IP Target', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-blacklist-')],
        #[sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-scanType-')],
        
        #[sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.InputCombo(values = toolList, font=('None 12'),size=(20, 1), key= '-scanType-')],
        
        #[sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.Listbox(values = toolList, text_color = 'white',background_color = 'black', select_mode = 'LISTBOX_SELECT_MODE_MULTIPLE',size=(20, 1), key= '-scanType-')],
        #[sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.Listbox(values = toolList2, size = (15, len(toolList2)), font=('None 12'), select_mode = 'LISTBOX_SELECT_MODE_MULTIPLE',size=(20, 1), key= '-scanTTT-')],
        [sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.Listbox(toolList, select_mode = 'yes',no_scrollbar = True, background_color= table_background_color, size=(15, len(toolList)), key='-scanType-'),sg.Button('Add', key = '-addScan-')],
        [sg.Text('Scan', font=('None 12'),size=(20,1)),sg.InputText('', size=(60,1),font=('None 12'),key= '-scanNames-')],
        [sg.Text('OR',font=('None 16'))],
        [sg.Text('Run Configuration File', font=('None 12'),pad=((5,5),(0,0)),size=(20,1)), sg.InputText('', font=('None 12'),key= '-runConfigurationFile-'),
         sg.FileBrowse('Browse',key= '-runConfigurationFileBrowse')],    ##Added!
        [sg.Button('Save', pad=((5,5),(10,0)), key= '-saveRunConfiguration-', button_color=(buttondefault)), sg.Button('Cancel', key= '-cancelRunConfiguration-',button_color=(buttondefault), pad=((5,5),(10,0)))]
        ]
xmlCol = [
        #[sg.Text('XML Report', font=('none 16'),size=(20,1))],
        [sg.Text('Report Name', font=('None 12'),pad=((5,5),(30,3)),size=(15,1)), sg.InputText('',font=('None 12'),size=(55,1),pad=((5,5),(30,3)))],
        [sg.Text('Report Description', font=('None 12'),size=(15,1)), sg.InputText('',font=('None 12'),size=(55,1))],
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
        [sg.Button('Dark Mode')]]





outputTabCol = [
            [sg.Output(size=(120,30), font=('none 16'), pad=((0,0),(30,0)),background_color='#1D1F21', text_color='white')]
            #[sg.TabGroup([[sg.Tab('Scan X', tab1_layout,pad=((0,0),(30,0))), sg.Tab('Scan Y', tab2_layout, pad=((0,0),(30,0)))]], tab_location = 'topleft',pad=((0,0),(0,0)))]
            ]


scanFrame = [
            [sg.Frame('Scan', scanCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]

runFrame = [
            [sg.Frame('Run', runCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
xmlFrame = [
            [sg.Frame('XML Report', xmlCol, title_color = titles, pad=((5,20),(0,0)), title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
runConfigFrame = [
            [sg.Frame('Configuration of the Selected Run', runConfigCol, pad=((5,5),(0,5)), title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]

specColFrame = [
            [sg.Frame('Tool Specification', specCol, pad=((5,5),(20,0)), title_color = titles,title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]
#toolDepColFrame = [
#            [sg.Frame('Tool Dependency', toolDepCol, pad=((5,5),(20,0)), title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
#            ]
# outputFrame = [
#             [sg.Frame('Output', outputTabCol, title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
#             ]


run_tab_layout =  [
                [sg.Column(scanFrame, vertical_alignment=('Top')), sg.Column(runFrame, vertical_alignment=('Top'))],
                [sg.Column(xmlFrame, vertical_alignment=('Top')), sg.Column(runConfigFrame, vertical_alignment=('Top'))],
                #[sg.Column(outputFrame)]
                ]

tool_tab_layout =  [
                [sg.Frame('Tool List', toolListCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width, font='none 20')],
                [sg.Column(specColFrame, vertical_alignment='top')]]

output_tab_layout = [
                [sg.Frame('Output', outputTabCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width, font='none 20')],
                #[sg.Output(size =(225, 50),pad=((0,0),(30,0)),background_color='#1D1F21', text_color='white')]
                ]
help_tab_layout =  [
                [sg.Frame('Help', helpView, title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')],
                ]


#window layout
layout = [
        [sg.TabGroup([[sg.Tab('Run', run_tab_layout, font=('none 24')), sg.Tab('Tool', tool_tab_layout), sg.Tab('Output', output_tab_layout), sg.Tab('Help', help_tab_layout)]],title_color=title_color,border_width=tab_border_width)]

        ]

#create window
window = sg.Window('SEA Tool Version 1.0 - Home', layout, resizable= True)

#event loop


while True:
    
    event, values = window.read()
    #print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    #print('whitelist :' + whitelistIPS)
    
    #need to auto populate tool list into drop down combo, so get tool list into a list 
    
    #tableElement = window['-TABLE-'].get()
    #tableRow = values['-TABLE-']
    #print(tableRow)

    
    if event == 'Pause':
        
        scanTypeList = values['-scanNames-'] 
        print('scan type list')
        
        scanTypeList = scanTypeList
        
        print(scanTypeList)
        print(len(scanTypeList))


    

    if event == '-addScan-':
        
        #print('hello')

        tableElement = window['-scanType-']
        tableRow = values['-scanType-']

        #print(tableRow)

        scans.append(tableRow[0])
        
        print('scans')
        print(scans)
        print(len(scans))
        
        window['-scanNames-'].update(scans)
    
    

    
        
    
    if event == 'Start':
        
        tableElement = window['-SCANTABLE-'].get()
        tableRow = values['-SCANTABLE-']
        
        #print(tableRow)
        tableRow = tableRow[0]
        rowClicked = tableElement[tableRow]
        
        #print('hello' + rowClicked[0])
        
        nameOfScan = rowClicked[1]
        ipOfScan = rowClicked[5]
        #gotta increment scan number
        #print(ipOfScan)
        
        
        #need to get unique number 

        #query = {"Run Name": nameOfRun}
        #select * from scan where name == value
        
        uniqueID = rowClicked[8]
        
        query = {"_id": uniqueID}
       
        mydoc = collectionScan.find(query)



       
        #important rowclicked[8] will give us unique ID
        #print(getStartTime())

        startTime = getStartTime()
        
        #for d in mydoc:
            #print (d)

        doc2 = collectionScan.find_one_and_update(
    
        {"_id" : ObjectId(uniqueID)},
        {"$set":
            {"Start Time": startTime}
        },upsert=True)

        #update Table
        updateScanTable2()

        
        whitelistIPS = ipOfScan.split()
        
        #print("whitelist " + whitelistIPS)

        #operation = nameOfScan + ' ' + whitelistIPS
        
        
        #print(operation)
        
        for ips in whitelistIPS:
            operation = nameOfScan + ' ' + ips
            runCommand(cmd=operation, window=window)
        
        #ip addresses 

        endTime = getStartTime()

        doc3 = collectionScan.find_one_and_update(
        {"_id" : ObjectId(uniqueID)},
        {"$set":
            {"End Time": endTime}
        },upsert=True)

        updateScanTable2()

    
    # if event == 'Stop':
    #     print('Stop')
    #     #pause scan

    if event == 'Load Run':
        
        updateScanTable()

    
        
        
      

    if event == '-addSpec-':
        
        print('addSpec')
        
        if ((values['-spec1-'] != "") and (values['-spec2-'] != "") and (values['-spec3-'] != "")  and
                (values['-spec4-'] != "") and values['-spec5-'] != "") and (values['-toolData1-'] != "") \
                and (values['-toolData2-'] != "") and (values['-toolData3-'] != "") and (
                    values['-toolData4-'] != ""):
            data = data = {"Name of Tool": values['-spec1-'], "Description of Tool": values['-spec2-'], "Path of Tool": values['-spec3-']
                           , "Option and Argument of Tool": values['-spec4-'], "Output Data Specification of Tool"
                           : values['-spec5-'], "Dependent Data": values['-toolData1-'], "Operator": values['-toolData2-'],
                               "Value": values['-toolData3-']
                    , "Dependency Expression": values['-toolData4-']}
            collection.insert_one(data)
            data = makeToolConfigurationTable(3)
            window.FindElement('-TABLE-').Update(values=data)

            window['-toolData1-'].update('')
            window['-toolData2-'].update('')
            window['-toolData3-'].update('')
            window['-toolData4-'].update('')
            window['-spec1-'].update('')
            window['-spec2-'].update('')
            window['-spec3-'].update('')
            window['-spec4-'].update('')
            window['-spec5-'].update('')
            
            
        
        elif values['-toolSpecificationFile-'] != "":
            f = open(values['-toolSpecificationFile-'], "r")
            data = []
            for line in f:
                line = line.rstrip("\n")
                items = line.split(":", 1)
                items[1] = items[1][1:]
                data.append(items)
            data = {data[0][0]: data[0][1], data[1][0]: data[1][1],
                    data[2][0]: data[2][1], data[3][0]: data[3][1],
                    data[4][0]: data[4][1], data[5][0]: data[5][1],
                    data[6][0]: data[6][1], data[7][0]: data[7][1],
                    data[8][0]: data[8][1]}
            collection = database['Tool List']
            collection.insert_one(data)
            window['-toolSpecificationFile-'].update('')
            data = makeRunTable()
            window.FindElement('-RUNTABLE-').Update(values=data)
            

        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')
        
        tools = updateToolListDropdown(toolList)
        
        window['-scanType-'].update(values = tools)
        
    if event == "-removeConfig-":
        
        tableElement = window['-TABLE-'].get()

        tableRow = values['-TABLE-']
        tableRow = tableRow[0]
        rowClicked = tableElement[tableRow]
        # print(rowClicked[0])

        confirm = sg.popup_yes_no('Are you sure you want to remove the selected configuration?', title='Remove')

        
        if confirm == "Yes":
            toolList = updateToolListDropdown(toolList)
            # print('ok')
            tool = rowClicked[0]
            remove_tool_list(rowClicked[0])
            data = makeToolConfigurationTable(3)
            window.FindElement('-TABLE-').Update(values=data)
            tools = updateToolListDropdown(toolList)
            window['-scanType-'].update(values = tools)

    if event == "-saveRunConfiguration-":
        if ((values['-runName-'] != "") and (values['-runDescription-'] != "") and (values['-whitelist-'] != "") and (values['-blacklist-'] != "") and (values['-scanType-'] != "")):
            collection = database['Run List']
            # data = data = {"Dependent Data": values['-toolData1-'], "Operator": values['-toolData2-'],
            #                "Value": values['-toolData3-']
            #     , "Dependency Expression": values['-toolData4-']}
            
            data = {"Name of Run": values['-runName-'], "Description of Run": values['-runDescription-'],
                    "Whitelisted IP Target": values['-whitelist-'], "Blacklisted IP Target": values['-blacklist-'],
                    "Scan Type": values['-scanType-'], "Control": "None", "Result with Timestamp": "TBI"}
            

              


            
            #this is the scan types different tool names
            scanTypeList = values['-scanNames-']
            
            #getting ip from fields to store to database
            ipList = values['-whitelist-']
            
            #scanTypeList = scanTypeList.split()
            
            runName = values['-runName-']

            

            
            collection.insert_one(data)
            
            window['-runName-'].update('')
            window['-runDescription-'].update('')
            window['-whitelist-'].update('')
            window['-blacklist-'].update('')
            window['-scanType-'].update('')

            data = makeRunTable()
            window.FindElement('-RUNTABLE-').Update(values=data)

            #save Scan in Table
            collection2 = database['Scan']
            
            for i, scan in enumerate(scans):
                scanData = {"Scan": i, "Name of Scan": scan,
                    "Execution Number": i, "Start Time": "0",
                    "End Time": "0", "Scanned IPs": ipList, "Succesful Execution": "0", "Run Name": runName}
                collection2.insert_one(scanData)



            
            
            

            


        elif values['-runConfigurationFile-'] != "":
            f = open(values['-runConfigurationFile-'], "r")
            data = []
            for line in f:
                line = line.rstrip("\n")
                items = line.split(":")
                items[1] = items[1][1:]
                data.append(items)

            data = {data[0][0]: data[0][1], data[1][0]: data[1][1],
                    data[2][0]: data[2][1], data[3][0]: data[3][1],
                    data[4][0]: data[4][1], data[5][0]: data[5][1], data[6][0]: data[6][1]}
            collection = database['Run List']
            collection.insert_one(data)
            window['-runConfigurationFile-'].update('')
            data = makeRunTable()
            window.FindElement('-RUNTABLE-').Update(values=data)

        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')
    
    if event  == "-cancelRunConfiguration-":
        scans = []
        window['-runName-'].update('')
        window['-runDescription-'].update('')
        window['-whitelist-'].update('')
        window['-blacklist-'].update('')
        window['-scanNames-'].update('')

        tools = updateToolListDropdown(toolList)
        window['-scanType-'].update(values = tools)

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
                window['-toolData1-'].update(element.get("Dependent Data"))
                window['-toolData2-'].update(element.get("Operator"))
                window['-toolData3-'].update(element.get("Value"))
                window['-toolData4-'].update(element.get("Dependency Expression"))
    
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
                window['-toolData1-'].update('')
                window['-toolData2-'].update('')
                window['-toolData3-'].update('')
                window['-toolData4-'].update('')
            else:
                sg.popup(title="Missing input", custom_text='Please check the missing parameters')