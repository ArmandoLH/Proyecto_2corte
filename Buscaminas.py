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
        
class Tablero:    #Es la clase con la que representaremos el tablero 
    def __init__(self, filas, columnas, num_minas): #Le vamos a definir las filas, columnas y las minas
        self._filas = filas
        self._columnas = columnas
        self._num_minas = num_minas
        self._grid = [[Casilla() for _ in range(columnas)] for _ in range(filas)] #Con este vamos a creaar una matriz que representa el tablero
        self._colocar_minas()  #se colocaran las minas en el tablero

    def _colocar_minas(self):   #Para colocar minas en el tablero
        minas_colocadas = 0       #Aqui el numero de minas es 0 porque apenas se van a colocar
        while minas_colocadas < self._num_minas:  #Un ciclo while para poner las minas sin poner de mas
            fila = random.randint(0, self._filas-1)
            columna = random.randint(0, self._columnas-1)
            if self._grid[fila][columna]._valor != -1: #Se ocupa para saber si hay una mina colocada en el lugar elegido
                self._grid[fila][columna]._valor = -1
                minas_colocadas += 1
                self._incrementar_contadores(fila, columna)

    def _incrementar_contadores(self, fila, columna): #Se va a utilizar para incrementar el contador de las casillas que esten a los lados de las minas
        for f in range(fila-1, fila+2):   #Se hace un bucle para recorrer las casillas de los lados de la casilla actual
            for c in range(columna-1, columna+2):
                if (0 <= f < self._filas and 0 <= c < self._columnas and 
                    self._grid[f][c]._valor != -1): #Lo usamos para verificar si todavia estamos en el tablero y para saber si hay una mina
                    self._grid[f][c]._valor += 1  #Se incrementa el valor de las casillas +1
