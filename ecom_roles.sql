-- ===============================
-- Conectar a la base de datos ecom
-- ===============================
\c ecom

-- ===============================
-- Eliminar roles y usuarios si existen
-- ===============================

-- Para eliminar usuarios primero hay que revocar roles y luego eliminar usuarios
DO $$
BEGIN
   IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user_readonly') THEN
      REVOKE readonly_shop FROM user_readonly;
      DROP USER user_readonly;
   END IF;

   IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user_dba') THEN
      REVOKE dba_shop FROM user_dba;
      DROP USER user_dba;
   END IF;

   IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'readonly_shop') THEN
      DROP ROLE readonly_shop;
   END IF;

   IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'dba_shop') THEN
      DROP ROLE dba_shop;
   END IF;
END$$;

-- ===============================
-- Crear rol de administrador (superusuario) con INHERIT
-- ===============================
CREATE ROLE dba_shop WITH SUPERUSER LOGIN PASSWORD 'admin123' INHERIT;

-- ===============================
-- Crear rol de solo lectura sin herencia
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
-- Usuario solo lectura SIN herencia
CREATE USER user_readonly WITH PASSWORD 'readonly123' NOINHERIT;
GRANT readonly_shop TO user_readonly;

-- Usuario DBA CON herencia
CREATE USER user_dba WITH PASSWORD 'dba123' INHERIT;
GRANT dba_shop TO user_dba;
