#  Proyecto SIAR: Sistema de Identificación de Áreas para Reforestación

**SIAR** es una aplicación web geoespacial diseñada para potenciar la restauración de ecosistemas a nivel global, facilitando la toma de decisiones informadas y basadas en datos para proyectos de reforestación.

---

##  Características Principales (MVP)

-   **Selección de Área Interactiva:** Permite al usuario dibujar un polígono de interés directamente sobre un mapa.
-   ** Análisis de Viabilidad Asíncrono:** Procesa en segundo plano múltiples variables geoespaciales (suelo, clima, topografía) para el área seleccionada.
-   **Visualización de Resultados:** Genera un mapa de calor que clasifica el terreno en zonas de viabilidad **Alta**, **Media** y **Baja**.
-   **Recomendación de Especies:** Sugiere especies nativas compatibles con las zonas de más alta viabilidad, consultando datos de la API de GBIF.
-   **Consulta de Datos:** Permite al usuario hacer clic en cualquier zona del resultado para ver los datos que determinaron su clasificación.

---

##  Pila Tecnológica (Tech Stack)

| Área              | Tecnología                                                              |
| ----------------- | ----------------------------------------------------------------------- |
| **Backend**       | Python, Django, Django Rest Framework, Celery                           |
| **Frontend**      | React, TypeScript, Vite, Leaflet.js, Material-UI (MUI)                  |
| **Base de Datos** | PostgreSQL + PostGIS                                                    |
| **Análisis GIS**  | GeoPandas, Rasterio, GDAL, Shapely                                      |
| **Entorno**       | Docker, Docker Compose                                                  |

---

## Prerrequisitos

Para ejecutar este proyecto, solo necesitas tener instalado:

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/) (generalmente incluido con Docker Desktop)

---

## Guía de Inicio Rápido (Getting Started)

Gracias a Docker, el proyecto está contenido y su configuración es mínima.

1.  **Clona el Repositorio:**
    ```bash
    git clone [URL-del-repositorio]
    cd SIAR
    ```

2.  **Levanta los Contenedores:**
    Este comando construirá las imágenes de Docker para el frontend y el backend, descargará la imagen de la base de datos e iniciará todos los servicios.
    ```bash
    docker-compose up -d --build
    ```
    *La primera vez que se ejecute, este proceso puede tardar varios minutos mientras se descargan las dependencias y se construyen las imágenes.*

3.  **¡Listo! Accede a la Aplicación:**
    -   **Interfaz de Usuario (Frontend):** Abre tu navegador y ve a [http://localhost:5173](http://localhost:5173)
    -   **API del Backend:** La API estará disponible en [http://localhost:8000](http://localhost:8000)

---

## Estructura del Proyecto

```
/
├── backend/         # Contenedor del backend en Django
│   ├── analysis/    # App principal de Django con la lógica del análisis
│   ├── backend/     # Configuraciones del proyecto Django
│   └── ...
├── frontend/        # Contenedor del frontend en React
│   ├── src/
│   │   ├── components/ # Componentes de React
│   │   ├── hooks/      # Hooks personalizados
│   │   └── ...
│   └── ...
├── docker-compose.yml # Orquestador de los servicios
└── README.md          # Esta guía
```

---

## Comandos Útiles

Para ejecutar comandos dentro de los contenedores, puedes usar `docker-compose exec`.

-   **Poblar la base de datos con especies de ejemplo:**
    ```bash
    docker-compose exec backend python manage.py generate_species_data
    ```

-   **Acceder al shell de Django:**
    ```bash
    docker-compose exec backend python manage.py shell
    ```

-   **Ver logs de un servicio (ej. backend):**
    ```bash
    docker-compose logs -f backend
    ```