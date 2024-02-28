"""Importing the parser turned out to be a nightmare, so I am just making a system call to the parser"""
# type: ignore
import subprocess
import pytest


# -- COMPILATION UNIT TESTS --
def run_parser(input_string: str) -> tuple[str, str, int]:
    """Save the input string to a file and run the parser"""
    with open("./src/submodules/parse/test_input.kxi", "w") as f:
        f.write(input_string)

    result = subprocess.run(
        [
            "python3",
            "./src/main.py",
            "-p",
            "-i",
            "./src/submodules/parse/test_input.kxi",
        ],
        text=True,
        capture_output=True,
    )

    return (result.stdout, result.stderr, result.returncode)


SUCCESS_STD_OUT = "Creating an AST diagram\n"


# -- COMPILATION UNIT TESTS --
@pytest.mark.parametrize(
    "code_snippet",
    [
        "void main() {}",
        "class Cheese {} class Motz {} void main() {}",
        "class Node {} void main() {int x;}",
    ],
)
def test_compilation_unit_valid(code_snippet: str) -> None:
    """Test valid main compilation units."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet, expected_return_code",
    [
        ("void main() {", 1),
        ("class Cheese { void main() {} }", 1),
        ("Cheese void main() {}", 1),
        ("void main() {} class Cheese {}", 1),
        ("void main {}", 1),
        ("void main()", 1),
        ("class Cheese {}", 1),
    ],
)
def test_compilation_unit_invalid(code_snippet: str, expected_return_code: int) -> None:
    """Test invalid main compilation units."""
    _, _, return_code = run_parser(code_snippet)
    assert return_code == expected_return_code


@pytest.mark.parametrize(
    "code_snippet, expected_return_code",
    [
        ("void potato() {}", 1),
        ("void main() {}", 0),
    ],
)
def test_compilation_unit_main_identifier_check(
    code_snippet: str, expected_return_code: int
) -> None:
    """Test that lexeme main is enforced."""
    _, _, return_code = run_parser(code_snippet)
    assert return_code == expected_return_code


# # -- CLASS DEFINITION TESTS --
main = " void main() {}"


@pytest.mark.parametrize(
    "code_snippet",
    [
        "class Cheese {}",
        "class Cheese { } class Motz { }",
        "class Node { }",
    ],
)
def test_class_definition_valid_basic(code_snippet: str) -> None:
    """Test basic class definitions."""
    stdout, _, return_code = run_parser(code_snippet + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """ class Cheese { static public int amazing_method() {} } """ + main,
        """ class Cheese { public int amazing_method() {} } """ + main,
        """ class Cheese { private int amazing_method() {} static private int amazing_method2() {} }"""
        + main,
        """ class Cheese { public char amazing_method(int x, char y, bool e) {} } """
        + main,
    ],
)
def test_class_definition_valid_method_declaration(code_snippet: str) -> None:
    """Test valid class definitions with method declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


# -- METHOD DECLARATION --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """ class Cheese { static! public int sad_method() {} public int amazing_method() {} } """
        + main,
        """ class Cheese { public sad_method() {} }""" + main,
        """ class Cheese { public char sad_method(so, so, sad) {} } """ + main,
    ],
)
def test_class_definition_invalid_method_declaration(code_snippet: str) -> None:
    """Test invalid class definition method declarations."""
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 1


@pytest.mark.parametrize(
    "code_snippet",
    [
        """ class SomeAmazingClass{ static private int count; }""" + main,
        """ class SomeAmazingClass{ private int count; }""" + main,
        """ class SomeAmazingClass{ private bool count; }""" + main,
        """ class SomeAmazingClass{ public int count; }""" + main,
        """ class SomeAmazingClass{ public int count = 4; }""" + main,
        """ class SomeAmazingClass{ static private int count = 4; }""" + main,
        """ class SomeAmazingClass{ static public char favChar = 'a'; }""" + main,
        """ class SomeAmazingClass { static private string favString = "This is awesome!"; } """
        + main,
    ],
)
def test_class_definition_data_member_declaration(code_snippet: str) -> None:
    """Test valid class definitions with data member declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """class SomeAmazingClass { static private count = "4"; }""" + main,
        """class SomeAmazingClass{ static private int count = "4" }""" + main,
        """class SomeAmazingClass{ char a = 'a'; }""" + main,
        """class SomeAmazingClass{ char private a = 'a'; }""" + main,
    ],
)
def test_class_definition_invalid_data_member_declaration(code_snippet: str) -> None:
    """Test invalid class definition data member declarations."""
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 1


# -- CONSTRUCTOR DECLARATION
@pytest.mark.parametrize(
    "code_snippet",
    [
        """class SomeAmazingClass { SomeAmazingClass() {} }""" + main,
        """class SomeAmazingClass { SomeAmazingClass() {} SomeAmazingClass() {} }"""
        + main,
        """class SomeAmazingClass { SomeAmazingClass(int[] x, char y, bool e) {} }"""
        + main,
    ],
)
def test_class_definition_constructor_declaration(code_snippet: str) -> None:
    """Test valid class definitions with constructor declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """ class SomeAmazingClass { SomeAmazingClass {} } """ + main,
        """ class SomeAmazing { () {} } """ + main,
    ],
)
def test_class_definition_invalid_constructor_declaration(code_snippet: str) -> None:
    """Test invalid class definitions with constructor declarations."""
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 1


# -- Array Declaration --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {new cheese[] ();}""",
        """void main() {new int[] ();}""",
        """void main() {new cheese[][][][][][][][] ();}""",
        """void main() {new int[][][][][] ();}""",
        """void main() {new cheese();}""",
        """void main() {new int();}""",
    ],
)
def test_new_type_identifier(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


def test_new_type_identifier_invalid() -> None:
    _, _, return_code = run_parser("void main() {new cheese[];}")
    assert return_code == 1


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {new cheese[1];}""",
        """void main() {new int[1];}""",
        """void main() {new cheese[][][1];}""",
        """void main() {new char[][][1];}""",
    ],
)
def test_new_expression_index(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese[1];}""",
        """void main() {"cheese"[1];}""",
        """void main() {false[1];}""",
        """void main() {true[1];}""",
    ],
)
def test_expression_index(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheeto(1, 2, 3);}""",
        """void main() {cheeto(x, y);}""",
        """void main() {cheeto(x, 'a');}""",
        """void main() {cheeto(12, new custom[1]);}""",
    ],
)
def test_expression_arguments(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese = 4;}""",
        """void main() {x = y;}""",
    ],
)
def test_expression_eq(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese += 4;}""",
        """void main() {cheese += x;}""",
    ],
)
def test_expression_plus_eq(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese -= 4;}""",
        """void main() {cheese -= x;}""",
    ],
)
def test_expression_minus_eq(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese *= 4;}""",
        """void main() {cheese *= x;}""",
    ],
)
def test_expression_times_eq(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese /= 4;}""",
        """void main() {cheese /= x;}""",
    ],
)
def test_expression_divide_eq(code_snippet: str) -> None:
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 + 4;}""",
        """void main() {x + 4;}""",
    ],
)
def test_expression_plus(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 - 4;}""",
        """void main() {x - 4;}""",
    ],
)
def test_expression_minus(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 * 4;}""",
        """void main() {x * 4;}""",
    ],
)
def test_expression_times(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 / 4;}""",
        """void main() {x / 4;}""",
    ],
)
def test_expression_divide(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 == 4;}""",
        """void main() {x == 4;}""",
    ],
)
def test_expression_eq_eq(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 != 4;}""",
        """void main() {x != 4;}""",
    ],
)
def test_expression_neq(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 < 4;}""",
        """void main() {x < 4;}""",
    ],
)
def test_expression_lt(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 > 4;}""",
        """void main() {x > 4;}""",
    ],
)
def test_expression_gt(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 <= 4;}""",
        """void main() {x <= 4;}""",
    ],
)
def test_expression_le(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 >= 4;}""",
        """void main() {x >= 4;}""",
    ],
)
def test_expression_ge(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 && 4;}""",
        """void main() {x && 4;}""",
    ],
)
def test_expression_and(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4 || 4;}""",
        """void main() {x || 4;}""",
    ],
)
def test_expression_or(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {!4;}""",
        """void main() {!x;}""",
    ],
)
def test_expression_not(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {+'a';}""",
        """void main() {+x;}""",
    ],
)
def test_expression_plus_unary(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {-'a';}""",
        """void main() {-x;}""",
    ],
)
def test_expression_minus_unary(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {(4);}""",
        """void main() {(x);}""",
    ],
)
def test_expression_parenthesized(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {4;}""",
        """void main() {'a';}""",
        """void main() {true;}""",
        """void main() {false;}""",
        """void main() {null;}""",
        """void main() {this;}""",
        """void main() {cheese;}""",
    ],
)
def test_expression_literal_identifier(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { switch ( x ) {case 1: break; default: break; }}""",
        """void main() { switch ( x ) {case 2: break; case 2: 1+1; default: break; }}""",
    ],
)
def test_statement_switch(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


# -- STATEMENT --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { if (true) {int x;}}""",
        """void main() { if (false) if(true) {} else return 5;}""",
        """void main() { if (true) {int x;} else {int x;}}""",
        """void main() { if (true) {int x;} else if (true) {int x;} else {int x;}}""",
    ],
)
def test_statement_if(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { while (true) {int x;}}""",
        """void main() { while (true) {int x;} }""",
    ],
)
def test_statement_while(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { for (i = 0; i < 10; i += 1) {int x;}}""",
        """void main() { for (i = 0; i < 10; i += 1) for (i = 0; i < 10; i += 1) break;}""",
        """void main() { for (;i < 10;) {int x;} }""",
        """void main() { for (;i < 10; i += 5) {int x;} }""",
        """void main() { for (i = 0; i += 5;) {int x;} }""",
    ],
)
def test_statement_for(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { return; }""",
        """void main() { return 1; }""",
        """void main() { return x; }""",
        """void main() { return "cheese"; }""",
    ],
)
def test_statement_return(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { break; }""",
    ],
)
def test_statement_break(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { cin >> x; }""",
        """void main() { cin >> x + y; }""",
    ],
)
def test_statement_input(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() { cout << x; }""",
        """void main() { cout << x + y; }""",
    ],
)
def test_statement_output(code_snippet: str) -> None:
    _, _, return_code = run_parser(code_snippet)
    assert return_code == 0


# -- METHOD SUFFIX, PARAMETER LIST, PARAMETER --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """class Cheesy { static public void motz(int a, char b, int c) {} }""" + main,
        """class Cheesy { static public void motz() {} }""" + main,
    ],
)
def test_method_suffix_valid(code_snippet: str) -> None:
    """Test valid method suffix."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


# -- VARIABLE DECLARATION --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """class Cheese {private int x;}""" + main,
        """class Cheese {private char[][] x;}""" + main,
        """class Mozz {private int x = 4;}""" + main,
        """class American {private int x = 4 + 4;}""" + main,
        """class parm {private int x = 4 + 4; public char a = 'a';}""" + main,
        """class cheddar {private int x = 4 + 4; private char k = 'k'; private string side_dish = "beaan";}"""
        + main,
        """class PepperJack {public int x = 4 + 4; public char y = 'a';}""" + main,
        """class ColbyJack {private int x = 4 + 4; public int y = 4 + 4; private int z = 4 + 4; public int a = 4 + 4; private int b = 4 + 4;}"""
        + main,
    ],
)
def test_variable_declaration_valid(code_snippet: str) -> None:
    """Test valid variable declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

# -- DATA MEMBER ACCESS ORDER
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {x.num;}""",
        """void main() {x.num + 3;}""",
        """void main() {x.num + 3 * 7 + 8;}""",
        """void main() {4 + x.num;}"""
    ],
)
def test_data_member_access_order(code_snippet: str) -> None:
    """Test valid variable declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


# -- INDEX ACCESS ORDER
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {x[4];}""",
        """void main() {x[8] + 3;}""",
        """void main() {x[2+3] + 3 * 7 + 8;}""",
        """void main() {4 + x[3];}"""
    ],
)
def test_index_access_order(code_snippet: str) -> None:
    """Test valid variable declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

# -- NEW EXPRESSION ORDER
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {new cheese() + 4;}""",
        """void main() {new cheese() + x;}""",
        """void main() {4 + new cheese();}""",
        """void main() {new cheese() + new cheese();}""",
    ],
)
def test_new_expression_order(code_snippet: str) -> None:
    """Test valid variable declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

# -- FUNCTION CALL ORDER
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {cheese(4, 5, 6) + 4;}""",
        """void main() {4 + cheese(4, 5, 6);}""",
        """void main() {cheese(4);}""",
        """void main() {cheese() + cheese();}""",
        """void main() {cheese() + cheese() + 5;}""",
    ],
)
def test_function_call_order(code_snippet: str) -> None:
    """Test valid variable declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

# -- UNARY EXPRESSION ORDER
@pytest.mark.parametrize(
    "code_snippet",
    [
        """void main() {!4 + 4;}""",
        """void main() {!x + 4;}""",
        """void main() {!4 + x;}""",
        """void main() {!x + x;}""",
        """void main() {+4 + 4;}""",
        """void main() {+x + 4;}""",
        """void main() {+4 + x;}""",
        """void main() {+x + x;}""",
        """void main() {-4 + 4;}""",
        """void main() {-x + 4;}""",
        """void main() {-4 + x;}""",
        """void main() {-x + x;}""",
        """void main() {4 + !4;}""",
        """void main() {4 + +4;}""",
        """void main() {4 + -4;}""",
    ],
)
def test_unary_op_order(code_snippet: str) -> None:
    """Test valid variable declarations."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

# -- IGNORE COMMENTS TESTS --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """// This is a comment\nvoid main() {}""",
        """// This is a comment\n// This is a comment\nvoid main() {}""",
    ],
)
def test_ignore_comments(code_snippet: str) -> None:
    """Test that comments are ignored."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


# -- IGNORE WHITESPACE TESTS --
@pytest.mark.parametrize(
    "code_snippet",
    [
        """\nvoid main() {}""",
        """\n\n\nvoid main() {}""",
        """\tvoid main() {}""",
        """\t\t\tvoid main() {}""",
        """\n\tvoid main() {}""",
        """\n\n\tvoid main() {}""",
    ],
)
def test_ignore_whitespace(code_snippet: str) -> None:
    """Test that whitespace is ignored."""
    stdout, _, return_code = run_parser(code_snippet)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0