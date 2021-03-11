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

import pymongo
from bson import ObjectId

#theme
sg.theme('LightGrey1')

def remove_data(name):
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
information = get_multiple_data(collection)

#tool View
data = []
headingsTool = ['Name of Tool', 'Description of Tool']

def make_table(num_cols):
    data = []
    i = 0
    data = [[j for j in range(num_cols)] for i in range(len(information))]
    for element in information:
        data[i] = [element.get("Name of Tool"), element.get("Description of Tool")]
        i += 1
    return data

# ------ Make the Table Data ------
data = make_table(num_cols=3)

toolCol = [
        [sg.Table(values=data[:][:], headings=headingsTool, max_col_width=25,
                                # background_color='light blue',
                                auto_size_columns=True,
                                display_row_numbers=True,
                                justification='middle',
                                num_rows=20,
                                alternating_row_color='lightgrey',
                                key='-TABLE-',
                                row_height=35,
                                tooltip='This is a table')]]


specCol = [
        [sg.Text('Tool Specification', font=('none 16'),size=(20,1))],
        [sg.Text('Tool Name', size=(20,1)), sg.InputText('')],
        [sg.Text('Tool Description', size=(20,1)), sg.InputText('')],
        [sg.Text('Tool Path', size=(20,1)), sg.InputText(''), sg.Button('Browse')],
        [sg.Text('Option and Argument', size=(20,1)), sg.InputText('')],
        [sg.Text('Output Data Specification', size=(20,1)), sg.InputText(''), sg.Button('Add', key= '-addSpecification')],
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
            [sg.Text('Dependent Data', size=(15,1)), sg.InputCombo(['X', 'Y'], size=(15, 1)), sg.Text('Operator', size=(0,0)), sg.InputCombo(['X', 'Y'], size=(15, 1)), sg.Text('Value', size=(0,0)), sg.InputText('')],
            [sg.Text('Dependency Expression', size=(20,1)), sg.InputText('')],
            [sg.Button('Add'),sg.Button('Remove')]

        ]


#create window
window = sg.Window('SEA Tool Version 1.0 - Tool', layout)

#event loop
while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Add':
        print("Add clicked")
        if ((values[0] != "") and (values[1] != "") and (values[2] != "") and (values[3] != "") and (values[4] != "")):
            data = data = {"Name of Tool": values[0], "Description of Tool": values[1], "Path of Tool": values[2]
                           , "Option and Agurment of Tool": values[3], "Output Data Specification of Tool"
                           : values[4]}
            collection.insert_one(data)
            for i in range (5):
                window[i].update("")
        else:
            sg.popup(title= "Missing input", custom_text= 'Please check the missing parameters')
    if event == "Add60":
        if ((values[6] != "") and (values[7] != "") and (values[8] != "") and (values[9] != "")):
            collection = database['Tool Dependency']
            data = data = {"Dependent Data": values[6], "Operator": values[7],
                           "Value": values[8]
                , "Dependency Expression": values[9]}
            collection.insert_one(data)
            for i in range (6, 10):
                window[i].update("")
    if event == "Remove":
        if (values[6] != ""):
            remove_data(values[6])
            window[6].update("")
    if event == '-TABLE-':
        print("Table clicked")
        if event == '-removeConfig-':
            print("We did it")
