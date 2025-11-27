-- Create Inventory Table (Dimension)
CREATE TABLE IF NOT EXISTS inventory (
    id INT PRIMARY KEY,
    name TEXT,
    category TEXT,
    price DECIMAL(10, 2),
    stock INT,
    last_updated TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Sales Table (Fact)
CREATE TABLE IF NOT EXISTS sales (
    id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    total DECIMAL(10, 2),
    sale_date TIMESTAMP,
    customer TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product
        FOREIGN KEY(product_id) 
        REFERENCES inventory(id)
);
