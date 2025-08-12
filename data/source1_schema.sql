-- Source 1: E-commerce Platform (snake_case naming convention)
-- This represents a legacy system with traditional database naming

CREATE DATABASE IF NOT EXISTS source1_ecommerce;
USE source1_ecommerce;

-- Customer information table
CREATE TABLE customer_info (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email_address VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0.00
);

-- Product catalog table
CREATE TABLE product_catalog (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    product_description TEXT,
    category_name VARCHAR(50),
    unit_price DECIMAL(8,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    supplier_name VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Order details table
CREATE TABLE order_details (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT,
    payment_method VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customer_info(customer_id)
);

-- Order items table
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity_ordered INT NOT NULL,
    unit_price_at_time DECIMAL(8,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0.00,
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