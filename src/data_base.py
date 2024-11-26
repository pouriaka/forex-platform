import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine
import yfinance as yf
import pandas as pd

from Metatrader import *




class database:
    def __init__(self): 
        self.connect()

    def connect(self):
        try:
            # Set a custom timeout value (in seconds)
            custom_timeout = 100

            # Create a connection configuration with the custom timeout
            config = {
                'host': 'localhost',
                'user': 'root',
                'passwd': '***************',
                'database': 'forex',
                'connect_timeout': custom_timeout,
            }

            self.db = mysql.connector.connect(**config)
            self.cursor = self.db.cursor()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.handle_connection_error()

    def handle_connection_error(self):
        # Handle the lost connection error here
        print("Attempting to reconnect...")
        self.connect()


    def save_main_pos(self, ticket, symbol, main_trend, management_level, fix_price, 
                      volume, pip_part, zone, riskfree_wait, riskfree_level, magic, money_involved, spread):
        query = ("INSERT INTO main_trend_positions"
                "(ticket, symbol, main_trend, management_level," 
                "fix_price, volume, pip_part, zone, riskfree_wait, riskfree_level, time, magic, money_involved, spread) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        self.cursor.execute(query,(ticket, symbol, main_trend, management_level, fix_price, volume, 
                    pip_part, zone, riskfree_wait, riskfree_level, datetime.now(), magic, money_involved, spread))
        self.db.commit()


    def save_riskfree_pos(self, ticket, main_pos_ticket, symbol, main_trend, management_level, 
                          fix_price, volume, pip_part, zone, riskfree_wait, riskfree_level, spread, magic):
        query = ("INSERT INTO riskfree_positions"
                "(ticket, main_pos_ticket, symbol, main_trend, management_level," 
                "fix_price, volume, pip_part, zone, riskfree_wait, riskfree_level, time, spread, magic) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        self.cursor.execute(query,(ticket, main_pos_ticket, symbol, main_trend, management_level, fix_price, 
                        volume, pip_part, zone, riskfree_wait, riskfree_level, datetime.now(), spread, magic))
        self.db.commit()


    def save_log(self, log):
        query = ("INSERT INTO program_log"
                "(time, log)"
                "VALUES (%s, %s)")
        
        self.cursor.execute(query,(datetime.now(), log))
        self.db.commit()

    
    def save_money_loss(self, money_loss, management_level, parameters, ticket):
        query = ("INSERT INTO loss_money"
                "(time, amount, management_level, parameters, ticket)"
                "VALUES (%s, %s, %s, %s, %s)")
        
        self.cursor.execute(query,(datetime.now(), money_loss, management_level, parameters, ticket))
        self.db.commit()

    
    def save_no_money_loss(self, money_loss, management_level, parameters, ticket):
        query = ("INSERT INTO no_loss_money"
                "(time, amount, management_level, parameters, ticket)"
                "VALUES (%s, %s, %s, %s, %s)")
        
        self.cursor.execute(query,(datetime.now(), money_loss, management_level, parameters, ticket))
        self.db.commit()


    def save_user_input(self, input_type, value):
        query = ("INSERT INTO inputs"
                "(input_type, value, time) "
                "VALUES (%s, %s, %s)")
        self.cursor.execute(query,(input_type, value, datetime.now()))
        self.db.commit()

    
    def save_loss_level(self, ticket, loss_level):
        query = f"UPDATE main_trend_positions SET loss_level = {loss_level} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit()


    def save_auto_change_riskfree(self, ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved):
        query = ("INSERT INTO auto_change_riskfree_level"
                "(ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved, time) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
        self.cursor.execute(query,(ticket, type_of_autochange, amount, new_riskfree_level, new_money_involved, datetime.now()))
        self.db.commit()


    def update_management_level(self, table, ticket, management_level):
        query = f"UPDATE {table} SET management_level = {management_level} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit()


    def update_sum_loss(self, ticket, sum_loss):
        query = f"UPDATE main_trend_positions SET sum_loss = {sum_loss} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit()


    def update_number_auto_change_riskfree(self, ticket, new_number_auto_change_riskfree):
        query = f"UPDATE main_trend_positions SET number_auto_change_riskfree = {new_number_auto_change_riskfree} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit()


    def update_riskfree_level(self, table, ticket, riskfree_level):
        if table == "main_trend_positions":
            query = f"UPDATE {table} SET riskfree_level = {riskfree_level} WHERE ticket = {ticket}"
            self.cursor.execute(query)
            self.db.commit()   
        else:
            query = f"UPDATE {table} SET riskfree_level = {riskfree_level} WHERE main_pos_ticket = {ticket}"
            self.cursor.execute(query)
            self.db.commit()


    def update_money_involved(self, ticket, money_involved):
        query = f"UPDATE main_trend_positions SET money_involved = {money_involved} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit()   


    def update_achieve(self, id, condition):
        query = f"UPDATE auto_change_riskfree_level SET achieve = '{condition}' WHERE id = {id}"
        self.cursor.execute(query)
        self.db.commit()     

    
    def update_achieve_by_ticket(self, ticket, condition):
        query = f"UPDATE auto_change_riskfree_level SET achieve = '{condition}' WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit() 


    def clear_table(self, table):
        query = f"DELETE FROM {table};"
        self.cursor.execute(query)
        self.db.commit()


    def delete_row(self, table, ticket):
        query = f"DELETE FROM {table} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        self.db.commit()


    def load_riskfree_level(self, ticket):
        query = f"SELECT riskfree_level FROM main_trend_positions WHERE ticket = {ticket}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result
    

    def load_main_pos_spread(self, ticket):
        query = f"SELECT spread FROM main_trend_positions WHERE ticket = {ticket}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result


    def load_row(self, table, ticket):
        query = f"SELECT * FROM {table} WHERE ticket = {ticket}"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            print(f"No row found with ticket {ticket}")
            return None


    def load_row_2(self, table, ticket):
        query = f"SELECT * FROM {table} WHERE id = {ticket}"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            print(f"No row found with ticket (or id) {ticket}")
            return None


    def load_last_row(self, table, primary_key_column):
        query = f"SELECT * FROM {table} ORDER BY {primary_key_column} DESC LIMIT 1;"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            print(f"No row found. Table is empty.")


    def load_table(self, table):
        rows_list = []
        # Execute the SELECT query to fetch all rows from the table
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)

        # Fetch all rows
        rows = self.cursor.fetchall()

        # Process the rows (print in this example)
        for row in rows:
            rows_list.append(row)

        return rows_list


    def calculate_all_money_involved_in_full_riskfree(self):
        main_trend_table = self.load_table("main_trend_positions")
        sum_money = 0
        for item in main_trend_table:
            sum_money += item[13]  
        return sum_money



class historical_database:
    def __init__(self): 
        self.connect()

    def connect(self):
        try:
            # Set a custom timeout value (in seconds)
            custom_timeout = 100

            # Create a connection configuration with the custom timeout
            config = {
                'host': 'localhost',
                'user': 'root',
                'passwd': '$gpMFuBJ3Q1#U6^V',
                'database': 'historical_data',
                'connect_timeout': custom_timeout,
            }

            self.db = mysql.connector.connect(**config)
            self.cursor = self.db.cursor()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.handle_connection_error()


    def handle_connection_error(self):
        # Handle the lost connection error here
        print("Attempting to reconnect...")
        self.connect()
    

    def save_dataframe_to_database(self, df, table_name):
        try:
            # Define the MySQL connection string
            engine = create_engine('mysql+mysqlconnector://root:$gpMFuBJ3Q1#U6^V@localhost/historical_data')

            # Save the DataFrame to the MySQL database
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=True)

            print(f"DataFrame saved to MySQL database table '{table_name}'.")

        except Exception as e:
            print(f"Error: {e}")


    def save_input_dict_to_database(self, input_dict):
        for item in input_dict:
            self.save_dataframe_to_database(input_dict[item], item)


    def load_historical_data(self, table_name, start_date=None, end_date=None):
        try:
            # Create a Pandas DataFrame by selecting all data from the MySQL table
            query = f'SELECT * FROM {table_name}'

            # Execute the SQL query
            self.cursor.execute(query)

            # Fetch all the results into a Pandas DataFrame
            result_df = pd.DataFrame(self.cursor.fetchall(), columns=[desc[0] for desc in self.cursor.description])

            if start_date != None and end_date != None:
                result_df = self.filter_dataframe_by_date(result_df, start_date, end_date)

            return result_df

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return pd.DataFrame()  # Return an empty DataFrame in case of an error
        

    def filter_dataframe_by_date(self, df, start_date, end_date):
        df['time'] = pd.to_datetime(df['time'])  # Convert 'time' column to datetime format
        mask = (df['time'] >= start_date) & (df['time'] <= end_date)
        filtered_df = df.loc[mask]

        return filtered_df



class historical_statistic_database:
    def __init__(self): 
        self.connect()

    def connect(self):
        try:
            # Set a custom timeout value (in seconds)
            custom_timeout = 100

            # Create a connection configuration with the custom timeout
            config = {
                'host': 'localhost',
                'user': 'root',
                'passwd': '$gpMFuBJ3Q1#U6^V',
                'database': 'historical_statistic_data',
                'connect_timeout': custom_timeout,
            }

            self.db = mysql.connector.connect(**config)
            self.cursor = self.db.cursor()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.handle_connection_error()


    def handle_connection_error(self):
        # Handle the lost connection error here
        print("Attempting to reconnect...")
        self.connect()


    def create_table(self, table_name):
        try:
            # Construct the SQL query to create the table with appropriate columns
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                Symbol VARCHAR(10),
                Market_Cap BIGINT,
                Enterprise_Value BIGINT,
                Trailing_PE FLOAT,
                Forward_PE FLOAT,
                PEG_Ratio FLOAT,
                Price_Sales FLOAT,
                Price_Book FLOAT,
                Enterprise_Value_Revenue FLOAT,
                Enterprise_Value_EBITDA FLOAT,
                Beta FLOAT,
                Week_52_Change FLOAT,
                Week_52_High FLOAT,
                Week_52_Low FLOAT,
                Day_50_Moving_Avg FLOAT,
                Day_200_Moving_Avg FLOAT,
                Avg_Vol_3_month BIGINT,
                Avg_Vol_10_day BIGINT,
                Shares_Outstanding BIGINT,
                Percent_Held_by_Insiders FLOAT,
                Percent_Held_by_Institutions FLOAT,
                Shares_Short BIGINT,
                Short_Ratio FLOAT,
                Short_Percent_of_Float FLOAT,
                Short_Percent_of_Shares_Outstanding FLOAT,
                Dividend_Rate FLOAT,
                Dividend_Yield FLOAT,
                Payout_Ratio FLOAT,
                Revenue BIGINT,
                Profit_Margin FLOAT,
                Operating_Margin FLOAT,
                Return_on_Assets FLOAT,
                Return_on_Equity FLOAT,
                Total_Cash BIGINT,
                Total_Debt BIGINT,
                Current_Ratio FLOAT,
                Book_Value_Per_Share FLOAT,
                Operating_Cash_Flow BIGINT,
                Levered_Free_Cash_Flow BIGINT
            );
            '''

            # Execute the SQL query
            self.cursor.execute(create_table_query)

            # Commit the changes
            self.db.commit()

            print(f"Table '{table_name}' created successfully.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # Rollback in case of errors
            self.db.rollback()


    def check_table_exist(self, table_name):
        # Check if table exists
        self.cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = self.cursor.fetchone()

        # If result is not None, table exists
        if result:
            return True
        else:
            return False


    def get_stock_statistics(self, ticker_symbol):
        try:
            # Download stock data
            stock_data = yf.Ticker(ticker_symbol)

            # Get statistics
            statistics = {
                "Symbol": ticker_symbol,
                "Market Cap": stock_data.info.get("marketCap"),
                "Enterprise Value": stock_data.info.get("enterpriseValue"),
                "Trailing P/E": stock_data.info.get("trailingPE"),
                "Forward P/E": stock_data.info.get("forwardPE"),
                "PEG Ratio": stock_data.info.get("pegRatio"),
                "Price/Sales": stock_data.info.get("priceToSalesTrailing12Months"),
                "Price/Book": stock_data.info.get("priceToBook"),
                "Enterprise Value/Revenue": stock_data.info.get("enterpriseToRevenue"),
                "Enterprise Value/EBITDA": stock_data.info.get("enterpriseToEbitda"),
                "Beta": stock_data.info.get("beta"),
                "52-Week Change": stock_data.info.get("52WeekChange"),
                "52 Week High": stock_data.info.get("fiftyTwoWeekHigh"),
                "52 Week Low": stock_data.info.get("fiftyTwoWeekLow"),
                "50-Day Moving Average": stock_data.info.get("fiftyDayAverage"),
                "200-Day Moving Average": stock_data.info.get("twoHundredDayAverage"),
                "Avg Vol (3 month)": stock_data.info.get("averageVolume"),
                "Avg Vol (10 day)": stock_data.info.get("averageVolume10days"),
                "Shares Outstanding": stock_data.info.get("sharesOutstanding"),
                "percent Held by Insiders": stock_data.info.get("heldPercentInsiders"),
                "percent Held by Institutions": stock_data.info.get("heldPercentInstitutions"),
                "Shares Short": stock_data.info.get("sharesShort"),
                "Short Ratio": stock_data.info.get("shortRatio"),
                "Short percent of Float": stock_data.info.get("shortPercentOfFloat"),
                "Short percent of Shares Outstanding": stock_data.info.get("shortPercentOfSharesOutstanding"),
                "Dividend Rate": stock_data.info.get("dividendRate"),
                "Dividend Yield": stock_data.info.get("dividendYield"),
                "Payout Ratio": stock_data.info.get("payoutRatio"),
                "Revenue": stock_data.info.get("totalRevenue"),
                "Profit Margin": stock_data.info.get("profitMargins"),
                "Operating Margin": stock_data.info.get("operatingMargins"),
                "Return on Assets": stock_data.info.get("returnOnAssets"),
                "Return on Equity": stock_data.info.get("returnOnEquity"),
                "Total Cash": stock_data.info.get("totalCash"),
                "Total Debt": stock_data.info.get("totalDebt"),
                "Current Ratio": stock_data.info.get("currentRatio"),
                "Book Value Per Share": stock_data.info.get("bookValue"),
                "Operating Cash Flow": stock_data.info.get("operatingCashflow"),
                "Levered Free Cash Flow": stock_data.info.get("freeCashflow"),
            }

            return statistics

        except Exception as e:
            return f"Error: {e}"


    def save_statistic_data(self, table_name, data):
        # Define the SQL query to insert data into the table
        sql_query = f"INSERT INTO {table_name}" +'''
         (Symbol, `Market_Cap`, `Enterprise_Value`, `Trailing_PE`, `Forward_PE`,
        `PEG_Ratio`, `Price_Sales`, `Price_Book`, `Enterprise_Value_Revenue`, `Enterprise_Value_EBITDA`, Beta, 
        `Week_52_Change`, `Week_52_High`, `Week_52_Low`, `Day_50_Moving_Avg`, `Day_200_Moving_Avg`,
        `Avg_Vol_3_month`, `Avg_Vol_10_day`, `Shares_Outstanding`, `percent_Held_by_Insiders`, 
        `percent_Held_by_Institutions`, `Shares_Short`, `Short_Ratio`, `Short_percent_of_Float`, 
        `Short_percent_of_Shares_Outstanding`, `Dividend_Rate`, `Dividend_Yield`, `Payout_Ratio`, Revenue, 
        `Profit_Margin`, `Operating_Margin`, `Return_on_Assets`, `Return_on_Equity`, `Total_Cash`, `Total_Debt`, 
        `Current_Ratio`, `Book_Value_Per_Share`, `Operating_Cash_Flow`, `Levered_Free_Cash_Flow`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
         
        # Extract values from the data dictionary and convert them into a tuple
        values = (
            data['Symbol'],
            data['Market Cap'],
            data['Enterprise Value'],
            data['Trailing P/E'],
            data['Forward P/E'],
            data['PEG Ratio'],
            data['Price/Sales'],
            data['Price/Book'],
            data['Enterprise Value/Revenue'],
            data['Enterprise Value/EBITDA'],
            data['Beta'],
            data['52-Week Change'],
            data['52 Week High'],
            data['52 Week Low'],
            data['50-Day Moving Average'],
            data['200-Day Moving Average'],
            data['Avg Vol (3 month)'],
            data['Avg Vol (10 day)'],
            data['Shares Outstanding'],
            data['percent Held by Insiders'],
            data['percent Held by Institutions'],
            data['Shares Short'],
            data['Short Ratio'],
            data['Short percent of Float'],
            data['Short percent of Shares Outstanding'],
            data['Dividend Rate'],
            data['Dividend Yield'],
            data['Payout Ratio'],
            data['Revenue'],
            data['Profit Margin'],
            data['Operating Margin'],
            data['Return on Assets'],
            data['Return on Equity'],
            data['Total Cash'],
            data['Total Debt'],
            data['Current Ratio'],
            data['Book Value Per Share'],
            data['Operating Cash Flow'],
            data['Levered Free Cash Flow']
        )

        # Execute the SQL query with the data
        self.cursor.execute(sql_query, values)
        self.db.commit()


    def save_update_spx_statistic(self, show=True):
        spx_symbols_list = [
        'MMM', 'ACE', 'ABT', 'ANF', 'ACN', 'ADBE', 'AMD', 'AES', 'AET', 'AFL',
        'A', 'GAS', 'APD', 'ARG', 'AKAM', 'AA', 'ALXN', 'ATI', 'AGN', 'ALL',
        'ANR', 'ALTR', 'MO', 'AMZN', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP',
        'ABC', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'APOL', 'AAPL',
        'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVB', 'AVY', 'AVP',
        'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BAX', 'BBT', 'BEAM', 'BDX', 'BBBY', 'BMS',
        'BRK.B', 'BBY', 'BIG', 'BIIB', 'BLK', 'HRB', 'BMC', 'BA', 'BWA', 'BXP', 'BSX',
        'BMY', 'BRCM', 'BF.B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH',
        'CFN', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF',
        'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS',
        'CLF', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA',
        'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'CBE', 'GLW', 'COST', 'CVH', 'COV',
        'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DF', 'DE', 'DELL',
        'DNR', 'XRAY', 'DVN', 'DV', 'DO', 'DTV', 'DFS', 'DISCA', 'DLTR', 'D', 'RRD',
        'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY',
        'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQR',
        'EL', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV', 'FDO', 'FAST', 'FII', 'FDX',
        'FIS', 'FITB', 'FHN', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI',
        'F', 'FRX', 'FOSL', 'BEN', 'FCX', 'FTR', 'GME', 'GCI', 'GPS', 'GD', 'GE', 'GIS',
        'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOG', 'GWW', 'HAL', 'HOG', 'HAR', 'HRS', 'HIG',
        'HAS', 'HCP', 'HCN', 'HNZ', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST',
        'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'TEG', 'INTC', 'ICE', 'IBM', 'IFF', 'IGT',
        'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JBL', 'JEC', 'JDSU', 'JNJ', 'JCI',
        'JOY', 'JPM', 'JNPR', 'K', 'KEY', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KFT',
        'KR', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LUK', 'LXK', 'LIFE', 'LLY',
        'LTD', 'LNC', 'LLTC', 'LMT', 'L', 'LO', 'LOW', 'LSI', 'MTB', 'M', 'MRO', 'MPC',
        'MAR', 'MMC', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MHP', 'MCK', 'MJN', 'MWV',
        'MDT', 'MRK', 'MET', 'PCS', 'MCHP', 'MU', 'MSFT', 'MOLX', 'TAP', 'MON', 'MNST',
        'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NBR', 'NDAQ', 'NOV', 'NTAP', 'NFLX',
        'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC',
        'NTRS', 'NOC', 'NU', 'NRG', 'NUE', 'NVDA', 'NYX', 'ORLY', 'OXY', 'OMC', 'OKE',
        'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'BTU', 'JCP', 'PBCT', 'POM',
        'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL',
        'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD',
        'PRU', 'PEG', 'PSA', 'PHM', 'QEP', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'RHT',
        'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RDC', 'R', 'SWY',
        'SAI', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SHLD', 'SRE', 'SHW',
        'SIAL', 'SPG', 'SLM', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'S', 'STJ', 'SWK',
        'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'SUN', 'STI', 'SYMC', 'SYY', 'TROW',
        'TGT', 'TEL', 'TE', 'THC', 'TDC', 'TER', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO',
        'TIF', 'TWX', 'TWC', 'TIE', 'TJX', 'TMK', 'TSS', 'TRIP', 'TSN', 'TYC', 'USB',
        'UNP', 'UNH', 'UPS', 'X', 'UTX', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN',
        'VZ', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WAG', 'DIS', 'WPO', 'WM', 'WAT', 'WPI',
        'WLP', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFM', 'WMB', 'WIN', 'WEC', 'WPX', 'WYN',
        'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZMH', 'ZION'
        ]
        today = datetime.today()

        # Extract just the date
        date_only = today.date()

        # Format the date as a string in the desired format (YYYY-MM-DD)
        formatted_date_str = date_only.strftime('%Y-%m-%d')
        table_number = formatted_date_str.replace("-", "")
        table_name = f"spx{table_number}"

        if self.check_table_exist(table_name):
            print(f"We save statistic data for date {formatted_date_str} in the past.")
        else:
            self.create_table(table_name)
            for stock in spx_symbols_list:
                stock_data = self.get_stock_statistics(stock)
                if stock_data['Market Cap'] is not None and stock_data['Enterprise Value'] is not None:
                    self.save_statistic_data(table_name, stock_data)
                    if show:
                        print(stock_data)


    def save_update_dji_statistic(self, show=True):
        dji_symbols_list = [
            "MSFT",  # Microsoft Corporation
            "AAPL",  # Apple Inc
            "AMZN",  # Amazon.com, Inc.
            "V",     # Visa Inc.
            "JPM",   # JPMorgan Chase & Co.
            "WMT",   # Walmart Inc.
            "UNH",   # UnitedHealth Group Incorporated
            "JNJ",   # Johnson & Johnson
            "PG",    # The Procter & Gamble Company
            "HD",    # The Home Depot, Inc.
            "MRK",   # Merck & Co., Inc.
            "CRM",   # Salesforce, Inc.
            "CVX",   # Chevron Corporation
            "KO",    # The Coca-Cola Company
            "DIS",   # The Walt Disney Company
            "CSCO",  # Cisco Systems, Inc.
            "MCD",   # McDonald's Corporation
            "INTC",  # Intel Corporation
            "IBM",   # International Business Machines Corporation
            "CAT",   # Caterpillar Inc.
            "VZ",    # Verizon Communications Inc.
            "AXP",   # American Express Company
            "NKE",   # NIKE, Inc.
            "AMGN",  # Amgen Inc.
            "HON",   # Honeywell International Inc.
            "GS",    # The Goldman Sachs Group, Inc.
            "BA",    # The Boeing Company
            "MMM",   # 3M Company
            "TRV",   # The Travelers Companies, Inc.
            "DOW"    # Dow Inc.
            ]

        today = datetime.today()

        # Extract just the date
        date_only = today.date()

        # Format the date as a string in the desired format (YYYY-MM-DD)
        formatted_date_str = date_only.strftime('%Y-%m-%d')
        table_number = formatted_date_str.replace("-", "")
        table_name = f"dji{table_number}"

        if self.check_table_exist(table_name):
            print(f"We save statistic data for date {formatted_date_str} in the past.")
        else:
            self.create_table(table_name)
            for stock in dji_symbols_list:
                stock_data = self.get_stock_statistics(stock)
                if stock_data['Market Cap'] is not None and stock_data['Enterprise Value'] is not None:
                    self.save_statistic_data(table_name, stock_data)
                    if show:
                        print(stock_data)


    def save_update_litefinance_stockCFD_statistic (self, show=True):
        NYSE_symbols = ['VMC', 'DIS', 'NFLX', 'F', 'HD', 'MCD', 'STZ', 'ADM', 'WMT'
        , 'CLX', 'LRLCY', 'PG', 'MO', 'SLB', 'CVX', 'BAC', 'AXP', 'JNJ', 'PFE', 'ABT', 
        'BA', 'GD', 'LMT', 'RTX', 'CAT', 'NSC', 'AHT', 'GPN', 'MMM', 'BT-A.L']

        NASDAQ_symbols = ['APPL', 'GOOG', 'AMZN', 'CSCO', 'INTC', 'MSFT', 'PEP', 'NVDA', 'TSLA',
        'SBUX', 'AMGN', 'GILD', 'EBAY', 'ADP', 'MDLZ', 'BKNG', 'POOL', 'LRCX', 'AMD', 'QCOM']

        EUR_symbols = ['BMW.DE', 'PAH3.DE', 'VOW.DE', 'CON.DE', 'ADS.DE', 'SIE.DE', 'MC.PA', 'BRBYL.XC', 'ITRK.L']

        all_dict = NYSE_symbols + NASDAQ_symbols + EUR_symbols

        today = datetime.today()

        # Extract just the date
        date_only = today.date()

        # Format the date as a string in the desired format (YYYY-MM-DD)
        formatted_date_str = date_only.strftime('%Y-%m-%d')
        table_number = formatted_date_str.replace("-", "")
        table_name = f"litefinance{table_number}"

        if self.check_table_exist(table_name):
            print(f"We save statistic data for date {formatted_date_str} in the past.")
        else:
            self.create_table(table_name)
            for stock in all_dict:
                stock_data = self.get_stock_statistics(stock)
                if stock_data['Market Cap'] is not None and stock_data['Enterprise Value'] is not None:
                    self.save_statistic_data(table_name, stock_data)
                    if show:
                        print(stock_data)


    def avg_of_column(self, table_name, column):
        # Execute query to calculate average of column
        query = f"SELECT AVG({column}) FROM {table_name}"
        self.cursor.execute(query)
        
        # Fetch result
        result = self.cursor.fetchone()[0]

        return result
    

    def avg_with_filter(self, table_name, column_number, filter_low, filter_high):
        statiistic_table = self.load_table(table_name)
        column_list = []
        for item in statiistic_table:
            column_list.append(item[column_number])

        # Remove None values
        column_list = [x for x in column_list if x is not None]

        # Filter data 
        column_list = [x for x in column_list if x >= filter_low and x <= filter_high]
        
        avg_of_column_list = sum(column_list) / len(column_list)

        return avg_of_column_list


    def load_table(self, table):
        rows_list = []
        # Execute the SELECT query to fetch all rows from the table
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)

        # Fetch all rows
        rows = self.cursor.fetchall()

        # Process the rows (print in this example)
        for row in rows:
            rows_list.append(row)

        return rows_list
    

