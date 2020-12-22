# Pacotes utilizados:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame as df

def despacho_economico(data, pd):
    print('\nProblema: ')
    print(data)
    print(f'\npotência demanda: {pd} (MW)'.format())

    U = data['Unid.']
    N = len(U)

    alpha = data['A']
    beta = data['B']
    gama = data['C']

    custo = []
    [custo .append([i]) for i in data['Custo']]

    Pmin = data['Min']
    Pmax = data['Max']

    print('\nCurva Característica:')
    H = []
    [H.append([alpha[i], beta[i], gama[i]]) for i in range(N)]
    print(H)

    print('\nFunção-custo:')
    F = np.multiply(H,custo)
    print(F)

    a = F[:,0]
    b = F[:,1]
    c = F[:,2]

    print('\nOrganizando temos:')
    print('A: ', a)
    print('B: ', b)
    print('C: ', c)

    print('\nRELATÓRIO: ')
    desp_no_ideal_op(U,a,b,c,Pmin,Pmax,pd)



def desp_ideal_op(u,a,b,c,pmin,pmax, pd):
    print('DESPACHO ECONOMICO DESPREZANDO PERDAS E LIMITES DE OPERAÇÃO')

def desp_no_ideal_op(u,a,b,c,pmin,pmax, pd):
    print('DESPACHO ECONOMICO DESPREZANDO PERDAS E INCLUINDO LIMITES DE OPERAÇÃO')
    ng = len(u)

    # Definições iniciais:
    Lambda = 9.0
    delP = 0.1
    delL = 0.0
    Iter = 0.0

    # Calculos iniciais:
    while(abs(delP) > 0.00001):
        #print("\t\t>>While 01 erro: ", delP)
        soma = 0.0
        Lambda = Lambda + delL

        p   = np.zeros((ng,1), np.float)
        Cin = np.zeros((ng,1), np.float)

        for i in range(ng):
            p[i] = ((Lambda-b[i])/(2*c[i]))
            soma = soma + p[i]
            Cin[i] = (Lambda)
        #end_for

        delP = pd - soma # error

        # Calculo de mudança em lambda
        Den = 0

        for i in range(ng):
            Den = Den + 0.5*(1/c[i])
        #end_for

        delL = delP/Den
    #end_while

    # Verifica se algum gerador teve seus limites de operação violados:
    violado = 0 # 0 - sem violações; 1 - pelo menos uma violação.

    estado = np.zeros((ng,1), np.int) # variavel para verificar os estados de cada unidade
    # estado[unidade]: 1 => houve violação na unidade, 0 => unidade operando em regime ideal

    # Corrige a violação na geração da unidade de acordo com seus limites operacionais:
    for i in range(ng):
        if(p[i] < pmin[i] or p[i] > pmax[i]):
            violado = 1
            estado[i] = 1
            print(f'\nViolação: G{i+1}'.format())
            print(f'\nG{i+1} pretende gerar: {p[i]} (MW)...'.format())

            if(p[i] < pmin[i]):
                p[i] = pmin[i]
                print(f'Contudo, viola o limite mínimo para operação de {pmin[i]} (MW) ')

            elif(p[i] > pmax[i]):
                p[i] = pmax[i]
                print(f'Contudo, viola o limite máximo para operação de {pmax[i]} (MW) ')

            #end_if
        #end_if
    #end_for

    if(violado == 0):
        print('\nA unidades geradoras estão operando dentro dos limites operacionais...')

    delP = 0.1
    delL = 0.0
    #Den = 0.0
    Iter = 0
    soma = 0.0

    # Ajusta a geração para que não ocorra mais violação nos limites da unidade:
    while(abs(delP)>0.000000001 and violado==1):
        #print("\t\t>>While 02 erro: ", delP)
        Iter = Iter + 1
        Lambda = Lambda + delL
        soma = 0.0
        #
        Den = 0.0

        for i in range(ng):

            if(estado[i]==0):
                p[i] = (Lambda-b[i]/(2*c[i]))
                Cin[i] = Lambda
                Den = Den + 0.5*(1/c[i])
            #end_if
        #end_for

        for i in range(ng):
            soma = soma + p[i]
        #end_for

        delP = pd - soma # error

        # Calcula mundança em Lambda:
        #delL = delP/Den
        # Calculo de mudança em lambda
        #Den = 0

        #for i in range(ng):
        #    Den = Den + 0.5*(1/c[i])
        #end_for

        delL = delP/Den

    #end_while

    # Calcula o custo de combustivel incremental
    Cci = np.zeros((ng,1))
    Cop = np.zeros((ng,1))
    for i in range(ng):
        Cci[i] = b[i] + 2*c[i]*p[i]
        Cop[i] = a[i] + b[i]*p[i] + c[i]*p[i]*p[i]
    #end_for

    print('\nP: ')
    print(p)
    print('\niterações: ',Iter)
    #print('\nlambda = ', Lambda)
    print('\nCusto de combustivel incremental: ')
    print(Cci)
    print('\nCusto de operação: ')
    print(Cop)
    print('\nCusto total de operação')
    print(np.sum(Cop))

    resultado = []
    [resultado.append(p[i]) for i in range (ng)]
    resultado.append(Cci[0])
    resultado = np.array(resultado)

    print(f'\nLambda = {(resultado[-1])}\n'.format())

    print('\nResultado:')
    print(resultado)


    return resultado

def variacao_de_p(var):
    a = var

def limite_elevacao(p,pmax):
    UR = pmax - p


def limite_diminuicao(p,pmin):
    DR = p - pmin








def teste_desp(N,data):
    pd = np.random.randint(550,1550,size = N)
    print(pd)

    DE = np.array((4,N))
    for i in range(N):
        DE[:,i] = despacho_economico(data,pd[i])

    tit = str(data['Unid.'])
    val = DE
    plt.plot(tit, val)
    plt.ylim(100000, 120000)
    plt.show()

def controle_despacho(data, pd):
    ng = len(data['Unid.'])
    over = 0
    state = np.zeros((1,ng))

    cap_max = np.sum(data['Pmax'])
    cap_min = np.sum(data['Pmin'])

    if(pd>cap_max):
        print('\nDespacho restrito, a demanda é maior que a cap. máxima de operação do sistema...')
        over = pd-cap_max;
        despacho_economico(data,pd-over)
    elif(pd<cap_min):
        print('\nDespacho restrito, a demanda é mnor que a cap. minima de operação do sistema...')

        for i in range(data['Pmin']):
            if(pd>[i]):
                state[i] = 1
            else:
                state[i] = 0
    else:
        print('\nDespacho sem restrição!')


def normalize(x):
    return [(x[n] - min(x)) / (max(x) -
           min(x)) for n in range(len(x))]





if __name__ == '__main__':
    data = pd.read_csv('data/input1.csv')
    data.head()

    despacho_economico(data, 1500)

    #teste_desp(25,data)
    #exemplo = np.random.randint(50,9999,size = 3)
    #print(normalize(exemplo))

