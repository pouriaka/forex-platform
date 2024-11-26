from Metatrader import *
from Datamine import *
from TechnicalTools import *

class calculator:
    def __init__(self) -> None:
        pass


    # Use this code to find out how much lot you should consider for fix price in any pip diffrence in any symbol
    @staticmethod
    def lot_calculator(symbol="EURUSD", pip_dif=100, pos_money=10, cent=True):
        symbol_info = mt5.symbol_info(symbol)
        pip_value = symbol_info.trade_tick_value
        pip = symbol_info.point
        contract_size = symbol_info.trade_contract_size
        standard_lot = 1/pip

        if cent:
            loss = 0.01 * standard_lot * pip * pip_value * pip_dif
            volume = pos_money / (standard_lot * pip * pip_value * pip_dif)
            max_sl_pip = pos_money / (standard_lot * 0.01 *  pip * pip_value )

            print("For cent account")
            print(f"loss for 0.01 lot is {loss} ¢ ({loss / 100}$)")
            print(f"{symbol} pip = ",pip)
            print(f"{symbol} contract size = ",contract_size)
            print(f"volume size for loss {pos_money} ¢({pos_money / 100} $) in {pip_dif} pip is {volume} lot")
            print(f"Maximum sl with {pos_money} ¢ ({pos_money / 100} $) is {max_sl_pip} pip")
        else:
            loss = 0.01 * standard_lot * pip * pip_value * pip_dif
            volume = pos_money / (standard_lot * pip * pip_value * pip_dif)
            max_sl_pip = pos_money / (standard_lot * 0.01 *  pip * pip_value )

            print("loss for 0.01 lot" , loss)
            print(f"{symbol} pip = ",pip)
            print(f"{symbol} standard lot = ",contract_size)
            print(f"volume size for loss {pos_money} $ in {pip_dif} pip is {volume} lot")
            print(f"Maximum sl with {pos_money} $ is {max_sl_pip} pip")


    @staticmethod
    def percent_spread_calculator(symbol="EURUSD", open_posetion_period="1h"):
        symbol_info = mt5.symbol_info(symbol)
        pip_value = symbol_info.trade_tick_value
        pip = symbol_info.point
        
        data = datamine(open_posetion_period, symbol, 'online', number_data=1000)
        data = data.df()
        data = indicator.atr(data, 256)
        now_atr = data["atr_256"].iloc[-1]

        spread_pip = symbol_info.point * data["spread"].iloc[-1]
        percent_spread = (spread_pip /now_atr ) * 100
        percent_spread = round(percent_spread, 2)

        print(f"avrage percent spread for holding position in {open_posetion_period} is {percent_spread}%")

        return percent_spread


    @staticmethod
    def margin_need_calculator(symbol, volume, price, leverage, cent=True, show=True):  
        symbol_info = mt5.symbol_info(symbol)
        contract_size = symbol_info.trade_contract_size

        # Fix levrage for btcusd
        if "BTCUSD" in symbol.upper():
            leverage = 50

        margin = volume * contract_size * price * (1 / leverage)
        if show:
            if cent:
                print(f"The margin you need for open {volume} lot position is : {round(margin, 3)} ¢ ({round(margin, 3)/100}$)")
            else:
                print(f"The margin you need for open {volume} lot position is : {round(margin, 3)}$")
        return round(margin, 3)


    @staticmethod
    def full_margin_calculator(symbol, balance, price, leverage, cent=True):
        symbol_info = mt5.symbol_info(symbol)
        contract_size = symbol_info.trade_contract_size

        # Fix levrage for btcusd
        if "BTCUSD" in symbol.upper():
            leverage = 50

        volume = balance / (contract_size * price * (1 / leverage))   
        volume = round(volume, 4)
        if cent:
            print(f"You can open {volume * 100} lot in {symbol} with your full margin")
        else:
            print(f"You can open {volume} lot in {symbol} with your full margin")
        return volume


    @staticmethod
    def money_calculator(symbol, volume, pip_dif=None, price_dif=None, cent=True, show=False):
        symbol_info = mt5.symbol_info(symbol)
        pip_value = symbol_info.trade_tick_value
        pip = symbol_info.point
        contract_size = symbol_info.trade_contract_size
        standard_lot = 1/pip
        
        if pip_dif is None and price_dif is None:
            return None
        
        elif pip_dif:
          # money = volume * contract_size * pip * pip_value * pip_dif    This formoul doesen't work good for cripto 
            money = volume * standard_lot * pip * pip_value * pip_dif
            if show:
                if cent:
                    print(f"Change money with {volume} lot of {symbol} in {pip_dif} pip is {money} ¢ ({money/100} $).")
                else:
                    print(f"Change money with {volume} lot of {symbol} in {pip_dif} pip is {money} $.")
                    
        elif price_dif:
            money = volume * standard_lot  * pip_value * price_dif
            if show:
                if cent:
                    print(f"Change money with {volume} lot of {symbol} in {pip_dif} pip is {money} ¢ ({money/100} $).")
                else:
                    print(f"Change money with {volume} lot of {symbol} in {pip_dif} pip is {money} $.")

        return round(money, 4)


    @staticmethod
    def dif_calculator(symbol, volume, money, price_or_pip, show=False):
        symbol_info = mt5.symbol_info(symbol)
        pip_value = symbol_info.trade_tick_value
        pip = symbol_info.point
        contract_size = symbol_info.trade_contract_size
        standard_lot = 1/pip
        
        if price_or_pip == 'pip':
            dif = money / (volume * standard_lot * pip * pip_value)
            if show:
                print(f'The pip_dif that price should change in {symbol} to make {money}$ money is {dif} pip.')

        elif price_or_pip == 'price':
            dif = money / (volume * standard_lot * pip_value)
            if show:
                print(f'The pip_dif that price should change in {symbol} to make {money}$ money is {dif} USD.')

        return dif    






# login = metatrader(51735591, 'Wy7v5r4hu', 'Alpari-MT5-Demo')
# login = metatrader(88959413, 'qR5D36GN4CJ^', 'LiteFinance-MT5-Live')
# login = metatrader(317931, 'iHQLhGKZ28kG74_', 'LiteFinance-MT5-Live')
# login = metatrader(88990864, 'bQ6N8T6V4P1(', 'LiteFinance-MT5-Demo')
# login.start_mt5()

"""
calculator().lot_calculator(symbol="XAUUSD_l", pip_dif=100, pos_money=1000)
calculator().percent_spread_calculator("EURUSD_l", "4h")
calculator().margin_need_calculator("XAUUSD_l", 0.03, 2072, 1000)
"""
# calculator().money_calculator("EURUSD_l", 0.01, 11, show=True, cent=False)
# calculator().money_calculator("USDCHF_l", 0.1, 200, show=True, cent=False)
# calculator().full_margin_calculator("XAUUSD_l", 100, 2011.5, 1000)




