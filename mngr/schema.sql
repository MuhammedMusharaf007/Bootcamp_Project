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
    id INTEGER NOT NULL,
    tag VARCHAR(50)
);

CREATE TABLE tags_notes(
    notes INTEGER,
    tags INTEGER,
    FOREIGN KEY (notes) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (tags) REFERENCES tags(id) ON DELETE CASCADE
);

INSERT INTO tags (id, tag) VALUES (1, "Action and Adventure");
INSERT INTO tags (id, tag) VALUES (2, "Classics");
INSERT INTO tags (id, tag) VALUES (3, "Comic or Graphic Novel");
INSERT INTO tags (id, tag) VALUES (4, "Detective and Mystery");
INSERT INTO tags (id, tag) VALUES (5, "Fantasy");
INSERT INTO tags (id, tag) VALUES (6, "Historical Fiction");
INSERT INTO tags (id, tag) VALUES (7, "Horror");
INSERT INTO tags (id, tag) VALUES (8, "Literary Fiction");
INSERT INTO tags (id, tag) VALUES (9, "Romance");
INSERT INTO tags (id, tag) VALUES (10, "Science Fiction");
INSERT INTO tags (id, tag) VALUES (11, "Short Stories");
INSERT INTO tags (id, tag) VALUES (12, "Suspense and Thrillers");
INSERT INTO tags (id, tag) VALUES (13, "Women's Fiction");
INSERT INTO tags (id, tag) VALUES (14, "Biography/Autobiography");
INSERT INTO tags (id, tag) VALUES (15, "Cookbooks");
INSERT INTO tags (id, tag) VALUES (16, "Essays");
INSERT INTO tags (id, tag) VALUES (17, "History");
INSERT INTO tags (id, tag) VALUES (18, "Memoir");
INSERT INTO tags (id, tag) VALUES (19, "Poetry");
INSERT INTO tags (id, tag) VALUES (20, "Self-Help");
INSERT INTO tags (id, tag) VALUES (21, "True Crime");
