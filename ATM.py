import datetime


class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transactions = []

    def verify_pin(self, pin):
        return self.pin == pin

    def add_transaction(self, transaction_type, amount):
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)


class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def register_user(self, user_id, pin):
        if user_id in self.users:
            print("User ID already exists. Please try a different User ID.")
        else:
            new_user = User(user_id, pin)
            self.users[user_id] = new_user
            print("User registered successfully.")

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.verify_pin(pin):
            self.current_user = user
            return True
        return False

    def show_transaction_history(self):
        if self.current_user:
            for transaction in self.current_user.transactions:
                print(f"{transaction['date']}: {
                      transaction['type']} - ${transaction['amount']}")
        else:
            print("No user is currently logged in.")

    def withdraw(self, amount):
        if self.current_user:
            if self.current_user.balance >= amount:
                self.current_user.balance -= amount
                self.current_user.add_transaction('Withdraw', amount)
                print(f"Rs.{amount} has been withdrawn.")
            else:
                print("Insufficient balance.")
        else:
            print("No user is currently logged in.")

    def deposit(self, amount):
        if self.current_user:
            self.current_user.balance += amount
            self.current_user.add_transaction('Deposit', amount)
            print(f"Rs.{amount} has been deposited.")
        else:
            print("No user is currently logged in.")

    def transfer(self, target_user_id, amount):
        if self.current_user:
            target_user = self.users.get(target_user_id)
            if target_user:
                if self.current_user.balance >= amount:
                    self.current_user.balance -= amount
                    target_user.balance += amount
                    self.current_user.add_transaction(
                        'Transfer to ' + target_user_id, amount)
                    target_user.add_transaction(
                        'Transfer from ' + self.current_user.user_id, amount)
                    print(f"Rs.{amount} has been transferred to user {
                          target_user_id}.")
                else:
                    print("Insufficient balance.")
            else:
                print(f"User {target_user_id} does not exist.")
        else:
            print("No user is currently logged in.")

    def quit(self):
        self.current_user = None
        print("User logged out.")


def main():
    atm = ATM()

    while True:
        if atm.current_user is None:
            print("\nATM Menu:")
            print("1. Register")
            print("2. Login")
            choice = input("Enter choice: ")

            if choice == '1':
                user_id = input("Enter User ID: ")
                pin = input("Enter PIN: ")
                atm.register_user(user_id, pin)
            elif choice == '2':
                user_id = input("Enter User ID: ")
                pin = input("Enter PIN: ")
                if atm.authenticate_user(user_id, pin):
                    print("Authentication successful.")
                else:
                    print("Authentication failed.")
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\nATM Menu:")
            print("1. Transaction History")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. Quit")
            choice = input("Enter choice: ")

            if choice == '1':
                atm.show_transaction_history()
            elif choice == '2':
                amount = float(input("Enter amount to withdraw: "))
                atm.withdraw(amount)
            elif choice == '3':
                amount = float(input("Enter amount to deposit: "))
                atm.deposit(amount)
            elif choice == '4':
                target_user_id = input("Enter target user ID: ")
                amount = float(input("Enter amount to transfer: "))
                atm.transfer(target_user_id, amount)
            elif choice == '5':
                atm.quit()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
