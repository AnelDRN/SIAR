# **Material para Video Académico del Proyecto SIAR**

A continuación se presenta el desglose completo del material necesario para producir un video académico de 15 a 20 minutos sobre el proyecto SIAR.

---

## **1. Tabla de Tiempos Estimada**

| # | Sección | Duración Estimada | Tiempo Acumulado |
| :- | :--- | :--- | :--- |
| 1 | Introducción y Objetivos | 2.5 minutos | 2:30 |
| 2 | Metodología y Arquitectura | 6.0 minutos | 8:30 |
| 3 | Caso de Estudio: Mapa y Fases | 4.0 minutos | 12:30 |
| 4 | Análisis de Impacto Ambiental | 3.5 minutos | 16:00 |
| 5 | Conclusiones y Cierre | 2.0 minutos | 18:00 |
| | **Total** | **18 minutos** | |

---

## **2. Guion Narrativo Completo**

**(Inicio del Video)**

**[00:00 - 00:30] (Música inspiradora de fondo, imágenes de alta calidad de bosques frondosos y biodiversidad, que lentamente se transicionan a imágenes de deforestación, sequía y noticias sobre el cambio climático.)**

**Narrador:** Nuestro planeta enfrenta una encrucijada. El cambio climático, impulsado en gran medida por la deforestación, amenaza la estabilidad de nuestros ecosistemas y el futuro de nuestra civilización. Cada hectárea de bosque que perdemos no solo libera carbono a la atmósfera, sino que también destruye un santuario de biodiversidad y desestabiliza ciclos hídricos vitales. La reforestación ha surgido como una de las soluciones más poderosas a nuestro alcance, pero una pregunta fundamental persiste: ¿dónde y cómo empezamos?

**[00:30 - 01:15] (Aparece el logo de SIAR y el título del proyecto. Transición a un screencast rápido de la aplicación web en acción.)**

**Narrador:** Para responder a esta pregunta, hemos desarrollado el Sistema de Identificación de Áreas para Reforestación, o SIAR. Es una aplicación web geoespacial de código abierto diseñada para democratizar y acelerar la planificación de proyectos de restauración de ecosistemas. SIAR transforma un proceso que antes tomaba semanas de análisis manual por expertos en una tarea que cualquier planificador ambiental puede realizar en minutos.

**[01:15 - 02:30] (La pantalla muestra la diapositiva de "Objetivos del Proyecto" con los puntos clave apareciendo secuencialmente.)**

**Narrador:** El objetivo principal de este proyecto fue crear una herramienta funcional y robusta que automatizara la identificación de áreas óptimas para reforestar. Para lograrlo, nos propusimos objetivos específicos claros: primero, desarrollar una interfaz interactiva donde el usuario pudiera definir cualquier área de interés en el mundo. Segundo, automatizar la obtención de datos científicos de fuentes reconocidas para analizar criterios clave como la topografía, el suelo y el clima. Tercero, implementar un motor de análisis basado en un modelo de superposición ponderada, permitiendo al usuario ajustar la importancia de cada criterio. Y finalmente, visualizar los resultados de forma clara, transparente y accionable, incluyendo recomendaciones de especies nativas para las zonas más viables.

**[02:30 - 03:30] (La pantalla muestra la diapositiva de "Metodologías Utilizadas" con los logos de las tecnologías apareciendo.)**

**Narrador:** Para construir SIAR, adoptamos una pila tecnológica moderna y escalable. El proyecto está completamente contenerizado con Docker, garantizando su reproducibilidad. El backend utiliza Python con el framework Django, ideal por su robustez y el vasto ecosistema científico de Python. Para las tareas de análisis intensivo, implementamos un sistema de procesamiento asíncrono con Celery y Redis, evitando que la interfaz se bloquee. La base de datos es PostgreSQL, potenciada con la extensión PostGIS para el manejo de datos geoespaciales complejos.

**[03:30 - 04:30] (Continúa la diapositiva de "Metodologías", ahora mostrando un diagrama de flujo simplificado del frontend.)**

**Narrador:** En el frontend, utilizamos React con TypeScript para construir una interfaz de usuario interactiva y segura. La visualización de mapas se maneja con la librería Leaflet.js, conocida por su ligereza y potencia. Finalmente, todo el análisis raster y vectorial se realiza con el conjunto de librerías geoespaciales estándar de la industria: GDAL, Rasterio y GeoPandas.

**[04:30 - 06:00] (La pantalla muestra el diagrama de "Flujo de Trabajo del Análisis" animado.)**

**Narrador:** El flujo de trabajo de SIAR está diseñado para ser eficiente y desacoplado. Todo comienza cuando el usuario dibuja un polígono en el mapa. Al hacer clic en "Analizar", el frontend envía la geometría y los pesos seleccionados a nuestra API REST. El backend de Django recibe esta petición, crea un registro en la base de datos con estado "Pendiente" y delega inmediatamente el trabajo pesado a un worker de Celery. Este worker es el que ejecuta el análisis principal: contacta a los proveedores de datos, descarga la información, procesa cada uno de los cinco criterios, y realiza la superposición ponderada para crear el mapa de viabilidad final. Mientras tanto, el frontend sondea el estado de la tarea. Una vez completada, solicita los resultados finales y los dibuja en el mapa.

**[06:00 - 08:30] (La pantalla muestra el screencast de la aplicación, haciendo zoom en la sección de sliders de ponderación.)**

**Narrador:** El corazón científico de SIAR es el análisis de superposición ponderada. No todos los criterios son igualmente importantes en todos los contextos. Por ejemplo, en una zona montañosa, la pendiente podría ser el factor más crítico. En una región árida, sería la precipitación. SIAR permite al usuario experto reflejar este conocimiento local asignando un peso, de 1 a 5, a cada uno de los cinco criterios: la pendiente del terreno, la altitud, la composición del suelo, la precipitación anual y la cobertura actual del suelo. La puntuación final de cada píxel en el mapa ya no es una simple suma, sino el resultado de esta fórmula ponderada, lo que produce un análisis mucho más matizado y adaptable a la realidad de cada proyecto. La clasificación en "Alta", "Media" o "Baja" viabilidad se determina dinámicamente como un porcentaje del puntaje máximo posible.

**[08:30 - 09:30] (La pantalla muestra el mapa del caso de estudio: la Cuenca del Canal de Panamá.)**

**Narrador:** Para validar SIAR, lo aplicamos a un caso de estudio complejo y de importancia global: la Cuenca del Canal de Panamá. Esta región es un mosaico de bosques, áreas agrícolas, zonas urbanas y los grandes lagos que alimentan el canal. Su salud ecológica es vital para el comercio mundial. Seleccionamos un polígono que abarca tanto zonas boscosas protegidas como áreas de pastizales degradados, un escenario perfecto para probar la capacidad de discriminación de nuestro sistema.

**[09:30 - 11:00] (La pantalla muestra la diapositiva de "Actividades del Proyecto por Fase".)**

**Narrador:** El desarrollo del proyecto fue un proceso iterativo y estructurado. Iniciamos con la configuración del entorno y el esqueleto de la aplicación. La Fase 1 se centró en construir la API y los modelos de datos. En la Fase 2, desarrollamos el motor de análisis inicial. La Fase 3 vio la construcción de la interfaz de usuario en React. La Fase 4 fue la más larga, donde integramos todo el sistema de forma asíncrona y conectamos los proveedores de datos reales. Finalmente, la Fase 5 de profesionalización fue donde implementamos las características clave que hemos visto: la transparencia de resultados y el análisis ponderado, además de una depuración exhaustiva que nos permitió superar desafíos técnicos como la sincronización de migraciones y la configuración de servicios WCS.

**[11:00 - 12:30] (Screencast mostrando los resultados del análisis en el mapa de Panamá. El cursor hace clic en un polígono verde.)**

**Narrador:** Como pueden ver, SIAR ha procesado el área y la ha clasificado. Las zonas en verde oscuro son las de más alta viabilidad. Al hacer clic en una de ellas, el sistema nos muestra el porqué de su clasificación en la sección de "Datos de Transparencia": una pendiente promedio de 8.5 grados, 120 metros de altitud, una precipitación anual de más de 2500 milímetros... y, crucialmente, el sistema nos informa que el tipo de cobertura actual es "Pradera", lo que la convierte en un candidato ideal para reforestar. Además, nos provee una lista de especies nativas de la región, obtenidas de GBIF, aptas para este ecosistema.

**[12:30 - 13:30] (La pantalla muestra la diapositiva sobre "Fuentes de GEI" con infografías.)**

**Narrador:** El análisis de nuestro caso de estudio también nos permite contextualizar su impacto ambiental. Las principales fuentes de Gases de Efecto Invernadero en la cuenca provienen del cambio de uso de la tierra, principalmente la conversión de bosques a pastizales para la ganadería. Reforestar las áreas identificadas por SIAR no solo restauraría el paisaje, sino que actuaría como una medida directa para contrarrestar estas emisiones.

**[13:30 - 14:30] (La pantalla muestra la diapositiva de "Línea Base Ambiental".)**

**Narrador:** El sistema nos permite establecer una línea base ambiental clara. Sabemos que el área de estudio posee suelos tropicales, una topografía ondulada, un régimen de lluvias abundante y una biodiversidad que, aunque rica en las zonas protegidas, es pobre en las áreas de pastizales que SIAR ha priorizado. Este es nuestro punto de partida para la restauración.

**[14:30 - 16:00] (La pantalla muestra la Matriz de Impactos Ambientales.)**

**Narrador:** Un proyecto de reforestación, aunque netamente positivo, tiene impactos que deben ser gestionados. Durante la fase de plantación, existen impactos negativos menores y temporales, como la alteración del suelo. Sin embargo, como muestra esta matriz, los impactos positivos a largo plazo son abrumadoramente superiores en magnitud e importancia. Hablamos de una mejora drástica en la estructura del suelo, la regulación del ciclo hidrológico, la creación de hábitat y, por supuesto, el secuestro masivo de carbono. Para mitigar los pequeños impactos negativos, proponemos medidas simples como el uso de técnicas de plantación de bajo impacto y la socialización del proyecto con las comunidades locales.

**[16:00 - 17:00] (Diapositiva de "Medidas de Mitigación del Cambio Climático".)**

**Narrador:** El beneficio principal es la mitigación del cambio climático. Al reforestar las áreas que SIAR identifica, creamos nuevos sumideros de carbono. Utilizando estimaciones conservadoras, un proyecto derivado de este análisis podría llegar a secuestrar miles de toneladas de CO2 cada año, contribuyendo directamente a las metas climáticas de Panamá y del mundo.

**[17:00 - 18:00] (Diapositiva de Conclusiones. Transición a la diapositiva de presentación del equipo.)**

**Narrador:** En conclusión, el proyecto SIAR ha validado exitosamente su hipótesis: es posible construir una herramienta potente, accesible y científicamente rigurosa para optimizar la planificación de la reforestación. Hemos superado desafíos técnicos significativos para entregar un producto funcional que abstrae la complejidad del análisis geoespacial. El futuro de SIAR podría incluir análisis económicos y proyecciones de cambio climático, pero su estado actual ya representa un valioso aporte a la caja de herramientas de la conservación.

**[RECOMENDACIÓN DE PRESENTACIÓN DEL EQUIPO: En esta diapositiva final, mostrar un video corto o fotografías profesionales de los integrantes del equipo. El narrador puede hacer una pausa o la música puede subir de volumen.]**

**Narrador:** Este proyecto ha sido posible gracias al trabajo de un equipo dedicado. [PAUSA] Gracias por su atención.

**(Fin del video. Logo de SIAR y créditos finales.)**

---

## **3. Diapositivas con Texto y Recursos Visuales Sugeridos**

Aquí tienes el desglose diapositiva por diapositiva.

---
**Diapositiva 1: Título**
*   **Texto:**
    *   SIAR: Sistema de Identificación de Áreas para Reforestación
    *   Un Enfoque Tecnológico para la Restauración de Ecosistemas
    *   [Nombres del equipo], [Universidad]
*   **Contenido Visual:** Fondo con una imagen de alta calidad, mitad bosque frondoso, mitad imagen satelital con polígonos de análisis. Logo de SIAR prominente.

---
**Diapositiva 2: El Problema Global**
*   **Texto:**
    *   **El Desafío:** La deforestación impulsa el cambio climático y la pérdida de biodiversidad.
    *   **La Solución:** La reforestación es una estrategia clave de mitigación.
    *   **La Barrera:** ¿Cómo identificar las mejores áreas de forma rápida y científica?
*   **Contenido Visual:**
    *   **[Prompt para IA generadora de imágenes]:** "Una infografía dramática que muestra un globo terráqueo. De un lado, un bosque verde y saludable con un icono de '+O₂'. Del otro lado, un área marrón y deforestada con un icono de '+CO₂' subiendo a la atmósfera."

---
**Diapositiva 3: Objetivos del Proyecto**
*   **Texto:**
    *   **General:** Automatizar el análisis de viabilidad para la reforestación.
    *   **Específicos:**
        *   Permitir definición interactiva de áreas de interés.
        *   Integrar datos de fuentes científicas (Suelo, Clima, Topografía).
        *   Implementar análisis ponderado ajustable por el usuario.
        *   Visualizar resultados (Alta, Media, Baja viabilidad).
        *   Ofrecer transparencia de datos y recomendación de especies.
*   **Contenido Visual:** Iconos simples representando cada objetivo específico (un globo terráqueo con un polígono, una pila de datos, una balanza, un mapa de calor, una lupa sobre un dato, una hoja de árbol).

---
**Diapositiva 4: Metodología - Pila Tecnológica**
*   **Texto:** "Una Arquitectura Moderna, Robusta y Escalable"
*   **Contenido Visual:**
    *   **[Prompt para IA generadora de diagramas]:** "Crear un diagrama visualmente atractivo mostrando los logos de las siguientes tecnologías organizadas en tres capas: 'Frontend' (React, TypeScript, Leaflet.js, Material-UI), 'Backend' (Python, Django, Celery, Redis), y 'Datos' (PostgreSQL con el logo de PostGIS, GDAL, Rasterio). Conectar las capas con flechas indicando el flujo de datos. Todo el sistema debe estar dentro de una caja más grande con el logo de Docker."

---
**Diapositiva 5: Metodología - Flujo de Trabajo**
*   **Texto:** "Un Proceso Asíncrono y Desacoplado"
*   **Contenido Visual:**
    *   **[Prompt para IA generadora de diagramas]:** "Crear un diagrama de flujo animado con 5 pasos: 1. 'Usuario' dibuja polígono en el 'Frontend'. 2. 'Frontend' envía petición a 'API Backend'. 3. 'API Backend' crea la tarea y la envía al 'Broker (Redis)'. 4. 'Worker (Celery)' procesa el análisis. 5. 'Frontend' sondea el estado y muestra los resultados del 'Backend'. Usar iconos para cada componente."

---
**Diapositiva 6: El Motor Científico - Superposición Ponderada**
*   **Texto:**
    *   El usuario ajusta el "peso" (importancia) de cada criterio.
    *   `Puntuación Final = (Criterio1 * Peso1) + (Criterio2 * Peso2) + ...`
*   **Contenido Visual:**
    *   Izquierda: Screencast corto mostrando los 5 sliders siendo ajustados.
    *   Derecha: **[Prompt para IA generadora de animaciones]:** "Crear una animación conceptual simple. Cinco capas semitransparentes, cada una con un patrón diferente (rayas, puntos, etc.) y un número (su peso), se deslizan una sobre otra. Al alinearse, se combinan en una capa final con un patrón de colores complejo."

---
**Diapositiva 7: Caso de Estudio - Cuenca del Canal de Panamá**
*   **Texto:**
    *   **Ubicación:** Cuenca Hidrográfica del Canal de Panamá.
    *   **Importancia:** Vital para el comercio mundial y la biodiversidad regional.
    *   **Escenario:** Mosaico complejo de bosques, agua y áreas deforestadas.
*   **Contenido Visual:**
    *   **[Prompt para IA generadora de mapas]:** "Generar un mapa satelital de alta resolución centrado en la Cuenca del Canal de Panamá. Destacar con un polígono de ejemplo de color amarillo translúcido un área que contenga parte del Parque Nacional Soberanía y zonas de pastizales al este del parque."

---
**Diapositiva 8: Fases del Proyecto**
*   **Texto:** "De la Idea a la Implementación Profesional"
    *   Fase 0: Configuración y Andamiaje
    *   Fase 1-3: Desarrollo de API, Motor de Análisis y Frontend
    *   Fase 4: Integración Asíncrona y Conexión a Datos Reales
    *   Fase 5: Profesionalización (Transparencia y Análisis Ponderado)
*   **Contenido Visual:** Una línea de tiempo horizontal simple con 5 hitos.

---
**Diapositiva 9: Resultados del Análisis**
*   **Texto:**
    *   Discriminación efectiva de áreas aptas y no aptas.
    *   Transparencia total: ¿Por qué esta área es viable?
    *   Recomendaciones de especies nativas para acción inmediata.
*   **Contenido Visual:** Una captura de pantalla del popup de resultados de SIAR, mostrando claramente la sección "Datos de Transparencia" y la lista de especies recomendadas. Usar flechas o resaltados para enfocar la atención en estas secciones.

---
**Diapositiva 10: Análisis de Impacto Ambiental**
*   **Texto:** "Evaluando el Ciclo de Vida del Proyecto de Reforestación"
*   **Contenido Visual:**
    *   **[Prompt para IA generadora de tablas]:** "Crear una tabla con el título 'Matriz de Impactos Ambientales'. Columnas: 'Componente Ambiental', 'Impacto en Fase de Plantación', 'Impacto a Largo Plazo'. Filas: 'Suelo', 'Agua', 'Aire', 'Biodiversidad'. Rellenar las celdas con texto conciso y usar iconos de flecha verde hacia arriba para impacto positivo y flecha roja hacia abajo para impacto negativo."

---
**Diapositiva 11: Mitigación y Beneficio Climático**
*   **Texto:**
    *   Medidas: Uso de especies nativas, técnicas de bajo impacto.
    *   Beneficio Principal: Creación de un nuevo sumidero de carbono.
    *   Potencial: 10,000 hectáreas reforestadas ≈ 50,000 - 150,000 toneladas de CO₂ secuestradas por año.
*   **Contenido Visual:**
    *   **[Prompt para IA generadora de infografías]:** "Crear una infografía simple y limpia. A la izquierda, un icono de un árbol con el texto 'Especies Nativas'. A la derecha, un icono de una nube de CO₂ con una flecha grande y verde apuntando hacia abajo, con el texto '50-150k Toneladas CO₂/año'."

---
**Diapositiva 12: Conclusiones**
*   **Texto:**
    *   **Éxito Validado:** SIAR es una herramienta funcional y efectiva.
    *   **Impacto:** Reduce tiempo y costos, democratizando la planificación ambiental.
    *   **Futuro:** Análisis económico, proyecciones climáticas, gestión de usuarios.
*   **Contenido Visual:** Iconos para "Economía" (€/$), "Clima Futuro" (un termómetro con un gráfico de tendencia) y "Usuarios" (un icono de perfil).

---
**Diapositiva 13: Equipo y Cierre**
*   **Texto:** "Gracias por su atención"
*   **Contenido Visual:**
    *   **Recomendación:** En esta diapositiva, mostrar un video corto o fotografías profesionales de los integrantes del equipo. Puede ser en un formato de grilla o apareciendo secuencialmente.
    *   Logo de SIAR y de la universidad.
    *   [URL del proyecto o repositorio de GitHub, si aplica]
