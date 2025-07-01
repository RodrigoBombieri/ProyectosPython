"""
Este módulo define las clases relacionadas con cartas para juegos de naipes.
Incluye una clase abstracta `Carta` con atributos protegidos mediante propiedades,
y una clase concreta `CartaPoker` que representa una carta estándar de Poker.
"""

from abc import ABC, abstractmethod
from txtcolores import strclr

class Carta(ABC):
    """
    Clase abstracta que representa una carta genérica.
    Cada carta tiene un número, un palo y puede estar tapada o destapada.
    """

    def __init__(self, numero: int, palo: int, tapada: bool = False) -> None:
        """
        Inicializa los atributos de la carta.

        :param numero: Número de la carta (1 al 13).
        :param palo: Palo representado como entero (1 a 4).
        :param tapada: True si la carta está tapada al inicio.
        """
        self.__numero = numero  # Número de la carta (1=A, 11=J, 12=Q, 13=K)
        self.__palo = palo      # Palo de la carta (1=♥, 2=♦, 3=♣, 4=♠)
        self.__tapada = tapada  # Indica si la carta está boca abajo

    @property
    def numero(self) -> int:
        """Devuelve el número de la carta."""
        return self.__numero

    @property
    def palo(self) -> int:
        """Devuelve el palo de la carta."""
        return self.__palo

    @property
    def tapada(self) -> bool:
        """Devuelve True si la carta está tapada."""
        return self.__tapada

    @tapada.setter
    def tapada(self, estado: bool) -> None:
        """
        Cambia el estado de la carta (tapada o destapada).

        :param estado: True para tapar, False para destapar
        """
        self.__tapada = estado

    def tapar(self) -> None:
        """Marca la carta como tapada."""
        self.tapada = True

    def destapar(self) -> None:
        """Marca la carta como destapada."""
        self.tapada = False

    def istapada(self) -> bool:
        """Devuelve True si la carta está tapada."""
        return self.tapada

    def isdestapada(self) -> bool:
        """Devuelve True si la carta está destapada."""
        return not self.tapada

    @abstractmethod
    def dibujo_numero(self) -> str:
        """
        Devuelve el número decorado de la carta como string.
        :return: Cadena representando el número de la carta
        """
        pass

    @abstractmethod
    def dibujo_palo(self) -> str:
        """
        Devuelve el palo decorado de la carta como string.
        :return: Cadena representando el símbolo del palo
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.numero}, {self.palo}, {self.tapada})"

    def __str__(self) -> str:
        return f"{strclr('[','aquamarine_3')}{self.dibujo_numero()}{self.dibujo_palo()}{strclr(']','aquamarine_3')}"


class CartaPoker(Carta):
    """
    Clase concreta para representar una carta de Poker.
    """
    NUMEROS = ('#', 'A', '2', '3', '4', '5', '6','7', '8', '9', '10', 'J', 'Q', 'K') 
    PALOS = ('#', '♥', '♦', '♣', '♠')

    def isRoja(self) -> bool:
        """Devuelve True si la carta es de corazones o diamantes."""
        return self.palo in (1, 2)

    def isfigura(self) -> bool:
        """Devuelve True si la carta es J, Q o K."""
        return self.numero > 10

    def isNegra(self) -> bool:
        """Devuelve True si la carta es trébol o pica."""
        return not self.isRoja()

    def isPica(self) -> bool:
        """Devuelve True si la carta es una pica (♠)."""
        return self.palo == 4

    def isCorazon(self) -> bool:
        """Devuelve True si la carta es un corazón (♥)."""
        return self.palo == 1

    def isDiamante(self) -> bool:
        """Devuelve True si la carta es un diamante (♦)."""
        return self.palo == 2

    def isTrebol(self) -> bool:
        """Devuelve True si la carta es un trébol (♣)."""
        return self.palo == 3

    def isAs(self) -> bool:
        """Devuelve True si la carta es un As (A)."""
        return self.numero == 1

    def dibujo_numero(self) -> str:
        """
        Devuelve la representación visual del número.
        Si está tapada, se muestra un símbolo genérico.
        """
        if self.istapada():
            return strclr(CartaPoker.NUMEROS[0],'dark_orange')
        return strclr(CartaPoker.NUMEROS[self.numero],'dark_orange')

    def dibujo_palo(self) -> str:
        """
        Devuelve la representación visual del palo.
        Si está tapada, se muestra un símbolo genérico.
        El color depende si es roja o negra.
        """
        if self.istapada():
            return strclr(CartaPoker.PALOS[0], 'dark_orange')
        return strclr(CartaPoker.PALOS[self.palo], 'red_1' if self.isRoja() else 'white')

class CartaEspanola(Carta):
    """
    Clase concreta para representar una carta de baraja Española.
    """
    NUMEROS = ('#', '1', '2', '3', '4', '5', '6','7','8','9','10','11','12') 
    PALOS = {0:'#', 1:'🪙', 2:'🏆', 3:'🗡️',4:'🌿'}

    def isFigura(self):
        """Devuelve True si la carta es 10, 11 o 12."""
        return self.numero > 9
    
    def isOro(self):
        """Devuelve True si la carta es de Oro (🪙)."""
        return self.palo == 1

    def isCopa(self):
        """Devuelve True si la carta es de Copa (🏆)."""
        return self.palo == 2
    
    def isEspada(self):
        """Devuelve True si la carta es de Espada (🗡️)."""
        return self.palo == 3
    
    def isBasto(self):
        """Devuelve True si la carta es de Basto (🌿)."""
        return self.palo == 4
    
    def dibujo_numero(self)-> str:
        """
        Devuelve la representación visual del número.
        Si está tapada, se muestra un símbolo genérico.
        """
        if self.istapada():
            return strclr(CartaEspanola.NUMEROS[0],'dark_orange')
        return strclr(CartaEspanola.NUMEROS[self.numero],'dark_orange')
    
    def dibujo_palo(self)-> str:
        """
        Devuelve la representación visual del palo.
        Si está tapada, se muestra un símbolo genérico.
        """
        if self.istapada():
            return strclr(CartaEspanola.NUMEROS[0],'dark_orange')
        return CartaEspanola.PALOS[self.palo]
    
    def __str__(self) -> str:
        if self.istapada():
            return f"{strclr('[','aquamarine_3')}{self.dibujo_numero()}{self.dibujo_palo()}{strclr(']','aquamarine_3')}"
        return f"{strclr('[','aquamarine_3')}{self.dibujo_numero()}{self.dibujo_palo()}{' '}{strclr(']','aquamarine_3')}"
    
# ----------------------
# Prueba de funcionalidad
# ----------------------
if __name__ == '__main__':
    print("\nProbando creación de cartas:")
    carta1 = CartaPoker(1, 1)  # As de corazones
    carta2 = CartaPoker(12, 3)  # Reina de tréboles
    carta3 = CartaPoker(7, 4, tapada=True)  # 7 de picas tapado
    
    carta4 = CartaEspanola(5,1)
    carta5 = CartaEspanola(9,2)
    carta6 = CartaEspanola(11,3)
    carta7 = CartaEspanola(10,4)
    carta8 = CartaEspanola(5,1,tapada=True)
    
    for carta in (carta1, carta2, carta3, carta4, carta5, carta6, carta7,carta8):
        print(f"{carta} → Número: {carta.numero}, Palo: {carta.palo}, Tapada: {carta.tapada}")

    print("\n❌ Intentando instanciar la clase abstracta Carta...")
    try:
        carta_erronea = Carta(1, 1)
    except TypeError as e:
        print(f"Error al instanciar clase abstracta: {e}")
