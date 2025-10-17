import mesa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import random

class AgentePerceptron(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Inicializar pesos y sesgo aleatoriamente
        self.peso1 = random.uniform(-1, 1)
        self.peso2 = random.uniform(-1, 1)
        self.sesgo = random.uniform(-1, 1)
        self.tasa_aprendizaje = 0.1
        self.iteracion_actual = 0
        self.max_iteraciones = 100
        self.entrenando = False
        self.convergio = False
        self.historial_pesos = []
        
    def step(self):
        if self.entrenando and not self.convergio and self.iteracion_actual < self.max_iteraciones:
            self.entrenar_epoca()
            self.iteracion_actual += 1
            
            # Guardar historial de pesos para visualización
            self.historial_pesos.append((self.peso1, self.peso2, self.sesgo))
            
            # Verificar convergencia
            if self.verificar_convergencia():
                self.convergio = True
                self.entrenando = False
                print(f" Perceptrón convergió en {self.iteracion_actual} iteraciones")
    
    def predecir(self, x1, x2):
        """Realizar predicción para un punto (x1, x2)"""
        suma_ponderada = self.peso1 * x1 + self.peso2 * x2 + self.sesgo
        return 1 if suma_ponderada >= 0 else -1
    
    def entrenar_epoca(self):
        """Entrenar por una época completa"""
        puntos_mal_clasificados = 0
        
        for punto in self.model.agentes_puntos:
            prediccion = self.predecir(punto.x, punto.y)
            error = punto.etiqueta_real - prediccion
            
            if error != 0:
                puntos_mal_clasificados += 1
                # Actualizar pesos y sesgo usando la regla del perceptrón
                self.peso1 += self.tasa_aprendizaje * error * punto.x
                self.peso2 += self.tasa_aprendizaje * error * punto.y
                self.sesgo += self.tasa_aprendizaje * error
        
        print(f"Iteración {self.iteracion_actual}: {puntos_mal_clasificados} errores")
    
    def verificar_convergencia(self):
        """Verificar si todos los puntos están clasificados correctamente"""
        for punto in self.model.agentes_puntos:
            if self.predecir(punto.x, punto.y) != punto.etiqueta_real:
                return False
        return True
    
    def obtener_linea_decision(self):
        """Obtener puntos para dibujar la línea de decisión"""
        if self.peso2 == 0:  # Evitar división por cero
            return [], []
        
        x_vals = np.array([-1, 1])
        y_vals = (-self.peso1 * x_vals - self.sesgo) / self.peso2
        return x_vals, y_vals
    
    def calcular_precision(self, puntos):
        """Calcular precisión en un conjunto de puntos"""
        correctos = 0
        for punto in puntos:
            if self.predecir(punto.x, punto.y) == punto.etiqueta_real:
                correctos += 1
        return correctos / len(puntos) * 100

class AgentePunto(mesa.Agent):
    def __init__(self, unique_id, model, x, y, etiqueta_real):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.etiqueta_real = etiqueta_real
        self.etiqueta_predicha = 0
        self.color = 'gray'  # Color inicial
    
    def actualizar_prediccion(self):
        """Actualizar predicción y color basado en el perceptrón actual"""
        perceptron = self.model.perceptron
        self.etiqueta_predicha = perceptron.predecir(self.x, self.y)
        
        # Actualizar color: verde si correcto, rojo si incorrecto
        if self.etiqueta_predicha == self.etiqueta_real:
            self.color = 'green'
        else:
            self.color = 'red'

class AgenteDatos(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pendiente_real = 0.5  # Pendiente de la línea de separación real
        self.intercepto_real = 0.2  # Intercepto de la línea real
    
    def generar_datos_entrenamiento(self, n_puntos=20):
        """Generar datos de entrenamiento linealmente separables"""
        agentes_puntos = []
        
        for i in range(n_puntos):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            # Determinar etiqueta real según la línea de separación
            if y > self.pendiente_real * x + self.intercepto_real:
                etiqueta_real = 1
            else:
                etiqueta_real = -1
            
            punto = AgentePunto(i, self.model, x, y, etiqueta_real)
            agentes_puntos.append(punto)
        
        return agentes_puntos
    
    def generar_datos_prueba(self, n_puntos=10):
        """Generar datos de prueba"""
        agentes_prueba = []
        
        for i in range(n_puntos):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            if y > self.pendiente_real * x + self.intercepto_real:
                etiqueta_real = 1
            else:
                etiqueta_real = -1
            
            punto = AgentePunto(100 + i, self.model, x, y, etiqueta_real)
            agentes_prueba.append(punto)
        
        return agentes_prueba

class ModeloPerceptron(mesa.Model):
    def __init__(self, n_puntos=20):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.n_puntos = n_puntos
        
        # Crear agentes
        self.perceptron = AgentePerceptron(0, self)
        self.schedule.add(self.perceptron)
        
        self.agente_datos = AgenteDatos(1, self)
        self.schedule.add(self.agente_datos)
        
        # Generar datos de entrenamiento
        self.agentes_puntos = self.agente_datos.generar_datos_entrenamiento(n_puntos)
        for punto in self.agentes_puntos:
            self.schedule.add(punto)
        
        # Configurar visualización
        self.fig, self.ax = None, None
        self.scatter = None
        self.linea_decision = None
        self.linea_real = None
        self.texto_info = None
        
    def step(self):
        self.schedule.step()
        # Actualizar predicciones de todos los puntos
        for punto in self.agentes_puntos:
            punto.actualizar_prediccion()
    
    def configurar_visualizacion(self):
        """Configurar la interfaz gráfica"""
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.3)
        
        # Configurar ejes
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Perceptrón - Clasificación de Puntos')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', alpha=0.3)
        self.ax.axvline(x=0, color='k', alpha=0.3)
        
        # Crear sliders
        ax_tasa_aprendizaje = plt.axes([0.2, 0.2, 0.6, 0.03])
        ax_iteraciones = plt.axes([0.2, 0.15, 0.6, 0.03])
        
        self.slider_tasa = Slider(
            ax_tasa_aprendizaje, 'Tasa de Aprendizaje', 0.01, 1.0, 
            valinit=0.1, valstep=0.01
        )
        self.slider_iteraciones = Slider(
            ax_iteraciones, 'Iteraciones Máximas', 10, 500, 
            valinit=100, valstep=10
        )
        
        # Crear botones
        ax_iniciar = plt.axes([0.3, 0.05, 0.15, 0.06])
        ax_reiniciar = plt.axes([0.55, 0.05, 0.15, 0.06])
        
        self.boton_iniciar = Button(ax_iniciar, 'Iniciar Entrenamiento')
        self.boton_reiniciar = Button(ax_reiniciar, 'Reiniciar')
        
        # Conectar eventos
        self.slider_tasa.on_changed(self.actualizar_tasa_aprendizaje)
        self.slider_iteraciones.on_changed(self.actualizar_max_iteraciones)
        self.boton_iniciar.on_clicked(self.iniciar_entrenamiento)
        self.boton_reiniciar.on_clicked(self.reiniciar_simulacion)
        
        self.dibujar_estado_inicial()
    
    def dibujar_estado_inicial(self):
        """Dibujar estado inicial"""
        self.ax.clear()
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Perceptrón - Clasificación de Puntos')
        self.ax.grid(True, alpha=0.3)
        
        # Dibujar puntos
        x_vals = [p.x for p in self.agentes_puntos]
        y_vals = [p.y for p in self.agentes_puntos]
        colores = [p.color for p in self.agentes_puntos]
        
        self.scatter = self.ax.scatter(x_vals, y_vals, c=colores, s=50, alpha=0.7)
        
        # Dibujar línea de separación real
        x_real = np.array([-1, 1])
        y_real = self.agente_datos.pendiente_real * x_real + self.agente_datos.intercepto_real
        self.linea_real, = self.ax.plot(x_real, y_real, 'b--', 
                                      label='Línea Real', alpha=0.7)
        
        # Dibujar línea de decisión actual
        x_decision, y_decision = self.perceptron.obtener_linea_decision()
        if len(x_decision) > 0:
            self.linea_decision, = self.ax.plot(x_decision, y_decision, 'r-', 
                                             linewidth=2, label='Línea de Decisión')
        
        # Información del estado
        precision = self.perceptron.calcular_precision(self.agentes_puntos)
        info_str = f"Iteración: {self.perceptron.iteracion_actual}\nPrecisión: {precision:.1f}%"
        self.texto_info = self.ax.text(0.02, 0.98, info_str, transform=self.ax.transAxes,
                                     verticalalignment='top', 
                                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        self.ax.legend()
        plt.draw()
    
    def actualizar_visualizacion(self):
        """Actualizar visualización"""
        # Actualizar colores de puntos
        colores = [p.color for p in self.agentes_puntos]
        self.scatter.set_color(colores)
        
        # Actualizar línea de decisión
        x_decision, y_decision = self.perceptron.obtener_linea_decision()
        if len(x_decision) > 0:
            self.linea_decision.set_data(x_decision, y_decision)
        
        # Actualizar información
        precision = self.perceptron.calcular_precision(self.agentes_puntos)
        info_str = f"Iteración: {self.perceptron.iteracion_actual}\nPrecisión: {precision:.1f}%"
        if self.perceptron.convergio:
            info_str += "\n CONVERGIDO!"
        self.texto_info.set_text(info_str)
        
        plt.draw()
    
    def actualizar_tasa_aprendizaje(self, valor):
        self.perceptron.tasa_aprendizaje = valor
    
    def actualizar_max_iteraciones(self, valor):
        self.perceptron.max_iteraciones = int(valor)
    
    def iniciar_entrenamiento(self, event):
        if not self.perceptron.entrenando:
            self.perceptron.entrenando = True
            self.perceptron.convergio = False
            print("Iniciando entrenamiento del perceptrón...")
            
            # Función para ejecutar pasos de entrenamiento
            def ejecutar_paso():
                if (self.perceptron.entrenando and 
                    not self.perceptron.convergio and 
                    self.perceptron.iteracion_actual < self.perceptron.max_iteraciones):
                    
                    self.step()
                    self.actualizar_visualizacion()
                    plt.pause(0.1)  # Pausa para visualización
                    ejecutar_paso()
                else:
                    # Evaluar con datos de prueba al finalizar
                    self.evaluar_perceptron()
            
            ejecutar_paso()
    
    def reiniciar_simulacion(self, event):
        """Reiniciar simulación"""
        # Reiniciar perceptrón
        self.perceptron.peso1 = random.uniform(-1, 1)
        self.perceptron.peso2 = random.uniform(-1, 1)
        self.perceptron.sesgo = random.uniform(-1, 1)
        self.perceptron.iteracion_actual = 0
        self.perceptron.entrenando = False
        self.perceptron.convergio = False
        self.perceptron.historial_pesos = []
        
        # Regenerar datos
        self.agentes_puntos = self.agente_datos.generar_datos_entrenamiento(self.n_puntos)
        
        # Actualizar predicciones iniciales
        for punto in self.agentes_puntos:
            punto.actualizar_prediccion()
        
        # Redibujar
        self.dibujar_estado_inicial()
        print("Simulación reiniciada")
    
    def evaluar_perceptron(self):
        """Evaluar el perceptrón con datos de prueba"""
        datos_prueba = self.agente_datos.generar_datos_prueba(10)
        precision_prueba = self.perceptron.calcular_precision(datos_prueba)
        
        print(f"\n EVALUACIÓN FINAL:")
        print(f"Precisión en entrenamiento: {self.perceptron.calcular_precision(self.agentes_puntos):.1f}%")
        print(f"Precisión en prueba: {precision_prueba:.1f}%")
        print(f"Pesos finales: w1={self.perceptron.peso1:.3f}, w2={self.perceptron.peso2:.3f}")
        print(f"Sesgo final: {self.perceptron.sesgo:.3f}")

# Función principal
def ejecutar_simulacion():
    modelo = ModeloPerceptron(n_puntos=30)
    modelo.configurar_visualizacion()
    plt.show()

if __name__ == "__main__":
    ejecutar_simulacion()