CREATE TABLE users(
    email TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE genres(
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT
);

CREATE TABLE movies(
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    genre_id INTEGER
);

CREATE TABLE ratings(
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    movie_id INTEGER,
    rating INTEGER
);