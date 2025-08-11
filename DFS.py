import heapq
import math
import os
import random
import time
import sys

# Busca em Profundidade (DFS)

# Branco - Vértice não visitado 
# Cinza - Vértice já foi visitado, mas seus vizinhos ainda não foram visitados
# Preto - Vértice já foi visitadoe e seus vizinhos já foram visitados

global quantidade_nos_expandidos_dfs
global quantidade_filhos_dfs

def dfs(graph_distance, origem, destino):
    global quantidade_nos_expandidos_dfs
    global quantidade_filhos_dfs

    cores = {}
    
    quantidade_nos_expandidos_dfs = 0
    
    quantidade_filhos_dfs = 0
    
    for vertice in graph_distance.keys():
        cores[vertice] = "Branco"
        
    rota = []
    
    if dfs_vizinho(graph_distance, origem, destino, cores, rota):
        return rota, quantidade_nos_expandidos_dfs, quantidade_filhos_dfs
    else:
        return rota, quantidade_nos_expandidos_dfs, quantidade_filhos_dfs
    
def dfs_vizinho(graph_distance, vertice, destino, cores, rota):
    global quantidade_nos_expandidos_dfs
    global quantidade_filhos_dfs
    
    quantidade_nos_expandidos_dfs += 1
    numero_filhos_do_vertice = 0
    
    cores[vertice] = "Preto"
    rota.append(vertice)
    
    if vertice == destino:
        return True
    
    for novo_vertice in graph_distance[vertice]:
        if cores[novo_vertice] == "Branco":
            if dfs_vizinho(graph_distance, novo_vertice, destino, cores, rota):
                return True
            
            numero_filhos_do_vertice += 1
    
    rota.pop()
    quantidade_filhos_dfs += numero_filhos_do_vertice
    
    return False