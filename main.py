from formula import Atom, Not, And, Or, Implies
from functions import subformulas, length, atoms, number_of_atoms, number_of_connectives, is_literal, substitution
from semantics import truth_value, satisfiability_brute_force

#Entrada de dados
# PI, PT, LA, SS, RP, GS
#column_bin_<f>a_<n>p.csv, em que <f> é a quantidade de atributos dos pacientes e <n> é a quantidade de pacientes no arquivo
#Exemplos de teste para leitura de dados.
"""
#Exemplo Teste1
atributos = [
    'PI<=42.09', 'PI<=70.62', 'PI<=80.61', 'GS<=37.89', 'GS<=57.55', 'P'
]
valor_atributos = [[0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 0]]
pacientes = 3
tipo = ['p', 'n', 's']
#quantidade de regras
m = 4
"""
#Exemplo Teste2
atributos = ['PI<=42.09', 'PI<=70.62', 'GS<=37.89', 'P']
valor_atributos = [[0, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]]
pacientes = 3
tipo = ['p', 'n', 's']
#quantidade de regras
m = 2
"""
#Exemplo Teste3
atributos = ['PI<=42.09', 'PI<=70.62', 'P']
valor_atributos = [[0, 0, 1], [0, 1, 0]]
pacientes = 2
tipo = ['p', 'n', 's']
#quantidade de regras
m = 2
"""


#Restrições
#Função para criar atomicas no formato atributo/regra
def watritbuto(a, i, t):
    #return Atom('X_' + a + '_' + str(i + 1) + '_' + t)
    return Atom(a + '-' + str(i + 1) + '-' + t)


def wregra(i, j):
    #return Atom('C_' + str(i + 1) + '_' + str(j + 1))
    return Atom('C-' + str(i + 1) + '-' + str(j + 1))


#Restrição 1.
def r1():
    lista = []
    lista2 = []
    lista3 = []
    for i in range(m):
        for a in atributos:
            if a != 'P':
                """for t in tipo:
                    lista.append(watritbuto(a, i, t))
                lista2.append(or_all(lista))
                lista.clear()"""

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


#Restrição 2.
def r2():
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


#Restrição 3.
def r3():
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


#Restrição 4.
def r4():
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


#Restrição 5.
def r5():
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


#Funções
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


#Executa as restrições
f1 = r1()
f2 = r2()
f3 = r3()
f4 = r4()
f5 = r5()

#Imprime as restrições
print('\n\nRestrição 1: ' + f1)
print('\n\nRestrição 2: ' + f2)
print('\n\nRestrição 3: ' + f3)
print('\n\nRestrição 4: ' + f4)
print('\n\nRestrição 5: ' + f5)

#Formula que combina as Restrições
rf = And(And(And(And(f1, f2), f3), f4), f5)

#Imprime a satisfabilidade da formula
print(satisfiability_brute_force(rf))

#Imprime as Atomicas
""" 
print('\n\nAtomicas:\n')
for x in atoms(rf):
    print(x)
"""
