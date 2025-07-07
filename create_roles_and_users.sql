\set ON_ERROR_STOP on

\c ecom

-- ======================================
-- Rol: editor_orders (editar orders)
-- ======================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'editor_orders') THEN
        CREATE ROLE editor_orders NOINHERIT;
    END IF;
END $$;
GRANT SELECT, INSERT, UPDATE, DELETE ON constumer_order TO editor_orders;
GRANT SELECT, INSERT, UPDATE, DELETE ON order_details TO editor_orders;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user_editor_orders') THEN
        CREATE USER user_editor_orders WITH PASSWORD 'editor123';
    END IF;
END $$;
GRANT editor_orders TO user_editor_orders;

-- ======================================
-- Rol: consulta_inventario (ver inventario)
-- ======================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'inventory_query') THEN
        CREATE ROLE inventory_query NOINHERIT;
    END IF;
END $$;
GRANT SELECT ON inventory TO inventory_query;
GRANT SELECT ON product TO inventory_query;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user_inventory') THEN
        CREATE USER user_inventory WITH PASSWORD 'inventario123';
    END IF;
END $$;
GRANT inventory_query TO user_inventory;

-- ======================================
-- Rol: auditor_logs (solo lectura de logs)
-- ======================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'auditor_logs') THEN
        CREATE ROLE auditor_logs NOINHERIT;
    END IF;
END $$;
GRANT SELECT ON logs TO auditor_logs;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user_auditor') THEN
        CREATE USER user_auditor WITH PASSWORD 'auditor123';
    END IF;
END $$;
GRANT auditor_logs TO user_auditor;
