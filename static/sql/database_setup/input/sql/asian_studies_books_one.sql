-- Combine Descriptive Metadata records from Michigan Publishing Services
-- and data collected from the WorldCat Search API

--
-- Create database
--
--
-- CREATE DATABASE IF NOT EXISTS asian_studies_books;
USE asian_studies_books;

--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS book, version, publisher, series, creator, role, format,
                     country, institution, holding, attribution;
SET FOREIGN_KEY_CHECKS=1;

--
-- Publishers
--

CREATE TABLE IF NOT EXISTS publisher
  (
    publisher_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    publisher_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (publisher_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO publisher (publisher_name) VALUES
  ('UM Center for Chinese Studies'),
  ('UM Center for Japanese Studies'),
  ('UM Center for South Asian Studies'),
  ('UM Center for South East Asian Studies'),
  ('UM Center for Souh and Southeast Asian Studies'),
  ('UM Center for Southeast Asian Studies');

--
-- Series
--

CREATE TABLE IF NOT EXISTS series
(
  series_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  series_name VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (series_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO series (series_name) VALUES
('Film Guides for Students of Chinese'),
('Michigan Abstracts of Chinese and Japanese Works in Chinese History'),
('Michigan Classics in Chinese Studies'),
('Michigan Classics in Japanese Studies'),
('Michigan Monograph Series in Japanese Studies'),
('Michigan Monographs in Chinese Studies'),
('Michigan Papers in Japanese Studies'),
('Michigan Papers on South and Southeast Asia'),
('Michigan Series in South and Southeast Asian Languages and Linguistics'),
('Michigan Studies in Buddhist Literature'),
('Science, Medicine, and Technology in East Asia'),
('Studies of South and Southeast Asia');

--
-- Series
--

CREATE TABLE IF NOT EXISTS role
  (
    role_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (role_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO role (role_name) VALUES
  ('Author'),
  ('Contributor'),
  ('Editor'),
  ('Translator');

--
-- Format
--

CREATE TABLE IF NOT EXISTS format
  (
    format_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    format_code VARCHAR(10) NOT NULL UNIQUE,
    format_name VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (format_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO format (format_code, format_name) VALUES
  ('HC', 'Hardcover'),
  ('PB', 'Paperback'),
  ('EB', 'E-book'),
  ('EB (OA)', 'E-book (Open Access)');

--
-- Creator
--

CREATE TABLE IF NOT EXISTS creator
  (
    creator_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    last_name VARCHAR(45) NOT NULL,
    first_name VARCHAR(45) NOT NULL,
    display_name VARCHAR(100),
    PRIMARY KEY (creator_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/creators.csv'
INTO TABLE creator
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (last_name, first_name, display_name)
  SET display_name = IF(display_name = '', NULL, display_name);

--
-- Country
--

CREATE TABLE IF NOT EXISTS country
  (
    country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    country_name VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (country_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/countries.csv'
INTO TABLE country
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (country_name);
