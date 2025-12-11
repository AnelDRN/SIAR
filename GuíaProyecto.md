# **Documento Guía del Proyecto: Sistema de Identificación de Áreas para Reforestación (SIAR)**

**Versión:** 2.2
**Fecha:** 10 de Diciembre de 2025

**Instrucciones para el Asistente de IA (Gemini CLI)**
- Este documento es la referencia principal y la **única fuente de verdad** para el "Proyecto SIAR".
- Representa el estado actual y final del desarrollo funcional del proyecto.
- Al final de cada sesión de trabajo, el asistente debe leer este documento y añadir un nuevo bloque de resumen a la Sección 8, manteniendo la bitácora histórica y actualizando el resto de secciones según sea necesario.

---

**Sección 1: Visión y Misión del Proyecto**

- **Nombre del Proyecto:** Sistema de Identificación de Áreas para Reforestación (SIAR).
- **Visión:** Potenciar la restauración de ecosistemas a nivel global, facilitando la toma de decisiones informadas y basadas en datos para proyectos de reforestación.
- **Misión:** Desarrollar una herramienta de software robusta que analice variables geoespaciales y ambientales para identificar y clasificar las áreas más viables y prioritarias para la reforestación con especies nativas.

---

**Sección 2: Objetivos y Alcance del Sistema Actual**

- **Objetivo Principal:** Proveer un sistema web funcional y profesional que, a partir de un área geográfica definida por el usuario, genere un mapa de viabilidad para la reforestación, destacando las zonas óptimas, recomendando especies nativas adecuadas y excluyendo áreas no viables.

- **Funcionalidades Implementadas:**
    1.  **Selección de Área Interactiva:** Permitir al usuario definir un polígono de interés en un mapa dinámico.
    2.  **Análisis Asíncrono y Robusto:** Procesar en el backend las variables críticas para el área seleccionada de forma asíncrona (con Celery/Redis).
    3.  **Feedback en Tiempo Real:** Informar al usuario sobre el progreso del análisis con mensajes de estado dinámicos.
    4.  **Visualización de Resultados (Heatmap):** Generar y mostrar un mapa de calor que clasifica las zonas en niveles de viabilidad (Alta, Media, Baja).
    5.  **Recomendación de Especies Nativas:** Sugerir una lista de especies nativas compatibles con las zonas de "Alta" viabilidad (integración con GBIF).
    6.  **Consulta de Datos Detallada:** Permitir al usuario hacer clic en una zona del mapa para ver un resumen de las variables y el criterio limitante.
    7.  **Análisis de Cobertura del Suelo:** Excluir automáticamente áreas no reforestables (ciudades, agua, etc.) usando datos de ESA WorldCover.
    8.  **Historial de Análisis:** Guardar y permitir la revisión de análisis previos.

---

**Sección 3: Persona de Usuario Principal**

- **Nombre:** Ana, la Planificadora Ambiental.
- **Rol:** Trabaja en una ONG local, agencia gubernamental o empresa de consultoría ambiental.
- **Objetivo:** Identificar de manera rápida y científica qué terrenos degradados son los mejores candidatos para reforestar.
- **Frustración (Solucionada por SIAR):** El proceso manual de recopilación y análisis de datos geoespaciales es lento y subjetivo.

---

**Sección 4: Variables Críticas y Fuentes de Datos**

| Categoría | Variable Crítica | Fuente de Datos (Implementada) |
| :--- | :--- | :--- |
| **Suelo** | Textura (Arcilla, Limo), pH | ISRIC SoilGrids (vía librería `soilgrids`) |
| **Topografía** | Pendiente, Altitud | OpenTopography SRTMGL1 (vía librería `bmi-topography`) |
| **Clima** | Precipitación Media Anual | WorldClim v2.1 (archivos GeoTIFF locales) |
| **Ecología** | Uso Actual del Suelo | ESA WorldCover 2020 (vía servicio WCS) |
| **Ecología** | Especies Nativas | GBIF (Global Biodiversity Information Facility) (vía API REST) |

---

**Sección 5: Pila Tecnológica (Tech Stack)**

- **Lenguaje Principal (Backend):** Python 3.9
- **Backend:** Django, Django Rest Framework, DRF-GIS
- **Frontend:** React, TypeScript
- **Visualización de Mapas:** Leaflet.js, React-Leaflet, Leaflet-Draw
- **Base de Datos:** PostgreSQL con extensión PostGIS
- **Análisis Geoespacial (Python):** GeoPandas, Rasterio, GDAL, NumPy, Shapely, OWSLib
- **Procesamiento Asíncrono:** Celery, Redis
- **Configuración de Entorno:** `django-environ`
- **Entorno de Desarrollo y Producción:** Docker, Docker-Compose
- **UI Framework Frontend:** Material-UI (MUI)
- **Librerías de Acceso a Datos:** `bmi-topography`, `soilgrids`

---

**Sección 6: Arquitectura del Sistema**

1.  **Frontend (React + Leaflet + MUI):** El usuario define un polígono. La aplicación envía las coordenadas vía API REST al backend y entra en modo "polling" para consultar el estado del análisis, mostrando el progreso en tiempo real. Una vez completado, renderiza los resultados GeoJSON en el mapa.
2.  **Backend (Django + PostGIS + Celery/Redis):** Una API recibe la solicitud y la delega a un worker de Celery. Esto mantiene la API receptiva. La API expone endpoints para consultar el estado de la tarea y obtener los resultados finales.
3.  **Módulo de Análisis Geoespacial (`core.py`):** Ejecutado por Celery, este módulo orquesta a los proveedores de datos para obtener la información, la procesa, la reclasifica y la sintetiza para generar el mapa de viabilidad y las recomendaciones de especies.

---

**Sección 7: Glosario de Términos Clave**

- **MVP:** Minimum Viable Product.
- **SIG:** Sistema de Información Geográfica.
- **DEM:** Digital Elevation Model.
- **WCS:** Web Coverage Service.
- **GeoJSON:** Formato estándar para codificar información geográfica.

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

- **Resumen de la Sesión del 29 de Octubre de 2025:**
    - **Resumen Ejecutivo:** Se dedicó la sesión a intentar configurar el entorno de desarrollo del frontend, encontrando numerosos problemas de compatibilidad y configuración con React, react-leaflet y Docker. Se resolvieron múltiples conflictos de dependencias, pero el frontend aún no es completamente funcional.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [Completada]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa [En Progreso - Bloqueado]
        - **Fase 4:** Integración Completa y Visualización de Resultados
    - **Hitos Clave de la Sesión:**
        - [x] Completado el motor de análisis del backend (criterio de altitud, clasificación granular).
        - [x] Andamiaje de la aplicación frontend con React y TypeScript.
        - [x] Instalación de Leaflet.
        - [x] Configuración del entorno de desarrollo Docker para el frontend.
        - [x] Depuración y resolución de la corrupción de `npm audit fix --force`.
        - [x] Depuración y resolución de la incompatibilidad de la versión de Node.js (`ERR_OSSL_EVP_UNSUPPORTED`).
        - [x] Depuración y resolución de problemas de compatibilidad de `react-leaflet-draw` (decisión de eliminarlo).
        - [x] Depuración y resolución de conflictos de versión de `react` / `react-dom`.
        - [x] Depuración y resolución de conflictos de versión de `react-scripts`.
        - [x] Depuración y resolución del error `ReactDOM.render is not a function`.
        - [ ] Renderizado exitoso del mapa base en el frontend.
        - [ ] Integración directa de `leaflet-draw`.
    - **Posición Actual:** Nos encontramos en la Fase 3, con el entorno de desarrollo del frontend configurado, pero la aplicación React aún no se renderiza correctamente debido a un un error en `react-leaflet` (`div-overlay.js`).
    - **Siguiente Tarea Inmediata:**
        - [ ] Diagnosticar y resolver el error `at ./node_modules/@react-leaflet/core/lib/div-overlay.js` en el frontend.
        - [ ] Eliminar la corrección de los iconos de Leaflet de `Map.tsx` (propuesta pendiente).
        - [ ] Integrar `leaflet-draw` directamente en `Map.tsx`.
    - **Bloqueos o Dudas:**
        - [x] Persistente error en el frontend relacionado con `react-leaflet` y `div-overlay.js` después de múltiples intentos de resolución de dependencias.

---

- **Resumen de la Sesión del 31 de Octubre de 2025:**
    - **Resumen Ejecutivo:** Se diagnosticaron y resolvieron múltiples problemas de serialización de GeoJSON y renderizado en el frontend, permitiendo la correcta visualización de los resultados del análisis, incluyendo la consulta de datos y la recomendación de especies.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [Completada]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa [Completada]
        - **Fase 4:** Integración Completa y Visualización de Resultados [Completada]
    - **Hitos Clave de la Sesión:**
        - [x] Diagnóstico y resolución del error "Invalid GeoJSON object" en el frontend, causado por la serialización incorrecta de la geometría en el backend.
        - [x] Modificación de `backend/analysis/serializers.py` para usar un `ModelSerializer` estándar para `AnalysisResult`.
        - [x] Corrección del método `list` en `AnalysisResultViewSet` en `backend/analysis/views.py` para construir manualmente la `FeatureCollection` y serializar `result_area` a un objeto GeoJSON.
        - [x] Corrección de errores de indentación e importación en `backend/analysis/views.py`.
        - [x] Reemplazo del componente `GeoJSON` de `react-leaflet` por la iteración sobre `analysisResults.features` y renderizado de componentes `Polygon` individuales en `frontend/src/components/MapView.tsx`.
        - [x] Verificación de que el backend ahora devuelve GeoJSON válido y el frontend lo renderiza correctamente.
        - [x] Creación y ejecución del comando `generate_species_data.py` para poblar la base de datos con especies de ejemplo.
        - [x] Modificación de `backend/analysis/core.py` para asociar especies aleatorias a los objetos `AnalysisResult` con viabilidad 'HIGH'.
        - [x] Actualización de `AnalysisResultSerializer` para incluir los datos completos de las especies recomendadas.
        - [x] Implementación de la funcionalidad de "Consulta de Datos" en el frontend, mostrando popups con el nivel de viabilidad.
        - [x] Implementación de la funcionalidad de "Recomendación de Especies" en el frontend, mostrando especies recomendadas en los popups para zonas de alta viabilidad.
    - **Posición Actual:** Nos encontramos en la **Fase 4**, con la integración completa del frontend y backend para la visualización de los resultados del análisis, incluyendo la consulta de datos y la recomendación de especies. El MVP está funcional.
    - **Siguiente Tarea Inmediata:**
        - [ ] Refactorizar el código del frontend para mejorar la legibilidad y mantenibilidad, especialmente en `MapView.tsx`.
        - [ ] Mejorar la interfaz de usuario (UI) y la experiencia de usuario (UX) del frontend.
        - [ ] Implementar pruebas unitarias y de integración para el frontend.
    - **Bloqueos o Dudas:**
        - [ ] Ninguno.

---

- **Resumen de la Sesión del 22 de Noviembre de 2025:**
    - **Resumen Ejecutivo:** Sesión enfocada en la profesionalización del proyecto. Se refactorizó el backend para usar tareas asíncronas con Celery/Redis y se externalizó la configuración usando `django-environ`. Se ampliaron las pruebas del backend, incluyendo un test de integración para el algoritmo de análisis. El frontend se adaptó para manejar el flujo asíncrono, refactorizando componentes clave y mejorando la UI/UX con Material-UI. La sesión se vio afectada por problemas persistentes de sincronización de Docker en el entorno del usuario, lo que requirió la eliminación del montaje de volumen del frontend y un proceso de depuración exhaustivo.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [Completada]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa [Completada]
        - **Fase 4:** Integración Completa y Visualización de Resultados [Completada]
    - **Hitos Clave de la Sesión:**
        - **Backend:**
            - [x] Añadida dependencia `celery` y `redis` a `backend/requirements.txt`.
            - [x] Actualizado `docker-compose.yml` para incluir servicios de `redis` y `celery_worker`.
            - [x] Configurado Celery en el proyecto Django.
            - [x] Creado `backend/analysis/tasks.py` con tarea Celery para `execute_analysis`.
            - [x] Modificado `AnalysisRequest` para incluir campo `status` y corregido `__str__` (usando `id` en lugar de `request_id`).
            - [x] Aplicadas migraciones de base de datos para el campo `status`.
            - [x] Actualizado `AnalysisRequestViewSet` para disparar la tarea Celery asíncronamente.
            - [x] Externalizada la configuración de `core.py` a variables de entorno usando `django-environ`.
            - [x] Creados archivos `.env` y `.env.example` en el backend.
            - [x] Actualizado `backend/backend/settings.py` para usar `django-environ` y leer parámetros de análisis.
            - [x] Refactorizado `backend/analysis/core.py` para usar la configuración de Django.
            - [x] Actualizado `docker-compose.yml` para pasar el `.env` a los servicios `backend` y `celery_worker`.
            - [x] Añadida suite de pruebas de integración para la lógica de análisis en `backend/analysis/tests.py`.
        - **Frontend:**
            - [x] Adaptado el frontend para manejar el flujo asíncrono del backend (polling de estado).
            - [x] Refactorizado `MapView.tsx` para usar un nuevo hook `useAnalysis.ts` y componentes dedicados (`StatusOverlay`, `AnalysisLayer`).
            - [x] Mejorada la UI/UX con Material-UI (MUI), incluyendo `Layout.tsx` e `InfoPanel.tsx`.
            - [x] Depurados problemas de renderizado del mapa (`ERR_EMPTY_RESPONSE`, fondo negro) causados por la configuración de Vite y problemas de sincronización de volúmenes de Docker.
            - [x] Corregido el acceso a `status` en el frontend (buscando en `response.data.properties.status`).
            - [x] Solucionados conflictos de sintaxis de `Grid` de MUI (MUI v1 vs v2).
            - [x] Eliminado el montaje de volumen del frontend (`./frontend:/app`) en `docker-compose.yml` para resolver problemas de sincronización de archivos, copiando el código directamente en la imagen Docker en la construcción.
            - [x] Revertido `App.tsx` al layout de Flexbox con `<Box>` para garantizar la estabilidad de la visualización del mapa, sacrificando temporalmente el layout de `Grid` de MUI debido a problemas persistentes de compatibilidad de renderizado.
    - **Posición Actual:**
        - El proyecto es un MVP funcional y estable.
        - El backend ha sido profesionalizado con tareas asíncronas, configuración externa y pruebas de integración.
        - El frontend ha sido profesionalizado para manejar el flujo asíncrono y presenta una UI mejorada con Material-UI, utilizando un layout flexible (`Box`).
        - La visualización del mapa es funcional.
    - **Siguiente Tarea Inmediata:**
        - [ ] **Integración de Datos Reales:** Investigar y conectar fuentes de datos geoespaciales (WCS) para la precipitación media anual y el uso del suelo.
    - **Bloqueos o Dudas:**
        - [ ] La integración de datos reales es una tarea compleja que requerirá una investigación exhaustiva de las APIs y formatos de datos disponibles.

---

- **Resumen de la Sesión del 26 de Noviembre de 2025:**
    - **Resumen Ejecutivo:** Se realizó una refactorización exhaustiva del módulo de adquisición de datos para integrar fuentes de datos reales y modernas. Se reemplazaron proveedores WCS inestables por APIs dedicadas (`bmi-topography` para DEM, `soilgrids` para suelo) y un proveedor de archivo local para precipitación. Se resolvieron múltiples errores de configuración y compatibilidad con servicios externos, dejando el pipeline de análisis geoespacial funcional con datos reales (excepto especies nativas).
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [Completada]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa [Completada]
        - **Fase 4:** Integración Completa y Visualización de Resultados [En Progreso - Pendiente GBIF]
            - Integración de Datos Reales: [Completada - Pendiente GBIF]
    - **Hitos Clave de la Sesión:**
        - [x] Refactorización del módulo `data_acquisition.py` a un patrón de proveedor basado en clases.
        - [x] Actualización de `backend/backend/settings.py`, `backend/.env` y `backend/.env.example` para una configuración de proveedor más flexible y para eliminar variables obsoletas (`DEM_WCS_URL`, `DEM_COVERAGE_ID`, `SOIL_WCS_URL`, `SOIL_MAP_TEMPLATE`, `SOIL_SILT_PROPERTY`, `SOIL_CLAY_PROPERTY`, `PRECIPITATION_WCS_URL`, `PRECIPITATION_COVERAGE_ID`).
        - [x] Actualización del test de integración (`backend/analysis/tests.py`) para usar los nuevos mocks de proveedores.
        - [x] Depuración y resolución del error `TypeError` en `AnalysisRequestSerializer` (`create` method).
        - [x] Depuración y resolución del error `400 Bad Request` por `ALLOWED_HOSTS` en el backend.
        - [x] Depuración y resolución del error `ModuleNotFoundError: No module named 'owslib'` en Celery worker mediante reconstrucción de imágenes.
        - [x] Depuración y resolución de errores de formato (`Unsupported format: image/tiff` -> `GeoTIFF`) y parámetros faltantes (`WIDTH`/`HEIGHT`) con el servidor WCS de Digital Earth Africa (`ows.digitalearth.africa`).
        - [x] **Decisión clave:** Reemplazar el `CopernicusDEMProvider` (WCS) por el `OpenTopographyDEMProvider` (usando la librería `bmi-topography`) para el DEM.
        - [x] Instalación de la dependencia `bmi-topography`.
        - [x] Depuración y resolución del `TypeError` en la inicialización de `bmi-topography` (requiere `bbox` en constructor).
        - [x] **Decisión clave:** Reemplazar el `SoilProvider` (WCS) por el `SoilGridsProvider` (usando la librería `soilgrids`) para datos de suelo.
        - [x] Instalación de la dependencia `soilgrids`.
        - [x] Depuración y resolución del `TypeError` (`get_coverage_data() got an unexpected keyword argument 'output_crs'`) en `SoilGridsProvider`.
        - [x] **Decisión clave:** Reemplazar el `PrecipitationProvider` (WCS) por un `LocalFilePrecipitationProvider` (usando archivo local) para precipitación.
        - [x] Descarga manual y verificación del archivo `wc2.1_30s_prec.zip` y su ubicación en `backend/analysis/data/worldclim/`.
        - [x] Descompresión exitosa de `wc2.1_30s_prec.zip`, obteniendo los archivos GeoTIFF mensuales.
        - [x] Depuración y resolución del `ValueError` (`Please provide width and height values when the coordinate system (crs) is EPSG 4326.`) en `SoilGridsProvider`.
        - [ ] Implementación y corrección final de `LocalFilePrecipitationProvider` en `core.py`.
        - [ ] Verificación de que el pipeline de análisis se ejecuta completamente sin errores con todos los nuevos proveedores de datos.
    - **Posición Actual:** Los proveedores para DEM, Suelo y Cobertura del Suelo están funcionando con fuentes de datos fiables. El `LocalFilePrecipitationProvider` ha sido implementado en `data_acquisition.py` y los archivos GeoTIFF están disponibles localmente, pero su integración final en `core.py` y la verificación de todo el pipeline aún están pendientes.
    - **Siguiente Tarea Inmediata:**
        1.  Completar la integración del `LocalFilePrecipitationProvider` en `core.py`.
        2.  Verificar que el pipeline de análisis se ejecuta completamente sin errores para todas las variables críticas.
        3.  Implementar la integración de datos para **Especies Nativas** usando la API de GBIF.
    - **Bloqueos o Dudas:** Ninguno.
- **Resumen de la Sesión del 27 de Noviembre de 2025:**
    - **Resumen Ejecutivo:** Se dedicó la sesión a mejorar la experiencia de usuario y la robustez del backend. Se implementaron mejoras en la interfaz de usuario, como mensajes de estado detallados y validación de área. Se diagnosticó y solucionó un problema crítico en el motor de análisis que causaba resultados de baja viabilidad. Se revirtió una implementación de "tiling" que causaba inestabilidad, dejando el sistema en un estado funcional y mejorado.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 5:** Profesionalización y Refuerzo de Calidad [En Progreso]
            - Backend: [En Progreso]
            - Frontend: [En Progreso]
    - **Hitos Clave de la Sesión:**
        - [x] **Mejoras de UI/UX:**
            - [x] Implementado un sistema de mensajes de estado dinámicos durante el análisis.
            - [x] Añadida validación en el frontend para limitar el tamaño mínimo y máximo del área de análisis.
            - [x] Limpieza de la vista inicial del mapa, eliminando polígonos de prueba estáticos.
            - [x] Creados componentes de React para mostrar un resumen de resultados y una lista detallada de especies.
        - [x] **Diagnóstico y Corrección de Lógica de Análisis:**
            - [x] Identificado que los datos de suelo (silt, clay) de SoilGrids se proveen en g/kg.
            - [x] Corregido el `core.py` para convertir las unidades de suelo a porcentaje antes de la evaluación.
            - [x] Ajustados los umbrales de los criterios de análisis para ser más permisivos y generar resultados más realistas.
        - [x] **Reversión de Cambios:**
            - [x] Revertida la implementación de la estrategia de "tiling" en el backend para restaurar la funcionalidad principal del análisis.
            - [x] Eliminado el modelo de `parent_request` y las migraciones asociadas.
    - **Posición Actual:**
        - El MVP es funcional. El motor de análisis ahora produce resultados más precisos y variados. La interfaz de usuario proporciona un feedback más claro al usuario.
    - **Siguiente Tarea Inmediata:**
        - [ ] Re-evaluar e implementar de forma estable la estrategia de **tiling** para el manejo de áreas grandes, asegurando que no se introduzcan errores.
    - **Bloqueos o Dudas:**
        - [x] **Error de Backend Persistente:** Existe un problema recurrente con el backend que causa fallos en el análisis, incluso con la lógica de tiling revertida. La causa raíz parece ser el límite de la API de OpenTopography. Se necesita una API Key para solucionar esto de forma definitiva.

---
- **Resumen de la Sesión del 27 de Noviembre de 2025 (Continuación):**
    - **Resumen Ejecutivo:** La sesión se centró en robustecer el sistema contra los límites de las API externas. Se diagnosticó que los fallos del backend se debían a la superación de la cuota anónima de la API de OpenTopography y se implementó una solución permanente mediante el uso de una API key.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 5:** Profesionalización y Refuerzo de Calidad [En Progreso]
    - **Hitos Clave de la Sesión:**
        - [x] Diagnosticado el límite de la API de OpenTopography como causa de los fallos del backend.
        - [x] Investigada la documentación de `bmi-topography` para el uso de API keys.
        - [x] Actualizado `backend/backend/settings.py` para leer la variable de entorno `OPENTOPOGRAPHY_API_KEY`.
        - [x] Actualizado `backend/analysis/data_acquisition.py` para inyectar la API key en las peticiones a OpenTopography.
        - [x] Actualizado `backend/.env.example` para incluir la nueva variable.
    - **Posición Actual:**
        - El código del backend ha sido modificado para solucionar el problema de límites de la API de OpenTopography. La solución está pendiente de verificación.
    - **Siguiente Tarea Inmediata:**
        1.  [ ] Que el usuario solucione los problemas de su entorno Docker local.
        2.  [ ] Reconstruir las imágenes Docker para aplicar los cambios (`docker-compose build`).
        3.  [ ] Ejecutar un análisis de prueba para confirmar que la API key soluciona el error con OpenTopography.
        4.  [ ] Implementar la integración de datos para **Especies Nativas** usando la API de GBIF.
    - **Bloqueos o Dudas:**
        - [x] **El entorno Docker del usuario no es funcional**, lo que impide la compilación y verificación de la solución. Requiere una acción por parte del usuario (reinicio del sistema).

---
- **Resumen de la Sesión del 30 de Noviembre de 2025 (Sincronización):**
    - **Resumen Ejecutivo:** Se realizó una sincronización completa del estado del proyecto, verificando que el código base está más avanzado que la última bitácora registrada. El MVP es funcional, con un backend robusto que utiliza tareas asíncronas, configuración externalizada y proveedores de datos reales (OpenTopography, SoilGrids, GBIF, WorldClim local). El frontend está adaptado al flujo asíncrono y presenta una UI/UX mejorada.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [Completada]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa [Completada]
        - **Fase 4:** Integración Completa y Visualización de Resultados [Completada]
        - **Fase 5:** Profesionalización y Refuerzo de Calidad [Completada]
    - **Hitos Clave de la Sesión (Verificados en el Código):**
        - [x] Verificada la integración exitosa de la API Key de OpenTopography en el `OpenTopographyDEMProvider`.
        - [x] Verificada la implementación completa del `GBIFAPIProvider` y su integración en `core.py` para la recomendación de especies.
        - [x] Confirmado que el frontend gestiona correctamente el ciclo de vida del análisis asíncrono, incluyendo el polling de estado y la visualización de resultados y especies.
        - [x] Verificado que el entorno Docker del proyecto es completamente funcional.
    - **Posición Actual:** El proyecto es un MVP funcional y completo. El backend es estable, consume datos de fuentes reales y el frontend está integrado para visualizar los resultados, incluyendo las especies recomendadas.
    - **Bloqueos o Dudas:**
        - [ ] Ninguno.

---
- **Resumen de la Sesión del 30 de Noviembre de 2025 (Continuación - Resolución de Bugs):**
    - **Resumen Ejecutivo:** Sesión intensiva dedicada a la depuración y resolución de dos bugs críticos: la no visualización de especies recomendadas y el funcionamiento incorrecto del "fly-to" en el mapa, además de una regresión que causaba la desaparición del polígono. Se identificó y resolvió una compleja interacción entre el entorno Docker (problemas de montajes de volumen y caché) y la lógica de procesamiento de geometría. La aplicación es ahora completamente funcional y estable.
    - **Hoja de Ruta del Proyecto (MVP):**
        - **Fase 0:** Configuración del Entorno y Esqueleto [Completada]
        - **Fase 1:** Modelo de Datos y Creación de la API [Completada]
        - **Fase 2:** Implementación del Núcleo de Análisis Geoespacial [Completada]
        - **Fase 3:** Desarrollo del Frontend y Visualización de Mapa [Completada]
        - **Fase 4:** Integración Completa y Visualización de Resultados [Completada]
        - **Fase 5:** Profesionalización y Refuerzo de Calidad [Completada]
    - **Hitos Clave de la Sesión:**
        - [x] **Diagnóstico y Corrección de Regresión:** Identificación de conflicto de lógica en `MapView.tsx` (`DrawControlLayer`) causando la desaparición del polígono, y corrección.
        - [x] **Diagnóstico y Corrección de "Fly to":** Identificación de prop faltante (`selectedPolygon`) en `MapView.tsx` desde `App.tsx` y corrección.
        - [x] **Diagnóstico y Corrección de Especies No Visibles (Backend):**
            - [x] Identificación de problema de `volumes` en `docker-compose.yml` que impedía la aplicación de cambios en el backend.
            - [x] Eliminación de `volumes` para `backend` y `celery_worker` para forzar el uso del código de la imagen.
            - [x] Identificación del error `Polygon with clockwise exterior ring` de la API de GBIF persistente.
            - [x] Implementación de lógica manual de inversión de coordenadas en `GBIFAPIProvider` para garantizar orden antihorario, superando inconsistencias con `shapely.ops.orient`.
        - [x] **Limpieza de Código:** Eliminación de todos los `console.log` de depuración del frontend.
        - [x] **Refactorización Frontend:** Extracción de `DrawControlLayer` y `MapFlyTo` de `MapView.tsx` a sus propios archivos.
    - **Posición Actual:** El MVP es completamente funcional y estable. Todos los bugs reportados han sido resueltos.
    - **Siguiente Tarea Inmediata:**
        - [ ] Revisión y potencial refactorización del componente `MapView.tsx` para mejorar la legibilidad y modularidad.
    - **Bloqueos o Dudas:**
        - [ ] Ninguno.

---
- **Resumen de la Sesión del 1 de Diciembre de 2025:**
    - **Resumen Ejecutivo:** Se implementó la funcionalidad de "Historial de Análisis" y se definió una nueva hoja de ruta para elevar la calidad del software a un nivel profesional. La implementación del historial introdujo varios bugs en cascada (tanto en el backend como en el frontend) que fueron depurados y resueltos. Luego, se inició la Fase 1 de la nueva hoja de ruta ("Análisis de Cobertura del Suelo"), pero la sesión concluyó mientras se depuraba un error de conexión con el servicio externo WCS.
    - **Hoja de Ruta del Proyecto (Profesional):**
        - **Fase 1:** Implementar Análisis de Cobertura del Suelo [En Progreso - BLOQUEADO]
        - **Fase 2:** Aumentar la Transparencia de Resultados [Pendiente]
        - **Fase 3:** Implementar Análisis Ponderado [Pendiente]
    - **Hitos Clave de la Sesión:**
        - [x] Implementación de la UI para el historial de análisis con pestañas en `InfoPanel.tsx`.
        - [x] Creación del hook `useAnalysisHistory.ts` para obtener datos del historial.
        - [x] Creación del componente `AnalysisHistory.tsx` para mostrar la lista.
        - [x] Refactorización de `App.tsx` y `useAnalysis.ts` para manejar la carga de resultados históricos.
        - [x] **Depuración de `useAnalysisHistory.ts`:** Corregido el error `response.data.sort is not a function` al procesar la `FeatureCollection` de la API.
        - [x] **Depuración de `App.tsx`:** Corregida la condición en `useEffect` que causaba llamadas a la API con `id` indefinido.
        - [x] **Definición de Hoja de Ruta Profesional:** Analizada la utilidad del software y definida una estrategia de 3 fases para mejorarlo (Cobertura, Transparencia, Ponderación).
        - [x] **Inicio de Fase 1:**
            - [x] Añadido "interruptor" (feature toggle) `ENABLE_LAND_COVER_ANALYSIS`.
            - [x] Actualizado el modelo `AnalysisResult` y aplicadas las migraciones de BD.
            - [x] Implementado `LandCoverProvider` para el servicio WCS de cobertura del suelo.
            - [x] Integrado el proveedor en `core.py` (con varios ciclos de depuración para `KeyError` y `UnboundLocalError`).
    - **Posición Actual:**
        - Nos encontramos en la **Fase 1** de la nueva hoja de ruta profesional. Estamos bloqueados intentando implementar el criterio de **Cobertura del Suelo**.
    - **Siguiente Tarea Inmediata:**
        - [ ] Diagnosticar y resolver el error `CoverageNotDefined` que devuelve el servicio WCS. El plan actual es forzar una reconstrucción sin caché de los contenedores Docker para descartar un problema de entorno y luego volver a ejecutar el script de diagnóstico `inspect_wcs.py`.
    - **Bloqueos o Dudas:**
        - [x] **Error `CoverageNotDefined` del WCS:** El análisis falla porque el servicio externo `https://ows.digitalearth.africa/wcs` rechaza la petición para la capa `esa_worldcover_2020`.
        - [x] **Posible Discrepancia en Entorno Docker:** Sospechamos que el contenedor de Docker puede no estar usando la versión más reciente de los archivos de configuración (`.env`), lo que impide una depuración correcta del error WCS.

---
- **Resumen de la Sesión del 10 de Diciembre de 2025:**
    - **Resumen Ejecutivo:** Se confirmó que todo el desarrollo de funcionalidades, incluyendo la "Hoja de Ruta de Profesionalización", está completo. El foco del proyecto ha pivotado hacia la consolidación, la documentación final y la mejora de la portabilidad.
    - **Hoja de Ruta del Proyecto (Estado Final):**
        - **Fase 0-5 (MVP y Profesionalización):** [Completadas]
    - **Hitos Clave de la Sesión:**
        - [x] Confirmación de la finalización de todo el desarrollo de funcionalidades.
        - [x] Generación del informe académico final del proyecto (`Informe_Academico_SIAR.md`).
        - [x] Actualización de la guía del proyecto para reflejar el estado de desarrollo completado.
    - **Posición Actual:**
        - El desarrollo de funcionalidades ha concluido. El proyecto entra en una fase de **consolidación y documentación**.
    - **Siguiente Tarea Inmediata:**
        - [ ] Mejorar la documentación (`README.md`) y revisar la configuración de Docker para asegurar que el proyecto se pueda ejecutar en cualquier máquina con mínimos pasos.
    - **Bloqueos o Dudas:**
        - [ ] Ninguno.

---

**Sección 9: Hoja de Ruta de Profesionalización (Completada)**

*   **Fase 1: Implementar Análisis de Cobertura del Suelo.**
    *   **Objetivo:** Excluir áreas no reforestables (ciudades, agua, etc.).
    *   **Estado:** *[Completada]*

*   **Fase 2: Aumentar la Transparencia de Resultados.**
    *   **Objetivo:** Guardar y mostrar los valores de datos reales para cada criterio.
    *   **Estado:** *[Completada]*

*   **Fase 3: Implementar Análisis Ponderado.**
    - **Objetivo:** Permitir al usuario ajustar la importancia relativa de cada criterio.
    - **Estado:** *[Completada]*

---
**Sección 10: Guía de Despliegue y Portabilidad**

El enfoque actual del proyecto es asegurar que cualquier desarrollador pueda clonar y ejecutar SIAR sin fricciones. Los objetivos de esta nueva fase son:

1.  **Revisar y Documentar Variables de Entorno:** Asegurar que el archivo `.env.example` esté completo y que cada variable esté claramente explicada en el `README.md`.
2.  **Simplificar el Proceso de Inicio:** El objetivo es que el proyecto se pueda iniciar con un único comando (`docker-compose up --build`).
3.  **Crear un `README.md` Integral:** El archivo `README.md` principal debe ser el único documento que un nuevo usuario necesite leer para entender el proyecto y ponerlo en marcha.