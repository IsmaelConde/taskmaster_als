# taskmaster_als
TaskMaster ALS es una aplicación web de gestión de proyectos y tareas diseñada siguiendo el modelo de Aprendizaje Basado en Problemas (ALS). La aplicación permite a los usuarios organizar su flujo de trabajo mediante una jerarquía estructurada de categorías, proyectos y tareas, garantizando la persistencia y la integridad de los datos en una base de datos NoSQL.
![alt text](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![alt text](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![alt text](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

✨ Características Principales
Gestión de Usuarios: Registro e inicio de sesión seguro mediante Flask-Login y hashing de contraseñas con Werkzeug.
Arquitectura de 3 Entidades: Cumple con requisitos avanzados de complejidad mediante el uso de Categorías, Proyectos y Tareas.
Integridad Estructural: Implementación de borrado en cascada (al eliminar un proyecto, se eliminan automáticamente sus tareas vinculadas).
Diseño Robusto: Manejo de excepciones y parches de seguridad para garantizar la compatibilidad con objetos de datos antiguos.
Interfaz Moderna: UI limpia y responsive construida con Pico CSS y plantillas Jinja2.
Persistencia NoSQL: Uso de Sirope como capa de persistencia de objetos sobre Redis.

🛠️ Stack Tecnológico
Backend: Python 3 + Flask.
Base de Datos: Redis + Sirope (Object Persistence).
Frontend: Jinja2 + Pico CSS.
Autenticación: Flask-Login.

📂 Estructura del Proyecto

├── src/               # Código fuente de la aplicación

│   ├── app.py         # Controlador principal y rutas

│   ├── model.py       # Definición de entidades (Clases)

│   ├── templates/     # Plantillas Jinja2 (HTML)

│   └── static/        # Archivos estáticos (CSS/JS)

├── doc/               # Documentación del proyecto

│   ├── memoria.pdf    # Memoria técnica detallada

│   └── info.txt       # Información de entrega

└── bin/               # Scripts de ejecución

🚀 Instalación y Ejecución
1. Clonar el repositorio:
   git clone https://github.com/tu-usuario/taskmaster-als.git
   cd taskmaster-als
   
2. Instalar dependencias:
   pip install flask flask-login sirope redis
   
3. Iniciar el servidor Redis:
   redis-server
   
4. Ejecutar la aplicación:
   cd src
   python app.py

📝 Criterios Académicos Cumplidos
Este proyecto ha sido desarrollado cumpliendo los estándares de la asignatura ALS:

Modularidad: Separación lógica entre modelos y controladores.

Complejidad: Manejo de 3 entidades relacionadas.

Robustez: La aplicación gestiona situaciones de error inesperadas sin detener su ejecución.

UX: Navegación fluida e intuitiva sin necesidad de recargar páginas manualmente para reflejar cambios.

