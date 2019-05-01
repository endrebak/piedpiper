import pyparsing as pp
from pydbg import dbg


import re
opening_or_closing_parens = re.compile("(^\(|\)$)")

def pretokenize(src):

    last_e = 0

    src_tokenized = list(pp.nestedExpr().scanString(src))
    _, start, end = src_tokenized[0]

    start_expression = src[last_e:start]
    parens = src[start:end]

    surrounding_parens = len(src_tokenized) == 1
    if surrounding_parens:
        # parens = parens[1:-1]
        parens = re.sub(opening_or_closing_parens, " ", parens)
        src_tokenized = list(pp.nestedExpr().scanString(parens))
        src = parens
    else:
        start_expression = start_expression + parens

    assignment = "=" in start_expression

    assignment_variable = ""
    if assignment:
        expr_split = start_expression.split("=")
        assignment_variable = expr_split[0].strip()
        start_expression = expr_split[1].strip()

    return assignment_variable, start_expression, src_tokenized, src

def brackets(expression):

    expr_tokenized = list(pp.nestedExpr('[', ']').scanString(expression))
    results = []

    last_e = 0
    for _, start, end in expr_tokenized:
        _expression = expression[last_e:start]
        parens = expression[start:end]
        last_e = end
        if _expression:
            # this part takes care of ["wa"].hi.df["bla"], i.e. properties
            for _x in _expression.split("."):
                if _x:
                    results.append("." + _x)
        if parens:
            results.append(parens)

    if expression[last_e:]:
        results.append(expression[last_e:])

    return results

def tokenize(src):

    assignment_variable, start_expression, src_tokenized, src = pretokenize(src)
    results = []

    last_e = 0
    for _, start, end in src_tokenized:
        # print("-----" * 10)
        expression = src[last_e:start]
        parens = src[start:end]
        brackets(expression)
        # print("expression", expression)
        # print("parens", parens)
        last_e = end
