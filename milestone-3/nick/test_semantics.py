import subprocess
import pytest
# --Helper Functions--
def run_parser(input_string: str) -> tuple[str, str, int]:
    """Save the input string to a file and run the parser"""
    with open("./src/submodules/parse/test_input.kxi", "w") as f:
        f.write(input_string)
    args = [
        "python3",
        "./src/main.py",
        "-s",
        "-i",
        "./src/submodules/parse/test_input.kxi",
    ]
    result = subprocess.run(args, text=True, capture_output=True)
    return (result.stdout, result.stderr, result.returncode)

"""Doubly declared variables"""
@pytest.mark.parametrize(
    "input_string",
    [
        # Should fail on variable declaration, not constructor declaration
        """
        class Cheese {
            Cheese() {
                int Cheese;
            }
        }
        void main() {int x;}
        """,
        # Should fail because class Lheese doesn't exist, it's like loser cheese (not chill)
        """
        class Cheese {}
        void main() {
            Cheese c = new Lheese(1, 2, 3);
        }
        """,
        # Should fail from overwriting a name in the global namespace Cheese
        """
        class Cheese {}
        void main() {int Cheese;}
        """,
        # Should fail from two constructors
        """
        class Cheese{
            Cheese() {}
            Cheese() {}
        }
        void main() {}
        """,
        # Should fail from data member overriding name of the scope
        """
        class Cheese{
            static public int Cheese = 4;
        }
        void main() {}
        """,
        # Duplicate class declarations should fail
        """
        class Cheese{
            static public int cheese = 4;
        }
        class Cheese{

        }
        void main() {}
        """,
        # Functions overriding class name should fail
        """
        class Cheese { 
            public void Cheese() {

            }
        }
        void main() {}
        """,
        # Duplicate variable declarations within the same scope
        """
        void main() {
            int x = 5;
            int x = 2; 
        }
        """
    ]
)

def test_invalid_symbol_table_smith(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""

@pytest.mark.parametrize(
    "input_string",
    [
        # Valid constructor
        """
        class Cheese{
            Cheese() {}
        }
        void main() {}
        """,
        # Variable declarations within different scopes (of the same name)
        """
        void main() {
            int x = 5;
            if (true) {
                int x = 2;
            }
        }
        """,
        #'This' keyword is fine if it is a data member, in a method
        """
        class Cheese {
            public int x;
            public int motz() {
                return this.x;
            }
        } void main() {}
        """,
        #'This' keyword is fine if it is a data member, in a constructor
        """
        class Cheese {
            public int x;
            Cheese() {
                return this.x;
            }
        } void main() {}
        """,
        # Shadowing declaration names
        """
        class Cheese {
            private int x;
            public void motz() {
                int x;
            }
        }
        void main() {
            int x;
            while (true) {
                int x;
            }
        }
        """,
        # Redeclaring main should shadow
        """
        void main() {
            int main;
        }
        """,
        """
        class Cheese {
            public int x;
        }    
        void main() {
           Cheese x = new Cheese(); 
        }
        """
    ],
)

def test_valid_symbol_table_smith(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 0
    assert stderr == ""


"""Test undeclared variables"""
@pytest.mark.parametrize(
    "input_string",
    [
        """
        void main() {
            int x = y;
        }
        """,
        """
        void main() {
            x;
        }
        """,
        """
        class Cheese {
            public int motz() {
                return x;
            }
        } void main() {}
        """,
        """
        class Cheese {
            public int motz() {
                return this.x;
            }
        } void main() {}
        """,
        # Scope check, x should be uninitialzed
        """
        class Cheese {
            public int x;
            public int motz() {
                char inside_motz = 'a';
            }
        }
        void main() {
            x;
        }
        """,
        #Double constructor should fail
        """
        class Cheese {
            public int x;
            Cheese() {
                return this.x;
            }
            Cheese() {
                return this.x;
            }
        } void main() {}
        """,
        # Triple constructor should fail
        """
        class Cheese {
            public int x;
            Cheese() {
                return this.x;
            }
            Cheese() {
                return this.x;
            }
            Cheese() {
                return this.x;
            }
        } void main() {}
        """,
        """
        //this keyword should always grab the instance data members, even if that same ident has been shadowed
        //therefore, this should fail, hard.

        class Cheese {
        private int x;
            Cheese(char x) {
                this.x = x;
            }
        }
        void main() {}
        """
        """
        class Cheese {
            public int x;
            public int motz() {
                char inside_motz = 'a';
            }
        }
        void main() {
            this.x; //This should fail
        }
        """,
        # Constuctor name needs to match the class name
        """
        class Cheese {
            private int x;
            Peese() {}
        }
        void main() {
            int x;
        }
        """,
        # Don't be lazy and match against the global class list
        """
        class Peese {}
        class Cheese {
            private int x;
            Peese() {}
        }
        void main() {
            int x;
        }
        """
        # Order doesn't matter, this should fail too
        """
        class Foo {
            private int Cheese;
            }
            class Cheese {}
            void main(){
            }
        """,
        """
        class Foo {
            private void Test() {
                Cheese;
            }
        }
        class Cheese {}
        void main(){}
        """,
        """
        class Foo {
            private void Cheese() {
            }
        }
        class Cheese {}
        void main(){}
        """,
        """
        class Foo {
            private void Test() {
                int Cheese = 4;
            }
        }
        class Cheese {}
        void main() {}
        """,
        """
        class Foo {
            private void Test() {
            }
        }
        class Cheese {}
        void main() {int Cheese;}
        """,
        # Should fail from undeclared class
        """
        void main() {
            Cheese x = new Cheese();
        }
        """,
    ])

def test_undeclared_variables(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""


@pytest.mark.parametrize("input_string", [
    #Type check LHS of assignment
    """
    class Cheese {}
    void main() {
        Cheese x = 4;
    }
    """,
    #Type check RHS of assignment
    """
    class Cheese {}
    void main() {
        Cheese c = true;
    }
    """,
    #Invalid type in if statement
    """void main() {
        if (null) {
            int x = 5;
        }
    }
    """,
    # Invalid Relational operators
    """
    void main() {
        if (1 < 'a') {
            int x = 5;
        }
    }
    """,
    """
    void main() {
        if (1 > "lol") {
            int x = 5;
        }
    }
    """,
    """
    void main() {
        if (true >= 2) {
            int x = 5;
        }
    }
    """,
    """
    void main() {
        if (1 <= null) {
            int x = 5;
        }
    }
    """,
    # Logical operators must be bool
    """
    void main() {
        if (1 < 2 && 'a') {
            return;
        }
    }
    """,
    # Artithmetic operators must be int
    """
    void main() {
        1 + 'a';
    }
    """,
    """
    void main() {
        null - null;
    }
    """,
    """
    void main() {
        1 * true;
    }
    """,
    """
    void main() {
        1 / null;
    }
    """,
    """
    void main() {
        1 += true;
    }
    """,
    """
    void main() {
        1 -= null;
    }
    """,
    """
    void main() {
        1 *= true;
    }
    """,
    #Unary operators
    """
    void main() {
        +1;
    }
    """,
    """
    void main() {
        +true;
    } 
    """,
    """
    void main() {
        +"string";
    } 
    """,
    """
    void main() {
        -true;
    }
    """,
    """
    void main() {
        -"string";
    }
    """,
    """
    void main() {
        !1;
    }
    """,
    """
    void main() {
        !'a';
    }
    """,
    """
    void main() {
        !null;
    }
    """,
    # Invalid while statement
    """
    void main() {
        while (1) {
        }
    }
    """,
    """
    void main() {
        while ('a') {
        }
    }
    """,
    """
    void main() {
        while (null) {
        }
    }
    """,
    """
    void main() {
        while (true && 1) {
        }
    }
    """,
    # Invalid for statement
    """
    void main() {
        int i;
        for (i = 4; "CHEEEESE" ; i += 5) {}
    }
    """,
    """
    void main() {
        int i;
        for (i = 4; null ;) {}
    }
    """,
    """
    void main() {
        for (; null ;) {}
    }
    """,
    # Cout statements
    """
    void main() {
        cout << true;
        cout << bool;
    }
    """,
    """
    void main() {
        cout << null;
    }
    """,
    # Switch statement should have int | char expression
    """
    void main() {
        switch (true) {
            default:
                break;
        } 
    }
    """,
    """
    void main() {
        switch (null) {
            default:
                break;
        } 
    }
    """,
    """
    void main() {
        switch ("string") {
            default:
                break;
        } 
    }
    """,
    """
    void main() {
        int x;
        int y = 2;
        switch (y) {
            case 'a': 
                break;
            case 2:
                break;
            case 3:
                break;
            default:
                break;
        } 
    }
    """,
    # Function return types
    """
    class Cheese {
        static public char wee() {
            int x;
        }
    }
    void main() {}
    """,
    """
    class Cheese {
        static public int wee() {
            char x;
        }
    }
    void main() {}
    """,
    """
    class Cheese {
        static public int wee() {
            return;
        }
    }
    void main() {}
    """,
    #Invalid main return type
    """
    void main() {
        return 4;
    }
    """,
    """
    void main() {
        return 'a';
    }
    """,
    """
    void main() {
        return "string";
    }
    """,
    """
    void main() {
        return true;
    }
    """,
    """
    void main() {
        return null;
    }
    """,
    """
    void main() {
        int[] x = new int[][5];
    }
    """,
    """
    void main() {
        int[][][][][][] x = new int[][5];
    }
    """,
    """
    void main() {
        char[][] x = new int[][5];
    }
    """,
    # Ensure only nullptr can be a substitution for reference types
    """
    void main() {
        int x = null;
    }
    """,
    """
    void main() {
        char x = null;
    }
    """,
    """
    class Cheese {}
    void main() {
        Cheese x = void;
    }
    """,
    #Index access should return the enclosed type of the defined array
    """
    void main() {
        char[][] y = new char[][3];
        int[][] x = y[5];
    }
    """,
    """
    void main() {
        char[] y = new char[3];
        char[] x = y[5];
    }
    """,
    #Private function calls should fail in main, or other classes
    """
    class Cheese {
        private void Wee() {
        }
    }
    void main() {
        Cheese c = new Cheese();
        c.Wee();
    }
    """,
    # Test invalid params
    """
    class Cheese {
        public int Motz(int x, int y) {
            return x + y;
        }
    }
    void main() {
        Cheese c = new Cheese();
        int x = c.Motz(4, 'a');
    }
    """,
    #Can't use `this` within a static function
    """
    class Cheese {
        private int y = 2;
        static private int x = this.y;
        static private void failure() {
            this.x;
        }
    }
    void main() {}
    """,
    # Invalid index access
    """
    class Cheese {}
    void main() {
        int[] x = new int['a'];
    }
    """,
    """
    class Cheese {}
    void main() {
        int[] x = new int[true];
    }
    """,
    # Invalid constructor params
    """
    class Cheese {
        Cheese(int x) {}
    }
    void main() {
        Cheese c = new Cheese('a');
    }
    """,
    # Too few arguments
    """
    class Cheese {
        Cheese(int x, char y) {}
    }
    void main() {
        Cheese c = new Cheese(true);
    }
    """,
    """
    void main() {
        void x;
    }
    """,
    # LOL void arrays, get outta here
    """
    void main() {
        void[] x;
    }
    """
])
def test_invalid_types(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""


@pytest.mark.parametrize("input_string", [
    #Valid index access
    """
    void main() {
        int[] x = new int[1200];
    }
    """,
    """
    void main() {
     bool y = true;
    }
    """,
    """
    class Cheese {}
    void main() {
        Cheese c = new Cheese();
    }
    """,
    #If Statements
    """
    void main() {
        if (true) {
            int x = 5;
        }
    }
    """,
    #Logical operators
    """
    void main() {
        if (true && true) {
            int x = 5;
        }
    }
    """,
    #Relational operators
    """
    void main() {
        if (1 < 2) {
            int x = 5;
        }
    }
    """,
    """
    void main() {
        if (1 > 2) {
            int x = 5;
        }
    }
    """,
    """
    void main() {
        if (1 >= 2) {
            int x = 5;
        }
    }
    """,
    """
    void main() {
        if (1 <= 2) {
            int x = 5;
        }
    }
    """,
    #Logical operators
    """
    void main() {
        if (1 < 2 && 2 < 4) {
            return;
        }
    }
    """,
    """
    void main() {
        if (1 < 2 || 2 < 3002) {
            return;
        }
    }
    """,
    # Arithmetic operators must be int
    """
    void main() {
        1 + 2;
    }
    """,
    """
    void main() {
        1 - 2;
    }
    """,
    """
    void main() {
        1 * 2;
    }
    """,
    """
    void main() {
        1 / 2;
    }
    """,
    """
    void main() {
        1 += 2;
    }
    """,
    """
    void main() {
        1 -= 2;
    }
    """,
    """
    void main() {
        1 *= 2;
    }
    """,
    """
    void main() {
        1 /= 2;
    }
    """,
    """
    void main() {
        +'a';
    }""",
    """
    void main() {
        -1;
    }
    """,
    """
    void main() {
        !true;
    }
    """,
    """
    void main() {
        !false;
    }
    """,
    # While statement
    """
    void main() {
        while (true) {
        }
    }
    """,
    """
    void main() {
        while (3 < 4) {
        }
    }
    """,
    """
    void main() {
        while (!(1 < 3) && false) {
        }
    }
    """,
    # For statement
    """
    void main() {
        int i;
        for (i = 4; i < 10; i += 5) {}
    }
    """,
    """
    void main() {
        for (; false ;) {}
    }
    """,
    """
    void main() {
        int i;
        for (i = 4; i < 10; i += 5) {}
    }
    """,
    # cout statements
    """
    void main() {
        cout << 5;
    }
    """,
    """
    void main() {
        cout << "Cheese, really getting sick of all this cheese";
    }
    """,
    """
    void main() {
        cout << 'o';
    }
    """,
    # cin should take in int or char
    """
    void main() {
        int x;
        cin >> x;
    }
    """,
    """
    void main() {
        char x;
        cin >> x;
    }
    """,
    # Switch statement should have int | char expression
    """
    void main() {
        switch (4) {
            default:
                break;
        } 
    }
    """,
    """
    void main() {
        switch ('a') {
            default:
                break;
        } 
    }
    """,
    """
    void main() {
        int x;
        int y = 2;
        switch (y) {
            case 1: 
                break;
            case 2:
                break;
            case 3:
                break;
            default:
                break;
        } 
    }
    """,
    #Valid return types
    """
    class Cheese {
        static public int Wee() {
            int x;
            return x;
        }
    }
    void main() {}
    """,
    """
    class Cheese {
        static public char Wee() {
            char x;
            return x;
        }
    }
    void main() {}
    """,
    """
    class Cheese {
        static public void Wee() {
            return;
        }
    }
    void main() {}
    """,
    """
    class Cheese {
        static public void Wee() {
            return;
        }
    }
    void main() {}
    """,
    """
    class Cheese {
        static public void Wee() {
        }
    }
    void main() {}
    """,
    # Valid main return type
    """
    void main() {
        return;
    }
    """,
    """
    void main() {
    }
    """,
    """
    void main() {
        int[][] x = new int[][5];
    }
    """,
    #Ensure we can assign null to reference types
    """
    void main() {
        char[][] x = null;
    }
    """,
    """
    void main() {
        string x = null;
    }
    """,
    """
    class Cheese {}
    void main() {
        Cheese x = null;
    }
    """,
    #Ensure that index access returns the enclosed type of the defined array
    """
    void main() {
        char[][] y = new char[][3];
        char[] x = y[5];
    }
    """,
    """
    void main() {
        char[] y = new char[3];
        char x = y[5];
    }
    """,
    #Verify that function calls work
    """
    class Cheese {
        public int Motz() {
            return 4;
        }
    }
    void main() {
        Cheese c = new Cheese();
        int x = c.Motz();
    }
    """,
    """
    class Motz {
        public int Yeet() {
            return 4;
        }
    }

    class Cheese {
        private void Yeet() {
            Motz m = new Motz();
            int x = m.Yeet();
        }
    }
    void main() {}
    """,
    # Test valid params
    """
    class Cheese {
        public int Motz(int x, int y) {
            return x + y;
        }
    }
    void main() {
        Cheese c = new Cheese();
        int x = c.Motz(4, 5);
    }
    """,
    # We can call main in a block scope
    """
    class Cheese {
        public void Motz() {
            main();
        }
    }
    void main() {
        main();
    }
    """,
    # Support chained function calls
    """
    class Baz {
        public bool Foo(int y) {
            return true;
        }
    }

    class Motz {
        public Baz baz = new Baz();
        public Baz Cheeto() {
            return this.baz;
        }
    }
    void main() {
        Motz m = new Motz();
        bool continue = m.Cheeto().Foo(4);
    }
    """,
    # Chained member access off of a function call
    """
    class Baz {
        public int x = 4;
    }

    class Motz {
        public Baz baz = new Baz();
        public Baz Cheeto() {
            return this.baz;
        }
    }
    void main() {
        Motz m = new Motz();
        int continue = m.Cheeto().x;
    }
    """,
    # Private member acccess within a class
    """
    class Cheese {
    private int x;
        public int X() {
            this.x = 7;
            return this.x;
        }
    }
    void main() {}
    """,
    # Valid constructor params
    """
    class Cheese {
        Cheese(int x) {}
    }
    void main() {
        Cheese c = new Cheese(4);
    }
    """,
    """
    class Cheese {
        Cheese(int x, char y) {}
    }
    void main() {
        Cheese c = new Cheese(4, 'a');
    }
    """,
    """
    class Cheese {
        Cheese(int x, char y, string z) {}
    }
    void main() {
        Cheese c = new Cheese(4, 'a', "hello");
    }
    """,

])
def test_valid_types(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 0
    assert stderr == ""

@pytest.mark.parametrize("input_string", [
    """
    class Beans {
        static public int x = 4;
    }
    void main() {
        Beans.x;
        Beans.x;
    }
    """,
    """
    class Cheese {
        static private int x = 4;
        private void func() {
            this.x = 4;
        }
    }
    void main() {}
    """
    ])
def test_valid_static(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 0
    assert stderr == ""

@pytest.mark.parametrize("input_string", [
    # Because of the order of execution, non-static elemenents don't exist when
    # static elements are called
    """
    class Cheese {
        private int y = 2;
        static private int x = this.y; //this is not allowed
        private void failure() {}
    }
    void main() {}
    """])
def test_invalid_static(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""

@pytest.mark.parametrize("input_string", [
    """
    void main() {
        break;
    }
    """,
    """
    void main() {
        if (true) {
            break;
        }
    }
    """,
    """
    class Cheese {
        public void Motz() {
            break;
        }
    }
    """,])
def test_invalid_breaks(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""

@pytest.mark.parametrize("input_string", [
    """
    void main() {
        while (true) {
            break;
        }
    }
    """,
    """
    void main() {
        int i;
        for (i = 0; i < 5; i += 1) {
            break;
        }
    }
    """,
    """
    void main() {
        switch (4) {
            default:
                break;
        }
    }
    """,
    ])
def test_valid_breaks(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 0
    assert stderr == ""

#Invalid Writes
    

# Shared tests
@pytest.mark.parametrize(
    "input_string",
    [
    # Duplicate variable declarations
    """
    void main() {
        int x = 5;
        int x = 2; 
    }
    """,
    # Invalid if statements
    """
    void main() {
        if (x = 3) {
            int x = 5;
        }
    }
    """,
        """
    void main() {
        int x = 3;
        if (x) {
            int b = 5;
        }
    }
    """,
        # Invalid if statement with assignment instead of comparison
        """
    void main() {
        bool x = true;
        if (x - x && x) {
            int b = 5;
        }
    }
    """,
        # If statement with wrong datatype comparison
    """
    void main() {
        int x = 5;
        char y = 'y';
        if (x < 5 && y == 5) {
            cout << "x is less than 5 and y";
        }
    }
    """,
        # Break statement outside of loop or switch
        """
    void main() {
        break;
    }
    """,
        # Break statement inside an if not inside a loop
    """
    void main() {
        if (true) {
            break;
        }
    }
    """,
        # Invalid cin statement
    """
    void main() {
        cin >> x;
    }
    """,
        # Invalid write statements
    """
    void main() {
        int x = 5;
        x = true;
    }
    """,
    """
    void main() {
        bool x = true;
        x = 5 + 5;
    }
    """,
        # Expression with undeclared variable
    """
    void main() {
        int x = 5;
        int y = x + z;
    }
    """,
        # Invalid cout statements
    """
    void main() {
        int x = 5;
        cout << x + true; 
    }
    """,
        # Cin >> string and cin >> bool
    """
    void main() {
        string x;
        cin >> x;
        bool y;
        cin >> y;
    }
    """,
    """
    void main() {
        char x = 'a';
        int y = 5;
        if (x < y) {
            cout << "x is less than y";
        }
    }
    """,
        # Invalid use of unary operator
    """
    void main() {
        bool x = true;
        x = -x;
        int y = 5;
        y = !y;
    }
    """,
        # Assign null to literal
    """
    void main() {
        int x = null;
    }
    """,
        # Unary NOT operator on a non-boolean
    """
    void main() { 
        int x = 5;
        if (!(x + 3)) {
            cout << "x is not equal to 5";
        }
    }
    """,
        # Adding a char to an int, and a bool to an int
    """
    void main() {
        int x = 5;
        char y = 'a';
        int z = x + y;
    }
    """,
    """
    void main() {
        int x = 5;
        bool y = true;
        int z = x + y;
    }
    """,
    # Comparisons of different types
    """
    void main() {
        int x = 5;
        char y = 'a';
        string z = "hello";
        bool a = true;
        if (x < y) {
            cout << "x is less than y";
        }
        if (x < z) {
            cout << "x is less than z";
        }
        if (x < a) {
            cout << "x is less than a";
        }
        while (x < y) {
            cout << "x is less than y";
        }
    }
    """,
        # Unary NOT operator that's not on a boolean
    """
    void main() {
        int x = 5;
        bool y = !x;
        char z = 'a';
        bool a = !z;
        string b = "hello";
        bool c = !b;
    }
    """,
    # Unary MINUS operator on types other than int
    """
    void main() {
        char x = 'a';
        int y = -x;
        string z = "hello";
        int a = -z;
        bool b = true;
        int c = -b;
    }
    """,
    ],
)
def test_type_checker_fail(input_string: str) -> None:
    """Test the type checker with expected failures."""
    _, _, returncode = run_parser(input_string)
    assert returncode != 0, "Expected an error but none was thrown."


@pytest.mark.parametrize(
    "input_string",
    [
    # Valid if statement where ID is a bool
    """
    void main() {
        bool x = true;
        if (x) {
            int b = 5;
        }
    }
    """,
    # Valid if statement with conditional && or ||
    """
    void main() {
        bool x = true;
        if (x && x || x && x) {
            int c = 5;
        }
        if (x || x) {
            int b = 5;
        }
    }
    """,
    # Multiple conditional statements
    """
    void main() {
        bool x = true;
        if (x && x || x && x) {
            int c = 5;
        }
        if (x || x) {
            int b = 5;
        }
    }
    """,
    # Break statements inside loops
    """
    void main() {
        int i;
        while(true) {
            break;
        }
        for (i = 0; i < 5; i += 1) {
            break;
        }
    }
    """,
    # Break statement has embedded if
    """
    void main() {
        int i;
        while(true) {
            if (true) {
                break;
            }
        }
        for (i = 0; i < 5; i += 1) {
            if (true) { 
                if (true) {
                    break;
                }
            }
        }
    }
    """,
    # Valid cin statements with valid types
    """
    void main() {
        int x;
        cin >> x;
        char a;
        cin >> a;
    }
    """,
    # Valid write statement
    """
    void main() {
        int x = 5;
        x = 5;
        x = 5 + 5;
    }
    """,
    # Valid variable declarations
    """
    void main() {
        int x = 5;
        bool y = true;
        string z = "hello";
        char a = 'a';
    }
    """,
    # Expression with variable declared in the symbol table
    """
    void main() {
        int x = 5;
        int y = x + x;
        int z = y + x;
    }
    """,
    # Valid cout statement with 2 valid identifiers
    """
    void main() {
        int x = 5;
        int y = 5;
        cout << x + y; 
    }
    """,
    # Valid cout statement
    """
    void main() {
        int x = 5;
        cout << x + 5 + 5;
    }
    """,
    # Valid cout statements based on type
    """
    void main() {
        int x = 5;
        char y = 'a';
        string z = "hello";
        cout << x;
        cout << y;
        cout << z;
    }
    """,
    # Cin >> int and cin >> char
    """
    void main() {
        int x;
        cin >> x;
        char y;
        cin >> y;
    }
    """,
    # Relational comparison of two chars
    """
    void main() {
        char x = 'a';
        char y = 'b';
        if (x < y) {
            cout << "x is less than y";
        }
    }
    """,
    # Unary NOT operator on an equality expression
    """
    void main() {
        int x = 5;
        bool y = true;
        if (!(x == 5)) {
            cout << "x is not equal to 5";
        }
        if (!(y == true)) {
            cout << "y is not equal to true";
        }
    }
    """,
    # Adding two ints
    """
    void main() {
        int x = 5;
        int y = 5;
        int z = x + y;
    }
    """,
    # Expression with multiple ints
    """
    void main() {
        int x = 5;
        int y = 5;
        int a = 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5;
        int b = x + y + x + y + a + a + x + y;
        int z = x + y + 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5;
    }
    """,
    # Comparison of two ints
    """
    void main() {
        int x = 5;
        int y = 5;
        if (x < y) {
            cout << "x is less than y";
        }
    }
    """,
    # Comparison of two chars
    """
    void main() {
        char x = 'a';
        char y = 'b';
        if (x < y) {
            cout << "x is less than y";
        }
    }
    """,
    # Unary PLUS operator on a char
    """
    void main() {
        char x = 'a';
        int y = +x;
    }
    """,
    # Unary NOT operator on a boolean
    """
    void main() {
        bool f = false;
        bool t = !f;
    }
    """,
    ],
)
def test_type_checker_success(input_string: str) -> None:
    """Test the type checker with expected successes."""
    _, _, returncode = run_parser(input_string)
    assert returncode == 0, "Expected no error but an error was thrown."