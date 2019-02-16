'''This is the start of the myStaffer project.
Created by Cory Paller.'''

# shebang line
#! usr/bin/env Python3.

import openpyxl
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import shelve

# global variables and import shelve data

file_name = ''
list_of_people = []
search_results = []


# create object that inherits from Tk
class MyStafferApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, 'myStaffer Program')
        container = ttk.Frame(self)

        # pack container into Tk
        container.pack(side='top', fill=BOTH, expand=TRUE)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # create dictionary that hold our frames
        self.Frames = {}

        for F in (StartPage, ChooseFile, Staffer, Candidate, SearchPage, AddNewPerson):
            # create page
            frame = F(container, self)
            # add our new frame into the dictionary of frames
            self.Frames[str(F)] = frame
            # grid the frame

            frame.grid(row=0, column=0, sticky='nsew')
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame(StartPage)

        # create cascading toolbar at the top
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # create General cascade
        # create second cascade
        general_cascade = Menu(menu_bar)
        menu_bar.add_cascade(label='General', menu=general_cascade)
        general_cascade.add_command(label='Back to Home Page', command=lambda: self.show_frame(StartPage))
        general_cascade.add_command(label='Search', command=lambda: self.show_frame(SearchPage))

        # create Candidate cascade
        candidate_cascade = Menu(menu_bar)
        menu_bar.add_cascade(label='Candidate', menu=candidate_cascade)
        candidate_cascade.add_command(label='Search', command=lambda: self.show_frame(SearchPage))
        candidate_cascade.add_command(label='Call Time')
        candidate_cascade.add_command(label='Reports')

        # create Staffer cascade
        staffer_cascade = Menu(menu_bar)
        menu_bar.add_cascade(label='Staffer', menu=staffer_cascade)
        staffer_cascade.add_command(label='Search', command=lambda: self.show_frame(SearchPage))
        staffer_cascade.add_command(label='Add New Person To Database', command=lambda: self.show_frame(AddNewPerson))
        staffer_cascade.add_command(label='Upload New File', command=lambda: self.show_frame(ChooseFile))
        staffer_cascade.add_command(label='Create List')

        # load in pre-loaded people
        global list_of_people
        shelve_data = shelve.open('my_shelve_data')
        if 'list_of_people' in shelve_data:
            list_of_people = shelve_data['list_of_people']
        shelve_data.close()

    # create method that will show the frame we want
    def show_frame(self, controller):
        frame = self.Frames[str(controller)]
        # raise frame to front using built in Tk method
        frame.tkraise()


# create StartPage for the program, inheriting from Frame
class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # add a widget that welcomes the user.
        frame1 = ttk.Frame(self)
        ttk.Label(frame1, text="Welcome to myStaffer").grid(sticky='ew')
        ttk.Button(frame1, text="Candidate", command= lambda: controller.show_frame(Candidate)).grid(row=1,
                                                                                                     sticky='ew')
        ttk.Button(frame1, text="Staffer", command=lambda: controller.show_frame(Staffer)).grid(row=2, sticky='ew')
        ttk.Button(frame1, text="Upload New File", command=lambda: controller.show_frame(ChooseFile)).\
            grid(row=3, sticky='ew')
        frame1.grid(row=0, column=0)
        frame1.grid_rowconfigure(0, weight=1)


# create Staffer Window
class Staffer(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # add widgets
        frame1 = ttk.Frame(self)
        ttk.Button(frame1, text='Search', command=lambda: controller.show_frame(SearchPage)).\
            grid(row=0, column=0, sticky='ew')
        ttk.Button(frame1, text='Add New Person To Database', command=lambda: controller.show_frame(AddNewPerson)). \
            grid(row=1, column=0, sticky='ew')
        ttk.Button(frame1, text='Upload New File', command=lambda: controller.show_frame(ChooseFile)).\
            grid(row=2, column=0, sticky='ew')
        ttk.Button(frame1, text='Back to Home Page', command=lambda: controller.show_frame(StartPage)).\
            grid(row=3, column=0, sticky='ew')
        frame1.grid(row=0, column=0)
        frame1.grid_rowconfigure(0, weight=1)


# create Candidate Window
class Candidate(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # add widgets
        frame1 = ttk.Frame(self)
        ttk.Button(frame1, text='Search', command=lambda: controller.show_frame(SearchPage)).grid(row=0, column=0,
                                                                                                  sticky='ew')
        ttk.Button(frame1, text='Call Time').grid(row=1, column=0, sticky='ew')
        ttk.Button(frame1, text='Reports').grid(row=2, column=0, sticky='ew')
        ttk.Button(frame1, text='Back to Home Page', command=lambda:controller.show_frame(StartPage)).\
            grid(row=3, column=0, sticky='ew')
        frame1.grid(row=0, column=0)
        frame1.grid_rowconfigure(0, weight=1)


# create ChooseFile frame for the program, inheriting from Frame
class ChooseFile(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # create a label, an entry and a button.
        ttk.Button(self, text="Choose File", command=lambda: self.open_dialog_box(controller)).\
            grid(row=0, column=0, padx=5, pady=10)
        ttk.Label(self, text='File name: ').grid(row=0, column=1)

    def open_dialog_box(self, controller):
        global file_name
        file_name = filedialog.askopenfilename()
        ttk.Label(self, text=file_name).grid(row=0, column=2)
        ttk.Button(self, text="Import File Contents", command=import_file).\
            grid(row=1, columnspan=2, pady=10)
        ttk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(StartPage)).\
            grid(row=1, column=2)


class SearchPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        master_frame = ttk.Frame(self)
        # define my StringVariables
        self.first_strvar = StringVar()
        self.last_strvar = StringVar()
        self.address_strvar = StringVar()
        self.city_strvar = StringVar()
        self.state_strvar = StringVar()
        self.zip_strvar = StringVar()
        self.cell_strvar = StringVar()
        self.work_strvar = StringVar()
        self.home_strvar = StringVar()
        self.email_strvar = StringVar()

        # create frame for user input
        frame1 = ttk.Frame(master_frame)
        ttk.Label(frame1, text="Search for a Person").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(frame1, text="First: ").grid(row=2, column=0, sticky='w')
        ttk.Label(frame1, text="Last: ").grid(row=3, column=0, sticky='w')
        ttk.Label(frame1, text="Address: ").grid(row=4, column=0, sticky='w')
        ttk.Label(frame1, text="Phone: ").grid(row=5, column=0, sticky='w')
        ttk.Label(frame1, text="Email: ").grid(row=6, column=0, sticky='w')
        self.first_entry = ttk.Entry(frame1, width=10)
        self.first_entry.grid(row=2, column=1, sticky='e')
        self.last_entry = ttk.Entry(frame1, width=10)
        self.last_entry.grid(row=3, column=1, sticky='e')
        self.address_entry = ttk.Entry(frame1, width=10)
        self.address_entry.grid(row=4, column=1, sticky='e')
        self.phone_entry = ttk.Entry(frame1, width=10)
        self.phone_entry.grid(row=5, column=1, sticky='e')
        self.email_entry = ttk.Entry(frame1, width=10)
        self.email_entry.grid(row=6, column=1, sticky='e')
        ttk.Button(frame1, text="Search...", command=self.submit_search).grid(row=8, column=0,
                                                                              columnspan=2, sticky='ew')
        frame1.grid(row=0, column=0, sticky='n')

        # create frame for search results to be displayed as buttons
        self.frame2 = ttk.Frame(master_frame)
        ttk.Label(self.frame2, text="Search Results").grid(row=0, column=0, pady=5)
        self.frame2.grid(row=0, column=1, sticky='n')

        # create frame for person info to be displayed if their button is pressed
        self.frame3 = ttk.Frame(master_frame)
        ttk.Label(self.frame3, text='Contact Details').grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(self.frame3, text='First: ').grid(row=1, column=0, sticky='w')
        ttk.Label(self.frame3, text='Last: ').grid(row=2, column=0, sticky='w')
        ttk.Label(self.frame3, text='Address: ').grid(row=3, column=0, sticky='w')
        ttk.Label(self.frame3, text='City: ').grid(row=4, column=0, sticky='w')
        ttk.Label(self.frame3, text='State: ').grid(row=5, column=0, sticky='w')
        ttk.Label(self.frame3, text='Zip Code: ').grid(row=6, column=0, sticky='w')
        ttk.Label(self.frame3, text='Cell: ').grid(row=7, column=0, sticky='w')
        ttk.Label(self.frame3, text='Work: ').grid(row=8, column=0, sticky='w')
        ttk.Label(self.frame3, text='Home: ').grid(row=9, column=0, sticky='w')
        ttk.Label(self.frame3, text='Email: ').grid(row=10, column=0, sticky='w')
        # blank labels to be set later
        self.first_label = ttk.Label(self.frame3, textvariable=self.first_strvar, width=15)\
            .grid(row=1, column=1, sticky='e')
        self.last_label = ttk.Label(self.frame3, textvariable=self.last_strvar, width=15)\
            .grid(row=2, column=1, sticky='e')
        self.address_label = ttk.Label(self.frame3, textvariable=self.address_strvar, width=15)\
            .grid(row=3, column=1, sticky='e')
        self.city_label = ttk.Label(self.frame3, textvariable=self.city_strvar, width=15)\
            .grid(row=4, column=1, sticky='e')
        self.state_label = ttk.Label(self.frame3, textvariable=self.state_strvar, width=15)\
            .grid(row=5, column=1, sticky='e')
        self.zip_code_label = ttk.Label(self.frame3, textvariable=self.zip_strvar, width=15)\
            .grid(row=6, column=1, sticky='e')
        self.cell_label = ttk.Label(self.frame3, textvariable=self.cell_strvar, width=15).\
            grid(row=7, column=1, sticky='e')
        self.work_label = ttk.Label(self.frame3, textvariable=self.work_strvar, width=15)\
            .grid(row=8, column=1, sticky='e')
        self.home_label = ttk.Label(self.frame3, textvariable=self.home_strvar, width=15)\
            .grid(row=9, column=1, sticky='e')
        self.email_label = ttk.Label(self.frame3, textvariable=self.email_strvar, width=15)\
            .grid(row=10, column=1, sticky='e')
        self.frame3.grid(row=0, column=2, sticky='n')

        frame4 = ttk.Frame(master_frame)
        ttk.Button(frame4, text="Return to Home Screen", command=lambda: controller.show_frame(StartPage)).\
            grid(row=1, column=0)
        frame4.grid(row=1, column=0, sticky='ew', columnspan=4, pady=50)
        frame4.grid_columnconfigure(0, weight=1)

        # create dictionary to hold entry edits
        self.search_dict = {}

        master_frame.grid(row=0, column=0, sticky='ew', padx= 20)
        master_frame.grid_rowconfigure(0, weight=1)
        master_frame.grid_columnconfigure(0, weight=1)
        master_frame.grid_columnconfigure(1, weight=1)

    def submit_search(self):
        # assign entry edits to keys and place in dictionary
        self.search_dict['first'] = self.first_entry.get()
        self.search_dict['last'] = self.last_entry.get()
        self.search_dict['address'] = self.address_entry.get()
        self.search_dict['phone'] = self.phone_entry.get()
        self.search_dict['email'] = self.email_entry.get()

        # pass dictionary to search_list function
        search_list(self.search_dict)
        # display results
        row_num = 1
        for x in search_results:
            new_button = ResultButton(self.frame2, x, self)
            new_button.grid(row=row_num, column=0)
            row_num += 1

class AddNewPerson(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # master frame for page
        master_frame = ttk.Frame(self)

        # title frame
        frame1 = ttk.Frame(master_frame)
        ttk.Label(frame1, text="Add New Person to Database").grid(sticky='ew', pady=15)
        frame1.grid(row=0, column=0, sticky='ew')

        # body frame
        frame2 = ttk.Frame(master_frame)
        # header labels
        ttk.Label(frame2, text='First: ').grid(row=1, column=0, sticky='w')
        ttk.Label(frame2, text='Last: ').grid(row=2, column=0, sticky='w')
        ttk.Label(frame2, text='Address: ').grid(row=3, column=0, sticky='w')
        ttk.Label(frame2, text='City: ').grid(row=4, column=0, sticky='w')
        ttk.Label(frame2, text='State: ').grid(row=5, column=0, sticky='w')
        ttk.Label(frame2, text='Zip Code: ').grid(row=6, column=0, sticky='w')
        ttk.Label(frame2, text='Cell: ').grid(row=7, column=0, sticky='w')
        ttk.Label(frame2, text='Home: ').grid(row=8, column=0, sticky='w')
        ttk.Label(frame2, text='Work: ').grid(row=9, column=0, sticky='w')
        ttk.Label(frame2, text='Email: ').grid(row=10, column=0, sticky='w')
        # user entry
        self.first_entry = ttk.Entry(frame2)
        self.first_entry.grid(row=1, column=1, sticky='e')
        self.last_entry = ttk.Entry(frame2)
        self.last_entry.grid(row=2, column=1, sticky='e')
        self.address_entry = ttk.Entry(frame2)
        self.address_entry.grid(row=3, column=1, sticky='e')
        self.city_entry = ttk.Entry(frame2)
        self.city_entry.grid(row=4, column=1, sticky='e')
        self.state_entry = ttk.Entry(frame2)
        self.state_entry.grid(row=5, column=1, sticky='e')
        self.zip_code_entry = ttk.Entry(frame2)
        self.zip_code_entry.grid(row=6, column=1, sticky='e')
        self.cell_entry = ttk.Entry(frame2)
        self.cell_entry.grid(row=7, column=1, sticky='e')
        self.home_entry = ttk.Entry(frame2)
        self.home_entry.grid(row=8, column=1, sticky='e')
        self.work_entry = ttk.Entry(frame2)
        self.work_entry.grid(row=9, column=1, sticky='e')
        self.email_entry = ttk.Entry(frame2)
        self.email_entry.grid(row=10, column=1, sticky='e')
        # submit button
        self.submit_button = ttk.Button(frame2, text='Submit New Person', command=self.submit_person_to_database)
        self.submit_button.grid(row=11, column=0, columnspan=2, sticky='ew')
        # pack body frame
        frame2.grid(row=1, column=0)

        master_frame.grid(row=0, column=0)
        master_frame.grid_rowconfigure(0, weight=1)
        master_frame.grid_columnconfigure(0, weight=1)

    def submit_person_to_database(self):
        global list_of_people
        new_person_list = {
            'first': self.first_entry.get(),
            'last': self.last_entry.get(),
            'address': self.address_entry.get(),
            'city': self.city_entry.get(),
            'state': self.state_entry.get(),
            'zip_code': self.zip_code_entry.get(),
            'cell': self.cell_entry.get(),
            'home': self.home_entry.get(),
            'work': self.work_entry.get(),
            'email': self.email_entry.get(),
            }

        new_person = Person()
        new_person.take_via_new_person(new_person_list)
        list_of_people.append(new_person)

        # clear the entries
        self.first_entry.delete(0, 'end')
        self.last_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.city_entry.delete(0, 'end')
        self.state_entry.delete(0, 'end')
        self.zip_code_entry.delete(0, 'end')
        self.cell_entry.delete(0, 'end')
        self.home_entry.delete(0, 'end')
        self.work_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')


# function that takes a file and creates Person objects out of each row and appends them to the list of people.
def import_file():
    global list_of_people
    file1 = openpyxl.load_workbook(file_name)
    for row in file1.active.rows:
        new_person = Person()
        new_person.take_via_excel(row)
        list_of_people.append(new_person)
    print_list_of_people(list_of_people)


# function that searches list of people and returns a person
def search_list(person_to_find):
    global list_of_people
    global search_results

    # flip through the tuples in person_to_find looking for a match
    for x in person_to_find:
        # check for first name match
        if x == 'first':
            # flip through tuples in list_of_people to find match
            for y in list_of_people:
                if person_to_find.get(x) == y.first:
                    search_results.append(y)
        # check for last name match
        elif x == 'last':
            for y in list_of_people:
                if person_to_find.get(x) == y.last:
                    search_results.append(y)
        # check for address match
        elif x == 'address':
            for y in list_of_people:
                if person_to_find.get(x) == y.address:
                    search_results.append(y)
        # check for phone match
        elif x == 'phone':
            for y in list_of_people:
                if person_to_find.get(x) == y.cell or x == y.home or x == y.work:
                    search_results.append(y)
        # check for email match
        elif x == 'email':
            for y in list_of_people:
                if person_to_find.get(x) == y.email:
                    search_results.append(y)


# Class that creates a Person object
class Person(object):
    def __init__(self):
        self.first = ''
        self.last = ''
        self.address = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.cell = ''
        self.work = ''
        self.home = ''
        self.email = ''

    # function for when you make Person objects via Excel import
    def take_via_excel(self, row):
        self.first = row[0].value
        self.last = row[1].value
        self.address = row[2].value
        self.city = row[3].value
        self.state = row[4].value
        self.zip_code = row[5].value
        self.cell = row[6].value
        self.home = row[7].value
        self.work = row[8].value
        self.email = row[9].value

    # function for when you make Person object via New Person Page
    def take_via_new_person(self, new_person_list):
        self.first = new_person_list['first']
        self.last = new_person_list['last']
        self.address = new_person_list['address']
        self.city = new_person_list['city']
        self.state = new_person_list['state']
        self.zip_code = new_person_list['zip_code']
        self.cell = new_person_list['cell']
        self.home = new_person_list['home']
        self.work = new_person_list['work']
        self.email = new_person_list['email']


# creates a button for each result
class ResultButton(Button):
    def __init__(self, parent, person, controller):
        Button.__init__(self, parent)
        self.controller = controller
        self.person = person
        self.config(text=(person.last + ', ' + person.first), command=self.display_page)

    def display_page(self):
        self.controller.first_strvar.set(self.person.first)
        self.controller.last_strvar.set(self.person.last)
        self.controller.address_strvar.set(self.person.address)
        self.controller.city_strvar.set(self.person.city)
        self.controller.state_strvar.set(self.person.state)
        self.controller.zip_strvar.set(self.person.zip_code)
        self.controller.cell_strvar.set(self.person.cell)
        self.controller.work_strvar.set(self.person.work)
        self.controller.home_strvar.set(self.person.home)
        self.controller.email_strvar.set(self.person.email)


def quit_save():
    shelve_data = shelve.open('my_shelve_data')
    shelve_data['list_of_people'] = list_of_people
    shelve_data.close()
    myStaffer.destroy()


myStaffer = MyStafferApp()
myStaffer.geometry('800x600')
myStaffer.title = 'myStaffer'
myStaffer.protocol("WM_DELETE_WINDOW", quit_save)
myStaffer.mainloop()


'''
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
'''
