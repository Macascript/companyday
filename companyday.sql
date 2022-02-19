CREATE TABLE pais (
    id INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
)

CREATE TABLE provincia (
    id INT,
    pais_id INT FOREIGN KEY REFERENCES pais(id) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (pais_id,id)
);

CREATE TABLE poblacion (
    id INT AUTO_INCREMENT,
    provincia_id INT FOREIGN KEY REFERENCES provincia(id) NOT NULL,
    pais_id INT FOREIGN KEY REFERENCES pais(id) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY (provincia,id)
);

CREATE TABLE actividad (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(25) NOT NULL
)

CREATE TABLE empresa (
    id INT(32) PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    nombre_persona_contacto VARCHAR(100),
    email VARCHAR(320),
    telefono VARCHAR(13),
    direccion VARCHAR(500),
    poblacion INT FOREIGN KEY REFERENCES poblacion(id) NOT NULL,
    codigo_postal VARCHAR(10) NOT NULL,
    web VARCHAR(500),
    logo_url VARCHAR(200),
    buscando_candidatos BOOLEAN NOT NULL
);

CREATE TABLE participa (
    empresa_id INT(32) FOREIGN KEY REFERENCES empresa(id),
    actividad_id INT FOREIGN KEY REFERENCES actividad(id),
    PRIMARY KEY(empresa_id,actividad_id)
);