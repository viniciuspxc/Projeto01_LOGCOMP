from formula import Atom, Not, And, Or, Implies
from functions import subformulas, length, atoms, number_of_atoms, number_of_connectives, is_literal, substitution
from semantics import truth_value, satisfiability_brute_force

#Entrada de dados
# PI, PT, LA, SS, RP, GS
#column_bin_<f>a_<n>p.csv, em que <f> é a quantidade de atributos dos pacientes e <n> é a quantidade de pacientes no arquivo
#Exemplos de teste para leitura de dados.
#Comentar ou tirar do comentario o exemplo a ser testado
"""
#Exemplo Teste1
atributos = [
    'PI<=42.09', 'PI<=70.62', 'PI<=80.61', 'GS<=37.89', 'GS<=57.55', 'P'
]
valor_atributos = [[0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 0]]
pacientes = 3
tipo = ['p', 'n', 's']
m = 4 #quantidade de regras

#Exemplo Teste2
atributos = ['PI<=42.09', 'PI<=70.62', 'GS<=37.89', 'P']
valor_atributos = [[0, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]]
pacientes = 3
tipo = ['p', 'n', 's']
m = 2 #quantidade de regras
"""
#Exemplo Teste3
atributos = ['PI<=42.09', 'PI<=70.62', 'P']
valor_atributos = [[1, 1, 0], [0, 1, 1]]
pacientes = 2
tipo = ['p', 'n', 's']
m = 1  #quantidade de regras

#Fim dos exemplos de teste


#Funções auxiliares
#Funções para criar atomicas no formato atributo/regra
def watritbuto(a, i, t):
    return Atom(a + '-' + str(i + 1) + '-' + t)


def wregra(i, j):
    return Atom('C-' + str(i + 1) + '-' + str(j + 1))


#Funções para criar and/or de multiplas formulas
def and_all(lista_formulas):
    and_formulas = lista_formulas[0]
    del lista_formulas[0]
    for formula in lista_formulas:
        and_formulas = And(and_formulas, formula)
    return and_formulas


def or_all(lista_formulas):
    or_formulas = lista_formulas[0]
    del lista_formulas[0]
    for formula in lista_formulas:
        or_formulas = Or(or_formulas, formula)
    return or_formulas


#Funções para restrições
#Restrição 1. Para cada atributo e cada regra, temos exatamente uma das três possibilidades: o atributo aparece positivamente na regra, o atributo aparece negativamente na regra ou o atributo não aparece na regra.
def r1(m, atributos):
    lista = []
    lista2 = []
    lista3 = []
    for i in range(m):
        for a in atributos:
            if a != 'P':
                lista.append(watritbuto(a, i, 'p'))
                lista.append(Not(watritbuto(a, i, 'n')))
                lista.append(Not(watritbuto(a, i, 's')))
                lista2.append(and_all(lista))
                lista.clear()

                lista.append(Not(watritbuto(a, i, 'p')))
                lista.append(watritbuto(a, i, 'n'))
                lista.append(Not(watritbuto(a, i, 's')))
                lista2.append(and_all(lista))
                lista.clear()

                lista.append(Not(watritbuto(a, i, 'p')))
                lista.append(Not(watritbuto(a, i, 'n')))
                lista.append(watritbuto(a, i, 's'))
                lista2.append(and_all(lista))
                lista.clear()

                lista3.append(or_all(lista2))
                lista2.clear()
    formula = and_all(lista3)
    return formula


#Restrição 2. Cada regra deve ter algum atributo aparecendo nela.
def r2(m, atributos):
    lista = []
    lista2 = []
    for i in range(m):
        for a in atributos:
            if a != 'P':
                lista.append(Not(watritbuto(a, i, 's')))
        lista2.append(or_all(lista))
        lista.clear()
    formula = and_all(lista2)
    return formula


#Restrição 3. Para cada paciente sem patologia e cada regra, algum atributo do paciente não pode ser aplicado à regra.
def r3(m, atributos, pacientes, valor_atributos):
    lista = []
    lista2 = []
    for j in range(pacientes):
        if valor_atributos[j][atributos.index('P')] == 0:
            for i in range(m):
                for a in atributos:
                    if a != 'P':
                        if valor_atributos[j][atributos.index(str(a))] == 1:
                            lista.append(watritbuto(a, i, 'n'))
                        else:
                            lista.append(watritbuto(a, i, 'p'))
                lista2.append(or_all(lista))
                lista.clear()
    formula = and_all(lista2)
    return formula


#Restrição 4. Para cada paciente com patologia, cada regra e cada atributo, se o atributo do paciente não se aplicar ao da regra, então a regra não cobre esse paciente.
def r4(m, atributos, pacientes, valor_atributos):
    lista = []
    lista2 = []
    for j in range(pacientes):
        if valor_atributos[j][atributos.index('P')] == 1:
            for i in range(m):
                for a in atributos:
                    if a != 'P':
                        if valor_atributos[j][atributos.index(str(a))] == 1:
                            lista.append(
                                Implies(watritbuto(a, i, 'n'),
                                        Not(wregra(i, j))))
                        else:
                            lista.append(
                                Implies(watritbuto(a, i, 'p'),
                                        Not(wregra(i, j))))
                lista2.append(and_all(lista))
                lista.clear()
    formula = and_all(lista2)
    return formula


#Restrição 5. Cada paciente com patologia deve ser coberto por alguma das regras.
def r5(m, atributos, pacientes, valor_atributos):
    lista = []
    lista2 = []
    for j in range(pacientes):
        if valor_atributos[j][atributos.index('P')] == 1:
            for i in range(m):
                lista.append(wregra(i, j))
            lista2.append(or_all(lista))
            lista.clear()
    formula = and_all(lista2)
    return formula


#Gerar conjunto de Regras
def conj_regras(valoracao, m, atributos):
    val = valoracao.copy()
    lista = []
    lista2 = []
    for i in range(m):
        for a in atributos:
            if a != 'P':
                if val[str(watritbuto(a, i, 's'))] != True:
                    if val[str(watritbuto(a, i, 'n'))] == True:
                        a2 = a.replace("<=", ">")
                        lista.append(a2)
                        #mudar <= para >
                    else:
                        lista.append(a)
        #conjunto
        #if (str(lista) + ' \u21E8 P') in lista2:
        #    lista.clear()
        #else:
        lista2.append(str(lista) + ' \u21E8 P')
        lista.clear()
    return lista2


def wpacientes(j, p):
    if p == 1:
        return ('Paciente ' + str(j + 1) + ' possui patologia.')
    else:
        return ('Paciente ' + str(j + 1) + ' não possui patologia.')


def test_pacientes(valoracao, m, atributos, pacientes, valor_atributos):
    val = valoracao.copy()
    lista = []
    lista2 = []
    for j in range(pacientes):
        for i in range(m):
            pat = 0
            for a in atributos:
                if a != 'P':
                    if val[str(watritbuto(a, i, 's'))] != True:
                        if val[str(watritbuto(a, i, 'n'))] == True:
                            a2 = a.replace("<=", ">")
                            lista.append(a2)
                            if valor_atributos[j][atributos.index(a)] == 0:
                                pat = pat + 1
                        else:
                            lista.append(a)
                            if valor_atributos[j][atributos.index(a)] == 1:
                                pat = pat + 1
            if pat == len(lista):
                if wpacientes(j, 0) in lista2:
                    lista2.remove(wpacientes(j, 0))
                    lista2.append(wpacientes(j, 1))
                elif wpacientes(j, 1) in lista2:
                    pass
                else:
                    lista2.append(wpacientes(j, 1))
            else:
                if wpacientes(j, 0) in lista2:
                    pass
                elif wpacientes(j, 1) in lista2:
                    pass
                else:
                    lista2.append(wpacientes(j, 0))
            lista.clear()
            #conjunto
    return lista2


#Executa as restrições
f1 = r1(m, atributos)
f2 = r2(m, atributos)
f3 = r3(m, atributos, pacientes, valor_atributos)
f4 = r4(m, atributos, pacientes, valor_atributos)
f5 = r5(m, atributos, pacientes, valor_atributos)

#Formula que combina as Restrições
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
    print('\n\nTeste dos pacientes a partir da valoracao:')

    for t in test:
        print(t)
else:
    print('\nA formula é insatisfativel')
