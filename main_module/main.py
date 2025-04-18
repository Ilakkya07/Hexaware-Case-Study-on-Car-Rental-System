import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyodbc
from dao.ICarLeaseRepositoryImpl import ICarLeaseRepositoryImpl
from datetime import date
from exceptions.CarNotFoundException import CarNotFoundException
from exceptions.LeaseNotFoundException import LeaseNotFoundException
from entity.Customer import Customer
from entity.Vehicle import Vehicle
from entity.Lease import Lease
from entity.Payment import Payment
from util.DBConnection import DBConnUtil


def main():
    db_connection = DBConnUtil.getConnection()
    car_lease_repo = ICarLeaseRepositoryImpl(db_connection)

    while True:
        print("\nCar Rental System Menu:")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Get Customer Info")
        print("4. Add Car")
        print("5. Update Car Availability")
        print("6. Get Car Info")
        print("7. Create Lease")
        print("8. Calculate Lease Cost")
        print("9. Record Payment")
        print("10. Get Payment History")
        print("11. Calculate Total Revenue")
        print("12. Exit")

        choice = input("Enter your choice (1-12): ")

        if choice == '1':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            customer = Customer(first_name, last_name, email, phone)
            car_lease_repo.add_customer(customer)
            print("Customer added successfully.")

        elif choice == '2':
            customer_id = int(input("Enter customer ID to update: "))
            first_name = input("Enter new first name: ")
            last_name = input("Enter new last name: ")
            email = input("Enter new email: ")
            phone = input("Enter new phone number: ")
            customer = Customer(first_name, last_name, email, phone)
            car_lease_repo.update_customer(customer_id, customer)
            print("Customer updated successfully.")

        elif choice == '3':
            customer_id = int(input("Enter customer ID: "))
            try:
               customer = car_lease_repo.get_customer(customer_id)
               print(f"Customer Info - Name: {customer.get_first_name()} {customer.get_last_name()}, Email: {customer.get_email()}, Phone: {customer.get_phone_number()}")
            except Exception as e:
               print(e)

        elif choice == '4':
            make = input("Enter car make: ")
            model = input("Enter car model: ")
            year = int(input("Enter car year: "))
            daily_rate = float(input("Enter daily rate: "))
            status = input("Enter status (available/notAvailable): ")
            passenger_capacity = int(input("Enter passenger capacity: "))
            engine_capacity = float(input("Enter engine capacity: "))
            vehicle = Vehicle(make, model, year, daily_rate, status, passenger_capacity, engine_capacity)
            car_lease_repo.add_car(vehicle)
            print("Car added successfully.")

        elif choice == '5':
            vehicle_id = int(input("Enter vehicle ID: "))
            available = input("Enter availability status (True/False): ").lower() == 'true'
            car_lease_repo.update_car_availability(vehicle_id, available)
            print("Car availability updated.")

        elif choice == '6':
            vehicle_id = int(input("Enter vehicle ID: "))
            try:
                vehicle = car_lease_repo.get_car_info(vehicle_id)
                print(f"Car Info - Make: {vehicle.get_make()}, Model: {vehicle.get_model()}, Year: {vehicle.get_year()}")
            except Exception as e:
                print(e)

        elif choice == '7':
            try:
                customer_id = int(input("Enter customer ID: "))
                vehicle_id = int(input("Enter vehicle ID: "))
                start_date = input("Enter lease start date (YYYY-MM-DD): ")
                end_date = input("Enter lease end date (YYYY-MM-DD): ")
                lease_type = input("Enter lease type (DailyLease/MonthlyLease): ")
                while lease_type not in ['DailyLease', 'MonthlyLease']:
                    print("Invalid lease type. Please enter 'DailyLease' or 'MonthlyLease'.")
                    lease_type = input("Enter lease type (DailyLease/MonthlyLease): ")
        
                lease = Lease(vehicle_id, customer_id, start_date, end_date, lease_type)
                print(f"Attempting to create lease for vehicle ID {vehicle_id}...")
                car_lease_repo.create_lease(lease)
                print("Lease created successfully.")
            except CarNotFoundException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '8':
            lease_id = int(input("Enter lease ID: "))
            try:
                lease = car_lease_repo.get_lease(lease_id) 
                cost = car_lease_repo.calculate_lease_cost(lease)
                print(f"Total lease cost: {cost}")
            except LeaseNotFoundException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


        elif choice == '9':
            lease_id = int(input("Enter lease ID: "))
            amount = float(input("Enter payment amount: "))
            payment_date = input("Enter payment date (YYYY-MM-DD): ")  
            payment_date = date.fromisoformat(payment_date)  
            payment = Payment(lease_id, amount, payment_date)
            car_lease_repo.record_payment(payment)
            print("Payment recorded successfully.")


        elif choice == '10':
            customer_id = int(input("Enter customer ID: "))
            try:
                payments = car_lease_repo.get_payment_history(customer_id)
                print("Payment History:")    
                if not payments:
                    print("No payments found for this customer.")
                else:
                    for payment in payments:
                        print(f"Lease ID: {payment.get_lease_id()}, Amount: {payment.get_amount()}, Date: {payment.get_payment_date()}")
            except Exception as e:
                print(f"Error: {e}")


        elif choice == '11':
            total_revenue = car_lease_repo.calculate_total_revenue()
            print(f"Total Revenue: {total_revenue}")

        elif choice == '12':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
