from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *
from Risk_and_money_management import *


class auto_trade:
    def __init__(self, symbol, timeframe, minor_timeframe, position_type):
        self.symbol = symbol
        self.timeframe = timeframe
        self.minor_timeframe = minor_timeframe
        self.position_type = position_type
        self.pip = mt5.symbol_info(symbol).point
        self.pip_value = mt5.symbol_info(symbol).trade_tick_value
        self.standard_lot = 1/self.pip
        

    # This function take a claster zone and check the price every minute until price reach the zone
    def reach_claster(self, claster1, claster2, faile_point, pip_tolerance=None):
        in_claster = False
        # It doesen't matter which claster is enterd by user, larger or smaller
        # User can consider a tolerance for his analysis
        if pip_tolerance is not None:
            if claster1 > claster2:
                claster1 = claster1 + (pip_tolerance * self.pip)
                claster2 = claster2 - (pip_tolerance * self.pip)
            else:
                claster1 = claster2 + (pip_tolerance * self.pip)
                claster2 = claster1 - (pip_tolerance * self.pip)

            print(f"claster1 with tolerance is {claster1} and claster2 with tolerance is {claster2}")
            print("(all ways shuold claster1 > claster2)")
        else:
            if claster1 > claster2:
                pass
            else:
                claster1 = claster2
                claster2 = claster1

        while in_claster is False:
            data = datamine(self.timeframe, self.symbol, 'online', number_data=5)
            data = data.df()

            if self.position_type == "short":
                if data["high"][-2] >= claster2:
                    print("Price reach the claster")
                    in_claster = True
                    return True
                elif data["close"][-2] < faile_point:
                    print("The candle close price broke the faile point befor reaching claster.")
                    in_claster = False
                    return False
                else: 
                    print("Wait for reach claster ...")
                    in_claster = False

            else:
                if data["low"][-2] <= claster1:
                    print("Price reach the claster")
                    in_claster = True
                    return True
                elif data["close"][-2] > faile_point:
                    print("The candle close price broke the faile point befor reaching claster.")
                    in_claster = False
                    return False
                else:
                    print("Wait for reach claster ...")
                    in_claster = False

            time.sleep(60)


    # This function take a trigger point or condition and check the price every minute until price reach the trigger
    def reach_trigger(self, trigger_type, faile_point, trigger_point=None, DTlist=[8, 5, 3, 3]):
        data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
        data = data.df()
        in_trigger = False
        last_floor = swing_finder(data, macdhistogram_signal=True).last_swing("floor")
        last_ceiling = swing_finder(data, macdhistogram_signal=True).last_swing("ceiling")
        
        # Trigger by DToscilator
        if trigger_type == "DToscilator":
            while in_trigger is False:
                data = datamine(self.timeframe, self.symbol, 'online', number_data=500)
                data = data.df()

                # Add dt oscilator and it 's signal to the df
                data = indicator.dt_oscillator(data, 
                                               lengthRSI=DTlist[0], 
                                               lengthStoch=DTlist[1], 
                                               smoothK=DTlist[2], 
                                               smoothD=DTlist[3])
                
                if self.position_type == "short":
                    # Check if price make a new ceiling
                    new_ceiling = swing_finder(data, macdhistogram_signal=True).last_swing("ceiling")
                    if new_ceiling > last_ceiling:
                        last_ceiling = new_ceiling
                        # Check if price is in the faile point range
                        if data["close"][-2] > faile_point:
                            print("The price go up to the faile point and the analysis get failed")
                            in_trigger = False
                            self.botrun = False
                            break
                        else:
                            print("price make a new ceiling under the faile point")

                    # Check if DT oscilator go against the position befor trigger
                    if (data[-2]["DToscilator_signal"] == "Bull Rev in OS"
                            or data[-2]["DToscilator_signal"] == "Bull Rev"
                            or data[-2]["DToscilator_signal"] == "Bear OS"):
                        
                        print("DT oscilator go against the position befor trigger and analysis get failed")
                        in_trigger = False
                        self.botrun = False
                        break

                    if (data[-2]["DToscilator_signal"] ==  "Bear Rev in OB" 
                        or data[-2]["DToscilator_signal"] ==  "Bear Rev"):
                        print(f'Price activate trigger by {data[-2]["DToscilator_signal"]}')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        in_trigger = True
                        return entry_point
                        
                else:
                    # Check if price make a new floor
                    new_floor = swing_finder(data, macdhistogram_signal=True).last_swing("floor")
                    if new_floor < last_floor:
                        last_floor = new_floor
                        # Check if price is in the claster range
                        if data["close"][-2] < faile_point:
                            print("The price go down to the faile point and the analysis get failed")
                            self.botrun = False
                            in_trigger = False
                            break
                        else:
                           print("Price make a new floor over the faile point") 

                    # Check if DT oscilator go against the position befor trigger
                    if (data[-2]["DToscilator_signal"] == "Bear Rev in OB"
                            or data[-2]["DToscilator_signal"] == "Bear Rev"
                            or data[-2]["DToscilator_signal"] == "Bull OB"):
                        
                        print("DT oscilator go against the position befor trigger and analysis get failed")
                        in_trigger = False
                        self.botrun = False
                        break

                    if (data[-2]["DToscilator_signal"] ==  "Bull Rev in OS"
                        or data[-2]["DToscilator_signal"] ==  "Bull Rev"):
                        print(f'Price activate trigger by {data[-2]["DToscilator_signal"]}')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        in_trigger = True
                        return entry_point
                
                time.sleep(60)

        # Trigger by minor swing
        elif trigger_type == "minorswing":
            # Automatically trigger point finding, if user doesen't enter it manually
            if trigger_point is None:
                minor_data = datamine(self.minor_timeframe, self.symbol, 'online', number_data=10000)
                minor_data = data.df()
                if self.position_type == "short":
                    # Find last minor floor for trigger point
                    trigger_point = swing_finder(minor_data, macdhistogram_signal=True).last_swing("floor")
                
                else:
                    # Find last minor ceiling for trigger point
                    trigger_point = swing_finder(minor_data, macdhistogram_signal=True).last_swing("ceiling")
            

            while in_trigger is False:
                data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
                data = data.df()

                if self.position_type == "short":
                    # Check if price make a new ceiling
                    new_ceiling = swing_finder(data, macdhistogram_signal=True).last_swing("ceiling")
                    if new_ceiling > last_ceiling:
                        last_ceiling = new_ceiling
                        # Check if price is in the faile point range
                        if data["close"][-2] > faile_point:
                            print("The price go up to the faile point and the analysis get failed")
                            in_trigger = False
                            self.botrun = False
                            break
                        else:
                            print("price make a new ceiling under the faile point")

                    # When price go under the trigger point, trigger activate
                    if data["close"][-2] < trigger_point:
                        print(f'Price activate trigger by {data["close"][-2]} price')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        in_trigger = True
                        return entry_point   
                    
                else:
                    # Check if price make a new floor
                    new_floor = swing_finder(data, macdhistogram_signal=True).last_swing("floor")
                    if new_floor < last_floor:
                        last_floor = new_floor
                        # Check if price is in the claster range
                        if data["close"][-2] < faile_point:
                            print("The price go down to the faile point and the analysis get failed")
                            self.botrun = False
                            in_trigger = False
                            break
                        else:
                           print("Price make a new floor over the faile point") 

                    # When price go above the trigger point, trigger activate
                    if data["close"][-2] > trigger_point:
                        print(f'Price activate trigger by {data["close"][-2]} price')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        in_trigger = True
                        return entry_point

        # Trigger by a simple point
        elif trigger_type == "simplepoint":
            # Automatically trigger point finding, if user doesen't enter it manually
            if trigger_point is None:
                print("You should enter your trigger point in this type of trigger")
                return None

            while True:
                data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
                data = data.df()

                if self.position_type == "short":
                    if data["close"][-2] > faile_point:
                        print("The price go up to the faile point and the analysis get failed")
                        return None         

                    # When price go under the trigger point, trigger activate
                    if data["close"][-2] < trigger_point:
                        print(f'Price activate trigger by {data["close"][-2]} price')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        return entry_point   
                    
                else:
                    if data["close"][-2] < faile_point:
                        print("The price go under the faile point and the analysis get failed")
                        return None         

                    # When price go under the trigger point, trigger activate
                    if data["close"][-2] > trigger_point:
                        print(f'Price activate trigger by {data["close"][-2]} price')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        return entry_point

        # Trigger by major swing in other words the start point of the wave we trade in
        else:
            # Automatically trigger point finding, if user doesen't enter it manually
            if trigger_point is None:
                major_data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
                major_data = data.df()
                if self.position_type == "short":
                    # Find last major floor for trigger point
                    trigger_point = swing_finder(major_data, macdhistogram_signal=True).last_swing("floor")
                else:
                    # Find last major ceiling for trigger point
                    trigger_point = swing_finder(major_data, macdhistogram_signal=True).last_swing("ceiling")
            

            while in_trigger is False:
                data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
                data = data.df()

                if self.position_type == "short":
                    # Check if price make a new ceiling
                    new_ceiling = swing_finder(data, macdhistogram_signal=True).last_swing("ceiling")
                    if new_ceiling > last_ceiling:
                        last_ceiling = new_ceiling
                        # Check if price is in the faile point range
                        if data["close"][-2] > faile_point:
                            print("The price go up to the faile point and the analysis get failed")
                            in_trigger = False
                            self.botrun = False
                            break
                        else:
                            print("price make a new ceiling under the faile point")

                    # When price go under the trigger point, trigger activate
                    if data["close"][-2] < trigger_point:
                        print(f'Price activate trigger by {data["close"][-2]} price')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        in_trigger = True
                        return entry_point   
                    
                else:
                    # Check if price make a new floor
                    new_floor = swing_finder(data, macdhistogram_signal=True).last_swing("floor")
                    if new_floor < last_floor:
                        last_floor = new_floor
                        # Check if price is in the claster range
                        if data["close"][-2] < faile_point:
                            print("The price go down to the faile point and the analysis get failed")
                            self.botrun = False
                            in_trigger = False
                            break
                        else:
                           print("Price make a new floor over the faile point") 

                    # When price go above the trigger point, trigger activate
                    if data["close"][-2] > trigger_point:
                        print(f'Price activate trigger by {data["close"][-2]} price')
                        tick_info = mt5.symbol_info(self.symbol)
                        entry_point = tick_info.bid
                        in_trigger = True
                        return entry_point


    # This function automatically find stop loss by last swing or standard the input stop loss
    def sl(self, stop_loss=None):
        # If user doesen't enter the stop loss, bot find it automatically by the last floor and ceiling
        if stop_loss is None:
            data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
            data = data.df()
            # For short positions stop loss is last ceiling
            if self.position_type == "short":
                stop_loss = swing_finder(data, macdhistogram_signal=True).last_swing("ceiling")
            # For long positions stop loss is last floor
            else:
                stop_loss = swing_finder(data, macdhistogram_signal=True).last_swing("floor")

        # Add broker tolerance pip and spread on bid price in short positions
        spread = mt5.symbol_info(self.symbol).spread
        if self.position_type == "short":
           stop_loss = stop_loss + (10 * self.pip) + (spread * self.pip)
           
        else:
           stop_loss = stop_loss - (10 * self.pip) 

        return stop_loss
    

    # This function check whether the stop loss size is not too large according to the money of each position
    def max_sl_check(self, stop_loss, entry, pos_money):
        if pos_money:
            max_sl_pip = pos_money / (self.standard_lot * 0.01 *  self.pip * self.pip_value)
            sl_size = abs(stop_loss - entry)
            sl_pip = sl_size / self.pip

            # Check if stop loss is not too much big
            if sl_pip < max_sl_pip:
                print(f"Yor stop loss size is {sl_size} and it is lower than {max_sl_pip} that is maximum stop loss")
                return True
            else:
                print(f"Yor stop loss size is {sl_size} and it is bigger than {max_sl_pip} that is maximum stop loss")
                print("You can't take this position")
                return False

        else:
            print("For max sl check you should enter pos money")
            return None


    # This function is using to find out tp1 for diffrent strategies
    # You can fill B and C with D and E for miner strategy
    def tp1(self, tp_type=None, sl=None, entry=None, B=None, C=None, correction_start_point=None):
        if tp_type == "miner_fast" or tp_type == "miner_middle":
            # Check all parameter we need have entered
            if B and C and sl and entry:
                pass
            else:
                print("All the parameter that are needed to caclculate tp1 are not entered")
                return None

            # Check the strategy for find RR = 1 target for tp1
            if self.position_type == "short":
                if abs(B - C) * 0.5 >= abs(entry - sl):
                    tp_1 = C - (abs(B - C) * 0.5)
                elif abs(B - C) * 0.618 >= abs(entry - sl):
                    tp_1 = C - (abs(B - C) * 0.618)
                else:
                    tp_1 = C - (abs(B - C) * 0.786)
            else:
                if abs(B - C) * 0.5 >= abs(entry - sl):
                    tp_1 = C + (abs(B - C) * 0.5)
                elif abs(B - C) * 0.618 >= abs(entry - sl):
                    tp_1 = C + (abs(B - C) * 0.618)
                else:
                    tp_1 = C + (abs(B - C) * 0.786)

        if tp_type == "miner_slow":
            # Check all parameter we need have entered
            if correction_start_point and C and sl and entry:
                pass
            else:
                print("All the parameter that are needed to caclculate tp1 are not entered")
                return None

            # Check the strategy for find RR = 1 target for tp1
            if self.position_type == "short":
                if abs(correction_start_point - C) * 1.27 >= abs(entry - sl):
                    tp_1 = C - (abs(correction_start_point - C) * 1.27)
                else:
                    tp_1 = C - (abs(correction_start_point - C) * 1.618)

            else:
                if abs(correction_start_point - C) * 1.27 >= abs(entry - sl):
                    tp_1 = C + (abs(correction_start_point - C) * 1.27)
                
                else:
                    tp_1 = C + (abs(correction_start_point - C) * 1.618)

        return tp_1


    # This function is using to find out tp2 for diffrent strategies
    # You can fill C with E for miner strategy
    def tp2(self, tp_type=None, sl=None, entry=None, C=None, correction_start_point=None):
        # Check all parameter we need have entered
        if correction_start_point and C and sl and entry:
            pass
        else:
            print("All the parameter that are needed to caclculate tp2 are not entered")
            return None
        
        if tp_type == "miner_fast" or tp_type == "miner_middle":
            # Check the strategy for find RR = 3 target for tp2
            # tp2 is just set for fast and middle strategy
            if self.position_type == "short":
                if abs(correction_start_point - C) * 1.27 >= abs(entry - sl) * 3:
                    tp_2 = C - (abs(correction_start_point - C) * 1.27)
                else:
                    tp_2 = C - (abs(correction_start_point - C) * 1.618)

            else:
                if abs(correction_start_point - self.C) * 1.27 >= abs(entry - sl) * 3:
                    tp_2 = self.C + (abs(correction_start_point - C) * 1.27)
                
                else:
                    tp_2 = C + (abs(correction_start_point - C) * 1.618)

            return tp_2


    # Calculate the volume
    def volume(self, sl, entry, pos_money=None, RR=None, round_up=None):
        # Calculate the volume factor by the risk managment strategy 
        if RR is None:
            profit_factor = 1
        else:
            profit_factor = risk_management(RR).calculate()

        if pos_money is None:
            pos_money = self.pos_money

        # Calculate volume
        sl_size = abs(sl - entry)
        sl_pip = sl_size / self.pip
        pos_volume = (pos_money * profit_factor) / (self.standard_lot * self.pip * self.pip_value * sl_pip)

        if round_up is None:
            pos_volume = self.costum_round(pos_volume, 2, 7)
        else:
            pos_volume = self.costum_round(pos_volume, 2, round_up)

        return pos_volume
    

    # Candle trailing stop
    def candle_trailing(self, order_ticket):
        # Retrieve the order information
        order_info = mt5.order_get(ticket=order_ticket)

        # Check if the order exists
        if order_info == ():
            print(f"Order with ticket {order_ticket} not found.")
            print("Maybe it closed befor we remove tp for candle trailing stop.")
            return None
        else:
            order_info = order_info[0]
            
        # Check if the order has a take profit
        if order_info.tp > 0.0:
            # Set the take profit to 0.0 to remove it
            result = mt5.order_modify(
                ticket=order_ticket,
                tp=0.0
            )

            # Check the result
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Take profit removed successfully for order {order_ticket}")
            else:
                print(f"Removing take profit failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")

        while True:
            # Check if the order exists
            if order_info.order == 0:
                print(f"Order with ticket {order_ticket} not found. Candle trailing stop is finish.")
                return True

            data = datamine(self.timeframe, self.symbol, 'online', number_data=5)
            data = data.df()
            if self.position_type == "short":
                self.spread = mt5.symbol_info(self.symbol).spread
                new_sl = data["high"][-2] + (10 * self.pip) + self.spread
                # Set the new stop loss
                result = mt5.order_modify(
                    ticket=order_ticket,
                    sl=new_sl
                )
                # Check the result
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    print(f"Stop loss set to {new_sl} successfully for order {order_ticket}")
                else:
                    print(f"Setting stop loss failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")
                
            else:
                new_sl = data["low"][-2] - (10 * self.pip)
                # Set the new stop loss
                result = mt5.order_modify(
                    ticket=order_ticket,
                    sl=new_sl
                )
                # Check the result
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    print(f"Stop loss set to {new_sl} successfully for order {order_ticket}")
                else:
                    print(f"Setting stop loss failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")


    # Swing trailing stop
    def swing_trailing(self, order_ticket):
        # Retrieve the order information
        order_info = mt5.positions_get(ticket=order_ticket)
        
        # Check if order exist
        if order_info == ():
            print(f"Order with ticket {order_ticket} not found.")
            print("Maybe it closed befor we remove tp for swing trailing stop.")
        else:
            order_info = order_info[0]
            initial_sl = order_info.sl
             
        # Check if the order has a take profit
        if order_info.tp > 0.0:
            # Set the take profit to 0.0 to remove it
            result = mt5.order_modify(
                ticket=order_ticket,
                tp=0.0
            )

            # Check the result
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Take profit removed successfully for order {order_ticket}")
            else:
                print(f"Removing take profit failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")

        while True:
            # Retrieve the order information
            order_info = mt5.positions_get(ticket=order_ticket)
            # Check if the order exists
            if order_info.order == ():
                print(f"Order with ticket {order_ticket} not found. Swing trailing stop is finish.")
                return True
            
            data = datamine(self.minor_timeframe, self.symbol, 'online', number_data=10000)
            data = data.df()
            # Add swing list to the df
            data = swing_finder(data, macdhistogram_signal=True).Add_swinglist()
            
            if self.position_type == "short":
                # Find last confirm ceiling
                last_ceiling = swing_finder.last_swing("ceiling")
                # If last ceiling is under the last sl, we update the sl with it
                if initial_sl > last_ceiling:
                    self.spread = mt5.symbol_info(self.symbol).spread
                    new_sl = last_ceiling + (10 * self.pip) + self.spread
                    initial_sl = new_sl
                    # Set the new stop loss
                    result = mt5.order_modify(
                        ticket=order_ticket,
                        sl=new_sl
                    )
                    # Check the result
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        print(f"Stop loss set to {new_sl} successfully for order {order_ticket}")
                    else:
                        print(f"Setting stop loss failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")
                    
            else:
                # Find last confirm floor
                last_floor = swing_finder.last_swing("floor")
                # If last ceiling is under the last sl, we update the sl with it
                if initial_sl < last_floor:
                    self.spread = mt5.symbol_info(self.symbol).spread
                    new_sl = last_floor - (10 * self.pip)
                    initial_sl = new_sl
                    # Set the new stop loss
                    result = mt5.order_modify(
                        ticket=order_ticket,
                        sl=new_sl
                    )
                    # Check the result
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        print(f"Stop loss set to {new_sl} successfully for order {order_ticket}")
                    else:
                        print(f"Setting stop loss failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")


    # This method risk free the one part trget positions 
    # Note that your position should has sl
    def risk_free(self, order_ticket):
        pos_info = mt5.positions_get(ticket=int(order_ticket))
        pos_info = pos_info[0]
        if pos_info.sl != 0:
            sl = pos_info.sl
        else:
            print("Your position doesen't has sl. We can't riskfree this position")
            return None
        entry = pos_info.price_open

        riskfree_tp = entry + abs(sl - entry)
        # Wait for price to achive the RR = 1 take profit
        while True:
            data = datamine(self.timeframe, self.symbol, 'online', number_data=1000)
            data = data.df()
            if self.positon_type == "short":
                if data["close"][-2] <= riskfree_tp:
                    print("position reach RR = 1 target, now wait for make a ceiling")
                    break
            else:
                if data["close"][-2] >= riskfree_tp:
                    print("position reach RR = 1 target, now wait for make a floor")
                    break
            time.sleep(60)

        # Wait for price make a confirm floor or ceiling passed the tp
        while True:
            data = datamine(self.timeframe, self.symbol, 'online', number_data=10000)
            data = data.df()
            swing = swing_finder(data)
            if self.positon_type == "short":
                last_ceiling = swing.last_swing("ceiling")
                if last_ceiling <= riskfree_tp:
                    print("price make a new confirm ceiling under the risk free tp")
                    break
            else:
                last_floor = swing.last_swing("floor")
                if last_floor >= riskfree_tp:
                    print("price make a new confirm floor above the risk free tp")
                    break
            time.sleep(60)

        # Set new riskfree sl
        if self.position_type == "short":
            self.spread = mt5.symbol_info(self.symbol).spread
            new_sl = last_ceiling + (10 * self.pip) + self.spread
            # Set the new stop loss
            result = mt5.order_modify(
                ticket=order_ticket,
                sl=new_sl
            )
            # Check the result
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Stop loss set to {new_sl} successfully for order {order_ticket}")
                money_management().note_riskfree_pos(str(order_ticket))
                return True
            else:
                print(f"Setting stop loss failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")
                return False
        else:
            new_sl = last_floor - (10 * self.pip)
            # Set the new stop loss
            result = mt5.order_modify(
                ticket=order_ticket,
                sl=new_sl
            )
            # Check the result
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Stop loss set to {new_sl} successfully for order {order_ticket}")
                money_management().note_riskfree_pos(str(order_ticket))
                return True
            else:
                print(f"Setting stop loss failed for order {order_ticket}. Error code: {result.retcode}, Error description: {result.comment}")
                return False
        
        
    # This method take a number and round it as you specified by number_decimal and up_down_round
    def costum_round(self, number, number_decimal, up_down_round):
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
    
