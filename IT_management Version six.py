# Nayland College IT and building management program

# Ella Harley - 3CSC - 08/05/2026

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Importing Tkinter, which is the framework for my GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from queue import PriorityQueue

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Data storage

# Lets me access all of the site navigation data anywhere
class site_navigation:
    def __init__(self):
        # empty stack to put all of the open windows
        self.history_stack = []
        # sets current page to be empty - this gets replaced every time a new window is opened
        self.current_page = None

    # runs when a new window is opened
    def visit(self, new_page):

        # if current page has a value
        if self.current_page:
            # hides the current window (without destroying it), so it can be restored later with deicoinify() 
            self.current_page.withdraw()
            # Saves the hidden page onto the stack
            self.history_stack.append(self.current_page)

        # Sets the newly opened window as the current [age]
        self.current_page = new_page

    # Runs when a back button is pressed
    def go_back(self):
        # Destroys the current page
        self.current_page.destroy()

        # If there is anything on the stack,
        if self.history_stack:
            # Removes the most recent page from the stack and makes it the current page
            self.current_page = self.history_stack.pop()
            # Opens the hidden window
            self.current_page.deiconify()
        
# Creates an object out of the class
nav_controller = site_navigation()

# Stores all the current issues
current_issues = []

# Creates a priority queue for the issues   
issue_queue = PriorityQueue()

# ID
issue_number = 1

# Makes a back arrow character to be used for the back button
back_arrow = "\u2190"

# Language setting, the program starts in english

language = "English"
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# This is the window that allows all issues to be viewed
def dashboard():

    # Establishes the framework
    dashboard_window = tk.Toplevel()

    nav_controller.visit(dashboard_window)

    # Sets the size of the window
    dashboard_window.geometry("500x500+700+200")

    # Gives the window a title
    # If the language is set to english, displays the English translation. If the language is Māori, displays the Māori translation. This is consistent across the program.
    if language == "English":
        dashboard_window.title("IT and Building Management - Nayland College")
    else:
        dashboard_window.title("Hangarau pārongo me te Whakahaere Whare - Te Kāreti o Neirana")

    # Makes the window non-resizable
    dashboard_window.resizable(False, False) 

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Creates a back button to go back to the preivous window
    back_button_report = tk.Button(dashboard_window, text = f"{back_arrow}", font = ("Wingdings 3", 10), command = nav_controller.go_back)
    # Places the button in a specific location on the screen - It is placed in a spot that most websies generally have a back button (top left corner)
    back_button_report.place(x = 15, y = 10)

    # Title
    if language == "English":
        dashboard_heading = tk.Label(dashboard_window, text = "Current Issues", font = ("Arial", 17))
    else:
        dashboard_heading = tk.Label(dashboard_window, text = "Nga take o naianei", font = ("Arial", 17))
    
    dashboard_heading.pack(pady = 10)

    # Sets up a tkinter treeview - like a spreadsheet, with different columns for each item in the issue dictionary
    dashboard_tree = ttk.Treeview(dashboard_window, columns = ("ID", "Type", "Location", "Priority", "Status"), show = "headings", height = 11)

    # Sets up the heading texts and puts them in the right spots
    if language == "English":
        dashboard_tree.heading("ID", text = "ID")
        dashboard_tree.heading("Type", text = "Issue Type")
        dashboard_tree.heading("Location", text = "Location")
        dashboard_tree.heading("Priority", text = "Priority")
        dashboard_tree.heading("Status", text = "Status")

    # Māori headings
    else:
        dashboard_tree.heading("ID", text = "Tautuhi")
        dashboard_tree.heading("Type", text = "Momo")
        dashboard_tree.heading("Location", text = "Wāhi")
        dashboard_tree.heading("Priority", text = "Whakaarotau")
        dashboard_tree.heading("Status", text = "Āhua")

    # Sets the widths of each column
    dashboard_tree.column("ID", width = 40)
    dashboard_tree.column("Type", width = 120)
    dashboard_tree.column("Location", width = 100)
    dashboard_tree.column("Priority", width = 70)
    dashboard_tree.column("Status", width = 90)

    # For every issue in my current_issues, puts the specificed value in the treeview by calling the key
    for issue in current_issues:
        dashboard_tree.insert("", "end", values = (issue["id"], issue["type"], issue["location"], issue["priority"], issue["status"]))
    
    # Places the tree
    dashboard_tree.pack(pady = 10)

    # Labels the description
    if language == "English":
        description_label = tk.Label(dashboard_window, text = "Description", font = ("Arial", 10))
    else:
        description_label = tk.Label(dashboard_window, text = "Whakaaturanga", font = ("Arial", 10))

    description_label.pack()

    # A place for the description to be shown
    description_box = tk.Text(dashboard_window, font = ("Arial", 10), width = 59, height = 6, state = "disabled")
    description_box.pack(pady = 5)

    # Runs whenever an item in the treeview is clicked
    def show_issue(event):

        # Gets whichever row is selected
        selected_item = dashboard_tree.selection()
        
        # If nothing is selected, stop function
        if not selected_item:
            return

        # Gets all of the data stored in the row
        item = dashboard_tree.item(selected_item)

        # Extracts the values from the row
        values = item["values"]
        
        # Gets the issue ID from the first column
        issue_id = values[0]

        # Iterates through all of the issues
        for issue in current_issues:

            # if the current issue matches the ID
            if issue["id"] == issue_id:
                # Clears the previous description text
                description_box.delete("1.0", "end-1c")
                
                # Inserts the selected description issue into the box
                description_box.insert(tk.END, issue["desc"])
          

    # Binds show_issue to run whenever something is selected
    dashboard_tree.bind("<<TreeviewSelect>>", show_issue)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# This is the window that allows for the reporting of issues to happen
def report():

    # Establishes the framework
    report_window = tk.Toplevel()

    nav_controller.visit(report_window)

    # Sets the size of the window
    report_window.geometry("500x500+700+200")

    # Gives the window a title
    if language == "English":
        report_window.title("IT and Building Management - Nayland College")
    else:
        report_window.title("Hangarau pārongo me te Whakahaere Whare - Te Kāreti o Neirana")
    
    # Makes the window non-resizable
    report_window.resizable(False, False) 

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Saves the entered combobox options to a dictionary
    def issue_submit():
        # GLobals the issue number so I can access it in this function
        global issue_number

        # Checking to see if all fields have been filled out for reporting before creating the issue

        # if the combobox hasnt been changed,
        if language == "English":
            if issue_type_cb.get() == "Select Issue:":
                # Show an error
                messagebox.showerror("Error", "Please fill out what type of issue you are reporting!")
                # Break the loop
                return
    
            if issue_location_cb.get() == "Select Location:":
                messagebox.showerror("Error", "Please fill out where the issue you are reporting is located!")
                return
        
            # description box has a string of characters, so the 1.0 to end-1c tells the code to check the whole thing
            if issue_description.get("1.0", "end-1c") == "":
                messagebox.showerror("Error", "Please fill out a description for your report!")
                return
        
            if priority_cb.get() == "Select Priority:":
                messagebox.showerror("Error", "Please select a priority!")
                return
            
        # Māori translation
        else:
            if issue_type_cb.get() == "Whiriwhiri take:":
                # Show an error
                messagebox.showerror("Hē", "Tēnā koa whakakī he aha te momo take kei te rīpoata e koe!")
                # Break the loop
                return
    
            if issue_location_cb.get() == "Momo take:":
                messagebox.showerror("Hē", "Tēnā koa whakakī kei hea te take e rīpoata ana e koe!")
                return
        
            # description box has a string of characters, so the 1.0 to end-1c tells the code to check the whole thing
            if issue_description.get("1.0", "end-1c") == "":
                messagebox.showerror("Hē", "Tēnā koa whakakī he whakaahuatanga mo to rīpoata!")
                return
        
            if priority_cb.get() == "Whakaarotau take:":
                messagebox.showerror("Hē", "Tēnā koa whakaarotau take!")
                return

        # Framework for the dictionary, grabs all of the data so I can access it later
        issue = {"id" : issue_number,
                 "type" : issue_type_cb.get(),
                 "location" : issue_location_cb.get(),
                 "desc" : issue_description.get("1.0", "end-1c"),
                 "priority" : int(priority_cb.get()),
                 "status" : "incomplete"
        }

        # Appends the issue dictionary to the current issues list
        current_issues.append(issue)

        # Puts the issue into the priority queue
        issue_queue.put((issue["priority"], issue["id"], issue))

        # Increments the issue number by one so more can be stored
        issue_number += 1

        # Messagebox to show a completed issue submission
        if language == "English":
            messagebox.showinfo("Success!", "Issue submitted successfully!")
        else:
            messagebox.showinfo("Angitūtanga!", "I pai te tuku take!")

        nav_controller.go_back()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Creates the priority messagebox to explain the priority system. \n places the text that comes after on the next line.
    def priority_msg():
        if language == "English":
            messagebox.showinfo("Priority Help", "The numbered priority system is a way for us to catalog how urgent the issues are. Please be honest with your selection\n" \
        "\n3 = Lowest Priority, will be fixed within 1-2 weeks.\n2 = Medium Priority, will be fixed within 1-2 days\n1 = Highest Priority, Will be fixed within a few hours to 1 day")
        else: 
            messagebox.showinfo("Te awhina matua","Ko te punaha matua kua tau he huarahi ki a maatau ki te whakariterite i te tere o nga take. Tena koa kia pono to whiringa\n3 = Te Manaakitanga Iti, ka whakatika i roto i te ka tahi-rua wiki. \n2 = Waenga Tuatahi, ka whakatika i roto i te ka tahi-ka rua ra \n 1 = Te Manaakitanga Nui, Ka whakatika i roto i etahi haora ki te ra ka tahi")   

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Defining issue types

    # The different types of issue there could be, plus an other that can be changed

    if language == "English":
        issue_types = ["Wifi", "Broken technology", "Teams syncing", "Broken air conditioning", "Hot water", "Power", "Cybersecurity", "Mould", 
                    "Structural", "Other: Please Specify"]

    # The different locations of the incident
        issue_locations = ["Block 1", "Block 2", "Block 3", "Block 4", "Hospitality", "MT Block", "Red Gym", "Blue Gym", "Canteen", "Student Center", 
                       "MC Block", "F Block", "Field", "Library", "Hall", "Other: Please Specify"]

    # The different priority levels of tasks
        issue_priority = ["1", "2", "3"]

    # Māori
    else:
        issue_types = ["Ipurangi", "Hangarau pakaru", "Tukutahi kapa", "Wai wera", "Punahiko", "Mōhiohio marutau", "Hekaheka", 
                    "Hanganga", "Etahi atu: Tena Whakatauhia"]

    # The different locations of the incident
        issue_locations = ["Poraka Tahi", "Poraka Rua", "Poraka Toru", "Poraka Wha", "Manaaki", "Poraka MT", "Whero Whare kori tinana", "Kahurangi Whare kori tinana", "Kāmuri", "Whare ākonga", 
                       "MC Poraka", "F Poraka", "Apure", "Whare pukapuka", "Hōro", "Etahi atu: Tena Whakatauhia"]

    # The different priority levels of tasks
        issue_priority = ["1", "2", "3"]

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Framework

    # Title of the window
    if language == "English":
        report_title = tk.Label(report_window, text = "Issue Report", font = ("Arial", 17))
    else:
        report_title = tk.Label(report_window, text = "Purongo whakaputa", font = ("Arial", 17))
    
    report_title.pack(pady = 20)

    # Creates a back button to go back to the preivous window
    back_button_report = tk.Button(report_window, text = f"{back_arrow}", font = ("Wingdings 3", 10), command = nav_controller.go_back)
    # Places the button in a specific location on the screen - It is placed in a spot that most websies generally have a back button (top left corner)
    back_button_report.place(x = 15, y = 10)


    # Creates a drop down meny that holds all of the different types of issues, detailed in the "issue types" list above
    issue_type_cb = ttk.Combobox(report_window, values = issue_types)
        
    # Sets the text of the dropdown menu so it is clear what needs to be changed
    if language == "English":
        issue_type_cb.set("Select Issue:")
    else:
        issue_type_cb.set("Whiriwhiri take:")
    
    issue_type_cb.pack(pady = 10)


    # Holds the different locations, as detailed in the "issue locations" list above
    issue_location_cb = ttk.Combobox(report_window, values = issue_locations)
    if language == "English":
        issue_location_cb.set("Select Location:")
    else:
        issue_location_cb.set("Momo take:")
    
    issue_location_cb.pack(pady = 10)


    # Creates a label above the description box 
    if language == "English":
        issue_description_label = tk.Label(report_window, text = "Please describe the issue", font = ("Arial", 10))
    else:
        issue_description_label = tk.Label(report_window, text = "Whakaahuahia te take", font = ("Arial", 10))
    
    issue_description_label.pack(pady = 10)


    # Creates a box that users can type into to go into more detail about the issue they are reporting
    issue_description = tk.Text(report_window, font = ("Arial", 10), width = 60, height = 5)
    issue_description.pack(pady = 1)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Priority assigning

    # Creates a questionmark button to explain the priority system
    priority_help = tk.Button(report_window, text = "?", font = ("Arial", 10), width = 2, command = priority_msg)
    priority_help.place(x = 330, y = 328)

    # Creates a title so the user knows what to do
    if language == "English":
        priority_assignment_label = tk.Label(report_window, text = "Please assign a priority to the task", font = ("Arial", 10))
    else:
        priority_assignment_label = tk.Label(report_window, text = "Whakaritea he kaupapa matua mo te mahi", font = ("Arial", 10))
    
    priority_assignment_label.pack(pady = 9)

    # Makes a dropdown menu
    priority_cb = ttk.Combobox(report_window, values = issue_priority)
    if language == "English":
        priority_cb.set("Select Priority:")
    else:
        priority_cb.set("Whakaarotau take:")
    
    priority_cb.pack(pady = 10)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Save & Close

    # Submits the issue to be displayed on the dashboard.
    if language == "English":
        save_issue = tk.Button(report_window, text = "Submit", font = ("Arial", 10), command = issue_submit)
    else:
        save_issue = tk.Button(report_window, text = "Tuku", font = ("Arial", 10), command = issue_submit)

    save_issue.pack(pady = 10)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# This is the first window to be opened, launching when the app starts. 
def home():
    global root_window
    # Establishes the framework
    root_window = tk.Tk()

    nav_controller.current_page = root_window

    # Sets the size of the window
    root_window.geometry("500x500+700+200")
    
    # Gives the window a title
    if language == "English":
        root_window.title("IT and Building Management - Nayland College")
    else:
        root_window.title("Hangarau pārongo me te Whakahaere Whare Te Kāreti o Neirana")
    
    # Makes the window non-resizable
    root_window.resizable(False, False) 

    # Creating the heading
    # root_window assigns it to the correct window, text sets the text that it shows, and font sets the font and size.   
    if language == "English":        
        root_heading = tk.Label(root_window, text = "Nayland College Building and IT Reports", font = ("Arial", 17))
    else:
        root_heading = tk.Label(root_window, text = "Te Kāreti o Neirana\npūrongo whare me te hangarau", font = ("Arial", 17))

    # packs everything so it knows to run. pady spaces the text out from the other components
    root_heading.pack(pady = 20)

    # Creating the buttons and their Māori translations. Command calls the dashboard function when the button is clicked
    if language == "English":
        dashboard_button = tk.Button(root_window, text = "Current Issues", command = dashboard)
    else:
        dashboard_button = tk.Button(root_window, text = "Nga Take o Naianei", command = dashboard)

    dashboard_button.pack(pady = 10)

    if language == "English":
        issue_button = tk.Button(root_window, text = "Report an issue", command = report)
    else:
        issue_button = tk.Button(root_window, text = "Pūrongo he take", command = report)

    issue_button.pack(pady = 10)

    if language == "English":
        language_button = tk.Button(root_window, text = "English/Māori", command = language_switch)
    else:    
        language_button = tk.Button(root_window, text = "Ingarihi/Māori", command = language_switch)

    language_button.pack(pady = 10)

    if language == "English":
        close_button = tk.Button(root_window, text = "Close", command = close)
    else:    
        close_button = tk.Button(root_window, text = "Whakaweto", command = close)

    close_button.pack(pady = 10)

    root_window.mainloop()  

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Command to switch the language
def language_switch():
    # Makes language globally accessable so it can be used in this function
    global language
    
    # If the language is English, switches it to Māori
    if language == "English":
        language = "Māori"
    
    # If the language is Māori, switches it to english
    else:
        language = "English"
        
    # Closes and opens the window so it can update
    root_window.destroy()
    home()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Command to close the application
def close():
    root_window.destroy()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Runs the first window when the application starts
home()