from formula import Atom, Not, And, Or, Implies
from semantics import and_all, or_all

#Funções auxiliares
#Funções para criar atomicas no formato atributo/regra
#'t' representa o tipo: 'p'=positivo, 'n'=negativo, 's'=não aparece]
def watritbuto(a, i, t):
    return Atom(a + '-' + str(i + 1) + '-' + t)

def wregra(i, j):
    return Atom('C-' + str(i + 1) + '-' + str(j + 1))


#Funções para restrições
#Restrição 1. Para cada atributo e cada regra, temos exatamente uma das três possibilidades: 
#o atributo aparece positivamente na regra, o atributo aparece negativamente na regra ou o atributo não aparece na regra.
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
        if valor_atributos[j][atributos.index('P')] == '0':
            for i in range(m):
                for a in atributos:
                    if a != 'P':
                        if valor_atributos[j][atributos.index(str(a))] == '1': 
                            lista.append(watritbuto(a, i, 'n'))
                        else:
                            lista.append(watritbuto(a, i, 'p'))
                lista2.append(or_all(lista))
                lista.clear()
    formula = and_all(lista2)
    return formula


#Restrição 4. Para cada paciente com patologia, cada regra e cada atributo, 
#se o atributo do paciente não se aplicar ao da regra, então a regra não cobre esse paciente.
def r4(m, atributos, pacientes, valor_atributos):
    lista = []
    lista2 = []
    for j in range(pacientes):
        if valor_atributos[j][atributos.index('P')] == '1':
            for i in range(m):
                for a in atributos:
                    if a != 'P':
                        if valor_atributos[j][atributos.index(str(a))] == '1':
                            lista.append(Implies(watritbuto(a, i, 'n'), Not(wregra(i, j))))
                        else:
                            lista.append(Implies(watritbuto(a, i, 'p'), Not(wregra(i, j))))
                lista2.append(and_all(lista))
                lista.clear()
    formula = and_all(lista2)
    return formula


#Restrição 5. Cada paciente com patologia deve ser coberto por alguma das regras.
def r5(m, atributos, pacientes, valor_atributos):
    lista = []
    lista2 = []
    for j in range(pacientes):
        if valor_atributos[j][atributos.index('P')] == '1':
            for i in range(m):
                lista.append(wregra(i, j))
            lista2.append(or_all(lista))
            lista.clear()
    formula = and_all(lista2)
    return formula


#Gera conjunto de regras com base na valoração
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
                    else:
                        lista.append(a)
        lista2.append(str(lista) + ' \u21E8 P')
        lista.clear()
    return lista2

#Preenche a função test_pacientes com strings
def wpacientes(j, p):
    if p == 1:
        return ('Paciente ' + str(j + 1) + ' possui patologia.')
    else:
        return ('Paciente ' + str(j + 1) + ' não possui patologia.')

#Testa se os pacientes tem patologia com base na valoração
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
                            if valor_atributos[j][atributos.index(a)] == '0':
                                pat = pat + 1
                        else:
                            lista.append(a)
                            if valor_atributos[j][atributos.index(a)] == '1':
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
    return lista2