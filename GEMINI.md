
### 1. Prompt de Inicio de Sesión (El "Handshake")

**Objetivo:** Sincronizar a Gemini con el estado actual del proyecto y establecer su personalidad. Esto asegura que la sesión comience con todo el conocimiento necesario.

**Cuándo usarlo:** Al principio de CADA nueva sesión de trabajo.

```markdown
Hola Gemini. Vamos a iniciar una sesión de trabajo para el 'Proyecto SIAR'.

Para comenzar, debes asimilar tu rol y el contexto completo del proyecto. Sigue estas dos instrucciones en orden:

**1. Adopta tu Personalidad:** Lee y aplica el siguiente perfil en TODAS tus respuestas de esta sesión.
```
[@Persona.md]
```

**2. Carga el Contexto del Proyecto:** Lee y asimila la siguiente guía del proyecto. Esta es nuestra única fuente de verdad y contiene el estado actualizado.
```
[@GuíaProyecto.md]
```

**3. Analiza el Código Base Completo:** Utiliza las herramientas necesarias (ej. `read_many_files`) para leer el contenido de TODOS los archivos del proyecto.

**4. Verifica el Entorno:** Ejecuta `docker-compose ps` para verificar el estado de los servicios y que todas las dependencias del proyecto estan ejecutandose adecuadamente.

Por favor, ejecuta todos los pasos anteriores. Al finalizar, confirma lo siguiente:
- Que has adoptado tu rol.
- Que has analizado la totalidad de los archivos del proyecto.
- El estado de los servicios Docker.
- El resumen del estado actual del proyecto y la 'Siguiente Tarea'.

**Espera mi siguiente instrucción después de tu confirmación.**
```

---

### 2. Prompt de Fin de Sesión (Handoff & Refactor)

**Objetivo:** Forzar a Gemini a consolidar el progreso de la sesión directamente en el `GuíaProyecto.md`, manteniendo el documento siempre limpio y actualizado.

**Cuándo usarlo:** Cuando hayas terminado de trabajar por el día.

```markdown
Excelente trabajo hoy. Vamos a finalizar esta sesión con nuestro proceso de "Handoff & Refactor".

Tu tarea final es actualizar nuestro documento `GuíaProyecto.md` para reflejar todo el progreso de la sesión de hoy. Sigue estos pasos:

1.  **Lee el `GuíaProyecto.md`:** Carga la versión más reciente del documento.
2.  **Prepara un Bloque de Resumen:** Crea un nuevo bloque de resumen para la sesión de hoy usando el formato definido a continuación.
3.  **Actualiza la Bitácora:** Añade el nuevo bloque de resumen al final de la **Sección 8**. No borres el contenido histórico.
4.  **Actualiza el Resto del Documento:** Revisa y actualiza cualquier otra sección que haya cambiado (ej. Pila Tecnológica, Arquitectura, etc.). Si hemos discutido nuevas mejoras, añádelas a la **Sección 9**.
5.  **Presenta el Documento Completo:** Muéstrame el contenido íntegro y final del `GuíaProyecto.md` actualizado para mi revisión y aprobación.
6.  **Espera la Aprobación:** No escribas los cambios hasta que yo te dé la confirmación final.

**Formato para el Bloque de Resumen de la Sesión:**
````markdown
- **Resumen de la Sesión del [FECHA]:**
    - **Resumen Ejecutivo:** (Resume aquí los logros estratégicos y decisiones clave de la sesión en 1-2 frases.)
    - **Hoja de Ruta del Proyecto (MVP):**
        - (Incrusta aquí el plan de fases del proyecto, marcando el estado actualizado de cada fase.)
    - **Hitos Clave de la Sesión:**
        - [x] (Lista los logros técnicos y comandos clave ejecutados.)
    - **Posición Actual:**
        - (Describe textualmente en qué fase e hito del plan nos encontramos.)
    - **Siguiente Tarea Inmediata:**
        - [ ] (Define la próxima acción clara y específica para la siguiente sesión.)
    - **Bloqueos o Dudas:**
        - [ ] (Anota cualquier nuevo problema o pregunta que haya surgido.)
````

Por favor, comienza el proceso de "Handoff & Refactor" ahora.
```
