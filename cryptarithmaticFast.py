# -------------
# User Instructions
#
# Complete the fill_in(formula) function by adding your code to
# the two places marked with ?????.

import string
import re
import time
import itertools


def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f


def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = "".join(set("".join(re.findall("[A-Z]+", formula))))  # should be a string
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)


def valid(f):
    """Formula f is valid if and only if it has no
    numbers with leading zero, and evals true."""
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d))
                 for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word


def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the fomula; only one eval per formula.
    """
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1, 2, 3, 4, 5, 6, 7, 8, 9, 0),
                                         len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass


def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. For example, 'YOU == ME ** 2' returns
    (lambda Y, M, E, U, O: Y!=0 and M!=0 and ((U+10*O+100*Y) == (E+10*M)**2)), 'YMEUO'"""
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    firstletters = ''.join(set(re.findall(r'\b([A-Z])[A-Z]', formula)))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    # check if the first letter is 0, to avoid 012 type number
    if firstletters:
        tests = ' and '.join(L + '!=0' for L in firstletters)
        body = '%s and (%s)' % (tests, body)

    f = 'lambda %s: %s' % (parms, body)
    if verbose:
        print(f)
    return eval(f), letters


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1 - t0, result


examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + RM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])
DELTA == R * [ ( AADR * O ) + R]
ALGER == R**2 * NIG
ABCBCACAB == DB*DD*DE*FD*HD
ABC == C**4
A*B*(A+B) == A**3 + B**3
TEN + HERONS + REST + NEAR + NORTH + SEA + SHORE + AS + TAN + TERNS + SOAR + TO + ENTER + THERE  + AS + HERONS + NEST + ON + STONES + AT + SHORE + THREE + STARS + ARE + SEEN + TERN + SNORES + ARE + NEAR == SEVVOTH""".splitlines()


def test():
    t0 = time.clock()
    for example in examples:
        print
        print 13 * ' ', example
        print '%6.4f sec:  %s ' % timedcall(faster_solve, example)
    print '%6.4f tot.' % (time.clock() - t0)


# print(solve('ODD+ODD==EVEN'))
test()

# python -m cProfile cryptarithmatic.py
# import cProfile
# cProfile.run('test()')
