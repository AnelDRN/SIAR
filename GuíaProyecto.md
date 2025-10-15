# **Documento Guía del Proyecto: Sistema de Identificación de Áreas para Reforestación (SIAR)**

**Versión:** 1.1
**Fecha:** 03 de Octubre de 2025

**Instrucciones para el Asistente de IA (Gemini CLI)**
- Este documento es la referencia principal y la **única fuente de verdad** para el "Proyecto SIAR".
- Todas tus respuestas, sugerencias de código y recomendaciones deben estar estrictamente alineadas con los objetivos, alcance y pila tecnológica definidos aquí.
- Prioriza siempre el alcance del **Producto Mínimo Viable (MVP)**. Descarta funcionalidades que no estén listadas en la sección 2.
- Cuando se solicite código, utiliza las tecnologías especificadas en la Sección 5.
- El objetivo es seguir las mejores prácticas de la ingeniería de software y la ingeniería ambiental.

---

**Sección 1: Visión y Misión del Proyecto**

- **Nombre del Proyecto:** Sistema de Identificación de Áreas para Reforestación (SIAR).
- **Visión:** Potenciar la restauración de ecosistemas a nivel global, facilitando la toma de decisiones informadas y basadas en datos para proyectos de reforestación.
- **Misión:** Desarrollar una herramienta de software (MVP) que analice variables geoespaciales y ambientales para identificar y clasificar las áreas más viables y prioritarias para la reforestación con especies nativas.

---

**Sección 2: Objetivos y Alcance del MVP**

- **Objetivo Principal del MVP:** Crear un sistema web funcional que, a partir de un área geográfica definida por el usuario, genere un mapa de viabilidad para la reforestación, destacando las zonas óptimas y recomendando especies nativas adecuadas.

- **Funcionalidades Dentro del Alcance (In-Scope):**
    1.  **Selección de Área:** Permitir al usuario definir un polígono de interés en un mapa interactivo.
    2.  **Análisis de Viabilidad:** Procesar en el backend las variables críticas para el área seleccionada.
    3.  **Visualización de Resultados:** Generar y mostrar un mapa de calor (heatmap) que clasifique las zonas en niveles de viabilidad (Alta, Media, Baja).
    4.  **Recomendación de Especies:** Sugerir una lista de especies nativas compatibles con las zonas de "Alta" viabilidad.
    5.  **Consulta de Datos:** Permitir al usuario hacer clic en una zona del mapa para ver un resumen de las variables que determinaron su clasificación.

- **Funcionalidades Fuera de Alcance (Out-of-Scope):**
    - Análisis de costos económicos, monitoreo en tiempo real, gestión de equipos, integración con redes sociales, análisis predictivo de cambio climático.

---

**Sección 3: Persona de Usuario Principal (MVP)**

- **Nombre:** Ana, la Planificadora Ambiental.
- **Rol:** Trabaja en una ONG local o agencia gubernamental.
- **Objetivo:** Identificar de manera rápida y científica qué terrenos degradados son los mejores candidatos para reforestar.
- **Frustración:** El proceso actual es manual, lento y requiere consultar múltiples fuentes de datos complejas.

---

**Sección 4: Variables Críticas y Fuentes de Datos (MVP)**

| Categoría | Variable Crítica | Fuente de Datos (Ejemplo) |
| :--- | :--- | :--- |
| **Suelo** | Tipo/Textura, Profundidad, Erosión | Mapas de suelos nacionales, datos geológicos. |
| **Topografía** | Pendiente, Altitud | Modelos Digitales de Elevación (DEM) de SRTM/ASTER. |
| **Clima** | Precipitación Media Anual | Datasets globales como WorldClim. |
| **Ecología** | Uso Actual del Suelo, Especies Nativas | Imágenes satelitales (Sentinel, Landsat), bases de datos de biodiversidad. |

---

**Sección 5: Pila Tecnológica (Tech Stack)**

- **Lenguaje Principal:** Python
- **Backend:** Django
- **Frontend:** React
- **Visualización de Mapas:** Leaflet.js
- **Base de Datos:** PostgreSQL con extensión PostGIS
- **Análisis Geoespacial (Python):** GeoPandas, Rasterio, GDAL
- **Entorno de Desarrollo:** Docker

---

**Sección 6: Arquitectura del Sistema (Simplificada)**

1.  **Frontend (React + Leaflet):** Usuario dibuja un polígono. Envía coordenadas vía API REST al backend.
2.  **Backend (Django + PostGIS):** Recibe el polígono, consulta las capas de datos, ejecuta el módulo de análisis y expone los resultados en la API.
3.  **Frontend:** Recibe los datos y los renderiza en el mapa.

---

**Sección 7: Glosario de Términos Clave**

- **MVP:** Minimum Viable Product.
- **SIG:** Sistema de Información Geográfica.
- **DEM:** Digital Elevation Model.
- **Especie Nativa:** Especie que pertenece a una región de forma natural.

---

**Sección 8: Estado Actual del Proyecto (Actualizado el 14 de Octubre de 2025)**

- **Completado:**
    - [x] Se definió la **"Fase 0: Configuración del Entorno y Esqueleto del Proyecto"** como el punto de partida estratégico.
        - **Razón de esta decisión:** Acordamos comenzar por la infraestructura para construir una base sólida, reproducible y escalable. Este enfoque nos permite verificar que todos los componentes (backend, frontend, base de datos) se comunican correctamente antes de empezar a desarrollar la lógica de negocio, minimizando así riesgos de integración futuros.
        - **Componentes de esta fase:** La fase incluye la creación de la estructura de directorios, la configuración de la orquestación de contenedores con `docker-compose.yml`, la creación de los `Dockerfile` para cada servicio y, finalmente, la inicialización de los esqueletos de los proyectos Django y React.
    - [x] Se crearon la estructura de directorios y todos los archivos de configuración iniciales de Docker (`docker-compose.yml`, `Dockerfile`s, `requirements.txt`).
    - [x] Se estableció el flujo de trabajo "Handshake/Handoff" como nuestro proceso estándar para garantizar la continuidad entre sesiones.

- **En Progreso:**
    - [ ] Instalación del entorno de desarrollo local por parte del usuario (WSL2 y Docker Desktop).

- **Siguiente Tarea:**
    - [ ] Una vez que Docker esté operativo, inicializar el esqueleto del proyecto Django usando el comando `docker compose run`.

- **Bloqueos o Dudas:**
    - [ ] El avance en la configuración del proyecto está en pausa hasta que Docker Desktop esté instalado y funcional en la máquina local.



