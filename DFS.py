import heapq
import math
import os
import random
import time
import sys

# Branco - Vértice não visitado 
# Cinza - Vértice já foi visitado, mas seus vizinhos ainda não foram visitados
# Preto - Vértice já foi visitadoe e seus vizinhos já foram visitados

def dfs(graph_distance, origem, destino):
    cores = {}
    
    global quantidade_nos_expandidos_dfs
    quantidade_nos_expandidos_dfs = 0
    
    global quantidade_filhos_dfs
    quantidade_filhos_dfs = 0
    
    # Inicializa cada vértice com o valor branco
    for vertice in graph_distance.keys():
        cores[vertice] = "Branco"
        
    rota = []
    
    # Inicia a busca pela origem
    if dfs_vizinho(graph_distance, origem, destino, cores, rota):
        return rota
    
def dfs_vizinho(graph_distance, vertice, destino, cores, rota):
    global quantidade_nos_expandidos_dfs
    quantidade_nos_expandidos_dfs += 1
    
    global quantidade_filhos_dfs
    numero_filhos_do_vertice = 0
    
    # Vértice é visitado, marcado como Preto e adicionado a rota
    cores[vertice] = "Preto"
    rota.append(vertice)
    
    # Verifica se encontrou o destino
    if vertice == destino:
        return True
    
    # Loop com os vértices adjacentes do vértice atual
    for novo_vertice in graph_distance[vertice]:
        # Verifica se ainda não foi visitado
        if cores[novo_vertice] == "Branco":
            # Explora o novo vértice
            if dfs_vizinho(graph_distance, novo_vertice, destino, cores, rota):
                return True
            
            numero_filhos_do_vertice += 1
    
    # Remove o vértice da rota quando o caminho não é encontrado
    rota.pop()
    quantidade_filhos_dfs += numero_filhos_do_vertice
    
    return False