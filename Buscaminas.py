import random   #Proporciona una funcion para generar numeros aleatorios.

class Casilla:  #Es la clase que vamos a ocupar para representar una casilla en el juego
    def __init__(self, valor=0, revelado=False):
        self._valor = valor  #Representa el numero de minas a los lados de esta 
        self._revelado = revelado  #Para saber si la casilla se revvelo o nel

    def __str__(self):  #va a representar la casilla como una cadena cuando se use la funcion str
        if self._revelado:       #Es para saber si el valor ya se revelo y sino sigue apareciendo X en la casilla
            return str(self._valor)
        else:
            return "X"
