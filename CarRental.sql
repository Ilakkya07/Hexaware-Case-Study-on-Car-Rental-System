create database CarRental;
use CarRental;

--Vehicle table
create table Vehicle 
   ( vehicleID int identity(1,1) primary key,
    make varchar(50),
    model varchar(50),
    year int,
    dailyRate decimal(10, 2),
    status varchar(15)check (status in ('available', 'notAvailable')),
    passengerCapacity int,
    engineCapacity decimal(10,2));

-- Customer table
create table Customer 
   ( customerID int identity(100,1) primary key,
    firstName varchar(50),
    lastName varchar(50),
    email varchar(100),
    phoneNumber varchar(15));

--Lease table
create table Lease 
   ( leaseID int primary key identity(300,1),
    vehicleID int,
    customerID int,
    startDate date,
    endDate date,
    type varchar(50)check(type in ('DailyLease', 'MonthlyLease')),
    foreign key(vehicleID) references Vehicle(vehicleID),
    foreign key(customerID) references Customer(customerID));

-- Payment table
create table Payment 
   ( paymentID int identity (1000,1)primary key,
    leaseID int,
    paymentDate date,
    amount decimal(10, 2),
    foreign key(leaseID) references Lease(leaseID));

-- inserting values

insert into Vehicle (make, model, year, dailyRate, status, passengerCapacity, engineCapacity)values

('Tata', 'Safari', 2022, 1500.00, 'available', 7, 2.0),
('Maruti', 'Baleno', 2021, 1100.00, 'notAvailable', 5, 1.3),
('Mahindra', 'Thar', 2023, 2500.00, 'available', 4, 2.2),
('Hyundai', 'Verna', 2023, 1700.50, 'available', 5, 1.6),
('Honda', 'Civic', 2020, 2200.00, 'available', 5, 1.8),
('Kia', 'Sonet', 2024, 1600.00, 'notAvailable', 5, 1.5),
('Renault', 'Kwid', 2021, 900.00, 'available', 5, 1.0),
('Toyota', 'Fortuner', 2022, 3500.00, 'available', 7, 2.8),
('Ford', 'Endeavour', 2020, 2800.00, 'notAvailable', 7, 3.2),
('Volkswagen', 'Tiguan', 2022, 2000.00, 'available', 5, 2.0);

insert into Customer (firstName, lastName, email, phoneNumber)values
('Ravi', 'Varma', 'ravivarma@gmail.com', '8882345678'),
('Priya', 'Shri', 'priyashri@gmail.com', '9998765432'),
('Riya', 'yadhav', 'riyaa@gmail.com', '8887765432'),
('Aishwarya', 'Rai', 'aishwarya12@gmail.com', '9776654321'),
('Vikram', 'Pandey', 'vikramp10@gmail.com', '9665543210'),
('Dhruv', 'Vikram', 'iamdhruv@gmail.com', '8776654321'),
('Kiran', 'Reddy', 'kiran@gmail.com', '9443321098'),
('Sonia', 'Shah', 'sonia@gmail.com', '9332210987'),
('Mohan', 'Raj', 'mohanraj73@gmail.com', '9221109876'),
('Isha', 'Mahesh', 'isha0703@gmail.com', '9009987654');

insert into Lease (vehicleID, customerID, startDate, endDate, type) values

(1, 100, '2023-01-05', '2023-01-15', 'MonthlyLease'),
(2, 101, '2023-02-10', '2023-02-25', 'DailyLease'),
(3, 102, '2023-03-01', '2023-03-10', 'MonthlyLease'),
(4, 103, '2023-04-01', '2023-04-20', 'DailyLease'),
(5, 104, '2023-05-10', '2023-05-20', 'MonthlyLease'),
(6, 105, '2023-06-01', '2023-06-10', 'MonthlyLease'),
(7, 106, '2023-07-05', '2023-07-15', 'DailyLease'),
(8, 107, '2023-08-10', '2023-08-18', 'MonthlyLease'),
(9, 108, '2023-09-01', '2023-09-10', 'DailyLease'),
(10, 109, '2023-10-05', '2023-10-15', 'MonthlyLease');

insert into Payment (leaseID, paymentDate, amount)values
 
(300, '2023-02-10', 6500.00),
(301, '2023-03-05', 21500.00),
(302, '2023-04-15', 5800.50),
(303, '2023-05-10', 17500.00),
(304, '2023-06-12', 4600.00),
(305, '2023-07-05', 20000.00),
(306, '2023-08-10', 5200.00),
(307, '2023-09-01', 26000.00),
(308, '2023-10-01', 8800.00),
(309, '2023-11-12', 22500.00);



select * from Payment;
select * from Vehicle;
select * from Lease;
select * from Customer;





