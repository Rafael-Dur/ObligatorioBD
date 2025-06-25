\c ecom

-- ======================================
-- Rol: editor_orders (editar orders)
-- ======================================
CREATE ROLE editor_orders NOINHERIT;
GRANT SELECT, INSERT, UPDATE, DELETE ON constumer_order TO editor_orders;
GRANT SELECT, INSERT, UPDATE, DELETE ON order_details TO editor_orders;

CREATE USER user_editor_orders WITH PASSWORD 'editor123';
GRANT editor_orders TO user_editor_orders;

-- ======================================
-- Rol: consulta_inventario (ver inventario)
-- ======================================
CREATE ROLE inventory_query NOINHERIT;
GRANT SELECT ON inventory TO inventory_query;
GRANT SELECT ON product TO inventory_query;

CREATE USER user_inventory WITH PASSWORD 'inventario123';
GRANT inventory_query TO user_inventory;

-- ======================================
-- Rol: auditor_logs (solo lectura de logs)
-- ======================================
CREATE ROLE auditor_logs NOINHERIT;
GRANT SELECT ON logs TO auditor_logs;

CREATE USER user_auditor WITH PASSWORD 'auditor123';
GRANT auditor_logs TO user_auditor;
