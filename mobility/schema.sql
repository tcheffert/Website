-- DROP TABLE IF EXISTS ville;
-- DROP TABLE IF EXISTS rue;
-- DROP TABLE IF EXISTS vitesse;
-- DROP TABLE IF EXISTS trafic;


CREATE TABLE IF NOT EXISTS ville (
    code_postal INTEGER NOT NULL,
    nom         TEXT    NOT NULL,
    population  INTEGER NOT NULL,
    PRIMARY KEY(code_postal)
);


CREATE TABLE IF NOT EXISTS rue (
    rue_id      INTEGER NOT NULL,
    nom         TEXT    NOT NULL,
    code_postal INTEGER NOT NULL,
    FOREIGN KEY(code_postal) REFERENCES ville(code_postal),
    PRIMARY KEY(rue_id)
);


CREATE TABLE IF NOT EXISTS vitesse (
    rue_id      INTEGER NOT NULL,
    date        TEXT    NOT NULL,
    tranche_de_vitesse TEXT NOT NULL,
    proportion  REAL    NOT NULL,
    FOREIGN KEY(rue_id) REFERENCES rue(rue_id),
    PRIMARY KEY(rue_id, date, tranche_de_vitesse)
);


CREATE TABLE IF NOT EXISTS trafic (
    rue_id  INTEGER NOT NULL,
    date    TEXT    NOT NULL,
    lourd   INTEGER NOT NULL,
    voiture INTEGER NOT NULL,
    velo    INTEGER NOT NULL,
    pieton  INTEGER NOT NULL,
    v85     REAL,
    FOREIGN KEY(rue_id) REFERENCES rue(rue_id),
    PRIMARY KEY(date, rue_id)
);