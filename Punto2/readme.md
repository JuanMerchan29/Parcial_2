## Componentes Clave del Sistema
1. Agentes de Operación

Especializados en operaciones matemáticas específicas

Cada agente maneja una operación: suma, resta, multiplicación, división, potencia

Procesan tareas de forma independiente cuando reciben operandos

2. Agente de Entrada/Salida (E/S)

Coordina todo el proceso de cálculo

Parse expresiones matemáticas en tareas individuales

Gestiona dependencias entre tareas

Distribuye trabajo y recolecta resultados

3. Modelo de Comunicación

Sistema de mensajería asíncrona entre agentes

Bandejas de entrada para cada agente

Entrega centralizada de mensajes a través del modelo

## Sincronización y Entrega de Mensajes

Gestión de Estados:

Cada tarea tiene un estado (pendiente/completada)

El agente E/S rastrea dependencias entre tareas

Solo se envían tareas cuyos operandos están disponibles

## Manejo de Errores

Control de Errores Matemáticos:

Detección de división por cero

Manejo de errores en operaciones de potencia

Propagación de excepciones a través del sistema

Recuperación de Errores:

Mensajes de error estructurados

Finalización controlada de la evaluación

Información clara al usuario sobre el error
