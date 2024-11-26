from . import *


class Rsi:
    def __init__(self):
        self.colors_list = creat_redtogreen_hexcolorlist()
        self.standard_timeframe = creat_standard_timeframelist()
        self.period = 14
        self.timeframe = '1m'
        self.rsi_remove_flag = False
        self.numberbuttons_for_remove = []
        

    def take_buttons_list(self, buttons_list):  
        self.buttons_list = buttons_list  


    def rsi_button(self, button_data, button_number):
        
        self.button_data = button_data
        self.button_number_click  = button_number 

        # Open rsi option 
        top = Toplevel()
        top.title('RSI option')
        self.rsi_period_label = Label(top, text="Period:")
        self.rsi_period_label.grid(row=0, column=0)
        
        self.rsi_period_entery = Entry(top, font=("Helvetica", 14), width=25)
        self.rsi_period_entery.grid(row=0, column=1)

        # Create a ComboBox variable
        self.combobox_var = StringVar()
        
        self.timeframe_combobox = ttk.Combobox(top, width=40, textvariable=self.combobox_var)
        self.timeframe_combobox['values'] = self.standard_timeframe
        self.timeframe_combobox.grid(row=4, column=1)

        # Bind the function to the ComboBox's text variable
        self.combobox_var.trace("w", self.filtertimeframe_combobox)

        self.timeframe_combobox.current(0)
        self.timeframe_combobox.bind("<<ComboboxSelected>>", lambda event: self.indicator_combobox_click(event))


        self.rsi_timeframe_label = Label(top, text="Time frame:")
        self.rsi_timeframe_label.grid(row=1, column=0)
        
        self.rsi_timeframe_entery = Entry(top, font=("Helvetica", 14), width=25)
        self.rsi_timeframe_entery.grid(row=1, column=1)

        self.rsi_remove_button = Button(top, text="Remove button", command=self.remove_button, width=25)
        self.rsi_remove_button.grid(row=2, column=1)

        self.rsi_ok_button = Button(top, text="OK", command=self.rsi_option_ok)
        self.rsi_ok_button.grid(row=3, column=1)


    def rsi_option_ok(self):
        self.button_data["period"] = int(self.rsi_period_entery.get())
        self.button_data["timeframe"] = self.rsi_timeframe_entery.get()


    def rsi_update_button(self, button_data):
        
        self.button_data = button_data
        data = datamine(self.button_data["timeframe"], self.button_data["paircurrency"], 'online', number_data=self.button_data["period"] + 5)
        data = data.df()
        # Reversed list if we need
        reversed_colors_list = self.colors_list[::-1] 

        # Calculate RSI
        rsi_calculate = indicator.rsi(data, self.button_data["period"])
        rsi_value = rsi_calculate[f'ind_rsi{self.button_data["period"]}'].iloc[-1]
        # Simplify to two decimal places
        rsi_value = round(rsi_value, 2)

        # Button text update
        constant_text = self.button_data["text"]
        new_text = f'{constant_text}\nRSI_value: {rsi_value}\nRSI_period:{self.button_data["period"]}'  # Add the new text on the next line
        
        # Update the RSI button's text
        self.button_data["button"].config(text=new_text)

        # Update the RSI button's color
        if rsi_value > 30 and rsi_value < 70:
            color_number = int(rsi_value - 30) // 2 
            self.button_data["button"].config(bg=reversed_colors_list[color_number])
        
        elif rsi_value < 30:
            # Full red when rsi is lower than 30
            self.button_data["button"].config(bg=reversed_colors_list[0])

        else:
            # Full green when rsi is higher than 70
            self.button_data["button"].config(bg=reversed_colors_list[-1])


        return self.button_data


    def remove_button(self):
        # In this method we just make a flag and return the number of button that we want to delet
        self.rsi_remove_flag = True
        self.numberbuttons_for_remove.append(self.button_number_click)
        print("--------------------",self.numberbuttons_for_remove,type(self.numberbuttons_for_remove))


    def updat_button_remove_parameters(self):
        self.rsi_remove_flag = False
        self.numberbuttons_for_remove = []

    
    def filtertimeframe_combobox(self, *args):
        # Get the typed text from the entry widget
        typed_text = self.combobox_var.get()

        # Create an empty list to store filtered options
        filtered_options = []

        # Loop through each option in all_options
        for option in self.standard_timeframe:
            # Convert both the typed text and the option to lowercase for case-insensitive comparison
            if typed_text.lower() in option.lower():
                filtered_options.append(option)

        # Update the ComboBox dropdown list
        self.timeframe_combobox['values'] = filtered_options


class Macd:
    def __init__(self):
        pass
    
    def macd_button(self):
        pass
