import requests
import telebot
from telebot import types
import dotenv 
import os
from data_base import *
import threading



dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


# Telegram notification
def telegram_send_message(message):
    w = 'https://api.telegram.org/bot5875292982:AAGEHSR1NqmA04OWt_vp2vTIPGUSJ4W9Luw/sendmessage?chat_id=305034927&text='
    #message = 'hellow'

    Dict_data = {"UrlBox" : w+message , 
                "AgentList" : "Mozilla+Firefox" ,
                "VersionsList" : "VersionsList" ,
                "MethodList" : "POST"}

    send = requests.post("https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx" , data=Dict_data)
    if send.status_code == 200:
        print('message send to telegram bot')
    else:
        print('message fail to send')   


def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("open_and_close_pos")
    item2 = types.KeyboardButton("change_riskfree_level")
    item3 = types.KeyboardButton("margin_and_money")
    item4 = types.KeyboardButton("program_monitoring")
    item5 = types.KeyboardButton("exit")
    markup.add(item1, item2, item3, item4, item5)
    return markup


class telegram_bot:
    def __init__(self):
        pass
        
        
    def run_bot(self):
        print('Polling . . .')
        bot.infinity_polling()     
        
        
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Bot start.")


    @bot.message_handler(commands=['stop'])
    def stop_bot_polling(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("y")
        item2 = types.KeyboardButton("n")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "If you stop polling you should start it again from server.\n"
                     "Do you want to stop polling? (y/n)", reply_markup=markup)
        # Define a function to handle the user input for "close_pos"
        def process_close_pos(message):
            try:
                if message.text.lower() == 'y':
                    bot.stop_polling()
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(message.chat.id, "Polling stop.", reply_markup=markup)
                    print('Polling stop . . .')
                elif message.text.lower() == 'n':
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(message.chat.id, "Polling continue.", reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(message.chat.id, "Invalid input.", reply_markup=markup)
            except Exception as e:
                # Handle any errors that may occur during input processing
                print(f"Error processing input: {e}")
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
        bot.register_next_step_handler(message, process_close_pos)
        

    # Main menu keyboard
    @bot.message_handler(commands=['input'])
    def inputs_menu(message):
        markup = markup = create_main_menu_markup()
        bot.send_message(message.chat.id, "Choose one of the inputs menue.", reply_markup=markup)


    # Handle each item of main menu 
    @bot.message_handler(
    func=lambda m: m.text in [
        "open_and_close_pos",
        "change_riskfree_level",
        "margin_and_money",
        "program_monitoring"
    ],
    chat_types=['private'])
    def handle_inputs_menu(message):
        if message.text == "open_and_close_pos":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("open_fixprice_pos")
            item2 = types.KeyboardButton("open_volume_pos")
            item3 = types.KeyboardButton("close_pos")
            item4 = types.KeyboardButton("back")
            
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, "Choose one of the input options or press back to return main menu.", reply_markup=markup)

        elif message.text == "change_riskfree_level":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("change_riskfree")
            item2 = types.KeyboardButton("auto_change_riskfree")
            item3 = types.KeyboardButton("stop_auto_change_riskfree_by_id")
            item4 = types.KeyboardButton("stop_auto_change_riskfree_by_ticket")
            item5 = types.KeyboardButton("back")
            
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, "Choose one of the input options or press back to return main menu.", reply_markup=markup)

        elif message.text == "margin_and_money":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("min_margin_level")
            item2 = types.KeyboardButton("max_margin")
            item3 = types.KeyboardButton("max_money_involved")
            item4 = types.KeyboardButton("pos_sum_loss")
            item5 = types.KeyboardButton("back")
            
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, "Choose one of the input options or press back to return main menu.", reply_markup=markup)

        elif message.text == "program_monitoring":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("show_tasks")
            item2 = types.KeyboardButton("Turn_on_pos_logs")
            item3 = types.KeyboardButton("Turn_off_pos_logs")
            item4 = types.KeyboardButton("stop_program")
            item5 = types.KeyboardButton("back")
            
            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, "Choose one of the input options or press back to return main menu.", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "You enterd invalid input menu.", reply_markup=markup)


    # Handle all inputs
    @bot.message_handler(
    func=lambda m: m.text in [
        "open_fixprice_pos",
        "open_volume_pos",
        "close_pos",
        "change_riskfree",
        "auto_change_riskfree",
        "stop_auto_change_riskfree_by_id",
        "stop_auto_change_riskfree_by_ticket",
        "min_margin_level",
        "max_margin",
        "max_money_involved",
        "pos_sum_loss",
        "show_tasks",
        "Turn_on_pos_logs",
        "Turn_off_pos_logs",
        "stop_program",
        "back",
        "exit"
    ],
    chat_types=['private'])
    def handle_inputs(message):

        if message.text == "open_fixprice_pos":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter symbol, main trend, fix price, pip part, zone, riskfree wait, magic number"
                            " separated by ',' or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "open_fixprice_pos"
            def process_open_fixprice_pos_input(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        # Extract user input and split it into individual components
                        input_values = message.text.split(',')

                        # Validate the number of input values
                        if len(input_values) != 7:
                            raise ValueError("Invalid number of input values")
                        
                        # You can also save these values to a database or perform any other desired action
                        database().save_user_input("open_fixprice_pos", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_open_fixprice_pos_input)

        elif message.text == "open_volume_pos":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter symbol, main trend, volume, pip part, zone, riskfree wait, magic number" 
                             " separated by ',' or press back to return main menu."
                             , reply_markup=markup)
            # Define a function to handle the user input for "open_volume_pos"
            def process_open_volume_pos_input(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        # Extract user input and split it into individual components
                        input_values = message.text.split(',')

                        # Validate the number of input values
                        if len(input_values) != 7:
                            raise ValueError("Invalid number of input values")
                        
                        # You can also save these values to a database or perform any other desired action
                        database().save_user_input("open_volume_pos", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_open_volume_pos_input)

        elif message.text == "close_pos":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter position ticket to close or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "close_pos"
            def process_close_pos(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        database().save_user_input("close_pos", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_close_pos)

        elif message.text == "change_riskfree":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter ticket and new risk free level separated by ',' or press back to return main menu."
                            , reply_markup=markup)
            # Define a function to handle the user input for "change_riskfree"
            def process_change_riskfree(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        # Extract user input and split it into individual components
                        input_values = message.text.split(',')

                        # Validate the number of input values
                        if len(input_values) != 2:
                            raise ValueError("Invalid number of input values")
                        
                        # You can also save these values to a database or perform any other desired action
                        database().save_user_input("change_riskfree", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_change_riskfree)

        elif message.text == "auto_change_riskfree":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter ticket, type of auto change (price / profit), amount of (price / profit)"
            " and new riskfree level (price / profit) separated by ',' or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "change_riskfree"
            def process_change_riskfree(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        # Extract user input and split it into individual components
                        input_values = message.text.split(',')

                        # Validate the number of input values
                        if len(input_values) != 4:
                            raise ValueError("Invalid number of input values")
                        
                        # You can also save these values to a database or perform any other desired action
                        database().save_user_input("auto_change_riskfree", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_change_riskfree)

        elif message.text == "stop_auto_change_riskfree_by_id":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter auto_change_riskfree id to stop or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "stop_auto_change_riskfree_by_id"
            def process_stop_auto_change_riskfree_by_id(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        database().save_user_input("stop_auto_change_riskfree_by_id", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_stop_auto_change_riskfree_by_id)

        elif message.text == "stop_auto_change_riskfree_by_ticket":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter position ticket to stop any related auto_change_riskfree or press back to return main menu."
                            , reply_markup=markup)
            # Define a function to handle the user input for "stop_auto_change_riskfree_by_ticket"
            def process_stop_auto_change_riskfree_by_ticket(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        database().save_user_input("stop_auto_change_riskfree_by_ticket", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_stop_auto_change_riskfree_by_ticket)

        elif message.text == "min_margin_level":
            database().save_user_input("min_margin_level", "telegram")
            markup = create_main_menu_markup()
            bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
        
        elif message.text == "max_margin":
            database().save_user_input("max_margin", "telegram")
            markup = create_main_menu_markup()
            bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
        
        elif message.text == "max_money_involved":
            database().save_user_input("max_money_involved", "telegram")
            markup = create_main_menu_markup()
            bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)

        elif message.text == "pos_sum_loss":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter position ticket to show related sum loss or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "pos_sum_loss"
            def process_pos_sum_loss(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        database().save_user_input("pos_sum_loss", f'{message.text}, telegram')
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_pos_sum_loss)

        elif message.text == "show_tasks":
            database().save_user_input("show_tasks", "telegram")
            markup = create_main_menu_markup()
            bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)

        elif message.text == "Turn_on_pos_logs":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter position ticket to turn it logs on or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "Turn_on_pos_logs"
            def process_Turn_on_pos_logs(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        database().save_user_input("Turn_on_pos_logs", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_Turn_on_pos_logs)
        
        elif message.text == "Turn_off_pos_logs":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            item1 = types.KeyboardButton("back")
            markup.add(item1)
            bot.send_message(message.chat.id, "Enter position ticket to turn it logs off or press back to return main menu.", reply_markup=markup)
            # Define a function to handle the user input for "Turn_off_pos_logs"
            def process_Turn_off_pos_logs(message):
                if message.text == 'back':
                    markup = create_main_menu_markup()
                    bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)
                else:
                    try:
                        database().save_user_input("Turn_off_pos_logs", message.text)
                        bot.send_message(message.chat.id, "User input successfully processed!")
                        
                    except Exception as e:
                        # Handle any errors that may occur during input processing
                        print(f"Error processing input: {e}")
                        markup = types.ReplyKeyboardRemove(selective=False)
                        bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_Turn_off_pos_logs)

        elif message.text == "stop_program":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("y")
            item2 = types.KeyboardButton("n")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "Do you want to stop program? (y/n)", reply_markup=markup)
            
            # Define a function to handle the user input for "stop_program"
            def process_stop_program(message):
                try:
                    if message.text.lower() == "y":
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                        item1 = types.KeyboardButton("y")
                        item2 = types.KeyboardButton("n")
                        markup.add(item1, item2)
                        bot.send_message(message.chat.id, "Do you want to close all positions? (y/n)", reply_markup=markup)

                        # Define a function to handle the user input for "close all pos"
                        def process_close_all_pos(message):
                            close_confermation = message.text.lower()
                            if close_confermation != "y" and close_confermation != "n":
                                markup = create_main_menu_markup()
                                bot.send_message(message.chat.id, "Invalid input, the program continues to wor. You back to main menu.", reply_markup=markup)
                            else:
                                markup = types.ReplyKeyboardRemove(selective=False)
                                database().save_user_input("stop_program", close_confermation)
                                bot.send_message(message.chat.id, "User input successfully processed!", reply_markup=markup)
                            
                        bot.register_next_step_handler(message, process_close_all_pos)

                    elif message.text.lower() == "n":
                        markup = create_main_menu_markup()
                        bot.send_message(message.chat.id, "The program continues to work. You back to main menu", reply_markup=markup)

                    else:
                        markup = create_main_menu_markup()
                        bot.send_message(message.chat.id, "Invalid input, the program continues to work. You back to main menu", reply_markup=markup)

                except Exception as e:
                    # Handle any errors that may occur during input processing
                    print(f"Error processing input: {e}")
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(message.chat.id, f"Error processing input: {e}. Please try again.", reply_markup=markup)
                    
            bot.register_next_step_handler(message, process_stop_program)

        elif message.text == "back":
            markup = create_main_menu_markup()
            bot.send_message(message.chat.id, "You back to main menu.", reply_markup=markup)

        elif message.text == "exit":
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "You exit the menu. For open again  the menu use /input command", reply_markup=markup)

        else:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "You enterd invalid input type.", reply_markup=markup)
            







