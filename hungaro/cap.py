import numpy as np

def checar_matriz_quadrada(matriz_custo: np.array) -> bool:
    return matriz_custo.shape[0] == matriz_custo.shape[1]

def subtrair_mínimos(matriz_custo: np.array) -> np.array:
    # passso 1 e 2 do método hungaro: subtrai o menor valor de cada linha e coluna
    #de todos os valores das respectivas linhas / colunas
    matriz_custo -= matriz_custo.min(axis=1).reshape(-1,1)
    matriz_custo -= matriz_custo.min(axis=0)
    return matriz_custo

def matriz_boleana(matriz_custo: np.array) -> np.array:
    #retorna matriz boleana com valor true onde há zeros e false no resto
    return matriz_custo == 0   

def encontrar_numero_minimo_de_zeros(matriz_boleana: np.array, matriz_indices: np.array) -> None:
    #percorre toda matriz boleana de zeros retornando a matriz boleana corrigida e o número mínimo de zeros para cada iteração 
    linha_min = [np.inf, -1]
    for numero_linha in range(len(matriz_boleana)):
        numero_zeros = np.sum(matriz_boleana[numero_linha])
        if numero_zeros > 0 and numero_zeros < linha_min[0]:
            linha_min = [numero_zeros, numero_linha]
   
    indice_zero = np.where(matriz_boleana[linha_min[1]])[0][0]
    matriz_indices.append((linha_min[1], indice_zero))
    matriz_boleana[linha_min[1], :] = False
    matriz_boleana[:, indice_zero] = False

def teste_de_otmizacao(matriz_custo: np.array) -> np.array:
    matriz_boleana_de_zeros = matriz_boleana(matriz_custo)
    matriz_boleana_de_zeros_cp = matriz_boleana_de_zeros.copy()
    
    matriz_linhas_marcadas = []
    while np.any(matriz_boleana_de_zeros_cp): 
        encontrar_numero_minimo_de_zeros(matriz_boleana_de_zeros_cp, matriz_linhas_marcadas)
    #gravando as posições de linhas e colunas com possíveis zero
    linhas_com_zero = [linha for linha, _ in matriz_linhas_marcadas] 
    linhas_sem_zeros = list(set(range(matriz_custo.shape[0])) - set(linhas_com_zero))
    # Gravar colunas com zero.
    colunas_marcadas = []
    while True:
        controle = False
        for linha in linhas_sem_zeros:
            for col, zeros in enumerate(matriz_boleana_de_zeros[linha]):
                if zeros and col not in colunas_marcadas:
                    colunas_marcadas.append(col)
                    controle = True

        for numero_linha, numero_coluna in matriz_linhas_marcadas:
            if numero_linha not in linhas_sem_zeros and numero_coluna in colunas_marcadas:
                linhas_sem_zeros.append(numero_linha)
                controle = True

        if not controle:
            break
# Marcar linhas com zeros
    linhas_marcadas = list(set(range(matriz_custo.shape[0])) - set(linhas_sem_zeros))
    return matriz_linhas_marcadas, linhas_marcadas, colunas_marcadas

def ajuste_de_otmizacao(matriz_custo: np.array, linhas_para_ajustar: np.array, colunas_para_ajustar: np.array) ->np.array:   
    matriz_custo_cp = matriz_custo.copy()
    
    # Encontrar o valor mínimo de um elemento que não esteja em uma linha/coluna marcada
    elmementos_nao_zerados = [matriz_custo_cp[linha, coluna] for linha in range(len(matriz_custo_cp))
                         if linha not in linhas_para_ajustar for coluna in range(len(matriz_custo_cp[linha]))
                         if coluna not in colunas_para_ajustar]
    numero_minimo = min(elmementos_nao_zerados)

    # Subtrair o valor mínimo de todos os valores que não estão em uma linha/coluna marcada
    for linha in range(len(matriz_custo_cp)):
        if linha not in linhas_para_ajustar:
            for coluna in range(len(matriz_custo_cp[linha])):
                if coluna not in colunas_para_ajustar:
                    matriz_custo_cp[linha, coluna] -= numero_minimo

    # Adicionar o valor mínimo a todos os valores em linhas/colunas marcadas
    for linha in linhas_para_ajustar:
        for coluna in colunas_para_ajustar:
            matriz_custo_cp[linha, coluna] += numero_minimo

    return matriz_custo_cp

def algoritmo_hungaro(matriz_custo: np.array):
    assert checar_matriz_quadrada(matriz_custo)
    matriz_operacao = subtrair_mínimos(matriz_custo)
    dimensao_matriz = matriz_operacao.shape[0] # condição de otmização: menor numero de linhas + colunas unicas com zero = n
    contador = 0
    while contador < dimensao_matriz:
        linhas_menor_custo, linhas_marcadas, colunas_marcadas = teste_de_otmizacao(matriz_operacao)
        contador = len(linhas_marcadas) + len(colunas_marcadas)
        if contador < dimensao_matriz:
            matriz_operacao = ajuste_de_otmizacao(matriz_operacao, linhas_marcadas, colunas_marcadas)     
    return matriz_operacao, linhas_menor_custo

def calcular_custo(matriz_custo: np.array, indice_menor_custo: np.array) -> None:
    total = 0
    for i in range(len(matriz_custo)):
        total += matriz_custo[indice_menor_custo[i][0], indice_menor_custo[i][1]]
    print(f"Custo total {total}")


def main():
    
    matriz_teste = np.array([
    [0, 5, 20],  
    [5, 0, 25],  
    [20, 25, 0]
    ])  

    #usando valores de: http://sbemparana.com.br/arquivos/anais/epremxii/ARQUIVOS/MINICURSOS/autores/MCA016.pdf
    #para validar o algoritmo
    matriz_teste_2 = np.array([
    [90, 75, 75, 80],  
    [35, 85, 55, 65],  
    [125, 95, 90, 105],
    [45, 110, 95, 115]
    ])  
    
    #precisa da copia para o algoritmo n sobreescrever a matriz
    matriz_operacional = matriz_teste_2.copy()
    matriz_final, menor_custo = algoritmo_hungaro(matriz_operacional)
    print(f"Matriz de otimização: \n {matriz_final} \n")

    calcular_custo(matriz_teste_2, menor_custo)

if __name__ =="__main__":
    main()