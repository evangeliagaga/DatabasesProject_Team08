DROP TABLE IF EXISTS contract;
CREATE TABLE contract (
	contract_ID INT NOT NULL AUTO_INCREMENT,
	start_date DATE NOT NULL,
	end_date DATE NOT NULL,
	songs_num INT NOT NULL,
	albums_num INT NOT NULL,
	PRIMARY KEY (contract_ID)
);

DROP TABLE IF EXISTS member;
CREATE TABLE member (
    person_AFM INT NOT NULL,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telephone VARCHAR(10) NOT NULL,
    birth_date DATE NOT NULL,
    sex ENUM('Male', 'Female') NOT NULL,
    street_number INT NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    zip_code INT NOT NULL,
    country VARCHAR(255) NOT NULL,
    expertise VARCHAR(255) NOT NULL,
    PRIMARY KEY (person_AFM)
);

DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
	artist_ID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	genre VARCHAR(255) NOT NULL,
	PRIMARY KEY (artist_ID)
);

DROP TABLE IF EXISTS collaborator;
CREATE TABLE collaborator (
	person_AFM INT NOT NULL,
	fname VARCHAR(255) NOT NULL,
	lname VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	telephone VARCHAR(10) NOT NULL,
	birth_date DATE NOT NULL,
	sex ENUM('Male', 'Female') NOT NULL,
	street_number INT NOT NULL,
	street VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
	zip_code INT NOT NULL,
	country VARCHAR(255) NOT NULL,
	PRIMARY KEY (person_AFM)
);

DROP TABLE IF EXISTS col_type;
CREATE TABLE col_type (
	col_type_ID INT NOT NULL AUTO_INCREMENT,
	type ENUM('Producer', 'Music composer', 'Lyrics composer') NOT NULL,
	PRIMARY KEY (col_type_ID)
);

DROP TABLE IF EXISTS album;
CREATE TABLE album (
	album_ID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	released_date DATE NOT NULL,
	songs_num INT NOT NULL,
	album_price FLOAT NOT NULL,
	PRIMARY KEY (album_ID)
);

DROP TABLE IF EXISTS song;
CREATE TABLE song (
	song_ID INT NOT NULL AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	track_num INT, 
	music_cost FLOAT NOT NULL,
	lyrics_cost FLOAT NOT NULL,
	song_price FLOAT NOT NULL,
	single BOOLEAN NOT NULL, -- 1: YES, 0: NO
	duration FLOAT NOT NULL,
    album_ID INT,
	PRIMARY KEY (song_ID),
    FOREIGN KEY (album_ID) REFERENCES album(album_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS studio_engineer;
CREATE TABLE studio_engineer (
	se_AFM INT NOT NULL,
	fname VARCHAR(255) NOT NULL,
	lname VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	telephone VARCHAR(10) NOT NULL,
	birth_date DATE NOT NULL,
	sex ENUM('Male', 'Female') NOT NULL,
	street_number INT NOT NULL,
	street VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
	zip_code INT NOT NULL,
	country VARCHAR(255) NOT NULL,
	PRIMARY KEY (se_AFM)
);

DROP TABLE IF EXISTS se_type;
CREATE TABLE se_type (
	se_type_ID INT NOT NULL AUTO_INCREMENT,
	type ENUM('Mixing engineer', 'Editing engineer', 
              'Mastering engineer', 'Recording engineer') NOT NULL,
	PRIMARY KEY (se_type_ID)
);

DROP TABLE IF EXISTS studio;
CREATE TABLE studio (
	studio_ID INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	price_per_hour FLOAT NOT NULL,
	telephone VARCHAR(10) NOT NULL,
	email VARCHAR(255) NOT NULL,
	available_start DATETIME NOT NULL,
	available_end DATETIME NOT NULL,
	street_number INT NOT NULL,
	street VARCHAR(255) NOT NULL,
	city VARCHAR(255) NOT NULL,
    zip_code INT NOT NULL,
	country VARCHAR(255) NOT NULL,
	PRIMARY KEY (studio_ID)
);


-- TABLES FOR FOREIGN KEYS

DROP TABLE IF EXISTS Member_Signs_Contract;
CREATE TABLE Member_Signs_Contract(
    person_AFM INT NOT NULL,
    contract_ID INT NOT NULL,
    PRIMARY KEY (person_AFM, contract_ID),
    FOREIGN KEY (person_AFM) REFERENCES member(person_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (contract_ID) REFERENCES contract(contract_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Col_Signs_Contract;
CREATE TABLE Col_Signs_Contract(
    person_AFM INT NOT NULL,
    contract_ID INT NOT NULL,
    PRIMARY KEY (person_AFM, contract_ID),
    FOREIGN KEY (person_AFM) REFERENCES collaborator(person_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (contract_ID) REFERENCES contract(contract_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Member_Has_Artist;
CREATE TABLE Member_Has_Artist(
    person_AFM INT NOT NULL,
    artist_ID INT NOT NULL,
    PRIMARY KEY (person_AFM, artist_ID),
    FOREIGN KEY (person_AFM) REFERENCES member(person_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (artist_ID) REFERENCES artist(artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Col_Has_ColType;
CREATE TABLE Col_Has_ColType(
    person_AFM INT NOT NULL,
    col_type_ID INT NOT NULL,
    PRIMARY KEY (person_AFM, col_type_ID),
    FOREIGN KEY (person_AFM) REFERENCES collaborator(person_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (col_type_ID) REFERENCES col_type(col_type_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Song_BelongsTo_Artist;
CREATE TABLE Song_BelongsTo_Artist(
    song_ID INT NOT NULL,
    artist_ID INT NOT NULL,
    PRIMARY KEY (song_ID, artist_ID),
    FOREIGN KEY (song_ID) REFERENCES song(song_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (artist_ID) REFERENCES artist(artist_ID)  ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Col_Composes_Song;
CREATE TABLE Col_Composes_Song(
    person_AFM INT NOT NULL,
    song_ID INT NOT NULL,
    PRIMARY KEY (person_AFM, song_ID),
    FOREIGN KEY (person_AFM) REFERENCES collaborator(person_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (song_ID) REFERENCES song(song_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS SE_WorksOn_Song;
CREATE TABLE SE_WorksOn_Song(
    song_ID INT NOT NULL,
    se_AFM INT NOT NULL,
    PRIMARY KEY (song_ID, se_AFM),
    FOREIGN KEY (song_ID) REFERENCES song(song_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (se_AFM) REFERENCES studio_engineer(se_AFM) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS SE_WorksAt_Studio;
CREATE TABLE SE_WorksAt_Studio(
    se_AFM INT NOT NULL,
    studio_ID INT NOT NULL,
    PRIMARY KEY (se_AFM, studio_ID),
    FOREIGN KEY (se_AFM) REFERENCES studio_engineer(se_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (studio_ID) REFERENCES studio(studio_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS SE_Has_SEType;
CREATE TABLE SE_Has_SEType(
    se_AFM INT NOT NULL,
    se_type_ID INT NOT NULL,
    PRIMARY KEY (se_AFM, se_type_ID),
    FOREIGN KEY (se_AFM) REFERENCES studio_engineer(se_AFM) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (se_type_ID) REFERENCES se_type(se_type_ID) ON DELETE CASCADE ON UPDATE CASCADE
);


