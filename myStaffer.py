'''This is the start of the myStaffer project.
Created by Cory Paller.'''

# shebang line
#! usr/bin/env Python3.

import openpyxl
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

file_name = ''


# create object that inherits from Tk
class myStafferapp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, 'myStaffer Program')
        container = Frame(self)
        # create cascading toolbar at the top
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # create first cascade
        first_cascade = Menu(menu_bar)
        menu_bar.add_cascade(label='File', menu=first_cascade)
        first_cascade.add_command(label='Choose Excel File...', command=self.choose_Excel_File)

        # create second cascade
        second_cascade = Menu(menu_bar)
        menu_bar.add_cascade(label='Functions', menu=second_cascade)
        second_cascade.add_command(label='Sort First Sheet by Subsequent Sheets')
        second_cascade.add_command(label='Add People into Database')

        # pack container into Tk
        container.pack()

        # create dictionary that hold our frames
        self.Frames = {}

        for F in (StartPage, ChooseFile):
            # create StartPage frame
            frame = F(container, self)
            # add our new frame into the dictionary of frames
            self.Frames[str(F)] = frame
            # pack frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    # create method that will show the frame we want
    def show_frame(self, controller):
        frame = self.Frames[str(controller)]
        # raise frame to front using built in Tk method
        frame.tkraise()

    def choose_Excel_File(self):
        self.show_frame(ChooseFile)


# create StartPage for the program, inheriting from Frame
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # add a widget that welcomes the user.
        label = Label(self, text="Welcome to myStaffer").pack(side=TOP, fill=X)
        ttk.Button(self, text="Upload New File", command=controller.choose_Excel_File).pack(side=TOP)


# create ChooseFile frame for the program, inheriting from Frame
class ChooseFile(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # create a label, an entry and a button.
        ttk.Button(self, text="Choose File", command=lambda:self.open_dialog_box(controller)).grid(row=0, column=0,\
                                                                                                   padx=5, pady=10)
        ttk.Label(self, text='File name: ').grid(row=0, column=1)

    def open_dialog_box(self, controller):
        file_name = (filedialog.askopenfilename())
        ttk.Label(self, text=file_name).grid(row=0, column=2)
        ttk.Button(self, text="Import File Contents", command=import_file).grid(row=1, columnspan=2, pady = 10)
        ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(StartPage)).grid(row=1, column=2)


def import_file():
    list_of_people = []
    file1 = openpyxl.load_workbook(file_name)
    for row in file1.active.rows:
        new_person = Person(row)
        list_of_people.append(new_person)
    print(list_of_people)


class Person(object):
    def __init__(self, row):
        self.first = row[0]
        self.last = row[1]
        self.address = row[2]
        self.city = row[3]
        self.state = row[4]
        self.zip_code = row[5]
        self.cell = row[6]
        self.home = row[7]
        self.work = row[8]
        self.email = row[9]


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


myStaffer = myStafferapp()
myStaffer.title = 'myStaffer'
myStaffer.mainloop()