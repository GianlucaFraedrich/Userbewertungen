USE Userratings;
INSERT INTO
  content (Titel, release_date)
VALUES
  ("UP", "10-09-2009");
INSERT INTO
  content (Titel, release_date)
VALUES
  ("Inception", "29-06-2010");
INSERT INTO
  content (Titel, release_date)
VALUES
  ("Matrix", "12.01.1999");
INSERT INTO
  content (Titel, release_date)
VALUES
  ("Geostorm", "19.10.2017");
INSERT INTO
  content (Titel, release_date)
VALUES
  (
    "the ultimate showdown of ultimate destiny",
    "22.12.2005"
  );
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
  users (username, pw_hash, admin_flag)
VALUES
  ("user", "user", 0);
INSERT INTO
  content_genre(genreID, ContentID)
VALUES
  (1, 5);