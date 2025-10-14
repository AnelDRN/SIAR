
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

Por favor, lee y procesa ambos documentos. Confirma que has adoptado tu rol como 'Arquitecto de Software GIS' y que comprendes la 'Siguiente Tarea' definida en la Sección 8.

**Espera mi siguiente instrucción después de tu confirmación.**
```

---

### 2. Prompt de Fin de Sesión (El "Handoff")

**Objetivo:** Forzar a Gemini a resumir el trabajo realizado durante la sesión. Este resumen se convierte en la actualización que pegarás en tu `PROJECT_GUIDE.md`, creando un ciclo perfecto de continuidad.

**Cuándo usarlo:** Cuando hayas terminado de trabajar por el día.

```markdown
Excelente trabajo hoy. Vamos a finalizar esta sesión.

Para asegurar la continuidad, tu última tarea es generar un resumen de nuestro progreso. Este resumen lo usaré para actualizar la Sección 8 del `PROJECT_GUIDE.md` para nuestra próxima sesión.

**Instrucciones para el Resumen:**
- Sé conciso y utiliza listas.
- Basa el resumen **únicamente** en lo que discutimos y logramos en la conversación de hoy.
- Utiliza el siguiente formato Markdown exacto:

**Formato Requerido:**
```markdown
- **Completado:**
    - [x] [Descripción de la tarea completada hoy, ej: Implementación del endpoint POST /api/v1/analysis/].
    - [x] [Otra tarea completada hoy].
- **En Progreso:**
    - [ ] [La tarea que quedó a medias, si aplica].
- **Siguiente Tarea:**
    - [ ] [La próxima tarea clara y definida que abordaremos en la siguiente sesión].
- **Bloqueos o Dudas:**
    - [ ] [Nuevas preguntas o problemas que surgieron hoy, ej: "Necesitamos decidir la mejor forma de manejar análisis de larga duración (tareas asíncronas)"].
```

Por favor, genera este bloque de resumen ahora.
```

### El Flujo de Trabajo Completo en 3 Pasos:

1.  **Inicio de Sesión:**
    *   Abre tu archivo `PROJECT_GUIDE.md` local.
    *   Copia y pega el **Prompt de Inicio de Sesión** en el CLI.
    *   Rellena los dos marcadores con el contenido de tus archivos `GEMINI_PERSONA.md` y `PROJECT_GUIDE.md`.
    *   Comienza a trabajar.

2.  **Fin de Sesión:**
    *   Copia y pega el **Prompt de Fin de Sesión** en el CLI.
    *   Gemini generará el bloque de resumen en Markdown.

3.  **Actualización (El Cierre del Ciclo):**
    *   Copia el resumen generado por Gemini.
    *   Pégalo en la **Sección 8** de tu archivo `PROJECT_GUIDE.md` local, reemplazando el contenido anterior.
    *   Guarda el archivo.

¡Listo! La próxima vez que inicies una sesión, tu `PROJECT_GUIDE.md` estará perfectamente actualizado, y el ciclo comenzará de nuevo. Este sistema profesional te ahorrará incontables horas y mantendrá tu proyecto (y a tu asistente de IA) siempre en el camino correcto.

