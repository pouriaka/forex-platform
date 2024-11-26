from . import *


class Tab:
    def __init__(self, technicaltools_frame):
        self.technicaltools_frame = technicaltools_frame
        self.double_click_flag = False  # Initialize the flag
        self.tab_number = 0
        self.tabs = []
        self.tab_remove_flag = False
        self.tab_remove_button_flag = False
        self.numbertab_for_remove = []
        self.selectedtab_for_remove = []


    def open_new_tab(self, event, widget):  
        self.double_click_flag = True  # Set the flag for double-click
        # Create frames for tab pages
        new_tab = ttk.Frame(self.technicaltools_frame, width=1230, height=820)

        # Add frames to the notebook of technicaltools_frame
        self.technicaltools_frame.add(new_tab, text=widget.get())

        self.close_button = tk.Label(new_tab, text='X', padx=5, pady=2, bg='white', fg='black')
        self.close_button.place(x=1210, y=0)
        self.close_button.bind("<Button-1>", self.close_tab)
        self.close_button.bind("<Enter>", self.highlight_button)
        self.close_button.bind("<Leave>", self.unhighlight_button)

        self.tab_data = {"tab":new_tab,
                    "tabnumber":self.tab_number,
                    "xlocator":0,
                    "ylocator":0,
                    "button_number":0,
                    "number_in_row":0,
                    "closebutton":self.close_button}

        self.tabs.append(self.tab_data)
        self.tab_number += 1


    # The function for close tab button work
    def close_tab(self, event):
        selected_tab = self.technicaltools_frame.select()
        selected_tab_index = self.technicaltools_frame.index(selected_tab)
        self.tab_remove_flag = True
        self.tab_remove_button_flag = True
        self.numbertab_for_remove.append(selected_tab_index)
        print("remove--------------------", self.numbertab_for_remove, type(self.numbertab_for_remove))


    def updat_tab_remove_parameter(self):
        self.tab_remove_button_flag = False
        self.numbertab_for_remove = []


    def highlight_button(self, event):
        selected_tab = self.technicaltools_frame.select()
        selected_tab_index = self.technicaltools_frame.index(selected_tab)
        for tab in self.tabs:
            if tab["tabnumber"] == selected_tab_index:
                tab["closebutton"].config(bg='red', fg='white')


    def unhighlight_button(self, event):
        try:
            selected_tab = self.technicaltools_frame.select()
            selected_tab_index = self.technicaltools_frame.index(selected_tab)
            for tab in self.tabs:
                if tab["tabnumber"] == selected_tab_index:
                    tab["closebutton"].config(bg='white', fg='black')
        except:
            pass

    
    def tab_update(self):
        if self.tab_remove_flag:
            new_number_list = []

            # Identify the tabs to be removed
            tabs_to_remove = []
            for number in self.numbertab_for_remove:
                for tab in self.tabs:
                    if tab["tabnumber"] == number:
                        tabs_to_remove.append(tab)

            # Update tab numbers and remove tabs
            for tab in tabs_to_remove:
                self.tab_number -= 1
                self.tabs.remove(tab)
                self.technicaltools_frame.forget(tab["tabnumber"])

            # Update tab numbers for the remaining tabs
            for i, tab in enumerate(self.tabs):
                tab["tabnumber"] = i
                new_number_list.append(i)

            # Rebind events for remaining tabs
            for tab in self.tabs:
                tab["closebutton"].unbind("<Button-1>")
                tab["closebutton"].unbind("<Enter>")
                tab["closebutton"].unbind("<Leave>")
                tab["closebutton"].bind("<Button-1>", self.close_tab)
                tab["closebutton"].bind("<Enter>", self.highlight_button)
                tab["closebutton"].bind("<Leave>", self.unhighlight_button)

            # Print the final button list to check if it has any bugs
            print("final list --------------", self.tabs)

            # After going through the deletion process, update the flag and remove list
            self.tab_remove_flag = False

        

