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

**Sección 8: Estado Actual del Proyecto (Actualizado el 15 de Octubre de 2025)**

### 1. Resumen Ejecutivo del Proyecto

Este proyecto busca desarrollar el Sistema de Identificación de Áreas para Reforestación (SIAR). Hemos completado la Fase 0 de configuración del entorno y hemos establecido un plan de desarrollo por fases y una visión clara de la arquitectura de datos. Actualmente, estamos en la Fase 1, habiendo creado y probado con éxito el primer endpoint de la API.

---

### 2. Hoja de Ruta del Proyecto (MVP)

- **Fase 0:** Configuración del Entorno y Esqueleto (Completada)
    - [x] Definición de la estrategia de infraestructura y herramientas.
    - [x] Creación de la estructura de directorios y archivos Docker iniciales.
    - [x] Establecimiento del flujo de trabajo "Handshake/Handoff".
- **Fase 1:** Modelo de Datos y Creación de la API (En Progreso)
    - [ ] Definir Modelos de Datos (`AnalysisRequest`, `AnalysisResult`, `Species`).
    - [ ] Crear Endpoints de API básicos para cada modelo.
    - [ ] Integrar Django Rest Framework.
- **Fase 2:** Implementación del Núcleo de Análisis Geoespacial
    - [ ] Desarrollar la lógica de procesamiento de datos geoespaciales.
    - [ ] Implementar el algoritmo de clasificación de viabilidad.
- **Fase 3:** Desarrollo del Frontend y Visualización de Mapa
    - [ ] Inicializar el proyecto React.
    - [ ] Integrar mapa interactivo y herramienta de dibujo de polígonos.
- **Fase 4:** Integración Completa y Visualización de Resultados
    - [ ] Conectar Frontend y Backend.
    - [ ] Renderizar el mapa de calor de resultados.
    - [ ] Mostrar información detallada y especies recomendadas.

---

### 3. Arquitectura de Datos Envisionada

- **Modelos Principales:**
    - `AnalysisRequest`: El registro de cada solicitud de análisis del usuario.
    - `AnalysisResult`: Almacena las zonas de resultado (Alta, Media, Baja) para cada solicitud.
    - `Species`: Catálogo de referencia de las especies nativas.
- **Relación Principal:** `[AnalysisRequest] 1--* [AnalysisResult] *--* [Species]`

---

### 4. Estado Actual y Siguientes Pasos

- **Progreso de Hoy (Sesión del 15 de Octubre de 2025):**
    - [x] Se completó la **Fase 0** (configuración de Docker, Django skeleton, DB connection).
    - [x] Se iniciaron los primeros hitos de la **Fase 1**:
        - [x] Creación de la app `analysis`.
        - [x] Integración de `Django Rest Framework` y `DRF-GIS`.
        - [x] Definición, migración y prueba exitosa del modelo `AnalysisRequest` y su endpoint de API (`GET /api/v1/analysis-requests/`).

- **Posición Actual:**
    - Nos encontramos en la **Fase 1**, ejecutando el hito "Definir Modelos de Datos". El modelo `AnalysisRequest` está completo.

- **Siguiente Tarea Inmediata:**
    - [ ] Aprobar la adición del modelo `AnalysisResult` (el segundo modelo de nuestra arquitectura de datos definida) al archivo `analysis/models.py`, para luego crear y aplicar su migración.

- **Bloqueos o Dudas:**
    - [ ] Ninguno.
4
- **Progreso de Hoy (Sesión del 20 de Octubre de 2025):**
    - [x] Se actualizó GEMINI.md para robustecer el protocolo de inicio de sesión del proyecto.
    - [x] Se verificó que los modelos AnalysisResult y Species ya están definidos en analysis/models.py, adelantando el trabajo de la Fase 1.
    - [x] Se clarificó que la siguiente acción necesaria es la creación de las migraciones para los modelos existentes, no la escritura de su código.

- **Posición Actual:**
    - Nos encontramos en la Fase 1, listos para aplicar las migraciones de los modelos de datos ya definidos.
    - Siguiente Tarea Inmediata:

- **Siguiente Tarea Inmediata:**
    - [ ] Ejecutar el comando makemigrations para la app analysis para generar los archivos de migración correspondientes a los modelos Species y AnalysisResult.

- **Bloqueos o Dudas:**
    - [ ] Ninguno.
    
- **Progreso de Hoy(Sesión del 22 de Octubre de 2025)**:
- **Resumen Ejecutivo de la Sesión:**
   * Se dedicó gran parte de la sesión a solucionar problemas del entorno Docker, específicamente con montajes
      de volumen en Windows, y a resolver conflictos de migración en la aplicación analysis. Se logró poner en
      marcha el servicio de backend y aplicar las migraciones iniciales.Cabe aclarar que el usuario menciono que esta trabajando en el desarrollo del proyecto en distintos ordenadores de manera no simultanea, manteniendo la sincronizacion entre ellos con github. 

 - **Progreso:**
    - [x] Identificación y resolución de problemas de montaje de volumen de Docker en Windows.
    - [x] Configuración del servicio backend para que funcione sin montajes de volumen, dependiendo de la
        copia de código en la imagen.
    - [x] Reseteo completo de la base de datos y las migraciones de la aplicación analysis.
    - [x] Aplicación exitosa de las migraciones iniciales para los modelos AnalysisRequest, Species y
        AnalysisResult.
    - [ ] Intento fallido de hacer que el campo area_of_interest sea no nulo nuevamente debido a problemas
        persistentes con el sistema de migraciones de Django.  

- **Posición Actual:**
    - Nos encontramos en la Fase 1 (Modelo de Datos y Creación de la API). Los modelos AnalysisRequest,
        Species y AnalysisResult están definidos y sus migraciones iniciales han sido aplicadas exitosamente
        a la base de datos. El campo area_of_interest en AnalysisRequest actualmente acepta valores nulos.   

- **Siguiente Tarea Inmediata:**
    - [ ] Abordar el problema de hacer que el campo area_of_interest sea no nulo en el modelo
        AnalysisRequest. Esto podría requerir una investigación más profunda del sistema de migraciones de
        Django o una solución manual.
    - [ ] Crear los endpoints de API para los modelos Species y AnalysisResult.   

- **Bloqueos o Dudas:**
    - [x] Flujo de Trabajo de Desarrollo: Necesidad de reconstruir el contenedor backend en cada cambio de
        código debido a problemas con los montajes de volumen en Windows.Para la proxima sesion intentar configurar los contenedores para que esto no sea una necesidad.
    - [x] Portabilidad: Confirmación de la portabilidad del entorno a otros equipos.
