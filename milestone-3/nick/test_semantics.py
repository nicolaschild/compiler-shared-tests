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
        # Should fail on variable declaration, not constructor declaratio
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
                this.x = 4;
                return;
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
        cout << false;
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
    """,
    #Constructors can only return void
    """
    class Cheese {
        Cheese(int x, char y, string z) {
            return 4;
        }
    }
    void main() {
        Cheese c = new Cheese(4, 'a', "hello");
    }
    """,
    # Regular function call invalid params
    """
    class Cheese {
    public void Func(int y, int x, char b) {
        return Func(y, x, 7);
        }
    }

    void main() {
        Cheese c = new Cheese();
    }
    """,
])
def test_invalid_types(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""


@pytest.mark.parametrize("input_string", [
    #Constructors can only return void
    """
    class Cheese {
        private int x;
        private char y;
        private string z;
        Cheese(int x, char y, string z) {
            this.x = x;
            this.y = y;
            this.z = z;
            return;
        }
    }
    void main() {
        Cheese c = new Cheese(4, 'a', "hello");
    }
    """,
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
    """
    class Foo {
        private void Test() {
            Cheese;
        }
    }
    class Cheese {}
    void main(){}
    """,
    # Valid param types for function calls
    """
    class Cheese {
        public void Func2(int x, int y, char b) {}
        public void Func(int y, int x, char b) {
            return Func2(y, x, b);
        }
    }

    void main() {
        Cheese c = new Cheese();
    }
    """,
    # Recursive function calls with valid param types
    """
    class Cheese {
        public void Func(int y, int x, char b) {
            return Func(y, x, b);
        }
    }

    void main() {
        Cheese c = new Cheese();
    }
    """,
    #Null is a valid substitution for reference type string
    """
    void main() {
        cout << null;
    }
    """,
    """
    class Booz {
        public int pleaseWork() {
            return 1;
        }
    }

    class Cheese {
        static public Booz b;
        static public void cheddar() {
            b.pleaseWork();
        }
    }

    void main() {}
    """
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
    """,
    # Static functions can declare variables. They can also access static variables
    """
    class Cheese {
        public int x = 4;
        static public int cheddar() {
            int x = 4;
            return x;
        }
    }
    void main() {}
    """,
    # Static functions can access static variables
    """
    class Cheese {
        static public int x = 4;
        static public int cheddar() {
            return x;
        }
    }
    void main() {}
    """,
    # Static functions calling other static functions OK
    """
    class Booz {
        static public int pleaseWork() {
            return 1;
        }
    }

    class Cheese {
        static public Booz b;
        static public void cheddar() {
            b.pleaseWork();
        }
    }

    void main() {}
    """,
    #Function creates a new object, it becomes unstatic
    """
    class Booz {
        static public MyClass myfunc() {
            return new MyClass();
        }
    }
    class MyClass {
        public int x;
        static public Booz b;
    }
    void main() {
        MyClass.b.myfunc().x;
    }
    """,
    # We aren't doing a control flow graph so this should pass, we default initialize Beeze
    """
    class Beeze {
        public int z = 2;
    }
    class Cheese {
        static public Beeze b;
        static public int x = b.z;
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
    """,
    #Static functions can't access non-static data members
    """
    class Cheese {
        public int x = 4;
        static public int cheddar() {
                return x;
        }
    }
    void main() {}
    """,
    #Static class references have no clue what you're talking about (non-static hasn't been initialized yet)
    """
    class Booz {}
    class MyClass {
        public Booz b;
    }
    void main() {
        MyClass.b;
    }
    """
    ])
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
    void main() {}
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
    # Void cannot be used as a type for params
    """
    class Cheese {
        public int motz(void x) {
            return 2;
        }
    }
    void main() {
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

# More shared tests (should fail)
@pytest.mark.parametrize("input_string", [
    # Bad assignment
    """
    void main() {
        int x = 1;
        char y = 'c';
        string z = "string";
        bool b = true;
        x == y;
        z <= "string";
        b >= false;
    }
    """,
    # Invalid params
    """
    class MyClass {
        static public void func(int a, char b) {}
    }    
    void main(){
        MyClass.func('c', 1);
        MyClass.func();
    }
    """,
    # Bad binary type check
    """
    void main(){
        char x = 'c';
        int y = x + 2;
        int z = y - x * 3;
    }
    """,
    # Bad comp type check
    """
    void main(){
        int x = 1;
        char y = 'c';
        string z = "string";
        bool b = true;
        x == y;
        z <= "string";
        b >= false;
    }
    """,
    # Bad dec type check
    """
    void main() { 
        bool x = 1;
        int y = 'c';
        char z = "string";
        string b = true;
    }
    """,
    # Bad io type check
    """
    void main(){
        string x;
        cin >> x;
        cout << true;
    }
    """,
    # Bad logic type check
    """
    void main(){
        int x = 1;
        x >= 1 || 5;
        "apple" && x == 1;
    }
    """,
    # Bad loop type check
    """
    void main(){
        while ('c') {
            for (;1+1;) {
                if (null) {}
            } 
        }
    }
    """,
    # Bad return type check
    """
    class MyClass {
        static public int func(){
            return 'c';
        }
        static public int func2(){}
        static public void func3(){
            return 1;
        }
    }    
    void main(){}
    """,
    # Bad switch type
    """
    void main(){
    int x = 1;
    switch (x) {
        case 'c': x = x+1;
        case 2: x = x+2;
        default: x = x;
    }
    }
    """,
    # Bad unary type check
    """
    void main() {
        int x = -1;
        bool y = true;
        +y;
        !x;
    }
    """,
    # Double declared constructor
    """
    class MyClass { 
        public int x;
        static public char y;
        MyClass(int a, int b) {}
        public int[] myfunc() {}
        MyClass() {}
    }
    void main(){}
    """,
    # Double declared data
    """
    class MyClass { 
        public int x;
        static public char x;
        MyClass(int a, int b) {}
        public int[] myfunc() {}
    }
    void main(){}
    """,
    # Double declared function
    """
    class MyClass { 
        public int x;
        static public char y;
        MyClass(int a, int b) {}
        public int[] myfunc() {}
        public string myfunc() {}
    }
    void main(){}
    """,
    """
    class main { 
        public int x;
        static public char y;
        main(int a, int b) {}
        public int[] myfunc() {}
    }
    void main() {}
    """,
    # Double declared mix
    """
    class MyClass { 
        public int x;
        static public char y;
        MyClass(int a, int b) {}
        public int[] myfunc() {}
        public string x() {}
    }
    void main(){}
    """,
    # Double declared parameter
    """
    class MyClass { 
        public void myfunc(int x) {
            string x = "oops";
        }
    }
    void main(){}
    """,
    # Double declared variable
    """
    void main(){
        int j = 4;
        char j = 'j';
    }
    """,
    # Invalid Constructor
    """
    class MyClass { 
        public int x;
        static public char y;
        derp(int a, int b) {}
        public int[] myfunc() {}
    }
    void main(){}
    """,
    # Invalid data member access
    """
    class MyClass {
        public int x;
    }
    void main(){
        MyClass c = new MyClass();
        int y = c.q;
    }
    """,
    # Constructor param check
    """
    class MyClass {
        MyClass(int a, char b) {}
    }    
    void main(){
        MyClass A = new MyClass('c', 1);
        MyClass B = new MyClass();
    }
    """,
    # Non instanced non-static member reference / call
    """
    class MyClass {
        public int x;
        public int myfunc() {
            return x + 1;
        }
    }
    void main(){
        MyClass.x = MyClass.myfunc();
    }
    """,
    # Non-static in static
    """
    class MyClass {
        public int x;
        static public int myfunc() {
            return x + 1;
        }
    }
    void main(){}
    """,
    # Invalid scopes
    """
    class MyClass { 
        public void myfunc(int x) {
            return j + 1;
        }
    }
    void main(){
        int j = 4;
    }
    """,
    # Ensure scope looks to parent
    """
    void main(){
    {
        int y = 6;
    }
        y = 4;
    }
    """,
    # This in static function
    """
    class MyClass {
        public int x;
        static public int myfunc() {
            return this.x + 1;
        }
    }
    void main(){}
    """,
    #This in static declaration
    """
    class MyClass {
        private int x = 4;
        static private int y = this.x + 1;
    }
    void main(){}
    """
])

def test_invalid_types_shared(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""

@pytest.mark.parametrize("input_string", [
    # Args type check
    """
    class MyClass {
        static public void func(int a, char b) {}
    }    
    void main(){
        MyClass.func(1, 'c');
    }
    """,
    # Assign type check
    """
    void main() {
        int x;
        char y;
        string z;
        bool b;
        x = 1;
        y = 'c';
        z = "string";
        b = true;
    }
    """,
    # Binary type check
    """
    void main(){
        int x = 1;
        int y = x + 2;
        int z = y - x * 3;
    }
    """,
    # Class scope
    """
    class MyClass { 
        public int x;
        static public char y;
        MyClass(int a, int b) {}
    }
    class MyClass2 { 
        public int x;
        static public char y;
        MyClass2(int a, int b) {}
    }
    void main(){}
    """,
    # Comparison type check
    """
    void main(){
        int x = 1;
        char y = 'c';
        string z = "string";
        bool b = true;
        x >= 1;
        y <= 'a';
        z == "string";
        b != false;
    }
    """,
    # Declaration type check
    """
    void main() {
        int x = 1;
        char y = 'c';
        string z = "string";
        bool b = true;
    }
    """,
    # Dot operator type check
    """
    class MyClass {
        public int x = 4;
        public void func() {}
    }    
    void main(){
        MyClass A = new MyClass();
        A.func();
        int x = A.x;
    }
    """,
    # Indexed type check
    """
    void main(){
        int[][][] x = new int[][][10];
        x[0] = new int[][10];
        x[0][1] = new int[10];
        x[0][1][2] = 1;
        int y = x[0][1][2];
    }
    """,
    # Instanced dot operator type check
    """
    class MyClass {
        public int x;
    }
    void main(){
        MyClass c = new MyClass();
        int y = c.x;
    }
    """,
    # Instanced static member
    """
    class MyClass {
        static public int x;
    }
    void main(){
        MyClass c = new MyClass();
        int y = c.x;
    }
    """,
    # IO type check
    """
    void main(){
        int x;
        char y;
        cin >> x;
        cin >> y;
        cout << 'c';
        cout << 1;
        cout << "thing";
    }
    """,
    # Logic type check
    """
    void main(){
        int x = 1;
        char y = 'c';
        x >= 1 || x <= 1;
        x == 1 && y == 'c';
    }
    """,
    # Loop type check
    """
    void main() {
        int x = 0;
        while (true) {
            for (x=10;x>0;) {
                if (x > 0) {
                    x = x - 1;
                }
            } 
        }
    }
    """,
    # Main callable
    """
    class MyClass {
        static public void myfunc() {
            main();
        }
    }
    void main(){}
    """,
    # Nested dot
    """
    class MyClass {
        public int x;
        static public MyClass myfunc() {
            return new MyClass();
        }
    }
    void main(){
        MyClass.myfunc().x;
    }
    """,
    # Nested dot 2
    """
    class MyClass {
        public int x = 4;
        public void func() {}
    }
    class MyClass2 {
        public MyClass func() {
            MyClass c = new MyClass();
            return c;
        }
    }   
    void main(){
        MyClass2 A = new MyClass2();
        int x = A.func().x;
    }
    """,
    # Constructor params type check
    """
    class MyClass {
        MyClass(int a, char b) {}
    }    
    void main(){
        MyClass A = new MyClass(1, 'c');
    }
    """,
    # New index type check
    """
    void main() {
        int[][][] x = new int[][][10];
    }
    """,
    # Return type check
    """
    class MyClass {
        static public int func(){
            return 1;
        }
        static public void func2(){}
        static public void func3(){
            return;
        }
    }    
    void main(){}
    """,
    # Class Scope
    """
    class MyClass { 
        public int x;
        MyClass(int a, int b) {}
        public void myfunc() {
            x = 4;
        }
    }
    void main(){}
    """,
    # Function Scope
    """
    class MyClass { 
        public void myfunc() {
            int x = 4;
            x = 5;
        }
    }
    void main(){}
    """,
    # Param Scope
    """
    class MyClass {
        public int myfunc(int x) {
            return x + 1;
        }
    }
    void main(){}
    """,
    # Static in static
    """
    class MyClass {
        static public int x;
        static public int myfunc() {
            return x + 1;
        }
    }
    void main(){}
    """,
    # Static method call
    """
    class MyClass {
        static public int x;
        static public int myfunc() {
            return x + 1;
        }
    }
    void main(){
        MyClass.x = MyClass.myfunc();
    }
    """,
    # Switch
    """
    void main(){
        int x = 1;
        char y = 'c';
        switch (x) {
            case 1: x = x+1;
            case 2: x = x+2;
            default: x = x;
        }
        switch (y) {
            case 'c': true;
            case 'q': false;
            default: false;
        }
        switch (x) {
            default: x = 0;
        }
    }
    """,
    # This in non-static declaration
    """
    class MyClass {
        private int x = 4;
        private int y = this.x + 1;
    }
    void main(){}
    """,
    # Unary type check
    """
    void main(){
        int x = -1;
        bool y = true;
        x = +x;
        !y;
    }
    """,
    """
    class MyClass {
        static public int x;
        static public MyClass myfunc() {
            MyClass x = new MyClass();
            return x;
        }
    }

    void main() {
        MyClass.myfunc();
    }
    """,
    # We can always reference a class name
    """
    class MyClass {
        static public int x;
        static public MyClass myfunc() {
            return new MyClass();
        }
    }

    void main() {
        MyClass.myfunc();
    }
    """,
    """
    class MyClass {
        static public int x;
        static public void myfunc() {
            MyClass;
        }
    }

    void main() {
        MyClass;
    }
    """,
    # Can return function calls of the same return type
    """
    class MyClass {
        public int x;
        public void myfunc() {
            return main();
        }
        MyClass() {}
    }
    void main(){}
    """,
    """
    class MyClass {
        public int x;
        public void myOtherFunc () {
            x = 4;
        }

        public void myfunc(int x, int y) {
            myfunc(1, 5);
            myOtherFunc();
        }
    }
    void main() {
    }
    """,
    # Can change a value from yonder as long as the types match
    """
    class Chooz {
        static public int y = 5;
        static public int Func() {
            return 3;
        }
    }
    class Booz {
        static public Chooz c;
        static public int Func() {
            return 4;
        }
    }
    class Cheese {
        static public Booz b;
        public int Func() { 
            return 4;
        }
    }
    void main() {
        Cheese.b.c.y = 4;
    }
    """,
])

def test_valid_types_shared(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 0
    assert stderr == ""

#Invalid Writes
@pytest.mark.parametrize("input_string", [
    # Only have to worry about items of the same type or unification
    """
    void main() {
        4 = 3;
    }
    """,
    """
    void main() {
        "string" = null;
    }
    """,
    """
    void main() {
        null = null;
    }
    """,
    """
    void main() {
        true = false;
    }
    """,
    # Can't reassign a class definition
    """
    class MyClass {
        public int x;
        public int myfunc() {
            return 1;
        }
    }
    void main() {
        MyClass = MyClass;
    }
    """,
    # Can't assign to a function call
    """
    class MyClass {
        public int x;
        public int myfunc() {
            return x + 1;
        }
    }
    void main() {
        MyClass.myfunc() = 4;
    }
    """,
    # Can't return functions
    """
    class MyClass {
        public int x;
        public void myfunc() {
            return main;
        }
        MyClass() {}
    }
    void main() {}
    """,
    # Data member access not on a class, probably will fail in type checking
    # But make sure you have a nice error message instead of your program blowing up
    """
    class MyClass {
        public int x;
        public void myfunc() {
            return main.x;
        }
        MyClass() {}
    }
    void main(){
    }
    """,
    # Handle a graceful error for a function call in main that's not main
    """
    class MyClass {
        public int x;
        public void myfunc(int x, int y, int z) {
            myfunc(1, 2, 3); 
        }
        MyClass() {}
    }

    void main(){
        myfunc(1, 2, 3);
    }
    """,
    # Don't crash, give me a good error pal
    """
    class Cheese {
        public void Func() {}
    }
    void main() {
        c.Func();
    }
    """,
    # New cannot be written to
    """
    void main() {
        new Cheese() = new Cheese();
    }
    """,
    #LHS can't be a function call/reference, no matter how chained
    """
    class Chooz {
        static public int y = 5;
        static public int Func() {
            return 3;

        }
    }
    class Booz {
        static public Chooz c;
        static public int Func() {
            return 4;
        }
    }

    class Cheese {
        static public Booz b;
        public int Func() { 
            return 4;
        }
    }
    void main() {
    Cheese.b.c.Func = 4;
    }
    """,
    """
    class Chooz {
        static public int y = 5;
        static public int Func() {
            return 3;

        }
    }
    class Booz {
        static public Chooz c;
        static public int Func() {
            return 4;
        }
    }

    class Cheese {
        static public Booz b;
        public int Func() { 
            return 4;
        }
    }
    void main() {
        Cheese.b.c.Func() = 4;
    }
    """
    ])

def test_invalid_writes(input_string: str) -> None:
    """Test the semantics of the input string"""
    _, stderr, returncode = run_parser(input_string)
    assert returncode == 1
    assert stderr == ""
