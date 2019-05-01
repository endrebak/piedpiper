import pytest
from piedpiper.parsing import pretokenize, tokenize, brackets

assignment_parens = """hi = (df
.hi()
[['fi']][["why"]]
.there()
(__call__)
.NI(ni='NI!'))"""


assignment_no_parens = """hi = df.hi()[['fi']].there()(__call__).NI(ni='NI!')"""

no_assignment_parens = """(df
.hi()
[['fi']]
.there()
(__call__).NI(ni='NI!))"""

no_assignment_no_parens = """df.hi()[['fi']].there()(__call__).NI(ni='NI!')"""



inputs = [assignment_parens, assignment_no_parens, no_assignment_parens, no_assignment_no_parens]
expected_assignment_variables = ["hi", "hi", "", ""]
expected_start_expressions = ["", "df.hi()", "", "df.hi()"]

# @pytest.mark.parametrize("inputs,expected_assignment_variable,expected_start_expression", zip(inputs, expected_assignment_variables, expected_start_expressions))
# def test_pretokenize(inputs, expected_assignment_variable, expected_start_expression):
#     assignment_variable, start_expression, _, _ = pretokenize(inputs)
#     assert start_expression == expected_start_expression
#     assert assignment_variable == expected_assignment_variable



# @pytest.mark.parametrize("inputs,expected_assignment_variable,expected_start_expression", zip(inputs, expected_assignment_variables, expected_start_expressions))
# @pytest.mark.parametrize("inputs", inputs[:1])
# def test_tokenize(inputs):
#     result = tokenize(inputs)
#     assert 0
    # assert start_expression == expected_start_expression
    # assert assignment_variable == expected_assignment_variable

bracket1 = "[['fi']][[['why']]].there"

def test_brackets():

    result = brackets(bracket1)
    assert result == ["[['fi']]", "[[['why']]]", '.there']

bracket2 = ".hi"
def test_brackets2():

    result = brackets(bracket2)
    print(result)
    assert result == [".hi"]


bracket3 = "['woops'].hi.df['there']"
def test_brackets3():

    result = brackets(bracket3)
    print(result)
    assert result == [".hi"]
