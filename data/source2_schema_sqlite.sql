-- Source 2: CRM System (PascalCase naming convention) - SQLite3 Version
-- This represents a modern system with different naming patterns

-- Customer table with different naming convention
CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Phone TEXT,
    BirthDate TEXT,
    CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP,
    IsActive INTEGER DEFAULT 1,
    OrderCount INTEGER DEFAULT 0,
    LifetimeValue REAL DEFAULT 0.00
);

-- Product table
CREATE TABLE Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductTitle TEXT NOT NULL,
    ProductDesc TEXT,
    ProductCategory TEXT,
    Price REAL NOT NULL,
    InventoryLevel INTEGER DEFAULT 0,
    VendorName TEXT,
    DateCreated TEXT DEFAULT CURRENT_TIMESTAMP,
    LastModified TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Sales order table
CREATE TABLE SalesOrder (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER NOT NULL,
    OrderDateTime TEXT DEFAULT CURRENT_TIMESTAMP,
    OrderState TEXT DEFAULT 'pending',
    OrderTotal REAL NOT NULL,
    DeliveryAddress TEXT,
    PaymentType TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- Order line items table
CREATE TABLE OrderLineItem (
    LineItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    Qty INTEGER NOT NULL,
    PricePerUnit REAL NOT NULL,
    DiscountValue REAL DEFAULT 0.00,
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

-- Sample data for SalesOrder
INSERT INTO SalesOrder (CustomerID, OrderDateTime, OrderState, OrderTotal, DeliveryAddress, PaymentType) VALUES
(1, '2024-01-15 11:30:00', 'completed', 179.98, '123 Business Ave, City, State', 'credit_card'),
(2, '2024-01-16 15:20:00', 'shipped', 79.99, '456 Corporate Blvd, Town, State', 'paypal'),
(3, '2024-01-17 10:15:00', 'pending', 119.98, '789 Enterprise Dr, Village, State', 'credit_card');

-- Sample data for OrderLineItem
INSERT INTO OrderLineItem (OrderID, ProductID, Qty, PricePerUnit, DiscountValue) VALUES
(1, 1, 1, 89.99, 0.00),
(1, 3, 1, 39.99, 0.00),
(2, 2, 1, 79.99, 0.00),
(3, 1, 1, 89.99, 0.00),
(3, 3, 1, 39.99, 0.00); 