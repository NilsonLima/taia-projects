import random
import numpy

random.seed()
TAMANHO_POPULACAO = 100
POPULACAO = []

def fitness(individuo):
	fit = 0
	erro = 0

	for i in range(0, len(individuo), 3):
			aux = individuo[i:i+3]

			for j in range(i+3, len(individuo), 3):
				aux2 = individuo[j:j+3]

				if(aux == aux2):	#mesma coluna
					erro += 1
				if( abs(i/3 - j/3) == abs(int(aux, 2) - int(aux2, 2))):	#mesma diagonal
					erro += 1
					
	fit = 1.0/(1.0+erro)

	return fit

def geraPopulacao():
	global TAMANHO_POPULACAO
	global POPULACAO
	individuo = ''

	i = 0
	while( i < TAMANHO_POPULACAO ):
		individuo = ''
		for j in range(0, 8):
			aux = bin(random.randint(0,7)).split('b')[1]
			while( len(aux) < 3 ):
				aux = '0' + aux

			individuo += aux

		ind = (individuo, fitness(individuo))

		if ind not in POPULACAO:
			POPULACAO.append(ind)
			i += 1

	return

def mutacao(ind):
	individuoMutado = ind[:]
	cuts = []

	prob =  random.randint(1, 100)
	if(prob <= 40):
		
		cuts.append(random.randint(0, 7))
		cut = cuts[0]

		while cut == cuts[0]:
			cut = random.randint(0, 7)

		cuts.append(cut)
		cuts.sort()

		individuoMutado = ind[0:cuts[0]*3] + ind[cuts[1]*3: (cuts[1]*3) + 3] + ind[(cuts[0]*3) + 3: cuts[1]*3] + ind[cuts[0]*3: (cuts[0]*3) + 3] + ind[(cuts[1]*3) + 3: 24]

	return individuoMutado

def recombinacao(pai1, pai2):
	global POPULACAO

	prob = random.randint(1, 100)
	filho1 = ''
	filho2 = ''
	posicao = 0
	if prob <= 90:
		posicao = random.randint(0, 7)
		filho1 = pai1[0][0: posicao*3] + pai2[0][posicao*3: 24]
		filho2 = pai2[0][0: posicao*3] + pai1[0][posicao*3: 24]
	
		filho1novo = mutacao(filho1)
		filho2novo = mutacao(filho2)

		ind1 = (filho1novo, fitness(filho1novo))
		ind2 = (filho2novo, fitness(filho2novo))

		if ind1 not in POPULACAO:
			POPULACAO.append(ind1)

		if ind2 not in POPULACAO:
			POPULACAO.append(ind2)
		
	return

def getKey(item):
	return item[1]

def selecaoPais():
	global POPULACAO
	pais = []

	while len(pais) < 5:
		pai = random.randint(0, 99)

		if POPULACAO[pai] not in pais: 
			pais.append(POPULACAO[pai])

	pais.sort(key = getKey)
	
	recombinacao(pais[3], pais[4])

	return

def selecaoSobreviventes():
	global POPULACAO
	offspring_size = 0

	offspring_size = len(POPULACAO) - TAMANHO_POPULACAO
	POPULACAO.sort(key = getKey)

	if offspring_size == 1: 
		POPULACAO.remove(POPULACAO[0])
	elif offspring_size == 2:
		POPULACAO.remove(POPULACAO[0])
		POPULACAO.remove(POPULACAO[1])

	return

############################## MAIN #################################
geraPopulacao()

it = 0
flag = 0
uns = 0
count = 0
for i in range(0, 10000):
#while True:
	selecaoPais()
	selecaoSobreviventes()
	it = it + 1
	#count = 0
	#for j in range(0, len(POPULACAO)):
	#	if POPULACAO[j][1] == 1.0:
	#		count = count + 1
	#if count == 92:
	#	break

pop = [float(i[1]) for i in POPULACAO]
for i in range(0, len(POPULACAO)):
	print( str(POPULACAO[i][0]) + " " + str(POPULACAO[i][1] + "\n"))
	if POPULACAO[i][1] == 1.0:
		uns = uns + 1

print("iteracoes " + str(it))
print("Convergiram " + str(uns))
print(str(numpy.mean(pop)) + " " + str(numpy.std(pop, None, None, None, 0, False)) + "\n")




