from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *

from matplotlib.ticker import AutoMinorLocator, FixedLocator
import mplfinance as mpf
import matplotlib.pyplot as plt 


class plot:
    def __init__(self, df, mpf_ploting_data=None):
        self.df = df
        self.mpf_ploting_data = mpf_ploting_data
        self.addplot = []
        
    
    # This method take mpf_ploting_data and use it to make a list of buy/sell points of technical_column data for us it in mpf ploting
    def technical_column_mpflist(self, technical_column):
        self.df['mpf_ploting_data'] = self.mpf_ploting_data[0]

        def create_new_column(row):
            if row['mpf_ploting_data'] == 0.0:
                return 0
            else:
                return row[technical_column]

        new_column_data = {'technical_mpfcolumn': self.df.apply(create_new_column, axis=1)}
        new_df = self.df.assign(**new_column_data)

        technical_column_mpflist = new_df['technical_mpfcolumn'].tolist()
        technical_column_mpflist = [item if item != 0 else np.nan for item in technical_column_mpflist]

        return  technical_column_mpflist


    def mpf_add_data_nearbuyorsell_points(self, indicator=None, pivot=None, candlesticks=None):

        # Because in this method algoritm we have a lot of columns for adding to df. we seprate it from hole program.
        df = self.df
        distance_counter = 1
        distance_between_data = 0.001

        if indicator:    

            # Find columns that start with 'ind_'
            ind_columns_name = [col for col in self.df.columns if col.startswith('ind_')]  

            for ind_col in ind_columns_name:

                # Make mpf list for each indicator columns
                mpflist_ind_col = self.technical_column_mpflist(ind_col)
                distance_counter += 1
                # Remove no need text for more visibility
                ind_col = ind_col.replace('ind_', '')

                # Make add plot for every data that we have in any columns
                for signal in range(len(self.mpf_ploting_data[0])):
                    if self.mpf_ploting_data[0][signal] == 0:
                        pass
                    else:
                        # We creat a new column for each data that contain all the rows nan except the place of that data
                        single_signal_loc = [None if i != signal else self.mpf_ploting_data[0][i] + (distance_counter * distance_between_data * self.mpf_ploting_data[1][i] )  for i in range(len(self.mpf_ploting_data[0]))]
                        df[f'data{signal}_loc'] = single_signal_loc
                        self.addplot.append(mpf.make_addplot(df[f'data{signal}_loc'] ,type='scatter',markersize=5000 ,marker=f'${ind_col} : {round(mpflist_ind_col[signal], 7)}$', color='blue'))


        if pivot:    

            # Find columns that start with 'piv_'
            piv_columns_name = [col for col in self.df.columns if col.startswith('piv_')] 

            for piv_col in piv_columns_name:
                mpflist_piv_col = self.technical_column_mpflist(piv_col)
                distance_counter += 1
                # Change text for easier to understand
                piv_col = piv_col.replace('piv_', 'pivot ')

                # Make add plot for every data that we have in any columns
                for signal in range(len(self.mpf_ploting_data[0])):
                    if self.mpf_ploting_data[0][signal] == 0:
                        pass
                    else:
                        # We creat a new column for each data that contain all the rows nan except the place of that data
                        single_signal_loc = [None if i != signal else self.mpf_ploting_data[0][i] + (distance_counter * distance_between_data * self.mpf_ploting_data[1][i] ) for i in range(len(self.mpf_ploting_data[0]))]
                        df[f'data{signal}_loc'] = single_signal_loc
                        self.addplot.append(mpf.make_addplot(df[f'data{signal}_loc'] ,type='scatter',markersize=5000 ,marker=f'${piv_col} : {round(mpflist_piv_col[signal], 7)}$', color='blue'))


        if candlesticks:    
            # Find columns that start with 'cdl_'
            cdl_columns_name = [col for col in self.df.columns if col.startswith('cdl_')]  

            for cdl_col in cdl_columns_name:
                mpflist_cdl_col = self.technical_column_mpflist(cdl_col)
                distance_counter += 1
                # Remove no need text for more visibility
                cdl_col = cdl_col.replace('cdl_', '')

                # Make add plot for every data that we have in any columns
                for signal in range(len(self.mpf_ploting_data[0])):
                    if self.mpf_ploting_data[0][signal] == 0:
                        pass
                    else:
                        # We creat a new column for each data that contain all the rows nan except the place of that data
                        single_signal_loc = [None if i != signal else self.mpf_ploting_data[0][i] + (distance_counter * distance_between_data * self.mpf_ploting_data[1][i] )  for i in range(len(self.mpf_ploting_data[0]))]
                        df[f'data{signal}_loc'] = single_signal_loc
                        self.addplot.append(mpf.make_addplot(df[f'data{signal}_loc'] ,type='scatter',markersize=5000 ,marker=f'${cdl_col} : {round(mpflist_cdl_col[signal], 7)}$', color='blue'))

        
    def mpf_plot(self):
        panel_num = 2

        try:
            # Set 'time' column as the DataFrame index
            self.df.set_index('time', inplace=True)
        except:
            pass


        # Add buy_signal and sell_signal plots
        if 'open_buy_points' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['open_buy_points'], type='scatter', markersize=50, marker='^', color='green'))

        if 'close_buy_points' in self.df.columns:
            pale_green = (0.5, 1.0, 0.5, 0.7)  # Pale green in RGBA format, change pale by changing 0.7
            self.addplot.append(mpf.make_addplot(self.df['close_buy_points'], type='scatter', markersize=50, marker='^', color=pale_green))

        if 'open_sell_points' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['open_sell_points'], type='scatter', markersize=50, marker='v', color='red'))
            
        if 'close_sell_points' in self.df.columns:
            pale_red = (1.0, 0.5, 0.5, 0.7)  # Pale red in RGBA format, change pale by changing 0.7
            self.addplot.append(mpf.make_addplot(self.df['close_sell_points'], type='scatter', markersize=50, marker='v', color=pale_red))


        # Add RSI plot if 'rsi' column exists
        if 'ind_rsi14' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['ind_rsi14'], panel=panel_num, color='blue', ylim=(0, 100), ylabel='RSI'))
            self.addplot.append(mpf.make_addplot([70] * len(self.df), panel=panel_num, type='scatter', markersize=1, marker='.', color='black'))
            self.addplot.append(mpf.make_addplot([30] * len(self.df), panel=panel_num, type='scatter', markersize=1, marker='.', color='black'))
            panel_num += 1


        # Add MACD plot if 'ind_macdh_12_26_9' column exists
        if 'ind_macdh_12_26_9' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['ind_macdh_12_26_9'],type='bar',width=0.7,panel=panel_num,
                            color='dimgray',alpha=1,secondary_y=True))
            self.addplot.append(mpf.make_addplot(self.df['ind_macd_12_26_9'],panel=panel_num,color='fuchsia',secondary_y=False))
            self.addplot.append(mpf.make_addplot(self.df['ind_macds_12_26_9'],panel=panel_num,color='b',secondary_y=False))
            self.addplot.append(mpf.make_addplot([0] * len(self.df), panel=panel_num, type='scatter', markersize=1, marker='.', color='black'))


        # Add MACD histogram plot if just 'ind_macd_12_26_9' column exists
        if 'ind_macd_12_26_9' in self.df.columns and 'ind_macdh_12_26_9' not in self.df.columns :
            self.addplot.append(mpf.make_addplot(self.df['ind_macd_12_26_9'],panel=panel_num,color='blue',secondary_y=False))
            self.addplot.append(mpf.make_addplot([0] * len(self.df), panel=panel_num, type='scatter', markersize=1, marker='.', color='black'))
            


        # Add equity plot if 'equity' column exists
        if 'equity' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['equity'], panel=3, color='black', ylabel='equity'))


        # Add pivot points to plots
        if 'piv_st' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st'], type='scatter', markersize=5, marker='.', color='black'))
        if 'piv_st_sup_1' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st_sup_1'], type='scatter', markersize=5, marker='.', color='green'))
        if 'piv_st_res_1' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st_res_1'], type='scatter', markersize=5, marker='.', color='red'))
        if 'piv_st_sup_2' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st_sup_2'], type='scatter', markersize=5, marker='.', color='green'))
        if 'piv_st_res_2' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st_res_2'], type='scatter', markersize=5, marker='.', color='red'))
        if 'piv_st_sup_3' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st_sup_3'], type='scatter', markersize=5, marker='.', color='green'))
        if 'piv_st_res_3' in self.df.columns:
            self.addplot.append(mpf.make_addplot(self.df['piv_st_res_3'], type='scatter', markersize=5, marker='.', color='red'))

        # Add swing wave to plots
        if 'swing' in self.df.columns:
            
            self.addplot.append(mpf.make_addplot(self.df['swing'], color='black'))


        mpf.plot(self.df, type='candle', style='yahoo', volume=True, addplot=self.addplot)


"""
#ecn mt5
login_1 = metatrader(51735591,'Wy7v5r4hu','Alpari-MT5-Demo')
login_1.start_mt5()

#login_2 = metatrader(51740489,'9p8vE0za3','Alpari-MT5-Demo')
#login_2.start_mt5()



#data_1 = datamine('5m', 'EURUSD','offline', '2018-07-06', '2018-07-12')
data_2 = datamine('5m', 'EURUSD','online', '2023-05-03', '2023-05-12')
#data_3 = datamine('5m', 'EURUSD','online', number_data=1000)
#data_4 = datamine('5m', 'EURUSD','offline', number_data=1000)
data_2 = data_2.df()
#data_1 = data_1.df()


pivot_df = pivot(data_2).pivot_standard()
#pivot2_df = pivot(data_2).pivot_standard()

print(pivot_df)
#print(pivot_df)



#data_1 = candlestick().addallcd(data_1)
#data_1 = indicator().atr(data_1, 14)
#my_pivot = pivot(data_2).pivot_standard()

plot(pivot_df).mpf_plot()


_______________________________________________________________________________________________

#ecn mt5
login_1 = metatrader(51735591,'Wy7v5r4hu','Alpari-MT5-Demo')
login_1.start_mt5()

#login_2 = metatrader(51740489,'9p8vE0za3','Alpari-MT5-Demo')
#login_2.start_mt5()



#data_1 = datamine('5m', 'EURUSD','offline', '2018-07-06', '2018-07-12')
data_2 = datamine('5m', 'EURUSD','online', '2023-05-03', '2023-05-06')
#data_3 = datamine('5m', 'EURUSD','online', number_data=1000)
#data_4 = datamine('5m', 'EURUSD','offline', number_data=1000)
data_2 = data_2.df()
data_2 = indicator().rsi(data_2, 14)
data_2 = indicator().ema(data_2, 14)
data_2 = indicator().sma(data_2, 14)
data_2 = pivot(data_2).pivot_standard()
#data_1 = data_1.df()



data_2 = backtest(data_2, 0.00001, "self.df['ind_rsi14'] <= 30", "self.df['ind_rsi14'] <= 50","self.df['ind_rsi14'] >= 70", "self.df['ind_rsi14'] >= 50")
data_2.trading()
df_after_trade = data_2.return_df()
mpf_ploting_data = data_2.return_mpf_ploting_data()

plot_1 = plot(df_after_trade, mpf_ploting_data)
plot_1.mpf_add_data_nearbuyorsell_points(indicator=True)
plot_1.mpf_plot()


print(df_after_trade)

#plot(data_2).mpf_buyorsell_points_technical_datalist()
#print(data_2)

"""

login = metatrader(51735591, 'Wy7v5r4hu', 'Alpari-MT5-Demo')
login.start_mt5()

data = datamine('1d', 'EURUSD','online', number_data=1000)
data = data.df()



data = swing_finder(data, macdhistogram_signal=True, remove_price_minor_swings=True, wave_number_candles=True).Add_swinglist()
print(data.tail(60))

data= indicator().macd_histogram(data)
print(data)

plot_1 = plot(data)

plot_1.mpf_plot()