PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username VARCHAR(256) NOT NULL,
    name VARCHAR(128) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username)
);

CREATE TABLE answers(
    answerid integer PRIMARY KEY AUTOINCREMENT,
    questionnumber integer,
    questionid integer,
    answer VARCHAR(256) NOT NULL,
    owner VARCHAR(256),
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE
);

-- CREATE TABLE posts(
--     postid integer PRIMARY KEY AUTOINCREMENT,
--     filename VARCHAR(64),
--     owner VARCHAR(20),
--     created DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE
-- );
--
-- CREATE TABLE following(
--     username1 VARCHAR(20) NOT NULL,
--     username2 VARCHAR(20) NOT NULL,
--     created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- --      The following relation is username1 follows username2.
--     FOREIGN KEY (username1) REFERENCES users(username) ON DELETE CASCADE,
--     FOREIGN KEY (username2) REFERENCES users(username) ON DELETE CASCADE,
--     PRIMARY KEY(username1, username2)
-- );
--
-- CREATE TABLE comments(
--     commentid INTEGER PRIMARY KEY AUTOINCREMENT,
--     owner VARCHAR(20),
--     postid INTEGER,
--     text VARCHAR(1024),
--     created DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE,
--     FOREIGN KEY (postid) REFERENCES posts(postid) ON DELETE CASCADE
-- );
--
-- CREATE TABLE likes(
--     likeid integer PRIMARY KEY AUTOINCREMENT,
--     owner VARCHAR(20),
--     postid integer,
--     created DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE,
--     FOREIGN KEY (postid) REFERENCES posts(postid) ON DELETE CASCADE
-- );

