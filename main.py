#Projeto 01 - Logica de Computação 
#Tema: Aprendizagem de Regras para Classificação de Patologias da Coluna
#Aluno: Vinícius Peixoto Chagas
#Matricula: 20212045050533

#Declarações Iniciais
from formula import Atom, Not, And, Or, Implies
from functions import subformulas, length, atoms, number_of_atoms, number_of_connectives, is_literal, substitution
from semantics import truth_value, satisfiability_brute_force, and_all, or_all
from restrictions import r1, r2, r3, r4, r5, conj_regras, test_pacientes
atributos=[]
valor_atributos=[]
pacientes=0

# Atributos: PI: ângulo de incidência pélvica, PT: ângulo de versão pélvica, LA: ângulo de lordose,
# SS: inclinação sacral, RP: raio pélvico, GS: grau de deslizamento
#column_bin_<f>a_<n>p.csv, em que <f> é a quantidade de atributos dos pacientes e <n> é a quantidade de pacientes no arquivo
#Função Para leitura de dados, cria atributos, valor_atributos e pacientes
def ler_dados(atributos,valor_atributos,arquivo):
    import csv
    global pacientes 
    pacientes=0
    with open(arquivo,'r') as dados:
        leitor=csv.reader(dados)
        count=0
        linha=0
        for dado in leitor:
            if linha==0:
                while dado[count]!='P':
                    atributos.append(dado[count])
                    count+=1
                if dado[count]=='P':
                    atributos.append(dado[count])
                    count+=1
                linha+=1
            else:
                valor_atributos.append(dado)
                linha+=1
    pacientes=linha-1


#Define a quantidade de regras
m=1

#Executa a leitura de dados do arquivo especificado
ler_dados(atributos,valor_atributos,'Arquivos - Pacientes\column_bin_3a_3p.csv')

#Executa as restrições
f1 = r1(m, atributos)
f2 = r2(m, atributos)
f3 = r3(m, atributos, pacientes, valor_atributos)
f4 = r4(m, atributos, pacientes, valor_atributos)
f5 = r5(m, atributos, pacientes, valor_atributos)
rf = And(And(And(And(f1, f2), f3), f4), f5)

#Imprime a satisfabilidade da formula
valoracao = satisfiability_brute_force(rf)
if valoracao:
    print('\nValoração:')
    print(valoracao)

    #Imprime as atomicas verdadeiras
    res = conj_regras(valoracao, m, atributos)
    print('\n\nConjunto de regras:')
    for r in res:
        print(r)

    test = test_pacientes(valoracao, m, atributos, pacientes, valor_atributos)
    print('\nTeste dos pacientes a partir da valoracao:')

    for t in test:
        print(t)
else:
    print('\nA formula é insatisfativel ou a quantidade de regras não foi suficiente')
