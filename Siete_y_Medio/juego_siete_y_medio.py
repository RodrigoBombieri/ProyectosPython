"""
Modulo que implementa la lógica del juego de Siete y Medio.
Contiene la clase principal SieteYMedio que controla el flujo de la partida.
"""

from jugadores import CroupierSyM, JugadorHumanoSyM, JugadorComputadoraSyM, ClienteSyM
from random import randint
from typing import List
from txtcolores import strclr
from cartas import CartaEspanola
from mazos import MazoSieteYMedio
import sys
sys.path.append('recursos/')  # Agrega el directorio 'recursos/' al path para importaciones locales

class SieteYMedio:
    """
    Clase proncipal que implementa el juego de Siete y Medio.
    Controla el flujo del juego, manejo de jugadores, mazo y apuestas.
    """
    def __init__(self, nombres:str=None)-> None:
        """
        Constructor del juego. Inicializa los componentes necesarios.
        :param nombres: Cadena separada por comas con nombres de bots a crear automáticamente.
        """
        self.__color_alerta = 196 # Color ANSI para mostrar alertas.
        self.__color_sistema = 15 # Color ANSI para mensajes generales del sistema.
        self.__color_gana = 46 # Verde brillante - para cuando gana
        self.__color_empata = 226  # Amarillo - para empates
        self.__croupier = CroupierSyM() # Instancia del croupier (la banca).
        self.__jugadores: List[ClienteSyM] = [] # Lista de jugadores participantes.
        self.__las_apuestas: List[int] = [] # Lista de apuestas realizadas por los jugadores.
        self.__mazo = MazoSieteYMedio() # Mazo de cartas para Siete y Medio
        self.__mazo.llenar() # Llena el mazo con cartas.
        
        # Si se pasan nombres, se crean bots automáticamente
        if nombres:
            for nombre in nombres.split(','):
                fichas_iniciales = randint(100,1000) # Fichas aleatorias para el bot
                self.__jugadores.append(JugadorComputadoraSyM(nombre.strip(), fichas_iniciales))

    def agregar_jugador(self, cliente:ClienteSyM)-> None:
        """
        Agrega un jugador manualmente a la lista de jugadores.
        :param cliente: Instancia de Cliente (humano o bot).
        """
        if not isinstance(cliente, ClienteSyM):
            raise TypeError('El jugador debe ser un objeto del tipo ClienteSyM')
        self.__jugadores.append(cliente)

    def __hay_jugadores(self)-> bool:
        """
        Verifica si hay jugadores activos.
        :return: True si hay al menos un jugador.
        """
        return len(self.__jugadores) > 0
    
    def __repartir_una_carta_jugadores(self)-> None:
        """
        Reparte una carta a cada jugador.
        """
        for jugador in self.__jugadores:
            # carta_oculta = self.__mazo.sacar()
            # carta_oculta.tapar()
            jugador.poner(self.__mazo.sacar())

    def __repartir_una_carta_croupier(self)-> None:
        """Reparte una carta al croupier"""
        # carta_oculta = self.__mazo.sacar()
        # carta_oculta.tapar()
        self.__croupier.poner(self.__mazo.sacar())

    def __apostar(self)-> None:
        """
        Solicita las apuestas a cada jugador y las guarda.
        """
        self.__las_apuestas.clear()
        for jugador in self.__jugadores:
            self.__las_apuestas.append(jugador.apostar())
    
    def __jugadores_juegan(self)-> None:
        """
        Ejecuta el turno de cada jugador, permitiéndoles pedir cartas
        """
        for jugador in self.__jugadores:
            while not jugador.se_planta():
                jugador.poner(self.__mazo.sacar())        

    def __croupier_juega(self)-> None:
        """
        Ejecuta el turno del croupier.
        """
        while not self.__croupier.se_planta():
            self.__croupier.poner(self.__mazo.sacar())
        print(f"{self.__croupier} ({self.__croupier.mano.suma()})")

    def __descartar(self)-> None:
        """
        Descarta todas las cartas usadas devolviéndolas al mazo.
        """
        for jugador in self.__jugadores:
            while not jugador.mano.isvacio():
                self.__mazo.poner(jugador.mano.sacar())
        while not self.__croupier.mano.isvacio():
            self.__mazo.poner(self.__croupier.mano.sacar())
    
    def __repartir_premios(self)-> None:
        """
        Evalúa el resultado del juego y reparte o retira fichas según corresponda.
        """
        suma_croupier = self.__croupier.mano.suma()
        
        for idx, jugador in enumerate(self.__jugadores):
            suma_jugador = jugador.mano.suma()
            apuesta = self.__las_apuestas[idx]
            
            if suma_jugador > 7.5:
                print(jugador, strclr("Pierde! Se pasó.", self.__color_alerta))
                jugador.perder_fichas(apuesta)
            elif suma_croupier > 7.5:
                print(jugador, strclr("Gana! El croupier se pasó.", self.__color_gana))
                jugador.ganar_fichas(apuesta)
            elif suma_jugador < suma_croupier:
                print(jugador, strclr("Pierde! El croupier gana.", self.__color_alerta))
                jugador.perder_fichas(apuesta)
            elif suma_jugador == suma_croupier:
                print(jugador, strclr("Empate! No gana ni pierde.", self.__color_empata))
            else:
                if jugador.tiene_siete_y_medio_real():
                    if not self.__croupier.tiene_siete_y_medio_real():
                        print(jugador, strclr("Gana 200% con Siete y Medio Real!", self.__color_gana))
                        jugador.ganar_fichas(apuesta * 2)
                    else:
                        print(jugador, strclr("Empate! Ambos tienen Siete y Medio Real.", self.__color_empata))
                elif jugador.tiene_siete_y_medio():
                    if self.__croupier.tiene_siete_y_medio_real():
                        print(jugador, strclr("Pierde! El croupier tiene Siete y Medio Real.", self.__color_alerta))
                        jugador.perder_fichas(apuesta)
                    elif self.__croupier.tiene_siete_y_medio():
                        print(jugador, strclr("Empate! Ambos tienen Siete y Medio.", self.__color_empata))
                    else:
                        print(jugador, strclr("Gana 150% con Siete y Medio!", self.__color_gana))
                        jugador.ganar_fichas(int(apuesta * 1.5))
                else:
                    if self.__croupier.tiene_siete_y_medio_real() or self.__croupier.tiene_siete_y_medio():
                        print(jugador, strclr("Pierde! El croupier tiene mejor jugada.", self.__color_alerta))
                        jugador.perder_fichas(apuesta)
                    elif suma_jugador > suma_croupier:
                        print(jugador, strclr("Gana! Tiene mejor puntaje.", self.__color_gana))
                        jugador.ganar_fichas(apuesta)
                    elif suma_jugador == suma_croupier:
                        print(jugador, strclr("Empate! No gana ni pierde.", self.__color_empata))
                    else:
                        print(jugador, strclr("Pierde! El croupier gana.", self.__color_alerta))
                        jugador.perder_fichas(apuesta)

                    
                    
    def jugar(self)-> None:
        """
        Controla el bucle principal del juego.
        Mientras haya jugadores, se realiza una ronda completa de Siete y Medio
        """
        while self.__hay_jugadores():
            print(strclr("\n--- Nueva Ronda ---", self.__color_sistema))
            print(strclr("Mezclando el mazo...", self.__color_sistema))
            self.__mazo.mezclar()
            self.__apostar()
            self.__repartir_una_carta_jugadores()
            self.__repartir_una_carta_croupier()
            self.__jugadores_juegan() # Ver lo de la carta tapada, si se excede debe avisar (ya que hay una carta tapada)
            self.__croupier_juega()
            self.__repartir_premios()
            self.__descartar()
            
            jugadores_restantes = []
            for j in self.__jugadores:
                if j.fichas > 0:
                    jugadores_restantes.append(j)
                else:
                    print(strclr(f"{j.nombre} ha sido eliminado por quedarse sin fichas.", self.__color_alerta))                   
            self.__jugadores = jugadores_restantes

        print(strclr("\nNo quedan jugadores con fichas. Fin del juego.", self.__color_alerta))

def test():
    """
    Función de prueba que inicializa una partida con dos jugadores humanos y bots.
    """
    
    juego = SieteYMedio()
    
    juego.agregar_jugador(JugadorHumanoSyM("Raul", 1000))
    juego.agregar_jugador(JugadorHumanoSyM("Rosa", 1000))
    
    # juego.agregar_jugador(JugadorComputadoraSyM("Bot-Ana", randint(500, 1000)))
    # juego.agregar_jugador(JugadorComputadoraSyM("Bot-Luis", randint(500, 1000)))
    
    juego.jugar()

if __name__ == '__main__':
    test()