from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *
from Risk_and_money_management import *
from auto_trade import *

"""
We use data[##][-2], because of that the last candle that metatrader give us doesen't fixed.

"""

    
class miner_strategy:
    def __init__(self,
                login,
                strategy_type, 
                timeframe, 
                mother_timeframe,
                minor_timeframe, 
                symbol, 
                correction_start_point, A, B, C=None,
                C_claster1=None, C_claster2=None, pip_tolerance=None, trigger_point=None,
                pos_percent=0.01, period_percent=0.03, period_time=60):
        
        self.login = login
        self.strategy_type = strategy_type  # Can be "fast", "middle", "slow"
        self.timeframe = timeframe 
        self.mother_timeframe = mother_timeframe
        self.minor_timeframe = minor_timeframe
        self.symbol = symbol
        self.correction_start_point = correction_start_point
        self.A = A
        self.B = B 
        self.pip_tolerance = pip_tolerance
        
        self.trigger = False
        self.trigger_point = trigger_point
        self.pos_percent = pos_percent
        self.period_percent = period_percent
        self.period_time = period_time
        self.tp1_target = False
        self.tp2_target = False
        self.candle_trailing_stop = False
        self.swing_trailing_stop = False
        self.pip = mt5.symbol_info(symbol).point

        if C is None and C_claster1 is None and C_claster2 is None:
            print("You should fill C or C clasters")

        if C is not None and (C_claster1 is not None or C_claster2 is not None):
            print("You should fill just one of the C or C clasters")
        
        if C is not None:
            self.C = C
            self.C_type = "C_point"
        
        if C_claster1 is not None and C_claster2 is not None:
            self.C_claster1 = C_claster1
            self.C_claster2 = C_claster2 
            self.C_type = "C_claster"

        if A > B:
            self.position_type = "short"
        else:
            self.position_type = "long"

        print("Position type:", self.position_type)

    
    def fast_strategy(self):
        self.entry_point = auto_trade().reach_trigger(self, "DToscilator", self.B, DTlist=[8, 5, 3, 3])

        # After the price reach trigger with DToscilator we calculate the position parameter 
        self.pos_sl = auto_trade().sl()
        self.pos_tp1 = auto_trade().tp1(self.pos_sl, self.entry_point)
        self.pos_tp2 = auto_trade().tp2(self.pos_sl, self.entry_point)
        self.pos_RR = (abs(self.pos_tp2 - self.entry_point)/abs(self.pos_sl - self.entry_point))
        self.pos_volume = auto_trade().volume(self.pos_sl, self.entry_point, RR=self.pos_RR)

        print("sl:", self.pos_sl, "\n", 
              "tp1:", self.pos_tp1, "\n", 
              "tp2:", self.pos_tp2, "\n", 
              "RR:", self.pos_RR, "\n",
              "volume:", self.pos_volume, "\n")
        
        # Opening position
        if self.position_type == "short":
            result_1 = self.login.open_sell_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp1, type_filling=0)
            result_2 = self.login.open_sell_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp2, type_filling=0)
        else:
            result_1 = self.login.open_buy_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp1, type_filling=0)
            result_2 = self.login.open_buy_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp2, type_filling=0)
        
        trade_request_1 = result_1.request
        trade_request_2 = result_2.request

        while (self.tp1_target is False
               or self.tp2_target is False
               or self.candle_trailing_stop is True
               or self.swing_trailing_stop is True):
            
            data = datamine(self.mother_timeframe, self.symbol, 'online', number_data=200)
            data = data.df()

            if self.position_type == "short":
                # Check if price is near tp1, if it is start candle trailing
                if data["low"][-1] < self.pos_tp1 + (10 * self.pip) and self.tp1_target is False:
                    self.tp1_target = True 
                    self.candle_trailing_stop = True
                
                # Check if price is near tp2
                if data["low"][-1] < self.pos_tp2 + (15 * self.pip) and self.tp2_target is False:
                    self.tp2_target = True 
                    self.swing_trailing_stop = True

                if self.candle_trailing_stop:
                    money_management().note_riskfree_pos(trade_request_1.ticket)
                    money_management().note_riskfree_pos(trade_request_2.ticket)
                    auto_trade.candle_trailing(trade_request_1.ticket)

                if self.swing_trailing_stop:
                    auto_trade.swing_trailing(trade_request_2.ticket)

            else:
                # Check if price is near tp1
                if data["high"][-1] > self.pos_tp1 - (10 * self.pip) and self.tp1_target is False:
                    self.tp1_target = True 
                    self.candle_trailing_stop = True

                # Check if price is near tp2
                if data["high"][-1] > self.pos_tp2 - (15 * self.pip) and self.tp2_target is False:
                    self.tp2_target = True 
                    self.swing_trailing_stop = True

                if self.candle_trailing_stop:
                    money_management().note_riskfree_pos(trade_request_1.ticket)
                    money_management().note_riskfree_pos(trade_request_2.ticket)
                    check_candle_trailing = auto_trade().candle_trailing(trade_request_1.ticket)
                    if check_candle_trailing:
                        self.candle_trailing_stop = False

                if self.swing_trailing_stop:
                    check_swing_trailing = auto_trade().swing_trailing(trade_request_2.ticket)
                    if check_swing_trailing:
                        check_swing_trailing = False
            time.sleep(60)


    def middle_strategy(self):
        self.entry_point = auto_trade.reach_trigger("minorswing", self.B)
    
        # After the price reach trigger with minor swing we calculate the position parameter
        self.pos_sl = auto_trade().sl()
        self.pos_tp1 = auto_trade().tp1(self.pos_sl, self.entry_point)
        self.pos_tp2 = auto_trade().tp2(self.pos_sl, self.entry_point)
        self.pos_RR = (abs(self.pos_tp2 - self.entry_point)/abs(self.pos_sl - self.entry_point))
        self.pos_volume = auto_trade().volume(self.pos_sl, self.entry_point, RR=self.pos_RR)

        print("sl:", self.pos_sl, "\n", 
              "tp1:", self.pos_tp1, "\n", 
              "tp2:", self.pos_tp2, "\n", 
              "RR:", self.pos_RR, "\n",
              "volume:", self.pos_volume)
        
        # Opening position
        if self.position_type == "short":
            result_1 = self.login.open_sell_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp1, type_filling=0)
            result_2 = self.login.open_sell_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp2, type_filling=0)
        else:
            result_1 = self.login.open_buy_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp1, type_filling=0)
            result_2 = self.login.open_buy_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp2, type_filling=0)

        trade_request_1 = result_1.request
        trade_request_2 = result_2.request

        while (self.tp1_target is False
               or self.tp2_target is False
               or self.candle_trailing_stop is True
               or self.swing_trailing_stop is True):
            
            data = datamine(self.mother_timeframe, self.symbol, 'online', number_data=200)
            data = data.df()

            if self.position_type == "short":
                # Check if price is near tp1, if it is start candle trailing
                if data["low"][-1] < self.pos_tp1 + (10 * self.pip) and self.tp1_target is False:
                    self.tp1_target = True 
                    self.candle_trailing_stop = True
                
                # Check if price is near tp2
                if data["low"][-1] < self.pos_tp2 + (15 * self.pip) and self.tp2_target is False:
                    self.tp2_target = True 
                    self.swing_trailing_stop = True

                if self.candle_trailing_stop:
                    money_management().note_riskfree_pos(trade_request_1.ticket)
                    money_management().note_riskfree_pos(trade_request_2.ticket)
                    auto_trade.candle_trailing(trade_request_1.ticket)

                if self.swing_trailing_stop:
                    auto_trade.swing_trailing(trade_request_2.ticket)

            else:
                # Check if price is near tp1
                if data["high"][-1] > self.pos_tp1 - (10 * self.pip) and self.tp1_target is False:
                    self.tp1_target = True 
                    self.candle_trailing_stop = True

                # Check if price is near tp2
                if data["high"][-1] > self.pos_tp2 - (15 * self.pip) and self.tp2_target is False:
                    self.tp2_target = True 
                    self.swing_trailing_stop = True

                if self.candle_trailing_stop:
                    money_management().note_riskfree_pos(trade_request_1.ticket)
                    money_management().note_riskfree_pos(trade_request_2.ticket)
                    check_candle_trailing = auto_trade().candle_trailing(trade_request_1.ticket)
                    if check_candle_trailing:
                        self.candle_trailing_stop = False

                if self.swing_trailing_stop:
                    check_swing_trailing = auto_trade().swing_trailing(trade_request_2.ticket)
                    if check_swing_trailing:
                        check_swing_trailing = False
            time.sleep(60)


    def slow_strategy(self):
        self.entry_point = auto_trade().reach_trigger("majorswing", self.B)

        self.pos_sl = auto_trade().sl()
        self.pos_tp1 = auto_trade().tp1(self.pos_sl, self.entry_point)
        # Because we don't have any tp2, we consider it equal 2 
        self.pos_RR = 2
        self.pos_volume = auto_trade().volume(self.pos_sl, self.entry_point, RR=self.pos_RR)

        print("sl:", self.pos_sl, "\n", 
              "tp1:", self.pos_tp1, "\n", 
              "tp2:", self.pos_tp2, "\n", 
              "RR:", self.pos_RR, "\n",
              "volume:", self.pos_volume)

        # Opening position
        if self.position_type == "short":
            result_1 = self.login.open_sell_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp1, type_filling=0)
            result_2 = self.login.open_sell_pos(self.symbol, self.pos_volume, self.pos_sl, type_filling=0)
        else:
            result_1 = self.login.open_buy_pos(self.symbol, self.pos_volume, self.pos_sl, self.pos_tp1, type_filling=0)
            result_2 = self.login.open_buy_pos(self.symbol, self.pos_volume, self.pos_sl, type_filling=0)

        trade_request_1 = result_1.request
        trade_request_2 = result_2.request

        while (self.tp1_target is False
               or self.candle_trailing_stop is True
               or self.swing_trailing_stop is True):
            
            data = datamine(self.mother_timeframe, self.symbol, 'online', number_data=200)
            data = data.df()

            if self.position_type == "short":
                # Check if price is near tp1, if it is start candle trailing
                if data["low"][-1] < self.pos_tp1 + (10 * self.pip) and self.tp1_target is False:
                    self.tp1_target = True 
                    self.candle_trailing_stop = True
                

                if self.candle_trailing_stop:
                    money_management().note_riskfree_pos(trade_request_1.ticket)
                    money_management().note_riskfree_pos(trade_request_2.ticket)
                    auto_trade.candle_trailing(trade_request_1.ticket)

                if self.swing_trailing_stop:
                    auto_trade.swing_trailing(trade_request_2.ticket)

            else:
                # Check if price is near tp1
                if data["high"][-1] > self.pos_tp1 - (10 * self.pip) and self.tp1_target is False:
                    self.tp1_target = True 
                    self.candle_trailing_stop = True

                if self.candle_trailing_stop:
                    money_management().note_riskfree_pos(trade_request_1.ticket)
                    money_management().note_riskfree_pos(trade_request_2.ticket)
                    check_candle_trailing = auto_trade().candle_trailing(trade_request_1.ticket)
                    if check_candle_trailing:
                        self.candle_trailing_stop = False

                if self.swing_trailing_stop:
                    check_swing_trailing = auto_trade().swing_trailing(trade_request_2.ticket)
                    if check_swing_trailing:
                        check_swing_trailing = False
            time.sleep(60)


    def check_momentum(self, DT_timeframe, DTlist=[8, 5, 3, 3]):
        data = datamine(DT_timeframe, self.symbol, 'online', number_data=1000)
        data = data.df()

        # Add dt oscilator and it's signal to the df
        data = indicator.dt_oscillator(data, lengthRSI=DTlist[0], lengthStoch=DTlist[1], smoothK=DTlist[2], smoothD=DTlist[3])

        if self.position_type == "short":
            if (data["DToscilator_signal"][-2] == "Bull OB" 
                or data["DToscilator_signal"][-2] == "Bearish"
                or data["DToscilator_signal"][-2] == "Bear Rev"
                or data["DToscilator_signal"][-2] == "Bear Rev in OB"):
                return True
                
            else:
                print("Your position is against the mother time frame momentum")
                return False

        else:
            if (data["DToscilator_signal"][-2] == "Bear OS" 
                or data["DToscilator_signal"][-2] == "Bullish"
                or data["DToscilator_signal"][-2] == "Bull Rev"
                or data["DToscilator_signal"][-2] == "Bull Rev in OS"):
                return True
            else:
                print("Your position is against the mother time frame momentum")
                return False


    def auto_run(self, claster1, claster2):
        #try:
            while True:
                # Check if we can open position due to money management strategy
                moneymanagement = money_management().check_money_management(self.pos_percent, 
                                                                        self.period_percent, 
                                                                        period_seconds=self.period_time)
                if moneymanagement is False:
                    break
                
                # Check if the mother time frame momentum is in the same direction of position
                momentum = self.check_momentum(self.mother_timeframe)
                if momentum is False:
                    break
      
                # For the time that user give the C_clasters and C point doesen't made we should wait 
                if self.C_type == "C_claster":
                    # Check that if price reached the claster
                    reach = auto_trade.reach_claster(claster1, claster2, self.B, self.pip_tolerance)
                    if reach is False:
                        break
                    
                # After the price reach the claster or we have the exact price of C point, we wait for trigger 
                # Fast strategy
                if self.strategy_type == "fast":
                    self.fast_strategy()
                    break
                    
                # Middle strategy (broke minor swing high and low)
                # User can enter the trigger point manually or bot find the last minor swing automatically 
                elif self.strategy_type == "middel":
                    self.middle_strategy()
                    break
                # Slow strategy
                else:
                    self.slow_strategy()
                    break
                    
            money_management().check_exist_riskfree_pos()    
        # Press ctrl + c to stop  trading        
        #except KeyboardInterrupt:
        #    print('-------------------------------program stoped-----------------------------')
        #    pass 

        #except Exception as e:
        #    print("The program has stopped due to an error:", e)
        #    telegram_send_message(f"The program for symbol {symbol} has stopped due to an error{str(e)}")



"""
login = metatrader(51735591, 'Wy7v5r4hu', 'Alpari-MT5-Demo')
login.start_mt5()

data = datamine('1d', 'EURUSD','online', number_data=1000)
data = data.df()

data = swing_finder(data, macdhistogram_signal=True).Add_swinglist()
print(data.tail(50))


#print(indicator.dt_oscillator(data, lengthRSI=8, lengthStoch=5, smoothK=3, smoothD=3).tail(50))
"""

#miner_strategy("fast", "1m", "1h", "EURUSD", 1.09080, 1.09040, 1.09080, C_claster1=1.09036, C_claster2=1.09017).auto_trade()






