from Metatrader import *
#from . import server

import pandas as pd
from datetime import datetime
import pytz

server = 'Alpari-MT5-Demo' # Server must be a string, also we can import it from __init__.py file 
#for creating new object remember to assigning value to nuber data for example like thise (number_data="50")
#If you don't it will by mistake fill start_time
#time column is change to index for the whole project
class datamine:
    def __init__(self, timeframe, symbol, online_offline, start_time=None, end_time=None, number_data=None):
        
        self.timeframe = timeframe
        self.symbol = symbol
        self.online_offline = online_offline

        self.start_time = start_time
        self.end_time = end_time
        self.number_data = number_data

        # Check if both optional_var1 and optional_var2 are provided
        if self.start_time is not None and self.end_time is not None and self.number_data is not None:
            raise ValueError("You cannot provide both start/end time and number data.")
        
        # Check if neither optional_var1 nor optional_var2 are provided
        if self.start_time is None and self.end_time is None and self.number_data is None:
            raise ValueError("You must provide either start/end or number data.")
        
        # Chek if assining wrong value to onlin/offline parameter
        if self.online_offline == 'online' or self.online_offline == 'offline':
            pass

        else:
            print('online_offline variable should be one of "online" or "offline" string')
            

    @staticmethod
    def makestandard_df(df):
        #make rates to panda dataframe
        df = pd.DataFrame(df)
        
        #making the df headers standard that we use in project
        header_names = ['time', 'open', 'high', 'low', 'close', 'volume']
        df.columns = [''] * len(df.columns)
        if len(df.columns) == 6:
            df.columns = header_names
        else:
            extra_column = len(df.columns) - 6
            for i in range(extra_column):
                header_names.append('NaN')
            df.columns = header_names  

        #change time stamp to date and time, also if it is not time stamp it will pass
        df['time'] = pd.to_datetime(df['time'], errors='coerce')


        return df


    # We use "change_timeframe" insted of thise method
    def change_dataset_timeframe(self, df):
        #Thise methode take 1 minute panda data frame and chang it to the time frame that we want
        moving_in_list = 1
        min_count = 0
        indext_drop = []

        #change 1m to 1 or other timeframes to integer
        if type(self.timeframe) is str:
            timeframe = int(self.timeframe[0])
        else:
            timeframe = self.timeframe   

        while moving_in_list < len(df) - 1 :
            while min_count < timeframe - 1:
                indext_drop.append(moving_in_list + min_count)
                min_count += 1
            
            min_count = 0
            moving_in_list += timeframe

        df = df.drop(indext_drop)
        #renumber df    
        df.index = range(len(df))

        return df
  

    def load_dataset(self):
        rates_1 = pd.read_csv('D:/project/python_pr/forexbacktest_platform/datasets/EURUSD/EURUSD_Candlestick_1_M_BID_01.01.2015-01.01.2016.csv')
        rates_2 = pd.read_csv('D:/project/python_pr/forexbacktest_platform/datasets/EURUSD/EURUSD_Candlestick_1_M_BID_01.01.2016-01.01.2017.csv')
        rates_3 = pd.read_csv('D:/project/python_pr/forexbacktest_platform/datasets/EURUSD/EURUSD_Candlestick_1_M_BID_01.01.2017-01.01.2018.csv')
        rates_4 = pd.read_csv('D:/project/python_pr/forexbacktest_platform/datasets/EURUSD/EURUSD_Candlestick_1_M_BID_01.01.2018-01.01.2019.csv')
        rates_5 = pd.read_csv('D:/project/python_pr/forexbacktest_platform/datasets/EURUSD/EURUSD_Candlestick_1_M_BID_01.01.2019-01.01.2020.csv')
        rates_6 = pd.read_csv('D:/project/python_pr/forexbacktest_platform/datasets/EURUSD/EURUSD_Candlestick_1_M_BID_01.01.2020-01.01.2021.csv')
        
        #make rates standard
        df_1 = datamine.makestandard_df(rates_1) 
        df_2 = datamine.makestandard_df(rates_2) 
        df_3 = datamine.makestandard_df(rates_3) 
        df_4 = datamine.makestandard_df(rates_4) 
        df_5 = datamine.makestandard_df(rates_5) 
        df_6 = datamine.makestandard_df(rates_6)  

        df = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6], ignore_index=True)

        # Set 'time' column as the DataFrame index
        df.set_index('time', inplace=True)

        return df


    def dataset_between2dates_datamine(self):
        df = self.load_dataset()

        # Create a date range between the start and end dates (inclusive)
        date_range = pd.date_range(start=self.start_time, end=self.end_time, freq='T')

        # Use boolean indexing to filter the DataFrame for the desired date range
        df = df.loc[df.index.isin(date_range)]
        
        df = change_timeframe(df, self.timeframe)

        return df


    def dataset_number_datamine(self):
        if type(self.number_data) is str:
            #make number of data int for standard of metatrader
            number_data = int(self.number_data) 
        else:
            number_data = self.number_data

        df = self.load_dataset()
        df = change_timeframe(df, self.timeframe)
        df = df.tail(number_data)

        # Set 'time' column as the DataFrame index
        df.set_index('time', inplace=True)

        return df


    def makestandard_mt5_value(self):
        # standard one of the number of data or dates
        if self.number_data is not None:
            if type(self.number_data) is str:
                #make number of data int for standard of metatrader
                self.mt_number_data = int(self.number_data)   
            else:
                self.mt_number_data = self.number_data


        if self.start_time is not None and self.end_time is not None:
            # Split the string into year, month, and day components
            year_start, month_start, day_start = self.start_time.split('-')
            year_end, month_end, day_end = self.end_time.split('-')

            # Convert the components to integers
            year_start = int(year_start)
            month_start = int(month_start)
            day_start = int(day_start)

            year_end = int(year_end)
            month_end = int(month_end)
            day_end = int(day_end)

            #set the correct time zone
            timezone = pytz.timezone("Etc/UTC")

            # Create the datetime object using the datetime constructor
            self.mt_start_time = datetime(year_start, month_start, day_start, tzinfo=timezone)
            self.mt_end_time = datetime(year_end, month_end, day_end, tzinfo=timezone)


        #make time frame to standard of metetrader timeframe
        if self.timeframe == '1m':
            self.mt_timeframe = mt5.TIMEFRAME_M1

        elif self.timeframe == '2m':
            self.mt_timeframe = mt5.TIMEFRAME_M2

        elif self.timeframe == '3m':
            self.mt_timeframe = mt5.TIMEFRAME_M3

        elif self.timeframe == '4m':
            self.mt_timeframe = mt5.TIMEFRAME_M4

        elif self.timeframe == '5m':
            self.mt_timeframe = mt5.TIMEFRAME_M5

        elif self.timeframe == '6m':
            self.mt_timeframe = mt5.TIMEFRAME_M6

        elif self.timeframe == '10m':
            self.mt_timeframe = mt5.TIMEFRAME_M10

        elif self.timeframe == '12m':
            self.mt_timeframe = mt5.TIMEFRAME_M12

        elif self.timeframe == '15m':
            self.mt_timeframe = mt5.TIMEFRAME_M15

        elif self.timeframe == '20m':
            self.mt_timeframe = mt5.TIMEFRAME_M20

        elif self.timeframe == '30m':
            self.mt_timeframe = mt5.TIMEFRAME_M30

        elif self.timeframe == '1h':
            self.mt_timeframe = mt5.TIMEFRAME_H1

        elif self.timeframe == '2h':
            self.mt_timeframe = mt5.TIMEFRAME_H2

        elif self.timeframe == '3h':
            self.mt_timeframe = mt5.TIMEFRAME_H3  

        elif self.timeframe == '4h':
            self.mt_timeframe = mt5.TIMEFRAME_H4

        elif self.timeframe == '6h':
            self.mt_timeframe = mt5.TIMEFRAME_H6    

        elif self.timeframe == '8h':
            self.mt_timeframe = mt5.TIMEFRAME_H8

        elif self.timeframe == '12h':
            self.mt_timeframe = mt5.TIMEFRAME_H12

        elif self.timeframe == '1d':
            self.mt_timeframe = mt5.TIMEFRAME_D1

        elif self.timeframe == '1w':
            self.mt_timeframe = mt5.TIMEFRAME_W1

        elif self.timeframe == '1mn':
            self.mt_timeframe = mt5.TIMEFRAME_MN1

        else:
            print('your input dataframe is not the standard dataframe that metatrader 5 has.')

        #make symbol to standard of metatrader and broker symbol
        #for future if we want to set the symbol for any other broker
        if server == 'Alpari-MT5-Demo' or server == 'Alpari-MT5':
            #self.symbol = f'{self.symbol}_i'
            pass         


    def mt5_between2dates_datamine(self):
        self.makestandard_mt5_value()
        
        rates = mt5.copy_rates_range(self.symbol, self.mt_timeframe, self.mt_start_time, self.mt_end_time)

        #make header of dataframe
        df = pd.DataFrame(rates)
        
        #change time stamp to date and time
        df['time'] = pd.to_datetime(df['time'],unit='s')

        # Set 'time' column as the DataFrame index
        df.set_index('time', inplace=True)
        df = df.rename(columns={'tick_volume': 'volume'})

        return df
        

    def mt5_number_datamine(self):
        self.makestandard_mt5_value()

        #get the now clock from datetime
        now = datetime.now()
        utc_from_year = now.year
        utc_from_month = now.month
        utc_from_day = now.day
        utc_from_hour = now.hour
        utc_from_minute = now.minute
        
        
        #set the correct time zone
        timezone = pytz.timezone("Etc/UTC")
        now_second = datetime(utc_from_year ,utc_from_month ,utc_from_day ,utc_from_hour ,utc_from_minute , tzinfo=timezone)
        
        rates = mt5.copy_rates_from(self.symbol, self.mt_timeframe, now_second, self.mt_number_data)
        
        #make rates to panda datat frame
        df = pd.DataFrame(rates)

        #change time stamp to date and time
        df['time'] = pd.to_datetime(df['time'],unit='s')
        
        # Set 'time' column as the DataFrame index
        df.set_index('time', inplace=True)
        df = df.rename(columns={'tick_volume': 'volume'})

        return df  


    def df(self):
        if self.online_offline == 'online':
            if self.number_data is not None:
                return self.mt5_number_datamine()
        
            if self.start_time is not None and self.end_time is not None:
                return self.mt5_between2dates_datamine()

        if self.online_offline == 'offline':
            if self.number_data is not None:
                return self.dataset_number_datamine()
        
            if self.start_time is not None and self.end_time is not None:
                return self.dataset_between2dates_datamine()



def find_timeframe(df):
    # Calculate the time difference between consecutive timestamps
    time_diff = df.index.to_series().diff().dropna()

    # When we have 1 minute data frame above method returns an empty pd
    if time_diff.empty:
        timeframe = '1m'
    else:
        # Find the most common time difference
        most_common_diff = time_diff.mode().iloc[0]

        # Convert the most common time difference to a string representation
        if most_common_diff.seconds < 3600 and most_common_diff.days < 1:  # lower than 1 hour, minute timeframe
            timeframe = f"{most_common_diff.seconds // 60}m"
        elif most_common_diff.seconds < 86400 and most_common_diff.days < 1:  # lower than 1 day, hour timeframe
            timeframe = f"{most_common_diff.seconds // 3600}h"
        elif 1 <= most_common_diff.days and most_common_diff.days < 7:  # lower than 1 week, day timeframe
            timeframe = f"{most_common_diff.days}d"
        elif 7 <= most_common_diff.days and most_common_diff.days < 28:  # lower than 1 month, week timeframe
            timeframe = f"{most_common_diff.days // 7}w"
        else:
            timeframe = '1mn'

    return timeframe




def change_timeframe(df, new_timeframe):
    # Map user-defined time frame strings to pandas frequency strings
    timeframe_mapping = {
        **{f'{i}m': f'{i}T' for i in range(1, 9999)},  # Minutes
        **{f'{i}d': f'{i}D' for i in range(1, 9999)},  # Days
        **{f'{i}w': f'{i}W' for i in range(1, 9999)},  # Weeks
        **{f'{i}mn': f'{i}M' for i in range(1, 9999)}  # Months
    }

    # Check if the new_timeframe exists in the mapping dictionary
    if new_timeframe in timeframe_mapping:
        new_timeframe = timeframe_mapping[new_timeframe]

    # Check if time is't index
    try:
        # Set 'time' column as the DataFrame index
        df.set_index('time', inplace=True)
    except:
        pass

    # Define the aggregation dictionary
    agg_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    }

    # If 'tick_volume' exists, add it to the aggregation dictionary
    if 'tick_volume' in df:
        agg_dict['tick_volume'] = 'sum'

    # If 'tick_volume' exists, add it to the aggregation dictionary
    if 'volume' in df:
        agg_dict['volume'] = 'sum'

    # If 'spread' exists, add it to the aggregation dictionary
    if 'spread' in df:
        agg_dict['spread'] = 'last'

    # If 'real_volume' exists, add it to the aggregation dictionary
    if 'real_volume' in df:
        agg_dict['real_volume'] = 'sum'

    # Resample the DataFrame to the new_timeframe
    resampled_df = df.resample(new_timeframe).agg(agg_dict)

    # Remove any rows with NaN values (if any)
    resampled_df.dropna(inplace=True)

    return resampled_df




