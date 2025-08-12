-- Source 2: CRM System (PascalCase naming convention)
-- This represents a modern system with different naming patterns

CREATE DATABASE IF NOT EXISTS source2_crm;
USE source2_crm;

-- Customer table with different naming convention
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    BirthDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IsActive BOOLEAN DEFAULT TRUE,
    OrderCount INT DEFAULT 0,
    LifetimeValue DECIMAL(10,2) DEFAULT 0.00
);

-- Product table
CREATE TABLE Product (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductTitle VARCHAR(100) NOT NULL,
    ProductDesc TEXT,
    ProductCategory VARCHAR(50),
    Price DECIMAL(8,2) NOT NULL,
    InventoryLevel INT DEFAULT 0,
    VendorName VARCHAR(100),
    DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    LastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sales order table
CREATE TABLE SalesOrder (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT NOT NULL,
    OrderDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    OrderState VARCHAR(20) DEFAULT 'pending',
    OrderTotal DECIMAL(10,2) NOT NULL,
    DeliveryAddress TEXT,
    PaymentType VARCHAR(30),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- Order line items table
CREATE TABLE OrderLineItem (
    LineItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Qty INT NOT NULL,
    PricePerUnit DECIMAL(8,2) NOT NULL,
    DiscountValue DECIMAL(8,2) DEFAULT 0.00,
    FOREIGN KEY (OrderID) REFERENCES SalesOrder(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- Sample data for Customer
INSERT INTO Customer (FirstName, LastName, Email, Phone, BirthDate, OrderCount, LifetimeValue) VALUES
('Emma', 'Wilson', 'emma.wilson@crm.com', '555-0201', '1987-05-12', 18, 1850.30),
('David', 'Miller', 'david.m@crm.com', '555-0202', '1992-09-18', 6, 450.75),
('Lisa', 'Davis', 'lisa.davis@crm.com', '555-0203', '1989-12-03', 22, 3200.45);

-- Sample data for Product
INSERT INTO Product (ProductTitle, ProductDesc, ProductCategory, Price, InventoryLevel, VendorName) VALUES
('Bluetooth Speaker', 'Portable wireless speaker with deep bass', 'Audio', 89.99, 30, 'SoundTech'),
('Running Shoes', 'Lightweight athletic shoes for runners', 'Footwear', 79.99, 60, 'SportGear'),
('Laptop Stand', 'Adjustable aluminum laptop stand', 'Office', 39.99, 45, 'WorkSpace'); 