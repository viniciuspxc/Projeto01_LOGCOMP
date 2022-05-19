from formula import Atom, Not, And, Or, Implies
from functions import subformulas, length, atoms, number_of_atoms, number_of_connectives, is_literal, substitution
from semantics import truth_value, satisfiability_brute_force

#Entrada de dados
# PI, PT, LA, SS, RP, GS
#column_bin_<f>a_<n>p.csv, em que <f> é a quantidade de atributos dos pacientes e <n> é a quantidade de pacientes no arquivo
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


#Restrições
#Escreve a atomica no formato do atributo
def watritbuto(a, i, t):
    return Atom('X_' + a + '_' + str(i + 1) + '_' + t)


def r1():
    lista = []
    lista2 = []
    for i in range(m):
        for a in atributos:
            if a != 'P':
                for t in tipo:
                    lista.append(watritbuto(a, i, t))
                lista2.append(or_all(lista))
                lista.clear()

                lista.append(watritbuto(a, i, t))
                lista.append(Not(watritbuto(a, i, t)))
                lista.append(Not(watritbuto(a, i, t)))
                lista2.append(and_all(lista))
                lista.clear()

                lista.append(Not(watritbuto(a, i, t)))
                lista.append(watritbuto(a, i, t))
                lista.append(Not(watritbuto(a, i, t)))
                lista2.append(and_all(lista))
                lista.clear()

                lista.append(Not(watritbuto(a, i, t)))
                lista.append(Not(watritbuto(a, i, t)))
                lista.append(watritbuto(a, i, t))
                lista2.append(and_all(lista))
                lista.clear()

    formula = and_all(lista2)
    return formula


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


def r3():
    lista = []
    lista2 = []
    for i in range(m):
        for a in atributos:
            if a != 'P':
                lista.append(watritbuto(a, i, 'p'))
        lista2.append(or_all(lista))
        lista.clear()
    formula = and_all(lista2)
    return formula


#def r4():


def r5():
    lista2 = []
    lista = []
    for j in range(pacientes):
        if valor_atributos[j][atributos.index('P')] == 1:
            for i in range(m):
                lista.append(Atom('C_' + str(i + 1) + '_' + str(j + 1)))
            lista2.append(or_all(lista))
            lista.clear()
    formula = and_all(lista2)
    return formula


#Funções


def atribuir_atributos():
    valores = {}
    for a in atributos:
        if a != 'P':
            for i in range(m):
                valores['X_' + a + '_' + str(i + 1) + '_' +
                        'p'] = valor_atributos[i][atributos.index(a)]
                if valor_atributos[i][atributos.index(a)] == 0:
                    valores['X_' + a + '_' + str(i + 1) + '_' + 'n'] = 1
                else:
                    valores['X_' + a + '_' + str(i + 1) + '_' + 'n'] = 0
    return valores


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


#print(valor_atributos[1][5])
"""Execução
y = atribuir_atributos()
print(y)
for x in y:
    print(x +': '+ str(y[x]))"""

print('\nRestrição 1: ' + str(r1()))
print('\nRestrição 2: ' + str(r2()))
print('\nRestrição 3: ' + str(r3()))
#print('\nRestrição 4: ' + str(r4()))
print('\nRestrição 5: ' + str(r5()))

#satisfiability_brute_force())

#z = and_all(y)
#print(z)
