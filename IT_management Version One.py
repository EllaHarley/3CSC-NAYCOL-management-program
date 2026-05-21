# Nayland College IT and building management program

# Ella Harley - 3CSC - 08/05/2026

# Importing Tkinter, which is the framework for my GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from queue import PriorityQueue

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Data storage

current_issues = []

issue_queue = PriorityQueue()

# ID
issue_number = 1

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def dashboard():
    # Establishes the framework
    dashboard_window = tk.Toplevel()
    # Sets the size of the window
    dashboard_window.geometry("500x500")
    # Gives the window a title
    dashboard_window.title("IT and Building Management - Nayland College")



    dashboard_window.mainloop()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def report():
    # Establishes the framework
    report_window = tk.Toplevel()
    # Sets the size of the window
    report_window.geometry("500x500")
    # Gives the window a title
    report_window.title("IT and Building Management - Nayland College")

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Saves the entered combobox options to a dictionary
    def issue_submit():
        # GLobals the issue number so I can access it in this function
        global issue_number

        # Checking to see if all fields have been filled out for reporting before creating the issue

        # if the combobox hasnt been changed,
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
       

        # Framework for the dictionary, grabs all of the data so I can access it later
        issue = {"id" : issue_number,
                 "type" : issue_type_cb.get(),
                 "location" : issue_location_cb.get(),
                 "desc" : issue_description,
                 "priority" : int(priority_cb.get()),
                 "status" : "incomplete"
        }

        # Appends the issue dictionary to the current issues list
        current_issues.append(issue)

        # Puts the issue into the priority queue
        issue_queue.put((issue["priority"], issue))

        # Increments the issue number by one so more can be stored
        issue_number += 1

        # Messagebox to show a completed issue submission
        messagebox.showinfo("Success!", "Issue submitted successfully!")

        # Destroys the report window
        report_window.destroy()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Creates the priority messagebox to explain the priority system
    def priority_msg():
        messagebox.showinfo("Priority Help", "The numbered priority system is a way for us to catalog how urgent the issues are. Please be honest with your selection\n" \
        "\n1 = Lowest Priority, will be fixed within 1-2 weeks.\n2 = Medium Priority, will be fixed within 1-2 days\n3 = Highest Priority, Will be fixed within a few hours to 1 day")
                            

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Defining issue types

    # The different types of issue there could be, plus an other that can be changed
    issue_types = ["a", "b", "c", "d", "Other: Please Specify"]

    # The different locations of the incident
    issue_locations = ["a", "b", "c", "d", "Other: Please Specify"]

    # The different priority levels of tasks
    issue_priority = ["1", "2", "3"]

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Framework

    # Title of the window
    report_title = tk.Label(report_window, text = "Issue Report", font = ("Arial", 17))
    report_title.pack(pady = 20)


    # Makes a back arrow character to be used for the back button
    back_arrow = "\u2190"
    # Creates a back button to go back to the preivous window
    back_button_report = tk.Button(report_window, text = f"{back_arrow}", font = ("Wingdings 3", 10))
    # Places the button in a specific location on the screen - It is placed in a spot that most websies generally have a back button (top left corner)
    back_button_report.place(x = 15, y = 10)


    # Creates a drop down meny that holds all of the different types of issues, detailed in the "issue types" list above
    issue_type_cb = ttk.Combobox(report_window, values = issue_types)
    # Sets the text of the dropdown menu so it is clear what needs to be changed
    issue_type_cb.set("Select Issue:")
    issue_type_cb.pack(pady = 10)


    # Holds the different locations, as detailed in the "issue locations" list above
    issue_location_cb = ttk.Combobox(report_window, values = issue_locations)
    issue_location_cb.set("Select Location:")
    issue_location_cb.pack(pady = 10)


    # Creates a label above the description box 
    issue_description_label = tk.Label(report_window, text = "Please describe the issue", font = ("Arial", 10))
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
    priority_assignment_label = tk.Label(report_window, text = "Please assign a priority to the task", font = ("Arial", 10))
    priority_assignment_label.pack(pady = 9)

    # Makes a dropdown menu
    priority_cb = ttk.Combobox(report_window, values = issue_priority)
    priority_cb.set("Select Priority:")
    priority_cb.pack(pady = 10)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Save & Close

    # Submits the issue to be displayed on the dashboard.
    save_issue = tk.Button(report_window, text = "Submit", font = ("Arial", 10), command = issue_submit)
    save_issue.pack(pady = 10)

    # Runs the program
    report_window.mainloop()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# This is the first window to be opened, launching when the app starts. 

# Establishes the framework
root_window = tk.Tk()
# Sets the size of the window
root_window.geometry("500x500")
# Gives the window a title
root_window.title("IT and Building Management - Nayland College")

# Creating the heading
# root_window assigns it to the correct window, text sets the text that it shows, and font sets the font and size.           
root_heading = tk.Label(root_window, text = "Nayland College Building and IT Reports", font = ("Arial", 17))
# packs everything so it knows to run. pady spaces the text out from the other components
root_heading.pack(pady = 20)

# Creating the buttons. Command calls the dashboard function when the button is clicked
dashboard_button = tk.Button(root_window, text = "Current Issues", command = dashboard)
dashboard_button.pack(pady = 20)

issue_button = tk.Button(root_window, text = "Report an issue", command = report)
issue_button.pack()

# Tells the code to start the root window
root_window.mainloop()

