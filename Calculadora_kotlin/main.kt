class CalculadoraConsola {
    private val calculadora = CalculadoraCientifica()
    private val parser = ExpressionParser(calculadora)
    
    fun iniciar() {
        println("calculadora científica")
        println("Comandos especiales:")
        println("  'mem' - Mostrar memoria")
        println("  'hist' - Mostrar historial")
        println("  'clear' - Limpiar todo")
        println("  'modo' - Cambiar modo de ángulos")
        println("  'exit' - Salir")
        println("Modo actual: ${calculadora.anguloModo}")
        println()
        
        while (true) {
            print(">>> ")
            val input = readLine()?.trim() ?: continue
            
            when (input.lowercase()) {
                "exit" -> break
                "mem" -> mostrarMemoria()
                "hist" -> mostrarHistorial()
                "clear" -> limpiarTodo()
                "modo" -> cambiarModoAngulo()
                else -> procesarExpresion(input)
            }
        }
    }
    
    private fun procesarExpresion(expresion: String) {
        try {
            when {
                expresion.contains("=") -> procesarAsignacionMemoria(expresion)
                expresion.startsWith("M+") -> procesarSumaMemoria(expresion)
                expresion.startsWith("M-") -> procesarRestaMemoria(expresion)
                else -> evaluarYMostrar(expresion)
            }
        } catch (e: CalculadoraException) {
            println(" ${e.message}")
        } catch (e: Exception) {
            println("Error: ${e.message}")
        }
    }
    
    private fun evaluarYMostrar(expresion: String) {
        val resultado = parser.evaluarExpresion(expresion)
        println("= $resultado")
    }
    
    private fun procesarAsignacionMemoria(expresion: String) {
        val partes = expresion.split("=")
        if (partes.size == 2) {
            val valor = parser.evaluarExpresion(partes[1].trim())
            calculadora.guardarEnMemoria(valor)
            println("Memoria establecida: $valor")
        }
    }
    
    private fun procesarSumaMemoria(expresion: String) {
        val valorStr = expresion.substring(2).trim()
        val valor = if (valorStr.isEmpty()) {
            calculadora.obtenerMemoria()
        } else {
            parser.evaluarExpresion(valorStr)
        }
        calculadora.sumarMemoria(valor)
        println("Memoria + $valor = ${calculadora.obtenerMemoria()}")
    }
    
    private fun procesarRestaMemoria(expresion: String) {
        val valorStr = expresion.substring(2).trim()
        val valor = if (valorStr.isEmpty()) {
            calculadora.obtenerMemoria()
        } else {
            parser.evaluarExpresion(valorStr)
        }
        calculadora.restarMemoria(valor)
        println("Memoria - $valor = ${calculadora.obtenerMemoria()}")
    }
    
    private fun mostrarMemoria() {
        println("Memoria: ${calculadora.obtenerMemoria()}")
    }
    
    private fun mostrarHistorial() {
        val historial = calculadora.obtenerHistorial()
        if (historial.isEmpty()) {
            println("Historial vacío")
        } else {
            println("=== HISTORIAL ===")
            historial.forEachIndexed { index, operacion ->
                println("${index + 1}. $operacion")
            }
        }
    }
    
    private fun limpiarTodo() {
        calculadora.limpiarTodo()
        println(" Todo limpiado")
    }
    
    private fun cambiarModoAngulo() {
        calculadora.anguloModo = when (calculadora.anguloModo) {
            AnguloModo.GRADOS -> AnguloModo.RADIANES
            AnguloModo.RADIANES -> AnguloModo.GRADOS
        }
        println("Modo de ángulos cambiado a: ${calculadora.anguloModo}")
    }
}

fun main() {
    val calculadoraUI = CalculadoraConsola()
    calculadoraUI.iniciar()
}
}