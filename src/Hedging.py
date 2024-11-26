from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *
from Risk_and_money_management import *
from auto_trade import *
from data_base import *
from calculator import *



class auto_hedging:
    def __init__(self, login, symbol,  main_trend, cent=True):
        self.login = login
        self.symbol = symbol
        self.main_trend = main_trend
        self.pip = mt5.symbol_info(symbol).point
        self.pip_value = mt5.symbol_info(symbol).trade_tick_value
        self.standard_lot = 1/self.pip
        self.cent = cent


    # This method calculate the equity in full risk free that involved with your hedging setup
    def calculate_equity_involved(self, volume, number_riskfree_part, pip_part=None, pip_total=None, show=True):
        number_riskfree_part += 1
        if pip_total:
            pip_part = pip_total / number_riskfree_part
        
        if pip_part is None and pip_total is None:
            print("You should fill one of pip_part or pip_total")
            return None
        
        total_equity_involved = 0
        spread = mt5.symbol_info(self.symbol).spread 
        part_volume = volume / number_riskfree_part
        level_volume = volume
        equity_involved_list = []

        if number_riskfree_part == 1:
            total_equity_involved = volume * self.standard_lot * self.pip * self.pip_value * (pip_part + (2 * spread))
        else:
            # Calculate money that involved in each level we riskfree position
            while level_volume > 0:
                part_equity_involved = (level_volume * self.standard_lot * self.pip * self.pip_value * (pip_part + (2 * spread)))
                total_equity_involved += part_equity_involved
                equity_involved_list.append(round(total_equity_involved, 3))
                level_volume -= part_volume

        total_equity_involved = round(total_equity_involved, 3)
        if show:
            print(f"equity involved in each level is:", equity_involved_list)
            if self.cent:
                print(f"{total_equity_involved} ¢ ({total_equity_involved/100} $) is involved with your riskfree setup and {spread} pip spread.") 
            else:
                print(f"({total_equity_involved} $) is involved with your riskfree setup and {spread} pip spread..")

        return total_equity_involved


    # This method try to find a sutable volume list for use to acheave fixprice at the end of riskfree
    # First member of volume list is the main position volume and others are risk free volumes
    def find_hedging_setup(self, fix_price, number_riskfree_part, pip_part, show=True):
        volume_list = []
        total_equity_involved = 0
        volume = 0.01

        while True:
            total_equity_involved = self.calculate_equity_involved(volume, number_riskfree_part, pip_part, show=False)
            if total_equity_involved >= fix_price:
                break
            else:
                volume += 0.01

        if number_riskfree_part != 0:
            part_volume = volume / number_riskfree_part

        if number_riskfree_part == 0:
            volume_list = [volume, volume]
        else:
            volume = self.costum_round(volume, 2, 1)
            part_volume = self.costum_round(part_volume, 2, 9)
            remain_volume_list = []
            n = 0
            remain_volume = 0
            while remain_volume >= 0:
                remain_volume = volume - (n * part_volume)
                if remain_volume < 0:
                    pass
                else:
                    remain_volume = round(remain_volume, 2)
                    remain_volume_list.append(remain_volume)
                n += 1

            remain_volume = remain_volume_list[-1]
            first_riskfree_volume = part_volume + remain_volume

            volume_list.append(volume)
            volume_list.append(first_riskfree_volume)
            for i in range(number_riskfree_part - 1):
                volume_list.append(part_volume)

            if show:
                if remain_volume > 0:
                    print(f"Set first position volume {volume} lot and set each risk free part {part_volume} lot")
                    print(f"Your main position volume has {remain_volume} lot remain volume when we divide it to {number_riskfree_part}.\n"
                        f"We add this remain volume to first risk free part volume and it increased from {part_volume} lot to {first_riskfree_volume} lot.") 
                
        return volume_list


    # This method use to findout your setup can be make or not 
    def calculate_fixprice_volume(self, fix_price, number_riskfree_part, pip_part, initial_volume=None, part_diff_volume=None):
        spread = mt5.symbol_info(self.symbol).spread 
        number_riskfree_part += 1
        spread = 20
        total_number_diff = 0
        for number in range(number_riskfree_part):
            total_number_diff += number

        
        total_volume = fix_price / ((pip_part + spread) * (self.standard_lot * self.pip * self.pip_value))

        # part_diff_volume = ?
        if initial_volume:
            part_diff_volume = ((total_volume/(number_riskfree_part/2)) - (2 * initial_volume)) / (number_riskfree_part - 1)
            part_diff_volume = round(abs(part_diff_volume), 2)
            volume_list = []
            for i in range(number_riskfree_part):
                volume_list.append(round(initial_volume - (i * part_diff_volume), 2))    
            # Show impressive volume in each section                    
            print("impressive volume in each section is:",volume_list)
            return part_diff_volume
        
        # volume = ?
        elif part_diff_volume:
            last_volume = ((total_volume/(number_riskfree_part/2)) - ((number_riskfree_part - 1) * part_diff_volume))/2
            volume_list = []
            for i in range(number_riskfree_part):
                volume_list.append(round(last_volume + (i * part_diff_volume), 2))   
            volume_list.reverse()                     
            print("volume list is:",volume_list)
            initial_volume = volume_list[-1]
            return initial_volume
        
        else:
            print("You should fill one of initial_volume or part_diff_volume.")
            return None


    # Auto position management
    # You can enter the loss zone manualy or calculate it by atr
    def position_management(self, pip_part, zone, stop_event, fix_price=None, volume=None, management_level=1, riskfree_wait=6, 
        sum_loss=0, cent=True, riskfree_level=None, magic=1000, loss_level=None, main_pos_ticket=None, riskfree_pos_ticket=None,
        hedge_time = datetime.now()):
 
        spread = mt5.symbol_info(self.symbol).spread 
        pip_loss = pip_part + spread
        start = False
        self.clock_flag = True
        
        if fix_price is None and volume is None:
            print("You should fill one of the fix price or volume parameter.")
            return None
        elif fix_price:
            volume_list = []
            number_riskfree_part = 0
            # In side find hedging setup algoritm we calculate two spreads and it doesen't need to use pip loss
            volume_list = self.find_hedging_setup(fix_price, number_riskfree_part, pip_part)
        else:
            fix_price = calculator().money_calculator(self.symbol, volume, pip_loss + spread)
            volume_list = [volume, volume * 2]


        if self.main_trend == 'bullish':
            # Calculate the profit that we close the risk free positions on it
            if riskfree_wait <= 4:
                print("Risk free wait should be more than 4.\n")
                return None
            else:
                riskfree_wait_close = riskfree_wait - 2
                riskfree_wait_pip = riskfree_wait * self.pip
                riskfree_wait_close_pip = riskfree_wait_close * self.pip
                wait_profit = calculator().money_calculator(self.symbol, volume, riskfree_wait)
                close_wait_profit = calculator().money_calculator(self.symbol, volume, riskfree_wait_close)

            #try:
                # 1
                # Open main position in main trend direction
                if management_level == 1:
                    log = f"----------1. Main position opend. {main_pos_ticket} ----------"
                    database().save_log(log)
                    print(log)
                    main_pos = self.login.open_buy_pos(self.symbol, volume_list[0], magic=magic, type_filling=0)

                    # Get the current time
                    current_datetime = datetime.now()
                    print("open main pos finished--------", current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

                    main_pos_spread = mt5.symbol_info(self.symbol).spread 
                    main_pos_ticket = main_pos.order
                    trade_request = main_pos.request

                    # The level(price) that if reach, we riskfree the position
                    price_loss = pip_loss * self.pip
                    riskfree_level = trade_request.price - price_loss
                    management_level = 2

                    # Calculate money involved in risk free mode
                    pip_money = pip_part + (2 * main_pos_spread)
                    money_involved = calculator().money_calculator(self.symbol, volume, pip_money) * (-1)
                    if cent:
                        print(f"Money involved in risk free mode is about {money_involved} ¢ ({money_involved/100} $).\n")
                        print(f"Wait profit is {wait_profit} ¢ ({wait_profit/100} $).")
                        print(f"Close Wait profit is {close_wait_profit} ¢ ({close_wait_profit/100} $).\n")
                    else:
                        print(f"Money involved in risk free mode is about {money_involved} $.\n")
                        print(f"Wait profit is {wait_profit}.")
                        print(f"Close Wait profit is {close_wait_profit} $.\n")
                        
                    database().save_main_pos(main_pos_ticket, self.symbol,self.main_trend, management_level, fix_price, volume, 
                                            pip_part, zone, riskfree_wait, riskfree_level, magic, money_involved, main_pos_spread)


                # Check every second (you can adjust the interval)
                while True:
                    # Get the current time
                    current_datetime = datetime.now()

                    # Compare the current time with the target time
                    if current_datetime >= hedge_time:
                        log = f"----------0. Hedging start. {main_pos_ticket}----------\n"
                        database().save_log(log)
                        print(log)
                        start = True
                        break
                    else:
                        pass


                while not stop_event.is_set() and start:
                    # Check position exist
                    main_pos_exist = self.check_position_exist(main_pos_ticket)
                    if main_pos_exist is False:
                        log = f"----------0. Position not found. {main_pos_ticket}----------"
                        database().save_log(log)
                        print(log)
                        # Delete position frome database
                        database().delete_row("main_trend_positions", main_pos_ticket)

                        # Set the auto change riskfree achieve to close if we had any in process order in the database
                        auto_change_riskfree_table = database().load_table("auto_change_riskfree_level")
                        for item in auto_change_riskfree_table:
                            if item[1] == main_pos_ticket and item[7] == 'no':
                                database().update_achieve_by_ticket(main_pos_ticket, 'close')

                        # Close related riskfree position if exist
                        try:
                            if riskfree_pos_ticket is not None:
                                self.login.close_pos(riskfree_pos_ticket)
                                database().delete_row("riskfree_positions", riskfree_pos_ticket)
                                print("Risk free position closed.")
                            else:
                                print("No risk free position has been opend yet to close.")
                        except:
                            database().delete_row("riskfree_positions", riskfree_pos_ticket)
                            print("There is no risk free position to close.")

                        return None
                    
                    # Chek riskfree position exist, If not close main position
                    if management_level == 3 or management_level == 4 or management_level == 6:
                        riskfree_pos_exist = self.check_position_exist(riskfree_pos_ticket)
                        if riskfree_pos_exist is False:
                            log = f"---------- Riskfree position not found. {riskfree_pos_ticket}----------"
                            database().save_log(log)
                            print(log)
                            database().delete_row("riskfree_positions", riskfree_pos_ticket)
                            self.login.close_pos(main_pos_ticket)
                            database().delete_row("main_trend_positions", main_pos_ticket)
                            print("Main position closed.")
                            return None

                    # Check if risk free level change by user
                    riskfree_level = database().load_riskfree_level(main_pos_ticket)

                    # Get update price (we use bid price because main trend is bullish)
                    tick_info = mt5.symbol_info(self.symbol)
                    now_price = tick_info.bid
                    now_ask_price = tick_info.ask
                    
                    
                    if self.clock_flag:
                        # Get the current time
                        current_datetime = datetime.now()
                        print("get on management level 2--------", current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
                        self.clock_flag = False

                    # 2 
                    # Open risk free position if price go down the risk free level
                    if management_level == 2:
                        if now_price < riskfree_level:
                            log = f"----------2. Risk free position opend. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)

                            riskfree_pos = self.login.open_sell_pos(self.symbol, volume_list[1], magic=magic, type_filling=0)
                            riskfree_pos_spread = mt5.symbol_info(self.symbol).spread
                            riskfree_pos_ticket = riskfree_pos.order
                            riskfree_trade_request = riskfree_pos.request
                            
                            # Get exact money involved frome metatrader
                            pos_info = mt5.positions_get(ticket=riskfree_pos_ticket)
                            pos_info = pos_info[0]
                            riskfree_pos_profit = pos_info.profit
                            pos_info = mt5.positions_get(ticket=main_pos_ticket)
                            pos_info = pos_info[0]
                            main_pos_profit = pos_info.profit
                            exact_money_involved = main_pos_profit + riskfree_pos_profit
                            database().update_money_involved(main_pos_ticket, exact_money_involved)

                            # Calculate the zone and money loss for it
                            loss_level = riskfree_trade_request.price + (zone * self.pip)
                            loss_level = round(loss_level, 5)
                            database().save_loss_level(main_pos_ticket, loss_level)
                            print(f"Loss level is {loss_level}.") 
                            money_loss = calculator().money_calculator(self.symbol, volume, (zone + riskfree_pos_spread))
                            if cent:
                                print("If price can't reach riskfree pos break even point plus wait profit, riskfree position closed\n"
                                    f"and you loss about {money_loss} ¢ ({money_loss/100} $) with this {zone} pip zone and {riskfree_pos_spread} pip spread.\n")
                            else:
                                print("If price can't reach riskfree pos break even point plus wait profit, riskfree position closed\n"
                                    f"and you loss about {money_loss} $ with this {zone} pip zone and {riskfree_pos_spread} pip spread.\n")
                                
                            database().save_riskfree_pos(riskfree_pos_ticket, main_pos_ticket, self.symbol,self.main_trend, management_level,
                                        fix_price, volume, pip_part, zone, riskfree_wait, riskfree_level, riskfree_pos_spread, magic)
                            
                            management_level = 3
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                    # 3
                    # After risk free position open, we wait for it to break even or revers to the main trend direction 
                    if management_level == 3:
                        wait_price = riskfree_level - riskfree_wait_pip

                        # Check the price to reach riskfree position break even pluse risk free wait or return back to the main direction
                        if now_price > loss_level :
                            self.login.close_pos(riskfree_pos_ticket)
                            # Take riskfree spread befor delet it from data base
                            riskfree_pos_spread = database().load_row("riskfree_positions", riskfree_pos_ticket)[12]
                            database().delete_row("riskfree_positions", riskfree_pos_ticket)
                            log = f"----------3. Go up to the zone. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)
                            print("Price go up to the zone befor reach risk free break even point,\n" 
                                "we forced to close it befor lossing more trend.")
                            
                            # Calculate money we loss for force close risk free position 
                            total_pip = riskfree_pos_spread + zone
                            more_money_involved = calculator().money_calculator(self.symbol, volume, total_pip)
                            parameters = "riskfree_pos_spread + zone"
                            
                            database().save_money_loss(more_money_involved, management_level, parameters, main_pos_ticket)
                            sum_loss += more_money_involved * (-1)
                            database().update_sum_loss(main_pos_ticket, sum_loss)
                            if cent:
                                print(f"You loss {more_money_involved} ¢ ({more_money_involved/100} $) for force close risk free position position.\n")
                            else:
                                print(f"You loss {more_money_involved} $ for force close risk free position position.\n")
                                
                            management_level = 2
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                        elif now_ask_price < wait_price:
                            log = f"----------3. Reach the risk free break even. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)
                            print(f"Price reach the risk free break even point plus {riskfree_wait} pip profit.\n")

                            # Calculate the money that if price doesen't go down to the zone we loss
                            riskfree_pos_spread = database().load_row("riskfree_positions", riskfree_pos_ticket)[12]
                            total_pip = riskfree_pos_spread + zone
                            more_money_involved = calculator().money_calculator(self.symbol, volume, total_pip)
                            parameters = "riskfree_pos_spread + zone"
                            database().save_no_money_loss(more_money_involved, management_level, parameters, main_pos_ticket)

                            management_level = 4
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                    # 4
                    # Now we should wait for price revers to the main direction
                    # We sense this revers by risk free position profit loss
                    if management_level == 4:
                        wait_close_price = riskfree_level - riskfree_wait_close_pip

                        if now_ask_price > wait_close_price :
                            log = f"----------4. Price revers to riskfree level. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)

                            riskfree_close_result = self.login.close_pos(riskfree_pos_ticket)
                            database().delete_row("riskfree_positions", riskfree_pos_ticket)
                            loss_level = riskfree_close_result.price - (zone * self.pip)
                            database().save_loss_level(main_pos_ticket, loss_level)
                            
                            print("Price revers and again reach the risk free level and we close the risk free position.\n" 
                                "it seams it is go back to the main trend direction.\n")
                            management_level = 5
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                    # 5
                    # After closing risk free position we consider a zone and price should go up to the riskfree level or go down to the zone
                    if management_level == 5:
                        if now_price > riskfree_level :
                            log = f"----------5. Go back up to the risk free level. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)
                            print("Price revers and go up to the start risk free level.\n")

                            # Calculate the money that if price doesen't go back up we loss
                            riskfree_pos_spread = mt5.symbol_info(self.symbol).spread 
                            main_pos_spread = database().load_main_pos_spread(main_pos_ticket)
                            total_pip = main_pos_spread + riskfree_pos_spread + riskfree_wait + zone
                            more_money_involved = calculator().money_calculator(self.symbol, volume, total_pip)
                            total_money_involved = calculator().money_calculator(self.symbol, volume, (total_pip + pip_loss))
                            parameters = "riskfree_pos_spread + riskfree_wait + zone"
                            database().save_no_money_loss(more_money_involved, management_level, parameters, main_pos_ticket)

                            management_level = 2
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                        elif now_price < loss_level :
                            log = f"----------5. Force open again risk free. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)

                            riskfree_pos = self.login.open_sell_pos(self.symbol, volume_list[1], magic=magic, type_filling=0)
                            riskfree_pos_ticket = riskfree_pos.order

                            # Get exact money involved frome metatrader
                            pos_info = mt5.positions_get(ticket=riskfree_pos_ticket)
                            pos_info = pos_info[0]
                            riskfree_pos_profit = pos_info.profit
                            pos_info = mt5.positions_get(ticket=main_pos_ticket)
                            pos_info = pos_info[0]
                            main_pos_profit = pos_info.profit
                            exact_money_involved = main_pos_profit + riskfree_pos_profit
                            database().update_money_involved(main_pos_ticket, exact_money_involved)

                            # Calculate the money we loss for force open again risk free position
                            riskfree_pos_spread = mt5.symbol_info(self.symbol).spread 
                            main_pos_spread = database().load_main_pos_spread(main_pos_ticket)
                            total_pip = main_pos_spread + riskfree_pos_spread + riskfree_wait + zone
                            more_money_involved = calculator().money_calculator(self.symbol, volume, total_pip)
                            total_money_involved = calculator().money_calculator(self.symbol, volume, (total_pip + pip_loss))
                            parameters = "riskfree_pos_spread + riskfree_wait + zone"

                            database().save_money_loss(more_money_involved, management_level, parameters, main_pos_ticket)
                            sum_loss += more_money_involved * (-1)
                            database().update_sum_loss(main_pos_ticket, sum_loss)

                            print("We Forced to opend again risk free position,\n"
                                "because price can't reach risk free level and go down to the close loss level.")
                            if cent:
                                print(f"Total money that involved now is {total_money_involved} ¢ ({total_money_involved/100} $),\n"
                                    f"You will loss {more_money_involved} ¢ ({more_money_involved/100} $) after level 6 for wait to price go up to the first risk free level.\n")
                            else:
                                print(f"Total money that involved now is {total_money_involved} $,\n"
                                    f"You will loss {more_money_involved} $ after level 6 for wait to price go up to the first risk free level.\n")

                            database().save_riskfree_pos(riskfree_pos_ticket, main_pos_ticket, self.symbol,self.main_trend, management_level,
                                        fix_price, volume, pip_part, zone, riskfree_wait, riskfree_level, riskfree_pos_spread, magic)
                            management_level = 6
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                    # 6 
                    # If risk free position moved to another level, we wait for price to go back to the last level and we close the risk free position in loss
                    if management_level == 6:
                        if now_price > riskfree_level:
                            log = f"----------6. Go up to the risk free level. {main_pos_ticket} ----------"
                            database().save_log(log)
                            print(log)

                            riskfree_close_result = self.login.close_pos(riskfree_pos_ticket)
                            database().delete_row("riskfree_positions", riskfree_pos_ticket)
                            
                            print("Price revers and go up to the start risk free level,\n" 
                                    "but we close the risk free position in loss because of special condition.\n")
                            management_level = 2
                            database().update_management_level("main_trend_positions", main_pos_ticket, management_level)
                            database().update_management_level("riskfree_positions", riskfree_pos_ticket, management_level)

                log = f" ----------0. Position management finish. {main_pos_ticket}----------"
                database().save_log(log)
                print(log)
            
            #except Exception as e:
                #print(f"Error in management_level {management_level}: {e}.")
                #telegram_send_message(f"Error in management_level {management_level}: {e}")
        else:
            pass
    

    def get_last_opened_position_ticket(self):
        positions = mt5.positions_get()
        ticket_list = []
        
        for pos in positions:
            ticket_list.append(pos.ticket)

        if ticket_list == []:
            print("No valid open positions.")
            return None
        else:
            max_ticket = max(ticket_list)
            return max_ticket
    

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


    # This method take a number and round it as you specified by number_decimal and up_down_round
    @staticmethod
    def costum_round(number, number_decimal, up_down_round):
        str_number = str(number)
        str_number_list = []
        for number in range(len(str_number)):
            str_number_list.append(str_number[number])
            if str_number[number] == '.':
                number_dot = number
        
        round_numbers = str_number_list[number_dot + number_decimal + 1:len(str_number_list)]
        if int(round_numbers[0]) >= up_down_round :
            str_number_list[number_dot + number_decimal] = str(int(str_number_list[number_dot+2]) + 1)
            del str_number_list[number_dot + number_decimal + 1:len(str_number_list)]
        else:
            del str_number_list[number_dot + number_decimal + 1:len(str_number_list)]

        result_str = ''.join(str_number_list)
        result = float(result_str)
        
        return result
    
