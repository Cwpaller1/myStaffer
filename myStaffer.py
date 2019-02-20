"""This is the start of the myStaffer project.
Created by Cory Paller."""

# shebang line
# ! usr/bin/env Python3.

from openpyxl import *              # for excel files
from tkinter import *               # for Gui
from tkinter import ttk             # for modern Gui widgets
from tkinter import filedialog      # for file chooser
import shelve                       # to save our database

# global variables and import shelve data
file_name = ''
list_of_people = []
search_results = []
id_num = 1000000000


'''Main Tk Window
'''


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

        for F in (StartPage, ChooseFile, Staffer, Candidate, SearchPage, AddNewPerson, EditPage):
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


'''Window Pages
'''


# create StartPage for the program, inheriting from Frame
class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # add a widget that welcomes the user.
        frame1 = ttk.Frame(self)
        ttk.Label(frame1, text="Welcome to myStaffer").grid(sticky='ew')
        ttk.Button(frame1, text="Candidate", command=lambda: controller.show_frame(Candidate)).grid(row=1, sticky='ew')
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
        ttk.Button(frame1, text='Back to Home Page', command=lambda: controller.show_frame(StartPage)).\
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

        self.status = StringVar()
        status_frame = StatusBar(self)
        status_frame.grid(row=2, columnspan=5, sticky='sew')
        status_frame.grid_columnconfigure(0, weight=1)

        self.grid(row=2, )

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    def open_dialog_box(self, controller):
        global file_name
        file_name = filedialog.askopenfilename()
        ttk.Label(self, text=file_name).grid(row=0, column=2)
        ttk.Button(self, text="Import File Contents", command=self.import_file).\
            grid(row=1, columnspan=2, pady=10, sticky='s')
        ttk.Button(self, text="Back to Home Page", command=lambda: controller.show_frame(StartPage)).\
            grid(row=1, column=2, sticky='s')

    # function that takes a file and creates Person objects out of each row and appends them to the list of people.
    def import_file(self):
        global list_of_people
        file1 = load_workbook(file_name)
        for row in file1.active.rows:
            new_person = Person()
            new_person.take_via_excel(row)
            list_of_people.append(new_person)
        self.status.set("List imported!")


# create SearchPage
class SearchPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        # define my StringVariables and page variables
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

        self.search_dict = []
        self.button_list = []

        # create master frame
        master_frame = ttk.Frame(self)

        # create frame for user input
        frame1 = ttk.Frame(master_frame)
        ttk.Label(frame1, text="Search for a Person").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(frame1, text="First: ").grid(row=2, column=0, sticky='w')
        ttk.Label(frame1, text="Last: ").grid(row=3, column=0, sticky='w')
        ttk.Label(frame1, text="Address: ").grid(row=4, column=0, sticky='w')
        ttk.Label(frame1, text="Phone: ").grid(row=5, column=0, sticky='w')
        ttk.Label(frame1, text="Email: ").grid(row=6, column=0, sticky='w')
        self.first_entry = ttk.Entry(frame1, width=15)
        self.first_entry.grid(row=2, column=1, sticky='e')
        self.last_entry = ttk.Entry(frame1, width=15)
        self.last_entry.grid(row=3, column=1, sticky='e')
        self.address_entry = ttk.Entry(frame1, width=15)
        self.address_entry.grid(row=4, column=1, sticky='e')
        self.phone_entry = ttk.Entry(frame1, width=15)
        self.phone_entry.grid(row=5, column=1, sticky='e')
        self.email_entry = ttk.Entry(frame1, width=15)
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
        self.first_label = ttk.Label(self.frame3, textvariable=self.first_strvar, width=25)\
            .grid(row=1, column=1, sticky='e')
        self.last_label = ttk.Label(self.frame3, textvariable=self.last_strvar, width=25)\
            .grid(row=2, column=1, sticky='e')
        self.address_label = ttk.Label(self.frame3, textvariable=self.address_strvar, width=25)\
            .grid(row=3, column=1, sticky='e')
        self.city_label = ttk.Label(self.frame3, textvariable=self.city_strvar, width=25)\
            .grid(row=4, column=1, sticky='e')
        self.state_label = ttk.Label(self.frame3, textvariable=self.state_strvar, width=25)\
            .grid(row=5, column=1, sticky='e')
        self.zip_code_label = ttk.Label(self.frame3, textvariable=self.zip_strvar, width=25)\
            .grid(row=6, column=1, sticky='e')
        self.cell_label = ttk.Label(self.frame3, textvariable=self.cell_strvar, width=25).\
            grid(row=7, column=1, sticky='e')
        self.work_label = ttk.Label(self.frame3, textvariable=self.work_strvar, width=25)\
            .grid(row=8, column=1, sticky='e')
        self.home_label = ttk.Label(self.frame3, textvariable=self.home_strvar, width=25)\
            .grid(row=9, column=1, sticky='e')
        self.email_label = ttk.Label(self.frame3, textvariable=self.email_strvar, width=25)\
            .grid(row=10, column=1, sticky='e')
        self.frame3.grid(row=0, column=2, sticky='n')

        frame4 = ttk.Frame(master_frame)
        ttk.Button(frame4, text="Return to Home Screen", command=lambda: controller.show_frame(StartPage)).\
            grid(row=1, column=0)
        frame4.grid(row=1, column=0, sticky='ew', columnspan=4, pady=50)
        frame4.grid_columnconfigure(0, weight=1)

        # add status bar
        self.status = StringVar()
        status_frame = StatusBar(self)
        status_frame.grid(row=1, column=0, sticky='nsew')
        status_frame.grid_columnconfigure(0, weight=1)

        master_frame.grid(row=0, column=0, padx=50, sticky='ew')
        master_frame.grid_rowconfigure(0, weight=1)
        master_frame.grid_columnconfigure(1, weight=1)

    def submit_search(self):
        self.search_dict = []
        # assign entry edits to keys and place in dictionary
        self.search_dict.append(self.first_entry.get().lower())
        self.search_dict.append(self.last_entry.get().lower())
        self.search_dict.append(self.address_entry.get().lower())
        self.search_dict.append(self.phone_entry.get().lower())
        self.search_dict.append(self.email_entry.get().lower())

        if self.search_dict[0] == '' and self.search_dict[1] == '' and self.search_dict[2] == '' and \
                self.search_dict[3] == '' and self.search_dict[4] == '':
            self.status.set('Error. Search fields are empty.')
        else:
            self.delete_search_data()

            # pass dictionary to search_list function
            search_list(self.search_dict)
            # display results
            row_num = 1
            for x in search_results:
                new_button = ResultButton(self.frame2, x, self)
                new_button.grid(row=row_num, column=0, sticky='ew')
                self.button_list.append(new_button)
                row_num += 1
            if len(search_results) > 0:
                self.status.set('Success. We found something!')
            else:
                self.status.set('We searched and searched...but nothing.')

    def delete_search_data(self):
        # clear search results
        global search_results
        search_results = []

        # clear entries
        self.first_entry.delete(0, END)
        self.last_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)

        # clear smart variables
        self.first_strvar.set('')
        self.last_strvar.set('')
        self.address_strvar.set('')
        self.city_strvar.set('')
        self.state_strvar.set('')
        self.zip_strvar.set('')
        self.cell_strvar.set('')
        self.work_strvar.set('')
        self.home_strvar.set('')
        self.email_strvar.set('')

        # delete all of the buttons
        for x in self.button_list:
            x.destroy()


class AddNewPerson(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # master frame for page
        master_frame = ttk.Frame(self)

        # title frame
        frame1 = ttk.Frame(master_frame)
        ttk.Label(frame1, text="Add New Person to Database").grid(sticky='ew', pady=15)
        frame1.grid(row=0, column=0, columnspan=2)
        frame1.grid_rowconfigure(0, weight=1)

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
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(1, weight=1)

        self.status = StringVar()
        status_frame = StatusBar(self)
        status_frame.grid(row=1, column=0, sticky='nsew')
        status_frame.grid_columnconfigure(0, weight=1)

        master_frame.grid(row=0, column=0)
        master_frame.grid_rowconfigure(0, weight=1)
        master_frame.grid_columnconfigure(0, weight=1)

        # create list for entries
        self.new_person_list = {}

    def check_fields(self):
        # call create_person_list to set entries to self.new_person_list
        self.create_person_list()

        if self.new_person_list['first'] is '' or self.new_person_list['last'] is '':
            return False
        else:
            return True

    def create_person_list(self):
        self.new_person_list = {
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

    def submit_person_to_database(self):
        global list_of_people

        # check fields
        if self.check_fields() is True:
            new_person = Person()
            new_person.take_via_new_person(self.new_person_list)
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
            self.status.set('Success. New Person was added to database.')

        else:
            self.status.set('Error. Missing First or Last Name. Try again.')


class EditPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        # master frame for page
        master_frame = ttk.Frame(self)

        # title frame
        frame1 = ttk.Frame(master_frame)
        ttk.Label(frame1, text="Edit Person").grid(sticky='ew', pady=15)
        frame1.grid(row=0, column=0, columnspan=2)
        frame1.grid_rowconfigure(0, weight=1)

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
        self.submit_button = ttk.Button(frame2, text='Submit Edits')
        self.submit_button.grid(row=11, column=0, columnspan=2, sticky='ew')
        # pack body frame
        frame2.grid(row=1, column=0)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(1, weight=1)

        self.status = StringVar()
        status_frame = StatusBar(self)
        status_frame.grid(row=1, column=0, sticky='nsew')
        status_frame.grid_columnconfigure(0, weight=1)

        master_frame.grid(row=0, column=0)
        master_frame.grid_rowconfigure(0, weight=1)
        master_frame.grid_columnconfigure(0, weight=1)


'''Global Functions
'''


# function that searches list of people and returns a person
def search_list(person_to_find):
    global search_results

    # flip through the tuples in person_to_find looking for a match
    for x in list_of_people:
        if person_to_find[0] in x.first.lower() or person_to_find[0] == '':
            if person_to_find[1] in x.last.lower() or person_to_find[1] == '':
                if person_to_find[2] in x.address.lower() or person_to_find[2] == '':
                    if person_to_find[3] in x.cell or person_to_find[3] in x.home or person_to_find[3] in x.work or \
                            person_to_find[3] == '':
                        if person_to_find[4] in x.email or person_to_find[4] == '':
                            search_results.append(x)


# function that saves data onto a Shelve file when the program closes.


'''Objects
'''


# Class that creates a Person object
class Person(object):
    def __init__(self):
        # set unique object id
        global id_num
        self.id = id_num
        id_num += 1

        # set object initialization variables.
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
        self.notes = ''

    # function for when you make Person objects via Excel import
    def take_via_excel(self, row):
        self.first = row[0].value
        self.last = row[1].value
        self.address = row[2].value
        self.city = row[3].value
        self.state = row[4].value
        self.zip_code = str(row[5].value)
        self.zip_code = self.zip_code[0:5]
        self.cell = str(row[6].value)
        self.cell = self.cell[0:10]
        self.home = str(row[7].value)
        self.home = self.home[0:10]
        self.work = str(row[8].value)
        self.work = self.work[0:10]
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
class ResultButton(ttk.Button):
    def __init__(self, parent, person, controller):
        ttk.Button.__init__(self, parent)
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


class StatusBar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.config(relief=SUNKEN, borderwidth=3)
        self.label1 = ttk.Label(self, textvariable=parent.status).pack(side='left')


class EditButton(ttk.Button):
    def __init__(self, parent, person):
        ttk.Button.__init__(self, parent)
        self.config(text="Edit Person...")
        self.person_obj = person

    def button_push(self):
        pass


def quit_save():
    shelve_data = shelve.open('my_shelve_data')
    shelve_data['list_of_people'] = list_of_people
    shelve_data.close()
    myStaffer.destroy()


myStaffer = MyStafferApp()
myStaffer.geometry('900x600')
myStaffer.title = 'myStaffer'
myStaffer.protocol("WM_DELETE_WINDOW", quit_save)
myStaffer.mainloop()
