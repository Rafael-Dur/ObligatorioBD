-- ===============================
-- Conectar a la base de datos ecom
-- ===============================
\c ecom

-- ===============================
-- Crear rol de administrador (superusuario)
-- ===============================
CREATE ROLE dba_shop WITH SUPERUSER LOGIN PASSWORD 'admin123';

-- ===============================
-- Crear rol de solo lectura
-- ===============================
CREATE ROLE readonly_shop NOINHERIT;

-- ===============================
-- Asignar permisos al rol de solo lectura
-- ===============================
GRANT CONNECT ON DATABASE ecom TO readonly_shop;
GRANT USAGE ON SCHEMA public TO readonly_shop;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_shop;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_shop;

-- ===============================
-- Crear usuarios de ejemplo
-- ===============================
-- Usuario solo lectura
CREATE USER user_readonly WITH PASSWORD 'readonly123';
GRANT readonly_shop TO user_readonly;

-- Usuario DBA
CREATE USER user_dba WITH PASSWORD 'dba123';
GRANT dba_shop TO user_dba;
