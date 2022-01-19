USE Userratings;
INSERT INTO
  content (Titel)
VALUES
  ("UP");
INSERT INTO
  content (Titel)
VALUES
  ("Inception");
INSERT INTO
  content (Titel)
VALUES
  ("Matrix");
INSERT INTO
  content (Titel)
VALUES
  ("Geostorm");
INSERT INTO
  content (Titel)
VALUES
  ("the ultimate showdown of ultimate destiny");
INSERT INTO
  genre (genre)
VALUES
  ("Comedy");
INSERT INTO
  genre (genre)
VALUES
  ("Action");
INSERT INTO
  genre (genre)
VALUES
  ("Drama");
INSERT INTO
  genre (genre)
VALUES
  ("Animation");
INSERT INTO
  users (username, pw_hash, admin_flag)
VALUES
  ("admin", "admin", 1);
INSERT INTO
  content_genre(genreID, ContentID)
VALUES
  (1, 5);