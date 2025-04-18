import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyodbc
from entity.Customer import Customer
from entity.Vehicle import Vehicle
from entity.Lease import Lease
from entity.Payment import Payment
from exceptions.CarNotFoundException import CarNotFoundException
from exceptions.LeaseNotFoundException import LeaseNotFoundException
from exceptions.CustomerNotFoundException import CustomerNotFoundException


class ICarLeaseRepositoryImpl:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # Customer Management
    def add_customer(self, customer: Customer):
        cursor=self.db_connection.cursor()
        cursor.execute("INSERT INTO Customer (firstName, lastName, email, phoneNumber) VALUES (?, ?, ?, ?)",
                       customer.get_first_name(), customer.get_last_name(), customer.get_email(), customer.get_phone_number())
        self.db_connection.commit()

    def update_customer(self, customer_id: int, customer: Customer):
        cursor=self.db_connection.cursor()
        cursor.execute("UPDATE Customer SET firstName = ?, lastName = ?, email = ?, phoneNumber = ? WHERE customerID = ?",
                       customer.get_first_name(), customer.get_last_name(), customer.get_email(), customer.get_phone_number(), customer_id)
        self.db_connection.commit()

    def get_customer(self, customer_id: int):
        cursor=self.db_connection.cursor()
        cursor.execute("SELECT * FROM Customer WHERE customerID = ?", customer_id)
        row=cursor.fetchone()
        if row:
            customer = Customer(row[1], row[2], row[3], row[4], row[0])  # customerID is row[0]
            print(f"Customer Name: {customer.get_first_name()} {customer.get_last_name()}")
            print(f"Email: {customer.get_email()}")
            print(f"Phone: {customer.get_phone_number()}")
            return customer
        else:
            raise CustomerNotFoundException("Customer not found.")

    # Car Management
    def add_car(self, vehicle: Vehicle):
        cursor=self.db_connection.cursor()
        cursor.execute("""
        INSERT INTO Vehicle (make, model, year, dailyRate, status, passengerCapacity, engineCapacity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        vehicle.get_make(),
        vehicle.get_model(),
        vehicle.get_year(),
        vehicle.get_daily_rate(),
        vehicle.get_status(),
        vehicle.get_passenger_capacity(),
        vehicle.get_engine_capacity()))
        self.db_connection.commit()

    def update_car_availability(self, vehicle_id: int, available: bool):
        cursor=self.db_connection.cursor()
        status='available' if available else 'notAvailable'
        cursor.execute("UPDATE Vehicle SET status = ? WHERE vehicleID = ?", (status, vehicle_id))
        self.db_connection.commit()

    def get_car_info(self, vehicle_id: int):
        cursor=self.db_connection.cursor()
        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = ?", (vehicle_id,))
        row=cursor.fetchone()
        if row:
            return Vehicle(
            make=row[1],
            model=row[2],
            year=row[3],
            daily_rate=row[4],
            status=row[5],
            passenger_capacity=row[6],
            engine_capacity=row[7],
            vehicle_id=row[0])
        else:
            raise CarNotFoundException("Car not found.")

    # Lease Management
    def create_lease(self, lease: Lease):
        cursor=self.db_connection.cursor()
        vehicle_id_to_check=lease.get_vehicle_id()
        print(f"Checking if vehicleID {vehicle_id_to_check} exists in the Vehicle table.")
        cursor.execute("SELECT * FROM Vehicle WHERE vehicleID = ?", vehicle_id_to_check)
        vehicle=cursor.fetchone()
        if vehicle: 
            cursor.execute("INSERT INTO Lease (vehicleID, customerID, startDate, endDate, type) VALUES (?, ?, ?, ?, ?)",
                       lease.get_vehicle_id(), lease.get_customer_id(), lease.get_start_date(), lease.get_end_date(), lease.get_type())
            self.db_connection.commit()
            print(f"Lease created for vehicleID {lease.get_vehicle_id()}.")
        else:
            print(f"Vehicle with ID {lease.get_vehicle_id()} not found in the database.")
            raise CarNotFoundException(f"Vehicle with ID {lease.get_vehicle_id()} not found.")


    def calculate_lease_cost(self, lease: Lease):
        cursor=self.db_connection.cursor()
        cursor.execute("SELECT dailyRate FROM Vehicle WHERE vehicleID = ?", lease.get_vehicle_id())
        row=cursor.fetchone()
        if row:
            daily_rate = row[0]
            duration = (lease.get_end_date() - lease.get_start_date()).days
            return daily_rate * duration
        else:
            raise CarNotFoundException("Car not found for lease.")
        
    def get_lease(self, lease_id: int) -> Lease:
        cursor=self.db_connection.cursor()
        cursor.execute("SELECT leaseID, vehicleID, customerID, startDate, endDate, type FROM Lease WHERE leaseID = ?", lease_id)
        row=cursor.fetchone()
        if row:
           lease=Lease(vehicle_id=row[1], customer_id=row[2], start_date=row[3], end_date=row[4], type=row[5], lease_id=row[0])
           return lease
        else:
           raise LeaseNotFoundException(f"Lease with ID {lease_id} not found.")


    # Payment Handling
    def record_payment(self, payment: Payment):
        cursor=self.db_connection.cursor()
        cursor.execute("INSERT INTO Payment (leaseID, paymentDate, amount) VALUES (?, ?, ?)",
                   (payment.get_lease_id(), payment.get_payment_date(), payment.get_amount())) #Tuple
        self.db_connection.commit()


    def get_payment_history(self, customer_id: int):
        cursor=self.db_connection.cursor()
        cursor.execute("""
        SELECT p.leaseID, p.amount, p.paymentDate
        FROM Payment p
        JOIN Lease l ON p.leaseID = l.leaseID
        WHERE l.customerID = ?
    """, customer_id) 
        rows=cursor.fetchall()
        payments=[] #List
        for row in rows:
            lease_id, amount, payment_date = row
            payment=Payment(lease_id, amount, payment_date)
            payments.append(payment) 
        return payments

    def calculate_total_revenue(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
        SELECT SUM(amount) 
        FROM Payment 
        WHERE leaseID IN (
            SELECT leaseID 
            FROM Lease)""")
        row = cursor.fetchone()
        if row and row[0]:
            return row[0]
        else:
            return 0.0
 

