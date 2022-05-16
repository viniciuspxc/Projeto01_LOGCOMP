from formula import Atom, Not, And, Or, Implies
from functions import subformulas, length, atoms, number_of_atoms, number_of_connectives, is_literal, substitution
from semantics import truth_value, satisfiability_brute_force
"""formula = And(Not(Implies(And(Not(Atom('k')),Atom('j')),Atom('p'))),Atom('k'))
print(formula)

for x in atoms(formula):
  print(x)"""

my_formula = Implies(Not(Atom('p')), Or(Atom('p'), Atom('s')))
print(my_formula)
print(substitution(my_formula,Not(Atom('p')),And(Atom('a'),Atom('p'))))



