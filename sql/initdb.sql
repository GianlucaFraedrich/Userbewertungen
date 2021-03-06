CREATE DATABASE IF NOT EXISTS Userratings;
USE Userratings;
CREATE TABLE IF NOT EXISTS content (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Titel VARCHAR(255),
  release_date VARCHAR(10)
);
CREATE TABLE IF NOT EXISTS users (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255),
  pw_hash VARCHAR(255),
  admin_flag BIT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ratings (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  rating INT,
  userID INT,
  contentID INT
);
CREATE TABLE IF NOT EXISTS genre (
  ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  genre VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS content_genre (genreID INT, contentID INT);