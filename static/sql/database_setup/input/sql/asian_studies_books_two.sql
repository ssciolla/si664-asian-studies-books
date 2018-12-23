
USE asian_studies_books;

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS book, temp_book, version, temp_version, institution, temp_institution;
SET FOREIGN_KEY_CHECKS=1;

--
-- Books
--

CREATE TEMPORARY TABLE temp_book
  (
    book_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    title VARCHAR(200) NOT NULL,
    prefix VARCHAR(100),
    subtitle VARCHAR(200),
    full_title VARCHAR(300),
    key_note VARCHAR(400),
    description LONGTEXT,
    pages INT,
    volume INT,
    publisher_name VARCHAR(100),
    series_name VARCHAR(100),
    PRIMARY KEY (book_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/books.csv'
INTO TABLE temp_book
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (title, prefix, subtitle, full_title, key_note, description, @pages, @volume, publisher_name, @series_name)
  SET prefix = IF(prefix = '', NULL, prefix),
  subtitle = IF(subtitle = '', NULL, subtitle),
  key_note = IF(key_note = '', NULL, key_note),
  description = IF(description = '', NULL, description),
  pages = IF(@pages = '', NULL, TRIM(@pages)),
  volume = IF(@volume = '', NULL, TRIM(@volume)),
  series_name = IF(@series_name = '', NULL, TRIM(@series_name));

CREATE TABLE IF NOT EXISTS book
  (
    book_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    title VARCHAR(200) NOT NULL,
    prefix VARCHAR(100),
    subtitle VARCHAR(200),
    full_title VARCHAR(300),
    key_note VARCHAR(400),
    description LONGTEXT,
    pages INT NULL,
    volume INT NULL,
    publisher_id INT NOT NULL,
    series_id INT NULL,
    PRIMARY KEY (book_id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(series_id) ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO book
  (
    title,
    prefix,
    subtitle,
    full_title,
    key_note,
    description,
    pages,
    volume,
    publisher_id,
    series_id
  )
SELECT tb.title, tb.prefix, tb.subtitle, tb.full_title, tb.key_note, tb.description, tb.pages, tb.volume,
       p.publisher_id, s.series_id
FROM temp_book tb
LEFT JOIN publisher p
  ON p.publisher_name = tb.publisher_name
LEFT JOIN series s
  ON s.series_name = tb.series_name;

DROP TABLE IF EXISTS temp_book;

--
-- Versions
--

CREATE TEMPORARY TABLE temp_version
  (
    version_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    full_title VARCHAR(200) NOT NULL,
    format_code VARCHAR(10) NOT NULL,
    isbn13 VARCHAR(13),
    year_published INT,
    bisac_status VARCHAR(100),
    PRIMARY KEY (version_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/versions.csv'
INTO TABLE temp_version
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (full_title, format_code, @isbn13, @year_published, @bisac_status)
  SET isbn13 = IF(@isbn13 = '', NULL, TRIM(@isbn13)),
  year_published = IF(@year_published = '', NULL, TRIM(@year_published)),
  bisac_status = IF(@bisac_status = '', NULL, TRIM(@bisac_status));

CREATE TABLE IF NOT EXISTS version
  (
    version_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    book_id INT NOT NULL,
    format_id INT NOT NULL,
    isbn13 VARCHAR(13),
    year_published INT,
    bisac_status VARCHAR(100),
    PRIMARY KEY (version_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (format_id) REFERENCES format(format_id) ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO version
  (
    book_id,
    format_id,
    isbn13,
    year_published,
    bisac_status
  )
SELECT b.book_id, f.format_id, tv.isbn13, tv.year_published, tv.bisac_status
FROM temp_version tv
LEFT JOIN book b
  ON b.full_title = tv.full_title
LEFT JOIN format f
  ON f.format_code = tv.format_code;

DROP TABLE IF EXISTS temp_version;

--
-- Institutions
--

CREATE TEMPORARY TABLE temp_institution
  (
    institution_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    institution_name VARCHAR(200) NOT NULL,
    oclc_symbol VARCHAR(5) NOT NULL,
    street_address VARCHAR(300),
    country_name VARCHAR(50),
    opac_url VARCHAR(700),
    PRIMARY KEY (institution_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/institutions.csv'
INTO TABLE temp_institution
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (institution_name, oclc_symbol, @street_address, @country_name, @opac_url)
  SET street_address = IF(@street_address = '', NULL, TRIM(@street_address)),
  country_name = IF(@country_name = '', NULL, TRIM(@country_name)),
  opac_url = IF(@opac_url = '', NULL, TRIM(@opac_url));

CREATE TABLE IF NOT EXISTS institution
  (
    institution_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    institution_name VARCHAR(200) NOT NULL,
    oclc_symbol VARCHAR(5) NOT NULL,
    street_address VARCHAR(300),
    country_id INT NOT NULL,
    opac_url VARCHAR(700),
    PRIMARY KEY (institution_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO institution
  (
    institution_name,
    oclc_symbol,
    street_address,
    country_id,
    opac_url
  )
SELECT ti.institution_name, ti.oclc_symbol, ti.street_address, c.country_id, ti.opac_url
FROM temp_institution ti
LEFT JOIN country c
  ON c.country_name = ti.country_name;

DROP TABLE IF EXISTS temp_institution;
