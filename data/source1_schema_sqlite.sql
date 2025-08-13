-- Source 1: E-commerce Platform (snake_case naming convention) - SQLite3 Version
-- This represents a legacy system with traditional database naming

-- Customer information table
CREATE TABLE customer_info (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email_address TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    date_of_birth TEXT,
    registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    total_orders INTEGER DEFAULT 0,
    total_spent REAL DEFAULT 0.00
);

-- Product catalog table
CREATE TABLE product_catalog (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_description TEXT,
    category_name TEXT,
    unit_price REAL NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    supplier_name TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Order details table
CREATE TABLE order_details (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    order_status TEXT DEFAULT 'pending',
    total_amount REAL NOT NULL,
    shipping_address TEXT,
    payment_method TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer_info(customer_id)
);

-- Order items table
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_ordered INTEGER NOT NULL,
    unit_price_at_time REAL NOT NULL,
    discount_amount REAL DEFAULT 0.00,
    FOREIGN KEY (order_id) REFERENCES order_details(order_id),
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id)
);

-- Sample data for customer_info
INSERT INTO customer_info (first_name, last_name, email_address, phone_number, date_of_birth, total_orders, total_spent) VALUES
('John', 'Smith', 'john.smith@email.com', '555-0101', '1985-03-15', 12, 1250.75),
('Sarah', 'Johnson', 'sarah.j@email.com', '555-0102', '1990-07-22', 8, 890.50),
('Michael', 'Brown', 'mike.brown@email.com', '555-0103', '1988-11-08', 15, 2100.25);

-- Sample data for product_catalog
INSERT INTO product_catalog (product_name, product_description, category_name, unit_price, stock_quantity, supplier_name) VALUES
('Wireless Headphones', 'High-quality wireless headphones with noise cancellation', 'Electronics', 199.99, 50, 'TechCorp'),
('Organic Cotton T-Shirt', 'Comfortable organic cotton t-shirt', 'Clothing', 29.99, 100, 'EcoFashion'),
('Smartphone Case', 'Durable protective case for smartphones', 'Accessories', 19.99, 75, 'ProtectPro');

-- Sample data for order_details
INSERT INTO order_details (customer_id, order_date, order_status, total_amount, shipping_address, payment_method) VALUES
(1, '2024-01-15 10:30:00', 'completed', 299.98, '123 Main St, City, State', 'credit_card'),
(2, '2024-01-16 14:20:00', 'shipped', 89.97, '456 Oak Ave, Town, State', 'paypal'),
(3, '2024-01-17 09:15:00', 'pending', 159.99, '789 Pine Rd, Village, State', 'credit_card');

-- Sample data for order_items
INSERT INTO order_items (order_id, product_id, quantity_ordered, unit_price_at_time, discount_amount) VALUES
(1, 1, 1, 199.99, 0.00),
(1, 3, 1, 19.99, 0.00),
(2, 2, 3, 29.99, 0.00),
(3, 1, 1, 159.99, 0.00); 