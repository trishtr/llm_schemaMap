-- Target: Data Warehouse (standardized naming convention)
-- This represents the unified target system with consistent naming

CREATE DATABASE IF NOT EXISTS target_datawarehouse;
USE target_datawarehouse;

-- Unified customer dimension table
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    source_system VARCHAR(20) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    registration_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Unified product dimension table
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    source_system VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    product_description TEXT,
    category VARCHAR(50),
    unit_price DECIMAL(8,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    supplier_name VARCHAR(100),
    created_date TIMESTAMP,
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Unified order fact table
CREATE TABLE fact_order (
    order_key INT PRIMARY KEY AUTO_INCREMENT,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    source_system VARCHAR(20) NOT NULL,
    customer_key INT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT,
    payment_method VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

-- Unified order item fact table
CREATE TABLE fact_order_item (
    order_item_key INT PRIMARY KEY AUTO_INCREMENT,
    order_key INT NOT NULL,
    product_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0.00,
    line_total DECIMAL(10,2) GENERATED ALWAYS AS (quantity * (unit_price - discount_amount)) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_key) REFERENCES fact_order(order_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
);

-- Source system mapping table
CREATE TABLE source_system_mapping (
    mapping_id INT PRIMARY KEY AUTO_INCREMENT,
    source_system VARCHAR(20) NOT NULL,
    source_table VARCHAR(100) NOT NULL,
    source_column VARCHAR(100) NOT NULL,
    target_table VARCHAR(100) NOT NULL,
    target_column VARCHAR(100) NOT NULL,
    data_type VARCHAR(50),
    transformation_rule TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert source system mappings for customer data
INSERT INTO source_system_mapping (source_system, source_table, source_column, target_table, target_column, data_type, transformation_rule) VALUES
-- Source 1 mappings
('source1', 'customer_info', 'customer_id', 'dim_customer', 'customer_id', 'INT', 'CAST(customer_id AS VARCHAR(50))'),
('source1', 'customer_info', 'first_name', 'dim_customer', 'first_name', 'VARCHAR(50)', 'first_name'),
('source1', 'customer_info', 'last_name', 'dim_customer', 'last_name', 'VARCHAR(50)', 'last_name'),
('source1', 'customer_info', 'email_address', 'dim_customer', 'email', 'VARCHAR(100)', 'email_address'),
('source1', 'customer_info', 'phone_number', 'dim_customer', 'phone', 'VARCHAR(20)', 'phone_number'),
('source1', 'customer_info', 'date_of_birth', 'dim_customer', 'birth_date', 'DATE', 'date_of_birth'),
('source1', 'customer_info', 'registration_date', 'dim_customer', 'registration_date', 'TIMESTAMP', 'registration_date'),
('source1', 'customer_info', 'is_active', 'dim_customer', 'is_active', 'BOOLEAN', 'is_active'),
('source1', 'customer_info', 'total_orders', 'dim_customer', 'total_orders', 'INT', 'total_orders'),
('source1', 'customer_info', 'total_spent', 'dim_customer', 'total_spent', 'DECIMAL(10,2)', 'total_spent'),

-- Source 2 mappings
('source2', 'Customer', 'CustomerID', 'dim_customer', 'customer_id', 'INT', 'CAST(CustomerID AS VARCHAR(50))'),
('source2', 'Customer', 'FirstName', 'dim_customer', 'first_name', 'VARCHAR(50)', 'FirstName'),
('source2', 'Customer', 'LastName', 'dim_customer', 'last_name', 'VARCHAR(50)', 'LastName'),
('source2', 'Customer', 'Email', 'dim_customer', 'email', 'VARCHAR(100)', 'Email'),
('source2', 'Customer', 'Phone', 'dim_customer', 'phone', 'VARCHAR(20)', 'Phone'),
('source2', 'Customer', 'BirthDate', 'dim_customer', 'birth_date', 'DATE', 'BirthDate'),
('source2', 'Customer', 'CreatedAt', 'dim_customer', 'registration_date', 'TIMESTAMP', 'CreatedAt'),
('source2', 'Customer', 'IsActive', 'dim_customer', 'is_active', 'BOOLEAN', 'IsActive'),
('source2', 'Customer', 'OrderCount', 'dim_customer', 'total_orders', 'INT', 'OrderCount'),
('source2', 'Customer', 'LifetimeValue', 'dim_customer', 'total_spent', 'DECIMAL(10,2)', 'LifetimeValue'),

-- Source 3 mappings
('source3', 'CUSTOMER_MASTER', 'CUST_ID', 'dim_customer', 'customer_id', 'INT', 'CAST(CUST_ID AS VARCHAR(50))'),
('source3', 'CUSTOMER_MASTER', 'CUST_FNAME', 'dim_customer', 'first_name', 'VARCHAR(50)', 'CUST_FNAME'),
('source3', 'CUSTOMER_MASTER', 'CUST_LNAME', 'dim_customer', 'last_name', 'VARCHAR(50)', 'CUST_LNAME'),
('source3', 'CUSTOMER_MASTER', 'CUST_EMAIL', 'dim_customer', 'email', 'VARCHAR(100)', 'CUST_EMAIL'),
('source3', 'CUSTOMER_MASTER', 'CUST_PHONE', 'dim_customer', 'phone', 'VARCHAR(20)', 'CUST_PHONE'),
('source3', 'CUSTOMER_MASTER', 'CUST_DOB', 'dim_customer', 'birth_date', 'DATE', 'CUST_DOB'),
('source3', 'CUSTOMER_MASTER', 'CUST_CREATE_DT', 'dim_customer', 'registration_date', 'TIMESTAMP', 'CUST_CREATE_DT'),
('source3', 'CUSTOMER_MASTER', 'CUST_STATUS', 'dim_customer', 'is_active', 'CHAR(1)', 'CASE WHEN CUST_STATUS = "A" THEN TRUE ELSE FALSE END'),
('source3', 'CUSTOMER_MASTER', 'CUST_ORDER_CNT', 'dim_customer', 'total_orders', 'INT', 'CUST_ORDER_CNT'),
('source3', 'CUSTOMER_MASTER', 'CUST_TOTAL_AMT', 'dim_customer', 'total_spent', 'DECIMAL(10,2)', 'CUST_TOTAL_AMT');

-- Insert source system mappings for product data
INSERT INTO source_system_mapping (source_system, source_table, source_column, target_table, target_column, data_type, transformation_rule) VALUES
-- Source 1 product mappings
('source1', 'product_catalog', 'product_id', 'dim_product', 'product_id', 'INT', 'CAST(product_id AS VARCHAR(50))'),
('source1', 'product_catalog', 'product_name', 'dim_product', 'product_name', 'VARCHAR(100)', 'product_name'),
('source1', 'product_catalog', 'product_description', 'dim_product', 'product_description', 'TEXT', 'product_description'),
('source1', 'product_catalog', 'category_name', 'dim_product', 'category', 'VARCHAR(50)', 'category_name'),
('source1', 'product_catalog', 'unit_price', 'dim_product', 'unit_price', 'DECIMAL(8,2)', 'unit_price'),
('source1', 'product_catalog', 'stock_quantity', 'dim_product', 'stock_quantity', 'INT', 'stock_quantity'),
('source1', 'product_catalog', 'supplier_name', 'dim_product', 'supplier_name', 'VARCHAR(100)', 'supplier_name'),
('source1', 'product_catalog', 'created_date', 'dim_product', 'created_date', 'TIMESTAMP', 'created_date'),
('source1', 'product_catalog', 'last_updated', 'dim_product', 'last_updated', 'TIMESTAMP', 'last_updated'),

-- Source 2 product mappings
('source2', 'Product', 'ProductID', 'dim_product', 'product_id', 'INT', 'CAST(ProductID AS VARCHAR(50))'),
('source2', 'Product', 'ProductTitle', 'dim_product', 'product_name', 'VARCHAR(100)', 'ProductTitle'),
('source2', 'Product', 'ProductDesc', 'dim_product', 'product_description', 'TEXT', 'ProductDesc'),
('source2', 'Product', 'ProductCategory', 'dim_product', 'category', 'VARCHAR(50)', 'ProductCategory'),
('source2', 'Product', 'Price', 'dim_product', 'unit_price', 'DECIMAL(8,2)', 'Price'),
('source2', 'Product', 'InventoryLevel', 'dim_product', 'stock_quantity', 'INT', 'InventoryLevel'),
('source2', 'Product', 'VendorName', 'dim_product', 'supplier_name', 'VARCHAR(100)', 'VendorName'),
('source2', 'Product', 'DateCreated', 'dim_product', 'created_date', 'TIMESTAMP', 'DateCreated'),
('source2', 'Product', 'LastModified', 'dim_product', 'last_updated', 'TIMESTAMP', 'LastModified'),

-- Source 3 product mappings
('source3', 'ITEM_MASTER', 'ITEM_ID', 'dim_product', 'product_id', 'INT', 'CAST(ITEM_ID AS VARCHAR(50))'),
('source3', 'ITEM_MASTER', 'ITEM_NAME', 'dim_product', 'product_name', 'VARCHAR(100)', 'ITEM_NAME'),
('source3', 'ITEM_MASTER', 'ITEM_DESC', 'dim_product', 'product_description', 'TEXT', 'ITEM_DESC'),
('source3', 'ITEM_MASTER', 'ITEM_CAT', 'dim_product', 'category', 'VARCHAR(50)', 'ITEM_CAT'),
('source3', 'ITEM_MASTER', 'ITEM_PRICE', 'dim_product', 'unit_price', 'DECIMAL(8,2)', 'ITEM_PRICE'),
('source3', 'ITEM_MASTER', 'ITEM_STOCK', 'dim_product', 'stock_quantity', 'INT', 'ITEM_STOCK'),
('source3', 'ITEM_MASTER', 'ITEM_SUPPLIER', 'dim_product', 'supplier_name', 'VARCHAR(100)', 'ITEM_SUPPLIER'),
('source3', 'ITEM_MASTER', 'ITEM_CREATE_DT', 'dim_product', 'created_date', 'TIMESTAMP', 'ITEM_CREATE_DT'),
('source3', 'ITEM_MASTER', 'ITEM_UPDATE_DT', 'dim_product', 'last_updated', 'TIMESTAMP', 'ITEM_UPDATE_DT'); 