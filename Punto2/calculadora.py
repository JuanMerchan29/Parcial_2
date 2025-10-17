from mesa import Agent, Model
from mesa.time import BaseScheduler
import re
import uuid

# Agentes de Operación
class AgenteOperacion(Agent):
    def __init__(self, unique_id, model, operacion):
        super().__init__(unique_id, model)
        self.operacion = operacion
        self.bandeja_entrada = []
        
    def step(self):
        while self.bandeja_entrada:
            mensaje = self.bandeja_entrada.pop(0)
            if mensaje["tipo"] == "tarea":
                self.procesar_tarea(mensaje)
    
    def procesar_tarea(self, mensaje):
        a = mensaje["operando_izq"]
        b = mensaje["operando_der"]
        id_tarea = mensaje["id_tarea"]
        respuesta_a = mensaje["respuesta_a"]
        
        try:
            if self.operacion == "suma":
                resultado = a + b
            elif self.operacion == "resta":
                resultado = a - b
            elif self.operacion == "multiplicacion":
                resultado = a * b
            elif self.operacion == "division":
                if b == 0:
                    raise ZeroDivisionError("División por cero")
                resultado = a / b
            elif self.operacion == "potencia":
                resultado = a ** b
            
            # Enviar resultado
            mensaje_respuesta = {
                "tipo": "resultado",
                "id_tarea": id_tarea,
                "valor": resultado,
                "de": self.unique_id
            }
            self.model.enviar_mensaje(mensaje_respuesta, respuesta_a)
            
        except Exception as error:
            mensaje_error = {
                "tipo": "error",
                "id_tarea": id_tarea,
                "error": str(error),
                "de": self.unique_id
            }
            self.model.enviar_mensaje(mensaje_error, respuesta_a)

# Agente de Entrada/Salida
class AgenteES(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.bandeja_entrada = []
        self.tareas = {}
        self.tareas_pendientes = set()
        self.dependencias = {}
        self.id_tarea_raiz = None
        self.finalizado = False
        self.resultado_final = None
        
    def enviar_expresion(self, expresion):
        # Reiniciar estado
        self.tareas.clear()
        self.tareas_pendientes.clear()
        self.dependencias.clear()
        self.finalizado = False
        self.resultado_final = None
        
        # Parsear expresión
        tareas, id_raiz = self.parsear_expresion(expresion)
        self.tareas = tareas
        self.id_tarea_raiz = id_raiz
        self.tareas_pendientes = set(tareas.keys())
        
        # Establecer dependencias
        for id_tarea, tarea in tareas.items():
            for operando in [tarea["izquierda"], tarea["derecha"]]:
                if isinstance(operando, str) and operando in self.tareas:
                    self.dependencias.setdefault(operando, []).append(id_tarea)
        
        # Enviar tareas listas
        self.enviar_tareas_listas()
    
    def step(self):
        while self.bandeja_entrada:
            mensaje = self.bandeja_entrada.pop(0)
            
            if mensaje["tipo"] == "resultado":
                self.procesar_resultado(mensaje["id_tarea"], mensaje["valor"])
            elif mensaje["tipo"] == "error":
                self.resultado_final = f"ERROR: {mensaje['error']}"
                self.finalizado = True
                print(self.resultado_final)
    
    def procesar_resultado(self, id_tarea, valor):
        # Actualizar tareas dependientes
        for id_dependiente in self.dependencias.get(id_tarea, []):
            tarea = self.tareas[id_dependiente]
            if tarea["izquierda"] == id_tarea:
                tarea["izquierda"] = valor
            if tarea["derecha"] == id_tarea:
                tarea["derecha"] = valor
        
        # Verificar si es el resultado final
        if id_tarea == self.id_tarea_raiz:
            self.resultado_final = valor
            self.finalizado = True
            print(f"Resultado: {valor}")
            return
        
        # Marcar tarea como completada
        self.tareas_pendientes.discard(id_tarea)
        if id_tarea in self.dependencias:
            del self.dependencias[id_tarea]
        
        # Enviar nuevas tareas listas
        self.enviar_tareas_listas()
    
    def enviar_tareas_listas(self):
        tareas_listas = []
        
        for id_tarea in list(self.tareas_pendientes):
            tarea = self.tareas[id_tarea]
            
            # Tareas constantes se resuelven automáticamente
            if tarea["operacion"] == "constante":
                self.procesar_resultado(id_tarea, tarea["izquierda"])
                self.tareas_pendientes.discard(id_tarea)
                continue
            
            # Verificar si los operandos están listos
            if (isinstance(tarea["izquierda"], (int, float)) and 
                isinstance(tarea["derecha"], (int, float))):
                tareas_listas.append(id_tarea)
        
        # Enviar tareas a los agentes
        for id_tarea in tareas_listas:
            tarea = self.tareas[id_tarea]
            id_agente = self.obtener_id_agente(tarea["operacion"])
            
            if id_agente:
                mensaje = {
                    "tipo": "tarea",
                    "id_tarea": id_tarea,
                    "operando_izq": tarea["izquierda"],
                    "operando_der": tarea["derecha"],
                    "respuesta_a": self.unique_id
                }
                self.model.enviar_mensaje(mensaje, id_agente)
    
    def obtener_id_agente(self, operacion):
        mapeo = {
            "+": "agente_suma",
            "-": "agente_resta", 
            "*": "agente_multiplicacion",
            "/": "agente_division",
            "^": "agente_potencia"
        }
        return mapeo.get(operacion)
    
    def recibir_mensaje(self, mensaje):
        self.bandeja_entrada.append(mensaje)
    
    def parsear_expresion(self, expresion):
        tokens = self.tokenizar(expresion)
        rpn = self.convertir_rpn(tokens)
        return self.construir_tareas(rpn)
    
    def tokenizar(self, expresion):
        expresion_limpia = expresion.replace(" ", "")
        return re.findall(r'(\d+\.?\d*|[+\-*/^()])', expresion_limpia)
    
    def convertir_rpn(self, tokens):
        salida = []
        pila = []
        precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        
        for token in tokens:
            if re.match(r'\d+\.?\d*', token):
                salida.append(token)
            elif token in precedencia:
                while (pila and pila[-1] in precedencia and 
                       precedencia[pila[-1]] >= precedencia[token]):
                    salida.append(pila.pop())
                pila.append(token)
            elif token == '(':
                pila.append(token)
            elif token == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                pila.pop()
        
        while pila:
            salida.append(pila.pop())
        
        return salida
    
    def construir_tareas(self, rpn):
        pila = []
        tareas = {}
        
        for token in rpn:
            if re.match(r'\d+\.?\d*', token):
                valor = float(token) if '.' in token else int(token)
                pila.append(valor)
            else:
                derecha = pila.pop()
                izquierda = pila.pop()
                id_tarea = f"tarea_{uuid.uuid4().hex[:8]}"
                
                tareas[id_tarea] = {
                    "operacion": token,
                    "izquierda": izquierda,
                    "derecha": derecha
                }
                pila.append(id_tarea)
        
        # Manejar caso de expresión simple (un solo número)
        if isinstance(pila[0], (int, float)):
            id_tarea = f"constante_{uuid.uuid4().hex[:6]}"
            tareas[id_tarea] = {
                "operacion": "constante", 
                "izquierda": pila[0],
                "derecha": 0
            }
            return tareas, id_tarea
        
        return tareas, pila[0]

# Modelo Principal
class ModeloCalculadora(Model):
    def __init__(self):
        super().__init__()
        self.schedule = BaseScheduler(self)
        self.agentes = {}
        self.mensajes_pendientes = []
        
        # Crear agentes de operación
        operaciones = [
            ("agente_suma", "suma"),
            ("agente_resta", "resta"), 
            ("agente_multiplicacion", "multiplicacion"),
            ("agente_division", "division"),
            ("agente_potencia", "potencia")
        ]
        
        for id_agente, operacion in operaciones:
            agente = AgenteOperacion(id_agente, self, operacion)
            self.agentes[id_agente] = agente
            self.schedule.add(agente)
        
        # Crear agente E/S
        agente_es = AgenteES("agente_es", self)
        self.agente_es = agente_es
        self.agentes["agente_es"] = agente_es
        self.schedule.add(agente_es)
    
    def enviar_mensaje(self, mensaje, destinatario_id):
        self.mensajes_pendientes.append((destinatario_id, mensaje))
    
    def entregar_mensajes(self):
        for destinatario_id, mensaje in self.mensajes_pendientes:
            if destinatario_id in self.agentes:
                agente = self.agentes[destinatario_id]
                if isinstance(agente, AgenteES):
                    agente.recibir_mensaje(mensaje)
                else:
                    agente.bandeja_entrada.append(mensaje)
        
        self.mensajes_pendientes.clear()
    
    def step(self):
        self.entregar_mensajes()
        self.schedule.step()
        self.entregar_mensajes()

# Función de ejecución
def ejecutar_expresion(expresion, max_pasos=100):
    modelo = ModeloCalculadora()
    agente_es = modelo.agente_es
    agente_es.enviar_expresion(expresion)
    
    pasos = 0
    while not agente_es.finalizado and pasos < max_pasos:
        modelo.step()
        pasos += 1
    
    return agente_es.resultado_final

# Interfaz interactiva
def interfaz_calculadora():
    print("Calculadora Basada en Agentes - MESA")
    print("Operaciones: + - * / ^")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        try:
            expresion = input("Expresión: ").strip()
            if expresion.lower() in ['salir', 'exit']:
                break
            if not expresion:
                continue
            
            resultado = ejecutar_expresion(expresion)
            if resultado:
                print(f"= {resultado}\n")
            else:
                print("Error: No se pudo calcular la expresión\n")
                
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    interfaz_calculadora()