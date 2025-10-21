
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

### 2. Prompt de Fin de Sesión (El "Handoff")

**Objetivo:** Forzar a Gemini a resumir el trabajo realizado durante la sesión, incluyendo el contexto estratégico, para crear una actualización de estado autosuficiente. Este resumen se convierte en la actualización para la `GuíaProyecto.md`.

**Cuándo usarlo:** Cuando hayas terminado de trabajar por el día.

```markdown
Excelente trabajo hoy. Vamos a finalizar esta sesión.

Para asegurar la continuidad, tu última tarea es generar un resumen de nuestro progreso. Este resumen lo usaré para añadir al final de la Sección 8 del `GuíaProyecto.md` el progreso de esta sesión, manteniendo un registro acumulativo.

**Instrucciones para el Resumen:**
- El resumen debe ser autosuficiente y no depender de la memoria de la sesión.
- Debe incluir no solo las tareas técnicas, sino el contexto estratégico acordado.
- Utiliza el siguiente formato Markdown exacto, llenando cada sección con la información correspondiente de la sesión actual:
 
**Formato Requerido:**
````markdown
**Resumen Ejecutivo de la Sesión:**
*   (Resume aquí los logros estratégicos y decisiones clave de la sesión en 1-2 frases.)

---

**Hoja de Ruta del Proyecto (MVP):**
*   (Incrusta aquí el plan de fases del proyecto acordado, marcando el estado de cada fase, ej: [Completada], [En Progreso].)

---

**Arquitectura de Datos Envisionada:**
*   (Describe aquí la visión de la arquitectura de la base de datos, incluyendo los modelos principales y sus relaciones.)

---

**Estado Actual y Siguientes Pasos:**
- **Progreso de Hoy:**
    - [x] (Lista los logros técnicos y comandos clave ejecutados.)
- **Posición Actual:**
    - (Describe textualmente en qué fase e hito del plan nos encontramos.)
- **Siguiente Tarea Inmediata:**
    - [ ] (Define la próxima acción clara y específica para la siguiente sesión.)
- **Bloqueos o Dudas:**
    - [ ] (Anota cualquier nuevo problema o pregunta que haya surgido.)
````

Por favor, genera este bloque de resumen ahora. Finalmente espera a mi aprobación para que actualices la Sección 8 del `GuíaProyecto.md` con tu resumen.
```
