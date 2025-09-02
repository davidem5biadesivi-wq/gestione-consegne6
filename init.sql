
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS lavorazioni;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    macchina TEXT
);

CREATE TABLE lavorazioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descrizione TEXT NOT NULL,
    macchina TEXT NOT NULL,
    data_richiesta TEXT NOT NULL
);

INSERT INTO users (username, password, role, macchina) VALUES
('ufficio1', 'scrypt:32768:8:1$Ahf6AX9nxFHssMpP$433c54adad33823276ac464837e2d98a8db32edfc8b814d3d63c864fee2765e7be19ebfad67490a4ce01661f3c3e330affc682213e6ae97a52e491322614b972', 'ufficio', NULL),
('operatore1', 'scrypt:32768:8:1$YYKroV9NuEwcdvG5$0d84b6dfc1798eaf02d58655a62f3936a4967e1b5b193494f9f1a691b3c7b0097909e8e4e90b6615e9a0fde6325d443a515b2f42a497e0ec9b1f881af7e8ed17', 'operatore', 'tornio');
