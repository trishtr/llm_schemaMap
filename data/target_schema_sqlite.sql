-- Target: Data Warehouse (standardized naming convention) - SQLite3 Version
-- This represents the unified target system with consistent naming

-- Unified customer dimension table
CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT UNIQUE NOT NULL,
    source_system TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    birth_date TEXT,
    registration_date TEXT,
    is_active INTEGER DEFAULT 1,
    total_orders INTEGER DEFAULT 0,
    total_spent REAL DEFAULT 0.00,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Unified product dimension table
CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE NOT NULL,
    source_system TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_description TEXT,
    category TEXT,
    unit_price REAL NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    supplier_name TEXT,
    created_date TEXT,
    last_updated TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Unified order fact table
CREATE TABLE fact_order (
    order_key INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT UNIQUE NOT NULL,
    source_system TEXT NOT NULL,
    customer_key INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    order_status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    shipping_address TEXT,
    payment_method TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

-- Unified order item fact table
CREATE TABLE fact_order_item (
    order_item_key INTEGER PRIMARY KEY AUTOINCREMENT,
    order_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount_amount REAL DEFAULT 0.00,
    line_total REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_key) REFERENCES fact_order(order_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
);

-- Source system mapping table
CREATE TABLE source_system_mapping (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system TEXT NOT NULL,
    source_table TEXT NOT NULL,
    source_column TEXT NOT NULL,
    target_table TEXT NOT NULL,
    target_column TEXT NOT NULL,
    data_type TEXT,
    transformation_rule TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Insert source system mappings for customer data
INSERT INTO source_system_mapping (source_system, source_table, source_column, target_table, target_column, data_type, transformation_rule) VALUES
-- Source 1 mappings
('source1', 'customer_info', 'customer_id', 'dim_customer', 'customer_id', 'INTEGER', 'CAST(customer_id AS TEXT)'),
('source1', 'customer_info', 'first_name', 'dim_customer', 'first_name', 'TEXT', 'first_name'),
('source1', 'customer_info', 'last_name', 'dim_customer', 'last_name', 'TEXT', 'last_name'),
('source1', 'customer_info', 'email_address', 'dim_customer', 'email', 'TEXT', 'email_address'),
('source1', 'customer_info', 'phone_number', 'dim_customer', 'phone', 'TEXT', 'phone_number'),
('source1', 'customer_info', 'date_of_birth', 'dim_customer', 'birth_date', 'TEXT', 'date_of_birth'),
('source1', 'customer_info', 'registration_date', 'dim_customer', 'registration_date', 'TEXT', 'registration_date'),
('source1', 'customer_info', 'is_active', 'dim_customer', 'is_active', 'INTEGER', 'is_active'),
('source1', 'customer_info', 'total_orders', 'dim_customer', 'total_orders', 'INTEGER', 'total_orders'),
('source1', 'customer_info', 'total_spent', 'dim_customer', 'total_spent', 'REAL', 'total_spent'),

-- Source 2 mappings
('source2', 'Customer', 'CustomerID', 'dim_customer', 'customer_id', 'INTEGER', 'CAST(CustomerID AS TEXT)'),
('source2', 'Customer', 'FirstName', 'dim_customer', 'first_name', 'TEXT', 'FirstName'),
('source2', 'Customer', 'LastName', 'dim_customer', 'last_name', 'TEXT', 'LastName'),
('source2', 'Customer', 'Email', 'dim_customer', 'email', 'TEXT', 'Email'),
('source2', 'Customer', 'Phone', 'dim_customer', 'phone', 'TEXT', 'Phone'),
('source2', 'Customer', 'BirthDate', 'dim_customer', 'birth_date', 'TEXT', 'BirthDate'),
('source2', 'Customer', 'CreatedAt', 'dim_customer', 'registration_date', 'TEXT', 'CreatedAt'),
('source2', 'Customer', 'IsActive', 'dim_customer', 'is_active', 'INTEGER', 'IsActive'),
('source2', 'Customer', 'OrderCount', 'dim_customer', 'total_orders', 'INTEGER', 'OrderCount'),
('source2', 'Customer', 'LifetimeValue', 'dim_customer', 'total_spent', 'REAL', 'LifetimeValue'),

-- Source 3 mappings
('source3', 'CUSTOMER_MASTER', 'CUST_ID', 'dim_customer', 'customer_id', 'INTEGER', 'CAST(CUST_ID AS TEXT)'),
('source3', 'CUSTOMER_MASTER', 'CUST_FNAME', 'dim_customer', 'first_name', 'TEXT', 'CUST_FNAME'),
('source3', 'CUSTOMER_MASTER', 'CUST_LNAME', 'dim_customer', 'last_name', 'TEXT', 'CUST_LNAME'),
('source3', 'CUSTOMER_MASTER', 'CUST_EMAIL', 'dim_customer', 'email', 'TEXT', 'CUST_EMAIL'),
('source3', 'CUSTOMER_MASTER', 'CUST_PHONE', 'dim_customer', 'phone', 'TEXT', 'CUST_PHONE'),
('source3', 'CUSTOMER_MASTER', 'CUST_DOB', 'dim_customer', 'birth_date', 'TEXT', 'CUST_DOB'),
('source3', 'CUSTOMER_MASTER', 'CUST_CREATE_DT', 'dim_customer', 'registration_date', 'TEXT', 'CUST_CREATE_DT'),
('source3', 'CUSTOMER_MASTER', 'CUST_STATUS', 'dim_customer', 'is_active', 'TEXT', 'CASE WHEN CUST_STATUS = "A" THEN 1 ELSE 0 END'),
('source3', 'CUSTOMER_MASTER', 'CUST_ORDER_CNT', 'dim_customer', 'total_orders', 'INTEGER', 'CUST_ORDER_CNT'),
('source3', 'CUSTOMER_MASTER', 'CUST_TOTAL_AMT', 'dim_customer', 'total_spent', 'REAL', 'CUST_TOTAL_AMT'); 