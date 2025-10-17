class CalculadoraCientifica : Calculadora() {
    var anguloModo: AnguloModo = AnguloModo.GRADOS
    
    // Conversión de ángulos
    private fun aRadianes(grados: Double): Double {
        return grados * Math.PI / 180.0
    }
    
    private fun aGrados(radianes: Double): Double {
        return radianes * 180.0 / Math.PI
    }
    
    private fun convertirAngulo(angulo: Double): Double {
        return when (anguloModo) {
            AnguloModo.GRADOS -> aRadianes(angulo)
            AnguloModo.RADIANES -> angulo
        }
    }
    
    // Funciones trigonométricas
    fun seno(angulo: Double): Double {
        val radianes = convertirAngulo(angulo)
        val resultado = Math.sin(radianes)
        historial.add("sin($angulo ${if (anguloModo == AnguloModo.GRADOS) "°" else "rad"}) = $resultado")
        return resultado
    }
    
    fun coseno(angulo: Double): Double {
        val radianes = convertirAngulo(angulo)
        val resultado = Math.cos(radianes)
        historial.add("cos($angulo ${if (anguloModo == AnguloModo.GRADOS) "°" else "rad"}) = $resultado")
        return resultado
    }
    
    fun tangente(angulo: Double): Double {
        val radianes = convertirAngulo(angulo)
        if (Math.cos(radianes) == 0.0) {
            throw CalculadoraException("Error: Tangente indefinida para este ángulo")
        }
        val resultado = Math.tan(radianes)
        historial.add("tan($angulo ${if (anguloModo == AnguloModo.GRADOS) "°" else "rad"}) = $resultado")
        return resultado
    }
    
    // Funciones trigonométricas inversas
    fun arcoseno(valor: Double): Double {
        if (valor < -1.0 || valor > 1.0) {
            throw CalculadoraException("Error: Valor fuera del dominio [-1, 1] para arcoseno")
        }
        val resultadoRadianes = Math.asin(valor)
        val resultado = when (anguloModo) {
            AnguloModo.GRADOS -> aGrados(resultadoRadianes)
            AnguloModo.RADIANES -> resultadoRadianes
        }
        historial.add("asin($valor) = $resultado ${if (anguloModo == AnguloModo.GRADOS) "°" else "rad"}")
        return resultado
    }
    
    fun arcocoseno(valor: Double): Double {
        if (valor < -1.0 || valor > 1.0) {
            throw CalculadoraException("Error: Valor fuera del dominio [-1, 1] para arcocoseno")
        }
        val resultadoRadianes = Math.acos(valor)
        val resultado = when (anguloModo) {
            AnguloModo.GRADOS -> aGrados(resultadoRadianes)
            AnguloModo.RADIANES -> resultadoRadianes
        }
        historial.add("acos($valor) = $resultado ${if (anguloModo == AnguloModo.GRADOS) "°" else "rad"}")
        return resultado
    }
    
    fun arcotangente(valor: Double): Double {
        val resultadoRadianes = Math.atan(valor)
        val resultado = when (anguloModo) {
            AnguloModo.GRADOS -> aGrados(resultadoRadianes)
            AnguloModo.RADIANES -> resultadoRadianes
        }
        historial.add("atan($valor) = $resultado ${if (anguloModo == AnguloModo.GRADOS) "°" else "rad"}")
        return resultado
    }
    
    // Potencias y raíces
    fun potencia(base: Double, exponente: Double): Double {
        val resultado = Math.pow(base, exponente)
        historial.add("$base ^ $exponente = $resultado")
        return resultado
    }
    
    fun raizCuadrada(valor: Double): Double {
        if (valor < 0) {
            throw CalculadoraException("Error: No se puede calcular raíz cuadrada de número negativo")
        }
        val resultado = Math.sqrt(valor)
        historial.add("√$valor = $resultado")
        return resultado
    }
    
    fun raizNesima(indice: Double, radicando: Double): Double {
        if (radicando < 0 && indice % 2 == 0.0) {
            throw CalculadoraException("Error: No se puede calcular raíz par de número negativo")
        }
        val resultado = Math.pow(radicando, 1.0 / indice)
        historial.add("${indice}√$radicando = $resultado")
        return resultado
    }
    
    // Logaritmos
    fun logaritmoNatural(valor: Double): Double {
        if (valor <= 0) {
            throw CalculadoraException("Error: Logaritmo natural definido solo para valores positivos")
        }
        val resultado = Math.log(valor)
        historial.add("ln($valor) = $resultado")
        return resultado
    }
    
    fun logaritmoBase10(valor: Double): Double {
        if (valor <= 0) {
            throw CalculadoraException("Error: Logaritmo base 10 definido solo para valores positivos")
        }
        val resultado = Math.log10(valor)
        historial.add("log10($valor) = $resultado")
        return resultado
    }
    
    fun logaritmoBaseN(base: Double, valor: Double): Double {
        if (valor <= 0 || base <= 0 || base == 1.0) {
            throw CalculadoraException("Error: Base y valor deben ser positivos, base ≠ 1")
        }
        val resultado = Math.log(valor) / Math.log(base)
        historial.add("log$base($valor) = $resultado")
        return resultado
    }
    
    // Exponencial
    fun exponencial(valor: Double): Double {
        val resultado = Math.exp(valor)
        historial.add("e^$valor = $resultado")
        return resultado
    }
    
    // Factorial
    fun factorial(n: Int): Long {
        if (n < 0) {
            throw CalculadoraException("Error: Factorial definido solo para números enteros no negativos")
        }
        if (n > 20) {
            throw CalculadoraException("Error: Número demasiado grande para factorial")
        }
        var resultado: Long = 1
        for (i in 1..n) {
            resultado *= i
        }
        historial.add("$n! = $resultado")
        return resultado
    }
    
    // Valor absoluto
    fun valorAbsoluto(valor: Double): Double {
        val resultado = Math.abs(valor)
        historial.add("|$valor| = $resultado")
        return resultado
    }
    
    // Redondeo
    fun redondear(valor: Double, decimales: Int = 0): Double {
        val factor = Math.pow(10.0, decimales.toDouble())
        val resultado = Math.round(valor * factor) / factor
        historial.add("round($valor, $decimales) = $resultado")
        return resultado
    }
}