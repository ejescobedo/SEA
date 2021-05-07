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
import xml2json
import xmltodict
import json
import pprint
from json2xml import json2xml
from json2xml.utils import readfromurl, readfromstring, readfromjson

theme = 'dark'
azure = '#ECF0F1'
whitelistIPS = ''
toolList = []
runList = []
scanList = []
scans = []
reportList = []

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

#dark theme
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
    data = collection.find()
    return list(data)

#Database connections
connection = pymongo.MongoClient('localhost', 27017)
database = connection['mydb_01']
collection = database['Tool List']
collectionScan = database['Scan']
collectionEmptyScan = database['Scan List']
collectionRun = database['Run List']
collectionXML = database['XML Report']


#data list
data = []
#headings for tables
headingsTool = ['Name of Tool', 'Description of Tool']
headingsScan = ['Scan', 'Name of Scan', 'Execution Number','Start Time', 'End Time', 'Scanned IPs', 'Sucessful Execution/Failure', 'Run']
headingsRun = ['Name of Run', 'Description of Run', 'Result with Timestemp', 'Control']
headingsTool2 = ['dumb', 'yes']

#run tool in command line
def runCommand(cmd, timeout=None, window=None):
    nop = None
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)

        if event == 'Stop':
            break;
        window.refresh() if window else nop
    retval = p.wait(timeout)
    return (retval, output)

#create configuration table
def makeToolConfigurationTable(num_cols):
    data = []
    i = 0
    information = get_multiple_data(collection)
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Name of Tool"), element.get("Description of Tool")]
        i += 1
    return data

#update the tool list
def updateToolListDropdown(toolList):
    toolList = []
    for x in collection.find():
            toolList.append(x['Name of Tool'])
    return toolList

#update the run list
def updateRunListDropdown(runList):
    runList = []
    for x in collectionRun.find():
            runList.append(x['Name of Run'])
    return runList

#update the scan list 
def updateScanListDropdown(scanList, runName):
    scanList = []
    
    query = {"Run Name": runName}
    mydoc = collectionScan.find(query)
    
    for x in mydoc:
        scanList.append(x['Name of Scan'])
    return scanList

#make the scan table
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

#make the scan table after updating
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
#make the run table
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

#reading a file
def readTextFile():
    f = open("hello.txt", "r")
    return f.read()

#getting the current time
def getStartTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

#populate scan table on load
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
        whitelistIPS = x2['Whitelisted IP Target']

    window.FindElement('-SCANTABLE-').Update(values=data3)    

#update the scan table after updating
def updateScanTable2():
    
    tableElement = window['-SCANTABLE-'].get()
    tableRow = values['-SCANTABLE-']
    tableRow = tableRow[0]
    nameOfRun = tableElement[tableRow]        
    nameOfRun = nameOfRun[7]    
    query = {"Run Name": nameOfRun}   
    mydoc = collectionScan.find(query)
    length = 0
    for x in mydoc:
        length = length + 1
    
    data3 = makeScanTable2(nameOfRun, length)
    
    window.FindElement('-SCANTABLE-').Update(values=data3)    
        
#populate tool list 
toolList = updateToolListDropdown(toolList)
#populate run list
runList = updateRunListDropdown(runList)


# Table Data
dataToolConfiguration = makeToolConfigurationTable(num_cols=3)
dataScan = makeScanTable()
dataRun = makeRunTable()

#gui tool column
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

#gui tool specification column
specCol = [
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


contentRun = []
contentScan = []

#gui scan column
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
    [sg.Button('Start', button_color=(buttondefault)), sg.Button('Pause', button_color=(buttondefault)), sg.Button('Stop', button_color=(buttondefault)),sg.Button('Run All', button_color=(buttondefault))]
    ]

#gui run column
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

#gui run configuration column
runConfigCol = [
        [sg.Text('Run Name', font=('None 12'),pad=((5,5),(30,3)), size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'), pad=((5,5),(30,3)),key= '-runName-')],
        [sg.Text('Run Description', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-runDescription-')],
        [sg.Text('Whitelisted IP Target', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-whitelist-')],
        [sg.Text('Blacklisted IP Target', font=('None 12'),size=(20,1)), sg.InputText('', size=(60,1),font=('None 12'),key= '-blacklist-')],
        [sg.Text('Scan Type', font=('None 12'),size=(20,1)), sg.Listbox(toolList, select_mode = 'yes',no_scrollbar = True, background_color= table_background_color, size=(15, 8), key='-scanType-'),sg.Button('Add', key = '-addScan-')],
        [sg.Text('Scan', font=('None 12'),size=(20,1)),sg.InputText('', size=(60,1),font=('None 12'),key= '-scanNames-')],
        [sg.Text('OR',font=('None 16'))],
        [sg.Text('Run Configuration File', font=('None 12'),pad=((5,5),(0,0)),size=(20,1)), sg.InputText('', font=('None 12'),key= '-runConfigurationFile-'),
         sg.FileBrowse('Browse',key= '-runConfigurationFileBrowse')],
        [sg.Button('Save', pad=((5,5),(10,0)), key= '-saveRunConfiguration-', button_color=(buttondefault)), sg.Button('Cancel', key= '-cancelRunConfiguration-',button_color=(buttondefault), pad=((5,5),(10,0)))]
        ]

#gui xml report column
xmlCol = [
        [sg.Text('Report Name', font=('None 12'),pad=((5,5),(30,3)),size=(15,1)), sg.InputText('',font=('None 12'),key='-reportName-',size=(55,1),pad=((5,5),(30,3)))],
        [sg.Text('Report Description', font=('None 12'),size=(15,1)), sg.InputText('',font=('None 12'), key='-reportDescription-',size=(55,1))],
        [sg.Text('Run', font=('None 12'),size=(15,1)), sg.Listbox(runList, select_mode = 'LISTBOX_SELECT_MODE_SINGLE',no_scrollbar = True, background_color= table_background_color, size=(15, 8), enable_events=True,key='-runListXML-'),sg.Button('Load Scans', key = '-loadScans-'),sg.Listbox(scanList, select_mode = 'LISTBOX_SELECT_MODE_SINGLE',no_scrollbar = True, background_color= table_background_color, size=(15, 8), enable_events=True,key='-scanListXML-'),sg.Button('Add', key = '-addScan2-')],
        [sg.Button('Generate',pad=((5,5),(30,5)), button_color=(buttondefault)), sg.Button('Cancel', button_color=(buttondefault), pad=((5,5),(30,5)))]
        ]

#gui help view
helpView = [
        [sg.Text('Run List -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('Shows the Run(s) that have been configured and added to the SEA Tool.',font='None 14')],
        [sg.Text('Scan List -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('Shows a detailed view of all the scans within a run. First select a Run from the Run List then click load Scans to populate the Scan table.',font='None 14')],
        [sg.Text('XML Report -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('Allows the user to build an XML report. First enter a Report Name and a Report Description, then select a Run from the list and click Load Scans in order to load the scans from that particular run.',font='None 14')],
        [sg.Text('After the Scans are loaded the user may select a scan and select Add to build a report. Finally, after all the desired scans have been added to the report the user can click Generate and a report will be saved to the filesystem.',font='None 14')],
        [sg.Text('Configuration of the Selected Run -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('Allows the user to configure a Run and add it to the SEA Tool. First fill out the fields and then select the tool you would like to use in the Scan Type table and click add.',font='None 14')],
        
        [sg.Text('Output -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('Displays the current output of the scan.',font='None 14')],
        [sg.Text('Tool List -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('The Tool List displays a list of the already configured underlying tools.',font='None 14')],
        [sg.Text('You have the option to select a tool from the list and either select Remove to remove the configuration or select Load Configuration to auto populate the tools configuration into the tool specification area below.',font='None 14')],
        [sg.Text('Tool Specificitation -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('The Tool Specification allows you to add or update a custom tool configuration to the tool list.',font='None 14')],
        [sg.Text('Tool Dependency -', font='None 18', pad=((5,0),(15,0)))],
        [sg.Text('The Tool Dependency allows you to add or remove the dependencies between different tools.',font='None 14')]
        ]

#gui output column
outputTabCol = [
            [sg.Output(size=(120,30), font=('none 16'), pad=((0,0),(30,0)),background_color='#1D1F21', text_color='white')]
            ]

#frames for gui
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
            [sg.Frame('Run Configuration', runConfigCol, pad=((5,5),(0,5)), title_color = titles, title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]

specColFrame = [
            [sg.Frame('Tool Specification', specCol, pad=((5,5),(20,0)), title_color = titles,title_location = title_location,relief=relief, border_width = border_width,font='none 20')]
            ]


#gui layouts
run_tab_layout =  [
                [sg.Column(scanFrame, vertical_alignment=('Top')), sg.Column(runFrame, vertical_alignment=('Top'))],
                [sg.Column(xmlFrame, vertical_alignment=('Top')), sg.Column(runConfigFrame, vertical_alignment=('Top'))],
                ]

tool_tab_layout =  [
                [sg.Frame('Tool List', toolListCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width, font='none 20')],
                [sg.Column(specColFrame, vertical_alignment='top')]]

output_tab_layout = [
                [sg.Frame('Output', outputTabCol, pad=((5,5),(20,0)),title_color = titles, title_location = title_location,relief=relief, border_width = border_width, font='none 20')],
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
    
    #if exit or closed
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    #get runlistXML window for updating 
    runSelected = window['-runListXML-'].get()
    
    #if button clicked is load scans
    if event == '-loadScans-':
        runName = runSelected[0]
        scanList = updateScanListDropdown(runList, runName)
        window.FindElement('-scanListXML-').Update(values=scanList)

    #if button clicked is add scan
    if event == '-addScan2-':

        runSelected = window['-runListXML-'].get()
        runName = runSelected[0]
        
        #run index
        rids = window['-runListXML-'].GetIndexes()
        rids = rids[0]

        #scan index
        sids = window['-scanListXML-'].GetIndexes()
        sids = sids[0] 
       
        query = {"Run Name": runName}
        mydoc = collectionScan.find(query)

        #get unique idfrom scantable 
        uniqueID = mydoc[sids]
        uniqueID = uniqueID['_id']

        reportList.append(uniqueID)
        print('Report List: ')
        print(reportList)

    #if button clicked is generate   
    if event == 'Generate':
        
        reportName = values['-reportName-']
        reportDescription = values['-reportDescription-']
        
    
        for i, x in enumerate(reportList):
            
            query = {"_id": x}
            mydoc = collectionScan.find(query)

            for c in mydoc:
               data = c["XML"]
            
            #convert back to xml
            doc2 = readfromstring(data)
            doc3 = json2xml.Json2xml(doc2).to_xml()

            #save to file
            f = open(reportName + '_' + reportDescription + str(i) + '_.xml', "w")
            
            f.write(doc3)
            f.close()

            reportList = []
    
    #if button clicked is run all
    if event == 'Run All':
        
        #getting all scans from table
        tableElement = window['-SCANTABLE-'].get()
        tableRow = values['-SCANTABLE-']

        for x in tableElement:
            nameOfScan = x[1]
            ipOfScan = x[5]
            uniqueID = x[8]
        
            query = {"_id": uniqueID}
       
            mydoc = collectionScan.find(query)
            
            startTime = getStartTime()
            
            doc2 = collectionScan.find_one_and_update(
                {"_id" : ObjectId(uniqueID)},
                {"$set":
                {"Start Time": startTime}
                },upsert=True)

            #update Table
            updateScanTable2()
            

            whitelistIPS = ipOfScan.split()

            for ips in whitelistIPS:
                operation = nameOfScan + ' ' + ips + ' -oX result.xml'
                runCommand(cmd=operation, window=window)

            endTime = getStartTime()

            doc3 = collectionScan.find_one_and_update(
                {"_id" : ObjectId(uniqueID)},
                {"$set":
                {"End Time": endTime}
                },upsert=True)

            updateScanTable2()

            #file name
            xmlFile = 'result.xml'

            
            #open file
            with open(xmlFile) as fd:
                doc = xmltodict.parse(fd.read())

            #to string
            x = json.dumps(doc)

            #save xml report to database
            doc4 = collectionScan.find_one_and_update(
            {"_id" : ObjectId(uniqueID)},
            {"$set":
                {"XML": x}
            },upsert=True)

    #if button clicked is pause
    if event == 'Pause':
        tableElement = window['-SCANTABLE-'].get()
        print(tableElement)


    #if button clicked is addscan
    if event == '-addScan-':
        
        tableElement = window['-scanType-']
        tableRow = values['-scanType-']

        scans.append(tableRow[0])
        
        window['-scanNames-'].update(scans)
    
    
    #if button clicked is start
    if event == 'Start':
        
        tableElement = window['-SCANTABLE-'].get()
        tableRow = values['-SCANTABLE-']
        
        
        tableRow = tableRow[0]
        rowClicked = tableElement[tableRow]
        
        
        
        nameOfScan = rowClicked[1]
        ipOfScan = rowClicked[5]
        
        uniqueID = rowClicked[8]
        
        query = {"_id": uniqueID}
       
        mydoc = collectionScan.find(query)

        startTime = getStartTime()

        doc2 = collectionScan.find_one_and_update(
        
        #update start time in database 
        {"_id" : ObjectId(uniqueID)},
        {"$set":
            {"Start Time": startTime}
        },upsert=True)

        #update Table
        updateScanTable2()

        #split whitelist string
        whitelistIPS = ipOfScan.split()
        
        for ips in whitelistIPS:
            operation = nameOfScan + ' ' + ips + ' -oX result.xml'
            runCommand(cmd=operation, window=window)
    

        endTime = getStartTime()

        #update end time in database 
        doc3 = collectionScan.find_one_and_update(
        {"_id" : ObjectId(uniqueID)},
        {"$set":
            {"End Time": endTime}
        },upsert=True)

        updateScanTable2()
       
        #file name
        xmlFile = 'result.xml'

        
        #open file
        with open(xmlFile) as fd:
            doc = xmltodict.parse(fd.read())

        #to string
        x = json.dumps(doc)

        #save xml report to database
        doc4 = collectionScan.find_one_and_update(
        {"_id" : ObjectId(uniqueID)},
        {"$set":
            {"XML": x}
        },upsert=True)

    #if button clicked is load run
    if event == 'Load Run':
        updateScanTable()

    #if button clicked is add specification
    if event == '-addSpec-':
            
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
     
    #if button click is remove    
    if event == "-removeConfig-":
        
        tableElement = window['-TABLE-'].get()
        tableRow = values['-TABLE-']
        tableRow = tableRow[0]
        rowClicked = tableElement[tableRow]

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

    #if button clicked is save run config
    if event == "-saveRunConfiguration-":
        if ((values['-runName-'] != "") and (values['-runDescription-'] != "") and (values['-whitelist-'] != "") and (values['-blacklist-'] != "") and (values['-scanType-'] != "")):
            collection = database['Run List']
            
            data = {"Name of Run": values['-runName-'], "Description of Run": values['-runDescription-'],
                    "Whitelisted IP Target": values['-whitelist-'], "Blacklisted IP Target": values['-blacklist-'],
                    "Scan Type": values['-scanType-'], "Control": "None", "Result with Timestamp": "TBI"}
              
            #this is the scan types different tool names
            scanTypeList = values['-scanNames-']
            
            #getting ip from fields to store to database
            ipList = values['-whitelist-']
            
            runName = values['-runName-']

            collection.insert_one(data)
            
            window['-runName-'].update('')
            window['-runDescription-'].update('')
            window['-whitelist-'].update('')
            window['-blacklist-'].update('')
            window['-scanType-'].update('')

            data = makeRunTable()
            runList = updateRunListDropdown(runList)
            window.FindElement('-RUNTABLE-').Update(values=data)
            window.FindElement('-runListXML-').Update(values=runList)

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
            runList = updateRunListDropdown(runList)
            window.FindElement('-RUNTABLE-').Update(values=data)
            window.FindElement('-runListXML-').Update(values=runList)

        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')
    
    #if button clicked is cancel
    if event  == "-cancelRunConfiguration-":
        scans = []
        window['-runName-'].update('')
        window['-runDescription-'].update('')
        window['-whitelist-'].update('')
        window['-blacklist-'].update('')
        window['-scanNames-'].update('')

        tools = updateToolListDropdown(toolList)
        window['-scanType-'].update(values = tools)

    #if button clicked is load config
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
    
    #if button clicked is update config
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