CREATE DATABASE image_gallery WITH OWNER = image_gallery;

GRANT ALL PRIVILEGES ON DATABASE image_gallery TO image_gallery;

CREATE TABLE public.users (
    user_id SERIAL PRIMARY KEY,
    username character varying(100) NOT NULL,
    password character varying(100),
    full_name character varying(200),
    admin boolean
);

CREATE TABLE public.images (
    id SERIAL PRIMARY KEY,
    filename character varying(100) NOT NULL,
    user_id integer,
    FOREIGN KEY (user_id) REFERENCES public.users (user_id)
);

GRANT SELECT, INSERT, UPDATE, DELETE ON users TO image_gallery;
GRANT SELECT, INSERT, UPDATE, DELETE ON images TO image_gallery;
GRANT USAGE, SELECT ON SEQUENCE users_user_id_seq TO image_gallery;
GRANT USAGE, SELECT ON SEQUENCE images_id_seq TO image_gallery;

INSERT INTO users (username, password, full_name, admin)
VALUES ('augrader', 'cpsc4973', 'gradey mcgrader', true);
