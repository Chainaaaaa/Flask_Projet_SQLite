DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    adresse TEXT NOT NULL
);
DROP TABLE IF EXISTS books;
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    stock INTEGER
);

DROP TABLE IF EXISTS emprunts; 
CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clients_id INTEGER,
    book_id INTEGER,
    date_emprunt TEXT,
    date_retour TEXT,
    FOREIGN KEY (clients_id) REFERENCES clients(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
