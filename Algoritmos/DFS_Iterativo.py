import heapq
import math
import os
import random
import time
import sys

global quantidade_nos_expandidos_dfs
global quantidade_filhos_dfs

def dfs(graph_distance, origem, destino):
    global quantidade_nos_expandidos_dfs
    global quantidade_filhos_dfs

    quantidade_nos_expandidos_dfs = 0
    quantidade_filhos_dfs = 0

    melhor_rota = None
    melhor_distancia = float('inf')

    # Pilha: cada elemento é (vertice_atual, rota_atual, distancia_acumulada, cores_atual)
    pilha = [(origem, [origem], 0, {v: "Branco" for v in graph_distance.keys()})]

    while pilha:
        vertice, rota, distancia_acumulada, cores = pilha.pop()
        quantidade_nos_expandidos_dfs += 1

        if vertice == destino:
            if distancia_acumulada < melhor_distancia:
                melhor_distancia = distancia_acumulada
                melhor_rota = rota.copy()
            continue

        cores_local = cores.copy()
        cores_local[vertice] = "Preto"

        filhos = 0
        for novo_vertice in graph_distance[vertice]:
            if cores_local[novo_vertice] == "Branco" and novo_vertice not in rota:
                filhos += 1
                nova_rota = rota + [novo_vertice]
                nova_distancia = distancia_acumulada + graph_distance[vertice][novo_vertice]
                pilha.append((novo_vertice, nova_rota, nova_distancia, cores_local))
        quantidade_filhos_dfs += filhos

    return melhor_rota, melhor_distancia, quantidade_nos_expandidos_dfs, quantidade_filhos_dfs