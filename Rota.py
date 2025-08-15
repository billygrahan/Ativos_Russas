import heapq
import math
import os
import random
import time
import sys

# pip install psutil openpyxl
import psutil
import openpyxl

from BFS import bfs
from DFS import dfs
from BCU import bcu
from A_ESTRELA import a_estrela, heuristica_euclidiana, heuristica_haversiana

melhor_rota = []
distancia_entre_ativos = {}
caminho_entre_ativos = []


graph_dist = {}
graph_Coordenadas = {}
qtd_vertices = 0

inicio = 5
ativos = []

alg = 'A_Estrela_Haversiano' 

def algoritmo(origem, destino):
    if alg == 'A_Estrela_Euclidiano':
        return a_estrela(graph_dist, graph_Coordenadas, origem, destino, heuristica_haversiana)
    elif alg == 'A_Estrela_Haversiano':
        return a_estrela(graph_dist, graph_Coordenadas, origem, destino, heuristica_euclidiana)
    elif alg == 'BFS':
        return bfs(graph_dist, origem, destino)
    elif alg == 'DFS':
        return dfs(graph_dist, origem, destino)
    elif alg == 'BCU':
        return bcu(graph_dist, origem, destino)

def carrega_teste():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos
    qtd_vertices = len(graph_Coordenadas)
    
    qtd_ativos_teste = 5
    ativos = random.sample(range(1, qtd_vertices + 1), qtd_ativos_teste)
    
    distancia_entre_ativos[inicio] = {}
    for ativo in ativos:
        distancia_entre_ativos[ativo] = {}

def Carrega_Dados():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos
    
    with open("RUSSAS_MAPA.gr", "r") as arquivo:  
        for linha in arquivo:
            linha_dividida = linha.split()
                
            vertice_origem = int(linha_dividida[1])
            vertice_destino = int(linha_dividida[2])
            vertice_distancia = int(linha_dividida[3])
            
            if vertice_origem not in graph_dist.keys():
                graph_dist[vertice_origem] = {vertice_destino:vertice_distancia}
            else:
                graph_dist[vertice_origem][vertice_destino] = vertice_distancia
                
    with open("RUSSAS_MAPA.co", "r") as arquivo:  
        for linha in arquivo:        
            linha_dividida = linha.split()
            
            vertice_origem = int(linha_dividida[1])
            coordenada1 = float(linha_dividida[2]) / 1_000_000
            coordenada2 = float(linha_dividida[3]) / 1_000_000
            
            graph_Coordenadas[vertice_origem] = (coordenada1, coordenada2)



def Construir():
    global melhor_rota, distancia_entre_ativos , inicio, ativos , graph_dist, graph_Coordenadas
    melhor_rota = []
    caminho_entre_ativos = []

    melhor_rota.append((inicio, 0))

    caminho_inicial = random.sample(ativos, len(ativos))

    for i in range(len(caminho_inicial)+1):
        if i == 0:
            heuristica = algoritmo(inicio, caminho_inicial[i])
            rota_encontrada, distancia_percorrida, quantidade_nos_expandidos, fator_ramificacao = heuristica
            distancia_entre_ativos[inicio][caminho_inicial[i]] = distancia_percorrida
            caminho_entre_ativos.append(rota_encontrada)
            melhor_rota.append((caminho_inicial[i], melhor_rota[-1][1] + distancia_percorrida))
        elif i >= (len(caminho_inicial)):
            heuristica = algoritmo(caminho_inicial[i-1], inicio)
            rota_encontrada, distancia_percorrida, quantidade_nos_expandidos, fator_ramificacao = heuristica
            distancia_entre_ativos[caminho_inicial[i-1]][inicio] = distancia_percorrida
            caminho_entre_ativos.append(rota_encontrada)
            melhor_rota.append((inicio, melhor_rota[-1][1] + distancia_percorrida))
        else:
            heuristica = algoritmo(caminho_inicial[i-1], caminho_inicial[i])
            rota_encontrada, distancia_percorrida, quantidade_nos_expandidos, fator_ramificacao = heuristica
            distancia_entre_ativos[caminho_inicial[i-1]][caminho_inicial[i]] = distancia_percorrida
            caminho_entre_ativos.append(rota_encontrada)
            melhor_rota.append((caminho_inicial[i], melhor_rota[-1][1] + distancia_percorrida))


if __name__ == "__main__":
    Carrega_Dados()
    carrega_teste()

    Construir()

    print("Melhor rota:")
    print(" -> ".join(str(tupla) for tupla in melhor_rota))


    


