-- Herald Database Initialization Script

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database (if not already created by POSTGRES_DB)
-- This is mainly for documentation purposes
-- Database is created automatically by postgres image

-- Set default timezone
SET timezone = 'UTC';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE herald TO herald;
