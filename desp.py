import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame as df 

def desp(data, demanda):

    print('\nDESPACHO SEM PERDAS CONSIDERANDO OS LIMITES OPERACIONAIS:\n')
    
    u = data['Unid.']
    N = len(u) # NUMERO DE UNIDADES GERADORAS
    
    # CARGA DEMANDADA:
    pd = demanda # (MW)
    
    # CURVA CARACTERISTICA:
    a = data['A']
    b = data['B']
    c = data['C']
    
    # lIMITES OPERACIONAIS:
    Pmin = data['Min'] # (MW)
    Pmax = data['Max'] # (MW)
    
    # CUSTO DE COMBUSTIVEL:
    custo = data['Custo']
    print(custo)
    
    # FUNÇÃO-CUSTO EM FUNÇÃO DA POTENCIA:
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

    # DEFINIÇÕES INICIAIS:
    Lambda = 9.0
    delP = 0.1
    delLambda = 0

    # 
    pv = np.zeros((N,i), np.byte) 
    pvf = np.zeros((N,i), np.byte)

    while(abs(delP) >= 0.0001):
        Lambda += delLambda
        soma = 0
        totGam = 0
        
        p = []
        for i in range(N):
            p.append((Lambda-beta[i])/(2*gama[i]))
            soma += p[i]
            totGam += 0.5*(1/gama[i])

        delP = (pd - soma)
        delLambda = delP/totGam
        ifc = Lambda

    limVio = 0

    for i in range(N):
        if (p[i] < Pmin[i] or p[i] > Pmax[i]):
            limVio = 1
            break
    
    if (limVio == 0):
        print('\nA GERAÇÃO ATENDE OS LIMITES OPERACIONAIS...\n')
    
    if (limVio == 1):
        soma = 0
        totGam = 0
        delP = 0.1
        loPrep = 1

        while(abs(delP) >= 0.01 and loPrep == 1):

            print('\nA GERAÇÃO ESTÁ FORA DOS LIMITES OPERACIONAIS...\n')
            print('VIOLAÇÃO APRESENTADA PELO GERADOR: ', i+1)

            if(p[i] < Pmin[i]):
                print('[ERRO]: VIOLAÇÃO DO LIMITE MÍNIMO: ', Pmin[i],' (MW)...')
            
            elif(p[i] > Pmax[i]):
                print('[ERRO]: VIOLAÇÃO DO LIMITE MÁXIMO: ', Pmax[i],' (MW)...')
            
            print(f'\n P{i+1}: {p[i]} (MW) '.format())
            
            soma = 0
            totGam = 0

            for i in range(N):
                pv[i] = 0
            
            for i in range(N):

                if (p[i]<Pmin[i] or p[i]>Pmax[i]):

                    if(p[i] < Pmin[i]):
                        p[i] = Pmin[i]

                    else:
                        p[i] = Pmax[i]
                    
                    pv[i] = 1
                    pvf[i] = 1
                    break
            
            for i in range(N):
                soma += p[i]

                if((pvf!=1).all()):
                    totGam += 0.5*(1/gama[i])
            
            delP =(pd - soma)
            delLambda = delP/totGam
            Lambda += delLambda
            ifc = delLambda

            for i in range(N):

                if((pvf!=1).all()):
                    p[i] = (Lambda - beta[i])/(2*gama[i])
            
                soma += p[i]
            
            delP  = pd - soma
            lolPrep = 0

            for i in range(N):
                if(p[i] < Pmin[i] or p[i] > Pmax[i]):
                    lolPrep = 1
                    break
    
    totgencost = 0

    for i in range(N):
        totgencost = totgencost + (alpha[i] + beta[i]*p[i] + gama[i]*p[i]*p[i])
    
    print('\nRELATÓRIO: ')
    print('\nLambda: ', Lambda)
    
    print('\nUNIDADE\tGERAÇÃO ÓTIMA\t\tLimite')
    for i in range(N):
        print(f'G{i+1} \t{p[i]:.4f}(MW)\t\t({Pmin[i]}/{Pmax[i]}) (MW)'.format())
    
    print(f'\nCUSTO INCREMENTAL DE COMBÚSTIVEL: ', ifc, ' (Rs./MWhr)\n')
    print(f'\nCUSTO TOTAL DE GERAÇÃO: ', totgencost,'\n')

    return np.array((p), dtype=float)


def main():

	data = pd.read_csv('input.csv')
	data.head()
	print(data)

	desp(data, 650)










if __name__ == '__main__':
	main()
