import random
import math

N = 30.0
D = math.sqrt(N + 1.0)
SIGMA = 10.0
ind = []

def initializeInd( ):
	for i in range(0, int(N)):
		ind.append(random.uniform(-15.0, 15.0))

	return

def normalDistribution( ):
	global ind
	global SIGMA
	x = []

	for i in range(0, len(ind)):
		nd = (math.e ** (-(ind[i] ** 2)/2))/(math.sqrt(2 * math.pi))
		x.append(nd)

	return [y * SIGMA for y in x]

def fitness(individual):
	soma1 = 0
	soma2 = 0
	n = 30.0

	for i in range(0, int(N)):
		soma1 += math.pow(individual[i], 2)
		soma2 += math.cos(2.0 * math.pi * individual[i])

	return -20.0 * math.exp(-0.2 * math.sqrt(soma1/n)) - math.exp(soma2/n) + 20 + 1

def ee_11(happy):
	global ind
	global SIGMA
	indNovo = []
	status = 0.0

	for i in range(0, happy):
		
		for i in range(0, len(ind)):
			indNovo.append(ind[i] + SIGMA * random.gauss(0, 1))

		fitOld = fitness(ind)
		fitNew = fitness(indNovo)

		if fitNew <= fitOld:
			status = 1.0
			ind = indNovo[:]
		else:
			status = 0.0

		SIGMA = SIGMA * math.exp(1.0/D) * (status - 0.2)
		indNovo = []

	return

################################ MAIN #######################################

initializeInd( )
# print(ind)

# for i in range(0, len(ind)):
# 	print("\n")
# 	print((-(ind[i] ** 2)/(2 * (SIGMA ** 2))))
# 	print (math.e ** (-(ind[i] ** 2)/(2 * (SIGMA ** 2))))

# print("\n")
# print(normalDistribution( ))

print (str(fitness(ind)) + " " + str(SIGMA))
ee_11(1000)
print (str(fitness(ind)) + " " + str(SIGMA))