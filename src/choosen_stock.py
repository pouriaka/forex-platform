from data_base import *




# 20 years data analysis ------------------------------------------------------------------

indexes_dict = {
    'S&P500': historical_database().load_historical_data('SP500'),
    'DowJones': historical_database().load_historical_data('DowJones'),
    'SX5E': historical_database().load_historical_data('SX5E'),
    'Nikkei225': historical_database().load_historical_data('Nikkei225'),
    'DAX': historical_database().load_historical_data('DAX'),
    'NASDAQ': historical_database().load_historical_data('NASDAQ'),
    'ASX200': historical_database().load_historical_data('ASX200'),
    'IBEX35': historical_database().load_historical_data('IBEX35'),
    'CAC': historical_database().load_historical_data('CAC')
}

NYSE_dict = {
    # 'GPN': historical_database().load_historical_data('GPN'),  # Global Payments
    # 'BA': historical_database().load_historical_data('BA'),  # The Boeing Company
    'DIS': historical_database().load_historical_data('DIS'),  # The Walt Disney Company
    # 'NFLX': historical_database().load_historical_data('NFLX'),  # Netflix
    # 'F': historical_database().load_historical_data('F'),  # Ford Motor Company
    # 'VMC': historical_database().load_historical_data('VMC'),  # Vulcan Materials Company
    'HD': historical_database().load_historical_data('HD'),  # The Home Depot
    'MCD': historical_database().load_historical_data('MCD'),  # McDonald's Corporation
    'STZ': historical_database().load_historical_data('STZ'),  # Constellation Brands
    'ADM': historical_database().load_historical_data('ADM'),  # Archer-Daniels-Midland Company
    'WMT': historical_database().load_historical_data('WMT'),  # Walmart
    'CLX': historical_database().load_historical_data('CLX'),  # The Clorox Company
    'LRLCY': historical_database().load_historical_data('LRLCY'),  # L'Oréal S.A.
    'PG': historical_database().load_historical_data('PG'),  # The Procter & Gamble Company
    'MO': historical_database().load_historical_data('MO'),  # Altria Group
    # 'SLB': historical_database().load_historical_data('SLB'),  # Schlumberger Limited
    'CVX': historical_database().load_historical_data('CVX'),  # Chevron Corporation
    # 'BAC': historical_database().load_historical_data('BAC'),  # Bank of America Corporation
    # 'AXP': historical_database().load_historical_data('AXP'),  # American Express Company
    'JNJ': historical_database().load_historical_data('JNJ'),  # Johnson & Johnson
    'PFE': historical_database().load_historical_data('PFE'),  # Pfizer
    'ABT': historical_database().load_historical_data('ABT'),  # Abbott Laboratories
    'GD': historical_database().load_historical_data('GD'),  # General Dynamics Corporation
    'LMT': historical_database().load_historical_data('LMT'),  # Lockheed Martin Corporation
    'RTX': historical_database().load_historical_data('RTX'),  # RTX Corporation
    # 'CAT': historical_database().load_historical_data('CAT'),  # Caterpillar
    # 'NSC': historical_database().load_historical_data('NSC'),  # Norfolk Southern Corporation
    'MMM': historical_database().load_historical_data('MMM'),  # 3M Company
    # 'BT': historical_database().load_historical_data('BT')  # BT Group plc
}

NASDAQ_dict = {
    # 'BKNG': historical_database().load_historical_data('BKNG'),  # Booking Holdings
    # 'AMZN': historical_database().load_historical_data('AMZN'),  # Amazon
    # 'LRCX': historical_database().load_historical_data('LRCX'),  # Lam Research Corporation
    # 'TSLA': historical_database().load_historical_data('TSLA'),  # Tesla
    # 'CSCO': historical_database().load_historical_data('CSCO'),  # Cisco Systems
    # 'GILD': historical_database().load_historical_data('GILD'),  # Gilead Sciences
    'GOOG': historical_database().load_historical_data('GOOG'),  # Alphabet (Google)
    
    # 'INTC': historical_database().load_historical_data('INTC'),  # Intel Corporation
    'MSFT': historical_database().load_historical_data('MSFT'),  # Microsoft Corporation
    'PEP': historical_database().load_historical_data('PEP'),  # PepsiCo
    # 'NVDA': historical_database().load_historical_data('NVDA'),  # NVIDIA Corporation
    'SBUX': historical_database().load_historical_data('SBUX'),  # Starbucks Corporation
    'AMGN': historical_database().load_historical_data('AMGN'),  # Amgen
    
    # 'EBAY': historical_database().load_historical_data('EBAY'),  # eBay Inc
    'ADP': historical_database().load_historical_data('ADP'),  # Automatic Data Processing
    'MDLZ': historical_database().load_historical_data('MDLZ'),  # Mondelez International
    'POOL': historical_database().load_historical_data('POOL'),  # Pool Corporation
    # 'AMD': historical_database().load_historical_data('AMD'),  # Advanced Micro Devices
    # 'QCOM': historical_database().load_historical_data('QCOM')  # QUALCOMM Incorporated
}

EUR_dict = {
    # 'VOW.DE': historical_database().load_historical_data('VOW'),  # Volkswagen AG
    'BMW.DE': historical_database().load_historical_data('BMW'),  # Bayerische Motoren Werke Aktiengesellschaft
    'PAH3.DE': historical_database().load_historical_data('PAH3'),  # Porsche Automobil Holding SE
    # 'CON.DE': historical_database().load_historical_data('CON'),  # Continental Aktiengesellschaft
    'ADS.DE': historical_database().load_historical_data('ADS'),  # adidas AG
    'SIE.DE': historical_database().load_historical_data('SIE'),  # Siemens Aktiengesellschaft
    'MC.PA': historical_database().load_historical_data('MC'),  # LVMH Moët Hennessy - Louis Vuitton, Société Européenne
    'ITRK.L': historical_database().load_historical_data('ITRK')  # Intertek Group plc (ITRK.L)
}




# After 2008 ------------------------------------------------------------------

start_date = '2009-01-01'
end_date = '2024-03-11'

indexes_dict = {
    'S&P500': historical_database().load_historical_data('SP500', start_date, end_date),
    'DowJones': historical_database().load_historical_data('DowJones', start_date, end_date),
    'SX5E': historical_database().load_historical_data('SX5E', start_date, end_date),
    'Nikkei225': historical_database().load_historical_data('Nikkei225', start_date, end_date),
    'DAX': historical_database().load_historical_data('DAX', start_date, end_date),
    'NASDAQ': historical_database().load_historical_data('NASDAQ', start_date, end_date),
    'ASX200': historical_database().load_historical_data('ASX200', start_date, end_date),
    'IBEX35': historical_database().load_historical_data('IBEX35', start_date, end_date),
    'CAC': historical_database().load_historical_data('CAC', start_date, end_date)
}

NYSE_dict = {
    'GPN': historical_database().load_historical_data('GPN', start_date, end_date),  # Global Payments
    # 'BA': historical_database().load_historical_data('BA', start_date, end_date),  # The Boeing Company
    'DIS': historical_database().load_historical_data('DIS', start_date, end_date),  # The Walt Disney Company
    # 'NFLX': historical_database().load_historical_data('NFLX', start_date, end_date),  # Netflix
    # 'F': historical_database().load_historical_data('F', start_date, end_date),  # Ford Motor Company
    # 'VMC': historical_database().load_historical_data('VMC', start_date, end_date),  # Vulcan Materials Company
    'HD': historical_database().load_historical_data('HD', start_date, end_date),  # The Home Depot
    'MCD': historical_database().load_historical_data('MCD', start_date, end_date),  # McDonald's Corporation
    'STZ': historical_database().load_historical_data('STZ', start_date, end_date),  # Constellation Brands
    'ADM': historical_database().load_historical_data('ADM', start_date, end_date),  # Archer-Daniels-Midland Company
    'WMT': historical_database().load_historical_data('WMT', start_date, end_date),  # Walmart
    'CLX': historical_database().load_historical_data('CLX', start_date, end_date),  # The Clorox Company
    # 'LRLCY': historical_database().load_historical_data('LRLCY', start_date, end_date),  # L'Oréal S.A.
    'PG': historical_database().load_historical_data('PG', start_date, end_date),  # The Procter & Gamble Company
    'MO': historical_database().load_historical_data('MO', start_date, end_date),  # Altria Group
    # 'SLB': historical_database().load_historical_data('SLB', start_date, end_date),  # Schlumberger Limited
    'CVX': historical_database().load_historical_data('CVX', start_date, end_date),  # Chevron Corporation
    # 'BAC': historical_database().load_historical_data('BAC', start_date, end_date),  # Bank of America Corporation
    # 'AXP': historical_database().load_historical_data('AXP', start_date, end_date),  # American Express Company
    'JNJ': historical_database().load_historical_data('JNJ', start_date, end_date),  # Johnson & Johnson
    'PFE': historical_database().load_historical_data('PFE', start_date, end_date),  # Pfizer
    'ABT': historical_database().load_historical_data('ABT', start_date, end_date),  # Abbott Laboratories
    'GD': historical_database().load_historical_data('GD', start_date, end_date),  # General Dynamics Corporation
    'LMT': historical_database().load_historical_data('LMT', start_date, end_date),  # Lockheed Martin Corporation
    'RTX': historical_database().load_historical_data('RTX', start_date, end_date),  # RTX Corporation
    # 'CAT': historical_database().load_historical_data('CAT', start_date, end_date),  # Caterpillar
    'NSC': historical_database().load_historical_data('NSC', start_date, end_date),  # Norfolk Southern Corporation
    'MMM': historical_database().load_historical_data('MMM', start_date, end_date),  # 3M Company
    'ADM': historical_database().load_historical_data('ADM', start_date, end_date),  # Archer-Daniels-Midland Company
    # 'BT': historical_database().load_historical_data('BT', start_date, end_date)  # BT Group plc
}

NASDAQ_dict = {
    # 'GOOG': historical_database().load_historical_data('GOOG', start_date, end_date),  # Alphabet (Google)
    # 'AMZN': historical_database().load_historical_data('AMZN', start_date, end_date),  # Amazon
    # 'BKNG': historical_database().load_historical_data('BKNG', start_date, end_date),  # Booking Holdings
    # 'LRCX': historical_database().load_historical_data('LRCX', start_date, end_date),  # Lam Research Corporation
    # 'TSLA': historical_database().load_historical_data('TSLA', start_date, end_date),  # Tesla
    'CSCO': historical_database().load_historical_data('CSCO', start_date, end_date),  # Cisco Systems
    'GILD': historical_database().load_historical_data('GILD', start_date, end_date),  # Gilead Sciences
    'INTC': historical_database().load_historical_data('INTC', start_date, end_date),  # Intel Corporation
    'MSFT': historical_database().load_historical_data('MSFT', start_date, end_date),  # Microsoft Corporation
    'PEP': historical_database().load_historical_data('PEP', start_date, end_date),  # PepsiCo
    # 'NVDA': historical_database().load_historical_data('NVDA', start_date, end_date),  # NVIDIA Corporation
    'SBUX': historical_database().load_historical_data('SBUX', start_date, end_date),  # Starbucks Corporation
    'AMGN': historical_database().load_historical_data('AMGN', start_date, end_date),  # Amgen
    'EBAY': historical_database().load_historical_data('EBAY', start_date, end_date),  # eBay Inc
    'ADP': historical_database().load_historical_data('ADP', start_date, end_date),  # Automatic Data Processing
    'MDLZ': historical_database().load_historical_data('MDLZ', start_date, end_date),  # Mondelez International
    'POOL': historical_database().load_historical_data('POOL', start_date, end_date),  # Pool Corporation
    # 'AMD': historical_database().load_historical_data('AMD', start_date, end_date),  # Advanced Micro Devices
    # 'QCOM': historical_database().load_historical_data('QCOM', start_date, end_date)  # QUALCOMM Incorporated
}


EUR_dict = {
    # 'VOW.DE': historical_database().load_historical_data('VOW', start_date, end_date),  # Volkswagen AG
    'BMW.DE': historical_database().load_historical_data('BMW', start_date, end_date),  # Bayerische Motoren Werke Aktiengesellschaft
    'PAH3.DE': historical_database().load_historical_data('PAH3', start_date, end_date),  # Porsche Automobil Holding SE
    # 'CON.DE': historical_database().load_historical_data('CON', start_date, end_date),  # Continental Aktiengesellschaft
    'ADS.DE': historical_database().load_historical_data('ADS', start_date, end_date),  # adidas AG
    'SIE.DE': historical_database().load_historical_data('SIE', start_date, end_date),  # Siemens Aktiengesellschaft
    'MC.PA': historical_database().load_historical_data('MC', start_date, end_date),  # LVMH Moët Hennessy - Louis Vuitton, Société Européenne
    'ITRK.L': historical_database().load_historical_data('ITRK', start_date, end_date)  # Intertek Group plc (ITRK.L)
}










"""

period = 10

# Global stock indexes ------------------------------------------------------------------------------
df1 = makestandard_df_from_yfinance(get_latest_data('^SPX', period)) # S&P500
df2 = makestandard_df_from_yfinance(get_latest_data('^DJI', period)) # DowJones
df3 = makestandard_df_from_yfinance(get_latest_data('^STOXX50E', period)) # SX5E
df4 = makestandard_df_from_yfinance(get_latest_data('^N225', period)) # Nikkei225
df5 = makestandard_df_from_yfinance(get_latest_data('^GDAXI', period)) # DAX
df6 = makestandard_df_from_yfinance(get_latest_data('^IXIC', period)) # NASDAQ
df7 = makestandard_df_from_yfinance(get_latest_data('^AXJO', period)) # ASX200
df8 = makestandard_df_from_yfinance(get_latest_data('^IBEX', period)) # IBEX35
df9 = makestandard_df_from_yfinance(get_latest_data('^NSEI', period))  # NIFTY50
df10 = makestandard_df_from_yfinance(get_latest_data('^FCHI', period)) # CAC

index_symbols = ['^SPX', '^DJI', '^STOXX50E', '^N225', '^GDAXI', '^IXIC', '^AXJO', '^IBEX', '^NSEI', '^FCHI']

indexes_dict = {
    'SP500':df1, 'DowJones':df2, 'SX5E':df3, 'Nikkei225':df4, 'DAX':df5, 
    'NASDAQ':df6, 'ASX200':df7, 'IBEX35':df8, 'NIFTY50':df9, 'CAC':df10
    }


# Global stock ---------------------------------------------------------------------------------------
# USA ----------------
# NYSE ------
df11 = makestandard_df_from_yfinance(get_latest_data('VMC', period)) # Vulcan Materials Company
df12 = makestandard_df_from_yfinance(get_latest_data('DIS', period)) # The Walt Disney Company
df13 = makestandard_df_from_yfinance(get_latest_data('NFLX', period)) # Netflix
df14 = makestandard_df_from_yfinance(get_latest_data('F', period)) # Ford Motor Company 
df15 = makestandard_df_from_yfinance(get_latest_data('HD', period)) # The Home Depot 
df16 = makestandard_df_from_yfinance(get_latest_data('MCD', period)) # McDonald's Corporation 
df17 = makestandard_df_from_yfinance(get_latest_data('STZ', period)) # Constellation Brands
df18 = makestandard_df_from_yfinance(get_latest_data('ADM', period)) # Archer-Daniels-Midland Company
df19 = makestandard_df_from_yfinance(get_latest_data('WMT', period)) # Walmart 
df20 = makestandard_df_from_yfinance(get_latest_data('CLX', period)) # The Clorox Company 
df21 = makestandard_df_from_yfinance(get_latest_data('LRLCY', period)) # L'Oréal S.A. 
df22 = makestandard_df_from_yfinance(get_latest_data('PG', period)) # The Procter & Gamble Company
df23 = makestandard_df_from_yfinance(get_latest_data('MO', period)) # Altria Group
df24 = makestandard_df_from_yfinance(get_latest_data('SLB', period)) # Schlumberger Limited 
df25 = makestandard_df_from_yfinance(get_latest_data('CVX', period)) # Chevron Corporation 
df26 = makestandard_df_from_yfinance(get_latest_data('BAC', period)) # Bank of America Corporation 
df27 = makestandard_df_from_yfinance(get_latest_data('MO', period)) # Altria Group
df28 = makestandard_df_from_yfinance(get_latest_data('AXP', period)) # American Express Company 
df29 = makestandard_df_from_yfinance(get_latest_data('JNJ', period)) # Johnson & Johnson 
df30 = makestandard_df_from_yfinance(get_latest_data('PFE', period)) # Pfizer 
df31 = makestandard_df_from_yfinance(get_latest_data('ABT', period)) # Abbott Laboratories 
df32 = makestandard_df_from_yfinance(get_latest_data('BA', period)) # The Boeing Company 
df33 = makestandard_df_from_yfinance(get_latest_data('GD', period)) # General Dynamics Corporation 
df34 = makestandard_df_from_yfinance(get_latest_data('LMT', period)) # Lockheed Martin Corporation 
df35 = makestandard_df_from_yfinance(get_latest_data('RTX', period)) # RTX Corporation 
df36 = makestandard_df_from_yfinance(get_latest_data('CAT', period)) # Caterpillar 
df37 = makestandard_df_from_yfinance(get_latest_data('NSC', period)) # Norfolk Southern Corporation 
df38 = makestandard_df_from_yfinance(get_latest_data('AHT', period)) # Ashford Hospitality Trust
df39 = makestandard_df_from_yfinance(get_latest_data('GPN', period)) # Global Payments 
df40 = makestandard_df_from_yfinance(get_latest_data('MMM', period)) # 3M Company 
df41 = makestandard_df_from_yfinance(get_latest_data('BT-A.L', period)) # BT Group plc 

NYSE_symbols = ['VMC', 'DIS', 'NFLX', 'F', 'HD', 'MCD', 'STZ', 'ADM', 'WMT'
, 'CLX', 'LRLCY', 'PG', 'MO', 'SLB', 'CVX', 'BAC', 'AXP', 'JNJ', 'PFE', 'ABT', 
'BA', 'GD', 'LMT', 'RTX', 'CAT', 'NSC', 'AHT', 'GPN', 'MMM', 'BT-A.L']


NYSE_dict = {
    'VMC': df11, 'DIS': df12, 'NFLX': df13, 'F': df14, 'HD': df15,
    'MCD': df16, 'STZ': df17, 'ADM': df18, 'WMT': df19, 'CLX': df20,
    'LRLCY': df21, 'PG': df22, 'MO': df23, 'SLB': df24, 'CVX': df25,
    'BAC': df26, 'MO': df27, 'AXP': df28, 'JNJ': df29, 'PFE': df30,
    'ABT': df31, 'BA': df32, 'GD': df33, 'LMT': df34, 'RTX': df35,
    'CAT': df36, 'NSC': df37, 'AHT': df38, 'GPN': df39, 'MMM': df40,
    'BT': df41
}


# NASDAQ  ------
df_forget_1 = makestandard_df_from_yfinance(get_latest_data('AAPL', period)) # Apple
df42 = makestandard_df_from_yfinance(get_latest_data('GOOG', period)) # Alphabet (Google)
df43 = makestandard_df_from_yfinance(get_latest_data('AMZN', period)) # Amazon
df44 = makestandard_df_from_yfinance(get_latest_data('CSCO', period)) # Cisco Systems
df45 = makestandard_df_from_yfinance(get_latest_data('INTC', period)) # Intel Corporation 
df46 = makestandard_df_from_yfinance(get_latest_data('MSFT', period)) # Microsoft Corporation 
df47 = makestandard_df_from_yfinance(get_latest_data('PEP', period)) # PepsiCo
df48 = makestandard_df_from_yfinance(get_latest_data('NVDA', period)) # NVIDIA Corporation 
df49 = makestandard_df_from_yfinance(get_latest_data('TSLA', period)) # Tesla
df50 = makestandard_df_from_yfinance(get_latest_data('SBUX', period)) # Starbucks Corporation 
df51 = makestandard_df_from_yfinance(get_latest_data('AMGN', period)) # Amgen 
df52 = makestandard_df_from_yfinance(get_latest_data('GILD', period)) # Gilead Sciences
df53 = makestandard_df_from_yfinance(get_latest_data('EBAY', period)) # eBay Inc
df54 = makestandard_df_from_yfinance(get_latest_data('ADP', period)) # Automatic Data Processing
df55 = makestandard_df_from_yfinance(get_latest_data('MDLZ', period)) # Mondelez International
df56 = makestandard_df_from_yfinance(get_latest_data('BKNG', period)) # Booking Holdings 
df57 = makestandard_df_from_yfinance(get_latest_data('POOL', period)) # Pool Corporation 
df58 = makestandard_df_from_yfinance(get_latest_data('LRCX', period)) # Lam Research Corporation 
df59 = makestandard_df_from_yfinance(get_latest_data('AMD', period)) # Advanced Micro Devices
df60 = makestandard_df_from_yfinance(get_latest_data('QCOM', period)) # QUALCOMM Incorporated 


NASDAQ_symbols = ['GOOG', 'AMZN', 'CSCO', 'INTC', 'MSFT', 'PEP', 'NVDA', 'TSLA',
'SBUX', 'AMGN', 'GILD', 'EBAY', 'ADP', 'MDLZ', 'BKNG', 'POOL', 'LRCX', 'AMD', 'QCOM']

NASDAQ_dict = {
    'GOOG': df42, 'AMZN': df43, 'CSCO': df44, 'INTC': df45, 'MSFT': df46,
    'PEP': df47, 'NVDA': df48, 'TSLA': df49, 'SBUX': df50, 'AMGN': df51,
    'GILD': df52, 'EBAY': df53, 'ADP': df54, 'MDLZ': df55, 'BKNG': df56,
    'POOL': df57, 'LRCX': df58, 'AMD': df59, 'QCOM': df60
}

# EUR ----------------
# XETRA ------
df61 = makestandard_df_from_yfinance(get_latest_data('BMW.DE', period)) # Bayerische Motoren Werke Aktiengesellschaft
df62 = makestandard_df_from_yfinance(get_latest_data('PAH3.DE', period)) # Porsche Automobil Holding SE 
df63 = makestandard_df_from_yfinance(get_latest_data('VOW.DE', period)) # Volkswagen AG 
df64 = makestandard_df_from_yfinance(get_latest_data('CON.DE', period)) # Continental Aktiengesellschaft
df65 = makestandard_df_from_yfinance(get_latest_data('ADS.DE', period)) # adidas AG  
df66 = makestandard_df_from_yfinance(get_latest_data('SIE.DE', period)) # Siemens Aktiengesellschaft 

# Paris ------
df67 = makestandard_df_from_yfinance(get_latest_data('MC.PA', period)) # LVMH Moët Hennessy - Louis Vuitton, Société Européenne

# UK ------
df68 = makestandard_df_from_yfinance(get_latest_data('BRBYL.XC', period)) # Burberry Group plc 
df69 = makestandard_df_from_yfinance(get_latest_data('ITRK.L', period)) # Intertek Group plc (ITRK.L)


EUR_symbols = ['BMW.DE', 'PAH3.DE', 'VOW.DE', 'CON.DE', 'ADS.DE', 'SIE.DE', 'MC.PA', 'BRBYL.XC', 'ITRK.L']

EUR_dict = {
    'BMW': df61, 'PAH3': df62, 'VOW': df63, 'CON': df64, 'ADS': df65,
    'SIE': df66, 'MC': df67, 'BRBYL': df68, 'ITRK': df69
}


input_dict = {**indexes_dict, **NYSE_dict, **NASDAQ_dict, **EUR_dict}
"""

# # Save forget historical price data --------------------------------------------------
# input_dict = {"aapl" : makestandard_df_from_yfinance(get_latest_data('AAPL', 6000))} 
# historical_database().save_input_dict_to_database(input_dict)













# # Load historical data from data set ------------------------------------------------------------------

# start_date = '2018-01-01'
# end_date = '2024-03-11'


# indexes_dict = {
#     'SP500': historical_database().load_historical_data('SP500', start_date, end_date),
#     'DowJones': historical_database().load_historical_data('DowJones', start_date, end_date),
#     'SX5E': historical_database().load_historical_data('SX5E', start_date, end_date),
#     # 'Nikkei225': historical_database().load_historical_data('Nikkei225', start_date, end_date),
#     'DAX': historical_database().load_historical_data('DAX', start_date, end_date),
#     'NASDAQ': historical_database().load_historical_data('NASDAQ', start_date, end_date),
#     'ASX200': historical_database().load_historical_data('ASX200', start_date, end_date),
#     # 'IBEX35': historical_database().load_historical_data('IBEX35', start_date, end_date),
#     'CAC': historical_database().load_historical_data('CAC', start_date, end_date)
# }

# NYSE_dict = {
#     'GPN': historical_database().load_historical_data('GPN', start_date, end_date),  # Global Payments
#     'DIS': historical_database().load_historical_data('DIS', start_date, end_date),  # The Walt Disney Company
#     'HD': historical_database().load_historical_data('HD', start_date, end_date),  # The Home Depot
#     'MCD': historical_database().load_historical_data('MCD', start_date, end_date),  # McDonald's Corporation
#     'STZ': historical_database().load_historical_data('STZ', start_date, end_date),  # Constellation Brands
#     'ADM': historical_database().load_historical_data('ADM', start_date, end_date),  # Archer-Daniels-Midland Company
#     'WMT': historical_database().load_historical_data('WMT', start_date, end_date),  # Walmart
#     'CLX': historical_database().load_historical_data('CLX', start_date, end_date),  # The Clorox Company
#     'PG': historical_database().load_historical_data('PG', start_date, end_date),  # The Procter & Gamble Company
#     'MO': historical_database().load_historical_data('MO', start_date, end_date),  # Altria Group
#     'CVX': historical_database().load_historical_data('CVX', start_date, end_date),  # Chevron Corporation
#     'JNJ': historical_database().load_historical_data('JNJ', start_date, end_date),  # Johnson & Johnson
#     'PFE': historical_database().load_historical_data('PFE', start_date, end_date),  # Pfizer
#     'ABT': historical_database().load_historical_data('ABT', start_date, end_date),  # Abbott Laboratories
#     'GD': historical_database().load_historical_data('GD', start_date, end_date),  # General Dynamics Corporation
#     'LMT': historical_database().load_historical_data('LMT', start_date, end_date),  # Lockheed Martin Corporation
#     'RTX': historical_database().load_historical_data('RTX', start_date, end_date),  # RTX Corporation
#     'NSC': historical_database().load_historical_data('NSC', start_date, end_date),  # Norfolk Southern Corporation
#     'MMM': historical_database().load_historical_data('MMM', start_date, end_date),  # 3M Company
# }

# NASDAQ_dict = {
#     'CSCO': historical_database().load_historical_data('CSCO', start_date, end_date),  # Cisco Systems
#     'GILD': historical_database().load_historical_data('GILD', start_date, end_date),  # Gilead Sciences
#     'INTC': historical_database().load_historical_data('INTC', start_date, end_date),  # Intel Corporation
#     'MSFT': historical_database().load_historical_data('MSFT', start_date, end_date),  # Microsoft Corporation
#     'PEP': historical_database().load_historical_data('PEP', start_date, end_date),  # PepsiCo
#     'SBUX': historical_database().load_historical_data('SBUX', start_date, end_date),  # Starbucks Corporation
#     'AMGN': historical_database().load_historical_data('AMGN', start_date, end_date),  # Amgen
#     'EBAY': historical_database().load_historical_data('EBAY', start_date, end_date),  # eBay Inc
#     'ADP': historical_database().load_historical_data('ADP', start_date, end_date),  # Automatic Data Processing
#     'MDLZ': historical_database().load_historical_data('MDLZ', start_date, end_date),  # Mondelez International
#     'POOL': historical_database().load_historical_data('POOL', start_date, end_date),  # Pool Corporation
# }


# EUR_dict = {
#     'BMW.DE': historical_database().load_historical_data('BMW', start_date, end_date),  # Bayerische Motoren Werke Aktiengesellschaft
#     'PAH3.DE': historical_database().load_historical_data('PAH3', start_date, end_date),  # Porsche Automobil Holding SE
#     'ADS.DE': historical_database().load_historical_data('ADS', start_date, end_date),  # adidas AG
#     'SIE.DE': historical_database().load_historical_data('SIE', start_date, end_date),  # Siemens Aktiengesellschaft
#     'MC.PA': historical_database().load_historical_data('MC', start_date, end_date),  # LVMH Moët Hennessy - Louis Vuitton, Société Européenne
#     'ITRK.L': historical_database().load_historical_data('ITRK', start_date, end_date)  # Intertek Group plc (ITRK.L)
# }

# all_dict = {**NYSE_dict, **NASDAQ_dict, **EUR_dict}


# Lite finance symbols statistic filter---------------------------------------------------------------------------------

# NYSE_symbols = ['VMC', 'DIS', 'NFLX', 'F', 'HD', 'MCD', 'STZ', 'ADM', 'WMT'
# , 'CLX', 'LRLCY', 'PG', 'MO', 'SLB', 'CVX', 'BAC', 'AXP', 'JNJ', 'PFE', 'ABT', 
# 'BA', 'GD', 'LMT', 'RTX', 'CAT', 'NSC', 'AHT', 'GPN', 'MMM', 'BT-A.L']

# NASDAQ_symbols = ['GOOG', 'AMZN', 'CSCO', 'INTC', 'MSFT', 'PEP', 'NVDA', 'TSLA',
# 'SBUX', 'AMGN', 'GILD', 'EBAY', 'ADP', 'MDLZ', 'BKNG', 'POOL', 'LRCX', 'AMD', 'QCOM']

# EUR_symbols = ['BMW.DE', 'PAH3.DE', 'VOW.DE', 'CON.DE', 'ADS.DE', 'SIE.DE', 'MC.PA', 'BRBYL.XC', 'ITRK.L']
# all_dict = NYSE_symbols + NASDAQ_symbols + EUR_symbols
# stock_find = []
# statiistic_table = historical_statistic_database().load_table('litefinance20240319')
# for item in statiistic_table:
#     Trailing_PE = item[3]
#     Forward_PE = item[4]
#     PEG_Ratio = item[5]
#     Price_Sales = item[6]
#     Price_Book = item[7]
#     Enterprise_Value_Revenue = item[8]
#     Enterprise_Value_EBITDA = item[9]
#     Beta = item[10]
#     try:
#         if (Trailing_PE <= 25 and Forward_PE <= 24 and PEG_Ratio <= 3 and 
#         Price_Sales <= 5 and Price_Book <= 4 and Enterprise_Value_Revenue <= 5 and 
#         Enterprise_Value_EBITDA <= 15 and Beta <= 1.3):
#             stock_find.append(item[0])
#     except:
#         print(f"Stock {item[0]} doesent have this parameter.")

# print(stock_find)





# #------------------------------------------------------------------------------------------------

#all_dict = { **NYSE_dict, **NASDAQ_dict, **EUR_dict}
# all_dict = {
#     'GILD': historical_database().load_historical_data('GILD', start_date, end_date),  # Gilead Sciences
#     'CVX': historical_database().load_historical_data('CVX', start_date, end_date),  # Chevron Corporation
#     'ADM': historical_database().load_historical_data('ADM', start_date, end_date),  # Archer-Daniels-Midland Company
#     'BMW.DE': historical_database().load_historical_data('BMW', start_date, end_date),  # Bayerische Motoren Werke Aktiengesellschaft
#     'MCD': historical_database().load_historical_data('MCD', start_date, end_date),  # McDonald's Corporation
#     'AAPL': historical_database().load_historical_data('AAPL', start_date, end_date),  # Apple 
#     'PEP': historical_database().load_historical_data('PEP', start_date, end_date),  # PepsiCo
#     'PG': historical_database().load_historical_data('PG', start_date, end_date),  # The Procter & Gamble Company
#     'VOW.DE': historical_database().load_historical_data('VOW', start_date, end_date),  # Volkswagen AG
# }






