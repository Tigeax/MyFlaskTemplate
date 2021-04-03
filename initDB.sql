-- SQL to run to setup the SQL database

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);