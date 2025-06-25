-- Create database and connect
CREATE DATABASE ecom;
\c ecom;

-- =======================
-- Tablespaces
-- =======================

-- CREATE TABLESPACE ts_data LOCATION '/var/lib/postgresql/ts_data';
-- CREATE TABLESPACE ts_catalogo LOCATION '/var/lib/postgresql/ts_catalogo';
-- CREATE TABLESPACE ts_temp LOCATION '/mnt/temp_pg/ts_temp';

-- Set default tablespaces for this database
ALTER DATABASE ecom SET default_tablespace = 'ts_datos';
ALTER DATABASE ecom SET temp_tablespaces = 'ts_temp';

-- =======================
-- Main Tables
-- =======================

-- Clients
CREATE TABLE client (
    id_client SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    city TEXT,
    zip_code TEXT,
    registration_date DATE DEFAULT CURRENT_DATE
) TABLESPACE ts_catalogo;

-- Products
CREATE TABLE product (
    id_product SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    stock INTEGER DEFAULT 0
) TABLESPACE ts_catalogo;

-- Orders
CREATE TABLE customer_order (
    id_order SERIAL PRIMARY KEY,
    id_client INTEGER REFERENCES client(id_client),
    order_date DATE DEFAULT CURRENT_DATE,
    total NUMERIC(10,2) DEFAULT 0,
    state TEXT DEFAULT 'pending'
) TABLESPACE ts_datos;

-- Order Details
CREATE TABLE order_details (
    id_detail SERIAL PRIMARY KEY,
    id_order INTEGER REFERENCES customer_order(id_order) ON DELETE CASCADE,
    id_product INTEGER REFERENCES product(id_product),
    amount INTEGER NOT NULL CHECK (amount > 0),
    unit_price NUMERIC(10,2) NOT NULL
) TABLESPACE ts_datos;

-- Inventory
CREATE TABLE inventory (
    id_inventory SERIAL PRIMARY KEY,
    id_product INTEGER REFERENCES product(id_product) ON DELETE CASCADE,
    location TEXT NOT NULL,
    current_stock INTEGER NOT NULL CHECK (current_stock >= 0),
    last_update_date DATE DEFAULT CURRENT_DATE
) TABLESPACE ts_datos;

-- =======================
-- Function and trigger: update order total
-- =======================

CREATE OR REPLACE FUNCTION update_order_total()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE customer_order
  SET total = (
    SELECT COALESCE(SUM(amount * unit_price), 0)
    FROM order_details
    WHERE id_order = NEW.id_order
  )
  WHERE id_order = NEW.id_order;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_order_total
AFTER INSERT OR UPDATE OR DELETE
ON order_details
FOR EACH ROW
EXECUTE FUNCTION update_order_total();

-- =======================
-- Function and trigger: update product stock
-- =======================

CREATE OR REPLACE FUNCTION update_product_stock()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE product
  SET stock = (
    SELECT COALESCE(SUM(current_stock), 0)
    FROM inventory
    WHERE id_product = NEW.id_product
  )
  WHERE id_product = NEW.id_product;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_product_stock
AFTER INSERT OR UPDATE OR DELETE
ON inventory
FOR EACH ROW
EXECUTE FUNCTION update_product_stock();