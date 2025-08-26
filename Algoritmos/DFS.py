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

    def dfs_recursivo(vertice, destino, cores, rota, distancia_acumulada):
        global quantidade_nos_expandidos_dfs
        global quantidade_filhos_dfs
        nonlocal melhor_rota, melhor_distancia
        quantidade_nos_expandidos_dfs += 1
        numero_filhos_do_vertice = 0

        cores[vertice] = "Preto"
        rota.append(vertice)

        if vertice == destino:
            if distancia_acumulada < melhor_distancia:
                melhor_distancia = distancia_acumulada
                melhor_rota = rota.copy()
            rota.pop()
            cores[vertice] = "Branco"
            return

        for novo_vertice in graph_distance[vertice]:
            if cores[novo_vertice] == "Branco":
                numero_filhos_do_vertice += 1
                dfs_recursivo(
                    novo_vertice,
                    destino,
                    cores,
                    rota,
                    distancia_acumulada + graph_distance[vertice][novo_vertice]
                )

        rota.pop()
        cores[vertice] = "Branco"
        quantidade_filhos_dfs += numero_filhos_do_vertice

    cores = {v: "Branco" for v in graph_distance.keys()}
    dfs_recursivo(origem, destino, cores, [], 0)

    return melhor_rota, melhor_distancia, quantidade_nos_expandidos_dfs, quantidade_filhos_dfs