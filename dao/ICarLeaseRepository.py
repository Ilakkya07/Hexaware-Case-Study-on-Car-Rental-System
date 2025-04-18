import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 

from abc import ABC, abstractmethod
from datetime import date
from entity.Vehicle import Vehicle
from entity.Customer import Customer
from entity.Lease import Lease
from entity.Payment import Payment
from typing import List
class ICarLeaseRepository(ABC):

    # Car Management
    @abstractmethod
    def add_car(self, vehicle: Vehicle) -> None:
        """ Adds a car to the system """
        pass

    @abstractmethod
    def remove_car(self, vehicle_id: int) -> None:
        """ Removes a car from the system by its ID """
        pass

    @abstractmethod
    def list_available_cars(self) -> List[Vehicle]:
        """ Lists all available cars for rental """
        pass

    @abstractmethod
    def list_rented_cars(self) -> List[Vehicle]:
        """ Lists all cars currently rented out """
        pass

    @abstractmethod
    def find_car_by_id(self, vehicle_id: int) -> Vehicle:
        """ Finds a car by its ID """
        pass
    
    # Customer Management
    @abstractmethod
    def add_customer(self, customer: Customer) -> None:
        """ Adds a customer to the system """
        pass

    @abstractmethod
    def remove_customer(self, customer_id: int) -> None:
        """ Removes a customer from the system by their ID """
        pass

    @abstractmethod
    def list_customers(self) -> List[Customer]:
        """ Lists all customers in the system """
        pass

    @abstractmethod
    def find_customer_by_id(self, customer_id: int) -> Customer:
        """ Finds a customer by their ID """
        pass

    # Lease Management
    @abstractmethod
    def create_lease(self, customer_id: int, vehicle_id: int, start_date: date, end_date: date) -> Lease:
        """ Creates a lease for a customer and vehicle """
        pass

    @abstractmethod
    def return_car(self, lease_id: int) -> Lease:
        """ Handles the return of a rented car by lease ID """
        pass

    @abstractmethod
    def list_active_leases(self) -> List[Lease]:
        """ Lists all active leases in the system """
        pass

    @abstractmethod
    def list_lease_history(self) -> List[Lease]:
        """ Lists the history of all leases (returned or completed) """
        pass

    # Payment Handling
    @abstractmethod
    def record_payment(self, lease: Lease, amount: float) -> None:
        """ Records a payment made for a specific lease """
        pass
