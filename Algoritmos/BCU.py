import heapq
import math
import os
import random
import time
import sys

# Busca de Custo Uniforme (BCU)

def bcu(grafo, origem, destino):
    # Inicia a fila com o custo 0 e a origem
    fila_prioridade = [(0, origem)]
    
    # Inicia o vértice com valores padrão
    custos_acumulados = {}
    for vertice in grafo:
        custos_acumulados[vertice] = float("inf")
        
    # Altera o valor da raiz
    custos_acumulados[origem] = 0 
    
    predecessores = {} 
    nos_expandidos = 0
    nos_gerados = 0

    while fila_prioridade:  
        custo, vertice_atual = heapq.heappop(fila_prioridade)
        nos_expandidos += 1
    
        # Verifica se encontrou o destino
        if vertice_atual == destino: 
            break

        if custo > custos_acumulados[vertice_atual]: 
            continue

        # Loop dos vizinhos do vértice atual
        for vizinho, peso in grafo[vertice_atual].items(): 
            custo_total = custos_acumulados[vertice_atual] + peso 

            if custo_total < custos_acumulados[vizinho]:  
                custos_acumulados[vizinho] = custo_total  
                predecessores[vizinho] = vertice_atual  
                heapq.heappush(fila_prioridade, (custo_total, vizinho)) 
                nos_gerados += 1

    # Refaz o caminho
    caminho_minimo = [destino]
    vertice_atual = destino
    while vertice_atual != origem:
        caminho_minimo.append(predecessores[vertice_atual])
        vertice_atual = predecessores[vertice_atual]
    caminho_minimo.reverse()

    # Calcula a distância total do caminho
    distancia_total = 0
    for i in range(len(caminho_minimo) - 1):
        distancia_total += grafo[caminho_minimo[i]][caminho_minimo[i+1]]

    return caminho_minimo, distancia_total, nos_expandidos, nos_gerados
