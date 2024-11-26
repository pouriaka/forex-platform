from data_base import *
from datetime import datetime, timedelta
from Metatrader import *



def cornometr1():
    # Set the target date and time
    target_datetime = datetime(2024, 3, 7, 17, 14, 54)
    # Input the number of milliseconds
    milliseconds_to_add = 200

    # Calculate the target timestamp with milliseconds
    target_timestamp = target_datetime.timestamp() + (milliseconds_to_add / 1000)

    # Calculate the target datetime for milliseconds
    delta = timedelta(milliseconds=milliseconds_to_add)
    target_datetime_with_ms = target_datetime + delta
    print("target time--------",target_datetime_with_ms.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])


    while True:
        # Get the current time
        current_datetime = datetime.now()
        # Compare the current timestamp with the target timestamp
        current_timestamp = current_datetime.timestamp()

        # Compare the current time with the target time
        if current_timestamp >= target_timestamp:
            database().save_user_input("open_volume_pos", "EURUSD_l, bullish, 0.1, 3, 30, 10, 1000")
            # Print the current datetime with milliseconds
            print("save task in data base--------",current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
            break
        else:
            pass
        



login = metatrader(88990864, 'bQ6N8T6V4P1(', 'LiteFinance-MT5-Demo')
#login = metatrader(317931, 'iHQLhGKZ28kG74_', 'LiteFinance-MT5-Live')
login.start_mt5()


cornometr1()
        
        

    

  
