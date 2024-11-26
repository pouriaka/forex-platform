from Metatrader import *
from Datamine import *
from TechnicalTools import *

import numpy as np
import matplotlib.pyplot as plt 
import re

# You can have just buy or sell strategy and test it, also for one side market you can write just buy strategy 
class backtest:
    def __init__(self, df, spread, open_buy_condition=None, close_buy_condition=None, open_sell_condition=None, close_sell_condition=None):
        self.df = df 
        self.spread = spread

        # This variables are use in trading algoritm for simulat waite for next price, buy or sell price and hold a position
        self.moving_in_df = 0
        self.moving_in_df_buyorsell = 0
        self.moving_in_df_in_position = 0

        # For making the condition str
        self.moving_in_df_str = "self.moving_in_df"
        self.moving_in_df_in_position_str = "self.moving_in_df_in_position"

        if open_buy_condition is not None and close_buy_condition is not None:
            self.open_buy = self.modify_condition_string(open_buy_condition, self.moving_in_df_str)
            self.close_buy = self.modify_condition_string(close_buy_condition, self.moving_in_df_in_position_str)

        if open_sell_condition is not None and close_sell_condition is not None:
            self.open_sell = self.modify_condition_string(open_sell_condition, self.moving_in_df_str)
            self.close_sell = self.modify_condition_string(close_sell_condition, self.moving_in_df_in_position_str)

        if open_buy_condition is None and open_sell_condition is None:
            print("You should fill one of the buy or sell condition for backtesting")


        
    # This method convert the condition string like "df['...'] > 70 to df['...'][n] > 70"
    @staticmethod
    def modify_condition_string(input_string, n):
        def replace(match):
            return match.group(0) + f"[{n}]"
        
        modified_string = re.sub(r"df\['[^']+'\]", replace, input_string)

        return modified_string
    
    
    def trading(self):
        
        equity_list = []
        equity = 0
        back_to_back_fail_list = []
        back_to_back_fail_counter = 0
        corect_conter = 0
        fail_counter = 0

        # np.nan for calibration
        open_buy_points = [np.nan]
        close_buy_points = [np.nan]
        open_sell_points = [np.nan]
        close_sell_points = [np.nan]

        # mpf ploting data for buy or sell points.We put zero for calibration
        # We use the second list for find out the buy or sell position to write data downside or upside
        self.mpf_ploting_data = [[0],[0]]
    
        #mpf equity
        equity_mpf = [0]

        while self.moving_in_df <= (len(self.df)) - 1:

            # Sell position opening condition   
            if eval(self.open_sell):
                print('open new pos----------------------------------------------')
                self.moving_in_df_buyorsell = self.moving_in_df
                self.moving_in_df_in_position = self.moving_in_df

                #mpf collecting point
                open_sell_points = open_sell_points[:-1]
                close_sell_points = close_sell_points[:-1]
                open_buy_points = open_buy_points[:-1]
                close_buy_points = close_buy_points[:-1]
                
                open_sell_points.append(self.df['high'][self.moving_in_df_buyorsell] + 0.0002)
                close_sell_points.append(np.nan)
                open_buy_points.append(np.nan)
                close_buy_points.append(np.nan)

                self.mpf_ploting_data[0] = self.mpf_ploting_data[0][:-1]
                self.mpf_ploting_data[1] = self.mpf_ploting_data[1][:-1]
                self.mpf_ploting_data[0].append(self.df['high'][self.moving_in_df_buyorsell])
                self.mpf_ploting_data[1].append(1)
                
                
                # Sell position closing condition 
                while eval(self.close_sell) and self.moving_in_df_in_position < len(self.df) - 2:    
                    
                    self.moving_in_df_in_position += 1

                    open_sell_points.append(np.nan)
                    close_sell_points.append(np.nan)
                    open_buy_points.append(np.nan)
                    close_buy_points.append(np.nan)

                    self.mpf_ploting_data[0].append(0)
                    self.mpf_ploting_data[1].append(0)
                    
                    equity_mpf.append(equity_mpf[-1])
                    
                # Close position 
                equity += ((self.df['close'][self.moving_in_df_buyorsell] - self.df['close'][self.moving_in_df_in_position])) - self.spread
                equity_list.append(equity)

                # mpf collecting point
                open_sell_points = open_sell_points[:-1]
                close_sell_points = close_sell_points[:-1]
                open_buy_points = open_buy_points[:-1]
                close_buy_points = close_buy_points[:-1]

                equity_mpf = equity_mpf[:-1]

                open_sell_points.append(np.nan)
                close_sell_points.append(self.df['high'][self.moving_in_df_in_position] + 0.0002)
                open_buy_points.append(np.nan)
                close_buy_points.append(np.nan)

                self.mpf_ploting_data[0] = self.mpf_ploting_data[0][:-1]
                self.mpf_ploting_data[1] = self.mpf_ploting_data[1][:-1]
                self.mpf_ploting_data[0].append(self.df['high'][self.moving_in_df_in_position])
                self.mpf_ploting_data[1].append(1)
                equity_mpf.append(equity)
                
                print('selling----')
                print('buysel_p',self.df['close'][self.moving_in_df_buyorsell])
                print('peimaiesh_p', self.df['close'][self.moving_in_df_in_position])

                self.moving_in_df = self.moving_in_df_in_position + 1

                open_sell_points.append(np.nan)
                close_sell_points.append(np.nan)
                open_buy_points.append(np.nan)
                close_buy_points.append(np.nan)
                
                self.mpf_ploting_data[0].append(0)
                self.mpf_ploting_data[1].append(0)
                equity_mpf.append(equity_mpf[-1])

                if equity >= 0 :
                    corect_conter += 1
                    back_to_back_fail_counter = 0
                          
                else:
                    fail_counter += 1
                    back_to_back_fail_counter += 1
                    
                back_to_back_fail_list.append(back_to_back_fail_counter)   
                    

            # Buy position opening condition         
            elif eval(self.open_buy):

                print('open new pos----------------------------------------------')
                self.moving_in_df_buyorsell = self.moving_in_df
                self.moving_in_df_in_position = self.moving_in_df
                

                #mpf collecting point
                open_sell_points = open_sell_points[:-1]
                close_sell_points = close_sell_points[:-1]
                open_buy_points = open_buy_points[:-1]
                close_buy_points = close_buy_points[:-1]

                open_sell_points.append(np.nan)
                close_sell_points.append(np.nan)
                open_buy_points.append(self.df['low'][self.moving_in_df_buyorsell] - 0.0002)
                close_buy_points.append(np.nan)

                self.mpf_ploting_data[0] = self.mpf_ploting_data[0][:-1]
                self.mpf_ploting_data[1] = self.mpf_ploting_data[1][:-1]
                self.mpf_ploting_data[0].append(self.df['low'][self.moving_in_df_buyorsell])
                self.mpf_ploting_data[1].append(-1)
                        
                # Buy position closing condition
                while eval(self.close_buy) and self.moving_in_df_in_position < len(self.df) - 2:     
                    
                    self.moving_in_df_in_position += 1

                    open_sell_points.append(np.nan)
                    close_sell_points.append(np.nan)
                    open_buy_points.append(np.nan)
                    close_buy_points.append(np.nan)

                    self.mpf_ploting_data[0].append(0)
                    self.mpf_ploting_data[1].append(0)

                    equity_mpf.append(equity_mpf[-1])
                    
                # Close position 
                equity += ((self.df['close'][self.moving_in_df_in_position] - self.df['close'][self.moving_in_df_buyorsell])) - self.spread
                equity_list.append(equity)

                # mpf collecting point
                open_sell_points = open_sell_points[:-1]
                close_sell_points = close_sell_points[:-1]
                open_buy_points = open_buy_points[:-1]
                close_buy_points = close_buy_points[:-1]

                equity_mpf = equity_mpf[:-1]
                
                open_sell_points.append(np.nan)
                close_sell_points.append(np.nan)
                open_buy_points.append(np.nan)
                close_buy_points.append(self.df['low'][self.moving_in_df_in_position] - 0.0002)

                self.mpf_ploting_data[0] = self.mpf_ploting_data[0][:-1]
                self.mpf_ploting_data[1] = self.mpf_ploting_data[1][:-1]
                self.mpf_ploting_data[0].append(self.df['low'][self.moving_in_df_in_position])
                self.mpf_ploting_data[1].append(-1)
                equity_mpf.append(equity)
                
                print('buying----')
                print('buysel_p', self.df['close'][self.moving_in_df_buyorsell])
                print('peimaiesh_p', self.df['close'][self.moving_in_df_in_position])

                self.moving_in_df = self.moving_in_df_in_position + 1

                open_sell_points.append(np.nan)
                close_sell_points.append(np.nan)
                open_buy_points.append(np.nan)
                close_buy_points.append(np.nan)

                self.mpf_ploting_data[0].append(0)
                self.mpf_ploting_data[1].append(0)
                equity_mpf.append(equity_mpf[-1])

                if equity >= 0 :
                    corect_conter += 1
                    back_to_back_fail_counter = 0
                    
                else:
                    fail_counter += 1
                    back_to_back_fail_counter += 1 
                    
                back_to_back_fail_list.append(back_to_back_fail_counter)    
            

            else:
                #when we don't have signal and we are not in position just move to next price
                self.moving_in_df += 1

                open_sell_points.append(np.nan)
                close_sell_points.append(np.nan)
                open_buy_points.append(np.nan)
                close_buy_points.append(np.nan)

                self.mpf_ploting_data[0].append(0)
                self.mpf_ploting_data[1].append(0)
                equity_mpf.append(equity_mpf[-1])
                
                    

        sum_sum = 0
        sum_pluse_sum = 0
        sum_mines_sum = 0
        pluse = 0
        mines = 0
        for i in range(len(equity_list)-2):
            sum_dev = abs(equity_list[i] - equity_list[i+1])
            sum_sum = sum_dev + sum_sum
            if equity_list[i] - equity_list[i+1] <= 0:
                sum_pluse_dev = abs(equity_list[i] - equity_list[i+1])
                sum_pluse_sum = sum_dev + sum_pluse_sum
                pluse += 1
            else:
                sum_pluse_dev = abs(equity_list[i] - equity_list[i+1])
                sum_mines_sum = sum_dev + sum_mines_sum
                mines += 1



        minimom = min(equity_list)
        print('min of equity',min(equity_list))
        print('meghdar miangin taghirat', sum_sum/len(equity_list))
        print('meghdar miangin taghirat mosbat', sum_pluse_sum/pluse)
        print('meghdar miangin taghirat manfi', sum_mines_sum/mines)
        print('corect count', corect_conter)
        print('fail count', fail_counter)
        print('percent of corect cont',(corect_conter/(corect_conter + fail_counter)*100))
        print('max back to back fail', max(back_to_back_fail_list))


        plt.plot(equity_list, color="black", label = 'equity')

        plt.show()


        # Calibrating point with removing the endest eleman
        open_sell_points = open_sell_points[:-1]
        close_sell_points = close_sell_points[:-1]
        open_buy_points = open_buy_points[:-1]
        close_buy_points = close_buy_points[:-1]

        self.mpf_ploting_data[0] = self.mpf_ploting_data[0][:-1]
        self.mpf_ploting_data[1] = self.mpf_ploting_data[1][:-1]
        equity_mpf = equity_mpf[:-1]


        self.df['open_sell_points'] = open_sell_points
        self.df['close_sell_points'] = close_sell_points
        self.df['open_buy_points'] = open_buy_points
        self.df['close_buy_points'] = close_buy_points
        
        self.df['equity'] = equity_mpf

        
        return self.df
    
    def return_mpf_ploting_data(self):
        return self.mpf_ploting_data
    
    def return_df(self):
        return self.df
           


