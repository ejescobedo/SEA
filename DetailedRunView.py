#!/usr/bin/env python
import PySimpleGUI as sg
import random
import string

"""
    Basic use of the Table Element
"""

sg.theme('Dark')


NewSpinner = [sg.Input('0', size=(3, 1), font='Any 12', justification='r', key='-SPIN-'),
              sg.Column([[sg.Button('▲', size=(1, 1), font='Any 7', border_width=0,
                                    button_color=(sg.theme_text_color(), sg.theme_background_color()), key='-UP-')],
                         [sg.Button('▼', size=(1, 1), font='Any 7', border_width=0,
                                    button_color=(sg.theme_text_color(), sg.theme_background_color()), key='-DOWN-')]])]

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = ["Scan", "Name of Scan", "Execution Order", "Start Time", "End Time", "Scanned IPs", "Sucessfull Execution/Failure", "Control"]
    #data[0] = NewSpinner
    for i in range(1, num_rows):
        data[i] = [[1], *[[1] for i in range(num_cols)]]
        data[i][num_cols - 1] = [2]
    return data

# ------ Make the Table Data ------
data = make_table(num_rows=14, num_cols=8)
headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]


# ------ Window Layout ------
layout = [[sg.Table(values=data[1:][:], headings=headings, max_col_width=25,
                    # background_color='light blue',
                    auto_size_columns=True,
                    justification='right',
                    num_rows=20,
                    alternating_row_color='lightyellow',
                    key='-TABLE-',
                    row_height=35,
                    tooltip='This is a table')]]


# ------ Create Window ------
window = sg.Window('The Table Element', layout,
                   # font='Helvetica 25',
                   )

# ------ Event Loop ------
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break

    #if event == 'Double':
    #    for i in range(len(data)):
    #        data.append(data[i])
    #    window['-TABLE-'].update(values=data)
    #elif event == 'Change Colors':
    #    window['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

window.close()