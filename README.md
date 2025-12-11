# Proyecto SIAR: Sistema de Identificación de Áreas para Reforestación

**SIAR** es una aplicación web geoespacial de código abierto diseñada para optimizar la planificación de proyectos de restauración de ecosistemas, identificando científicamente las áreas más viables para la reforestación con especies nativas.

---

## Características Principales

-   **Selección de Área Interactiva:** Permite al usuario dibujar un polígono de interés directamente sobre un mapa.
-   **Análisis Asíncrono y Multi-variable:** Procesa en segundo plano múltiples variables geoespaciales (suelo, clima, topografía y cobertura actual) para el área seleccionada, sin bloquear la interfaz.
-   **Visualización de Resultados:** Genera un mapa de calor (heatmap) que clasifica el terreno en zonas de viabilidad **Alta**, **Media** y **Baja**.
-   **Recomendación de Especies Nativas:** Se integra con la API de GBIF para sugerir especies vegetales nativas compatibles con las zonas de más alta viabilidad.
-   **Consulta de Datos Detallada:** Permite al usuario hacer clic en cualquier zona del resultado para ver los datos y criterios que determinaron su clasificación.
-   **Historial de Análisis:** Guarda y permite volver a consultar los resultados de análisis previos.

---

## Tech Stack

| Área | Tecnología |
| :--- | :--- |
| **Backend** | Python, Django, Django Rest Framework, Celery |
| **Frontend** | React, TypeScript, Vite, Leaflet.js, Material-UI (MUI) |
| **Base de Datos** | PostgreSQL + PostGIS |
| **Análisis GIS** | GeoPandas, Rasterio, GDAL, Shapely, OWSLib |
| **Entorno** | Docker, Docker Compose |

---

## Guía de Inicio Rápido (Getting Started)

Gracias a Docker, el proyecto está autocontenido. Sigue estos pasos para ponerlo en marcha.

### 1. Prerrequisitos

Asegúrate de tener instalado:
-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/) (normalmente incluido con Docker Desktop)
-   [Git](https://git-scm.com/downloads)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd SIAR
```
*(Reemplaza la URL con la del repositorio real)*

### 3. Configuración del Entorno (Paso Crítico)

El backend requiere variables de entorno para funcionar, incluyendo claves de API y la configuración de la base de datos.

1.  **Navega al directorio del backend:**
    ```bash
    cd backend
    ```

2.  **Copia el archivo de ejemplo:**
    Crea una copia del archivo `.env.example` y renómbrala a `.env`. Este archivo `.env` es ignorado por Git para mantener tus claves seguras.
    ```bash
    # En Windows (PowerShell)
    copy .env.example .env

    # En macOS / Linux
    cp .env.example .env
    ```

3.  **Edita el archivo `.env`:**
    Abre el archivo `.env` que acabas de crear con un editor de texto y revisa sus valores.
    -   **`SECRET_KEY`**: Por seguridad, es una buena práctica reemplazarla con una nueva clave generada.
    -   **`OPENTOPOGRAPHY_API_KEY`**: Esta clave es opcional, pero **muy recomendable**. Sin ella, es probable que las peticiones a la API de OpenTopography fallen por exceder los límites de uso anónimo. Puedes obtener una clave gratuita en [OpenTopography Portal](https://portal.opentopography.org/myopentopo).
    -   Las demás variables (`DATABASE_URL`, `REDIS_URL`, etc.) ya están pre-configuradas para funcionar con Docker Compose y no necesitan ser modificadas para un entorno de desarrollo local.

### 4. Levantar los Contenedores

Vuelve al directorio raíz del proyecto (donde se encuentra el `docker-compose.yml`) y ejecuta el siguiente comando:

```bash
docker-compose up -d --build
```
*La primera vez que se ejecute, este proceso puede tardar varios minutos mientras se descargan las dependencias y se construyen las imágenes.*

### 5. Acceder a la Aplicación

Una vez que los contenedores estén en funcionamiento:
-   **Interfaz de Usuario (Frontend):** Abre tu navegador y ve a [http://localhost:5173](http://localhost:5173)
-   **API del Backend:** La API estará disponible en [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)

---

## Estructura del Proyecto

```
/
├── backend/                # Contenedor del backend en Django
│   ├── analysis/           # App principal de Django con la lógica del análisis
│   ├── backend/            # Configuraciones del proyecto Django
│   ├── .env.example        # Plantilla de variables de entorno
│   └── ...
├── frontend/               # Contenedor del frontend en React
│   ├── src/
│   │   ├── components/     # Componentes de React
│   │   ├── hooks/          # Hooks personalizados
│   │   └── ...
│   └── ...
├── docker-compose.yml      # Orquestador de los servicios
└── README.md                 # Esta guía
```

---