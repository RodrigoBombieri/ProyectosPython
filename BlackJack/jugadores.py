"""
Este módulo define las clases de jugadores utilizadas en un juego de cartas tipo BlackJack.
Incluye clases abstractas y concretas que modelan jugadores humanos, de computadora,
croupier, y la lógica asociada a las apuestas y decisiones durante el juego.
"""

from abc import ABC, abstractmethod
from random import shuffle
from cartas import Carta, CartaPoker, CartaEspanola
from mazos import Mazo, MazoBlackJack, MazoEspanolas, MazoSieteYMedio
from txtcolores import strclr

# --- Clases de Jugadores ---

class JugadorCartas(ABC):
    """
    Clase abstracta que representa un jugador genérico con una mano de cartas.
    Es la base para todos los tipos de jugadores.
    """

    def __init__(self, nombre: str, mano: Mazo) -> None:
        self.__nombre = nombre      # Nombre identificatorio del jugador
        self.__mano = mano      # Mano del jugador, representada como un mazo

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__nombre

    @property
    def mano(self) -> Mazo:
        """Devuelve el mazo que representa la mano del jugador."""
        return self.__mano

    def poner(self, carta: Carta, index: int = -1) -> None:
        """
        Agrega una carta a la mano del jugador.
        :param carta: Objeto carta a agregar
        :param index: Posición en la mano (-1 al final por defecto)
        """
        self.__mano.poner(carta, index)

    def sacar(self, index: int = 0) -> Carta:
        """
        Extrae una carta de la mano del jugador.
        :param index: Índice de la carta a extraer
        :return: Carta extraída
        """
        return self.__mano.sacar(index)

    def tiene_cartas(self) -> bool:
        """Devuelve True si el jugador tiene cartas en la mano."""
        return not self.__mano.isvacio()

    def __str__(self) -> str:
        return f"{self.nombre} ==> {self.mano}"


class JugadorBlackjack(JugadorCartas):
    """
    Clase abstracta intermedia que representa un jugador de BlackJack.
    Agrega comportamiento específico como suma de mano y decisión de plantarse.
    """

    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, MazoBlackJack())
        self.__color = 15  # Color predeterminado en terminal (blanco)

    @property
    def color(self) -> int:
        return self.__color

    @color.setter
    def color(self, valor: int) -> None:
        self.__color = valor

    def poner(self, carta: CartaPoker, index: int = -1) -> None:
        self.mano.poner(carta, index)

    def sacar(self, index: int = 0) -> CartaPoker:
        return self.mano.sacar(index)

    def tiene_blackjack(self) -> bool:
        """Devuelve True si la mano es un BlackJack: 2 cartas que suman 21."""
        return len(self.mano) == 2 and self.mano.suma() == 21

    @property
    def mano(self) -> MazoBlackJack:
        return super().mano

    @abstractmethod
    def se_planta(self) -> bool:
        """Define si el jugador decide plantarse."""
        pass


class Croupier(JugadorBlackjack):
    """
    Clase concreta que representa al croupier o banca del casino.
    Tiene una lógica automática para decidir cuándo plantarse.
    """

    def __init__(self) -> None:
        super().__init__('Sr Croupier')
        self.color = 154  # Verde claro

    def se_planta(self) -> bool:
        suma = self.mano.suma()
        print(f"{self} ({suma})")
        if suma >= 21:
            return True
        if suma >= 17:
            print("Se planta [automático]")
            return True
        return False

    def __str__(self) -> str:
        return f"{strclr(self.nombre, self.color)} ==> {self.mano}"


class Cliente(JugadorBlackjack):
    """
    Clase abstracta que representa a un cliente del casino.
    Administra el sistema de fichas y apuestas.
    """

    colores = [10, 11, 12, 13, 14, 32, 125, 175, 201]  # Paleta de colores para diferenciar jugadores

    def __init__(self, nombre: str, fichas: int) -> None:
        super().__init__(nombre)
        self.__fichas = fichas
        shuffle(Cliente.colores)
        self.color = Cliente.colores.pop(0)

    @property
    def fichas(self) -> int:
        return self.__fichas

    def ganar_fichas(self, cantidad: int) -> None:
        """Suma fichas al jugador."""
        self.__fichas += cantidad

    def perder_fichas(self, cantidad: int) -> None:
        """Resta fichas al jugador."""
        self.__fichas -= cantidad

    @abstractmethod
    def apostar(self) -> int:
        """
        Método abstracto para definir cuánto apuesta el jugador.
        :return: Cantidad de fichas apostadas
        """
        pass

    def __str__(self) -> str:
        return f"{strclr(self.nombre, self.color)} ==> {self.mano} $[{self.fichas}] ({self.mano.suma()})"


class JugadorHumano(Cliente):
    """
    Clase concreta que representa a un jugador humano.
    Interactúa mediante entrada por teclado.
    """

    def __init__(self, nombre: str, fichas: int) -> None:
        super().__init__(nombre, fichas)

    def se_planta(self) -> bool:
        print(str(self))
        if self.mano.suma() >= 21:
            return True
        return input("¿Se planta? [S/N]: ").strip().upper() == 'S'

    def apostar(self) -> int:
        while True:
            try:
                apuesta = int(input(f"{self.nombre}, ingrese apuesta (tiene {self.fichas} fichas): "))
                if 1 <= apuesta <= self.fichas:
                    return apuesta
                print("Apuesta inválida. Debe ser mayor que 0 y menor o igual a sus fichas.")
            except ValueError:
                print("Por favor, ingrese un número entero válido.")


class JugadorComputadora(Cliente):
    """
    Clase concreta que representa a un jugador automático controlado por la computadora.
    """

    def __init__(self, nombre: str, fichas: int) -> None:
        super().__init__(nombre, fichas)

    def se_planta(self) -> bool:
        return self.mano.suma() >= 17

    def apostar(self) -> int:
        """
        Estrategia automática simple:
        Apuesta el 10% de sus fichas (al menos 1 ficha).
        """
        return max(1, self.fichas // 10)




class JugadorSieteYMedio(JugadorCartas):
    """
    Clase abstracta intermedia que representa un jugador de Siete y Medio.
    Agrega comportamiento específico como suma de mano y decisión de plantarse
    """
    def __init__(self, nombre:str)-> None:
        super().__init__(nombre, MazoSieteYMedio())
        self.__color = 15 # Color predeterminado en terminal (Blanco)
    
    @property
    def color(self)-> int:
        return self.__color
    
    @color.setter
    def color(self, valor:int)-> None:
        self.__color = valor
    
    def poner(self, carta:CartaEspanola, index:int = -1)-> None:
        self.mano.poner(carta, index)

    def sacar(self, index:int = 0)-> CartaEspanola:
        return self.mano.sacar(index)
    
    def tiene_siete_y_medio_real(self)-> bool:
        """
        Devuelve True si la mano es es Siete y Medio real: 
        Suma 7.5 y se forma con un siete y una figura del mismo palo.
        """
        if len(self.mano) != 2:
            return False

        it = iter(self.mano)
        c1 = next(it)
        c2 = next(it)

        es_7_c1 = c1.numero == 7
        es_figura_c2 = c2.numero in (10, 11, 12)
        mismo_palo = c1.palo == c2.palo

        es_7_c2 = c2.numero == 7
        es_figura_c1 = c1.numero in (10, 11, 12)

        return ((es_7_c1 and es_figura_c2) or (es_7_c2 and es_figura_c1)) and mismo_palo and self.mano.suma() == 7.5

    def tiene_siete_y_medio(self)-> bool:
        """
        Devuelve True si la mano es es Siete y Medio: 
        Suma 7.5 y se forma con un siete y una figura de distinto palo.
        """
        if len(self.mano) != 2:
            return False
        
        it = iter(self.mano)
        c1 = next(it)
        c2 = next(it)
        
        es_7_c1 = c1.numero == 7
        es_figura_c2 = c2.numero in (10,11,12)
        
        es_7_c2 = c2.numero == 7
        es_figura_c1 = c1.numero in (10,11,12)
        
        return ((es_7_c1 and es_figura_c2) or(es_7_c2 and es_figura_c1)) and self.mano.suma() == 7.5

    @property
    def mano(self)-> MazoEspanolas:
        return super().mano
    
    @abstractmethod
    def se_planta(self)-> bool:
        """Define si el jugador decide plantarse."""
        pass

class CroupierSyM(JugadorSieteYMedio):
    """
    Clase concreta que representa al croupier o banca del casino.
    Tiene una lógica automática para decidir cuando plantarse.
    """
    def __init__(self)-> None:
        super().__init__('Sr Croupier')
        self.color = 154 # Verde
    
    def se_planta(self)-> bool:
        suma = self.mano.suma()
        print(f"{self} ({suma})")
        if suma >= 7.5:
            return True
        if suma >= 5:
            print("Se planta [automático]")
            return True
        return False
    
    def __str__(self)-> str:
        return f"{strclr(self.nombre, self.color)} ==> {self.mano}"


class ClienteSyM(JugadorSieteYMedio):
    """
    Clase abstracta que representa a un cliente del casino.
    Administra el sistema de fichas y apuestas.
    """
    
    colores = [10,11,12,13,14,32,125,175,201] # Paleta de colores para diferenciar a los jugadores
    
    def __init__(self, nombre:str, fichas:int)-> None:
        super().__init__(nombre)
        self.__fichas = fichas
        shuffle(ClienteSyM.colores)
        self.color = ClienteSyM.colores.pop(0)
        
    @property
    def fichas(self)-> int:
        return self.__fichas
    
    def ganar_fichas(self, cantidad:int)-> None:
        """Suma fichas al jugador."""
        self.__fichas += cantidad
    
    def perder_fichas(self, cantidad:int)-> None:
        """Resta fichas al jugador."""
        self.__fichas -= cantidad
    
    @abstractmethod
    def apostar(self)-> int:
        """
        Método abstracto para definir cuánto apuesta el jugador.
        :return: Cantidad de fichas apostadas.
        """
        pass
    
    def __str__(self)-> str:
        return f"{strclr(self.nombre, self.color)} ==> {self.mano} $[{self.fichas}] ({self.mano.suma()})"

class JugadorHumanoSyM(ClienteSyM):
    """
    Clase concreta que representa a un jugador humano de Siete y Medio.
    Interactúa mediante entrada por teclado.
    """    
    def __init__(self, nombre:str, fichas:int)-> None:
        super().__init__(nombre, fichas)
    
    def se_planta(self)-> bool:
        print(str(self))
        if self.mano.suma() >= 7.5:
            return True
        return input("¿Se planta? [S/N]: ").strip().upper() == 'S'
    
    def apostar(self)-> int:
        while True:
            try:
                apuesta = int(input(f"{self.nombre}, ingrese apuesta (tiene {self.fichas}): "))
                if 1 <= apuesta <= self.fichas:
                    return apuesta
                print("Apuesta inválida. Debe ser mayor que 0 y menor o igual a sus fichas.")
            except ValueError:
                print("Por favor, ingrese un número entero válido.")
                
                
class JugadorComputadoraSyM(ClienteSyM):
    """
    Clase concreta que representa un jugador automático controlado por la computadora.
    """                
    
    def __init__(self, nombre:str, fichas:str)-> None:
        super().__init__(nombre, fichas)
    
    def se_planta(self)-> bool:
        return self.mano.suma() >= 5
    
    def apostar(self)-> int:
        """
        Estrategia automática simple:
        Apuesta el 10% de sus fichas (al menos 1 ficha).
        """
        return max(1, self.fichas //10)




# --- Bloque de prueba ---
if __name__ == '__main__':
    # print("\nProbando clases de jugadores:")

    # print("\nCroupier:")
    # c = Croupier()
    # print(c)

    # print("\nJugador automático:")
    # bot = JugadorComputadora("CPU-Rojo", 500)
    # print(bot)

    # print("\nJugador humano:")
    # human = JugadorHumano("Alfredo", 1000)
    # print(human)

    # print("\nIntentando instanciar Cliente (debe fallar):")
    # try:
    #     cliente = Cliente("Fantasma", 0)  # Esto debería lanzar TypeError
    # except TypeError as e:
    #     print(f"Error esperado: {e}")
        
        


# --- Bloque de prueba Siete y Medio ---
    print("\n=== PRUEBAS: Siete y Medio ===")

    print("\nCroupier SyM:")
    croupier_sym = CroupierSyM()
    print(croupier_sym)

    print("\nJugador automático SyM:")
    bot_sym = JugadorComputadoraSyM("CPU-Azul", 500)
    print(bot_sym)

    print("\nJugador humano SyM:")
    human_sym = JugadorHumanoSyM("Rodrigo", 1000)
    print(human_sym)

    print("\nProbando tiene_siete_y_medio_real() y tiene_siete_y_medio():")
    from cartas import CartaEspanola

    # Crea un jugador manual
    test_jugador = JugadorHumanoSyM("Test", 100)

    # Siete y figura del mismo palo → 7 y medio REAL
    # test_jugador.poner(CartaEspanola(7, 1))
    # test_jugador.poner(CartaEspanola(10, 1))
    # print(f"Mano: {test_jugador.mano}")
    # print("¿Siete y medio real?:", test_jugador.tiene_siete_y_medio_real())  # True
    # print("¿Siete y medio común?:", test_jugador.tiene_siete_y_medio())      # True
    # print(f"Puntos: {test_jugador.mano.suma()}")
    
    #Borra mano y prueba con 7 y figura de distinto palo → 7 y medio COMÚN
    # test_jugador.mano.vaciar()
    test_jugador.poner(CartaEspanola(7, 2))
    test_jugador.poner(CartaEspanola(11, 3))
    print(f"\nMano: {test_jugador.mano}")
    print("¿Siete y medio real?:", test_jugador.tiene_siete_y_medio_real())  # False
    print("¿Siete y medio común?:", test_jugador.tiene_siete_y_medio())      # True
    print(f"Puntos: {test_jugador.mano.suma()}")
    
    # Prueba mano inválida → 7 y 5 = 12 (no es 7.5)
    # test_jugador.mano.vaciar()
    # test_jugador.poner(CartaEspanola(7, 2))
    # test_jugador.poner(CartaEspanola(5, 2))
    # print(f"\nMano: {test_jugador.mano}")
    # print("¿Siete y medio real?:", test_jugador.tiene_siete_y_medio_real())  # False
    # print("¿Siete y medio común?:", test_jugador.tiene_siete_y_medio())      # False
    # print(f"Puntos: {test_jugador.mano.suma()}")

    print("\nIntentando instanciar ClienteSyM (debe fallar):")
    try:
        cliente_sym = ClienteSyM("Fantasma", 0)
    except TypeError as e:
        print(f"Error esperado: {e}")

