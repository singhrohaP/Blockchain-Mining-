from contract import SmartContract, BookingDetails

# Owner related details in smart contract
class Owner:
    def __init__(self, balance):
        self.contract = SmartContract
        self.balance = balance

# Adding a car to the contract
    def add_car_to_rent(self, day_price, car_info):
        car = Car(car_info)
        self.contract.add_booking_details(BookingDetails(car, day_price))

# Deploy it into blockchain
    def deploy(self, ether, blockchain):
        self.balance -= ether
        self.contract = SmartContract()
        self.contract.owner_deposit(ether)
        blockchain.add_new_transaction(self.contract)

# Details of earnings made from rentals
    def withdraw_earnings(self):
        self.balance += self.contract.withdraw_earnings()

#
    def allow_car_usage(self):
        self.contract.allow_car_usage()

    def encrypt_and_store_details(self, blockchain):
        blockchain.mine()
        
# Customer related details in smart contract
class Customer:
    def __init__(self, balance):
        self.balance = balance
        self.contract = SmartContract

    def request_book(self, ether, blockchain):
        self.contract = blockchain.get_unconfirmed_transactions()[0]
        self.contract.client_deposit(ether)
        self.balance -= ether

    def pass_number_of_days(self, days_no):
        self.contract.get_booking_details().request(days_no)

    def retrieve_balance(self):
        self.balance += self.contract.retrieve_balance()

    def end_car_rental(self):
        self.contract.end_car_rental()

    def access_car(self):
        self.contract.get_car().access()

# Car related details in smart contract
class Car:
    def __init__(self, car_info, **kwargs):
        self.car_info = car_info
        self.additional = kwargs
        self.is_rented = False
        self.allowed_to_use = False

# Renting state updated
    def access(self):
        print("Car access has been granted")
        self.is_rented = True

# Renting state updated
    def end_rental(self):
        print("Car access has been terminated")
        self.is_rented = False

# Car allowance given as rental is in effect
    def allow_to_use(self):
        self.allowed_to_use = True





