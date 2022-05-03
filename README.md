# companyday
## Proyecto de Miguel Abdon Sánchez-Herrero, Jose Luis Arrojo Abela, Adrián Mazuecos Pérez, Daniel Rello y Pedro Ventura Alvarez.




**dudas proyectos**

- que data necesitamos de las empresas
- que data necesitamos de los alumnos
- que data necesitamos de la utad
- la parte de maquetación, qué es lo que tiene que tener obligatoriamente?

**dudas hoy**
-- que datos se pueden cambiar una vez vez creada la cuenta(email, nombre empresa fijos,direccion,poblacion_id,codigo postal,consentimiento del nombre)

Empresa datos:

- contacto de la empresa

Orden de eventos:

- speed meeting
- feria
- presentacion de proyectos de alumnos
- charlas

Semana que viene:

- login de usuarios tanto apra empresa como para alumno
- base de datos (diagrama de e/r)
- diagrama de actividad de la aplicación

NAMES DE FORMULARIO:

- nombre
- nombre_persona_contacto
- email
- telefono
- direccion
- poblacion
- codigo_postal
- web
- logo_url
- consentimiento_uso_nombre
- buscando_candidatos
- feria_empresas
- presentacion
- speed_meetings
- charlas
- modalidad_presentacion
- animacion
- videojuegos
- disenio
- ingenieria
- modalidad_speed_meeting
- fecha_speed_meeting
- duracion
- descripcion_speed_meeting
- preguntas
- modalidad_charlas
- descripcion_charla
- fecha_charla
- hora_charla
- ponente

TODO de poblaciones:

- Si hay un país elegido, solo saldrán las provincias y las poblaciones de ese país.
- Si hay una provincia elegida, solo saldrán las poblaciones de esa provincia.
- Si no hay país elegido y se elije una provincia, el país se autorrellena.
- Si no hay provincia elegida y se elije una población, la provincia y el país se autorrellenan.
- Si había una provincia elegida y/o una población elegida, si se cambia de país, se vacían los campos de provincia y población.
- Si había una población elegida y se cambia de provincia, se vacía el campo de población.


TODO BACKEND:
    + HOME:
        - Onepage del HOME en una ruta HECHO
        - Ruta API nombre y logo de todas las empresas HECHO
        - Ruta API getpaises HECHO
        - Ruta Login POST (correo, contraseña) --> Respuesta redireccion a HOME con mensajes de error SIN HACER
        - Rescatar mensajes de error de flask login sin flash() SIN HACER
        - Ruta Registro API formulario tocho con eventos SIN HACER
        - Doble verificación de registro (primera por correo y segunda por api_uni) SIN HACER
        - Ruta cerrar sesión --> Redireccion a HOME sin estado SIN HACER
        - Reorganizar la estructura de directorios (rutas/api y rutas/views) SIN HACER

    + MI PERFIL:
        - Ruta Mi perfil SIN HACER
        - Ruta API getempresa autenticado para mi perfil HECHO
        - Ruta POST para cambiar parametros de mi empresa, no eventos, comprobar qué info se cambia para luego correo a Marta SIN HACER
        - BBDD tabla de cambios de info de empresa (clave foranea empresa, nombre variable) SIN HACER

    + Eventos
        - Ruta API eliminar evento parametro por identificador del tipo de evento y envía correo a Marta para avisar SIN HACER
        - Tabla/s de solicitud de nuevos eventos/edicion de eventos SIN HACER
        - Ruta añadir evento charla solicitud SIN HACER
        - Ruta añadir evento speedmeeting solicitud SIN HACER
        - Ruta añadir evento presentación proyecto empresa solicitud SIN HACER
        - Ruta modificar eventos solicitud SIN HACER

    + Trabajos alumnos
        - Añadir BBDD trabajos alumnos (ver qué datos hace falta) SIN HACER
        - Peticion API todas actividades alumnos, todos los datos SIN HACER 
