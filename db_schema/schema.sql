CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE incident (
	id INTEGER NOT NULL, 
	reg_number VARCHAR(50) NOT NULL, 
	registration_date DATETIME NOT NULL, 
	short_description VARCHAR(255) NOT NULL, 
	decision_status VARCHAR(50), 
	case_reg_number VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (reg_number)
);
CREATE TABLE person (
	id INTEGER NOT NULL, 
	reg_number VARCHAR(50) NOT NULL, 
	first_name VARCHAR(100) NOT NULL, 
	last_name VARCHAR(100) NOT NULL, 
	patronymic VARCHAR(100), 
	address VARCHAR(255), 
	convictions_count INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (reg_number)
);
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE incident_person (
	id INTEGER NOT NULL, 
	incident_id INTEGER NOT NULL, 
	person_id INTEGER NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(incident_id) REFERENCES incident (id), 
	FOREIGN KEY(person_id) REFERENCES person (id)
);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password_hash VARCHAR(128) NOT NULL, 
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	middle_name VARCHAR(50), 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(role_id) REFERENCES role (id), 
	UNIQUE (username)
);
