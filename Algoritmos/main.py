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


def memoria_alocada():
    processo = psutil.Process(os.getpid())
    return processo.memory_info().rss


def main():
    sys.setrecursionlimit(1000000)
    
    graph_distance = {}
    graph_coordinates = {}
    filepath_gr = os.path.join(os.path.dirname(__file__), "RUSSAS_MAPA_N81.gr")
    with open(filepath_gr, "r") as arquivo:
        for linha in arquivo:
            linha_dividida = linha.split()
                
            vertice_origem = int(linha_dividida[1])
            vertice_destino = int(linha_dividida[2])
            vertice_distancia = int(linha_dividida[3])
            
            if vertice_origem not in graph_distance.keys():
                graph_distance[vertice_origem] = {vertice_destino:vertice_distancia}
            else:
                graph_distance[vertice_origem][vertice_destino] = vertice_distancia
    filepath_co = os.path.join(os.path.dirname(__file__), "RUSSAS_MAPA_N81.co")
    with open(filepath_co, "r") as arquivo: 
        for linha in arquivo:        
            linha_dividida = linha.split()
            
            vertice_origem = int(linha_dividida[1])
            coordenada1 = float(linha_dividida[2])
            coordenada2 = float(linha_dividida[3])
            
            graph_coordinates[vertice_origem] = (coordenada1, coordenada2)
            
    algoritmos = ['BFS', 'DFS', 'BCU', 'A_Estrela_Euclidiano', 'A_Estrela_Haversiano']
    
    planilha = openpyxl.Workbook()
    del planilha['Sheet']
    
    for nome_planilha in algoritmos:
        planilha.create_sheet(nome_planilha)

    
    pontos = []
    for rota in range(5):
        random.seed()
        
        qtd_vertices = len(graph_coordinates)
        # Gera um par de vértices aleatórios
        origem, destino = random.sample(range(1, qtd_vertices + 1), 2)

        pontos.append((origem, destino))
        
    for nome_planilha in algoritmos:
        pagina = planilha[nome_planilha]
        pagina.sheet_format.baseColWidth = 30
        pagina.append(['Índice', 'Origem', 'Destino', 'Caminho', 'Distancia', 'Quantidade de nós expandidos', 'Fator de ramificação médio', 'Tempo', 'Memória Alocada'])

        # qtd de testes
        for test in pontos:
            row = 0
            origem = test[0]
            destino = test[1]
            
            if nome_planilha == 'BFS':
                inicio_bfs = time.time()
                memoria_antes_bfs = memoria_alocada()
                rota_bfs, distancia, quantidade_nos_expandidos_bfs, quantidade_filhos_bfs = bfs(graph_distance, origem, destino)
                memoria_depois_bfs = memoria_alocada()
                fim_bfs = time.time()

                fator_ramificacao = quantidade_filhos_bfs / quantidade_nos_expandidos_bfs
                tempo = fim_bfs - inicio_bfs
                memoria = memoria_depois_bfs - memoria_antes_bfs

                print(f"\nOrigem do Busca em Largura: {origem}")
                print(f"Destino do Busca em Largura: {destino}")
                print(f"Quantidade de nós expandidos na Busca em Largura: {quantidade_nos_expandidos_bfs}")
                print(f"Fator de ramificação médio na Busca em Largura: {fator_ramificacao}")
                print(f"Tempo de execução da Busca em Largura: {tempo}")
                print(f"Memória Alocada para a Busca em Largura: {memoria} bytes\n")
                
                pagina.append([f"{row + 1}", origem, destino, str(rota_bfs), distancia, quantidade_nos_expandidos_bfs, fator_ramificacao, tempo, memoria])
            
            if nome_planilha == 'DFS':     
                inicio_dfs = time.time()
                memoria_antes_dfs = memoria_alocada()
                rota_dfs, distancia, quantidade_nos_expandidos_dfs, quantidade_filhos_dfs = dfs(graph_distance, origem, destino)
                memoria_depois_dfs = memoria_alocada()
                fim_dfs = time.time()
                
                fator_ramificacao = quantidade_filhos_dfs / quantidade_nos_expandidos_dfs
                tempo = fim_dfs - inicio_dfs
                memoria = memoria_depois_dfs - memoria_antes_dfs

                print(f"\nOrigem do Busca em Profundidade: {origem}")
                print(f"Destino do Busca em Profundidade: {destino}")
                print(f"Quantidade de nós expandidos na Busca em Profundidade: {quantidade_nos_expandidos_dfs}")
                print(f"Fator de ramificação médio na Busca em Profundidade: {fator_ramificacao}")
                print(f"Tempo de execução da Busca em Profundidade: {tempo}")
                print(f"Memória Alocada para a Busca em Profundidade: {memoria} bytes\n")
                
                pagina.append([f"{row + 1}", origem, destino, str(rota_dfs), distancia, quantidade_nos_expandidos_dfs, fator_ramificacao, tempo, memoria])
    
            if nome_planilha == 'BCU':
                inicio_bcu = time.time()
                memoria_antes_bcu = memoria_alocada()
                rota_bcu, distancia, quantidade_nos_expandidos_bcu, quantidade_filhos_bcu = bcu(graph_distance, origem, destino)
                memoria_depois_bcu = memoria_alocada()
                fim_bcu = time.time()
                
                tempo = fim_bcu - inicio_bcu
                memoria = memoria_depois_bcu - memoria_antes_bcu

                if quantidade_filhos_bcu != 0:
                    fator_ramificacao = (quantidade_nos_expandidos_bcu - 1) / quantidade_filhos_bcu
                else:
                    fator_ramificacao = 0

                print(f"\nOrigem do Busca de Custo Uniforme: {origem}")
                print(f"Destino do Busca de Custo Uniforme: {destino}")
                print(f"Quantidade de nós expandidos na Busca de Custo Uniforme: {quantidade_nos_expandidos_bcu}")
                print(f"Fator de ramificação médio na Busca de Custo Uniforme: {fator_ramificacao}")
                print(f"Tempo de execução da Busca de Custo Uniforme: {tempo}")
                print(f"Memória Alocada para a Busca de Custo Uniforme: {memoria} bytes\n")
                
                pagina.append([f"{row + 1}", origem, destino, str(rota_bcu), distancia, quantidade_nos_expandidos_bcu, fator_ramificacao, tempo, memoria])
            
            if nome_planilha == 'A_Estrela_Euclidiano':
                inicio_a_estrela = time.time()
                memoria_antes_a_estrela = memoria_alocada()
                heuristica = a_estrela(graph_distance, graph_coordinates, origem, destino, heuristica_euclidiana) 
                rota_a_estrela, distancia_percorrida, quantidade_nos_expandidos_a_estrela, fator_ramificacao = heuristica # type: ignore
                memoria_depois_a_estrela = memoria_alocada()
                fim_a_estrela = time.time()
                
                tempo = fim_a_estrela - inicio_a_estrela
                memoria = memoria_depois_a_estrela - memoria_antes_a_estrela

                print(f"\nOrigem do A Estrela Euclidiano: {origem}")
                print(f"Destino do A Estrela Euclidiano: {destino}")
                print(f"Quantidade de nós expandidos no A Estrela Euclidiano: {quantidade_nos_expandidos_a_estrela}")
                print(f"Fator de ramificação médio no A Estrela Euclidiano: {fator_ramificacao}")
                print(f"Tempo de execução do A Estrela Euclidiano: {tempo}")
                print(f"Memória Alocada para o A Estrela Euclidiano: {memoria} bytes\n")
                
                pagina.append([f"{row + 1}", origem, destino, str(rota_a_estrela), distancia_percorrida, quantidade_nos_expandidos_a_estrela, fator_ramificacao, tempo, memoria])
                
            if nome_planilha == 'A_Estrela_Haversiano':

                inicio_a_estrela = time.time()
                memoria_antes_a_estrela = memoria_alocada()
                heuristica = a_estrela(graph_distance, graph_coordinates, origem, destino, heuristica_haversiana) 
                rota_a_estrela, distancia_percorrida, quantidade_nos_expandidos_a_estrela, fator_ramificacao = heuristica # type: ignore
                fim_a_estrela = memoria_alocada()
                destino_a_estrela = time.time()
                
                tempo = destino_a_estrela - inicio_a_estrela
                memoria = fim_a_estrela - memoria_antes_a_estrela

                print(f"\nOrigem do A Estrela Haversiano: {origem}")
                print(f"Destino do A Estrela Haversiano: {destino}")
                print(f"Quantidade de nós expandidos no A Estrela Haversiano: {quantidade_nos_expandidos_a_estrela}")
                print(f"Fator de ramificação médio no A Estrela Haversiano: {fator_ramificacao}")
                print(f"Tempo de execução do A Estrela Haversiano: {tempo}")
                print(f"Memória Alocada para o A Estrela Haversiano: {memoria} bytes\n")
                print(f"Rota encontrada: {rota_a_estrela}")
                
                pagina.append([f"{row + 1}", origem, destino, str(rota_a_estrela), distancia_percorrida, quantidade_nos_expandidos_a_estrela, fator_ramificacao, tempo, memoria])
                
            row += 1
    planilha.save('Algoritmos/Relatório.xlsx')

        
if __name__ == "__main__":
    main()