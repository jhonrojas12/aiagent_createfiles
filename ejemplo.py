#!/usr/bin/env python3
"""
Archivo ejemplo.py: funciones sumar, restar y multiplicar con main para CLI.
"""

# Este módulo proporciona una pequeña calculadora de tres operaciones:
# - sumar: a + b
# - restar: a - b
# - multiplicar: a * b
# y una interfaz de linea de comandos (CLI) a través de main().
# Mantiene las mismas funciones y comportamiento que la versión anterior.

def sumar(a, b):
    """Devuelve la suma de a y b."""
    return a + b


def restar(a, b):
    """Devuelve la resta de b a partir de a (a - b)."""
    return a - b


def multiplicar(a, b):
    """Devuelve el producto de a y b (a * b)."""
    return a * b


def main():
    """Punto de entrada cuando se ejecuta el script desde la CLI."""
    import sys
    # Verificar que se pasen exactamente 3 argumentos: operacion, a y b
    if len(sys.argv) != 4:
        print("Uso: python ejemplo.py <operacion> <a> <b>")
        print("Operaciones: sumar, restar, multiplicar")
        return

    operacion = sys.argv[1]
    try:
        a = float(sys.argv[2])
        b = float(sys.argv[3])
    except ValueError:
        print("Error: a y b deben ser números.")
        return

    if operacion == "sumar":
        resultado = sumar(a, b)
    elif operacion == "restar":
        resultado = restar(a, b)
    elif operacion == "multiplicar":
        resultado = multiplicar(a, b)
    else:
        print("Operación no reconocida. Usa sumar, restar o multiplicar.")
        return
    print("Resultado:", resultado)


if __name__ == "__main__":
    main()
