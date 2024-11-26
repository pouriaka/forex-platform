import yfinance as yf
import pandas as pd

# Replace 'AAPL' with the ticker symbol of the stock you're interested in
ticker_symbol = 'AAPL'

# Specify the start and end dates for the data
start_date = '2019-05-06'
end_date = '2024-05-06'

# Fetch the data from Yahoo Finance
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Print the balance sheet data
print(stock_data)


def get_latest_data(stock_symbol, num_days=1000):
    try:
        stock = yf.Ticker(stock_symbol)
        historical_data = stock.history(period=f"{num_days}d")
        return historical_data
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None


def makestandard_df_from_yfinance(df):
    # Make rates to panda dataframe
    df = pd.DataFrame(df)
    
    # Set 'time' column as the index
    df.reset_index('Date', inplace=True)

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

    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'], utc=True)

    time_column = []
    for index in range(len(df)):
        row_time = df.iloc[index]['time']
        
        # Extract just the date
        date_only = row_time.date()

        # Format the date as a string in the desired format (YYYY-MM-DD)
        formatted_date_str = date_only.strftime('%Y-%m-%d')
        time_column.append(formatted_date_str)
        
    df['time'] = time_column

    # Set 'time' column as the index
    #df.set_index('time', inplace=True)

    # Remove columns with NaN in column names
    df = df.drop('NaN', axis=1)

    return df




class portfolio_returne:
    def __init__(self):
        pass

    # For make a df just contain source columns 
    def concat_columns(self, df_dict, source_column='close'):
        # Extract source_column columns and concatenate them
        close_columns = [df[source_column] for df in df_dict.values()]
        concat_df = pd.concat(close_columns, axis=1, keys=df_dict.keys())

        # Rename the columns with the keys
        concat_df.columns = df_dict.keys()

        return concat_df


    # Use for when we short (sell in bearish market)
    def change_return_sign(self, return_df, sell_df_list_name):
        for name in sell_df_list_name:
            return_df[name] = -return_df[name]

        return return_df


    def make_percentage_df_returns(self, df_dict, sell_df_list_name=[], source_column='close'):
        # Calculate df returns panda data frame from source column
        concat_df = self.concat_columns(df_dict, source_column=source_column)
        returns_df = concat_df.pct_change().dropna() * 100

        if sell_df_list_name != []:
            # Change the assets return sign that we short
            returns_df = self.change_return_sign(returns_df, sell_df_list_name)

        return returns_df