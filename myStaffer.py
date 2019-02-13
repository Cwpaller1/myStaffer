'''This is the start of the myStaffer project.
Created by Cory Paller.'''

# shebang line
#! usr/bin/env Python3.

import openpyxl
from tkinter import *
import os

file_name = ''

class MainWindow:
    def __init__(self, master):
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)

        # create first cascade
        self.first_cascade = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label='File', menu=self.first_cascade)
        self.first_cascade.add_command(label='Choose Excel File...', command=self.choose_file)

        # create second cascade
        self.second_cascade = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label='Functions', menu=self.second_cascade)
        self.second_cascade.add_command(label='Sort First Sheet by Subsequent Sheets')
        self.second_cascade.add_command(label='Add People into Database')

        self.file_label = Label(master, text='Enter file name: ')
        self.file_entry = Entry(master)
        self.file_button = Button(text='Submit', command=self.commit_file)

    def choose_file(self):
        self.file_label.grid(row=0, column=0)
        self.file_entry.grid(row=0, column=1)
        self.file_button.grid(row=0, column=2)

    def commit_file(self):
        print(os.getcwd())
        file_name = str(self.file_entry.get())
        print(file_name)
        open_xl_file()


# function that takes in an Excel file and reads the data into a dictionary.
def open_xl_file():
    file1 = openpyxl.load_workbook(str(os.getcwd() + '/' + file_name))
    co_executive = file1['County_Exec_500']
    pros = file1['Prosecutor_250']
    galloway = file1['Galloway_250']
    zimmerman = file1['Zimmerman_100']
    schupp = file1['Schupp_250']
    sifton = file1['Sifton_250']
    adams_williams = file1['AdamsWilliams_100']
    council = file1['Council_100']
    state_rep = file1['StateRep_100']
    wam = file1['WAM_100']
    final_result = file1['FinalResult']

    flip_through(co_executive, pros, galloway, zimmerman, final_result, schupp,\
                 sifton, adams_williams, council, state_rep, wam, file1)
    
# function to handle the flipping through
def flip_through(co_executive, pros, galloway, zimmerman, final_result, schupp,\
                 sifton, adams_williams, council, state_rep, wam, file1):
    first_name = ''
    last_name = ''
    find_match = False
    zim_match = False
    row_to_append = []
    
    # cycle through County Exec
    for row_num_1 in co_executive.rows:

        # make sure we don't repeat:
        if first_name == row_num_1[6].value and \
           last_name == row_num_1[5].value and \
           find_match == True:
            for cell in row_num_1:
                row_to_append.append(cell.value)
            copy_to_final(row_to_append, final_result)
            row_to_append = []
            print("Copied duplicate Stenger/Mantovani")
            continue

        find_match = False
        zim_match = False
        first_name = row_num_1[6].value
        last_name = row_num_1[5].value

        # cycle through Zimmerman
        for row_num_2 in zimmerman.rows:
            if row_num_2[5].value == last_name and \
               row_num_2[6].value == first_name:
                zim_match = True
            
        # check to see if Zim kicked it
        if zim_match == False:
            # cycle through Prosecutor
            for row_num_3 in pros.rows:
                if row_num_3[5].value == last_name and \
                   row_num_3[6].value == first_name:
                    for cell in row_num_3:
                        row_to_append.append(cell.value)
                    copy_to_final(row_to_append, final_result)
                    row_to_append = []
                    find_match = True

            # cycle through Galloway
            for row_num_4 in galloway.rows:
                if row_num_4[5].value == last_name and \
                   row_num_4[6].value == first_name:
                    for cell in row_num_4:
                        row_to_append.append(cell.value)
                    copy_to_final(row_to_append, final_result)
                    row_to_append = []
                    find_match = True

            # cycle through Schupp
            find_match = go_through_list(schupp, last_name,\
                                         first_name, row_to_append,\
                                         final_result, find_match)

            # cycle through Sifton
            find_match = go_through_list(sifton, last_name,\
                                         first_name, row_to_append,\
                                         final_result, find_match)

            # cycle through Adams/Williams
            find_match = go_through_list(adams_williams, last_name,\
                                         first_name, row_to_append,\
                                         final_result, find_match)

            # cycle through Council
            find_match = go_through_list(council, last_name,\
                                         first_name, row_to_append,\
                                         final_result, find_match)

            # cycle through State Reps
            find_match = go_through_list(state_rep, last_name,\
                                         first_name, row_to_append,\
                                         final_result, find_match)

            # cycle through WAM
            find_match = go_through_list(wam, last_name,\
                                         first_name, row_to_append,\
                                         final_result, find_match)

        # print the county exec one too.
        if find_match == True:
            for cell in row_num_1:
                row_to_append.append(cell.value)
            copy_to_final(row_to_append, final_result)
            row_to_append = []
            print("Copied Stenger/Mantovani")

    file1 = file1.save(input("What would you like to name the save file?: "))


# function to copy row onto final_result
def copy_to_final(row_to_append, final_result):
    index = 1
    final_row = final_result.max_row + 1

    for i in row_to_append:
        if index < 19:
            final_result.cell(row=final_row, column=index).value = i
            index += 1


# function to handle sifting through a list
def go_through_list(sheet_to_go_through, last_name, first_name, row_to_append,\
                    final_result, find_match):
    for row_num in sheet_to_go_through.rows:
        if row_num[5].value == last_name and \
           row_num[6].value == first_name:
            for cell in row_num:
                row_to_append.append(cell.value)
            copy_to_final(row_to_append, final_result)
            row_to_append = []
            find_match = True
    return find_match


# main function
def main():
    open_xl_file()

root = Tk()
MainWindow(root)
root.mainloop()