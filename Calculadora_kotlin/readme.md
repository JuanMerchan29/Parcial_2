## Encapsulamiento
Aplicación en el código:

-Variables protegidas (protected) para memoria e historial

-Métodos privados para conversiones internas de ángulos

-Interfaz pública controlada mediante métodos específicos

-Beneficios logrados:

-Estado interno protegido contra modificaciones directas

-Validaciones centralizadas en puntos de acceso

-Implementación oculta detrás de una interfaz limpia

-Facilita el mantenimiento y evolución del código

## Herencia

Implementación:

-Clase base Calculadora con operaciones aritméticas básicas

-Clase derivada CalculadoraCientifica que extiende la funcionalidad

-Reutilización de atributos y métodos de la clase padre

-Ventajas obtenidas:

-Evita duplicación de código entre operaciones básicas y científicas

-Jerarquía lógica que refleja la especialización progresiva

-Extensibilidad sin modificar el código base existente

-Organización clara de responsabilidades

## Polimorfismo

Aplicación práctica:
Sobrecarga de métodos: Múltiples versiones de sumar, restar, etc. para diferentes tipos de datos
Funciones lambda: Comportamientos parametrizables en el ExpressionParser
Manejo uniforme: Misma interfaz para diferentes operaciones matemáticas

Resultados:
-Código más flexible y reutilizable

-Interfaz consistente para el usuario

-Fácil adición de nuevas operaciones sin afectar existentes

-Reducción de código repetitivo

## Manejo de Excepciones
Implementación:

-Clase personalizada CalculadoraException para errores específicos del dominio
-Validaciones en puntos críticos (división por cero, logaritmos de negativos)

-Mensajes claros y informativos para el usuario

-Beneficios:

-Aplicación más robusta y confiable

-Mejor experiencia de usuario con mensajes específicos

-Prevención de estados inconsistentes

-Fácil depuración y mantenimiento

## Conclusión

-La implementación demuestra una aplicación efectiva de los principios POO, resultando en:
-Código mantenible y organizado

-Sistema extensible para nuevas funcionalidades

-Arquitectura robusta con manejo adecuado de errores

-Interfaz coherente y fácil de usar
