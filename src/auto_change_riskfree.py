from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *
from Risk_and_money_management import *
from auto_trade import *
from data_base import *
from calculator import *


"""
We write some condition for auto change riskfree that if price or profit reach user goal
but it is illogical to change risk free level, the program pass.

when position is risk free --------> illogic to move riskfree level upward --------> because we loss a part of the market main trend
when position is no risk free --------> illogic to move riskfree level downward --------> because we loss a part of profit we take

"""

class auto_change_riskfree:
    def __init__(self):
        pass


    # For automaticly change riskfree level when position reach the enter goal
    def run(self, ticket, type_of_autochange, amount, new_riskfree_level, number_auto_change_riskfree
        , new_money_involved, id, stop_event):

        if type_of_autochange == "price":
            # Chek if user enter invalid price amount
            if amount <= 0:
                print("Price amount can't be zero or negetiv number.")
                telegram_send_message("Price amount can't be zero or negetiv number.")
                return None
            
            # Take position information
            pos = database().load_row("main_trend_positions", ticket)
            symbol = pos[1]
            pos_spread = pos[14]
            last_riskfree_level = pos[9]
            main_trend = pos[2]

            # Check symbol price and any information we need
            tick_info = mt5.symbol_info(symbol)
            pip = tick_info.point
            first_price = tick_info.bid
            now_price = first_price

            # Check that riskfree level is change to down level or up level
            if new_riskfree_level > last_riskfree_level:
                new_level = "up"
            elif new_riskfree_level < last_riskfree_level:
                new_level = "down"
            else:
                print("Equal riskfree level by last riskfree level.")
                new_level = None

            # Check that user is waiting for set new riskfree level if price go up or down.
            if first_price < amount:
                wait_for = "go_up"
            elif first_price > amount:
                wait_for = "go_down"
            else:
                print("Equal price, use simple change riskfree level, not auto.")
                wait_for = None

            while not stop_event.is_set():
                # Check if achieve set to close or stop
                row = database().load_row_2("auto_change_riskfree_level", id)
                if row[7] == 'close':
                    print(f"Auto change riskfree level with id {id} for position with ticket {ticket} is close.\n")
                    break
                elif row[7] == 'stop':
                    print(f"Auto change riskfree level with id {id} for position with ticket {ticket} is stop.\n")
                    break

                # Check symbol price
                tick_info = mt5.symbol_info(symbol)
                now_price = tick_info.bid
                if wait_for == "go_up":
                    if now_price < amount:
                        time.sleep(1)
                    else:   
                        if main_trend == 'bullish':
                            check_riskfree = self.check_position_isrikfree(ticket)
                            if check_riskfree:
                                if new_level == "down":
                                    if new_riskfree_level > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to up level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break

                            else: 
                                if new_level == "up":
                                    if new_riskfree_level < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break  
                                    else: 
                                        print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to down level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                        else:
                            check_riskfree = self.check_position_isrikfree(ticket)
                            if check_riskfree:
                                if new_level == "up":
                                    if new_riskfree_level < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                else:
                                    print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to down level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                            else: 
                                if new_level == "down":
                                    if new_riskfree_level > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break 
                                    else:
                                        print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                else: 
                                    print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to up level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break

                elif wait_for == "go_down":
                    if now_price > amount:
                        time.sleep(1)
                    else:   
                        if main_trend == 'bullish':
                            check_riskfree = self.check_position_isrikfree(ticket)
                            if check_riskfree:
                                if new_level == "down":
                                    if new_riskfree_level > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to up level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break

                            else: 
                                if new_level == "up":
                                    if new_riskfree_level < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break  
                                    else: 
                                        print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to down level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                        else:
                            check_riskfree = self.check_position_isrikfree(ticket)
                            if check_riskfree:
                                if new_level == "up":
                                    if new_riskfree_level < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                else:
                                    print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to down level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                            else: 
                                if new_level == "down":
                                    if new_riskfree_level > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break 
                                    else:
                                        print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                else: 
                                    print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to up level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                
                else:
                    break

                time.sleep(2)    

        elif type_of_autochange == "profit":
            # The new_riskfree_level  that user enter is a profit not price, and we should calculat the price
            new_riskfree_level_profit = new_riskfree_level 
            pos = database().load_row("main_trend_positions", ticket)
            symbol = pos[1]
            pos_spread = pos[14]
            last_riskfree_level = pos[9]
            main_trend = pos[2]
            tick_info = mt5.symbol_info(symbol)
            pip = tick_info.point
            pos_spread_price = pos_spread * pip

            # Check profit
            pos_info = mt5.positions_get(ticket=ticket)
            pos_info = pos_info[0]
            first_profit = pos_info.profit
            volume = pos_info.volume
            price_open = pos_info.price_open
            now_profit = first_profit

            if main_trend == 'bullish':
                # Change new_riskfree_level profit to new_riskfree_level price
                price_dif = calculator().dif_calculator(symbol, volume, new_riskfree_level_profit, price_or_pip='price')
                new_riskfree_level = price_open + price_dif - pos_spread_price
            else:
                # Change new_riskfree_level profit to new_riskfree_level price
                price_dif = calculator().dif_calculator(symbol, volume, new_riskfree_level_profit, price_or_pip='price')
                new_riskfree_level = price_open - price_dif + pos_spread_price

            # Check that riskfree level is change to down level or up level
            if new_riskfree_level > last_riskfree_level:
                new_level = "up"
            elif new_riskfree_level < last_riskfree_level:
                new_level = "down"
            else:
                print("Equal riskfree level by last riskfree level.\n")
                new_level = None

            # Check that user is waiting for set new riskfree level if price go up or down.
            if first_profit < amount:
                wait_for = "go_up"
            elif first_profit > amount:
                wait_for = "go_down"
            else:
                print("Equal price, use simple change riskfree level, not auto.")
                wait_for = None

            while not stop_event.is_set():
                # Check if achieve set to close or stop
                row = database().load_row_2("auto_change_riskfree_level", id)
                if row[7] == 'close':
                    print(f"Auto change riskfree level with id {id} for position with ticket {ticket} is close.\n")
                    break
                elif row[7] == 'stop':
                    print(f"Auto change riskfree level with id {id} for position with ticket {ticket} is stop.\n")
                    break

                # Check profit
                pos_info = mt5.positions_get(ticket=ticket)
                pos_info = pos_info[0]
                now_profit = pos_info.profit

                if wait_for == "go_up":
                    if now_profit < amount:
                        time.sleep(1)
                    else:   
                        check_riskfree = self.check_position_isrikfree(ticket)
                        if main_trend == 'bullish':
                            if check_riskfree:
                                if new_level == "down":
                                    if new_riskfree_level_profit > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to up level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break

                            else: 
                                if new_level == "up":
                                    if new_riskfree_level_profit < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break   
                                    else:
                                        print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to down level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                        else:
                            if check_riskfree:
                                if new_level == "up":
                                    if new_riskfree_level_profit < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to down level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                            else: 
                                if new_level == "down":
                                    if new_riskfree_level_profit > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break 
                                    else:
                                        print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else: 
                                    print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to up level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break

                elif wait_for == "go_down":
                    if now_profit > amount:
                        time.sleep(1)
                    else:   
                        check_riskfree = self.check_position_isrikfree(ticket)
                        if main_trend == 'bullish':
                            if check_riskfree:
                                if new_level == "down":
                                    if new_riskfree_level_profit > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in risk free mode, it is wrong to chang risk free level to up level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break

                            else: 
                                if new_level == "up":
                                    if new_riskfree_level_profit < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break   
                                    else:
                                        print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bullish main trend and in no risk free mode, it is wrong to chang risk free level to down level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                        else:
                            if check_riskfree:
                                if new_level == "up":
                                    if new_riskfree_level_profit < amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break
                                    else:
                                        print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to more than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else:
                                    print("In bearish main trend and in risk free mode, it is wrong to chang risk free level to down level\n"
                                          " because we loss trend so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                            else: 
                                if new_level == "down":
                                    if new_riskfree_level_profit > amount:
                                        # Change riskfree level after reach goal and all another things in the database change
                                        database().update_riskfree_level("main_trend_positions", ticket, new_riskfree_level)
                                        try:
                                            database().update_riskfree_level("riskfree_positions", ticket, new_riskfree_level)
                                        except:
                                            pass
                                        database().update_money_involved(ticket, new_money_involved)
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'yes')
                                        print(f"Risk free level change to {new_riskfree_level}")
                                        break 
                                    else:
                                        print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to less than\n"
                                            "amount so we close auto_change_riskfree with out any change in riskfree level.\n")
                                        database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                        database().update_achieve(id, 'close')
                                        break
                                else: 
                                    print("In bearish main trend and in no risk free mode, it is wrong to chang risk free level to up level\n"
                                    "because we loss our profit we take so we close auto_change_riskfree with out any change in riskfree level.\n")
                                    database().update_number_auto_change_riskfree(ticket, number_auto_change_riskfree - 1)
                                    database().update_achieve(id, 'close')
                                    break
                
                else:
                    break
        
        else:
            print("Invalid type of auto change.")


    @staticmethod           
    def check_position_isrikfree(ticket):
        riskfree_table = database().load_table("riskfree_positions")
        for riskfree_pos in riskfree_table:
            if ticket == riskfree_pos[1]:
                return True
            else:
                return False
