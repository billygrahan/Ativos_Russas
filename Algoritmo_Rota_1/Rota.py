import heapq
import math
import os
import random
import time
import sys
import copy
# pip install psutil openpyxl
import psutil
import openpyxl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Algoritmos.BFS import bfs
from Algoritmos.DFS import dfs
from Algoritmos.BCU import bcu
from Algoritmos.A_ESTRELA import a_estrela, heuristica_euclidiana, heuristica_haversiana

melhor_rota = []
distancia_entre_ativos = {}
caminho_entre_ativos = []


graph_dist = {}
graph_Coordenadas = {}
qtd_vertices = 0

inicio = 5
ativos = []

alg = 'A_Estrela_Haversiano' 
iteracoes = 10000

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
 
def Carrega_Dados():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos
    
    filepath = os.path.join(os.path.dirname(__file__), "RUSSAS_MAPA_N42.gr")
    with open(filepath, "r") as arquivo: 
        for linha in arquivo:
            linha_dividida = linha.split()
                
            vertice_origem = int(linha_dividida[1])
            vertice_destino = int(linha_dividida[2])
            vertice_distancia = int(linha_dividida[3])
            
            if vertice_origem not in graph_dist.keys():
                graph_dist[vertice_origem] = {vertice_destino:vertice_distancia}
            else:
                graph_dist[vertice_origem][vertice_destino] = vertice_distancia
                
    filepath_co = os.path.join(os.path.dirname(__file__), "RUSSAS_MAPA_N42.co")
    with open(filepath_co, "r") as arquivo:    
        for linha in arquivo:        
            linha_dividida = linha.split()
            
            vertice_origem = int(linha_dividida[1])
            coordenada1 = float(linha_dividida[2]) 
            coordenada2 = float(linha_dividida[3]) 
            
            graph_Coordenadas[vertice_origem] = (coordenada1, coordenada2)

def Construir():
    global melhor_rota, distancia_entre_ativos , inicio, ativos , graph_dist, graph_Coordenadas

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

def recalcula_distancias(melhor_rota_copia):
    global distancia_entre_ativos , inicio, ativos , graph_dist, graph_Coordenadas
    
    for i in range(len(melhor_rota_copia)-1):
        origem = melhor_rota_copia[i][0]
        destino = melhor_rota_copia[i+1][0]
        
        if destino not in distancia_entre_ativos[origem]:
            heuristica = algoritmo(origem, destino)
            rota_encontrada, distancia_percorrida, quantidade_nos_expandidos, fator_ramificacao = heuristica
            distancia_entre_ativos[origem][destino] = distancia_percorrida
            caminho_entre_ativos.append(rota_encontrada)
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1] + distancia_percorrida)
        else:
            distancia_percorrida = distancia_entre_ativos[origem][destino]
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1] + distancia_percorrida)

def Roleta():
    global melhor_rota, distancia_entre_ativos , inicio, ativos , graph_dist, graph_Coordenadas
    
    roleta = random.sample(range(1, melhor_rota[-1][1]), 1)

    melhor_rota_copia = copy.deepcopy(melhor_rota)

    for i in range(len(melhor_rota_copia)-2, 1, -1):
        if roleta[0] <= melhor_rota_copia[i][1]:
            elemento = melhor_rota_copia.pop(i)
            pos = random.randint(1, len(melhor_rota_copia)-1)
            melhor_rota_copia.insert(pos, elemento)
    
    recalcula_distancias(melhor_rota_copia)

    return melhor_rota_copia
   
def melhorar():
    global melhor_rota, distancia_entre_ativos , inicio, ativos , graph_dist, graph_Coordenadas

    for _ in range(iteracoes):
        melhor_rota_copia = Roleta()
        if melhor_rota_copia[-1][1] < melhor_rota[-1][1]:
            melhor_rota = melhor_rota_copia
        
def carrega_teste():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos, melhor_rota, caminho_entre_ativos, alg, iteracoes

    id = 0
    
    #algoritmos = ['BFS', 'DFS', 'BCU', 'A_Estrela_Euclidiano', 'A_Estrela_Haversiano']
    planilha = openpyxl.Workbook()
    del planilha['Sheet']
    planilha.create_sheet(alg)

    pagina = planilha[alg]
    pagina.sheet_format.baseColWidth = 30
    pagina.append(['Índice', 'Origem', 'Ativos', 'melhor_caminho', 'Distancia', 'Tempo'])

    for _ in range(10): # qtd de testes
        melhor_rota = []
        caminho_entre_ativos = []
        distancia_entre_ativos = {}
        ativos = []

        qtd_vertices = len(graph_Coordenadas)

        inicio = random.randint(1, qtd_vertices)
        #qtd_ativos_teste = random.randint(1, qtd_vertices-1)
        ativos = random.sample(range(1, qtd_vertices + 1), 5)

        # Inicializa as distâncias entre os ativos
        distancia_entre_ativos[inicio] = {}
        for ativo in ativos:
            distancia_entre_ativos[ativo] = {}


        inicio_tempo = time.time()
        Construir()
        melhorar()
        tempo_Rota = time.time() - inicio_tempo
        pagina.append([id, inicio, ", ".join(str(a) for a in ativos), " -> ".join(str(a[0]) for a in melhor_rota), melhor_rota[-1][1], tempo_Rota])
        id += 1

    planilha.save("Algoritmo_Rota_2/Ativos_Russas.xlsx")



if __name__ == "__main__":
    random.seed(141592)
    Carrega_Dados()
    carrega_teste()

    # Construir()

    # print("rota inicial:")
    # print(" -> ".join(str(tupla) for tupla in melhor_rota))

    # melhorar()

    # print("Melhor rota:")
    # print(" -> ".join(str(tupla) for tupla in melhor_rota))

    # print("\nDistâncias entre ativos:")
    # for origem in distancia_entre_ativos:
    #     for destino in distancia_entre_ativos[origem]:
    #         print(f"{origem} -> {destino}: {distancia_entre_ativos[origem][destino]}")

    # print("\nCaminho entre ativos:")
    # for caminho in caminho_entre_ativos:
    #     print(" -> ".join(str(vertice) for vertice in caminho))
    
    # melhor_rota_copia = Roleta()

    # print("Melhor rota:")
    # print(" -> ".join(str(tupla) for tupla in melhor_rota_copia))

    # print("\nDistâncias entre ativos:")
    # for origem in distancia_entre_ativos:
    #     for destino in distancia_entre_ativos[origem]:
    #         print(f"{origem} -> {destino}: {distancia_entre_ativos[origem][destino]}")




