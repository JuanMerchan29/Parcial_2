open class Calculadora {
    protected var memoria: Double = 0.0
    protected val historial: MutableList<String> = mutableListOf()
    
    // Operaciones básicas
    open fun sumar(a: Double, b: Double): Double {
        val resultado = a + b
        historial.add("$a + $b = $resultado")
        return resultado
    }
    
    open fun sumar(a: Int, b: Int): Int {
        val resultado = a + b
        historial.add("$a + $b = $resultado")
        return resultado
    }
    
    open fun restar(a: Double, b: Double): Double {
        val resultado = a - b
        historial.add("$a - $b = $resultado")
        return resultado
    }
    
    open fun restar(a: Int, b: Int): Int {
        val resultado = a - b
        historial.add("$a - $b = $resultado")
        return resultado
    }
    
    open fun multiplicar(a: Double, b: Double): Double {
        val resultado = a * b
        historial.add("$a × $b = $resultado")
        return resultado
    }
    
    open fun multiplicar(a: Int, b: Int): Int {
        val resultado = a * b
        historial.add("$a × $b = $resultado")
        return resultado
    }
    
    open fun dividir(a: Double, b: Double): Double {
        if (b == 0.0) {
            throw CalculadoraException("Error: División por cero")
        }
        val resultado = a / b
        historial.add("$a ÷ $b = $resultado")
        return resultado
    }
    
    open fun dividir(a: Int, b: Int): Double {
        if (b == 0) {
            throw CalculadoraException("Error: División por cero")
        }
        val resultado = a.toDouble() / b.toDouble()
        historial.add("$a ÷ $b = $resultado")
        return resultado
    }
    
    // Funciones de memoria
    open fun guardarEnMemoria(valor: Double) {
        memoria = valor
        historial.add("Memoria establecida: $valor")
    }
    
    open fun obtenerMemoria(): Double {
        return memoria
    }
    
    open fun limpiarMemoria() {
        memoria = 0.0
        historial.add("Memoria limpiada")
    }
    
    open fun sumarMemoria(valor: Double) {
        memoria += valor
        historial.add("Memoria + $valor = $memoria")
    }
    
    open fun restarMemoria(valor: Double) {
        memoria -= valor
        historial.add("Memoria - $valor = $memoria")
    }
    
    // Historial
    open fun obtenerHistorial(): List<String> {
        return historial.toList()
    }
    
    open fun limpiarHistorial() {
        historial.clear()
    }
    
    open fun limpiarTodo() {
        memoria = 0.0
        historial.clear()
    }
}