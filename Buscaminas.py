import random   #Proporciona una funcion para generar numeros aleatorios.
import openai
import requests
import json

openai.api_base = "https://api.openai.com/v1/chat/completions" 
openai.api_key = "Aqui va la Api_key"


class Casilla:  #Es la clase que vamos a ocupar para representar una casilla en el juego
    def __init__(self, valor=0, revelado=False):
        self._valor = valor  #Representa el numero de minas a los lados de esta 
        self._revelado = revelado  #Para saber si la casilla se revelo o nel

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
        self._grid = [[Casilla() for _ in range(columnas)] for _ in range(filas)] #Con este vamos a crear una matriz que representa el tablero
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

    def __str__(self):  #va a representar la casilla como una cadena cuando se use la funcion str
            return '\n'.join([' '.join([str(casilla) for casilla in fila]) for fila in self._grid]) #Lo ocupamos para representar el tablero como una cadena de texto y hay saltos de linea

    def revelar_casilla(self, fila, columna):  #Lo vamos a ocupar para revelar las casillas en el tablero
        if not (0 <= fila < self._filas) or not (0 <= columna < self._columnas): #Para que no nos salgamos del tablero
            print("Coordenadas fuera del tablero.")
            return
        if self._grid[fila][columna]._revelado:  #Lo vamos a ocupar para que nos indique si la casilla que elegimos ya esta revelada
            print("Esta casilla ya ha sido revelada.")
            return
        self._grid[fila][columna]._revelado = True #Se marca laa casilla como revelada
        if self._grid[fila][columna]._valor == 0:  #Se usa para que en caso de que la casilla no tenga minas se revelen laas casillas de los lados
            self._revelar_vecinos(fila, columna)

    def _revelar_vecinos(self, fila, columna):  #Lo ocupamos para revelar las casillas de los lados de una casilla dada
        for f in range(fila-1, fila+2):   #Se hace un bucle para recorrer las casillas de los lados de la casilla actual
            for c in range(columna-1, columna+2):
                if (0 <= f < self._filas and 0 <= c < self._columnas and 
                    not self._grid[f][c]._revelado):   #Lo vamos a usar para saber si la casilla seleccionada esta dentro del tablero y si no ah sido revelada pues se revela
                    self._grid[f][c]._revelado = True
                    if self._grid[f][c]._valor == 0:  #Si el valor de la casilla es 0 se revelan las casillas de los lados
                        self._revelar_vecinos(f, c)
                        
class Juego:     #Es la clase que representa el juego de buscaminas
    def __init__(self, filas=8, columnas=8, num_minas=10):   #Aqui definimos las dimensiones del tablero y el numero de minas
        self._tablero = Tablero(filas, columnas, num_minas)
        
    def _generar_mensaje_motivacional(self, ganador):
        prompt = "Tu " + ("ganaste" if ganador else "perder") + " el juego. Genera un mensaje motivacional."
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer quite mi api_key de aqui porque es privada"  # Aqui va la api_key"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 50
        }
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        print(response_data)  # Imprimir la respuesta completa para análisis
        return response_data["choices"][0]["message"]["content"].strip()
    
    def jugar(self):
        while True:
            print(self._tablero)
            fila, columna = map(int, input("Introduce la fila y columna separadas por espacio: ").split())
            self._tablero.revelar_casilla(fila, columna)

            if self._ha_perdido():
                print("Parece que te haz topado con una mina, que mala suerte")
                print("¡Has perdido!")
                mensaje_motivacional = self._generar_mensaje_motivacional(ganador=False)
                print("Mensaje motivacional:", mensaje_motivacional)
                input("Presiona Enter para salir del programa.")
                break
            elif self._ha_ganado():
                print("¡Felicidades! Has ganado.")
                mensaje_motivacional = self._generar_mensaje_motivacional(ganador=True)
                print("Mensaje motivacional:", mensaje_motivacional)
                input("Presiona Enter para salir del programa.")
                break
    def _ha_perdido(self):  #Lo creamos para saber si perdimos 
        for fila in self._tablero._grid:
            for casilla in fila:
                if casilla._revelado and casilla._valor == -1:
                    return True
        return False

    def _ha_ganado(self):  #Lo creamos paara saber si ganamos
        for fila in self._tablero._grid:
            for casilla in fila:
                if not casilla._revelado and casilla._valor != -1:
                    return False
        return True

if __name__ == "__main__":   #Lo vamos a ocupar para iniciar el juego
    print("Bienvenido al juego del ¡Buscaminas!")
    print("El terreno esta dividido en 8 filas y 8 columnas")
    print("Para acceder a ellas recuerda que la primera casilla se representa con 0 0 y la ultima con 7 7")
    print("Hay 10 minas en el terreno de juego, trata de evitarlas y ganaras, ¡Buena suerte!")
    juego = Juego()
    juego.jugar()                        
