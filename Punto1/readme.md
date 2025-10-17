## Modelo del Perceptrón
Entrada: vector x ∈ R² (coordenadas (x, y) en el plano)

Parámetros: pesos w = [w₁, w₂] y sesgo b

Función lineal: z = w₁x₁ + w₂x₂ + b

Activación (clasificación): ŷ = sign(z) → devuelve 1 si z ≥ 0, -1 si z < 0

Es un clasificador lineal; sólo puede resolver problemas linealmente separables

Regla de Aprendizaje (Perceptron Learning Rule)
Para cada muestra (x, y) con etiqueta y ∈ {1, -1}:

Calcular predicción ŷ = sign(w·x + b)

Si ŷ ≠ y, actualizar:

w ← w + η * (y - ŷ) * x

b ← b + η * (y - ŷ)

Donde η (eta) es la tasa de aprendizaje (learning rate).

El algoritmo itera sobre el conjunto de entrenamiento (épocas) hasta:

Convergencia: ninguna actualización en una época completa

Límite: alcanzar el número máximo de épocas

## Componentes Principales
AgentePerceptron:

Gestiona pesos w₁, w₂, sesgo b

Implementa regla de aprendizaje

Controla convergencia

AgentePunto:

Almacena coordenadas (x,y) y etiquetas

Actualiza colores según clasificación

Proporciona feedback visual

Interfaz Gráfica:

Sliders: tasa aprendizaje (0.01-1.0), iteraciones (10-500)

Visualización: puntos, línea decisión, línea real

Métricas: precisión, iteraciones, pesos

## Casos de Prueba
Preciso y Lento

η = 0.01, iteraciones = 200

Convergencia lenta pero estable

Rápido y Menos Preciso

η = 0.5, iteraciones = 50

Convergencia rápida con oscilaciones
