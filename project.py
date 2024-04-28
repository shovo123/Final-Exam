import random

class Account:
    def __init__(self, name, email, address, account_type):
        self.account_number = random.randint(10000, 99999)
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")

    def withdraw(self, amount):
        if self.balance < amount:
            print("Withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrew: {amount}")

    def transfer(self, amount, recipient):
        if self.balance < amount:
            print("Insufficient funds")
        elif recipient is None:
            print("Recipient account does not exist")
        else:
            self.balance -= amount
            recipient.balance += amount
            self.transactions.append(f"Transferred: {amount} to {recipient.name}")
            recipient.transactions.append(f"Received: {amount} from {self.name}")

    def check_balance(self):
        return self.balance

    def transaction_history(self):
        return self.transactions

class User:
    def __init__(self):
        self.accounts = []

    def create_account(self, name, email, address, account_type):
        account = Account(name, email, address, account_type)
        self.accounts.append(account)
        return account

    def take_loan(self, account):
        if len(account.transactions) >= 2:
            print("You have already taken the maximum number of loans")
            return
        loan_amount = float(input("Enter loan amount: "))
        account.deposit(loan_amount)
        print("Loan granted successfully")

    def bankrupt(self):
        print("Bank is bankrupt")

class Admin:
    def __init__(self):
        pass

    def create_account(self, user, name, email, address, account_type):
        return user.create_account(name, email, address, account_type)

    def delete_account(self, user, account):
        user.accounts.remove(account)
        print("Account deleted successfully")

    def list_accounts(self, user):
        for account in user.accounts:
            print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}")

    def total_balance(self, user):
        total_balance = sum(account.balance for account in user.accounts)
        print(f"Total available balance: {total_balance}")

    def total_loan(self, user):
        total_loan = sum(sum(account.transactions) for account in user.accounts if 'Deposited' in account.transactions)
        print(f"Total loan amount: {total_loan}")

    def toggle_loan_feature(self):
        global Loan_Feature
        Loan_Feature = not Loan_Feature
        print(f"Loan feature is {'enabled' if Loan_Feature else 'disabled'}")


user = User()
admin = Admin()

Loan_Feature = True

while True:
    print("\n1. Create Account\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Check Balance\n6. Transaction History\n7. Take Loan\n8. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        name = input("Enter name: ")
        email = input("Enter email: ")
        address = input("Enter address: ")
        account_type = input("Enter account type (Savings/Current): ").capitalize()
        account = admin.create_account(user, name, email, address, account_type)
        print(f"Account created successfully. Account Number: {account.account_number}")

    elif choice == 2:
        account_number = int(input("Enter account number: "))
        amount = float(input("Enter amount to deposit: "))
        for acc in user.accounts:
            if acc.account_number == account_number:
                acc.deposit(amount)
                print("Deposit successful")
                break
        else:
            print("Account not found")

    elif choice == 3:
        account_number = int(input("Enter account number: "))
        amount = float(input("Enter amount to withdraw: "))
        for acc in user.accounts:
            if acc.account_number == account_number:
                acc.withdraw(amount)
                break
        else:
            print("Account not found")

    elif choice == 4:
        from_acc_number = int(input("Enter your account number: "))
        to_acc_number = int(input("Enter recipient's account number: "))
        amount = float(input("Enter amount to transfer: "))
        from_acc = None
        to_acc = None
        for acc in user.accounts:
            if acc.account_number == from_acc_number:
                from_acc = acc
            elif acc.account_number == to_acc_number:
                to_acc = acc
        if from_acc is None or to_acc is None:
            print("Account not found")
        else:
            from_acc.transfer(amount, to_acc)

    elif choice == 5:
        account_number = int(input("Enter account number: "))
        for acc in user.accounts:
            if acc.account_number == account_number:
                print(f"Balance: {acc.check_balance()}")
                break
        else:
            print("Account not found")

    elif choice == 6:
        account_number = int(input("Enter account number: "))
        for acc in user.accounts:
            if acc.account_number == account_number:
                print("Transaction History:")
                print("\n".join(acc.transaction_history()))
                break
        else:
            print("Account not found")

    elif choice == 7:
        if Loan_Feature:
            account_number = int(input("Enter account number: "))
            for acc in user.accounts:
                if acc.account_number == account_number:
                    user.take_loan(acc)
                    break
            else:
                print("Account not found")
        else:
            print("Loan feature is disabled")

    elif choice == 8:
        break

    else:
        print("Invalid choice")
