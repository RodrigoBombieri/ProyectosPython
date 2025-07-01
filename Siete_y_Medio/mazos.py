
"""
Modulo que define la jerarquía de clases relacionadas con mazos de cartas.
Incluye una clase abstracta `Mazo` y dos implementaciones concretas: `MazoPoker` y `MazoBlackJack`.
Proporciona operaciones para manipular cartas: mezclar, sacar, poner, tapar, destapar, etc.
"""

from typing import List
from cartas import Carta, CartaPoker, CartaEspanola
from abc import ABC, abstractmethod
from random import shuffle

class Mazo(ABC):
    """
    Clase abstracta que representa un mazo de cartas.
    Gestiona una lista de cartas y ofrece operaciones comunes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__las_cartas: List[Carta] = []  # Lista privada que contiene las cartas del mazo

    def poner(self, carta: Carta, index: int = -1) -> None:
        """
        Agrega una carta al mazo.

        :param carta: Carta a agregar
        :param index: Posición donde insertar la carta. Por defecto, al final.
        """
        if index <= -1:
            self.__las_cartas.append(carta)
        else:
            self.__las_cartas.insert(index, carta)

    def sacar(self, index: int = 0) -> Carta:
        """
        Extrae una carta del mazo.

        :param index: Índice de la carta a extraer (por defecto, primera carta).
        :return: Carta extraída
        """
        if 0 <= index < len(self):
            return self.__las_cartas.pop(index)
        raise IndexError('Índice fuera de rango al sacar carta del mazo.')

    def tapar(self, index: int = None) -> None:
        """
        Tapa todas las cartas del mazo o una específica.

        :param index: Índice de la carta a tapar, o None para todas.
        """
        if index is None:
            for carta in self:
                carta.tapar()
        else:
            self.__las_cartas[index].tapar()

    def destapar(self, index: int = None) -> None:
        """
        Destapa todas las cartas del mazo o una específica.

        :param index: Índice de la carta a destapar, o None para todas.
        """
        if index is None:
            for carta in self:
                carta.destapar()
        else:
            self.__las_cartas[index].destapar()

    def mezclar(self) -> None:
        """
        Mezcla el orden de las cartas en el mazo.
        """
        shuffle(self.__las_cartas)

    def isvacio(self) -> bool:
        """
        Indica si el mazo está vacío.

        :return: True si el mazo no contiene cartas.
        """
        return len(self.__las_cartas) == 0

    def __len__(self) -> int:
        """
        Devuelve la cantidad de cartas en el mazo.

        :return: Cantidad de cartas
        """
        return len(self.__las_cartas)

    def __iter__(self):
        """
        Permite iterar sobre las cartas del mazo.
        """
        return iter(self.__las_cartas)

    def __str__(self) -> str:
        """
        Representación visual del mazo (solo para impresión).

        :return: Cadena con las cartas del mazo como string.
        """
        return ''.join(str(carta) for carta in self.__las_cartas)

    def __repr__(self) -> str:
        """
        Representación técnica del mazo para depuración.

        :return: Cadena con las cartas representadas técnicamente.
        """
        return ','.join(repr(carta) for carta in self.__las_cartas)

    @abstractmethod
    def llenar(self) -> None:
        """
        Método abstracto que debe ser implementado en subclases para llenar el mazo con cartas.
        """
        pass


class MazoPoker(Mazo):
    """
    Clase concreta para mazo estándar de Poker (52 cartas).
    """
    CANTIDAD_CARTAS = 52

    @classmethod
    def get_cantidad_cartas(cls) -> int:
        """Devuelve la cantidad total de cartas en el mazo de Poker."""
        return cls.CANTIDAD_CARTAS

    def llenar(self) -> None:
        """
        Llena el mazo con 52 cartas de Poker.
        """
        for numero in range(1, 14):
            for palo in range(1, 5):
                self.poner(CartaPoker(numero, palo))

    def sacar(self, index: int = 0) -> CartaPoker:
        return super().sacar(index)

    def poner(self, carta: CartaPoker, index: int = -1) -> None:
        super().poner(carta, index)


class MazoBlackJack(Mazo):
    """
    Mazo de BlackJack: combina 10 mazos de poker (520 cartas).
    """
    CANTIDAD_CARTAS = 52 * 10

    @classmethod
    def get_cantidad_cartas(cls) -> int:
        """Devuelve la cantidad total de cartas en el mazo de BlackJack."""
        return cls.CANTIDAD_CARTAS

    def llenar(self) -> None:
        """
        Llena el mazo con 520 cartas (10 mazos de Poker).
        """
        for _ in range(10):
            for numero in range(1, 14):
                for palo in range(1, 5):
                    self.poner(CartaPoker(numero, palo))

    def sacar(self, index: int = 0) -> CartaPoker:
        return super().sacar(index)

    def poner(self, carta: CartaPoker, index: int = -1) -> None:
        super().poner(carta, index)

    def suma(self) -> int:
        """
        Calcula la suma total de los valores de las cartas del mazo
        según reglas del BlackJack (A vale 1 u 11, figuras valen 10).

        :return: Suma entera total de las cartas visibles.
        """
        cantidad_unos = 0  # Cantidad de ases
        suma_numeros = 0  # Suma acumulada

        for carta in self:
            if carta.numero == 1:
                cantidad_unos += 1
            elif carta.numero <= 10:
                suma_numeros += carta.numero
            else:
                suma_numeros += 10

        if cantidad_unos == 0:
            return suma_numeros
        elif cantidad_unos == 1:
            return suma_numeros + (11 if suma_numeros + 11 <= 21 else 1)
        else:
            if suma_numeros + 11 + (cantidad_unos - 1) > 21:
                return suma_numeros + 11 + (cantidad_unos - 1)
            return suma_numeros + cantidad_unos

class MazoEspanolas(Mazo):
    """
    Clase concreta para mazo estándar de 52 cartas Españolas.
    """
    CANTIDAD_CARTAS = 52

    @classmethod
    def get_cantidad_cartas(cls)-> int:
        """Devuelve la cantidad total de cartas en el mazo de cartas Españolas."""
        return cls.CANTIDAD_CARTAS
    
    def llenar(self)-> None:
        """Llena el mazo con 52 cartas Españolas."""
        for numero in range(1,13):
            for palo in range(1,5):
                self.poner(CartaEspanola(numero,palo))
    
    def sacar(self, index = 0)-> CartaEspanola:
        return super().sacar(index) 
    
    def poner(self, carta: CartaEspanola, index: int = -1)-> None:
        super().poner(carta,index)  


class MazoSieteYMedio(MazoEspanolas):
    """
    Mazo de Siete y Medio: no incluye los 8 y 9 (40 cartas).
    """
    CANTIDAD_CARTAS = 40
    
    @classmethod
    def get_cantidad_cartas(cls):
        """Devuelve la cantidad total de cartas en el mazo de Siete y Medio"""
        return cls.CANTIDAD_CARTAS
    
    def llenar(self)-> None:
        """Llena el mazo con 40 cartas (sin 8 ni 9)."""
        for numero in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]:
            for palo in range(1,5):
                self.poner(CartaEspanola(numero,palo))

    def sacar(self, index: int=0)-> CartaEspanola:
        return super().sacar(index)
    
    def poner(self, carta: CartaEspanola, index: int=-1)-> None:
        super().poner(carta,index)
        
    def suma(self)-> float:
        """
        Calcula la suma total de los valores de las cartas del mazo
        según reglas del Siete y Medio (10,11 y 12 valen 0.5).
        
        :return: Suma entera total de las cartas visibles.
        """
        VALOR_FIGURAS = 0.5 # Valor de 10, 11 o 12
        suma_numeros = 0 # Suma acumulada
        
        for carta in self:
            if carta.numero in (10,11,12):
                suma_numeros += VALOR_FIGURAS
            else:
                suma_numeros += carta.numero
        
        return suma_numeros


# ----------------------
# Test básico de mazos
# ----------------------
if __name__ == '__main__':
    print("\n🃏 Test del MazoPoker")
    mazo_p = MazoPoker()
    mazo_p.llenar()
    mazo_p.mezclar()
    print(f"Cartas en MazoPoker: {len(mazo_p)}")
    print(mazo_p)

    print("\n🂡 Test del MazoBlackJack")
    mazo_bj = MazoBlackJack()
    mazo_bj.llenar()
    print(f"Cartas en MazoBlackJack: {len(mazo_bj)}")
    print("Suma de valores (primeras 10 cartas):")
    for _ in range(10):
        carta = mazo_bj.sacar()
        print(f"{carta} ", end='')
    print(f"\nSuma parcial: {mazo_bj.suma()}")
    
    # SIETE Y MEDIO
    print("\n🂮 Test del MazoSieteYMedio - suma controlada")
    mazo_test = MazoSieteYMedio()
    mazo_test.cartas = []  # Vaciar por si llena() se ejecuta en __init__

    # Agregar cartas específicas
    mazo_test.poner(CartaEspanola(1, 1))   # 1 🪙
    mazo_test.poner(CartaEspanola(5, 3))   # 5 ⚔️
    mazo_test.poner(CartaEspanola(12, 4))  # 12 🪵
    mazo_test.poner(CartaEspanola(11, 2))  # 11 🏆

    # Mostrar cartas y suma
    print("Cartas agregadas al mazo de prueba:")
    for carta in mazo_test:
        print(f"{'['}{carta.dibujo_numero()}{carta.dibujo_palo()}{' '}{']'}", end=' ')
    print(f"\nSuma esperada: 7.0")
    print(f"Suma calculada: {mazo_test.suma()}")
