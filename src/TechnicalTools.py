from Metatrader import *
from Datamine import *

import pandas_ta as ta
import pandas as pd
import numpy as np
import talib
import decimal


"""
 This code methods contains some of technical analysis tools that 
 can add indicators numbers to df.

 It also can contains any other technical analysis tools like price
 action tools for example candlesticks pattern and pivot points.

 In order to be able to categorize between technical tools in ploting, 
 at beginning of the names of the columns we use some things like 'ind_', 'cdl_', 'piv_'
 that refers to indicator, candlesticks, pivot.

"""

class indicator:
    def __init__(self):
        pass
    

    @staticmethod
    def rsi(df, length):
        #calculate rsi and add it to df
        rsi =  ta.rsi(df['close'], length=length) 
        df[f'ind_rsi{length}'] = pd.DataFrame(rsi)


        return df
    
    
    @staticmethod
    def sma(df, length):
        sma = ta.sma(df['close'], length=length)
        df[f'ind_sma{length}'] = pd.DataFrame(sma)


        return df
    
    
    @staticmethod
    def ema(df, length):
        ema = ta.ema(df['close'], length=length)
        df[f'ind_ema{length}'] = pd.DataFrame(ema)


        return df
    
    
    @staticmethod
    def adx(df, length):
        adx = ta.adx(high=df['high'], low=df['low'], close=df['close'], length=length)
        df = pd.concat([df, adx], axis=1)
        #change the column name to lower case
        df.rename(columns={f'ADX_{length}': f'ind_adx_{length}'}, inplace=True)
        df.rename(columns={f'DMP_{length}': f'ind_dmp_{length}'}, inplace=True)
        df.rename(columns={f'DMN_{length}': f'ind_dmn_{length}'}, inplace=True)


        return df
    

    @staticmethod
    def macd(df, fast=12, slow=26, signal=9):
        macd = ta.macd(close=df['close'], fast=fast, slow=slow, signal=signal)
        df = pd.concat([df, macd], axis=1)

        #change the column name to lower case
        df.rename(columns={f'MACD_{fast}_{slow}_{signal}': f'ind_macd_{fast}_{slow}_{signal}'}, inplace=True)
        df.rename(columns={f'MACDh_{fast}_{slow}_{signal}': f'ind_macdh_{fast}_{slow}_{signal}'}, inplace=True)
        df.rename(columns={f'MACDs_{fast}_{slow}_{signal}': f'ind_macds_{fast}_{slow}_{signal}'}, inplace=True)
        

        return df
    
    @staticmethod
    def macd_histogram(df, fast=12, slow=26, signal=9):

        macd = ta.macd(close=df['close'], fast=fast, slow=slow, signal=signal)
        df = pd.concat([df, macd], axis=1)

        #change the column name to lower case
        df.rename(columns={f'MACD_{fast}_{slow}_{signal}': f'ind_macd_{fast}_{slow}_{signal}'}, inplace=True)
        df.rename(columns={f'MACDh_{fast}_{slow}_{signal}': f'ind_macdh_{fast}_{slow}_{signal}'}, inplace=True)
        df.rename(columns={f'MACDs_{fast}_{slow}_{signal}': f'ind_macds_{fast}_{slow}_{signal}'}, inplace=True)

        df.drop([f'ind_macdh_{fast}_{slow}_{signal}', f'ind_macds_{fast}_{slow}_{signal}'], axis=1, inplace=True)
        

        return df
    
    
    @staticmethod
    def atr(df, length):
        atr = ta.atr(high=df['high'], low=df['low'], close=df['close'], length=length)
        
        #df[f'ind_atr{length}'] = pd.DataFrame(atr)
        df = pd.concat([df, atr], axis=1)

        #change the column name to lower case
        df.rename(columns={f'ATRr_{length}': f'atr_{length}'}, inplace=True)

        return df
    

    @staticmethod
    def stoch(df, length):
        # Calculate the lowest low and highest high over the specified length
        df['lowest_low'] = df['low'].rolling(window=length).min()
        df['highest_high'] = df['high'].rolling(window=length).max()

        # Calculate the Stochastic indicator
        df['stoch'] = 100 * (df['close'] - df['lowest_low']) / (df['highest_high'] - df['lowest_low'])

        # Drop the temporary columns used for calculations
        df.drop(['lowest_low', 'highest_high'], axis=1, inplace=True)

        return df
    

    @staticmethod
    def stoch_rsi(df, length_stoch):
        # Calculate the lowest RSI and highest RSI over the specified length
        df['lowest_rsi'] = df['rsi'].rolling(window=length_stoch).min()
        df['highest_rsi'] = df['rsi'].rolling(window=length_stoch).max()

        # Calculate the Stochastic RSI
        df['stoch_rsi'] = 100 * (df['rsi'] - df['lowest_rsi']) / (df['highest_rsi'] - df['lowest_rsi'])

        # Drop the temporary columns used for calculations
        df.drop(['lowest_rsi', 'highest_rsi'], axis=1, inplace=True)

        return df


    #DT oscilator use with these periods  8,5,3,3   13,8,5,5   21,13,8,8   34,21,13,13
    @staticmethod
    def dt_oscillator(df, lengthRSI=8, lengthStoch=5, smoothK=3, smoothD=3, signal=True):
        # Calculate RSI
        df['rsi'] = ta.rsi(df['close'], lengthRSI)

        # Calculate Stochastics RSI
        indicator.stoch_rsi(df, lengthStoch)

        # Smooth Stochastics RSI
        df['k'] = ta.sma(df['stoch_rsi'],length=smoothK)

        # Smooth K values to get D
        df['d'] = ta.sma(df['k'], length=smoothD)

        # Drop the temporary columns used for calculations
        df.drop(['rsi', 'stoch_rsi'], axis=1, inplace=True)

        if signal:
            indicator.DToscilator_signal(df)

        return df
    

    # This method is use to find out that DT oscilator signals according to miner strategy
    @staticmethod
    def DToscilator_signal(df):
        
        price_number = 0
        signal_list = []
        signal_list_2 = [None]

        while price_number < (len(df)):
            if df['k'][price_number] < df['d'][price_number]:
                signal_list.append(-1)
            elif df['k'][price_number] > df['d'][price_number]:
                signal_list.append(1)
            elif pd.isna(df['d'][price_number]):
                signal_list.append(None)
            
            price_number += 1
        
        if len(signal_list) < len(df):
            signal_list.insert(0, None)


        price_number = 0   
        while price_number < (len(signal_list) - 1):
            try:
                # When no revers happen
                if signal_list[price_number] == signal_list[price_number+1] and signal_list[price_number] != None:
                    if signal_list[price_number] == 1:
                        if df['k'][price_number] > 75 and df['d'][price_number] > 75:
                            signal_list_2.append("Bull OB")
                        else:
                            signal_list_2.append("Bullish")
                    else:
                        if df['k'][price_number] < 25 and df['d'][price_number] < 25:
                            signal_list_2.append("Bear OS")
                        else:
                            signal_list_2.append("Bearish")

                # Bearish reversal   
                elif signal_list[price_number] != signal_list[price_number+1] and signal_list[price_number] == 1 :
                    
                    if  df['k'][price_number] > 75 and df['d'][price_number] > 75:
                        signal_list_2.append("Bear Rev in OB")
                    else:
                        signal_list_2.append("Bear Rev")

                # Bullish reversal 
                elif signal_list[price_number] != signal_list[price_number+1] and signal_list[price_number] == -1:
                      
                    if  df['k'][price_number] < 25 and df['d'][price_number] < 25:
                        signal_list_2.append("Bull Rev in OS")
                    else:
                        signal_list_2.append("Bull Rev")

                #for None element   
                else:
                    signal_list_2.append(None)

                price_number += 1

            except IndexError:
                break
        
        df['DToscilator_signal'] = signal_list_2
        
     

class swing_finder:
    def __init__(self, df, macd_fast=12, macd_slow=26, 
                 macdhistogram_signal=False, 
                 remove_price_minor_swings=False,
                 remove_price_and_time_minor_swings=False, 
                 wave_number_candles=False):
        
        self.df = df
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow

        # You can remove macd histogram +1 and -1 signal if you don't need it
        self.macdhistogram_signal = macdhistogram_signal

        # You can remove minor swings that has less than 38% correction of last wave price or time when put this True
        self.remove_price_minor_swings = remove_price_minor_swings
        self.remove_price_and_time_minor_swings = remove_price_and_time_minor_swings 

        # You can remove wave candle column , this column showes each wave has how many candles 
        self.wave_number_candles = wave_number_candles
        

    def Add_swinglist(self):
        self.df = indicator.macd(self.df, fast=self.macd_fast, slow=self.macd_slow)
        price_number = 0
        signal_list = []
        

        while price_number < (len(self.df)):
            if self.df[f'ind_macd_{self.macd_fast}_{self.macd_slow}_9'][price_number] < 0:
                signal_list.append(-1)
            elif self.df[f'ind_macd_{self.macd_fast}_{self.macd_slow}_9'][price_number] > 0:
                signal_list.append(1)
            elif pd.isna(self.df[f'ind_macd_{self.macd_fast}_{self.macd_slow}_9'][price_number]):
                signal_list.append(None)
            
            price_number += 1
        
        if len(signal_list) < len(self.df):
            signal_list.insert(0, None)

        # Drop the temporary columns used for calculations
        self.df.drop([f'ind_macdh_{self.macd_fast}_{self.macd_slow}_9', f'ind_macds_{self.macd_fast}_{self.macd_slow}_9'], axis=1, inplace=True)
        self.df["macd signal"] = signal_list
        
        self.split_df_by_macd_signal()

        for any_df in self.sep_df_list:
            if any_df["macd signal"][0] == 0:
                self.make_nan_column(any_df)
            
            elif any_df["macd signal"][0] == 1:
                self.find_highesthigh(any_df)

            elif any_df["macd signal"][0] == -1: 
                self.find_lowestlow(any_df)
        
        self.df.reset_index(inplace=True)
        self.df = pd.concat(self.sep_df_list)
        self.df.loc[self.df['swing'].isnull(),'swing'] = 0


        # Remove the minor swings if user don't want them
        if self.remove_price_minor_swings or self.remove_price_and_time_minor_swings:
            self.delet_minor_swing()

        # Remove the number of each wave candles if user don't want them
        if self.wave_number_candles is False:
            self.df.drop(['wave candles'], axis=1, inplace=True)

        # Remove the macd signal from df list if user don't want it
        if self.macdhistogram_signal is False:
            self.df.drop(['macd signal'], axis=1, inplace=True)

        
        return self.df
       

    # In this function, we seprate the df to each part that macd histogram has cross to x axis
    def split_df_by_macd_signal(self):
        self.sep_df_list = []
        sep_i = 0
        self.df.loc[self.df['macd signal'].isnull(),'macd signal'] = 0
        
        for i in range(len(self.df)-1):
            if self.df["macd signal"][i] != self.df["macd signal"][i+1]:
                sep_df = self.df.iloc[sep_i:i+1, :]
                self.sep_df_list.append(sep_df)
                sep_i = i+1

        sep_df = self.df.iloc[sep_i:len(self.df), :]
        self.sep_df_list.append(sep_df)
        

    # Find the highest price for the time macd signal is 1 and we have a ceiling
    def find_highesthigh(self, df):
        high_list = df["high"].tolist()
        high_list_nanother = []
        wave_number_candles = []
        max_value = max(high_list)
        df_number_candles = len(df)

        for price in high_list:
            if price == max_value:
                high_list_nanother.append(max_value)
                
            else:
                high_list_nanother.append(None)
                
            wave_number_candles.append(df_number_candles)
            

        df["swing"] = high_list_nanother
        df["wave candles"] = wave_number_candles


    # Find the lowest price for the time macd signal is -1 and we have floor
    def find_lowestlow(self, df):
        low_list = df["low"].tolist()
        low_list_nanother = []
        wave_number_candles = []
        min_value = min(low_list)
        df_number_candles = len(df)
        for price in low_list:
            if price == min_value:
                low_list_nanother.append(min_value)

            else:
                low_list_nanother.append(None)
            
            wave_number_candles.append(df_number_candles)

        df["swing"] = low_list_nanother
        df["wave candles"] = wave_number_candles
        
    
    # Add none column to the swing column for when macd signal is 0, and we don't have any ceiling or floor
    def make_nan_column(self, df):
        nan_list = df["low"].tolist()
        all_nan_list = []
        wave_number_candles = []
        df_number_candles = len(df)
        for price in nan_list:
            all_nan_list.append(None)
            wave_number_candles.append(df_number_candles)

        df["swing"] = all_nan_list
        df["wave candles"] = wave_number_candles
        

    # Delet the minor swings frome df swing column
    def delet_minor_swing(self):
        df = self.df
        swing_list = df["swing"].tolist()
        wave_candles_list = df["wave candles"].tolist()
        ceilingfloor = []
        wave_candles = [] # We make this list for checking the 34% time correction
        minor_ceilingfloor = []

        # We shold check from end to first
        counter = len(swing_list) - 1
        while counter > 0:
            if swing_list[counter] != 0:
               ceilingfloor.append(swing_list[counter])
               wave_candles.append(wave_candles_list[counter])
            
            counter -= 1

        counter = len(ceilingfloor) -1 
        while counter > 0:
            # If the wave can't correct the 0.38 percent of last wave in time or price, it is a minor wave
            wave_price_correction = (decimal.Decimal(abs(ceilingfloor[counter] - ceilingfloor[counter-1]))/
                                    decimal.Decimal(abs(ceilingfloor[counter-1] - ceilingfloor[counter-2])))
            
            wave_time_correction = (decimal.Decimal(abs(wave_candles[counter]))/
                                    decimal.Decimal(abs(wave_candles[counter-1])))
            

            if self.remove_price_and_time_minor_swings:
                # If a wave is time major or price major we pass, else it is a minor wave
                if wave_price_correction >= 0.38 or wave_time_correction >= 0.38:
                    pass
                else:
                    minor_ceilingfloor.append(ceilingfloor[counter])
                    minor_ceilingfloor.append(ceilingfloor[counter-1])
                    

            elif self.remove_price_minor_swings:
                # If a wave is price major we pass, else it is a minor wave
                if wave_price_correction >= 0.38:
                    pass
                else:
                    minor_ceilingfloor.append(ceilingfloor[counter])
                    minor_ceilingfloor.append(ceilingfloor[counter-1])
                    
                
            counter -= 1

        # Chang the minor ceiling and floor to zero
        for price in minor_ceilingfloor:
            for i in range(len(df)):
                if df["swing"][i] == price:
                    df["swing"][i] = 0


    # Find last swing or last ceiling, floor
    def last_swing(self, type_swing=None, confirm=True, minor_filter=False):
        data = self.df

        if minor_filter:
            # Add swing list to the df
            data = swing_finder(data, macdhistogram_signal=True, remove_price_minor_swings=True).Add_swinglist()
        else:
            # Add swing list to the df
            data = swing_finder(data, macdhistogram_signal=True).Add_swinglist()

        if type_swing == "ceiling":
            # Find last ceiling
            counter = len(data) - 1
            while counter > 0:
                if data.iloc[counter]["swing"] != 0 and data.iloc[counter]["macd signal"] == 1:
                    print("last ceiling the bot find is:", data.iloc[counter]["swing"])
                    last_ceiling = data.iloc[counter]["swing"]
                    break  
                counter -= 1

            if confirm:
                # Find last floor
                counter = len(data) - 1
                while counter > 0:
                    if data.iloc[counter]["swing"] != 0 and data.iloc[counter]["macd signal"] == -1:
                        print("last minor swing the bot find is:", data.iloc[counter]["swing"])
                        last_floor = data.iloc[counter]["swing"]
                    counter -= 1

                if data["close"][-2] <= last_floor:
                    return last_ceiling
                # If ceiling doesen't confirm, it return the previous ceiling
                else:
                    # Find last previous ceiling
                    counter = len(data) - 1
                    last_ceiling_count = 0
                    while counter > 0 and last_ceiling_count <= 2:
                        if data.iloc[counter]["swing"] != 0 and data.iloc[counter]["macd signal"] == 1:
                            last_ceiling = data.iloc[counter]["swing"]
                            last_ceiling_count += 1
                        counter -= 1
                    print("last confirm ceiling the bot find is:", last_ceiling)
                    return last_ceiling
            else:
                return last_ceiling
        
        elif type_swing == "floor":
            # Find last floor
            counter = len(data) - 1
            while counter > 0:
                if data.iloc[counter]["swing"] != 0 and data.iloc[counter]["macd signal"] == -1:
                    print("last minor swing the bot find is:", data.iloc[counter]["swing"])
                    last_floor = data.iloc[counter]["swing"]
                    break  
                counter -= 1

            if confirm:
                # Find last ceiling
                counter = len(data) - 1
                while counter > 0:
                    if data.iloc[counter]["swing"] != 0 and data.iloc[counter]["macd signal"] == 1:
                        print("last ceiling the bot find is:", data.iloc[counter]["swing"])
                        last_ceiling = data.iloc[counter]["swing"]
                        break  
                    counter -= 1

                if data["close"][-2] >= last_ceiling:
                    return last_floor
                # If floor doesen't confirm, it return the previous floor
                else:
                    # Find last previous floor
                    counter = len(data) - 1
                    last_floor_count = 0
                    while counter > 0 and last_floor_count <= 2:
                        if data.iloc[counter]["swing"] != 0 and data.iloc[counter]["macd signal"] == -1:
                            last_floor = data.iloc[counter]["swing"]
                            last_floor_count += 1 
                        counter -= 1
                    print("last confirm floor the bot find is:", last_floor)
                    return last_floor
            else:
                return last_floor
        
        else:
            # Find last swinf (not confirm)
            counter = len(data) - 1
            while counter > 0:
                if (data.iloc[counter]["swing"] != 0 and 
                    (data.iloc[counter]["macd signal"] == -1 or data.iloc[counter]["macd signal"] == 1)):

                    print("last minor swing the bot find is:", data.iloc[counter]["swing"])
                    last_swing = data.iloc[counter]["swing"]
                    break   
                counter -= 1
            
            return last_swing



class pivot:
    # Be careful that you should put a larger time frame than you trading for calculating pivot point 
    def __init__(self, df, pivot_timeframe=None, pivot_type=None):
        self.df = df
        self.pivot_type = pivot_type

        #If user set the pivot timeframe we use that but if not we find it and chose a suitable pivot time frame for it
        if pivot_timeframe is not None:
            self.pivot_timeframe = pivot_timeframe

        else:
            df_timeframe = find_timeframe(df)
            print('df timeframe is :', df_timeframe)
            #for lower than 15 minute df timeframe 1 day pivot time frame is suitable
            if df_timeframe[1] == 'm' and int(df_timeframe[0]) <= 15:
                self.pivot_timeframe = '1d'

            #for more than 15 minute df timeframe up to few hours 1 week pivot time frame is suitable
            elif (df_timeframe[1] == 'm' and int(df_timeframe[0]) > 15) or  df_timeframe[1] == 'h':
                self.pivot_timeframe = '1w'

            #for more than 1 day  df timeframe month pivot time frame is suitable   
            elif df_timeframe[1] == 'd':
                self.pivot_timeframe = '1mn'
            
            else:
                print("We can't chose any suitable time frame automatically, check what is wrong")
        
    
    def pivot_standard(self):
        pivot_df = change_timeframe(self.df, self.pivot_timeframe)
        high = pivot_df['high']
        low = pivot_df['low']
        close = pivot_df['close']

        pivot = (high + low + close) / 3
        pivot = pivot.rename("piv_st")

        # Calculate support and resistance levels
        pivot_support_1 = pivot * 2 - high
        pivot_support_1 = pivot_support_1.rename("piv_st_sup_1")

        pivot_support_2 = pivot - (high - low)
        pivot_support_2 = pivot_support_2.rename("piv_st_sup_2")

        pivot_resistance_1 = pivot * 2 - low
        pivot_resistance_1 = pivot_resistance_1.rename("piv_st_res_1")

        pivot_resistance_2 = pivot + (high - low)
        pivot_resistance_2 = pivot_resistance_2.rename("piv_st_res_2")

        # Calculate additional support and resistance levels
        pivot_support_3 = pivot - 2 * (high - low)
        pivot_support_3 = pivot_support_3.rename("piv_st_sup_3")

        pivot_resistance_3 = pivot + 2 * (high - low)
        pivot_resistance_3 = pivot_resistance_3.rename("piv_st_res_3")

        # Combine the calculated levels into a new DataFrame
        pivot_points_df = pd.concat([pivot, pivot_support_1, pivot_support_2, pivot_resistance_1, pivot_resistance_2,
                                    pivot_support_3, pivot_resistance_3], axis=1)

        pivot_points_df = pivot_points_df.shift(1)
        pivot_points_df.dropna(inplace=True)
        print(pivot_points_df)

        # Merge pivot_points_df with the original DataFrame using merge_asof
        self.df = pd.merge_asof(self.df, pivot_points_df, left_index=True, right_index=True)

        
        return self.df
    


class candlestick:
    def __init__(self):
        pass
        
         
    #candlestick pattern ----------------------------------------------------------------------------------
    @staticmethod
    def cdldoji(df):
        cdl = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
        df['cdl_doji'] = cdl

        return df
    

    @staticmethod
    def cdlhammer(df):
        cdl = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
        df['cdl_hammer'] = cdl

        return df
    

    @staticmethod
    def cdlhangingman(df):
        cdl = talib.CDLHANGINGMAN(df['open'], df['high'], df['low'], df['close'])
        df['cdl_hanging man'] = cdl

        return df
    

    @staticmethod
    def cdlengulfing(df):
        cdl = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
        df['cdl_engolfing'] = cdl

        return df
    
    
    @staticmethod
    def cdlthreewhitesoldiers(df):
        cdl = talib.CDL3WHITESOLDIERS(df['open'], df['high'], df['low'], df['close'])
        df['cdl_3 white soldiers'] = cdl

        return df
    

    @staticmethod
    def cdlthreeblackcrows(df):
        cdl = talib.CDL3BLACKCROWS(df['open'], df['high'], df['low'], df['close'])
        df['cdl_3 black crows'] = cdl

        return df
    
    
    @staticmethod
    def cdlmorningstar(df):
        cdl = talib.CDLMORNINGSTAR(df['open'], df['high'], df['low'], df['close'])
        df['cdl_morning star'] = cdl

        return df
    

    @staticmethod
    def cdlshootingstar(df):
        cdl = talib.CDLSHOOTINGSTAR(df['open'], df['high'], df['low'], df['close'])
        df['cdl_shooting star'] = cdl

        return df
    

    
    def addallcd(self, df):

        df = self.cdldoji(df)
        df = self.cdlengulfing(df)
        df = self.cdlhammer(df)
        df = self.cdlhangingman(df)
        df = self.cdlmorningstar(df)
        df = self.cdlshootingstar(df)
        df = self.cdlthreeblackcrows(df)
        df = self.cdlthreewhitesoldiers(df)

        return df



"""
# Swing finder example

login = metatrader(51735591, 'Wy7v5r4hu', 'Alpari-MT5-Demo')
login.start_mt5()

data = datamine('1d', 'EURUSD','online', number_data=10000)
data = data.df()
print(data)


#data = swing_finder(data, macdhistogram_signal=True, remove_price_minor_swings=True, wave_number_candles=True).Add_swinglist()
#print(data.tail(50))
last_ceiling = swing_finder(data, macdhistogram_signal=True).last_swing("ceiling")
print(last_ceiling)
"""
