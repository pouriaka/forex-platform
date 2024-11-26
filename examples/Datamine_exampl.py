from src.Metatrader import *
from src.Datamine import *

#befor using online methods you should use this methods to start metatrader and login to a trading account 
#ID shold be int and other should be str
login = metatrader(11965591,'Wy7v8j9hu','Alpari-MT5-Demo')
login.start_mt5()

#be sure the data set path are corect for loading them 
data_1 = datamine('5m', 'EURUSD','online', '2023,1,3', '2023,3,12')
data_2 = datamine('5m', 'EURUSD','offline', '2017,5,3', '2017,7,12')
data_3 = datamine('5m', 'EURUSD','online', number_data=1000)
data_4 = datamine('5m', 'EURUSD','offline', number_data=1000)
print(data_1.df())
print(data_2.df())
print(data_3.df())
print(data_4.df())