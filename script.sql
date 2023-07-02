CREATE USER image_gallery;
GRANT image_gallery TO postgres;
CREATE DATABASE image_gallery OWNER image_gallery;
\c image_gallery;

-- restore database

GRANT SELECT, INSERT, UPDATE, DELETE ON users TO image_gallery;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO image_gallery;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO image_gallery;