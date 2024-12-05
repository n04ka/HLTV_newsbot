create table article (
	id          INTEGER PRIMARY KEY,
	title       TEXT DEFAULT NULL,
    author		TEXT DEFAULT NULL,
	timestamp	TIMESTAMP DEFAULT NULL,
	url     	TEXT DEFAULT NULL,
	description	TEXT DEFAULT NULL,
    content    	TEXT DEFAULT NULL
);


create table translation (
	id          INTEGER PRIMARY KEY,
	title       TEXT DEFAULT NULL,
    author		TEXT DEFAULT NULL,
	description	TEXT DEFAULT NULL,
    content    	TEXT DEFAULT NULL
);


create table image (
	id          SERIAL,
	article_id	INTEGER REFERENCES article (id),
	url			TEXT
);