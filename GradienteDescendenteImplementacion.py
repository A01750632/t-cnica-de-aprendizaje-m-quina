from re import X
import numpy as np

def read():
    variables = []
    variablesNum = []
    with open('inputs2.txt') as file:
        for line in file:
            variables.append(line.rstrip().split(','))
    for i in variables:
        res = [eval(x) for x in i]
        variablesNum.append(res)
    variablesNum = np.array(variablesNum)
    variablesNum = variablesNum.transpose()
    np.random.shuffle(variablesNum)
    PorcentajeTest = float(input('Porcentaje de registros test: '))/100
    #PorcentajeTest = 50/100
    registrosTrainNum = round(len(variablesNum) * PorcentajeTest)
    registrosTrain = variablesNum[0:registrosTrainNum]
    registrosTest = variablesNum[registrosTrainNum:]
    registrosTest = registrosTest.transpose()
    registrosTrain = registrosTrain.transpose()
    xVariablesTrain = registrosTrain[0:-1]
    xVariablesTrain = xVariablesTrain.transpose()
    xVariablesTest = registrosTest[0:-1]
    xVariablesTest = xVariablesTest.transpose()
    PesosIniciales = float(input('Qué peso quieres usar como inicial: '))
    alpha = float(input('Qué alpha quieres usar: '))
    Epocas = int(input('Cuntas epocas quieres: '))
    accuracyUsuario = float(input('cuanta accuracy te gustaría tener en consideracion: '))/100
    #PesosIniciales = 0.1
    #alpha = 0.000001
    #Epocas = 100
    pesos = np.full((xVariablesTrain.shape[1]), PesosIniciales)
    tTrain = registrosTrain[-1]
    tTest = registrosTest[-1]
    calculaO(pesos,xVariablesTrain,tTrain,alpha,xVariablesTest,tTest,Epocas,accuracyUsuario)

def calculaO(pesos,xVariablesTrain,variablesNum,alpha,xVariablesTest,tTest,Epocas,accuracyUsuario):
    o = []
    for i in range(len(xVariablesTrain)):
        o.append(np.sign(np.dot(xVariablesTrain[i], pesos)))
    o = np.array(o)
    EpocasCount = 0
    accuracy = 0
    dictpesos = dict()
    if str(pesos) not in dictpesos:
        dictpesos[str(pesos)] = 1
    while((accuracy < accuracyUsuario or np.array_equal(variablesNum, o, equal_nan=False)== False) and dictpesos[str(pesos)] < 20 and EpocasCount < Epocas): 
        #while(np.array_equal(variablesNum, o, equal_nan=False)== False):
        print("\nNo iguales Calculando....")
        print(f'{"O calculada":=^50}')
        print('Este es o: '+ str(o))
        print(f'{"Pesos usados para calcular o":=^50}')
        print(pesos)
        print(f'{"T":=^50}')
        print('Este es T: '+ str(variablesNum))
        pesos = calculaW(variablesNum,alpha,o,xVariablesTrain,pesos)
        o = []
        for i in range(len(xVariablesTrain)):
            oCalculada = (np.sign(np.dot(xVariablesTrain[i], pesos)))
            if (oCalculada == 0.0):
                oCalculada =1
            o.append(int(oCalculada))
        o = np.array(o)
        EpocasCount += 1
        accuracy,oFinal = CalculaPresicion(xVariablesTest,pesos,tTest)
        if str(pesos) not in dictpesos:
            dictpesos[str(pesos)] = 1
        else:
            dictpesos[str(pesos)] = dictpesos[str(pesos)] + 1
        
    print("\nIguales")
    print(f'{"Tarining: O calculada":=^50}')
    print('Este es o: '+ str(o))
    print(f'\n{"Training: T del Input":=^50}')
    print('Este es t del archivo input: '+ str(variablesNum))
    print(f'\n{"Pesos Finales veces repetidos":=^50}')
    print(f'pesos repetidos: {pesos} = {dictpesos[str(pesos)]}')
    print(f'\n{"Pesos diccionario":=^50}')
    print(f'{dictpesos}')
    print(f'\n{"Resultados Finales":=^50}')
    print(f'O calculada: {oFinal}    t de Output {tTest}     Pesos Usados {pesos}     accuracy {accuracy},     Epocas {EpocasCount}')
    #print('Estos son los pesos: '+ str(pesos))

def calculaW(t,alpha,o,listaX,listaW):
    for i in range(len(listaX)):
        listaW = listaW+alpha*(t[i]-o[i])*listaX[i]
    return listaW

def CalculaPresicion(xVariablesTest,pesos,tTest):
    o = []
    for i in range(len(xVariablesTest)):
        oCalculada = (np.sign(np.dot(xVariablesTest[i], pesos)))
        if (oCalculada == 0.0):
            oCalculada =1
        o.append(int(oCalculada))
    np.array(o)
    accuracy = (o == tTest).sum()/len(tTest)
    print(f'{"Accuracy":=^50}')
    print(accuracy)
    return accuracy,o

def main():
    read()

main()
