DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS notes;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
);

CREATE TABLE notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags VARCHAR(50),
    FOREIGN KEY (userid) REFERENCES user(id)
);