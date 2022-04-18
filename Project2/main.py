from blockchain import Blockchain
from car_sharing import Owner, Car, Customer


def show_initial_balance(cust_balance, owner_balance):
    print("Initial Customer balance: %s" % (cust_balance,))
    print("Initial Owner balance: %s\n" % (owner_balance,))

def show_final_balance(cust_balance, owner_balance):
    print("Balance after transaction for Customer: %s" % (cust_balance,))
    print("Balance after transaction for Owner: %s\n" % (owner_balance,))


def start():
    blockchain = Blockchain()
    customer = Customer(500)
    owner = Owner(500)
    eth = 50

    show_initial_balance(customer.balance, owner.balance)

    #1
    owner.deploy(eth, blockchain)

    #2
    customer.request_book(eth, blockchain)

    #3
    user = input("Enter yes if you want to add car:" )
    
    cars = {"Honda Civic" : "10",
            "Ford Focus" : "15",
            "Tesla Model X" : "20"}
    #vehicles = []
    
    if user == "yes": 
     x = "yes"
     #print(x)
     no_cars = input ("Enter the number of cars you want to add: " )
     number = int(no_cars)
     while (x == "yes") : 
          for i in range(number):
             car = input("Enter your car name:" )
             price  = input ("Enter rent of car per day:"  )
             daily_price = int(price)
             cars[car.title()] = daily_price
          # print("Enter Car details : ")  
           
           
          # cars. append(car)  
          #owner.add_car_to_rent(daily_price, car)
          x = input( " Do you wanna add more car, yes or no : ")

     vehicles = list(cars.items())
    #print("1.Honda Civic \n2.Ford Focus\n3.Tesla Model S \n")
    print (cars)
    #print(vehicles)
    vehicle = input("Choose your Vehicle (by entering the name):")
    days = input("Mention number for days car needs to be rented:")     
    ssn = cars.get(vehicle)  
    car = vehicle
    daily_price = ssn
    days_no = int(days)   
    
    owner.add_car_to_rent(daily_price, car)
    print("Details of car selected being added to smart contract" ,owner.add_car_to_rent)
    customer.pass_number_of_days(days_no)
         

    #4
    owner.encrypt_and_store_details(blockchain)
    owner.allow_car_usage()
    

    #5
    customer.access_car()

    #6
    customer.end_car_rental()

    #7
    owner.withdraw_earnings()
    customer.retrieve_balance()

    def show_rental_cost(cost):
          print("Rental cost of ", car ,"for " ,days, "days:", cost)

    show_rental_cost(daily_price*days_no)
    show_final_balance(customer.balance, owner.balance)


if __name__ == '__main__':
    start()
