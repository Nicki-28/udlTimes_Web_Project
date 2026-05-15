
# 🎓 UDL Times — Web Project

Una plataforma de juegos y acertijos diarios inspirada en *The New York Times Games*, desarrollada con **Django** y personalizada con la identidad visual de la **Universitat de Lleida (UdL)**.

Disfruta de *Connections*, *Wordle* y *Framed*: sigue tus estadísticas, compite en los rankings y vive una experiencia totalmente responsiva.

> **Nota:** Todo el contenido (palabras, categorías, películas) se basa en datos ficticios o universitarios creados para este proyecto. No refleja información oficial de la UdL.

---

## 🚀 Comenzando

### Requisitos previos
* [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/) instalados.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Nicki-28/udlTimes_Web_Project.git](https://github.com/Nicki-28/udlTimes_Web_Project.git)
cd udlTimes_Web_Project

```

### 2. Levantar el proyecto

```bash
docker-compose up --build

```

La aplicación estará disponible en: **http://localhost:8000**

### 3. Cargar datos de prueba (Mock Data)

En una nueva terminal, ejecuta:

```bash
docker compose exec web uv run python manage.py seed_mock_data

```

Esto creará usuarios, estadísticas y partidas de ejemplo para Wordle, Connections y Framed.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
| --- | --- |
| **Backend** | Python 3, Django |
| **Frontend** | HTML5, CSS3, Vanilla JS, Tailwind CSS |
| **Base de Datos** | PostgreSQL (Dockerizado) |
| **Tests E2E** | Behave (BDD), Splinter, Selenium |
| **Gestión Dependencias** | `uv`, `pyproject.toml` |

---

## 🧪 Testing End-to-End (E2E)

Hemos implementado una suite de pruebas robusta utilizando **Behave** (Behavior-Driven Development) y **Splinter** para asegurar el correcto funcionamiento de los flujos críticos.

### Estructura de Pruebas

```text
udltimes/
└── features/
    ├── environment.py              # Configuración del navegador (Headless Chrome)
    ├── *.feature                   # Escenarios en lenguaje Gherkin
    └── steps/
        ├── common_steps.py         # Pasos compartidos (Login, Navegación)
        └── *_wordle.py             # Lógica específica por funcionalidad

```

### Niveles de Implementación

1. **Nivel 1: `.feature` (Gherkin):** Definición de escenarios en lenguaje natural.
2. **Nivel 2: `steps/*.py` (Python):** Código que traduce el texto en acciones del navegador.
3. **Nivel 3: `environment.py` (Driver):** Configuración técnica del navegador (Chrome Headless, seguridad, etc.).

### Cobertura de Escenarios

| Funcionalidad | Escenarios | Puntos |
| --- | --- | --- |
| **Creación Custom Wordle** | Éxito, sin login, palabra vacía, longitud inválida, caracteres no permitidos. | 3.0 |
| **Edición Custom Wordle** | Éxito como autor, sin login, intento de editar ajeno, validación vacía. | 3.0 |
| **Eliminación Custom Wordle** | Éxito como autor, sin login, intento de eliminar ajeno. | 1.5 |

### Ejecución de Tests

Para ejecutar las pruebas en tu entorno local:

```bash
# 1. Asegúrate de que la DB esté corriendo
docker compose up -d db

# 2. Ejecutar Behave (desde el root del proyecto)
POSTGRES_HOST=localhost python3 manage.py behave --keepdb

```

> **Nota técnica:** Debido a que el modal de login es manejado por JavaScript, los tests utilizan `execute_script` para interactuar con elementos ocultos del DOM, garantizando la fluidez de las pruebas.

---

## 📂 Estructura del Proyecto

```bash
udlTimes_Web_Project/
├── static/                # Activos (CSS, JS, Imágenes)
├── templates/             # Plantillas HTML (Django Templates)
├── udlTimes_Web_Project/  # Configuración del Core del proyecto
├── udltimes/              # Aplicación principal (Models, Views, Features)
├── manage.py              # Script de gestión de Django
├── Dockerfile             # Configuración de imagen de contenedor
└── pyproject.toml         # Dependencias y herramientas de desarrollo

```

---

## 📝 Notas de Versión Recientes

* **Behave-Django:** Integrado en `INSTALLED_APPS`.
* **Corrección de Modelos:** Añadido `max_length` en descripciones de `FramedConcept`.
* **Docker Tuning:** Puerto `5432` expuesto para facilitar pruebas locales.
* **Login Fix:** Solucionada la interacción de Selenium con modales de Tailwind.
