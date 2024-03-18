from Professor import Professor
from Individuo import Individuo
from cProfile import label 
import random 
import copy
import matplotlib.pyplot as plt


#parametros globais 

solucao = []
solucao_fitness = 0 
solucao_index = 0
condicao_de_parada = True 
generation = 0
media_selection, media_crossover, media_mutation, melhores = [],[],[],[]

# Dados de entrada 

turmas = 8
aulas_por_dia = 4 
populacao = []
professores = []

for _ in range(0, 100):
    professores.append(Professor("Natan", "Geografia", 2))
    professores.append(Professor("Emerson", "História", 2))
    professores.append(Professor("Camila", "Português", 4))
    professores.append(Professor("Jorge", "Português", 4))
    professores.append(Professor("Clara", "Ciências", 2))
    professores.append(Professor("Carlos", "Educação Física", 2))
    professores.append(Professor("Maria", "Artes", 1))
    professores.append(Professor("Ana", "Ensino Religioso", 1))
    professores.append(Professor("Evelyn", "Matemática", 4))
    professores.append(Professor("Marcondes", "Matemática", 4))
    professores.append(Professor("Marta", "Inglês", 1))
    professores.append(Professor("Alenka", "Espanhol", 1))


# Retorna o score maximo e minimo 

def inicializar_grade(pop_professores):
       for n in pop_professores :
           n.grade = aulas_por_dia * 5

inicializar_grade(professores)

for professor in professores:
    print("Nome:", professor.nome)
    print("Disciplina:", professor.disciplina)
    print("Aulas por Turma:", professor.aulas_por_turma)
    print("Grade:", professor.grade)
    print("-----")
def max_min (populacao) : 
    menor,maior = 100000,0

    for individuo in populacao : 
        value = individuo.aptidao

        if value > maior :
            maior = value 
        elif value < menor :
            menor = value
    
    return menor,maior

def calcular_media (populacao,vetor) : 
    total = 0 

    for individuo in populacao : 
        total += individuo.aptidao
    
    vetor.append(total/len(populacao))


def buscar_melhor_ind (populacao) : 
    max = 0 
    for n in range (len(populacao)) : 
        aux = populacao[n].aptidao

        if aux > max :
            max = aux 
            solucao_index = n
    return solucao_index, max

def selection (populacao) : 
    nova_populacao = []
    soma_total = []
    probabilidade = []

    for individuo in populacao :
        soma_total += individuo.aptidao
    
    for individuo in populacao :
        probabilidade.append(individuo.aptidao/soma_total)
    
    index, temp = buscar_melhor_ind(populacao)

    for n in range (0,len(populacao)) : 
        if n < 10 :
            nova_populacao.append(copy.deepcopy(populacao[index]))
        else : 
            aux = 0 
            num = random.uniform(0,1)

            for i  in range (0,len(probabilidade)) : 
                aux += probabilidade[i]

                if num <= aux : 
                    nova_populacao.append(copy.deepcopy(populacao[i]))
                    break
    del populacao
    del probabilidade
    return nova_populacao

def crossover (populacao) : 
    for index, individuo in enumerate (populacao) : 

        if index > 0 :
            num = random.uniform(0,1)
            
            if num > 0.5 :
                parceiro = int (random.uniform(0,len(populacao) - 1))

                for n in range (0, int( len (individuo.professores)/2)) : 
                    aux = copy.deepcopy(individuo.professores[n].grade)
                    individuo.professores[n].grade = copy.deepcopy(populacao[parceiro].professores[n].grade)
                    populacao[parceiro].professores[n].grade = copy.deepcopy(aux)

                    del aux 


def mutation (populacao) : 
    for index,individuo in enumerate(populacao) : 
        if index > 0 :
            rng = random.uniform(0,1)

            if rng > 0.25 :
                professor = individuo.professores[int(random.uniform(0, len(individuo.professores)))]
                horario1 = int(random.uniform(0,len(professor.grade)))
                horario2 = int(random.uniform(0,len(professor.grade)))
                aux = professor.grade[horario1]
                professor.grade[horario1] = professor.grade[horario2]
                professor.grade[horario2] = professor.grade[aux]

                del aux





# método que torna o algoritmo híbrido
def solve(solucao):
    turmas = len(solucao.professores[0].grade)
    counter = []
    
    for _ in range(turmas):
        count = [0 for _ in range(turmas)]
        counter.append(count)

    for n in range(len(solucao.professores[0].grade)):
        for m in range(len(solucao.professores)):
            if solucao.professores[m].grade[n] != 0:
                counter[n][solucao.professores[m].grade[n] - 1] += 1

    for n in range(len(counter)):
        for m in range(len(counter[n])):
            if counter[n][m] > 1:
                for i in range(len(counter)):
                    if counter[i][m] == 0:
                        for r in range(len(solucao.professores)):
                            if solucao.professores[r].grade[n] == m + 1:
                                aux = solucao.professores[r].grade[n]
                                solucao.professores[r].grade[n] = solucao.professores[r].grade[i]
                                solucao.professores[r].grade[i] = aux
                                break
                        break




offset = 0

for professor in professores:
    limit = 0
    if professor.aulas_por_turma * turmas > aulas_por_dia * 5:
        limit = int(turmas / 2)
    else:
        limit = turmas
    janelas = (aulas_por_dia * 5) - (professor.aulas_por_turma * limit)
    professor.grade = [-1 for _ in range(aulas_por_dia * 5)]
    count = 1
    for i in range(offset, limit + offset):
        professor.grade[i] = count
        count += 1
    for n in range(aulas_por_dia * 5):
        if n < offset or n >= limit + offset:
            while True:
                num = random.randint(0, limit)
                if num != 0 and professor.grade.count(num) < professor.aulas_por_turma:
                    professor.grade[n] = num
                    break
                elif num == 0 and professor.grade.count(num) < janelas:
                    professor.grade[n] = num
                    break
            offset += 1
    discp = " "
    for n in range(len(professores)):
        if n == 0:
            discp = professores[0].disciplina
        else:
            if professores[n].disciplina == discp:
                for m in range(0, (aulas_por_dia * 5)):
                    if professores[n].grade[m] != 0:
                        professores[n].grade[m] += int(turmas / 2)
                discp = professores[n].disciplina
    populacao.append(Individuo(professores))
    professores.clear()

for professor in populacao[0].professores:
    print(professor.grade)
    print("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−")

for individuo in populacao:
    individuo.fitnessEvaluation(turmas)

while generation < 7000:
    populacao_aux = selection(populacao)
    populacao.clear()
    populacao = copy.deepcopy(populacao_aux)
    populacao_aux.clear()
    calcular_media(populacao, media_selection)
    crossover(populacao)
    mutation(populacao)
    for individuo in populacao:
        individuo.fitnessEvaluation(turmas)
    generation += 1
    r, value = buscar_melhor_ind(populacao)
    melhores.append(value)
    if value > solucao_fitness:
        print(value)
        solucao = copy.deepcopy(populacao[r])
        solucao_fitness = value
    if solucao_fitness == 7000:
        break

for professor in solucao.professores:
    print(professor.grade)
print(generation)

x = []
for n in range(len(media_selection)):
    x.append(n)
plt.plot(x, media_selection, label="Selection")
plt.plot(x, melhores, label="Melhor")
plt.legend()
plt.show()
