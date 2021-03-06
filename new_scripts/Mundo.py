""" Nome do módulo :        Mundo
    Ano de criação :        2019/10
    Descrição do módulo :   Módulo que define o Mundo onde ocorre o jogo
    Versão :                2.0
    Pré-requisitos :        Padrão Singleton
                            Jogador
                            Ball
                            ComportamentosJogadores Comportamentos
    Membros :               Lorena Bassani
"""
from .Patterns.Singleton import Singleton
from .Geometria import Ponto
from .Jogador import Jogador
from .ComportamentosJogadores.Comportamentos import COMPORTAMENTOS
from .Ball import Ball
from .Campo import Campo
from .Controle.ControleTrajeto.IControleTrajeto import IcontroleTrajeto
from .Controle.ControleTrajeto.ControleSiegwart import ControleSiegwart
from .PathPlanning.IPathPlanning import IPathPlanning
from .PathPlanning.AStar import AStar
from enum import Enum
import math as m

class Lado(Enum):
    ESQUERDO = 0
    DIREITO = 1

class Arena(object):
    cantoSuperior = {   "Direito"   : Ponto(170, 0),
                        "Esquerdo"  : Ponto(0, 0)
                    }
    cantoInferior = {   "Direito"   : Ponto(170, 130),
                        "Esquerdo"  : Ponto(0, 130)
                    }
    golDireito =    {   "Superior"  : Ponto(160 ,45),
                        "Meio"      : Ponto(160, 65),
                        "Inferior"  : Ponto(160, 95)
                    }
    golEsquerdo =   {   "Superior"  : Ponto(10 ,45),
                        "Meio"      : Ponto(10, 65),
                        "Inferior"  : Ponto(10, 95)
                    }
    marcacoes = {       "Meio" : Ponto(85, 65)
                }
    metricas = {        "Tamanho "  : (170, 130),
                        "Gol"       : (10, 40)
                }

class Mundo(Singleton):

    def __init__(self, *args, **keyargs):
        pass

    def inicializa(self, controladorTrajeto = ControleSiegwart(), pathPlanning = AStar, lado = Lado.DIREITO):
        self.__jogadores = {"Team" : list(), "Enemies" : list()}
        self.ball = Ball()
        self.campo = Campo(celulasX = 15, celulasY = 13)
        self.pathPlanning = AStar
        self.controladorTrajeto = controladorTrajeto
        self.lado = lado
    
    """ Nome da função :     inimigos (getter)
        Intenção da função : Retorna os Inimigos
        Pré-requisitos :     Nenhum
        Efeitos colaterais : Nenhum
        Parâmetros :         Nenhum
        Retorno :            list<Inimigos> : Lista de Inimigos
    """
    @property
    def inimigos(self):
        return self.__jogadores["Enemies"]
    
    """ Nome da função :     inimigos (setter)
        Intenção da função : Alterar a lista de inimigos
        Pré-requisitos :     Nenhum
        Efeitos colaterais : Altera todo o time de inimigos
        Parâmetros :         Novo time de Inimigos
        Retorno :            Nenhum
    """
    @inimigos.setter
    def inimigos(self, inimigos):
        self.__jogadores["Enemies"].clear()
        self.__jogadores["Enemies"].extend(inimigos)
    
    """ Nome da função :     goleiro (getter)
        Intenção da função : Retorna o Jogador Goleiro
        Pré-requisitos :     Nenhum
        Efeitos colaterais : Nenhum
        Parâmetros :         Nenhum
        Retorno :            Aliado : Jogador com Comportamento Goleiro
    """
    @property
    def goleiro(self):
        g = list(filter(lambda x: x.comportamento == COMPORTAMENTOS.GOLEIRO, self.__jogadores["Team"]))
        if g: 
            return g[0]
        return None
    
    """ Nome da função :     goleiro (setter)
        Intenção da função : Alterar o Goleiro
        Pré-requisitos :     Não ter um Goleiro previamente
        Efeitos colaterais : Define um novo goleiro
        Parâmetros :         int : Id do Jogador para alterar
        Retorno :            Nenhum
    """
    @goleiro.setter
    def goleiro(self, jogadorId):
        if not self.goleiro:
            p = self.jogador(jogadorId)
            p.comportamento = COMPORTAMENTOS.GOLEIRO
    
    """ Nome da função :     jogador (getter)
        Intenção da função : Retornar um Jogador de Acordo com seu Id
        Pré-requisitos :     Nenhum
        Efeitos colaterais : Nenhum
        Parâmetros :         int : Id do Jogador
        Retorno :            Jogador : Jogador correspondente ao Id
    """
    def jogador(self, jogadorId):
        p = list(filter(lambda x: x.id == jogadorId, self.__jogadores["Team"]))
        if p:
            return p
        return None
    
    @property
    def time(self):
        return self.__jogadores["Team"]
    
    @time.setter
    def time(self, newTime):
        self.__jogadores["Team"].clear()
        self.__jogadores["Team"].extend(newTime)

    def control(self):
        self.__defineFunction()
        controle = list()
        for p in self.__jogadores["Team"]:
            # Primeiro passo: Definir Objetivo
            goal = p.definirObjetivo(self).posicao
            start = p.posicao
            # Segundo passo: Planejar Caminho
            # path = self.pathPlanning.PathPlan(self.campo, self.campo.transform2Grid(start), self.campo.transform2Grid(goal))
            # path = self.pathPlanning.reconstructPath(path, self.campo.transform2Grid(start), self.campo.transform2Grid(goal))
            # Terceiro passo: Seguir Caminho
            # gx, gy = self.campo.transform2Cart(path.pop(0))
            gx, gy = goal
            sx, sy = start
            gt = m.acos((gx*sx + gy*sy)/(m.sqrt(gx**2 + gy**2)*m.sqrt(sx**2 + sy**2)))
            goal = gx, gy, gt
            start = sx, sy, p.theta
            vel = self.controladorTrajeto.controle(actualValue = start, objective = goal, speed = 100)
            controle.append(vel)
        return controle

    def __defineFunction(self):
        pass