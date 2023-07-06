-- this will initialize the database with some test records.
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    release_date DATE
);
CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    gender VARCHAR,
    age INTEGER,
    movie_id INTEGER REFERENCES movies(id)
);

-- Insert a new actor
INSERT INTO actors (name, gender, age)
VALUES ('Tom Cruise', 'Male', 35);

-- Insert a new movie
INSERT INTO movies (title, release_date)
VALUES ('Mission Impossible', CURRENT_DATE);
