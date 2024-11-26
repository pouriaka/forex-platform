import MetaTrader5 as mt5
import time

from Telegram_notif import *





#This code contain methods for loging and trading with metatrader pc app

class metatrader:
    def __init__(self, username, password, server):
        self.username = int(username)  # Username must be an int
        self.pasword = str(password)  # Password must be a string
        self.server = str(server) # Server must be a string
 

    def start_mt5(self):
        # Attempt to start MT5
        if mt5.initialize(login=self.username, password=self.pasword, server=self.server):
            # Login to MT5
            if mt5.login(login=self.username, password=self.pasword, server=self.server):
                return True
            else:
                print("Login Fail")
                quit()
                return PermissionError
        else:
            print("MT5 Initialization Failed")
            quit()
            return ConnectionAbortedError


    def open_buy_pos(self, symbol, lot, sl=0.0, tp=0.0, magic=1000, type_filling=mt5.ORDER_FILLING_RETURN, deviation=20):
        # display data on the MetaTrader 5 package
        print("MetaTrader5 package author: ", mt5.__author__)
        print("MetaTrader5 package version: ", mt5.__version__)
        
        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        
        # prepare the buy request structure
        
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            quit()
        
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol,True):
                print("symbol_select({}}) failed, exit",symbol)
                quit()
        
        i = 0
        try_num = 0
        while i < 3 and try_num < 3:
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).ask
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": deviation,
                "magic": magic,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": type_filling
            }
            print(request)
            # send a trading request
            result = mt5.order_send(request)

            # Get the current time
            current_datetime = datetime.now()
            print("open buy pos --------", current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

            # check the execution result
            print("1. order_send(): buy {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                i += 1
                print("2. order_send failed, retcode={}".format(result.retcode))
                # request the result as a dictionary and display it element by element
                result_dict=result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field,result_dict[field]))
                    # if this is a trading request structure, display it element by element as well
                    if field=="request":
                        traderequest_dict=result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                print("This order get filed------------------------------------------------------------------------------------------------")
                time.sleep(5)
                pass
                
            else:
                time.sleep(5)
                # check if the position is opened successfully
                position = mt5.positions_get(ticket=result.order)
                if position is not None and position[0].ticket == result.order:
                    print("2. order_send done, opened buy position with POSITION_TICKET={}".format(position[0].ticket))
                    i = 3
                    try_num = 3
                    return result
                else:
                    print("Unexpected position found. Retrying in 5 seconds...")
                    telegram_send_message(f'position for symbol {symbol} is not open I try again') 
                    time.sleep(5)
                    i = 0
                    try_num += 1
                    continue  # continue the while loop and retry
            
        telegram_send_message(f'Openning buy position for {symbol} get faild, check it what is wrong')  


    def open_sell_pos(self, symbol,  lot, sl=0.0, tp=0.0, magic=1000, type_filling=mt5.ORDER_FILLING_RETURN, deviation=20):
        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

        # prepare the buy request structure
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            quit()
        
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol,True):
                print("symbol_select({}}) failed, exit",symbol)
                quit()
        
        i = 0
        try_num = 0
        while i < 3 and try_num < 3:
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).bid
            deviation = 20
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": deviation,
                "magic": magic,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": type_filling
            }
            
            # send a trading request
            result = mt5.order_send(request)

            # Get the current time
            current_datetime = datetime.now()
            print("open sell pos--------", current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
        
            # check the execution result
            print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                i += 1
                print("2. order_send failed, retcode={}".format(result.retcode))
                # request the result as a dictionary and display it element by element
                result_dict=result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field,result_dict[field]))
                    # if this is a trading request structure, display it element by element as well
                    if field=="request":
                        traderequest_dict=result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                
                print("This order openning get filed---------------------------------------------------------------------------------------------")
                time.sleep(5)
                pass
                
            
            else:
                time.sleep(5)
                # check if the position is opened successfully
                position = mt5.positions_get(ticket=result.order)
                if position is not None and position[0].ticket == result.order:
                    print("2. order_send done, opened sell position with POSITION_TICKET={}".format(position[0].ticket))
                    i = 3
                    try_num = 3
                    return result
                else:
                    print("Unexpected position found. Retrying in 5 seconds...")
                    telegram_send_message(f'position for symbol {symbol} is not open I try again') 
                    time.sleep(5)
                    i = 0
                    try_num += 1
                    continue  # continue the while loop and retry

        telegram_send_message(f'Openning sell position for {symbol} get faild, check it what is wrong') 


    def close_buy_pos(self, result):
        result_recive = result
        trade_request = result.request
        i = 0
        try_num = 0
        while i < 3 and try_num < 3:    
            # create a close request
            position_id=result_recive.order
            price=mt5.symbol_info_tick(trade_request.symbol).bid
            request={
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": trade_request.symbol,
                "volume": trade_request.volume,
                "type": mt5.ORDER_TYPE_SELL,
                "position": position_id,
                "price": price,
                "deviation": trade_request.deviation,
                "magic": trade_request.magic,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": trade_request.type_filling,
            }
            # send a trading request
            result=mt5.order_send(request)
            # check the execution result
            print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id, trade_request.symbol,
                                                                                                    trade_request.volume,
                                                                                                    price,
                                                                                                    trade_request.deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                i += 1
                print("4. order_send failed, retcode={}".format(result.retcode))
                print("   result",result)
                #check if pos closed with some thing and now not found
                position = mt5.positions_get(ticket=result_recive.order)
                if position == ():
                    print('position not found , maybe it closed by sl , tp or closed manually ')
                    i = 3
                    try_num = 3
                    print("4. position #{} closed, {}".format(position_id,result))
                    # request the result as a dictionary and display it element by element
                    result_dict=result._asdict()
                    for field in result_dict.keys():
                        print("   {}={}".format(field,result_dict[field]))
                        # if this is a trading request structure, display it element by element as well
                        if field=="request":
                            traderequest_dict=result_dict[field]._asdict()
                            for tradereq_filed in traderequest_dict:
                                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

                    return result
                
                print("This order clossing get filed try to close it after 5 seconde-----------------------------------------------------------------")
                time.sleep(5)

            else:
                #check if it is closed
                position = mt5.positions_get(ticket=result_recive.order)
                if position == ():
                    i = 3
                    try_num = 3
                    print("4. position #{} closed, {}".format(position_id,result))
                    # request the result as a dictionary and display it element by element
                    result_dict=result._asdict()
                    for field in result_dict.keys():
                        print("   {}={}".format(field,result_dict[field]))
                        # if this is a trading request structure, display it element by element as well
                        if field=="request":
                            traderequest_dict=result_dict[field]._asdict()
                            for tradereq_filed in traderequest_dict:
                                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

                    return result
                    
            
                else :
                    print('position doesent close correctly , try again to close it')
                    try_num += 1
                    pass

        telegram_send_message(f'closing buy position with ticket {result_recive.order} for {trade_request.symbol} get faild, check it what is wrong')


    def close_sell_pos(self, result):
        result_recive = result
        trade_request = result.request
        i = 0
        try_num = 0
        while i < 3 and try_num < 3:
            # create a close request
            position_id=result_recive.order
            price=mt5.symbol_info_tick(trade_request.symbol).ask
            request={
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": trade_request.symbol,
                "volume": trade_request.volume,
                "type": mt5.ORDER_TYPE_BUY,
                "position": position_id,
                "price": price,
                "deviation": trade_request.deviation,
                "magic": trade_request.magic,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": trade_request.type_filling,
            }
            # send a trading request
            result=mt5.order_send(request)
            # check the execution result
            print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,
                                                                                                    trade_request.symbol,
                                                                                                    trade_request.volume,
                                                                                                    price,
                                                                                                    trade_request.deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                i += 1
                print("4. order_send failed, retcode={}".format(result.retcode))
                print("   result",result)
                #check if pos closed with some thing and now not found
                position = mt5.positions_get(ticket=result_recive.order)
                if position == ():
                    print('position not found , maybe it closed by sl , tp or closed manually ')
                    i = 3
                    try_num = 3
                    print("4. position #{} closed, {}".format(position_id,result))
                    # request the result as a dictionary and display it element by element
                    result_dict=result._asdict()
                    for field in result_dict.keys():
                        print("   {}={}".format(field,result_dict[field]))
                        # if this is a trading request structure, display it element by element as well
                        if field=="request":
                            traderequest_dict=result_dict[field]._asdict()
                            for tradereq_filed in traderequest_dict:
                                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

                    return result
                
                print("This order clossing get filed try to close it after 5 seconde-----------------------------------------------------------------")
                time.sleep(5)
            
            else:
                time.sleep(5)
                #check if it is closed
                position = mt5.positions_get(ticket=result_recive.order)
                if position == ():
                    i = 3
                    try_num = 3
                    print("4. position #{} closed, {}".format(position_id,result))
                    # request the result as a dictionary and display it element by element
                    result_dict=result._asdict()
                    for field in result_dict.keys():
                        print("   {}={}".format(field,result_dict[field]))
                        # if this is a trading request structure, display it element by element as well
                        if field=="request":
                            traderequest_dict=result_dict[field]._asdict()
                            for tradereq_filed in traderequest_dict:
                                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                    
                    return result
                    
                                
                else:
                    print('position doesent close correctly , try again to close it')
                    try_num += 1
                    pass

                
        telegram_send_message(f'closing sell position with ticket {result_recive.order} for {trade_request.symbol} get faild, check it what is wrong')


    def close_pos(self, ticket):
        pos_info = mt5.positions_get(ticket=ticket)
        pos_info = pos_info[0]
        trade_request = pos_info
        i = 0
        try_num = 0
        # For buy positions
        if trade_request.type == 0:
            while i < 3 and try_num < 3:    
                # create a close request
                position_id=ticket
                price=mt5.symbol_info_tick(trade_request.symbol).bid
                request={
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": trade_request.symbol,
                    "volume": trade_request.volume,
                    "type": mt5.ORDER_TYPE_SELL,
                    "position": position_id,
                    "price": price,
                    "magic": trade_request.magic,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": 0
                }
                # send a trading request
                result=mt5.order_send(request)
                # check the execution result
                print("3. close position #{}: sell {} {} lots at {} ".format(position_id, trade_request.symbol,
                                                                            trade_request.volume,
                                                                            price))
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    i += 1
                    print("4. order_send failed, retcode={}".format(result.retcode))
                    print("   result",result)
                    #check if pos closed with some thing and now not found
                    position = mt5.positions_get(ticket=ticket)
                    if position == ():
                        print('position not found , maybe it closed by sl , tp or closed manually ')
                        i = 3
                        try_num = 3
                        print("4. position #{} closed, {}".format(position_id,result))
                        # request the result as a dictionary and display it element by element
                        result_dict=result._asdict()
                        for field in result_dict.keys():
                            print("   {}={}".format(field,result_dict[field]))
                            # if this is a trading request structure, display it element by element as well
                            if field=="request":
                                traderequest_dict=result_dict[field]._asdict()
                                for tradereq_filed in traderequest_dict:
                                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

                        return result
                    
                    print("This order clossing get filed try to close it after 5 seconde-----------------------------------------------------------------")
                    time.sleep(5)

                else:
                    #check if it is closed
                    position = mt5.positions_get(ticket=ticket)
                    if position == ():
                        i = 3
                        try_num = 3
                        print("4. position #{} closed, {}".format(position_id,result))
                        # request the result as a dictionary and display it element by element
                        result_dict=result._asdict()
                        for field in result_dict.keys():
                            print("   {}={}".format(field,result_dict[field]))
                            # if this is a trading request structure, display it element by element as well
                            if field=="request":
                                traderequest_dict=result_dict[field]._asdict()
                                for tradereq_filed in traderequest_dict:
                                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

                        return result
                    
                    else :
                        print('position doesent close correctly , try again to close it')
                        try_num += 1
                        pass

            telegram_send_message(f'closing buy position with ticket {ticket} for {trade_request.symbol} get faild, check it what is wrong')

        # For sell positions
        elif trade_request.type == 1:
            while i < 3 and try_num < 3:
                # create a close request
                position_id=ticket
                price=mt5.symbol_info_tick(trade_request.symbol).ask
                request={
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": trade_request.symbol,
                    "volume": trade_request.volume,
                    "type": mt5.ORDER_TYPE_BUY,
                    "position": position_id,
                    "price": price,
                    "magic": trade_request.magic,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": 0
                }
                # send a trading request
                result=mt5.order_send(request)
                # check the execution result
                print("3. close position #{}: sell {} {} lots at {} ".format(position_id,
                                                                            trade_request.symbol,
                                                                            trade_request.volume,
                                                                            price))
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    i += 1
                    print("4. order_send failed, retcode={}".format(result.retcode))
                    print("   result",result)
                    #check if pos closed with some thing and now not found
                    position = mt5.positions_get(ticket=ticket)
                    if position == ():
                        print('position not found , maybe it closed by sl , tp or closed manually ')
                        i = 3
                        try_num = 3
                        print("4. position #{} closed, {}".format(position_id,result))
                        # request the result as a dictionary and display it element by element
                        result_dict=result._asdict()
                        for field in result_dict.keys():
                            print("   {}={}".format(field,result_dict[field]))
                            # if this is a trading request structure, display it element by element as well
                            if field=="request":
                                traderequest_dict=result_dict[field]._asdict()
                                for tradereq_filed in traderequest_dict:
                                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

                        return result
                    
                    print("This order clossing get filed try to close it after 5 seconde-----------------------------------------------------------------")
                    time.sleep(5)
                
                else:
                    time.sleep(5)
                    #check if it is closed
                    position = mt5.positions_get(ticket=ticket)
                    if position == ():
                        i = 3
                        try_num = 3
                        print("4. position #{} closed, {}".format(position_id,result))
                        # request the result as a dictionary and display it element by element
                        result_dict=result._asdict()
                        for field in result_dict.keys():
                            print("   {}={}".format(field,result_dict[field]))
                            # if this is a trading request structure, display it element by element as well
                            if field=="request":
                                traderequest_dict=result_dict[field]._asdict()
                                for tradereq_filed in traderequest_dict:
                                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                        
                        return result
                            
                    else:
                        print('position doesent close correctly , try again to close it')
                        try_num += 1
                        pass

            telegram_send_message(f'closing sell position with ticket {ticket} for {trade_request.symbol} get faild, check it what is wrong')




    # For closing all positions 
    def close_all_pos(self):
        positions = mt5.positions_get()
        print(positions)
        for position in positions:
            tick = mt5.symbol_info_tick(position.symbol)
            request={
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "position": position.ticket,
                "price": tick.ask if position.type == 1 else tick.bid,
                "magic": position.magic,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC
            }
            # send a trading request
            result=mt5.order_send(request)
            print(result)


"""
login = metatrader(51735591, 'Wy7v5r4hu', 'Alpari-MT5-Demo')
login.start_mt5()
# For alpari ecn account, we should fill "type_filling" manualy. For fill and kill it is equal to 0.
result = login.open_buy_pos("EURUSD", 1.07736, 1.10414, 0.01, 1001, 0)
print(result)
time.sleep(10)
#login.close_buy_pos(result)
#login.close_all_pos("EURUSD")

"""
