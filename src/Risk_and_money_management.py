from Metatrader import *
from Datamine import *
from TechnicalTools import *
from Backtest import *

import os
import datetime


# Example for pos percent: pos_percent=0.05 for 5%
class money_management:
    def __init__(self):
        self.filename = 'D:/project/python_pr/forex_platform/src/money_management_history.txt'
        self.filename_riskfree = 'D:/project/python_pr/forex_platform/src/riskfree.txt'
        

    @staticmethod
    def get_last_line(input_string):
        # Split the input string into lines
        lines = input_string.split('\n')

        # Filter out any empty lines
        non_empty_lines = [line for line in lines if line.strip() != '']

        # Return the last non-empty line
        if non_empty_lines:
            return non_empty_lines[-1]
        else:
            return None  # If the string is empty or contains only empty lines


    @staticmethod
    def remove_pattern(input_string, pattern):
        return input_string.replace(pattern, '')


    def update_account_info(self):
        # Get account information
        self.account_info = mt5.account_info()
        self.account_balance = self.account_info.balance
        self.equity = self.account_info.equity
    
    
    def money_management_calculation(self):
        self.update_account_info()
        self.pos_money = self.account_balance * self.pos_percent
        self.period_money = self.account_balance * self.period_percent

        return {'pos_money': self.pos_money, 
                'period_money': self.period_money, 
                'account_balance': self.account_balance}


    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = file.read()
                # If file is not empty, we read the last line of it
                if len(data) != 0:
                    last_line = self.get_last_line(data)
                    last_run_str, week_number_str, account_balance_str, pos_money_str, period_money_str = last_line.split(',')
                    
                    last_run_str = self.remove_pattern(last_run_str, 'last_run:')
                    week_number_str = self.remove_pattern(week_number_str, 'week_number:')
                    account_balance_str = self.remove_pattern(account_balance_str, 'account_balance:')
                    pos_money_str = self.remove_pattern(pos_money_str, 'pos_money:')
                    period_money_str = self.remove_pattern(period_money_str, 'period_money:')

                    return {'last_run': datetime.datetime.strptime(last_run_str, '%Y-%m-%d %H:%M:%S.%f'),
                            'week_number': int(week_number_str),
                            'account_balance': float(account_balance_str),
                            'pos_money': float(pos_money_str),
                            'period_money': float(period_money_str)}
                
        return None


    def save_data(self, filename, data):
        # At first we opne and check file that if it is not empty, we write to the next line
        run_info = self.load_data(self.filename)
        if run_info is not None:
            with open(filename, 'a') as file:  # Open the file in 'a' mode (append)
                file.write(f"\nlast_run:{data['last_run']},"
                f"week_number:{data['week_number']},"
                f"account_balance:{data['account_balance']},"
                f"pos_money:{data['pos_money']},"
                f"period_money:{data['period_money']}")
        else:
            with open(filename, 'a') as file:  # Open the file in 'a' mode (append)
                file.write(f"last_run:{data['last_run']},"
                f"week_number:{data['week_number']},"
                f"account_balance:{data['account_balance']},"
                f"pos_money:{data['pos_money']},"
                f"period_money:{data['period_money']}")

    
    def calculate(self, output, pos_percent, period_percent, period_seconds=None, period_days=None):
        self.pos_percent = pos_percent
        self.period_percent = period_percent
        self.period_seconds = period_seconds
        self.period_days = period_days   

        if self.period_days is None and self.period_seconds is None:
            print("You shold fill one of the period_days or period_seconds")
            return None

        if self.period_days is not None and self.period_seconds is not None:
            print("You shold fill one of the period_days or period_seconds")
            return None

        # Load previous run information
        run_info = self.load_data(self.filename)

        # This code is for priod with sconds up to hours period update
        if  self.period_seconds is not None:
            if run_info is None  or (datetime.datetime.now() - run_info['last_run']).seconds >= self.period_seconds:
                # Perform calculation if it's the first run or 1 minutes have passed
                result = self.money_management_calculation()

                # Update run information
                run_info = {'last_run': datetime.datetime.now(), 
                            'week_number': datetime.datetime.now().isocalendar()[1],
                            'account_balance': result['account_balance'],
                            'pos_money': result['pos_money'], 
                            'period_money': result['period_money']}
                self.save_data(self.filename, run_info)

                print(f"New calculation set--------------------"
                      f"\npos_money:{result['pos_money']}, period_money:{result['period_money']}")

            else:
                # If there is no update information, we fill the parameter with last information
                self.pos_money = run_info['pos_money']
                self.period_money = run_info['period_money']
                self.account_balance = run_info['account_balance']
                print(f"No calculation needed for this {self.period_seconds} seconds interval.")
                
        # This code is for days period update
        if self.period_days is not None:
            if run_info is None  or (datetime.datetime.now() - run_info['last_run']).days >= self.period_days:
                # Perform calculation if it's the first run or 1 minutes have passed
                result = self.money_management_calculation()

                # Add account balance to other information
                account_info = mt5.account_info()
                account_balance = account_info.balance

                # Update run information
                run_info = {'last_run': datetime.datetime.now(), 
                            'week_number': datetime.datetime.now().isocalendar()[1],
                            'account_balance': result['account_balance'],
                            'pos_money': result['pos_money'], 
                            'period_money': result['period_money']}
                self.save_data(self.filename, run_info)

                print(f"New calculation set--------------------"
                      f"\npos_money:{result['pos_money']}, period_money:{result['period_money']}")

            else: 
                # If there is no update information, we fill the parameter with last information
                self.pos_money = run_info['pos_money']
                self.period_money = run_info['period_money']
                self.account_balance = run_info['account_balance']
                print(f"No calculation needed for this {self.period_days} days interval.")

        if output == "pos":
            return self.pos_money 
        elif output == "period":
            return self.period_money
        else:
            return self.account_balance


    # Load riskfree txt file
    def load_riskfree_pos(self):
        if os.path.exists(self.filename_riskfree):
            with open(self.filename_riskfree, 'r') as file:
                data = file.read()
                if len(data) != 0:
                    return data       
        return None
    

    # This method add riskfree position ticket to riskfree txt file
    def note_riskfree_pos(self, pos_tiket):
        # At first we opne and check file that if it is not empty, we write to the next line
        run_info = self.load_riskfree_pos()
        if run_info is not None:
            with open(self.filename_riskfree, 'a') as file:
                # Write the string to the file
                file.write(f"\n{pos_tiket}")
        else:
            with open(self.filename_riskfree, 'a') as file:
                # Write the string to the file
                file.write(f"{pos_tiket}")


    # This method remove the the riskfree positions that doesn't exist
    def check_exist_riskfree_pos(self):
        all_pos_ticket = [] 
        riskfree_pos = []

        # Get all open positions
        open_positions = mt5.positions_get()
        for position in open_positions:
            all_pos_ticket.append(str(position.ticket))

        # Get riskfree positions
        riskfree_positions = self.load_riskfree_pos()
        if riskfree_positions is not None:
            # Split the multiline string into a list of lines
            riskfree_pos = riskfree_positions.splitlines()  

        # Get exist riskfree positions
        exist_pos = []
        for pos in riskfree_pos:
            for open_pos in all_pos_ticket:
                if pos == open_pos:
                    exist_pos.append(pos)

        line_count = 0
        # Open the file in write mode to clear its contents
        with open(self.filename_riskfree, 'w') as file:
            for pos in exist_pos:
                if line_count == 0:
                    # Write the string to the file
                    file.write(f"{pos}")
                else:
                    # Write the string to the file
                    file.write(f"\n{pos}")

                line_count += 1

        return exist_pos


    # This method return ticket of riskfree or inrisk open positions
    # If position with two part tp for riskfree is exist, this method doesen't sense
    def check_position_risk(self, inrisk_or_riskfree):
        # Get all open positions
        open_positions = mt5.positions_get()
        riskfree_positions = []
        inrisk_positions = []
        for pos in open_positions:
            pos_info = pos[0]
            pos_sl = pos_info.sl
            pos_entry = pos_info.price_open
            # 1 for short (sell)
            if pos_info.type == 1:
                if pos_entry > pos_sl:
                    riskfree_positions.append(pos_info.ticket)
                else:
                    inrisk_positions.append(pos_info.ticket)

            # 0 for long (buy)
            else:
                if pos_entry < pos_sl:
                    riskfree_positions.append(pos_info.ticket)
                else:
                    inrisk_positions.append(pos_info.ticket)

        if inrisk_or_riskfree == "inrisk":
            return inrisk_positions
        else:
            return riskfree_positions


    # This method calculate all the money in risk by postions sl
    # Becareful save all risk free positions in riskfree.txt file
    def check_money_in_risk(self):    
        all_pos = [] 
        no_sl_pos = []
        money_in_risk = 0
        # Get all open positions
        open_pos = mt5.positions_get()
        for pos in open_pos:
            all_pos.append(str(pos.ticket))

        # Check riskfree positions from txt file
        riskfree_pos = self.check_exist_riskfree_pos()
        inrisk_pos = [item for item in all_pos if item not in riskfree_pos]
        
        # Calculate all the money in risk from in risk positions
        for pos in inrisk_pos:
            pos_info = mt5.positions_get(ticket=int(pos))
            pos_info = pos_info[0]
            if pos_info.sl != 0:
                # Calculate money that position get it in risk
                sl_size = abs(pos_info.sl - pos_info.price_open)
                pip = mt5.symbol_info(pos_info.symbol).point
                sl_pip = sl_size / pip
                pip_value = mt5.symbol_info(pos_info.symbol).trade_tick_value
                standard_lot = 1/pip
                money = pos_info.volume * standard_lot * pip * pip_value * sl_pip
                money_in_risk += money
            else:
                no_sl_pos.append(pos)
                
        print("The list of no sl positions ticket is:", no_sl_pos)
        return money_in_risk


    # This method take your money management strategy and check if you can open position whith your in risk positions and account loss
    def check_money_management(self, pos_percent, period_percent, period_seconds=None, period_days=None):
        # You can set priod of update money management strategy by seconds and days
        if self.period_days is None and self.period_seconds is None:
            print("You shold fill one of the period_days or period_seconds")
            return None

        if self.period_days is not None and self.period_seconds is not None:
            print("You shold fill one of the period_days or period_seconds")
            return None
        
        # Calculate the total money can loss in a period and initial balance by money management strategy
        if period_seconds:
            money_can_risk = self.calculate("period", pos_percent, period_percent, period_seconds=period_seconds)
            start_period_balance = self.calculate("balance", self.pos_percent, self.period_percent, period_days=period_days)
        if period_days:
            money_can_risk = self.calculate("period", self.pos_percent, self.period_percent, period_days=period_days)
            start_period_balance = self.calculate("balance", self.pos_percent, self.period_percent, period_days=period_days)

        # Calculate all money in risk by no riskfree open positions  
        money_in_risk = self.check_money_in_risk()

        # Calculate the money loss from start of the period
        account_info = mt5.account_info()
        now_balance = account_info.balance
        change_balance = start_period_balance - now_balance
        if change_balance >= 0:
            money_loss_inperiod = 0
        else:
            money_loss_inperiod = abs(start_period_balance - now_balance)

        if money_can_risk - money_in_risk - money_loss_inperiod > 0:
            print("You can open position due to money management")
            return True
        elif money_can_risk - money_loss_inperiod <= 0:
            print("You can't open position because you have loss all period money")
            return False
        else:
            print(f"You can't open position because you have {money_in_risk} money in risk")
            print(f"and you loss {money_loss_inperiod}")
            print(f"This is more than {period_percent * 100}% of your balance")
            return False



class risk_management:
    def __init__(self, pos_RR):
        self.pos_RR = pos_RR
        self.filename = 'D:/project/python_pr/forex_platform/src/risk_management_history.txt'
        self.sequence = [1, 1, 2, 3]


    def update_account_info(self):
        # Get account information
        self.account_info = mt5.account_info()
        self.balance = self.account_info.balance
        self.equity = self.account_info.equity
    

    @staticmethod
    def get_last_line(input_string):
        # Split the input string into lines
        lines = input_string.split('\n')

        # Filter out any empty lines
        non_empty_lines = [line for line in lines if line.strip() != '']

        # Return the last non-empty line
        if non_empty_lines:
            return non_empty_lines[-1]
        else:
            return None  # If the string is empty or contains only empty lines


    @staticmethod
    def remove_pattern(input_string, pattern):
        return input_string.replace(pattern, '')


    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = file.read()
                
                # If file is not empty, we read the last line of it
                if len(data) != 0:
                    last_line = self.get_last_line(data)
                    last_run_str, RR2_str, RR3_str, RR4_str = last_line.split(',')
                    
                    last_run_str = self.remove_pattern(last_run_str, 'last_run:')
                    RR2_str = self.remove_pattern(RR2_str, 'RR_2:')
                    RR3_str = self.remove_pattern(RR3_str, 'RR_3:')
                    RR4_str = self.remove_pattern(RR4_str, 'RR_4:')

                    return {'last_run': datetime.datetime.strptime(last_run_str, '%Y-%m-%d %H:%M:%S.%f'),
                            'RR_2': int(RR2_str),
                            'RR_3': int(RR3_str),
                            'RR_4': int(RR4_str)}
                
        return None


    def save_data(self, filename, data):
        # At first we opne and check file that if it is not empty, we write to the next line
        run_info = self.load_data(self.filename)
        if run_info is not None:
            with open(filename, 'a') as file:  # Open the file in 'a' mode (append)
                file.write(f"\nlast_run:{data['last_run']},"
                f"RR_2:{data['RR_2']},"
                f"RR_3:{data['RR_3']},"
                f"RR_4:{data['RR_4']}")
        else:
            with open(filename, 'a') as file:  # Open the file in 'a' mode (append)
                file.write(f"last_run:{data['last_run']},"
                f"RR_2:{data['RR_2']},"
                f"RR_3:{data['RR_3']},"
                f"RR_4:{data['RR_4']}")


    def calculate(self):
        # Load previous run information
        run_info = self.load_data(self.filename)

        # Define counters for the first time, else load the last values in our variables
        if run_info is None:
            self.RR2_conter = 0
            self.RR3_conter = 0
            self.RR4_conter = 0
        else:
            self.RR2_conter = run_info['RR_2']
            self.RR3_conter = run_info['RR_3']
            self.RR4_conter = run_info['RR_4']

        # Update RR counter 
        if self.pos_RR < 3:
            if self.RR2_conter < 3:
                self.RR2_conter += 1
                coefficient = self.sequence[self.RR2_conter]
            else:
                self.RR2_conter = 0
                coefficient = self.sequence[self.RR2_conter]

        elif self.pos_RR < 4:
            if self.RR3_conter < 3:
                self.RR3_conter += 1
                coefficient = self.sequence[self.RR3_conter]
            else:
                self.RR3_conter = 0
                coefficient = self.sequence[self.RR3_conter]

        else:
            if self.RR4_conter < 3:
                self.RR4_conter += 1
                coefficient = self.sequence[self.RR4_conter]
            else:
                self.RR4_conter = 0
                coefficient = self.sequence[self.RR4_conter]

        # Update run information
        run_info = {'last_run': datetime.datetime.now(), 
                    'RR_2': self.RR2_conter,
                    'RR_3': self.RR3_conter, 
                    'RR_4': self.RR4_conter}
        self.save_data(self.filename, run_info)
        print(run_info)

        return coefficient


"""
login = metatrader(51735591, 'Wy7v5r4hu', 'Alpari-MT5-Demo')
login.start_mt5()
period_money = money_management().calculate("balance", 0.01, 0.03, period_seconds=60)
print(period_money)
a = risk_management(3.5).calculate()
print(a)



order_info = mt5.positions_get(ticket=192112917)
position_info = mt5.positions_get(ticket=192112917)
# Extract the TradePosition object from the tuple
trade_position = position_info[0]

print("-------------------------",trade_position.sl)


print(money_management().check_money_in_risk())
"""