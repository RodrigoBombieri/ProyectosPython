
"""
Modulo que implementa la lógica del juego de BlackJack.
Contiene la clase principal BlackJack que controla el flujo de la partida.
"""

from jugadores import Croupier, JugadorHumano, JugadorComputadora, Cliente
from random import randint
from typing import List
from txtcolores import strclr
from cartas import CartaPoker
from mazos import MazoBlackJack
import sys
sys.path.append('recursos/')  # Agrega el directorio 'recursos/' al path para importaciones locales


class BlackJack:
    """
    Clase principal que implementa el juego de BlackJack.
    Controla el flujo del juego, manejo de jugadores, mazo y apuestas.
    """

    def __init__(self, nombres: str = None) -> None:
        """
        Constructor del juego. Inicializa los componentes necesarios.

        :param nombres: Cadena separada por comas con nombres de bots a crear automáticamente.
        """
        self.__color_alerta = 196  # Color ANSI para mostrar alertas
        self.__color_sistema = 15  # Color ANSI para mensajes generales del sistema
        self.__croupier = Croupier()  # Instancia del croupier (la banca)
        self.__jugadores: List[Cliente] = []  # Lista de jugadores participantes
        self.__las_apuestas: List[int] = []  # Lista de apuestas realizadas por los jugadores
        self.__mazo = MazoBlackJack()  # Mazo de cartas para BlackJack
        self.__mazo.llenar()  # Llena el mazo con cartas

        # Si se pasan nombres, se crean bots automáticamente
        if nombres:
            for nombre in nombres.split(','):
                fichas_iniciales = randint(100, 1000)  # Fichas aleatorias para el bot
                self.__jugadores.append(JugadorComputadora(nombre.strip(), fichas_iniciales))

    def agregar_jugador(self, cliente: Cliente) -> None:
        """
        Agrega un jugador manualmente a la lista de jugadores.

        :param cliente: Instancia de Cliente (jugador humano o bot)
        """
        if not isinstance(cliente, Cliente):
            raise TypeError('El jugador debe ser un objeto de tipo Cliente.')
        self.__jugadores.append(cliente)

    def __hay_jugadores(self) -> bool:
        """
        Verifica si hay jugadores activos.

        :return: True si hay al menos un jugador.
        """
        return len(self.__jugadores) > 0

    def __repartir_dos_cartas_jugadores(self) -> None:
        """
        Reparte dos cartas a cada jugador.
        """
        for jugador in self.__jugadores:
            jugador.poner(self.__mazo.sacar())
            jugador.poner(self.__mazo.sacar())

    def __repartir_dos_cartas_croupier(self) -> None:
        """
        Reparte dos cartas al croupier, una de ellas tapada.
        """
        carta_oculta = self.__mazo.sacar()
        carta_oculta.tapar()  # La primera carta va tapada
        self.__croupier.poner(carta_oculta)
        self.__croupier.poner(self.__mazo.sacar())

    def __apostar(self) -> None:
        """
        Solicita apuestas a cada jugador y las guarda.
        """
        self.__las_apuestas.clear()
        for jugador in self.__jugadores:
            apuesta = jugador.apostar()
            self.__las_apuestas.append(apuesta)

    def __jugadores_juegan(self) -> None:
        """
        Ejecuta el turno de cada jugador, permitiéndoles pedir cartas.
        """
        for jugador in self.__jugadores:
            while not jugador.se_planta():
                jugador.poner(self.__mazo.sacar())

    def __croupier_juega(self) -> None:
        """
        Ejecuta el turno del croupier revelando su carta tapada y jugando según las reglas.
        """
        self.__croupier.mano.destapar(0)  # Destapa su primera carta
        while not self.__croupier.se_planta():
            self.__croupier.poner(self.__mazo.sacar())
        print(f"{self.__croupier} ({self.__croupier.mano.suma()})")

    def __descartar(self) -> None:
        """
        Descarta todas las cartas usadas devolviéndolas al mazo.
        """
        for jugador in self.__jugadores:
            while not jugador.mano.isvacio():
                self.__mazo.poner(jugador.mano.sacar())
        while not self.__croupier.mano.isvacio():
            self.__mazo.poner(self.__croupier.mano.sacar())

    def __repartir_premios(self) -> None:
        """
        Evalúa el resultado del juego y reparte o retira fichas según corresponda.
        """
        suma_croupier = self.__croupier.mano.suma()

        for idx, jugador in enumerate(self.__jugadores):
            suma_jugador = jugador.mano.suma()
            apuesta = self.__las_apuestas[idx]

            if suma_jugador > 21:
                print(jugador, "Pierde! Se pasó.")
                jugador.perder_fichas(apuesta)
            elif suma_croupier > 21:
                print(jugador, "Gana! El croupier se pasó.")
                jugador.ganar_fichas(apuesta)
            elif suma_jugador > suma_croupier:
                print(jugador, "Gana! Tiene mejor mano.")
                jugador.ganar_fichas(apuesta)
            elif suma_jugador < suma_croupier:
                print(jugador, "Pierde! El croupier gana.")
                jugador.perder_fichas(apuesta)
            else:
                print(jugador, "Empate! No gana ni pierde.")

    def jugar(self) -> None:
        """
        Controla el bucle principal del juego.
        Mientras haya jugadores, se realiza una ronda completa de BlackJack.
        """
        while self.__hay_jugadores():
            self.__mazo.mezclar()
            self.__repartir_dos_cartas_jugadores()
            self.__repartir_dos_cartas_croupier()
            self.__apostar()
            self.__jugadores_juegan()
            self.__croupier_juega()
            self.__repartir_premios()
            self.__descartar()


def test():
    """
    Función de prueba que inicializa una partida con dos jugadores humanos y bots.
    """
    juego = BlackJack()
    
    juego.agregar_jugador(JugadorHumano("Raul", 1000))
    juego.agregar_jugador(JugadorHumano("Rosa", 1000))
    juego.jugar()


if __name__ == '__main__':
    test()