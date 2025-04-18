import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import MagicMock
from datetime import date, datetime
from dao.ICarLeaseRepositoryImpl import ICarLeaseRepositoryImpl
from entity.Customer import Customer
from entity.Vehicle import Vehicle
from entity.Lease import Lease
from entity.Payment import Payment
from exceptions.LeaseNotFoundException import LeaseNotFoundException
from main_module.main import main

@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def car_lease_repo(mock_db_connection):
    return ICarLeaseRepositoryImpl(mock_db_connection)

def test_add_customer(car_lease_repo, mock_db_connection):
    customer = Customer("John", "Doe", "john.doe@example.com", "1234567890")
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value = mock_cursor

    car_lease_repo.add_customer(customer)

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO Customer (firstName, lastName, email, phoneNumber) VALUES (?, ?, ?, ?)",
        customer.get_first_name(), customer.get_last_name(),
        customer.get_email(), customer.get_phone_number())

def test_get_customer_found(car_lease_repo, mock_db_connection):
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value=(1, "John", "Doe", "john.doe@example.com", "1234567890")

    customer = car_lease_repo.get_customer(1)

    assert customer.get_first_name() == "John"
    assert customer.get_last_name() == "Doe"
    assert customer.get_email() == "john.doe@example.com"
    assert customer.get_phone_number() == "1234567890"

def test_get_customer_not_found(car_lease_repo, mock_db_connection):
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    with pytest.raises(Exception):
        car_lease_repo.get_customer(999)

def test_create_lease(car_lease_repo, mock_db_connection):
    lease = Lease(vehicle_id=1, customer_id=1, start_date="2025-04-01", end_date="2025-04-05", type="DailyLease")
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, "Honda", "Civic", 2020, 40.0, "available", 5, 2.5)

    car_lease_repo.create_lease(lease)

    mock_cursor.execute.assert_any_call(
        "INSERT INTO Lease (vehicleID, customerID, startDate, endDate, type) VALUES (?, ?, ?, ?, ?)",
        lease.get_vehicle_id(), lease.get_customer_id(),
        lease.get_start_date(), lease.get_end_date(), lease.get_type())

def test_calculate_lease_cost(car_lease_repo, mock_db_connection):
    lease = Lease(
    vehicle_id=1,
    customer_id=1,
    start_date=datetime.strptime("2025-04-01", "%Y-%m-%d").date(),
    end_date=datetime.strptime("2025-04-07", "%Y-%m-%d").date(),
    type="DailyLease")


def test_record_payment(car_lease_repo, mock_db_connection):
    payment = Payment(lease_id=1, amount=300.0, payment_date=date(2025, 4, 5))
    mock_cursor = MagicMock()
    mock_db_connection.cursor.return_value = mock_cursor

    car_lease_repo.record_payment(payment)

    mock_cursor.execute.assert_called_once_with(
    "INSERT INTO Payment (leaseID, paymentDate, amount) VALUES (?, ?, ?)",
    (payment.get_lease_id(), payment.get_payment_date(), payment.get_amount()))  # Pass as a tuple

def test_get_lease_not_found(car_lease_repo, mock_db_connection):
    mock_cursor=MagicMock()
    mock_db_connection.cursor.return_value=mock_cursor
    mock_cursor.fetchone.return_value=None

    with pytest.raises(LeaseNotFoundException):
        car_lease_repo.get_lease(999)