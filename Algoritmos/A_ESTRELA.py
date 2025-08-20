import heapq
import math
import os
import random
import time
import sys

# Converte para radianos
def converter_para_radianos(valor):
    return valor * math.pi / 180

# Calcula a heuristica haversiana
def heuristica_haversiana(grafo, vertice, destino):
    x1, y1 = grafo[vertice]
    x2, y2 = grafo[destino]
    
    x1 = converter_para_radianos(x1)
    x2 = converter_para_radianos(x2)
    y1 = converter_para_radianos(y1)
    y2 = converter_para_radianos(y2)
    
    diferenca_longitudes = y1 - x1
    diferenca_latitudes = y2 - x2
    
    formula1 = math.sin(diferenca_latitudes / 2)**2 + math.cos(x2) * math.cos(y2) * math.sin(diferenca_longitudes / 2)**2
    formula2 = 2 * math.asin(math.sqrt(formula1))
    
    raio_terra = 6371

    return raio_terra * formula2

# Calcula a heuristica euclidiana
def heuristica_euclidiana(grafo, vertice, destino):
    x1, y1 = grafo[vertice]
    x2, y2 = grafo[destino]

    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

# Função para calcular o fator de ramificação da busca A*
def fator_de_ramificação_a_estrela(grafo):
    filhos = 0
    for no in grafo:
        filhos = filhos + len(grafo[no])
    return filhos/len(grafo)

# Função para reconstruir o caminho a partir dos predecessores
def reconstruir_caminho(onde_veio, atual):
    caminho_total = [atual]
    while atual in onde_veio:
        atual = onde_veio[atual]
        caminho_total.append(atual)
    caminho_total.reverse()
    return caminho_total

def distancia_caminho(caminho, grafo):
    distancia = 0
    for i in range(len(caminho) - 1):
        distancia += grafo[caminho[i]][caminho[i + 1]]
    return distancia

def a_estrela(graph_distance, graph_coordinates, origem, destino, heuristica):
    lista_aberta = [origem]
    visitados = []
    onde_veio = {}

    valor_g = {}
    valor_f = {}
    
    # Inicializa o vértice com valores padrão
    for key in graph_distance.keys():
        valor_g[key] = float('inf')
        valor_f[key] = float('inf')
        
    # Chama a heuristica
    valor_g[origem] = 0
    valor_f[origem] = heuristica(graph_coordinates, origem, destino)


    while lista_aberta:
        atual = min(lista_aberta, key=lambda vertice: valor_f[vertice])
        visitados.append(atual)

        # Verifica se encontrou o caminho
        caminho = reconstruir_caminho(onde_veio, atual)
        if atual == destino:
            return caminho, distancia_caminho(caminho, graph_distance), len(visitados), fator_de_ramificação_a_estrela(graph_distance)

        lista_aberta.remove(atual)

        for vizinho in graph_distance[atual]:
            tentativa_valor_g = valor_g[atual] + graph_distance[atual][vizinho]

            if vizinho not in valor_g or tentativa_valor_g < valor_g[vizinho]:
                # Atualiza os custos se um caminho melhor for encontrado
                onde_veio[vizinho] = atual
                valor_g[vizinho] = tentativa_valor_g
                valor_f[vizinho] = tentativa_valor_g + heuristica(graph_coordinates, vizinho, destino)

                if vizinho not in lista_aberta:
                    lista_aberta.append(vizinho)

    return None