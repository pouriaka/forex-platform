import tkinter as tk
from tkinter import *
from tkinter import ttk

from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *
from Plot import *

from GUI_Technical_tools_functions.Indicators import *
from GUI_Technical_tools_functions.tab_methods import *


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Pitokei technical dashboard")
        tk.Tk.iconbitmap(self, default="icon.ico")
        
        ## Setting up Initial Things
        self.geometry("720x550")
        self.resizable(True, True)
        #self.iconphoto(False, tk.PhotoImage(file="assets/title_icon.png"))
    
        ## Creating a container
        container = tk.Frame(self, bg="#8AA7A9")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ## Initialize Frames
        self.frames = {}
        self.HomePage = HomePage
        self.Technical_dashboard = Technical_dashboard
        
        ## Defining Frames and Packing it
        for F in {HomePage, Technical_dashboard}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")    
           
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        menubar = frame.create_menubar(self)
        self.configure(menu=menubar)
        frame.tkraise()                         ## This line will put the frame on front
 


#---------------------------------------- HOME PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, container)

        label = tk.Label(self, text="Home Page", font=('Times', '20'))
        label.pack(pady=0,padx=0)

        ## ADD CODE HERE TO DESIGN THIS PAGE

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Technical_dashboard))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)  

        ## proccessing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Technical dashboard", menu=processing_menu)
        processing_menu.add_command(label="Technical dashboard")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")
        help_menu.add_separator()

        return menubar


#---------------------------------------- Technical dashboard PAGE FRAME / CONTAINER ------------------------------------------------------------------------
 

class Technical_dashboard(tk.Frame, Tab, Rsi, Macd):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, container)
        Rsi.__init__(self)
        Macd.__init__(self)
        
        self.app_notebook = ttk.Notebook(self)
        self.app_notebook.grid(row=0, column=0)

        # Create the constant frame
        self.constant_frame = ttk.Notebook(self.app_notebook)
        self.app_notebook.add(self.constant_frame)
        self.constant_frame.grid(row=0, column=0)

        # Create the technical tools frame frame
        self.technicaltools_frame = ttk.Notebook(self.app_notebook)
        self.app_notebook.add(self.technicaltools_frame)
        self.technicaltools_frame.grid(row=0, column=1)
        # We should init tab here because now we define self.technicaltools_frame
        Tab.__init__(self, self.technicaltools_frame)

        # Your existing code for the constant panel
        self.currencysearch_lable = tk.Label(self.constant_frame, text="Currency pairs", font=("Helvetica", 14), fg="black")
        self.currencysearch_lable.grid(row=0, column=0)

        self.currencysearch_entery = tk.Entry(self.constant_frame, font=("Helvetica", 14), width=20, borderwidth=15)
        # First fill of entrybox
        self.currencysearch_entery.insert(0, "Enter a currency pair ...")
        # Delete all in the entrybox by click on it 
        self.currencysearch_entery.bind("<Button-1>", lambda event: self.clear(event, self.currencysearch_entery))
        self.currencysearch_entery.bind("<Button-3>", lambda event: self.clear(event, self.currencysearch_entery))
        self.currencysearch_entery.grid(row=1, column=0)

        self.currencysearch_list = tk.Listbox(self.constant_frame, width=40, borderwidth=5)
        self.currencysearch_list.grid(row=2, column=0)

        self.currency_pairs_list = ["EURUSD", "USDCHF", "USDJPY"]

        # Add currency to our listbox
        self.update(self.currencysearch_list, self.currency_pairs_list)

        # When click on an item in the list box, fillout function occurs
        self.currencysearch_list.bind("<<ListboxSelect>>", lambda event: self.fillout(event, self.currencysearch_entery, self.currencysearch_list))
        self.currencysearch_list.bind("<Double-Button-1>", lambda event: self.open_new_tab(event, self.currencysearch_entery))

        # Create a binding on the entry box
        self.currencysearch_entery.bind("<KeyRelease>", lambda event: self.check(event, self.currencysearch_entery, self.currency_pairs_list))

        self.technical_tool_x = 0
        self.technical_tool_y = 0
        self.number_in_row = 0

        self.technicaltool_buttons_list = []
        self.technicaltool_buttons = []
        self.button_number = 0

        # Create a ComboBox variable
        self.combobox_var = StringVar()

        self.indicators_list = [
            "RSI (Relative Strength Index)",
            "MACD (Moving Average Convergence/Divergence)",
            "ATR (Average True Range)"
        ]

        self.indicator_combobox = ttk.Combobox(self.constant_frame, width=40, textvariable=self.combobox_var)
        
        self.indicator_combobox['values'] = self.indicators_list
        
        self.indicator_combobox.grid(row=3, column=0)
        
        # Bind the function to the ComboBox's text variable
        self.combobox_var.trace("w", self.filter_combobox)

        self.indicator_combobox.current(0)
        self.indicator_combobox.bind("<<ComboboxSelected>>", lambda event: self.indicator_combobox_click(event))

        # For prevent clutter
        self.blank_list = Listbox(self.constant_frame, width=40, height=35)
        self.blank_list.grid(row=4, column=0)

        # Schedule the initial call to buttons_updat and set the update interval
        self.update_interval = 500  # 1000 milliseconds = 1 second
        self.schedule_app_update()
        
        
        ## ADD CODE HERE TO DESIGN THIS PAGE


    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Technical_dashboard))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)  

        ## proccessing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Technical dashboard", menu=processing_menu)
        processing_menu.add_command(label="Technical dashboard")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")
        help_menu.add_separator()

        return menubar
    

    def update(self, widget, input_list):
        self.currencysearch_list.delete(0, END)
        for item in input_list:
            self.currencysearch_list.insert(END, item)


    # Update entry box with listbox clicked
    def fillout(self, event, widget, list_box):
        if not self.double_click_flag:
            # Delete whatever in the entry box
            widget.delete(0, END)

            # Add clicked list item to entry box
            widget.insert(0, list_box.get(ACTIVE))

        self.double_click_flag = False  # Reset the flag
        

    def clear(self, event, widget):
        # Delete whatever in the entry box
        widget.delete(0, END)


    # Check entery vs list box
    def check(self, event, widget, list_box):
        # Grab what was typed 
        typed = widget.get()
        
        if typed == "" :
            data = list_box
        else:
            data = []
            for item in list_box:
                if typed.lower() in item.lower():
                    data.append(item)    

        # Update our list with search items
        
        if widget == self.currencysearch_entery:
            self.currencysearch_list.delete(0, END)
            for item in data:
                self.currencysearch_list.insert(END, item)
        

    def filter_combobox(self, *args):
        # Get the typed text from the entry widget
        typed_text = self.combobox_var.get()

        # Create an empty list to store filtered options
        filtered_options = []

        # Loop through each option in all_options
        for option in self.indicators_list:
            # Convert both the typed text and the option to lowercase for case-insensitive comparison
            if typed_text.lower() in option.lower():
                filtered_options.append(option)

        # Update the ComboBox dropdown list
        self.indicator_combobox['values'] = filtered_options


    # this is a method for removing the ()
    @staticmethod
    def remove_inside_parentheses(input_string):
        # Find the index of the opening parenthesis
        index = input_string.find('(')
        
        # Extract the initial part of the string
        if index != -1:
            result = input_string[:index].strip()  # Remove leading/trailing spaces
        else:
            result = input_string  # No opening parenthesis found
        
        return result


    # This method find the first number in a string
    @staticmethod
    def first_number_of_string(input_string):
        # Use a regular expression to find the first number
        match = re.search(r'\d+', input_string)

        if match:
            first_number = match.group()
            return first_number
        else:
            print("No numbers found in the string.")
            pass


    def indicator_combobox_click(self, event): 
        #try:
            selected_indicator = self.indicator_combobox.get()
            selected_tab_index = self.technicaltools_frame.index("current")  # Get the index of the currently selected tab
            
            if selected_tab_index != -1:
                selected_tab = self.technicaltools_frame.tabs()[selected_tab_index]
                selected_tab_name = self.technicaltools_frame.tab(selected_tab, "text")
                
                # Remove extra in side ()
                selected_indicator = self.remove_inside_parentheses(selected_indicator)

                if self.indicator_combobox.get() == "RSI (Relative Strength Index)" :
                    # Creat new button 
                    new_button = Button(self.technicaltools_frame.nametowidget(selected_tab))   
                    new_button.config(text=f'{self.button_number}\n{selected_indicator}')
                    new_button.config(width=20, height=10, bg='#FFFFFF')

                    # Set the location of the buttons
                    new_button.place(x=self.tabs[selected_tab_index]["xlocator"], y=self.tabs[selected_tab_index]["ylocator"])  

                    button_data = {"button":new_button, 
                    "technicaltool":"RSI",
                    "text": f'button id:{self.button_number}\n'
                            f'button number:{self.tabs[selected_tab_index]["button_number"]}\n'
                            f'{selected_indicator}',
                    "xloc":self.tabs[selected_tab_index]["xlocator"],
                    "yloc":self.tabs[selected_tab_index]["ylocator"],
                    "number_in_row":self.tabs[selected_tab_index]["number_in_row"],
                    "buttonnumber":self.button_number,
                    "button_number_in_tab":self.tabs[selected_tab_index]["button_number"],
                    "paircurrency":selected_tab_name,
                    "timeframe":"1m",
                    "period":14,
                    "tab":selected_tab_index}
                    
                    new_button.config(command=lambda: self.button_click(new_button))
                    
                        
                    self.technicaltool_buttons.append(button_data)
                    
                    print("updat-----------------------------------------------------",self.technicaltool_buttons)
                    
                    #self.rsi_update_button(self.button_number)
                    self.button_number += 1
                
                if self.indicator_combobox.get() == "MACD (Moving Average Convergence/Divergence)" :
                    pass

                self.tabs[selected_tab_index]["xlocator"] += 150
                self.tabs[selected_tab_index]["number_in_row"] += 1
                self.tabs[selected_tab_index]["button_number"] += 1

                if self.tabs[selected_tab_index]["number_in_row"] == 8:
                    self.tabs[selected_tab_index]["ylocator"] += 160
                    self.tabs[selected_tab_index]["xlocator"] = 0
                    self.tabs[selected_tab_index]["number_in_row"] = 0     

        #except Exception as e:
            #print(f"Error in indicator_combobox_click: {str(e)}")
    

    def button_click(self, button):
        button_text = button.cget("text")
        button_number = int(self.first_number_of_string(button_text))
        print("this is butten number-----------------------", button_number)
        button_data = self.technicaltool_buttons[button_number]
        if button_data["technicaltool"] == "RSI":
            self.rsi_button(button_data, button_number)
            print("butten data transfer-----------------")
            print(button_data)


    def schedule_app_update(self):
        # Call functions for update the app 
        self.tab_update()
        self.buttons_update()
        self.after(self.update_interval, self.schedule_app_update)

                        
    def buttons_update(self):
        # Chek if any tab removed, we also remove the corresponding buttons
        if self.tab_remove_button_flag:
            for number in self.numbertab_for_remove:
                for button in self.technicaltool_buttons:
                    if button["tab"] == number:
                        self.technicaltool_buttons.remove(button)

            self.updat_tab_remove_parameter()
            
        # Chek if any button remove
        if self.rsi_remove_flag :

            new_number_list = []
            new_number_in_row = []
            new_number_in_tab = []
            new_button_xloc = []
            new_button_yloc = []
            
            # Find button that should remove
            for number in self.numberbuttons_for_remove:
                for button in self.technicaltool_buttons:    
                    if button["buttonnumber"] == number:
                        
                        # Update the tab parameter after removing button 
                        if self.tabs[button["tab"]]["number_in_row"] == 0:
                            self.tabs[button["tab"]]["xlocator"] += 1050
                            self.tabs[button["tab"]]["ylocator"] -= 160
                            self.tabs[button["tab"]]["number_in_row"] += 7
                            self.tabs[button["tab"]]["button_number"] -= 1
                        else:
                            self.tabs[button["tab"]]["xlocator"] -= 150
                            if self.tabs[button["tab"]]["number_in_row"] > 0:
                                self.tabs[button["tab"]]["number_in_row"] -= 1
                                self.tabs[button["tab"]]["button_number"] -= 1

                        if self.button_number > 0 :
                            self.button_number -= 1
                        
                        # Update the button valus that place after removen button
                        for i in range(0, len(self.technicaltool_buttons)):
                            if self.technicaltool_buttons[i]["buttonnumber"] < number + 1:
                                new_number_list.append(self.technicaltool_buttons[i]["buttonnumber"])
                                new_button_xloc.append(self.technicaltool_buttons[i]["xloc"])
                                new_button_yloc.append(self.technicaltool_buttons[i]["yloc"])
                                new_number_in_row.append(self.technicaltool_buttons[i]["number_in_row"])
                                new_number_in_tab.append(self.technicaltool_buttons[i]["button_number_in_tab"])

                            elif self.technicaltool_buttons[i]["buttonnumber"] >= number + 1 :
                                
                                new_number_list.append(self.technicaltool_buttons[i]["buttonnumber"] - 1)

                                # We only need to update the location of the buttons that were on the same tab as the removed button
                                if self.technicaltool_buttons[i]["tab"] == button["tab"]:
                                    # If the button is the first button in the line we shold move it to the top line
                                    if self.technicaltool_buttons[i]["number_in_row"] == 0:
                                        new_button_xloc.append(self.technicaltool_buttons[i]["xloc"] + 1050)
                                        new_button_yloc.append(self.technicaltool_buttons[i]["yloc"] - 160)
                                        new_number_in_row.append(self.technicaltool_buttons[i]["number_in_row"] + 7)
                                    else:
                                        new_button_xloc.append(self.technicaltool_buttons[i]["xloc"] - 150)
                                        new_button_yloc.append(self.technicaltool_buttons[i]["yloc"])
                                        new_number_in_row.append(self.technicaltool_buttons[i]["number_in_row"] - 1)  

                                    new_number_in_tab.append(self.technicaltool_buttons[i]["button_number_in_tab"] - 1)  

                                else:
                                    new_button_xloc.append(self.technicaltool_buttons[i]["xloc"])
                                    new_button_yloc.append(self.technicaltool_buttons[i]["yloc"])
                                    new_number_in_row.append(self.technicaltool_buttons[i]["number_in_row"])
                                    new_number_in_tab.append(self.technicaltool_buttons[i]["button_number_in_tab"])

                        # Assign new valus to the buttons and configur the new seting
                        for i in range(0, len(self.technicaltool_buttons)):
                            self.technicaltool_buttons[i]["buttonnumber"] = new_number_list[i]
                            self.technicaltool_buttons[i]["button_number_in_tab"] = new_number_in_tab[i]
                            self.technicaltool_buttons[i]["text"] = (
                            f'button id:{new_number_list[i]}\n'
                            f'button number:{new_number_in_tab[i]}\n'
                            f'{button["technicaltool"]}'
                            )
                            self.technicaltool_buttons[i]["xloc"] = new_button_xloc[i]
                            self.technicaltool_buttons[i]["yloc"] = new_button_yloc[i]
                            self.technicaltool_buttons[i]["number_in_row"] = new_number_in_row[i]
                            self.technicaltool_buttons[i]["button"].config(
                            text=f'button id:{new_number_list[i]}\n'
                                f'button number:{new_number_in_tab[i]}\n'
                                f'{button["technicaltool"]}'
                            )
                            self.technicaltool_buttons[i]["button"].place(x=new_button_xloc[i], y=new_button_yloc[i])  
                            
                        # Distroy the button that we want to remove and remove it from the buttons list
                        self.technicaltool_buttons.remove(button)
                        button["button"].destroy()

                        # Print the final button list to check if it has any bug
                        print("final list --------------",self.technicaltool_buttons)

            # After the going through the deletion process we update the flag and remove list
            self.updat_button_remove_parameters()


        # Update the buttons color and data                      
        for button in self.technicaltool_buttons:

            if button["technicaltool"] == "RSI":
                button = self.rsi_update_button(button)

            elif button["technicaltool"] == "MACD":
                pass
   

if __name__ == "__main__":
    app = App()
    app.mainloop()

    ## IF you find this useful >> Claps on Medium >> Stars on Github >> Subscription on youtube will help me
