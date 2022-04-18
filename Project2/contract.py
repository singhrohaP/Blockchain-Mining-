from datetime import datetime

# Smart contract used over blockchain
class SmartContract:
    idCounter = 1

    def __init__(self):
        self.id = SmartContract.idCounter
        SmartContract.idCounter += 1
        self.client_balance = 0
        self.owner_balance = 0
        self.booking_details = BookingDetails

# Borrowers balance is pulled
    def retrieve_balance(self):
        return self.client_balance 

# Lenders balance/earnings displayed
    def withdraw_earnings(self):
        return self.owner_balance

# Borrowers balance is added/subtracted by making deposit
    def client_deposit(self, ether):
        self.client_balance += ether

# Lenders balance is added/subtracted by making deposit
    def owner_deposit(self, ether):
        self.owner_balance += ether

# Gives permission for car usage
    def allow_car_usage(self):
        self.booking_details.get_car().allow_to_use()
# Booking details all bundled together
    def add_booking_details(self, booking_details):
        self.booking_details = booking_details
        print("Blockchain update with booking details", booking_details)

# Fetches booking details
    def get_booking_details(self):
        return self.booking_details
    
# The car rental contract terminated
    def end_car_rental(self):
        self.booking_details.get_car().end_rental()
        self.client_balance -= self.booking_details.get_summed_cost()
        self.owner_balance += self.booking_details.get_summed_cost()

# part of booking details   
    def get_car(self):
        return self.booking_details.get_car()

# Booking details such as request with number of days , cost and car attribute

class BookingDetails:
    def __init__(self, car, price_per_day):
        self.car = car
        self.price_per_day = price_per_day
        self.no_of_days = 0
        self.rental_date = datetime.now()

    def request(self, no_of_days):
        self.no_of_days = no_of_days

    def get_summed_cost(self):
        return int(self.price_per_day) * int(self.no_of_days)

    def get_car(self):
        return self.car


