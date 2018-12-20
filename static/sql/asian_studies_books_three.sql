
USE asian_studies_books;

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS attribution, temp_attribution, holding, temp_holding;
SET FOREIGN_KEY_CHECKS=1;

--
-- Attributions
--

CREATE TEMPORARY TABLE temp_attribution
  (
    attribution_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    full_title VARCHAR(200) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),
    role VARCHAR(15),
    PRIMARY KEY (attribution_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/attributions.csv'
INTO TABLE temp_attribution
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (full_title, last_name, first_name, @role)
  SET role = IF(@role = '', NULL, TRIM(@role));

CREATE TABLE IF NOT EXISTS attribution
  (
    attribution_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    book_id INT NOT NULL,
    creator_id INT NOT NULL,
    role_id INT,
    PRIMARY KEY (attribution_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (creator_id) REFERENCES creator(creator_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO attribution
  (
    book_id,
    creator_id,
    role_id
  )
SELECT b.book_id, c.creator_id, r.role_id
FROM temp_attribution ta
LEFT JOIN book b
  ON ta.full_title = b.full_title
LEFT JOIN creator c
  ON ta.last_name = c.last_name AND ta.first_name = c.first_name
LEFT JOIN role r
  ON ta.role = r.role_name;

DROP TABLE IF EXISTS temp_attribution;

--
-- Holdings
--

CREATE TEMPORARY TABLE temp_holding
  (
    holding_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    full_title VARCHAR(200) NOT NULL,
    oclc_symbol VARCHAR(5) NOT NULL,
    PRIMARY KEY (holding_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'input/csv/holdings.csv'
INTO TABLE temp_holding
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  -- FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '"'
  -- LINES TERMINATED BY '\n'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (full_title, oclc_symbol);

CREATE TABLE IF NOT EXISTS holding
  (
    holding_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    book_id INT NOT NULL,
    institution_id INT NOT NULL,
    PRIMARY KEY (holding_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (institution_id) REFERENCES institution(institution_id) ON DELETE CASCADE ON UPDATE CASCADE
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO holding
  (
    book_id,
    institution_id
  )
SELECT b.book_id, i.institution_id
FROM temp_holding th
LEFT JOIN book b
  ON th.full_title = b.full_title
LEFT JOIN institution i
  ON th.oclc_symbol = i.oclc_symbol;

DROP TABLE IF EXISTS temp_holding;
