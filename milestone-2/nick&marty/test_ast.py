import subprocess
import pytest

# --Helper Functions--
def run_parser(input_string: str) -> tuple[str, str, int]:
    """Save the input string to a file and run the parser"""
    with open("./src/submodules/parse/test_input.kxi", "w") as f:
        f.write(input_string)
    args = [ "python3", "./src/main.py", "-p", "-i", "./src/submodules/parse/test_input.kxi", "--debug",]
    result = subprocess.run(args, text=True, capture_output=True)

    return (result.stdout, result.stderr, result.returncode)


def remove_leading_whitespace(text: str) -> str:
    lines = text.split("\n")
    stripped_lines = [line.lstrip() for line in lines]
    return "\n".join(stripped_lines)


# --Test Cases--
@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        #--COMPILATION UNIT--
        ("void main() {}", 
         remove_leading_whitespace("CompilationUnit\n-Block")),

        #--CLASS DECLARATION--
        # Test case for multiple class declarations
        ("class Cheese {} class Motz {} void main() {}", 
         remove_leading_whitespace("""
            CompilationUnit
            -Class
            --ID: Cheese
            -Class
            --ID: Motz
            -Block
            """)),

        # Test case for class and variable declaration
        ("class Node {} void main() {int x;}", 
         remove_leading_whitespace("""
            CompilationUnit
            -Class
            --ID: Node
            -Block
            --VariableDeclaration
            ---Type
            ---ID: x
            """)),

        # Test case for a class with a data member and a method
        ("class foo { public char bar; static private int baz(int x){ return x + 1; } foo(){ return; } } void main () {}",
         remove_leading_whitespace("""
            CompilationUnit
            -Class
            --ID: foo
            --DataMember
            ---VariableDeclaration
            ----Type
            ----ID: bar
            --Method
            ---Type
            ---ID: baz
            ---Parameter
            ----Type
            ----ID: x
            ---Block
            ----ReturnStatement
            -----BinOp: +
            ------ID: x
            ------Int: 1
            --Constructor
            ---ID: foo
            ---Block
            ----ReturnStatement
            -Block
            """)),

        # Test case for a class with a data member
        ("""class SomeAmazingClass { static private string favString = "This is awesome!"; } void main() {}""",
        remove_leading_whitespace("""
            CompilationUnit
            -Class
            --ID: SomeAmazingClass
            --DataMember
            ---VariableDeclaration
            ----Type
            ----ID: favString
            ----String: This is awesome!
            -Block
        """)),

        # Test case for a class with a data member of array type
        ("""class Class { static private string[][][] cheese = "Triple dimensional!"; } void main() {}""",
        remove_leading_whitespace("""
            CompilationUnit
            -Class
            --ID: Class
            --DataMember
            ---VariableDeclaration
            ----Array
            -----Array
            ------Array
            -------Type
            ----ID: cheese
            ----String: Triple dimensional!
            -Block
        """)),

        # Array in method declaration
        ("class Class { Method(int[] x, char y, bool e) {} } void main() {}",
        remove_leading_whitespace("""
            CompilationUnit
            -Class
            --ID: Class
            --Constructor
            ---ID: Method
            ---Parameter
            ----Array
            -----Type
            ----ID: x
            ---Parameter
            ----Type
            ----ID: y
            ---Parameter
            ----Type
            ----ID: e
            ---Block
            -Block
        """)),

        #--EXPRESSIONS--
        # Test case for return statement
        ("void main () { return x; }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --ReturnStatement
            ---ID: x
            """)),

        #Unary operands
        # Test case for unary -
        ("void main () { -x; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --UnaryOp: -
            ---ID: x
            """)),

        # Test case for unary !
        ("void main () { !x; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --UnaryOp: !
            ---ID: x
            """)),
        
        # Test case for unary +
        ("void main () { +x; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --UnaryOp: +
            ---ID: x
            """)),

        # Test cases for unary op and binary op
        ("void main () { -x + 3; }",
        remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---UnaryOp: -
            ----ID: x
            ---Int: 3
        """)),
        ("void main() {!4 + 4;}",
            remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---UnaryOp: !
            ----Int: 4
            ---Int: 4
        """)),
        ("void main() {+x + 4;}",
            remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---UnaryOp: +
            ----ID: x
            ---Int: 4
        """)),
        ("void main() {4 + !4;}",
            remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---Int: 4
            ---UnaryOp: !
            ----Int: 4
        """)),
        ("void main() {4 + +4;}",
            remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---Int: 4
            ---UnaryOp: +
            ----Int: 4
        """)),
        ("""void main() {4 + -4;}""",
            remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---Int: 4
            ---UnaryOp: -
            ----Int: 4
        """)),

        #Array access
        ("void main () { x[3+2] + -4; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---IndexAccess
            ----ID: x
            ----BinOp: +
            -----Int: 3
            -----Int: 2
            ---UnaryOp: -
            ----Int: 4
        """)),

        # new type is an expression :^]
        ("void main () { new cheese() + new cheese() + 4;}",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---BinOp: +
            ----NewExpression
            -----Type
            ------ID: cheese
            ----NewExpression
            -----Type
            ------ID: cheese
            ---Int: 4
        """)),


        # Test case for binary operand addition and multiplication
        ("void main () { 1 + 3 * 4; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---Int: 1
            ---BinOp: *
            ----Int: 3
            ----Int: 4
            """)),

        # Test case for nested index access
        ("void main () { x[7][8]; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --IndexAccess
            ---IndexAccess
            ----ID: x
            ----Int: 7
            ---Int: 8
            """)),

        # Test case for creating a new 1D array
        ("void main () { new char[8]; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --NewExpression
            ---Array
            ----Type
            ---Index
            ----Int: 8
            """)),

        # Test case for basic binary operand
        ("void main () { x + 3 * 7 + 8; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---BinOp: +
            ----ID: x
            ----BinOp: *
            -----Int: 3
            -----Int: 7
            ---Int: 8
            """)),

        # Test case for data member access before addition
        ("void main() { x.num + 3; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --BinOp: +
            ---DataMemberAccess: .
            ----ID: x
            ----ID: num
            ---Int: 3
            """)),

        # Test case for constructor call
        ("void main() { new fib(10); }", 
            remove_leading_whitespace("""
            CompilationUnit
            -Block
            --NewExpression
            ---Type
            ----ID: fib
            ---Int: 10
            """)),

        # Test function call
        ("void main() { fib(10, 'd'); }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --FunctionCall
            ---ID: fib
            ---Int: 10
            ---Char: d
        """)),

        # -STATEMENTS
        # Block statements
        ("void main() { { { {0;} } } }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --Block
            ---Block
            ----Block
            -----Int: 0
        """)),

        # Return no expression
        ("void main() { return; }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --ReturnStatement
        """)),

        # Return with expression
        ("void main() { return 5; }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --ReturnStatement
            ---Int: 5
        """)),

        ("void main() {char[][] x;}" , remove_leading_whitespace("""
            CompilationUnit
            -Block
            --VariableDeclaration
            ---Array
            ----Array
            -----Type
            ---ID: x
        """)),

        # if statement
        ("void main() { if (x) { return; } }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --IfStatement
            ---ID: x
            ---Block
            ----ReturnStatement
        """)),

        # if-else statement
        ("void main() { if (false) {} else return 5;}", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --IfStatement
            ---Bool: False
            ---Block
            ---ReturnStatement
            ----Int: 5
        """)),

        # if if else statement
        ("void main() {if (false) if (true) {} else return 5;}",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --IfStatement
            ---Bool: False
            ---IfStatement
            ----Bool: True
            ----Block
            ----ReturnStatement
            -----Int: 5
        """)),

        # for loop
        ("void main() {for (i = 0; i< 10; i = i + 1) return 5;}",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --ForStatement
            ---BinOp: =
            ----ID: i
            ----Int: 0
            ---BinOp: <
            ----ID: i
            ----Int: 10
            ---BinOp: =
            ----ID: i
            ----BinOp: +
            -----ID: i
            -----Int: 1
            ---ReturnStatement
            ----Int: 5
        """)),
        # for loop with no initialization or increment
        ("void main() { for (; i< 10;) {} }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --ForStatement
            ---BinOp: <
            ----ID: i
            ----Int: 10
            ---Block
        """)),

        #declarations
        # empty declaration
        ("void main() { int x; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --VariableDeclaration
            ---Type
            ---ID: x
        """)),

        # declaration with assignment
        ("void main() { int x = 5; }",
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --VariableDeclaration
            ---Type
            ---ID: x
            ---Int: 5
        """)),

        #switch statement
        ("void main() { switch ('d') { case 'f': break; case 5: return; default: return 10; } }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --SwitchStatement
            ---Char: d
            ---CaseBlock
            ----Case
            -----break
            ----Case
            -----ReturnStatement
            ----ReturnStatement
            -----Int: 10
        """)),
        # CIN
        ("void main() { cin >> x; }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --ReadStatement
            ---ID: x
        """)),
        #COUT
        ("void main() { cout << x; }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --PrintStatement
            ---ID: x
        """)),
        # WHILE
        ("void main() { while (x) { return; } }", 
         remove_leading_whitespace("""
            CompilationUnit
            -Block
            --WhileStatement
            ---ID: x
            ---Block
            ----ReturnStatement
        """)),
    ]
)
def test_parser(input_string: str, expected_output: str) -> None:
    """Generalized test for compilation unit"""
    input_string = input_string.strip()
    stdout, stderr, returncode = run_parser(input_string)
    assert returncode == 0
    expected_output = expected_output.strip()
    assert stdout.strip() == expected_output
    assert stderr == ""
