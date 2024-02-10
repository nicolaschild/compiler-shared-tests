"""Importing the parser turned out to be a nightmare, so I am just making a system call to the parser"""
import subprocess

def run_parser(input_string: str) -> tuple[str, str, int]:
    """Save the input string to a file and run the parser"""
    with open("./src/submodules/parse/test_input.kxi", "w") as f:
        f.write(input_string)

    result = subprocess.run(
        ["python3", "./src/main.py", "-p", "-i", "./src/submodules/parse/test_input.kxi"],
        text=True,
        capture_output=True
    )

    return (result.stdout, result.stderr, result.returncode)

SUCCESS_STD_OUT = "Creating an AST diagram\n"

# -- COMPILATION UNIT TESTS --
def test_compilation_unit_valid() -> None:
    """Test the main compilation unit"""
    # arrange, act
    stdout, _, return_code = run_parser("void main() {}")
    # assert
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("class Cheese {} class Motz {} void main() {}")

    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("class Node {} void main() {int x;}")

    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


def test_compilation_unit_invalid() -> None:
    """Test the main compilation unit"""
    # arrange, act
    _, _, return_code = run_parser("void main() {")
    # assert
    assert return_code == 1


    # Main must be at the outermost scope
    _, _, return_code = run_parser("class Cheese { void main() {} }")
    assert return_code == 1

    _, _, return_code = run_parser("Cheese void main() {}")
    assert return_code == 1

    _, _, return_code = run_parser("void main() {} class Cheese {}")
    assert return_code == 1

    _, _, return_code = run_parser("void main {}")
    assert return_code == 1

    _, _, return_code = run_parser("void main()")
    assert return_code == 1

    _, _, return_code = run_parser("class Cheese {}")
    assert return_code == 1

def test_compilation_unit_main_identifier_check() -> None:
    """Test that lexeme main is enforced"""

    _, _, return_code = run_parser("void potato() {}")
    assert return_code == 1

    _, _, return_code = run_parser("void main() {}")
    assert return_code == 0


# -- CLASS DEFINITION TESTS --

main = " void main() {}"
def test_class_definition_valid_basic() -> None:
    """Test the class definition"""

    stdout, _, return_code = run_parser("class Cheese {}" + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("class Cheese { } class Motz { }" + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("class Node { }" + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

def test_class_definition_invalid_basic() -> None:
    """Test the class definition"""

    _, _, return_code = run_parser("class {}" + main)
    assert return_code == 1

    _, _, return_code = run_parser("class {} class Motz {}" + main)
    assert return_code == 1

def test_class_definition_valid_method_declaration() -> None:
    """Test the class definition with method declarations"""

    stdout, _, return_code = run_parser("""
    class Cheese
    {
        static public int amazing_method() {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class Cheese
    {
        public int amazing_method() {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class Cheese
    {
        private int amazing_method() {}
        static private int amazing_method2() {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class Cheese
    {
        public char amazing_method(int x, char y, bool e) {}
        private void amazing_method2(string cheese, Cheese motz) {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


# -- METHOD DECLARATION --
def test_class_definition_invalid_method_declaration() -> None:
    """Test the class definition with method declarations"""
    _, _, return_code = run_parser("""
    class Cheese
    {
        static! public int sad_method() {}
        public int amazing_method() {}
    }
    """ + main)
    assert return_code == 1

    _, _, return_code = run_parser("""
    class Cheese
    {
        public sad_method() {}
    }
    """ + main)
    assert return_code == 1

    _, _, return_code = run_parser("""
    class Cheese
    {
        public char sad_method(so, so, sad) {}
    }
    """ + main)
    assert return_code == 1 

# -- DATA MEMBER DECLARATION --
def test_class_definition_data_member_declaration() -> None:
    """Test the class definition with the data member declarations"""
    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        static private int count;
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        private int count;
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        private bool count;
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        public int count;
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        public int count = 4;
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        static private int count = 4;
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        static public char favChar = 'a';
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        static private string favString = "This is awesome!";
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

def test_class_definition_invalid_data_member_declaration() -> None:
    """Test the class definition with the data member declarations"""
    _, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        static private count = "4";
    }
    """ + main)
    assert return_code == 1

    _, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        static private int count = "4"
    }
    """ + main)
    assert return_code == 1

    _, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        char a = 'a';
    }
    """ + main)
    assert return_code == 1

    _, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        char private a = 'a';
    }
    """ + main)
    assert return_code == 1


# -- CONSTRUCTOR DECLARATION
def test_class_definition_constructor_declaration() -> None:
    """Test the class definition with the constructor declaration"""
    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        SomeAmazingClass() {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        SomeAmazingClass() {}
        SomeAmazingClass() {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0

    stdout, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        SomeAmazingClass(int x, char y, bool e) {}
    }
    """ + main)
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0


def test_class_definition_invalid_constructor_declaration() -> None:
    """Test the class definition with the constructor declaration"""
    _, _, return_code = run_parser("""
    class SomeAmazingClass
    {
        SomeAmazingClass {}
    }
    """ + main)
    assert return_code == 1

    _, _, return_code = run_parser("""
    class SomeAmazing {
        () {}
    }
    """ + main)
    assert return_code == 1

# -- Array Declaration --
def test_array_declaration() -> None:
    """Test array declarations"""
    stdout, _, return_code = run_parser("void main() {int[] x;}")
    assert stdout == SUCCESS_STD_OUT
    assert return_code == 0