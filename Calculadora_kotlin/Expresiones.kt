class ExpressionParser(private val calculadora: CalculadoraCientifica) {
    
    fun evaluarExpresion(expresion: String): Double {
        val tokens = tokenizar(expresion)
        return evaluarTokens(tokens)
    }
    
    private fun tokenizar(expresion: String): List<String> {
        val regex = Regex("(?:(?<=[+\\-*/^()])|(?=[+\\-*/^()]))|\\s+")
        return expresion.split(regex)
            .filter { it.isNotBlank() }
            .map { it.trim() }
    }
    
    private fun evaluarTokens(tokens: List<String>): Double {
        val pilaNumeros = mutableListOf<Double>()
        val pilaOperadores = mutableListOf<String>()
        
        for (token in tokens) {
            when {
                token.matches(Regex("-?\\d+(\\.\\d+)?")) -> {
                    pilaNumeros.add(token.toDouble())
                }
                token in listOf("+", "-", "*", "/", "^") -> {
                    while (pilaOperadores.isNotEmpty() && precedencia(pilaOperadores.last()) >= precedencia(token)) {
                        aplicarOperador(pilaOperadores.removeAt(pilaOperadores.size - 1), pilaNumeros)
                    }
                    pilaOperadores.add(token)
                }
                token == "(" -> {
                    pilaOperadores.add(token)
                }
                token == ")" -> {
                    while (pilaOperadores.isNotEmpty() && pilaOperadores.last() != "(") {
                        aplicarOperador(pilaOperadores.removeAt(pilaOperadores.size - 1), pilaNumeros)
                    }
                    pilaOperadores.removeAt(pilaOperadores.size - 1) // Remover "("
                }
                else -> {
                    // Es una función
                    pilaOperadores.add(token)
                }
            }
        }
        
        while (pilaOperadores.isNotEmpty()) {
            aplicarOperador(pilaOperadores.removeAt(pilaOperadores.size - 1), pilaNumeros)
        }
        
        return pilaNumeros.single()
    }
    
    private fun precedencia(operador: String): Int {
        return when (operador) {
            "+", "-" -> 1
            "*", "/" -> 2
            "^" -> 3
            in listOf("sin", "cos", "tan", "log", "ln", "sqrt", "exp") -> 4
            else -> 0
        }
    }
    
    private fun aplicarOperador(operador: String, pilaNumeros: MutableList<Double>) {
        when (operador) {
            "+" -> {
                val b = pilaNumeros.removeAt(pilaNumeros.size - 1)
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.sumar(a, b))
            }
            "-" -> {
                val b = pilaNumeros.removeAt(pilaNumeros.size - 1)
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.restar(a, b))
            }
            "*" -> {
                val b = pilaNumeros.removeAt(pilaNumeros.size - 1)
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.multiplicar(a, b))
            }
            "/" -> {
                val b = pilaNumeros.removeAt(pilaNumeros.size - 1)
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.dividir(a, b))
            }
            "^" -> {
                val b = pilaNumeros.removeAt(pilaNumeros.size - 1)
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.potencia(a, b))
            }
            "sin" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.seno(a))
            }
            "cos" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.coseno(a))
            }
            "tan" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.tangente(a))
            }
            "log" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.logaritmoBase10(a))
            }
            "ln" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.logaritmoNatural(a))
            }
            "sqrt" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.raizCuadrada(a))
            }
            "exp" -> {
                val a = pilaNumeros.removeAt(pilaNumeros.size - 1)
                pilaNumeros.add(calculadora.exponencial(a))
            }
        }
    }
}