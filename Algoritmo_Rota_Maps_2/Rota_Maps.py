import random
import copy
# pip install psutil openpyxl
import psutil
import openpyxl
import openrouteservice
import os
import time

melhor_rota = []
distancia_entre_ativos = {}
coordenadas = {}

inicio = 5
ativos = []

iteracoes = 10000

def Carrega_Dados():
    global coordenadas, ativos, inicio, distancia_entre_ativos

    filepath = os.path.join(os.path.dirname(__file__), "ATIVOS_MAP.co")
    with open(filepath, "r") as arquivo:  
        for linha in arquivo:        
            linha_dividida = linha.split()
            
            vertice_origem = int(linha_dividida[1])
            coordenada1 = float(linha_dividida[2]) 
            coordenada2 = float(linha_dividida[3]) 

            if vertice_origem != inicio:
                ativos.append(vertice_origem)
            coordenadas[vertice_origem] = (coordenada1, coordenada2)

    distancia_entre_ativos[inicio] = {}
    for ativo in ativos:
        distancia_entre_ativos[ativo] = {}
                
    

def algoritmo(origem, destino):
    global coordenadas

    origem_co = coordenadas[origem]
    destino_co = coordenadas[destino]

    if origem_co == destino_co:
        return 0

    coords = [origem_co[::-1], destino_co[::-1]]
    try:
        rota = client.directions(coords, profile='driving-car')
        distancia_metros = rota['routes'][0]['summary']['distance']
        print(f"a {origem} {destino} {distancia_metros:.0f}")

        time.sleep(2)
        
        return int(distancia_metros)
    except Exception as e:
        print(f"a {origem} {destino} ERRO: {e}")

    print("tuacha")

    return 0
    

def Roleta(roleta):
    objetos = [obj for obj, dist in roleta]
    distancias = [dist for obj, dist in roleta]

    for obj, dist in roleta:
        if dist == 0:
            return obj

    pesos = [1/(d if d > 0 else 1e-6) for d in distancias]
    total_peso = sum(pesos)
    probabilidades = [p/total_peso for p in pesos]

    escolhido = random.choices(objetos, weights=probabilidades, k=1)[0]
    return escolhido

def recalcula_distancias(melhor_rota_copia):
    global distancia_entre_ativos , inicio, ativos , graph_dist, graph_Coordenadas
    
    for i in range(len(melhor_rota_copia)-1):
        origem = melhor_rota_copia[i][0]
        destino = melhor_rota_copia[i+1][0]
        
        if destino not in distancia_entre_ativos[origem]:
            heuristica = algoritmo(origem, destino)
            distancia_percorrida= heuristica
            distancia_entre_ativos[origem][destino] = distancia_percorrida
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1] + distancia_percorrida)
        else:
            distancia_percorrida = distancia_entre_ativos[origem][destino]
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1] + distancia_percorrida)

def Gerar_Solucao():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos, melhor_rota, caminho_entre_ativos, alg, iteracoes

    melhor_rota_copia = []
    ativos_copia = ativos.copy()
    origem = inicio

    melhor_rota_copia.append((origem, 0))

    while len(ativos_copia) > 0:
        roleta = []

        for ativo in ativos_copia:
            if ativo not in distancia_entre_ativos[origem]:
                distancia= algoritmo(origem, ativo)
                distancia_entre_ativos[origem][ativo] = distancia
                roleta.append((ativo, distancia))
            else:
                roleta.append((ativo, distancia_entre_ativos[origem][ativo]))

        elemento = Roleta(roleta)

        melhor_rota_copia.append((elemento, 0))

        ativos_copia.remove(elemento)
        origem = elemento

    # Adiciona o ponto de origem ao final da rota
    if inicio not in distancia_entre_ativos[origem]:
        distancia= algoritmo(origem, inicio)
        distancia_entre_ativos[origem][inicio] = distancia
        melhor_rota_copia.append((inicio, 0))
    else:
        melhor_rota_copia.append((inicio, 0))

    recalcula_distancias(melhor_rota_copia)
    return melhor_rota_copia

def melhorar_Rota():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos, melhor_rota, caminho_entre_ativos, alg, iteracoes
    
    for i in range(iteracoes):
        melhor_rota_copia = Gerar_Solucao()

        if melhor_rota == [] or melhor_rota_copia[-1][1] < melhor_rota[-1][1]:
            melhor_rota = melhor_rota_copia
    

def carrega_teste():
    global graph_dist, graph_Coordenadas, qtd_vertices, ativos, inicio, distancia_entre_ativos, melhor_rota, caminho_entre_ativos, alg, iteracoes
    
    #algoritmos = ['BFS', 'DFS', 'BCU', 'A_Estrela_Euclidiano', 'A_Estrela_Haversiano']
    planilha = openpyxl.Workbook()
    del planilha['Sheet']
    planilha.create_sheet('openrouteservice')

    pagina = planilha['openrouteservice']
    pagina.sheet_format.baseColWidth = 30
    pagina.append(['Índice', 'Origem', 'Ativos', 'melhor_caminho', 'Distancia', 'Tempo'])
    
    for c in range(1): # qtd de testes

        random.seed(0)
        melhor_rota = []
        distancia_entre_ativos = {}

        # Inicializa as distâncias entre os ativos
        distancia_entre_ativos[inicio] = {}
        for ativo in ativos:
            distancia_entre_ativos[ativo] = {}

        inicio_tempo = time.time()
        melhorar_Rota()
        tempo_Rota = time.time() - inicio_tempo

        #print(f"{c} ; {i} = {melhor_rota[-1][1]} ; {tempo_Rota}")

        pagina.append([c, inicio, ", ".join(str(a) for a in ativos), " -> ".join(str(a[0]) for a in melhor_rota), melhor_rota[-1][1], tempo_Rota])

    planilha.save("Algoritmo_Rota_Maps_2/Ativos_Russas.xlsx")
        


if __name__ == "__main__":
    client = openrouteservice.Client(key='eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjA1Yzg4ZjM0MjY0ODQyNGViZTA3YWI0MmU1YmFlOTFkIiwiaCI6Im11cm11cjY0In0=')  # Substitua pela sua chave da API
    Carrega_Dados()
    carrega_teste()
    # Construir()

    # print("rota inicial:")
    # print(" -> ".join(str(tupla) for tupla in melhor_rota))

    # melhorar()

    # print("Melhor rota:")
    # print(" -> ".join(str(tupla) for tupla in melhor_rota))
