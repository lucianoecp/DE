import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame as df 

def de_sp(data):

	print('\nDESPACHO SEM PERDAS CONSIDERANDO OS LIMITES OPERACIONAIS:\n')

	u = data['Unid.']
	N = len(u) # NUMERO DE UNIDADES GERADORAS

	# CARGA DEMANDADA:
	PD = 1500 # (MW)

	# CURVA CARACTERISTICA:
	a = data['A']
	b = data['B']
	c = data['C']

	# lIMITES OPERACIONAIS:
	Pmin = data['Min'] # (MW)
	Pmax = data['Max'] # (MW)

	# CUSTO DE COMBUSTIVEL
	custo = data['Custo']

	# FUNÇÃO-CUSTO EM FUNÇÃO DA POTENCIA

	print('DADOS INICIAIS:\n')
	alpha = []
	beta = []
	gama = []

	for i in range (N):
		alpha.append(a[i] * custo[i])
		beta.append(b[i] * custo[i])
		gama.append(c[i] * custo[i])

		print(f'[G{i+1}]: {alpha[i]:G} + {beta[i]:G}*P{i+1} + {gama[i]:G}*P{i+1}²'.format())

	FP = np.array([[alpha],[beta],[gama]])

	Lambda = 9.0
	delp = 0.1
	delLambda = 0

	pv = []
	pvfin = []
	for i in range (N):
		pv.append(0)
		pvfin.append(0)

	while(abs(delp) >= 0.0001):
		Lambda += delLambda
		soma = 0
		totgam = 0

		p = []
		for i in range(N):
			p.append((Lambda-beta[i])/(2*gama[i]))
			soma += p[i]
			totgam += 0.5*(1/gama[i])

		delp = PD - soma
		delLambda = delp/totgam
		ifc = Lambda

	limvio = 0

	for i in range(N):
		if(p[i] < Pmin[i] or p[i] > Pmax[i]):
			limvio = 1
			break

	if (limvio == 0):
		print('\nA GERAÇÃO ESTÁ DENTRO DOS LIMITES OPERACIONAIS...\n')

	if (limvio == 1):
		soma = 0
		totgam = 0
		delp=0.1
		lolprep = 1

		while(abs(delp) >= 0.01 and lolprep == 1):
			print('\nA GERAÇÃO ESTÁ FORA DOS LIMITES OPERACIONAIS...\n')
			print('RELATORIO DA OPERAÇÃO:\n')

			if (p[i] < Pmin[i]):
				print('LIMITE DE OPERAÇÃO VIOLADO: G',i+1)
				print('LIMITE MÍNIMO: ',Pmin[i],' (MW)\tCARGA GERADA: ',p[i],'(MW)')

			elif(p[i] > Pmax[i]):
				print('LIMITE DE OPERAÇÃO VIOLADO:')
				print('LIMITE MÁXIMO: ',Pmax[i],' (MW)\tCARGA GERADA: ',p[i],'(MW)')

			soma = 0
			totgam = 0

			for i in range(N):
				pv[i] = 0

			for i in range(N):
				if(p[i] < Pmin[i] or p[i] > Pmax[i]):
					if (p[i] < Pmin[i]):
						p[i] = Pmin[i]
					else:
						p[i] = Pmax[i]

					pv[i] = 1
					pvfin[i] = 1
					break

			for i in range(N):
				soma += p[i]
				if (pvfin[i] != 1):
					totgam += 0.5*(1/gama[i])

			delp = PD - soma
			delLambda = delp/totgam
			Lambda += delLambda
			ifc = Lambda

			for i in range(N):
				if (pvfin != 1):
					p[i] = (Lambda-beta[i])/(2*gama[i])
				soma += p[i]

			delp = PD - soma
			loprep = 0;

			for i in range(N):
				if(p[i] < Pmin[i] or p[i] > Pmax[i]):
					loprep = 1
					break

	totgencost = 0

	for i in range(N):
		totgencost += (alpha[i]+beta[i]*p[i]+gama[i]*p[i]*p[i])

	print ('RESULTADO: \n')
	print('Lambda: ', Lambda,'\n')
	print ('\tUNIDADE\t\tGERAÇÃO ÓTIMA')

	for i in range(N):
		print(f'\tG{u[i]}\t\t\t{p[i]:.4F}')

	print (f'\nCUSTO DE COMBUSTIVEL INCREMENTAL {ifc:G} (Rs./MWhr):\n'.format())
	print (f'\nCUSTO TOTAL DE GERAÇÃO: {totgencost:G} (Rs./hr.)\n'.format())
























def main():

	data = pd.read_csv('input.csv')
	data.head()
	print(data)

	de_sp(data)










if __name__ == '__main__':
	main()