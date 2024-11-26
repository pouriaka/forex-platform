from Hedging import *
from datetime import datetime
from Telegram_notif import *
from auto_change_riskfree import *

import re


class concurrent_position_management:
    def __init__(self, login):
        self.login = login
        self.hedging_dict = {}
        self.task_dict = {}
        self.stop_event = threading.Event()
        self.cent = True

        # Temporary set for volume pos to order for news
        self.hedge_time = datetime(2024, 3, 7, 17, 15, 0)


    def take_user_input(self): 
        while not self.stop_event.is_set():
            input_type = input("Enter the input type:\n").lower()
            if input_type == "open_fixprice_pos":
                input_values = input("Enter symbol, main trend, fix price, pip part, zone, riskfree wait, magic number separated by ',':\n")
                symbol, main_trend, fix_price, pip_part, zone, riskfree_wait, magic = input_values.split(',')
                # Make a dictionary from run information
                run_info = {'time': datetime.now(), 
                            'symbol': symbol,
                            'main_trend': main_trend,
                            'fix_price': fix_price, 
                            'pip_part': pip_part,
                            'zone': zone,
                            'riskfree_wait': riskfree_wait,
                            'magic': magic}
                confirmation = input(f"Do you want to open position with this input values? (y/n)\n {run_info}: \n").lower()
                if confirmation == "y":
                    database().save_user_input("open_fixprice_pos", input_values)

            elif input_type == "open_volume_pos":
                input_values = input("Enter symbol, main trend, volume, pip part, zone, riskfree wait, magic number separated by ',':\n")
                symbol, main_trend, volume, pip_part, zone, riskfree_wait, magic = input_values.split(',')
                # Make a dictionary from run information
                run_info = {'time': datetime.now(), 
                            'symbol': symbol,
                            'main_trend': main_trend,
                            'volume': volume, 
                            'pip_part': pip_part,
                            'zone': zone,
                            'riskfree_wait': riskfree_wait,
                            'magic': magic}
                confirmation = input(f"Do you want to open position with this input values? (y/n)\n {run_info}: \n").lower()
                if confirmation == "y":
                    database().save_user_input("open_volume_pos", input_values)

            elif input_type == "close_pos":
                ticket = input("Enter position ticket to close:")
                confirmation = input(f"Do you want to close position with this ticket {ticket}? (y/n):").lower()
                check_pos = self.check_position_exist(ticket)
                if check_pos is False:
                    print(f"There is no position with ticket {ticket} to close.")
                else:
                    if confirmation == "y":
                        database().save_user_input("close_pos", ticket)
                
            elif input_type == "change_riskfree":
                input_values = input("Enter ticket and new risk free level separated by ',':\n")
                ticket, new_riskfree_level = input_values.split(',')
                confirmation = input(f"Do you want to change risk free level of position with ticket {ticket} to {new_riskfree_level}? (y/n): \n").lower()
                if confirmation == "y":
                    database().save_user_input("change_riskfree", input_values)
                    print("Riskfree level changed successfully.")
                elif confirmation == "n":
                    print("Riskfree level didn't change.")
                else:
                    print("Invalid input, riskfree level didn't change.")

            elif input_type == "auto_change_riskfree":
                input_values = input("Enter ticket, type of auto change (price / profit), amount of (price / profit)"
                                     " and new riskfree level (price / profit) separated by ',':\n")
                ticket, type_of_autochange, amount, new_riskfree_level = input_values.split(',')
                confirmation = input(f"Do you want to auto change risk free level of position with ticket {ticket} to {new_riskfree_level} when" 
                                    f"{type_of_autochange} equal to {amount}? (y/n): \n").lower()
                if confirmation == "y":
                    database().save_user_input("auto_change_riskfree", input_values)
                    print("Riskfree level auto changed save successfully.")
                elif confirmation == "n":
                    print("Riskfree level auto change didn't save.")
                else:
                    print("Invalid input, riskfree level auto change didn't save.")

            elif input_type == "stop_auto_change_riskfree_by_id":
                id = input("Enter auto ticket to close.")
                confirmation = input(f"Do you want to stop auto_change_riskfree with this id {id}? (y/n):\n").lower()
                if confirmation == "y":
                    database().save_user_input("stop_auto_change_riskfree_by_id", id)

            elif input_type == "stop_auto_change_riskfree_by_ticket":
                ticket = input("Enter auto ticket to close.")
                confirmation = input(f"Do you want to stop all auto_change_riskfree related to position with ticket {ticket}? (y/n):\n").lower()
                check_pos = self.check_position_exist(ticket)
                if check_pos is False:
                    print(f"There is no position with ticket {ticket} to close.")
                else:
                    if confirmation == "y":
                        database().save_user_input("stop_auto_change_riskfree_by_ticket", ticket)

            elif input_type == "min_margin_level":
                database().save_user_input("min_margin_level", "command")

            elif input_type == "max_margin":
                database().save_user_input("max_margin", "command")

            elif input_type == "max_money_involved":
                database().save_user_input("max_money_involved", "command")

            elif input_type == "show_tasks":
                database().save_user_input("show_tasks", 'command')

            elif input_type == "pos_sum_loss":
                ticket = input('Enter the position ticket:')
                database().save_user_input("pos_sum_loss", f'{ticket}, command')

            elif input_type == "stop_program":
                confirmation = input("Do you want to stop all threads? (y/n): \n").lower()
                if confirmation == "y":
                    close_confirmation = input("Do you want to close all positions? (y/n): \n").lower()
                    database().save_user_input("stop_program", close_confirmation)
                    break
                elif confirmation == "n":
                    print("The program continues to run.")
                else:
                    print("You enterd invalid input, the program continues to run.")

            else:
                print("You enterd invalid input type in the command line.\n")
        
        print("Take User input is finish.\n")    


    def do_user_input(self):
        inputs_table = database().load_table("inputs")
        while not self.stop_event.is_set(): 
            # Take update of inputs table every 1 secound and if it has any item that last update didn't have we do it
            update_inputs_table = database().load_table("inputs") 
            if inputs_table != update_inputs_table:
                new_duty = self.find_items_in_list1_not_in_list2(update_inputs_table, inputs_table)
                if new_duty != []:
                    for duty in new_duty:
                        # try:
                            if duty[1] == 'open_fixprice_pos':
                                # Load two times because openning position take time and we should wait for it to take it ticket
                                main_pos_table = database().load_table("main_trend_positions")
                                update_main_pos_table = database().load_table("main_trend_positions")

                                # Save all the parameters in variabls and run it task
                                symbol, main_trend, fix_price, pip_part, zone, riskfree_wait, magic = duty[2].split(',')
                                new_hedg = auto_hedging(self.login, symbol.strip(), main_trend.strip())
                                new_task = threading.Thread(target=new_hedg.position_management, 
                                args=[int(pip_part), int(zone), self.stop_event], 
                                kwargs={'management_level': 1, 'fix_price': float(fix_price), 'riskfree_wait': int(riskfree_wait),
                                'riskfree_level': None, 'magic': int(magic), 'loss_level': None})
                                new_task.start()

                                # Wait for opening position and add this position to main position data base
                                while main_pos_table == update_main_pos_table:
                                    update_main_pos_table = database().load_table("main_trend_positions")

                                # Take new position that create in database and use the ticket for save the task in task dict
                                new_pos = self.find_items_in_list1_not_in_list2(update_main_pos_table, main_pos_table)
                                new_pos_ticket = int(new_pos[0][0])
                                self.hedging_dict[f"hedg_{new_pos_ticket}"] = new_hedg
                                self.task_dict[f"task_{new_pos_ticket}"] = new_task

                            elif duty[1] == 'open_volume_pos':
                                # Load two times because openning position take time and we should wait for it to take it ticket
                                main_pos_table = database().load_table("main_trend_positions")
                                update_main_pos_table = database().load_table("main_trend_positions")

                                # Save all the parameters in variabls and run it task
                                symbol, main_trend, volume, pip_part, zone, riskfree_wait, magic = duty[2].split(',')
                                new_hedg = auto_hedging(self.login, symbol.strip(), main_trend.strip())
                                new_task = threading.Thread(target=new_hedg.position_management, 
                                args=[int(pip_part), int(zone), self.stop_event], 
                                kwargs={'management_level': 1, 'volume': float(volume), 'riskfree_wait': int(riskfree_wait),
                                'riskfree_level': None, 'magic': int(magic), 'loss_level': None, 'hedge_time': self.hedge_time})
                                new_task.start()

                                # Wait for opening position and add this position to main position data base
                                while main_pos_table == update_main_pos_table:
                                    update_main_pos_table = database().load_table("main_trend_positions")
                                
                                # Take new position that create in database and use the ticket for save the task in task dict
                                new_pos = self.find_items_in_list1_not_in_list2(update_main_pos_table, main_pos_table)
                                new_pos_ticket = int(new_pos[0][0])
                                self.hedging_dict[f"hedg_{new_pos_ticket}"] = new_hedg
                                self.task_dict[f"task_{new_pos_ticket}"] = new_task

                            elif duty[1] == 'close_pos':
                                ticket = int(duty[2])
                                check_pos = self.check_position_exist(ticket)
                                if check_pos:
                                    # Close position by it ticket that save in database
                                    self.login.close_pos(ticket)
                                else:
                                    print(f"Position with ticket {ticket} doesen't exist to close.")

                            elif duty[1] == 'change_riskfree':
                                ticket, new_riskfree_level = duty[2].split(',')
                                ticket = int(ticket)
                                new_riskfree_level = float(new_riskfree_level)
                                change_check = False
                                check_pos = self.check_position_exist(ticket)
                                if check_pos:
                                    # Take the data we need frome the related row in the database
                                    pos = database().load_row("main_trend_positions", int(ticket))
                                    last_riskfree_level = pos[9]
                                    pos_main_trend = pos[2]
                                    main_pos_spread = pos[14]
                                    symbol_info = mt5.symbol_info(pos[1])
                                    now_ask_price = symbol_info.bid
                                    now_bid_price = symbol_info.ask
                                    pip = symbol_info.point
                                    pos_price_spread = pip * (main_pos_spread * 2)  # If main_pos_spread == riskfree_pos_spread

                                    pos_info = mt5.positions_get(ticket=ticket)
                                    pos_info = pos_info[0]
                                    pos_open_price = pos_info.price_open
                                    
                                    # The condition that allow you change risk free level properly
                                    check_riskfree = auto_change_riskfree().check_position_isrikfree(ticket)
                                    if check_riskfree:
                                        if pos_main_trend == "bullish":
                                            if new_riskfree_level < last_riskfree_level:
                                                if now_bid_price < new_riskfree_level:
                                                    database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                                    try:
                                                        database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                                    except:
                                                        pass
                                                    print(f"Risk free level change to {new_riskfree_level}")
                                                    change_check = True
                                                else:
                                                    print("In bullish main trend and in risk free mode you can't move riskfree level to\n"
                                                      "a level less than now bid price so Risk free level desen't change.")
                                            else:
                                                print("In bullish main trend and in risk free mode you can't move riskfree level up.\n"
                                                      "Risk free level desen't change. ")
                                        else:
                                            if new_riskfree_level > last_riskfree_level:
                                                if now_ask_price > new_riskfree_level:
                                                    database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                                    try:
                                                        database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                                    except:
                                                        pass
                                                    print(f"Risk free level change to {new_riskfree_level}")
                                                    change_check = True
                                                else:
                                                    print("In bearish main trend and in risk free mode you can't move riskfree level to\n"
                                                      "a level more than now ask price so Risk free level desen't change.")
                                            else:
                                                print("In bearish main trend and in risk free mode you can't move riskfree level down.\n"
                                                      "Risk free level desen't change. ")
                                    else:
                                        if pos_main_trend == "bullish":
                                            if new_riskfree_level > last_riskfree_level:
                                                if now_bid_price > new_riskfree_level:
                                                    database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                                    try:
                                                        database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                                    except:
                                                        pass
                                                    print(f"Risk free level change to {new_riskfree_level}")
                                                    change_check = True
                                                else:
                                                    print("In bullish main trend and in no risk free mode you can't move riskfree level to\n"
                                                      "a level more than now bid price so Risk free level desen't change. ")
                                            else:
                                                print("In bullish main trend and in no risk free mode you can't move riskfree level down.\n"
                                                      "Risk free level desen't change. ")
                                        else:
                                            if new_riskfree_level < last_riskfree_level:
                                                if now_ask_price < new_riskfree_level:
                                                    database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                                    try:
                                                        database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                                    except:
                                                        pass
                                                    print(f"Risk free level change to {new_riskfree_level}")
                                                    change_check = True
                                                else:
                                                    print("In bearish main trend and in no risk free mode you can't move riskfree level to\n"
                                                      "a level less than now ask price so Risk free level desen't change. ")
                                            else:
                                                print("In bearish main trend and in no risk free mode you can't move riskfree level up.\n"
                                                      "Risk free level desen't change. ")
                                    
                                    # Calculate change money involved if risk free level changed
                                    if change_check:
                                        if pos_main_trend == "bullish":
                                            if new_riskfree_level > last_riskfree_level:
                                                change_riskfree_level = new_riskfree_level - last_riskfree_level
                                                price_dif_from_open = new_riskfree_level - pos_open_price - pos_price_spread 
                                                money_change = calculator().money_calculator(pos[1], pos[5], price_dif=change_riskfree_level)
                                                money_involved = calculator().money_calculator(pos[1], pos[5], price_dif=price_dif_from_open)
                                                database().update_money_involved(ticket, money_involved)
                                                print(f"Change money on equity in risk free mode with {new_riskfree_level} risk free level is {money_change} $.\n")
                                                print(f"Money involved with this new riskfree level is about {money_involved} $.\n")
                                            else:
                                                print("Money involved doesen't change.")
                                        else:
                                            if new_riskfree_level < last_riskfree_level:
                                                change_riskfree_level =  last_riskfree_level - new_riskfree_level
                                                price_dif_from_open = pos_open_price - new_riskfree_level - pos_price_spread
                                                money_change = calculator().money_calculator(pos[1], pos[5], price_dif=change_riskfree_level)
                                                money_involved = calculator().money_calculator(pos[1], pos[5], price_dif=price_dif_from_open)
                                                database().update_money_involved(ticket, money_involved)
                                                print(f"Change money on equity in risk free mode with {new_riskfree_level} risk free level is {money_change} $.\n")
                                                print(f"Money involved with this new riskfree level is about {money_involved} $.\n")
                                            else:
                                                print("Money involved doesen't change.")        
                                else:
                                    print(f"Position with ticket {ticket} doesen't exist.")
                                    telegram_send_message(f"Position with ticket {ticket} doesen't exist.")

                            elif duty[1] == 'auto_change_riskfree':
                                # Save input parameters in variabls
                                ticket, type_of_autochange, amount, new_riskfree_level = duty[2].split(',')
                                ticket = int(ticket)
                                type_of_autochange = str(type_of_autochange).strip()
                                amount = float(amount)
                                new_riskfree_level = float(new_riskfree_level)

                                check_pos = self.check_position_exist(ticket)
                                pos = database().load_row("main_trend_positions", ticket)

                                if check_pos:
                                    # Take the data we need frome the related row in the database
                                    pos = database().load_row("main_trend_positions", ticket)
                                    symbol = pos[1]
                                    last_riskfree_level = pos[9]
                                    pos_main_trend = pos[2]
                                    pos_spread = pos[14]
                                    last_money_involved = pos[13]
                                    symbol_info = mt5.symbol_info(pos[1])
                                    pip = symbol_info.point
                                    pos_spread_price = pip * (pos_spread * 2)  # If consider main_pos_spread = riskfree_pos_spread
                                    number_auto_change_riskfree = pos[15]
                                    number_auto_change_riskfree += 1
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree)

                                    pos_info = mt5.positions_get(ticket=ticket)
                                    pos_info = pos_info[0]
                                    volume = pos_info.volume
                                    price_open = pos_info.price_open

                                    # Change new_riskfree_level profit to new_riskfree_level_price
                                    if type_of_autochange == 'profit':
                                        if pos_main_trend == 'bullish':
                                            price_dif = calculator().dif_calculator(symbol, volume, new_riskfree_level, price_or_pip='price')
                                            new_riskfree_level_price = price_open + price_dif - pos_spread_price
                                        else:
                                            price_dif = calculator().dif_calculator(symbol, volume, new_riskfree_level, price_or_pip='price')
                                            new_riskfree_level_price = price_open - price_dif + pos_spread_price
                                    else:
                                        new_riskfree_level_price = new_riskfree_level

                                    # Calculate new money involved 
                                    if pos_main_trend == "bullish":
                                        if new_riskfree_level_price > last_riskfree_level:
                                            change_riskfree_level = new_riskfree_level_price - last_riskfree_level
                                            price_dif_from_open = new_riskfree_level_price - price_open - pos_spread_price 
                                            money_change = calculator().money_calculator(pos[1], pos[5], price_dif=change_riskfree_level)
                                            new_money_involved = calculator().money_calculator(pos[1], pos[5], price_dif=price_dif_from_open)
                                            print(f"Change money on equity in risk free mode with {new_riskfree_level} new risk free level is {money_change} $.")
                                            print(f"Money involved with {new_riskfree_level} new riskfree level is about {new_money_involved} $.")
                                            database().save_auto_change_riskfree(ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved)
                                            last_row_id = database().load_last_row("auto_change_riskfree_level", "id")[0]
                                        else:
                                            new_money_involved = last_money_involved
                                            print("Money involved doesen't change.")
                                            database().save_auto_change_riskfree(ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved)
                                            last_row_id = database().load_last_row("auto_change_riskfree_level", "id")[0]
                                    else:
                                        if new_riskfree_level_price < last_riskfree_level:
                                            change_riskfree_level =  last_riskfree_level - new_riskfree_level_price
                                            price_dif_from_open = price_open - new_riskfree_level_price - pos_spread_price
                                            money_change = calculator().money_calculator(pos[1], pos[5], price_dif=change_riskfree_level)
                                            new_money_involved = calculator().money_calculator(pos[1], pos[5], price_dif=price_dif_from_open)
                                            print(f"Change money on equity in risk free mode with {new_riskfree_level} new risk free level is {money_change} $.")
                                            print(f"Money involved with {new_riskfree_level} new riskfree level is about {new_money_involved} $.")
                                            database().save_auto_change_riskfree(ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved)
                                            last_row_id = database().load_last_row("auto_change_riskfree_level", "id")[0]
                                        else:
                                            new_money_involved = last_money_involved
                                            print("Money involved doesen't change.")
                                            database().save_auto_change_riskfree(ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved)
                                            last_row_id = database().load_last_row("auto_change_riskfree_level", "id")[0]

                                    # Start auto_change_riskfree_level task 
                                    new_task = threading.Thread(target=auto_change_riskfree().run, 
                                    args=[ticket, type_of_autochange, amount, new_riskfree_level, 
                                    number_auto_change_riskfree, new_money_involved, last_row_id, self.stop_event])
                                    new_task.start()

                                    # Add the auto change riskfree task to our task dictionary
                                    self.task_dict[f"task_{ticket}_auto_change_riskfree_{number_auto_change_riskfree}"] = new_task
                                    if type_of_autochange == 'price':
                                        print(f"Auto change riskfree level activate, if {type_of_autochange} reach {amount}" 
                                            f" riskfree level automatically change to {new_riskfree_level_price}.\n")
                                    else:
                                        print(f"Auto change riskfree level activate, if {type_of_autochange} reach {amount} (profit / loss) \n" 
                                        f"riskfree level automatically change to {new_riskfree_level_price} in {new_riskfree_level} (profit / loss).\n")
                                    
                                else:
                                    print(f"Position with ticket {ticket} doesen't exist.")
                                    telegram_send_message(f"Position with ticket {ticket} doesen't exist.")

                            elif duty[1] == 'stop_auto_change_riskfree_by_id':
                                # The auto_change_riskfree_level function check the achieve in every cycle
                                id = int(duty[2])
                                main_pos_table = database().load_table("main_trend_positions")
                                auto_change_riskfree_table = database().load_table("auto_change_riskfree_level")

                                # Find the position ticket that we set auto change on it
                                for auto_change in auto_change_riskfree_table:
                                    if auto_change[0] == id:
                                        ticket = auto_change[1]
                                        break
                                
                                # Save the position number risk free level in a variable to manage it
                                for pos in main_pos_table:
                                    if pos[0] == ticket:
                                        number_auto_change_riskfree = pos[15]
                                        break

                                database().update_achieve(id, 'stop')
                                database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)

                            elif duty[1] == 'stop_auto_change_riskfree_by_ticket':
                                ticket = int(duty[2])
                                # The auto_change_riskfree_level function check the achieve in every cycle
                                database().update_achieve_by_ticket(ticket, 'stop')
                                database().update_number_auto_change_riskfree(ticket, 0)

                            elif duty[1] == 'min_margin_level':
                                account_info = mt5.account_info()
                                equity = account_info.equity
                                margin = self.calculate_margin_in_full_onhedge()
                                try:
                                    margin_level = (equity / margin) * 100
                                    if duty[2] == 'command':
                                        print(f'minimum margin level for full onriskfree mode is: {margin_level} %')
                                    else:
                                        telegram_send_message(f'minimum margin level for full onriskfree mode is: {margin_level} %')
                                except ZeroDivisionError:
                                    if duty[2] == 'command':
                                        print(f'There is no open position and margin is 0 in full onriskfree mode.')
                                    else:
                                        telegram_send_message(f'There is no open position and margin is 0 in full onriskfree mode.')

                            elif duty[1] == 'max_margin':
                                margin = self.calculate_margin_in_full_onhedge()
                                if self.cent:
                                    if duty[2] == 'command':
                                        print(f'maximum margin for full on riskfree mode is: {margin} ¢ ({margin/100} $)')
                                    else:
                                        telegram_send_message(f'maximum margin for full on riskfree mode is: {margin} ¢ ({margin/100} $)')
                                else:
                                    if duty[2] == 'command':
                                        print(f'maximum margin for full on riskfree mode is: {margin} $')
                                    else:
                                        telegram_send_message(f'maximum margin for full on riskfree mode is: {margin} $')

                            elif duty[1] == 'max_money_involved':
                                money = database().calculate_all_money_involved_in_full_riskfree()
                                if self.cent:
                                    if duty[2] == 'command':
                                        print(f'max money involved for full riskfree mode is: {money} ¢ ({money/100} $)')
                                    else:
                                        telegram_send_message(f'max money involved for full riskfree mode is: {money} ¢ ({money/100} $)')
                                else:
                                    if duty[2] == 'command':
                                        print(f'max money involved for full riskfree mode is: {money} $')
                                    else:
                                        telegram_send_message(f'max money involved for full riskfree mode is: {money} $')

                            elif duty[1] == 'show_tasks':
                                # Print task dict in command or send it to the telegram bot
                                if duty[2] == 'command':
                                    print(self.task_dict)
                                else:
                                    telegram_send_message(str(self.task_dict))

                            elif duty[1] == 'pos_sum_loss':
                                ticket, monitor = duty[2].split(',')
                                ticket = int(ticket)
                                # Load sum loss of position with ticket from database
                                main_pos_table = database().load_table("main_trend_positions")
                                for pos in main_pos_table:
                                    if pos[0] == ticket:
                                        sum_loss = pos[16]
                                        break
                                
                                if monitor.strip() == "command":
                                    print(f'Sum loss for position with ticket {ticket} is {sum_loss}.')
                                else:
                                    telegram_send_message(f'Sum loss for position with ticket {ticket} is {sum_loss}.')

                            elif duty[1] == 'Turn_on_pos_logs':
                                ticket = int(duty[2])
                                check_pos = False
                                main_trend_table = database().load_table("main_trend_positions")
                                for pos in main_trend_table:
                                    if pos[0] == ticket:
                                        check_pos = True

                                if check_pos:
                                    if f"task_{ticket}_send_logs" in self.task_dict:
                                        telegram_send_message("We already have this task.\n")
                                    else:
                                        # Close position by it ticket that save in database
                                        new_task = threading.Thread(target=self.send_pos_logs, args=[ticket])
                                        new_task.start()
                                        self.task_dict[f"task_{ticket}_send_logs"] = new_task
                                        print(f"Send position {ticket} logs to telegram start.\n")
                                else:
                                    print(f"Position with ticket {ticket} doesen't exist in main_trend_table to send related logs.\n")
                                    telegram_send_message(f"Position with ticket {ticket} doesen't exist in main_trend_table to send related logs.")

                            elif duty[1] == 'Turn_off_pos_logs':
                                ticket = int(duty[2])
                                if f"task_{ticket}_send_logs" in self.task_dict:
                                    pass
                                else:
                                    telegram_send_message(f"There is not any task to send position {ticket} logs.")
                                    
                            elif duty[1] == 'stop_program':
                                self.stop_threads_dict(self.task_dict)
                                if duty[2] == 'y':
                                    self.login.close_all_pos()
                                    database().clear_table("main_trend_positions")
                                    database().clear_table("riskfree_positions")
                                break

                            else:
                                print("You enter invalid input type in the iputs table.\n")
                        
                        # except Exception as e:
                        #     print(f"Error in doing {duty[1]}: {e}")
                        #     telegram_send_message(f"Error in doing {duty[1]}: {e}")

                inputs_table = update_inputs_table

        print("Do User input is finish.\n")


    def stop_threads_dict(self, threads_dict):
        print("Stopping all threads...")
        self.stop_event.set()
        # Wait for all threads to finish
        for item in threads_dict:
            if item != "task_do_input" and item != "task_take_input":
                threads_dict[item].join()
        print("All threads have exited.")


    def load_last_positions(self):
        # Load positions tabls
        main_pos_table = database().load_table("main_trend_positions")
        riskfree_table = database().load_table("riskfree_positions")
        if main_pos_table == []:
            print("There is no existing open position from the past.\n")
        else:
            for pos in main_pos_table:
                print(f"Rerun the position_management for position {pos[0]}.\n")
                # Find risk free position ticket related to this position from risk free table
                if riskfree_table != []:
                    for item in riskfree_table:
                        if item[1] == pos[0]:
                            riskfree_pos_ticket = item[0]
                            riskfree = True
                            break  
                        else:
                            riskfree = False
                else:
                    riskfree = False

                if riskfree:
                    # Create a task for each position exist in the table
                    self.hedging_dict[f"hedg_{pos[0]}"] = auto_hedging(self.login, pos[1], pos[2])
                    self.task_dict[f"task_{pos[0]}"] = threading.Thread(target=self.hedging_dict[f"hedg_{pos[0]}"].position_management, 
                    args=[pos[6], pos[7], self.stop_event], 
                    kwargs={'management_level': pos[3], 'volume': pos[5], 'riskfree_wait': pos[8],
                    'riskfree_level': pos[9], 'magic': pos[11], 'sum_loss':pos[16],
                    'loss_level': pos[12], 'main_pos_ticket': pos[0], 'riskfree_pos_ticket': riskfree_pos_ticket})
                    self.task_dict[f"task_{pos[0]}"].start()
                else:
                    # Create a task for each position exist in the table
                    self.hedging_dict[f"hedg_{pos[0]}"] = auto_hedging(self.login, pos[1], pos[2])
                    self.task_dict[f"task_{pos[0]}"] = threading.Thread(target=self.hedging_dict[f"hedg_{pos[0]}"].position_management, 
                    args=[pos[6], pos[7], self.stop_event], 
                    kwargs={'management_level': pos[3], 'volume': pos[5], 'riskfree_wait': pos[8], 'sum_loss':pos[16],
                    'riskfree_level': pos[9], 'magic': pos[11], 'loss_level': pos[12], 'main_pos_ticket': pos[0]})
                    self.task_dict[f"task_{pos[0]}"].start()


    def load_last_auto_change_riskfree_level(self):
        auto_change_riskfree_table = database().load_table("auto_change_riskfree_level")
        in_process_list = []
        for item in auto_change_riskfree_table:
            if item[7] == 'no':
                in_process_list.append(item)

        if in_process_list == []:
            print("There is no existing auto_change_riskfree_level from the past.\n")
        else:
            for item in in_process_list:
                print(f"Rerun the auto_change_riskfree_level for position {item[1]}.")
                # Take all parameters save in the row
                id = item[0]
                ticket = item[1]
                type_of_autochange = item[2]
                amount = item[3]
                new_riskfree_level = item[4]
                new_money_involved = item[5]

                check_pos = self.check_position_exist(ticket)
                pos = database().load_row("main_trend_positions", ticket)

                if check_pos:
                    pos = database().load_row("main_trend_positions", ticket)
                    number_auto_change_riskfree = pos[15]
                    
                    # Star auto_change_riskfree_level task
                    new_task = threading.Thread(target=auto_change_riskfree().run, 
                    args=[ticket, type_of_autochange, amount, new_riskfree_level, 
                    number_auto_change_riskfree, new_money_involved, id, self.stop_event])
                    new_task.start()

                    # Add the auto change riskfree task to our task dictionary
                    self.task_dict[f"task_{ticket}_auto_change_riskfree_{number_auto_change_riskfree}"] = new_task
                    if type_of_autochange == 'price':
                        print(f"Auto change riskfree level activate, if {type_of_autochange} reach {amount}\n"
                            f"riskfree level change automatically to {new_riskfree_level}.")
                    else:
                        if self.cent:
                            print(f"Auto change riskfree level activate, if {type_of_autochange} reach {amount} ¢ ({amount/100} $)\n"
                                f"riskfree level change automatically to fix {new_riskfree_level} ¢ ({new_riskfree_level/100} $) (profit / loss).\n")
                        else:
                            print(f"Auto change riskfree level activate, if {type_of_autochange} reach {amount} $\n"
                                f"riskfree level change automatically to fix {new_riskfree_level} $ (profit / loss).\n")
                    
                else:
                    print(f"Position with ticket {ticket} doesen't exist for load auto change riskfree level.\n")
                    telegram_send_message(f"Position with ticket {ticket} doesen't exist for load auto change riskfree level.")


    def trade(self):
        log = f"----------0. Program start. ----------\n"
        database().save_log(log)
        print(log)

        # Run all the threads that program need to start
        self.load_last_positions()
        self.load_last_auto_change_riskfree_level()
        self.task_dict["task_take_input"] = threading.Thread(target=self.take_user_input)
        self.task_dict["task_take_input"].start()
        self.task_dict["task_do_input"] = threading.Thread(target=self.do_user_input)
        self.task_dict["task_do_input"].start()
        telegram_task = threading.Thread(target=telegram_bot().run_bot)
        telegram_task.start()
        
    
    def calculate_margin_in_full_onhedge(self):
        # Load all open positions in metatrader and all positions from database
        positions = mt5.positions_get()
        account_info = mt5.account_info()
        leverage = account_info.leverage
        main_trend_positions = database().load_table('main_trend_positions')
        main_positions_info_list = []
        all_margin = 0

        # Find the main positions by comparing the metatrader positions and database positions
        for item in positions:
            for pos in main_trend_positions:
                if item.ticket == pos[0]:
                    main_positions_info_list.append(item)

        # Calculate all margin in full on riskfree mode
        for pos in main_positions_info_list:
            margin = calculator().margin_need_calculator(pos.symbol, pos.volume, pos.price_open, leverage, show=False) 
            all_margin += margin

        return round(all_margin, 2)
    

    def send_pos_logs(self, ticket):
        logs_table = database().load_table("program_log")
        inputs_table = database().load_table("inputs")

        while not self.stop_event.is_set(): 
            # Take update of inputs table every 1 secound and if it has any item that last update didn't have we do it
            update_logs_table = database().load_table("program_log") 
            update_inputs_table = database().load_table("inputs")

            # Check if user stop the position send log
            if inputs_table != update_inputs_table:
                new_duty = self.find_items_in_list1_not_in_list2(update_inputs_table, inputs_table)
                if new_duty != []:
                    for duty in new_duty:
                        if duty[1] == "Turn_off_pos_logs" and int(duty[2]) == ticket:
                            print(f"Sending position {ticket} logs to the telegram stoped.\n")
                            self.task_dict.pop(f"task_{ticket}_send_logs")
                            return None
                            
                inputs_table = update_inputs_table

            # Check if there is new log, send it to the telegram
            elif logs_table != update_logs_table:
                new_log = self.find_items_in_list1_not_in_list2(update_logs_table, logs_table)
                if new_log != []:
                    for log in new_log:
                        try:
                            numbers = self.extract_numbers(log[2])
                            log_ticket = numbers[1]
                            if ticket == log_ticket:
                                telegram_send_message(log[2])

                        except:
                            pass
                
                logs_table = update_logs_table

            # Stop the loop if position not found
            else:
                check_pos = self.check_position_exist(ticket)
                if check_pos is False:
                    print(f"Sending position {ticket} logs to the telegram stoped.\n")
                    telegram_send_message(f"Sending position {ticket} logs to the telegram stoped.")
                    self.task_dict.pop(f"task_{ticket}_send_logs")
                    return None

            time.sleep(1)


    @staticmethod
    def extract_numbers(input_string):
        numbers = re.findall(r'\d+\.\d+|\d+', input_string)
        return [float(number) if '.' in number else int(number) for number in numbers]


    @staticmethod
    def find_items_in_list1_not_in_list2(list1, list2):
        items_list = []
        set1 = set(list1)
        set2 = set(list2)
        items_in_list1_not_in_list2 = set1.difference(set2)

        for item in items_in_list1_not_in_list2:
            items_list.append(item)

        return items_list
    

    @staticmethod
    def check_position_exist(ticket):
        # Retrieve the order information
        order_info = mt5.positions_get(ticket=ticket)
        # Check if the order exists
        if order_info == ():
            print(f"Order with ticket {ticket} not found.")
            return False
        else:
            return True



