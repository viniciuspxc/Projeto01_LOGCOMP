"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """

from formula import Atom, Not, And, Or, Implies
from functions import atoms


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        return interpretation[str(formula)]
    if isinstance(formula, Not):
        return not (truth_value(formula.inner, interpretation))
    if isinstance(formula, Implies):
        sub1 = truth_value(formula.left, interpretation)
        sub2 = truth_value(formula.right, interpretation)
        return not (sub1) or sub2
    if isinstance(formula, And):
        sub1 = truth_value(formula.left, interpretation)
        sub2 = truth_value(formula.right, interpretation)
        return sub1 and sub2
    if isinstance(formula, Or):
        sub1 = truth_value(formula.left, interpretation)
        sub2 = truth_value(formula.right, interpretation)
        return sub1 or sub2


def is_logical_consequence(
        premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it     returns False"""
    pass
    # ======== YOUR CODE HERE ========


def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an           
    interpretation that assigns true to the formula.
    Otherwise, it returns False."""

    valoracao = {}
    atomicas = atoms(formula)
    for atom in atoms(formula):
        valoracao[str(atom)] = None

    result = sat_check(formula, atomicas, valoracao)

    return(result)


def sat_check(formula, atomicas, valoracao):
    atomicas = atomicas.copy()
    if len(atomicas) == 0:
        if truth_value(formula, valoracao) == True:
            return (valoracao)
        else:
            return False

    atom = atomicas.pop()
    val1 = valoracao.copy()
    val2 = valoracao.copy()
    val1[str(atom)] = True
    val2[str(atom)] = False

    val1_result = sat_check(formula, atomicas, val1)
    if val1_result:
        return val1_result
    else:
        return sat_check(formula, atomicas, val2)


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
