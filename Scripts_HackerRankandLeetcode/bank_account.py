from datetime import datetime, timezone, timedelta


#Bank accounts are stored in this dictionary. Make sure to import this variable if running the BankAccount class as well. 
stored_transactions = dict()


class BankAccount:
    '''
    This class will represent BankAccounts and have the following funtionality:
    Deposit
    Withdraw
    Transfer Funds to another User
    Add Monthly Interest Rate to the BALANCE
    And generate Confirmation number for every transacton
    A way to recall a transaction and its details using the confirmation number
    '''



    routing_num = 67841214
    account_num = 1
    monthly_interest_amt = .02


    def __init__(self, fname, lname, pin, balance):
        self._fname = fname
        self._lname = lname
        self._pin = pin
        self._balance = balance
        self._accountnum = BankAccount.account_num
        BankAccount.account_num += 1

    @property
    def accountnum(self):
        print(self._accountnum)
        return self._accountnum

    @property
    def account_balance(self):
        print(self._balance)
        return self._balance
        
    # Use to directly set the balance of the account
    @account_balance.setter
    def account_balance(self, add_to_balance):
        self._balance += add_to_balance
        print(f'New balance {self._balance}')
        confirm = self.Confirm(self._accountnum, self._fname, self._lname, 'D')
        print(confirm.confirmation_id)
        stored_transactions[f'{confirm.confirmation_id}'] = confirm
        return confirm

# Transfers funds to another user
    def transfer_funds(self, trans_to_account_num, amount):
        if self._balance - amount > 0:
            trans_to_account_num._balance += amount
            self._balance -= amount
        else:
            print(f'you are not that rich.. you only have {self.account_balance} in your account')
        confirm = self.Confirm(self._accountnum, self._fname, self._lname, 'T')
        print(confirm.confirmation_id)
        stored_transactions[f'{confirm.confirmation_id}'] = confirm
        return confirm

# Use to withdraw funds from the account
    def withdraw(self, amount):
        if self._balance > 0:
            if self._balance - amount >=0:
                self._balance-=amount
                print(f'You have withdrawn {amount} and have a new balance of {self._balance}')
            else:
                print('Inseffichiant balance amount, Transaction declined')
        else:
            print('No funds to withdraw, please make a deposit')
        confirm = self.Confirm(self._accountnum, self._fname, self._lname, 'W')
        print(confirm.confirmation_id)
        stored_transactions[f'{confirm.confirmation_id}'] = confirm
        return confirm
        

#Use to deposit an amount into the account
    def deposit(self, amount):
        self._balance += amount
        print(f'You have deposited {amount} and have a NEW BALANCE OF: {self._balance}')
        confirm = self.Confirm(self._accountnum, self._fname, self._lname, 'D')
        print(confirm.confirmation_id)
        stored_transactions[f'{confirm.confirmation_id}'] = confirm
        return confirm

# Used to calculate a monthly interest rate and add that into the accounts. The rate is set as a class atribute. 
    def monthly_interest(self):
        added_amount = self._balance * BankAccount.monthly_interest_amt
        self._balance += added_amount
        confirm = self.Confirm(self._accountnum, self._fname, self._lname, 'I')
        print(confirm.confirmation_id)
        stored_transactions[f'{confirm.confirmation_id}'] = confirm
        return confirm


    #create an object that will house accnum, transcode, trans id, time and time UTC)
    class Confirm:
        transaction_id = 1

        def __init__(self, account, fname, lname, type, ):
            self.account_owner = f'{fname} {lname}'
            self._confirm_account_num = account
            self._confirm_trans_code = type
            self._confirm_trans_id = self.transaction_id
            self.transaction_id += 1
            self._time = datetime.now()
            
        @property
        def confirmation_id(self):
            date_text = str(self._time)
            new_str = ''
            for letter in date_text:
                if letter not in (' ', ':', '-', '.'):
                    new_str += letter
            date = new_str[0:12]
            num = f'{self._confirm_trans_code} - {str(self._confirm_account_num)} - {date} - {self._confirm_trans_id}' 
            return num


    @staticmethod
    def confirm_ids():
        print(stored_transactions)

    @staticmethod
    def confirmation_look_up(id):
        print(stored_transactions[f'{id}'])



user01 = BankAccount('Ryan', 'Phillip', 1234, 10)

user02 = BankAccount('John', 'Homie', 4321, 5)

user03 = BankAccount('Rob', 'Dedrick', 1234, 20)


user03.account_balance
user03.deposit(500)

user03.deposit(50)

user03.withdraw(275)

user02.deposit(125)

user02.account_balance
user02.transfer_funds(user03, 50)
user02.account_balance
