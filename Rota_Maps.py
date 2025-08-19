import random
import copy
# pip install psutil openpyxl
import psutil
import openpyxl
import openrouteservice


melhor_rota = []
distancia_entre_ativos = {}

coordenadas = {}

inicio = 5
ativos = []

#alg = 'A_Estrela_Haversiano' 
iteracoes = 10000

def Carrega_Dados():
    global coordenadas, ativos, inicio, distancia_entre_ativos

    with open("ATIVOS_MAP.co", "r") as arquivo:  
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

    coords = [origem_co[::-1], destino_co[::-1]]
    rota = client.directions(coords, profile='driving-car')

    # Distância em metros
    distancia_metros = rota['routes'][0]['summary']['distance']
    return int(distancia_metros)

def Construir():
    global melhor_rota, distancia_entre_ativos , inicio, ativos

    melhor_rota = [(inicio, 0)]
    
    caminho_inicial = random.sample(ativos, len(ativos))

    for i in range(len(caminho_inicial)):
        if i == 0:
            distancia = 0
            melhor_rota.append((caminho_inicial[i], distancia))
            distancia_entre_ativos[inicio][caminho_inicial[i]] = distancia
        elif caminho_inicial[i] == melhor_rota[-1][0]:
            melhor_rota.append((caminho_inicial[i], melhor_rota[-1][1]))
        else:
            heuristica = algoritmo(caminho_inicial[i-1], caminho_inicial[i])
            distancia = heuristica
            melhor_rota.append((caminho_inicial[i], melhor_rota[-1][1] + distancia))
            distancia_entre_ativos[caminho_inicial[i-1]][caminho_inicial[i]] = distancia
        
    heuristica = algoritmo(caminho_inicial[i-1], inicio)
    distancia = heuristica
    melhor_rota.append((inicio, melhor_rota[-1][1] + distancia))
    distancia_entre_ativos[caminho_inicial[i-1]][inicio] = distancia

    
def recalcula_distancias(melhor_rota_copia):
    global distancia_entre_ativos , inicio, ativos

    for i in range(len(melhor_rota_copia)-1):
        origem = melhor_rota_copia[i][0]
        destino = melhor_rota_copia[i+1][0]

        if origem == destino:
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1])
        elif destino not in distancia_entre_ativos[origem]:
            heuristica = algoritmo(origem, destino)
            distancia_percorrida = heuristica
            distancia_entre_ativos[origem][destino] = distancia_percorrida
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1] + distancia_percorrida)
        else:
            distancia_percorrida = distancia_entre_ativos[origem][destino]
            melhor_rota_copia[i+1] = (destino, melhor_rota_copia[i][1] + distancia_percorrida)
    

def Roleta():
    global melhor_rota, distancia_entre_ativos , inicio, ativos

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
    global melhor_rota, distancia_entre_ativos , inicio, ativos, coordenadas

    for _ in range(iteracoes):
        melhor_rota_copia = Roleta()
        if melhor_rota_copia[-1][1] < melhor_rota[-1][1]:
            melhor_rota = melhor_rota_copia

        


if __name__ == "__main__":
    client = openrouteservice.Client(key='KEY_AQUI')  # Substitua pela sua chave da API
    Carrega_Dados()

    Construir()

    print("rota inicial:")
    print(" -> ".join(str(tupla) for tupla in melhor_rota))

    melhorar()

    print("Melhor rota:")
    print(" -> ".join(str(tupla) for tupla in melhor_rota))
