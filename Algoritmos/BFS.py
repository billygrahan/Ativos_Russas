import heapq
import math
import os
import random
import time
import sys

# Busca em Largura (BFS)

def bfs(graph_distance, origem, destino):
    cores = {}
    distancias = {}
    predecessores = {}
    
    quantidade_nos_expandidos_bfs = 0
    quantidade_filhos_bfs = 0
    
    # Inicialização dos dicionários com valores padrão
    for vertice in graph_distance.keys():
        cores[vertice] = 'Branco'
        distancias[vertice] = float('inf')
        predecessores[vertice] = None
    
    # Altera os valores do primeiro vertice
    cores[origem] = 'Cinza'
    distancias[origem] = 0
    predecessores[origem] = None

    fila_vertices = []
    fila_vertices.append(origem)

    # Inicia o BFS
    while fila_vertices != []:
        # Remove o primeiro vértice da fila
        desenfileira = fila_vertices.pop(0)
        
        quantidade_nos_expandidos_bfs += 1

        # Verifica se encontrou o destino
        if desenfileira == destino:
            break

        numero_filhos_do_vertice_bfs = 0

        # Loop com os vértices adjacentes do vértice desenfileirado
        for vertice in graph_distance[desenfileira].keys():
            # Verifica se o vértice não foi visitado
            if cores[vertice] == 'Branco':
                # Marca o vértice como visitado
                cores[vertice] = 'Cinza'
                distancias[vertice] = distancias[desenfileira] + 1
                predecessores[vertice] = desenfileira
                fila_vertices.append(vertice)
                numero_filhos_do_vertice_bfs += 1

         # Atualiza o contador de filhos do BFS
        quantidade_filhos_bfs += numero_filhos_do_vertice_bfs
        
        # O vértice e todos os seus vizinhos já foram visitados
        cores[desenfileira] = 'Preto'

    rota = []
    caminho_atual = destino

    # Começa a procurar a rota
    while caminho_atual != origem:
        caminho_atual = predecessores[caminho_atual]
        rota.append(caminho_atual)

    rota.reverse()
    rota.append(destino)

    # Calcula a distância total do caminho
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += graph_distance[rota[i]][rota[i+1]]

    return rota, distancia_total, quantidade_nos_expandidos_bfs, quantidade_filhos_bfs
