import random
import math

POPULACAO = []
DESVIOS = []
TAMANHO_POPULACAO = 1
Ps = []
C = 0.9

def fitness(individuo):
	soma1 = 0
	soma2 = 0
	n = 30.0

	for i in range(0, 30):
		soma1 += math.pow(individuo[i], 2)
		soma2 += math.cos(2.0*math.pi*individuo[i])

	return -20.0*math.exp(-0.2*math.sqrt(soma1/n)) - math.exp(soma2/n) + 20 + 1

def distriNormal (x, sigma):

	zeta = 0
	p = 1.0/(sigma*math.sqrt(2.0*math.pi))
	p = p*math.exp(-math.pow(x-zeta, 2.0)/(2.0*math.pow(sigma, 2.0)))

	return p

def evolucaoSigma(posicao):
	global C
	global Ps
	global DESVIOS

	if(Ps[posicao] > 0.2): 
		DESVIOS[posicao] = DESVIOS[posicao]*1.0/C
	elif(Ps[posicao] < 0.2):
		DESVIOS[posicao] = DESVIOS[posicao]*C
	return

def mutacao(posicao):
	global POPULACAO
	global DESVIOS
	global Ps

	success = 0
	for i in range(0, len(POPULACAO[posicao])):
		z = 0
		if(DESVIOS[posicao] > 0.0000000001):
			z = distriNormal(POPULACAO[posicao][i], DESVIOS[posicao])
		xnovo = POPULACAO[posicao][i] + z
		individuoNovo = POPULACAO[posicao][:]
		individuoNovo[i] = xnovo
		if(fitness(individuoNovo) < fitness(POPULACAO[posicao])):
			POPULACAO[posicao] = individuoNovo[:]
			success += 1

	Ps[posicao] = success*1.0/len(POPULACAO[posicao])

	#print(str(fitness(POPULACAO[posicao])) + "   " + str(DESVIOS[posicao]))

	return

def geraPopulacao():
	global TAMANHO_POPULACAO

	for i in range(0, TAMANHO_POPULACAO):
		individuoNovo = []
		for j in range(0, 30):
			individuoNovo.append(random.uniform(-15.0, 15.0))

		POPULACAO.append(individuoNovo)
		Ps.append(0.2)
		DESVIOS.append(fitness(individuoNovo)/math.sqrt(30.0))

	return

#################### MAIN ###########################

geraPopulacao()
print(fitness(POPULACAO[0]))
for i in range(0, 10000):
	evolucaoSigma(0)
	mutacao(0)

#for i in range(0, 30):
#	print(POPULACAO[0][i])

print(fitness(POPULACAO[0]))