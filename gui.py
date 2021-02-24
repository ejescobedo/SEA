import PySimpleGUI as sg
import os

sg.theme('LightGrey1')
# All the stuff inside your window.


#col_layout = [
    # [sg.Button('Run', font=("Helvetica",25))],
    # [sg.Button('Tool', font=("Helvetica",25))]]

layout = [
    #[sg.Text('General', size=(100,1),justification=('c'), font=("Helvetica",25))],
    [sg.Button('Run', font=("Helvetica",25), pad=(0,40))],
    [sg.Button('Tool', font=("Helvetica",25), pad=(0,0))]
    ]
# Create the Window
window = sg.Window('SEA Tool Version 1.0 - General', layout, size =(500, 300), element_justification=('c'))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == 'Run':
        os.system('python3 run.py')
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

window.close()
