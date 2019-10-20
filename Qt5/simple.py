import PySimpleGUI as sg      


layout = [[sg.Listbox(values=('Listbox Item 1', 'Listbox Item 2', 'Listbox Item 3'), size=(30,15))], 
[sg.Listbox(values=('Listbox Item 1', 'Listbox Item 2', 'Listbox Item 3'), size=(30,15))]]      

window=sg.Window

event, values = window("Vocabulary", layout).Read()  
# print(dir(window))
