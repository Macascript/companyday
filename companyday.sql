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
    buscando_candidatos BOOLEAN NOT NULL,
    
);

CREATE TABLE asistente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    empresa_id INT(32) FOREIGN KEY REFERENCES empresa(id) NOT NULL,
    nombre_completo VARCHAR(250) NOT NULL,
    cargo VARCHAR(100) NOT NULL
);

CREATE TABLE presentacion (
    empresa_id INT(32) PRIMARY KEY FOREIGN KEY REFERENCES empresa(id),
    presencial BOOLEAN DEFAULT FALSE,
    animacion BOOLEAN DEFAULT FALSE,
    videojuegos BOOLEAN DEFAULT FALSE,
    disenio BOOLEAN DEFAULT FALSE,
    ingenieria BOOLEAN DEFAULT FALSE
);

CREATE TABLE sesion (
    id INT PRIMARY KEY,
    empresa_id INT(32) FOREIGN KEY REFERENCES empresa(id) NOT NULL,
    fecha DATE NOT NULL,
    duracion VARCHAR(2) NOT NULL
);

CREATE TABLE speed_meeting (
    empresa_id INT(32) PRIMARY KEY FOREIGN KEY REFERENCES empresa(id),
    presencial BOOLEAN,
    descripcion VARCHAR(500),
    preguntas VARCHAR(500)
);

CREATE TABLE charla (
    descripcion VARCHAR(500),
    presencial BOOLEAN DEFAULT FALSE,
    fecha DATETIME NOT NULL,
    ponente VARCHAR(100) NOT NULL
);

CREATE TABLE participa (
    empresa_id INT(32) FOREIGN KEY REFERENCES empresa(id),
    actividad_id INT FOREIGN KEY REFERENCES actividad(id),
    PRIMARY KEY(empresa_id,actividad_id)
);