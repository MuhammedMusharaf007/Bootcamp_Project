DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS tags_notes;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE tags(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(50)
);

CREATE TABLE tags_notes(
    notes INTEGER,
    tags INTEGER,
    FOREIGN KEY (notes) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (tags) REFERENCES tags(id) ON DELETE CASCADE
);