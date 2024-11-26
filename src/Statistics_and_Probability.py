from Metatrader import *
from Datamine import *
from TechnicalTools import *
from data_base import *

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import time


"""
Find code modern portfolio gide in link  https://www.youtube.com/watch?v=mJTrQfzr0R4  from youtube.
"""


def correlation(df1, df2, show=True):
    # Calculate correlations
    pearson_corr = df1['close'].corr(df2['close'], method='pearson')
    spearman_corr = df1['close'].corr(df2['close'], method='spearman')
    kendall_corr = df1['close'].corr(df2['close'], method='kendall')

    if show:
        # Print the results
        print("Pearson Correlation:", pearson_corr)
        print("Spearman Correlation:", spearman_corr)
        print("Kendall Correlation:", kendall_corr)

    return pearson_corr


def find_winrate(df, tp_percent, sl_percent):
    # List of random numbers
    random_numbers = [0, 1]
    # Adding a new column with random numbers
    df['Random_Column'] = np.random.choice(random_numbers, size=len(df))

    print(df)
    winrate_list = []
    flag_pos = False
    for index in range(len(df)):
        price = df.iloc[index]['close']
        if df.iloc[index]['Random_Column'] == 1 and flag_pos == False:
            # open buy 
            price_open_buy = df.iloc[index]['close']
            flag_pos = True
            print("pos open ---------------------------------------------")
            print("price_open_buy", price_open_buy)

        if flag_pos == True and  ((price_open_buy - price)/price_open_buy) * 100 > sl_percent:
            # close buy loss
            flag_pos = False
            winrate_list.append(-1)
            print("pos close ---------------------------------------------")
            print("price_close", price)
        elif flag_pos == True and ((price - price_open_buy)/price_open_buy) * 100 > tp_percent:
            # close buy profit
            flag_pos = False
            winrate_list.append(1)
            print("pos close ----------------------------------------------")
            print("price_close", price)
        else:
            print("price:", price)


    # Count the occurrences of 1 in the list
    count_of_ones = winrate_list.count(1)
    winrate = count_of_ones/len(winrate_list)
    print("Win rate : ", winrate)

    return winrate


def get_historical_data(stock_symbol, start_date, end_date):
    try:
        stock = yf.Ticker(stock_symbol)
        historical_data = stock.history(start=start_date, end=end_date)
        return historical_data
    except Exception as e:
        print(f"Error fetching historical data for {stock_symbol}: {e}")
        return None


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




class modern_portfolio:
    def __init__(self):
        pass
    

    # Divide diffrente assets price to their atr
    def df_standard_changes(self, df, average_atr=None, show=False):
        if average_atr:
            df = df / average_atr
        else:
            ATR_len = 10
            df = indicator().atr(df, ATR_len)
            average_atr = df[f'atr_{ATR_len}'].dropna().mean()
            df = df.drop(f'atr_{ATR_len}', axis=1)
            df = df / average_atr
            if show:
                print(f"Average atr that we use for df:{df}\n is {average_atr}.")
        
        return df
    

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
    

    def assets_variance(self, df_dict, source_column='close'):
        var_dict = {}
        for df in df_dict:
            var_dict[df] = df_dict[df][source_column].var()
        
        return var_dict
    

    def assets_mean_return(self, returns_df):
        mean_return_dict = {}
        for column in returns_df.columns:
            mean_return_dict[column] = returns_df[column].mean()

        return mean_return_dict


    # Calculate the portfolio retur by average return of assets and their weghts 
    def portfolio_return(self, df, weights):
        portfolio_return = np.dot(df.mean(), weights)

        return portfolio_return


    # Claculate standard deviation of a portfolio using it return df and weight of each asset
    def portfolio_standard_deviation(self, df, weights, duration=250):
        # Calculate covariance matrix
        covariance_matrix = df.cov()
        portfolio_variance = np.dot(np.dot(covariance_matrix, weights), weights)

        # Calculate annualised portfolio standard deviation
        standard_deviation = portfolio_variance ** (1/2) * np.sqrt(duration)

        return standard_deviation


    # Generate random portfolio weights that sum of them is equal 1
    def weights_cretor(self, df):
        rand = np.random.random(len(df.columns))
        # Sum of the weights should be 1
        rand /= rand.sum()

        return rand


    # Invest with diffrent random weights on returns list to find diffrente portfolio return and diffrent standard deviation
    def invest_test(self, returns_df, number_invest):
        portfolio_returns_list = []
        standard_deviations_list = []
        weights_list = []

        for number in range(number_invest):
            weights = self.weights_cretor(returns_df)
            weights_list.append(weights)

            new_return = self.portfolio_return(returns_df, weights)
            portfolio_returns_list.append(new_return)

            new_standard_deviation = self.portfolio_standard_deviation(returns_df, weights)
            standard_deviations_list.append(new_standard_deviation)

        return standard_deviations_list, portfolio_returns_list, weights_list


    # Take all portfolio datas and return a df contain just efficient frontier datas
    def efficient_frontier_data(self, df_dict, standard_deviations_list, portfolio_returns_list, weights_list, divide=0.1):
        # Create a panda dataframe for saving portfolio on the efficien frontier
        efficien_frontier_df = pd.DataFrame(columns=[])

        counter = 0
        while counter < max(standard_deviations_list):
            interval_return_list = []
            interval_std_list = []
            # Find all the points in the std interval and find the best one of them by it return
            for i in range(len(standard_deviations_list) - 1):
                if counter < standard_deviations_list[i] and standard_deviations_list[i] < counter + divide:
                    interval_return_list.append(portfolio_returns_list[i])
                    interval_std_list.append(standard_deviations_list[i])
                    

            if interval_return_list != []:
                # Information of best portfolio in the std interval  
                max_return_in_interval = max(interval_return_list)
                max_return_std = max(interval_std_list)
                max_data_number = standard_deviations_list.index(max(interval_std_list))
                max_return_weights = weights_list[max_data_number]
                
                # Save the information in a panda dataframe
                row = {}
                keys_list = list(df_dict.keys())
                for i in range(len(keys_list)):
                    row.update({f'{keys_list[i]}_W': max_return_weights[i]})
                
                row.update({'std': max_return_std, 'returns':max_return_in_interval})
                efficien_frontier_df = efficien_frontier_df._append(row, ignore_index=True)

            counter += divide

        return efficien_frontier_df
    

    def plot_diagram(self, ef_df, standard_deviations_list, portfolio_returns_list, weights_list, 
                     in_range_portfolio=pd.DataFrame(columns=[]), min_risk_point=True):
        if min_risk_point:
            print("minimum risk with maximum return portfolio:")
            print("min standard deviation:", min(standard_deviations_list))
            print("max return with min risk:", portfolio_returns_list[standard_deviations_list.index(min(standard_deviations_list))])
            print("weights:", weights_list[standard_deviations_list.index(min(standard_deviations_list))])

        # Plot modern Portfolio diagram
        plt.scatter(standard_deviations_list, portfolio_returns_list)

        # Plot efficient frontier
        for i in range(len(ef_df)):
            plt.scatter(ef_df['std'][i], ef_df['returns'][i], c='g')

        # Plot in range portfolio from efficient frontier
        if not in_range_portfolio.empty:
            for row in in_range_portfolio.itertuples(index=False):
                plt.scatter(row.std, row.returns, c='black')

        # Change the color of minimum risk point with maximum return to red
        plt.scatter(min(standard_deviations_list), portfolio_returns_list[standard_deviations_list.index(min(standard_deviations_list))], c='r')
        plt.title('Efficient frontier')
        plt.xlabel('Standard deviation of returns')
        plt.ylabel('Returns')
        plt.show()


    def run(self, df_dict, sell_df_list_name=[], number_invest=1000, source_column='close', 
            std_range=None, show_var=True, mean_return=True, plot=True, plot_weight_range=True):
        
        returns_df = self.make_percentage_df_returns(df_dict, sell_df_list_name, source_column)
        standard_deviations_list, portfolio_returns_list, weights_list = self.invest_test(returns_df, number_invest)
        ef_df = self.efficient_frontier_data(df_dict, standard_deviations_list, portfolio_returns_list, weights_list)


        if show_var:
            print("Variance of assets:\n",self.assets_variance(df_dict, source_column),"\n")

        if mean_return:
            print("Mean return of assets:\n",self.assets_mean_return(returns_df),"\n")

        if std_range :
            in_range_portfolio = self.best_portfolio_find(ef_df, std_range)

        if plot:
            if std_range:
                self.plot_diagram(ef_df, standard_deviations_list, portfolio_returns_list, weights_list, in_range_portfolio)
            else:
                self.plot_diagram(ef_df, standard_deviations_list, portfolio_returns_list, weights_list)


        if std_range:
            if plot_weight_range:
                self.plot_currencies_weight_range_diagram(in_range_portfolio)
            return in_range_portfolio
        else:
            if plot_weight_range:
                self.plot_currencies_weight_range_diagram(ef_df)
            return ef_df


    def best_portfolio_find(self, ef_df, std_range):
        # Filter the DataFrame based on the 'std' range
        filtered_df = ef_df[(ef_df['std'] >= std_range[0]) & (ef_df['std'] <= std_range[1])]

        return filtered_df


    def plot_currencies_weight_range_diagram(self, df):
        # Plotting a bar graph with dots for each currency
        fig, ax = plt.subplots(figsize=(12, 6))

        # Iterate over each currency (excluding 'std' and 'returns') and plot a dot for its value
        for currency in df.columns:
            if currency not in ['std', 'returns']:
                ax.scatter([currency] * len(df), df[currency], label=currency)

        # Set labels and title
        ax.set_xlabel('Currencies')
        ax.set_ylabel('Values')
        ax.set_title('Currencies weight range diagram')
        ax.legend()

        # Display the plot
        plt.show()


    def positive_return_percentage(self, df):
        # Ensure the DataFrame is not empty
        if df.empty:
            raise ValueError("DataFrame is empty")

        # Calculate the percentage of positive returns for each column
        positive_percentages = (df[df > 0].count() / len(df)) * 100

        return positive_percentages





period = 7000

df1 = makestandard_df_from_yfinance(get_latest_data('GILD', period)) 
# df2 = makestandard_df_from_yfinance(get_latest_data('CVX', period)) 
# df3 = makestandard_df_from_yfinance(get_latest_data('ADM', period)) 
# df4 = makestandard_df_from_yfinance(get_latest_data('BMW.DE', period)) 
# df5 = makestandard_df_from_yfinance(get_latest_data('MCD', period)) 
# df6 = makestandard_df_from_yfinance(get_latest_data('PEP', period)) 
# df7 = makestandard_df_from_yfinance(get_latest_data('PG', period)) 
# df8 = makestandard_df_from_yfinance(get_latest_data('VOW.DE', period)) 
df9 = makestandard_df_from_yfinance(get_latest_data('AAPL', period))


# df10 = makestandard_df_from_yfinance(get_latest_data('^SPX', period)) # S&P500
# df11 = makestandard_df_from_yfinance(get_latest_data('^DJI', period)) # DowJones
# df12 = makestandard_df_from_yfinance(get_latest_data('^STOXX50E', period)) # SX5E
# df13 = makestandard_df_from_yfinance(get_latest_data('^N225', period)) # Nikkei225
# df14 = makestandard_df_from_yfinance(get_latest_data('^GDAXI', period)) # DAX
# df15 = makestandard_df_from_yfinance(get_latest_data('^IXIC', period)) # NASDAQ
# df16 = makestandard_df_from_yfinance(get_latest_data('^AXJO', period)) # ASX200
# df17 = makestandard_df_from_yfinance(get_latest_data('^FCHI', period)) # CAC


# Short
df18 = makestandard_df_from_yfinance(get_latest_data('BAC', period)) # Banck of american


# indexes_dict = {
#     'SP500':df10, 
#     'DowJones':df11, 
#     'SX5E':df12, 
#     'Nikkei225':df13, 
#     'DAX':df14, 
#     'NASDAQ':df15, 
#     'ASX200':df16, 
#     'CAC':df17
#     }

all_dict = {#**indexes_dict,
    'GILD': df1,  # Gilead Sciences
    # 'CVX': df2,  # Chevron Corporation
    # 'ADM': df3,  # Archer-Daniels-Midland Company
    # 'BMW.DE': df4,  # Bayerische Motoren Werke Aktiengesellschaft
    # 'MCD': df5,  # McDonald's Corporation
    # 'PEP': df6,  # PepsiCo
    # 'PG': df7,  # The Procter & Gamble Company
    # 'VOW.DE': df8,  # Volkswagen AG
    'AAPL': df9,  # Apple
    'BAC': df18  # Banck of american
}

# login = metatrader(89471471, '137811P28p$', 'LiteFinance-MT5-Demo')
# login = metatrader(317931, 'iHQLhGKZ28kG74_', 'LiteFinance-MT5-Live')
# login.start_mt5()
# all_dict = {
#     #'EURUSD' : datamine('1d', 'EURUSD_l', 'online', number_data=period).df(),
#     #'XAUUSD' : datamine('1d', 'XAUUSD_l', 'online', number_data=period).df(),
#     'AAPL' : datamine('1d', '#AAPL_l', 'online', number_data=period).df(),
#     'PEP' : datamine('1d', '#PEP_l', 'online', number_data=period).df(),
#     'PG' : datamine('1d', '#PG_l', 'online', number_data=period).df(),
#     'SPX' : datamine('1d', 'SPX_l', 'online', number_data=period).df()
# }

print(all_dict)

# in_range_portfolio_df = modern_portfolio().run(all_dict, number_invest=10000)
df_return = modern_portfolio().make_percentage_df_returns(all_dict, ['BAC'])
df = df_return


# Initialize the initial investment
initial_investment = 100
weights = [0.35, 0.35, 0.3]
money_list = []

# Calculate the weighted investment for each weight and append to money_list
for weight in weights:
    weighted_investment = initial_investment * weight
    money_list.append(weighted_investment)


# Print the resulting DataFrame
print(df)
print(money_list)

# Returning the number of columns
num_columns = df.shape[1]
new_portfolio_stock_value = {}
old_portfolio_stock_value = {}
rebalance_portfolio = {}
portfolio_values = []
for column in range(num_columns):
    old_portfolio_stock_value[f'{column}'] = money_list[column] 
old_portfolio_value = sum(old_portfolio_stock_value.values())

for row in range(len(df)):
    for column in range(num_columns):
        new_portfolio_stock_value[f'{column}'] = (1 + (df.iloc[row, column]/100)) * old_portfolio_stock_value[f'{column}']

    new_portfolio_value = sum(new_portfolio_stock_value.values())
    change_portfolio_value = new_portfolio_value - old_portfolio_value

    for column in range(num_columns):
        rebalance_portfolio[f'{column}'] =  old_portfolio_stock_value[f'{column}'] + (weights[column] * change_portfolio_value)

    rebalance_portfolio_value = sum(rebalance_portfolio.values())
    portfolio_values.append(rebalance_portfolio_value)

    print(new_portfolio_stock_value)
    print(rebalance_portfolio)
    print(rebalance_portfolio_value)
    print(change_portfolio_value)
    

    old_portfolio_value = rebalance_portfolio_value
    old_portfolio_stock_value = rebalance_portfolio


df['portfolio value'] = portfolio_values
# Calculate the daily returns and add as a new column
df['portfolio return'] = df['portfolio value'].pct_change()

# Calculate the running maximum of the portfolio values
df['Running Max'] = df['portfolio value'].cummax()

# Calculate the drawdown
df['Drawdown'] = df['portfolio value'] / df['Running Max'] - 1

# Calculate the maximum drawdown
max_drawdown = df['Drawdown'].min()


# Calculate the rolling standard deviation of 'BAC' stock and add as a new column
df['BAC Rolling Std'] = df['BAC'].expanding().std()


# Display the DataFrame and the maximum drawdown
print(f"\nMaximum Drawdown: {max_drawdown * 100:.2f}%")

# Calculate the standard deviation of the 'Portfolio Return' column
std_dev_return = df['portfolio return'].std()
print(f"\nStandard Deviation of Portfolio Returns: {std_dev_return:.4f}")


# Remove multiple columns by name
df.drop(columns=['Running Max', 'Drawdown'], inplace=True)


hold_portfolio_return_list = []
hold_portfolio_return = 0
for row in range(len(df)):
    for column in range(num_columns):
        hold_portfolio_return += weights[column] * df.iloc[row, column]

    hold_portfolio_return_list.append(hold_portfolio_return)
    hold_portfolio_return = 0

df['hold portfolio return'] = hold_portfolio_return_list


portfolio_old_value = initial_investment
valu_dict = {}
total_list = []
total_value = 0

for column in range(num_columns):
    valu_dict[f'stock{column}'] = [weights[column] * initial_investment]

for row in range(len(df)):
    for column in range(num_columns):
        old_value = valu_dict[f'stock{column}'][row]
        new_value = old_value + (old_value * (df.iloc[row, column]/100))
        valu_dict[f'stock{column}'].append(new_value)

for column in range(num_columns):
    valu_dict[f'stock{column}'].pop(0)
    df[f'stock{column}'] = valu_dict[f'stock{column}']

for row in range(len(df)):
    for column in range(7, 7 + num_columns):
        total_value += df.iloc[row, column]

    total_list.append(total_value)
    total_value = 0


df['hold portfolio value'] = total_list

# Calculate the running maximum of the portfolio values
df['hold Running Max'] = df['hold portfolio value'].cummax()

# # Calculate the drawdown
df['hold Drawdown'] = df['hold portfolio value'] / df['hold Running Max'] - 1

# Calculate the maximum drawdown
max_drawdown = df['hold Drawdown'].min()


# Display the DataFrame and the maximum drawdown
print(f"\nMaximum Drawdown: {max_drawdown * 100:.2f}%")

# Calculate the standard deviation of the 'Portfolio Return' column
std_dev_hold_return = df['hold portfolio return'].std()
print(f"\nStandard Deviation of hold Portfolio Returns: {std_dev_hold_return:.4f}")


# Remove multiple columns by name
df.drop(columns=['hold Running Max', 'hold Drawdown'], inplace=True)
df.drop(columns=['stock0', 'stock1', 'stock2'], inplace=True)



# Calculate BAC new return by filtering high std
high_std_flag = False


# Drop rows with any NaN values
df = df.dropna()
# Resetting the index
df.reset_index(drop=True, inplace=True)


for row in range(len(df)):
    if high_std_flag is False and abs(df['BAC'][row]) >= (df['BAC Rolling Std'][row]) * 2 :
        high_std_flag = True

    if high_std_flag and abs(df['BAC'][row]) <= df['BAC Rolling Std'][row]:
        high_std_flag = False
        
    if high_std_flag:
        df.loc[row,'BAC'] = 0
        

portfolio_old_value = initial_investment
valu_dict = {}
total_list = []
total_value = 0

for column in range(num_columns):
    valu_dict[f'stock{column}'] = [weights[column] * initial_investment]


print(df)
for row in range(len(df)):
    for column in range(num_columns):
        old_value = valu_dict[f'stock{column}'][row]
        new_value = old_value + (old_value * (df.iloc[row, column]/100))
        valu_dict[f'stock{column}'].append(new_value)

for column in range(num_columns):
    valu_dict[f'stock{column}'].pop(0)
    df[f'stock{column}'] = valu_dict[f'stock{column}']


# Remove multiple columns by name
df.drop(columns=['portfolio value', 'portfolio return'], inplace=True)

for row in range(len(df)):
    for column in range(6, 6 + num_columns):
        total_value += df.iloc[row, column]

    total_list.append(total_value)
    total_value = 0


df['std portfolio value'] = total_list

# Calculate the running maximum of the portfolio values
df['std Running Max'] = df['std portfolio value'].cummax()

# # Calculate the drawdown
df['std Drawdown'] = df['std portfolio value'] / df['std Running Max'] - 1

# Calculate the maximum drawdown
max_drawdown = df['std Drawdown'].min()


# Display the DataFrame and the maximum drawdown
print(f"\nMaximum Drawdown: {max_drawdown * 100:.2f}%")

# Calculate the standard deviation of the 'Portfolio Return' column
# std_dev_hold_return = df['std portfolio return'].std()
# print(f"\nStandard Deviation of hold Portfolio Returns: {std_dev_hold_return:.4f}")


# Remove multiple columns by name
df.drop(columns=['std Running Max', 'std Drawdown'], inplace=True)
df.drop(columns=['stock0', 'stock1', 'stock2'], inplace=True)

print(df)

# Create a plot
plt.figure(figsize=(10, 5))
plt.plot(portfolio_values, marker='o', linestyle='-', color='b')

# Adding title and labels
plt.title('Portfolio change')
plt.xlabel('data')
plt.ylabel('portfolio Value')

# Display the plot
plt.grid(True)
plt.show()


# Create a plot
plt.figure(figsize=(10, 5))
plt.plot(total_list, marker='o', linestyle='-', color='b')

# Adding title and labels
plt.title('Portfolio change')
plt.xlabel('data')
plt.ylabel('portfolio Value')

# Display the plot
plt.grid(True)
plt.show()


# Print the covariance matrix
# covariance_matrix = df_return.cov()
# print("Covariance Matrix:")
# print(covariance_matrix)


# plt.imshow(covariance_matrix, cmap='coolwarm', interpolation='none')
# plt.title('Covariance Matrix ')
# # Set axis labels with asset names
# plt.xticks(range(len(covariance_matrix.columns)), covariance_matrix.columns, rotation=45, ha='right')
# plt.yticks(range(len(covariance_matrix.columns)), covariance_matrix.columns)
# plt.colorbar()

# plt.show()













