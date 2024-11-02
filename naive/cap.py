import numpy as np
from itertools import permutations

turmas = [
    {'id': 1, 'alunos': 30},
    {'id': 2, 'alunos': 25},
    {'id': 3, 'alunos': 20},
]

salas = [
    {'id': 'A', 'capacidade': 40, 'localizacao': 'Sala A'},
    {'id': 'B', 'capacidade': 20, 'localizacao': 'Sala B'},
    {'id': 'C', 'capacidade': 30, 'localizacao': 'Sala C'},
]

distancias = np.array([
    [0, 5, 20],  
    [5, 0, 25],  
    [20, 25, 0]  
])

def alocar_turmas(turmas, salas, distancias):
    alocacao_final = {}
    custo_minimo = float('inf')
    
    id_para_indice = {sala['id']: i for i, sala in enumerate(salas)}
    
    for permutacao in permutations(turmas):
        alocacao_atual = {}
        custo_atual = 0
        salas_usadas = set() 
        
        for i, turma in enumerate(permutacao):
            turma_id = turma['id']
            alunos = turma['alunos']
            
            salas_disponiveis = [s for s in salas if s['capacidade'] >= alunos and s['id'] not in salas_usadas]
            
            if not salas_disponiveis:
                break 
            
            sala_alocada = salas_disponiveis[0]
            alocacao_atual[turma_id] = sala_alocada['id']
            salas_usadas.add(sala_alocada['id']) 
            
            if i > 0: 
                sala_anterior_id = alocacao_atual[permutacao[i - 1]['id']]
                custo_atual += distancias[id_para_indice[sala_anterior_id]][id_para_indice[sala_alocada['id']]]
    
        if custo_atual < custo_minimo:
            custo_minimo = custo_atual
            alocacao_final = alocacao_atual
    
    return alocacao_final, custo_minimo

alocacao, custo = alocar_turmas(turmas, salas, distancias)

print("Alocação das turmas nas salas:", alocacao)
print("Custo total de deslocamento:", custo)
