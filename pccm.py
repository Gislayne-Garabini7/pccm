#Feito pelas alunas Gislayne Garabini Damasceno e Maryana S. Catonho

import sys

#Define o infinito como sugerido (2 · 10^9)
INFINITO = 2 *(10**9)

def ler_grafo(nome_arquivo):
    f = open(nome_arquivo, 'r')
    linha = f.readline().strip() #Lê a primeira linha e remove espaços em branco

    #Verifica se a linha é do tipo 'I'
    if len(linha) == 0 or linha[0] != 'I':
        return None, None, None
    
    #Divide a string da linha lida em partes separadas por espaço e coloca em uma lista
    partes = linha.split()
    if len(partes) != 3:
        return None, None, None

    n = int(partes[1])
    m = int(partes[2])
    grafo = [[] for _ in range(n)]

    #Leitura do restante do arquivo
    for linha in f:
        linha = linha.strip()
        if len(linha) == 0:
            continue

        tipo = linha[0]

        if tipo == 'T':
            break
        elif tipo == 'N':
            continue
        elif tipo == 'E':
            partes = linha.split()
            if len(partes) != 4:
                return None, None, None
            u = int(partes[1])
            v = int(partes[2])
            c = int(partes[3])
            if u < 0 or u >= n or v < 0 or v >= n:
                return None, None, None
            grafo[u].append((v, c))

    f.close()
    return grafo, n, m

#Executa o algoritmo de Bellman-ford com as devidas alterações
def pccm(grafo, n, origem):
    distancia = [INFINITO] * n
    anterior = [-1] * n
    distancia[origem] = 0

    #Cria as ordens crescente e decrescente a partir do vértice de origem
    OI = [origem] + [v for v in range(n) if v != origem]
    OP = [origem] + [v for v in reversed(range(n)) if v != origem]

    #Impremi as ordens 
    print("O I", ' '.join(map(str, OI)))
    print("O P", ' '.join(map(str, OP)))

    k = 0
    for rodada in range(1, n):
        k = rodada
        #Alterna a ordem das rodadas entre OI e OP
        if rodada % 2 == 1:
            O = OI
        else:
            O = OP

        atualizacao = False #Pra saber se na rodada teve atualização

        for u in O:
            for v, custo in grafo[u]:
                if distancia[u] + custo < distancia[v]:
                    distancia[v] = distancia[u] + custo
                    anterior[v] = u
                    atualizacao = True

        if not atualizacao:
            break

    #Impressão do estado final
    print(f"F {k}")
    print("D", ' '.join([str(d if d < INFINITO else "-" ) for d in distancia]))
    print("A", ' '.join([str(a if a != -1 else "-") for a in anterior]))

    #Possui ciclo negativo?
    for u in range(n):
        for v, custo in grafo[u]:
            if distancia[u] + custo < distancia[v]:
                print("CN")
                return

    #Imprime caminho mínimos da origem aos outros vértices
    for t in range(n):
        if distancia[t] >= INFINITO:
            print(f"U {t}") #Vértice inatingível
        else:
            caminho = reconstrui_caminho(anterior, origem, t)
            custo = distancia[t]
            tamanho = len(caminho)
            print(f"P {t} {custo} {tamanho} {' '.join(map(str, caminho))}")

#Rencontroi o caminho de s até t usando o vetor anterior
def reconstrui_caminho(anterior, origem, destino):
    caminho = []
    atual = destino
    while atual != -1:
        caminho.insert(0, atual)
        atual = anterior[atual]
    if len(caminho) == 0 or caminho[0] != origem:
        return [] #Não tem caminho que é válido
    return caminho

#Trata os argumentos da linha de comando e inicia o algoritmo
def main():
    if len(sys.argv) != 3:
        print("E") 
        return

    nome_arquivo = sys.argv[1]
    s = sys.argv[2]

    if not s.isdigit():
        print("E") 
        return

    origem = int(s)

    grafo, n, m = ler_grafo(nome_arquivo)
    if grafo is None or origem < 0 or origem >= n:
        print("E") #Erro ao ler o grafo ou a origem está errada
        return

    pccm(grafo, n, origem)

if __name__ == "__main__":
    main()
