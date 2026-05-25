CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    region_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    segment VARCHAR(100),
    region_id INTEGER REFERENCES regions(region_id),
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    unit_cost NUMERIC(12,2),
    unit_price NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) REFERENCES products(product_id),
    warehouse_location VARCHAR(100),
    stock_on_hand INTEGER,
    reorder_level INTEGER,
    last_restock_date DATE
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id VARCHAR(20) PRIMARY KEY,
    sale_date TIMESTAMP NOT NULL,
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    product_id VARCHAR(20) REFERENCES products(product_id),
    region_id INTEGER REFERENCES regions(region_id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2),
    unit_cost NUMERIC(12,2),
    discount_rate NUMERIC(5,2),
    revenue NUMERIC(14,2),
    cost NUMERIC(14,2),
    profit NUMERIC(14,2),
    sale_month VARCHAR(7),
    gross_revenue NUMERIC(14,2),
    net_revenue NUMERIC(14,2),
    profit_margin NUMERIC(8,4)
);

CREATE INDEX IF NOT EXISTS idx_sales_sale_date ON sales (sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer_id ON sales (customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales (product_id);
CREATE INDEX IF NOT EXISTS idx_sales_region_id ON sales (region_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory (product_id);
CREATE INDEX IF NOT EXISTS idx_customers_region_id ON customers (region_id);
