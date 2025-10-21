# **Documento Guía del Proyecto: Sistema de Identificación de Áreas para Reforestación (SIAR)**

**Versión:** 1.2
**Fecha:** 21 de Octubre de 2025

**Instrucciones para el Asistente de IA (Gemini CLI)**
- Este documento es la referencia principal y la **única fuente de verdad** para el "Proyecto SIAR".
- Todas tus respuestas, sugerencias de código y recomendaciones deben estar estrictamente alineadas con los objetivos, alcance y pila tecnológica definidos aquí.
- Prioriza siempre el alcance del **Producto Mínimo Viable (MVP)**. Descarta funcionalidades que no estén listadas en la sección 2.
- Al final de cada sesión de trabajo, el asistente debe leer este documento y añadir un nuevo bloque de resumen a la Sección 8, manteniendo la bitácora histórica y actualizando el resto de secciones según sea necesario.

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
- **Análisis Geoespacial (Python):** GeoPandas, Rasterio, GDAL, NumPy, Shapely
- **Entorno de Desarrollo:** Docker

---

**Sección 6: Arquitectura del Sistema (Simplificada)**

1.  **Frontend (React + Leaflet):** Usuario dibuja un polígono. Envía coordenadas vía API REST al backend.
2.  **Backend (Django + PostGIS):** Recibe el polígono, invoca al módulo de análisis (`core.py`) para procesar los datos, y expone los resultados en la API.
3.  **Frontend:** Recibe los datos y los renderiza en el mapa.

---

**Sección 7: Glosario de Términos Clave**

- **MVP:** Minimum Viable Product.
- **SIG:** Sistema de Información Geográfica.
- **DEM:** Digital Elevation Model.
- **Especie Nativa:** Especie que pertenece a una región de forma natural.

---

**Sección 8: Estado y Bitácora del Proyecto**

*Esta sección funciona como una bitácora cronológica del progreso.*

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

---

- **Progreso de Hoy (Sesión del 20 de Octubre de 2025):**
    - [x] Se actualizó GEMINI.md para robustecer el protocolo de inicio de sesión del proyecto.
    - [x] Se verificó que los modelos AnalysisResult y Species ya están definidos en analysis/models.py, adelantando el trabajo de la Fase 1.
    - [x] Se clarificó que la siguiente acción necesaria es la creación de las migraciones para los modelos existentes, no la escritura de su código.
- **Posición Actual:**
    - Nos encontramos en la Fase 1, listos para aplicar las migraciones de los modelos de datos ya definidos.
- **Siguiente Tarea Inmediata:**
    - [ ] Ejecutar el comando makemigrations para la app analysis para generar los archivos de migración correspondientes a los modelos Species y AnalysisResult.
- **Bloqueos o Dudas:**
    - [ ] Ninguno.

---
    
- **Progreso de Hoy(Sesión del 22 de Octubre de 2025)**:
- **Resumen Ejecutivo de la Sesión:**
   * Se dedicó gran parte de la sesión a solucionar problemas del entorno Docker, específicamente con montajes de volumen en Windows, y a resolver conflictos de migración en la aplicación analysis. Se logró poner en marcha el servicio de backend y aplicar las migraciones iniciales.
 - **Progreso:**
    - [x] Identificación y resolución de problemas de montaje de volumen de Docker en Windows.
    - [x] Reseteo completo de la base de datos y las migraciones de la aplicación analysis.
    - [x] Aplicación exitosa de las migraciones iniciales para los modelos AnalysisRequest, Species y AnalysisResult.
- **Posición Actual:**
    - Nos encontramos en la Fase 1 (Modelo de Datos y Creación de la API). Los modelos AnalysisRequest, Species y AnalysisResult están definidos y sus migraciones iniciales han sido aplicadas exitosamente a la base de datos.
- **Siguiente Tarea Inmediata:**
    - [ ] Crear los endpoints de API para los modelos Species y AnalysisResult.   
- **Bloqueos o Dudas:**
    - [x] Flujo de Trabajo de Desarrollo: Necesidad de reconstruir el contenedor backend en cada cambio de código debido a problemas con los montajes de volumen en Windows.

---

- **Resumen de la Sesión del 21 de Octubre de 2025:**
    - **Resumen Ejecutivo:** Se completó la Fase 1 con la implementación total de la API y se avanzó decisivamente en la Fase 2, construyendo y probando un motor de análisis geoespacial funcional de punta a punta que procesa pendiente y suelo, y guarda los resultados.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [En Progreso]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa
        - **Fase 4:** Integración Completa y Visualización de Resultados
    - **Hitos Clave de la Sesión:**
        - [x] Finalizada la API para los modelos `Species` y `AnalysisResult`.
        - [x] Corregido el flujo de Docker con un montaje de volumen para el backend.
        - [x] Creado un script para generar datos de muestra realistas (DEM y suelos).
        - [x] Implementado el núcleo del motor de análisis en `core.py` (carga, recorte, cálculo de pendiente, rasterización y combinación de criterios).
        - [x] Implementada la vectorización y guardado de los polígonos resultantes en la base de datos.
        - [x] Creado un script de prueba de integración (`test_api_integration.py`) que valida el flujo completo a través de una llamada a la API.
        - [x] ¡Logrado un flujo de análisis funcional de punta a punta!
    - **Posición Actual:**
        - Hemos completado la Fase 1 y la mayor parte de la Fase 2. Tenemos un motor de análisis funcional que se dispara desde la API y guarda resultados en la base de datos.
    - **Siguiente Tarea Inmediata:**
        - [ ] Añadir el criterio de **elevación** al algoritmo de análisis en `analysis/core.py`.
    - **Bloqueos o Dudas:**
        - [ ] Ninguno.

---

**Sección 9: Mejoras Futuras y Hoja de Ruta Post-MVP**

Esta sección documenta las mejoras estratégicas que se han identificado durante el desarrollo del MVP para ser consideradas en futuras versiones del proyecto.

- **Tareas Asíncronas:** La ejecución del análisis (`execute_analysis`) debe ser delegada a una cola de tareas en segundo plano (ej. Celery, Django-Q) para evitar que peticiones de larga duración bloqueen la API.
- **Integración de Datos Reales:** El sistema debe evolucionar para reemplazar los archivos de datos de muestra por un "Módulo de Adquisición de Datos" que se conecte a servicios externos y APIs (WMS, WCS, etc.) para obtener datos en tiempo real.
- **Suite de Pruebas Formal:** El script de prueba actual debe expandirse hasta convertirse en una suite de pruebas formal utilizando el framework de testing de Django, con una clara separación entre pruebas unitarias (para la lógica del motor) y pruebas de integración (para la API).
- **Refinamiento del Algoritmo:** El algoritmo de clasificación debe ser mejorado para incluir más criterios y para generar una clasificación más granular (ej. 'ALTO', 'MEDIO', 'BAJO') en lugar de un resultado binario.
