import random
from random import shuffle
import numpy

random.seed()
TAMANHO_POPULACAO = 100
POPULACAO = []
PAIS = []

def getKey(item):
	return item[1]

def fitness2(individuo):
	vet = [0] * 8
	
	for i in range(0, len(individuo)):
		for j in range(i + 1, len(individuo)):

			if individuo[i] == individuo[j]:
				vet[i] = 1
				vet[j] = 1
			if abs(i - j) == abs(individuo[i] - individuo[j]):
				vet[i] = 1
				vet[j] = 1
	erro = 0
	for i in range(0, 8):
		if vet[i] == 1:
			erro = erro + 1
	fit = 1.0/(1.0 + erro)

	return fit

def fitness(individuo):
	fit = 0
	erro = 0

	for i in range(0, len(individuo)):
		for j in range(i + 1, len(individuo)):

			if individuo[i] == individuo[j]:
				erro += 1
			if abs(i - j) == abs(individuo[i] - individuo[j]):
				erro += 1

	fit = 1.0/(1.0 + erro)

	return fit

def geraPopulacao( ):
	global POPULACAO
	individuo = []

	while len(POPULACAO) < TAMANHO_POPULACAO:
		while len(individuo) < 8:
			gene = random.randint(0, 7)

			if gene not in individuo:
				individuo.append(gene)

		tup = (individuo, fitness(individuo))

		if tup not in POPULACAO:
			POPULACAO.append(tup)
		
		individuo = []

	return

def swap_mutation(individuo):
	cut1 = cut2 = random.randint(0, 7)

	while cut1 == cut2:
		cut2 = random.randint(0, 7)

	individuo[cut1], individuo[cut2] = individuo[cut2], individuo[cut1]

	return individuo

def insert_mutation(individuo):
	cut1 = cut2 = random.randint(0, 7)

	while cut1 == cut2:
		cut2 = random.randint(0, 7)

	if cut1 > cut2:
		cut1, cut2 = cut2, cut1

	individuoNovo = individuo[0:cut1 + 1] + [individuo[cut2]] + individuo[cut1 + 1: cut2] + individuo[cut2 + 1: 8]

	return individuoNovo

def scramble_mutation(individuo):
	cut1 = cut2 = random.randint(0, 7)
	individuoNovo = individuo[:]

	while cut1 == cut2:
		cut2 = random.randint(0, 7)

	if cut1 > cut2:
		cut1, cut2 = cut2, cut1

	while individuo == individuoNovo:
		aux = individuo[cut1:cut2 + 1]
		shuffle(aux)
		individuoNovo[cut1:cut2 + 1] = aux	

	return individuoNovo

def mutacao(individuo):
	prob = random.randint(1, 100)
	individuoNovo = individuo[:]

	if prob <= 40:
		#cabe ao projetista decidir qual tecnica de mutacao desejar operar
		#individuoNovo = swap_mutation(individuo)
		individuoNovo = insert_mutation(individuo)
		#individuoNovo = scramble_mutation(individuo)

	return individuoNovo

def loop_PMX(pai1, pai2, cut1, cut2, value):
	
	while True:
		index = pai2.index(value)
		value = pai1[index]

		index = pai2.index(value)

		if index not in range(cut1, cut2 + 1):
			break

	return index

def PMX(pai1, pai2):
	global POPULACAO
	filho = [-1] * 8
	cut1 = -1
	cut2 = -1

	while cut1 == cut2:
		cut1 = random.randint(0, 7)
		cut2 = random.randint(0, 7) 

		if cut1 > cut2:
			cut1, cut2 = cut2, cut1
			
			if cut1 == 0 and cut2 == 7:
				cut1 = cut2 = -1

	filho[cut1:cut2 + 1] = pai1[cut1:cut2 + 1]
	aux = [item for item in pai2[cut1:cut2 + 1] if item not in filho[cut1:cut2 + 1]]

	for i in range(0, len(aux)):
		filho[loop_PMX(pai1, pai2, cut1, cut2, aux[i])] = aux[i]

	for i in range(0, len(filho)):
		if filho[i] == -1:
			filho[i] = pai2[i]

	return filho

def cycle_crossover(p1, p2):
	aux = [0] * 8
	filhos = []
	cycle = []
	cycles = []
	
	pai1 = p1[:]
	pai2 = p2[:]

	for i in range(0, len(aux)):

		if aux[i] == 0:
			pos = i
			index = -1

			while index != i:
				index = pai1.index(pai2[pos])
				aux[index] = 1
				pos = index
				cycle.append(index)
		
			cycles.append(cycle)
			cycle = []

	filhos.append(pai1)
	filhos.append(pai2)

	for i in range(0, len(cycles)):
		if (i + 1) % 2 == 0:
			for j in range(0, len(cycles[i])):
				filhos[0][cycles[i][j]], filhos[1][cycles[i][j]] = filhos[1][cycles[i][j]], filhos[0][cycles[i][j]]

	return filhos

def recombinacao(pais):
	global POPULACAO

	prob = random.randint(1, 100)

	if prob <= 90:
		# cabe ao projetista decidir qual tipo de recombinacao acha mais adequada (PMX ou Cycle Crossover)
		filho1 = PMX(pais[0][0], pais[1][0])
		filho2 = PMX(pais[1][0], pais[0][0])
		filho1 = mutacao(filho1)
		filho2 = mutacao(filho2)

		#filhos = cycle_crossover(pais[0][0], pais[1][0])
		#filho1 = mutacao(filhos[0])
		#filho2 = mutacao(filhos[1])

		tup1 = (filho1, fitness(filho1))

		# print(str(pais[0][0]) + " " + str(pais[1][0]))

		# print(str(tup1))

		if tup1 not in POPULACAO:
			POPULACAO.append(tup1)

		tup2 = (filho2, fitness(filho2))

		# print(str(tup2))

		if tup2 not in POPULACAO:
			POPULACAO.append(tup2)
		
	return

def rouletteSelection(pesos, lamdba):
	global POPULACAO
	pais = []
	current_number = 1

	while current_number <= lamdba:
		rand = random.random()
		i = 0

		while pesos[i] < rand:
			i += 1

		if POPULACAO[i] not in pais:
			pais.append(POPULACAO[i])
			current_number += 1

	return pais

def roulette( ):
	global POPULACAO
	global PAIS
	prob = []
	acc_prob = []

	fn = sum(y for x, y in POPULACAO)
	prob = [f/fn for x, f in POPULACAO]

	for i in range(0, len(prob)):
		acc_prob.append(sum(prob[0:i+1]))

	pais = rouletteSelection(acc_prob, 2) #seleciona dois pais

	PAIS = pais
	recombinacao(pais)

	return

def tournament( ):
	global POPULACAO
	global PAIS
	lamdba = 2 #quantidade de pais a serem escolhidos. fica a criterio do projetista.s
	current_number = 1
	pais = []

	while current_number <= lamdba:
		pool = []

		while len(pool) < 5:
			index = random.randint(0, 99)

			if POPULACAO[index] not in pool:
				pool.append(POPULACAO[index])

		pool.sort(key = getKey)
		
		if pool[4] not in pais:
			pais.append(pool[4])
			current_number += 1

	PAIS = pais
	recombinacao(pais)

	return	

def geracional( ):
	global PAIS

	offspring_size = len(POPULACAO) - TAMANHO_POPULACAO

	if offspring_size == 1:
		PAIS.sort(key = getKey)
		POPULACAO.remove(PAIS[0])
	elif offspring_size == 2:
		for i in range(0, len(PAIS)):
			POPULACAO.remove(PAIS[i])

	return

def eliminacaoPior( ):
	global POPULACAO

	offspring_size = len(POPULACAO) - TAMANHO_POPULACAO

	POPULACAO.sort(key = getKey)

	if offspring_size == 1:
		POPULACAO.remove(POPULACAO[0])
	elif offspring_size == 2:
		POPULACAO.remove(POPULACAO[0])
		POPULACAO.remove(POPULACAO[1])

	return

def selecaoPais( ):
	roulette()  #cabe ao projetista escolher qual algoritmo de selecao de pais eh melhor
	#tournament()

	return

def selecaoSobreviventes( ):
	geracional()
	#eliminacaoPior()
	return

################################## MAIN ################################


for k in range(0, 30):
	POPULACAO = []
	geraPopulacao()

	#it = 0
	#quit = 0
	for i in range(0, 10000):
		selecaoPais()
		selecaoSobreviventes()
		#it = it + 1
		#count = 0
		#for j in range(0, len(POPULACAO)):
		#	if POPULACAO[j][1] == 1.0:
		#		quit = 1
		#if quit == 1:
		#	break
		#		count = count + 1
		#if count == 92:
		#	break
	
	#print("it " + str(it))
	#pop = [float(i[1]) for i in POPULACAO]
	#print(str(numpy.mean(pop)))
	#print(str(numpy.std(pop, None, None, None, 0, False)))
	uns = 0
	for i in range(0, len(POPULACAO)):
		if POPULACAO[i][1] == 1.0:
			uns = uns + 1
	print(str(uns))





