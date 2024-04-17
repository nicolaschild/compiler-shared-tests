tests = [
    """
    void main() {
    cout << "\\\"    im spaced out    \\\"";
    }
    ---
    "    im spaced out    "
    """,
    """
    class Cheddar {
        static public int y = 1;
        static public int x = x + y + 1;
    }
    void main() {
        cout << Cheddar.y;
        cout << Cheddar.x;
    }
    ---
    12
    """,
    """
    class Beeze {
    static public void fun(){
        int x;
        cout << x;
        x = 14;// set x location on the stack
        }
    }

    void main() {
        Beeze.fun();
        Beeze.fun();
    }
    ---
    00
    """,
    """
    class Cheese {
        static public void print(int x, int y) {
            cout << x;
            cout << y;
        }
    }

    void main() {
        Cheese.print(3, 4);
    }
    ---
    34
    """,
    """
        void main(){
            int c = 2;
            c < 2 || (c += 5) < 2;
            cout << c;
            }
        ---
        7
    """,
    """
    void main(){
        int c = 2;
        false && (c += 1) > 2;// false and true
        cout << c;
        }
    ---
    2
    """,
    """
    void main(){
        int c = 2;
        true && false || (c += 1) > 2;// false and true
        cout << c;
    }
    ---
    3
    """,
    """
    void main() {
        int c = 2;
        false && (c += 2) > 2;// false and true
        cout << c;
    }
    ---
    2
    """,
    """
    void main() {
        int c = 2;
        true && (c += 2) > 2;// true and false
        cout << c;
    }
    ---
    4
    """,
    """
    void main(){
        int n = 3;
        int t = 3;
        (n += 1) > 3 || (t += 2) > 3;
        cout << n;
        cout << t;
    }
    ---
    43
    """,
    """
    void main() {
        int n = 3;
        int t = 3;
        (n += 1) == 4 || (t += 2) > 2;
        cout << n;
        cout << t;
        }
    ---
    43
    """,
    """
        void main(){
            int n = 1;
            switch(n){
                case 1:
                    cout << "one";
                    break;
                case 2:
                case 3:
                    cout << "two or three";
                    break;
                default:
                    cout << "a number not in the range of 1 to 3";
                    break;
                }
            }
        ---
        one
    """,
    """
    void main(){
        int n = 2;
        switch(n){
            case 1:
                cout << "one";
                break;
            case 2:
            case 3:
                cout << "two or three";
                break;
            default:
                cout << "a number not in the range of 1 to 3";
                break;
        }
    }
    ---
    two or three
    """,
    """
    void main(){
        int n = 0;
        switch(n){
            case 1:
                cout << "one";
                break;
            case 2:
            case 3:
                cout << "two or three";
                break;
            default:
                cout << "a number not in the range of 1 to 3";
                break;
        }
    }
    ---
    a number not in the range of 1 to 3
    """,
    """
    void main(){
        int n = 2;
        switch(n){
            case 1:
                cout << "one";
                break;
            case 2:
            case 3:
                switch (n) {
                    case 2:
                        cout << "two";
                        break;
                    case 3:
                        cout << "three";
                        break;
                    default:
                        cout << "something else";
                        break;
                }
                break;
            default:
                cout << "outer something else";
                break;
        }
    }
    ---
    two
    """,
    """
    void main(){
        if (false) {
            cout << "upper";
        } 
        else {
            cout << "lower";
        }
    }
    ---
    lower
    """,
    """
    void main() {
        bool x = 1 < 5 || false;
        if(x) {
            cout << "upper";
        }
        else {
            cout << "lower";
        }
    }
    ---
    upper
    """,
    """
    void main() {
        int x = 10;
        while(x > 0) {
            cout << x;
            x = x - 1;
        }
    }
    ---
    10987654321
    """,
    """
    void main() {
        int x = 10;
        while (x > 0){
            cout << x;
            //RHS should never evaluate, if it does, this is an infinite loop (you're welcome if this broke lol)
            true || x < (x += 10);
            x = x - 1;
        }
    }
    ---
    10987654321
    """,
    """
    void main() {
        cout << "Hello World!";
    }
    ---
    Hello World!
    """,
    """
    void main() {
        int x = 0;
        if(1 < x){
            cout << "This should not print";
        } else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if(x < 1) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if (x > 1) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }   
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if (1 > x) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if(x == 0) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }   
    ---
    This should print
    """,
    """
    void main() {
        int x = 1;
        if (0 == x) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if (x != 1) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 1;
        if (1 != x) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if (x == 0) {
            if (x == 0) {
                cout << "This should print";
            }
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if (x == 0) {
           if (x == 0) {
                if (x == 0) {
                    cout << "This should print";
                }
            }
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if (x != 0) {
            cout << "This should not print";
        }
        else {
            if(x == 0) {
               cout << "This should print";
            }
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 0;
        if  (x != 0) {
            cout << "This should not print";
        }
        else {
            if (x != 0) {
                cout << "This should not print";
            }
            else {
                cout << "This should print";
            }
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int i = 0;
        for (i = 0; i < 5; i = i + 1) {
            cout << i;
        }
    }
    ---
    01234
    """,
    """
    void main() {
        int i = 0;
        for(; i < 5; i = i + 1){
            cout << i;
        }
    }
    ---
    01234
    """,
    """
    void main() {
        int i = 0;
        for (; i < 5;) {
            cout << i;
            i = i + 1;
        }
    }
    ---
    01234
    """,
    """
    void main() {
        int i = 0;
        for(; i < 5;){
            cout << i;
            i = i + 1;
            if (i == 3) {
                break;
            }
        }
    }
    ---
    012
    """,
    """
    //00 01 02 10 12 20 21 22
    void main() {
        int i = 0;
        for(; i < 3; i = i + 1){
            int j = 0;
            for(; j < 3; j = j + 1){
                cout << i;
                cout << j;
            }
        }
    }
    ---
    000102101112202122
    """,
    """
    //00 01 10 11 20 21
    void main() {
        int i = 0;
        for (; i < 3; i = i + 1) {
            int j = 0;
            for (; j < 3; j = j + 1) {
                cout << i;
                cout << j;
                if (j == 1) {
                    break;
                }
            }
        }
    }
    ---
    000110112021
    """,
    """
    void main() {
        int i = 0;
        while (i < 5)  {
            cout << i;
            i = i + 1;
        }
    }
    ---
    01234
    """,
    """
    // 00 01 02 10 11 12 20 21 22
    void main() {
        int i = 0;
        while (i < 3)  {
            int j = 0;
            while (j < 3)  {
                cout << i;
                cout << j;
                j = j + 1;
            }
            i = i + 1;
        }
    }
    ---
    000102101112202122
    """,
    """
    //001020
    void main() {
        int i = 0;
        while (i < 3)  {
            int j = 0;
            while (j < 3)  {
                cout << i;
                cout << j;
                j = j + 1;
                if (j == 1) {
                    break;
                }
            }
            i = i + 1;
        }
    }
    ---
    001020
    """,
    """
    void main() {
        int x = 1;
        int y = 2;
        int z = x + y;
        cout << z;
    }
    ---
    3
    """,
    """
    void main() {
        int x = 1;
        int y = 2;
        {
            int z = x + y;
            {
                int a = z + x;
                {
                    cout << a;
                }
            }
        }
    }
    ---
    4
    """,
    """
    void main() {
        int x = 1 - 3 * 2 / 2 + 1;
        cout << x + 12; 
    }
    ---
    11
    """,
    """
    void main() {
        int x = 1;
        int y = 2;
        int z = 3;
        cout << x + y * z;
    }
    ---
    7
    """,
    """
    void main() {
        int x = 1;
        x -= 1;
        cout << x;
    }
    ---
    0
    """,
    """
    void main() {
        int x = 1;
        x += 1;
        cout << x;
    }
    ---
    2
    """,
    """
    void main() {
        int x = 2;
        x /= 2;
        cout << x;
    }
    ---
    1
    """,
    """
    void main() {
        int x = 2;
        x *= 2;
        cout << x;
    }
    ---
    4
    """,
    """
    void main() {
        if (!false) {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if(!!true) {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if (true && true){
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if (false && true) {
            cout << "This should not print";
        }
    }
    ---
    """,
    """
    void main() {
        if (true || false){
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if(false || false){
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if(true && true || false) {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if (true && false || false) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    # Test -=
    """
    void main() {
        int x = 10;
        x -= 5;
        cout << x;
    }
    ---
    5
    """,
    """
    void main() {
        int x = 500;
        x -= 500;
        cout << x;
    }
    ---
    0
    """,
    # You should be default initalizing things to 0
    """
    void main() {
        int y = 5;
        int x = 10;
        int z;
        z += x;
        cout << z;
    }
    ---
    10
    """,
    # Test *=
    """
    void main() {
        int x = 10;
        x *= 5;
        cout << x;
    }
    ---
    50
    """,
    # Test /=
    """
    void main() {
        int x = 10;
        x /= 5;
        cout << x;
    }
    ---
    2
    """,
    # Test < w/ one variable
    """
    void main() {
        int x = 1100;
        if (1000 < x) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    # Test < w/ two variables
    """
    void main() {
        int x = 4;
        int y = 5;
        if (x < y) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    # Some more but with orders reversed, just to be safe
    """
    void main() {
        if (10 < 3) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        if (1 < 12) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    # These are equal, should not pass
    """
    void main() {
        if (1 < 1) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    # Test >
    """
    void main() {
        int x = 1100;
        if (x > 1000) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    void main() {
        int x = 4;
        int y = 5;
        if (y > x) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    // 1 > 0
    void main() {
        if (10 > 3) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        
        }
    }
    ---
    This should print
    """,
    """
    // 1 > 0
    void main() {
        if (12 > 1) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    // These are equal, should not pass
    void main() {
        if (1 > 1) {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
    ---
    This should print
    """,
    # Test unaries
    """
    // ! inline
    void main() {
        if (!false) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    // ! variable
    void main() {
        bool x = false;
        if (!x) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    //! nested inline
    void main() {
        if (!!true) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    //! nested variable
    void main() {
        bool x = true;
        if (!!x) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    //One crazy example just for fun
    void main() {
        if (!false && !!true) {
            cout << "I should print";
        }
        else {
            cout << "I should not print";
        }

    }
    ---
    I should print
    """,
    """
    //One crazy example just for fun
    void main() {
        if (!false && !true) {
            cout << "I should not print";
        }
        else {
            cout << "I should print";
        }

    }
    ---
    I should print
    """,
    # Test unary +
    """
    void main() {
        char x = 'a';
        cout << +x;
    }
    ---
    97
    """,
    """
    void main() {
        char x = 'a';
        cout << +x + 1;
    }
    ---
    98
    """,
    """
    void main() {
        char x = 'a';
        cout << +++++++x;
    }
    ---
    97
    """,
    # Test unary -
    """
    void main() {
        char x = 'a';
        cout << -+x;
    }
    ---
    -97
    """,
    """
    void main() {
        int x = --4;
        cout << x;
    }
    ---
    4
    """,
    """
    void main() {
        int x = 4;
        cout << -x;
    }
    ---
    -4
    """,
    """
    void main() {
        int x = 4 - -3;
        cout << x;
    }
    ---
    7
    """,
    """
    void main() {
        int x = -4 + -3;
        cout << x;
    }
    ---
    -7
    """,
    """
    void main() {
        if (-4 < 3) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    """
    //Testing null
    void main() {
        string x = null;
        string y;
        if (x == y) {
            cout << "This should print";
        }
        else {
            cout << "This should not print";
        }
    }
    ---
    This should print
    """,
    # The example Aldous put in Teams
    """
    //Aldous put this example in teams
    void main() {
        int y = 3;
        cout << (y = 1) + (y = 2);
        cout << y;
    }
    ---
    32
    """,
    """
    class Cheese {
        static public int x = 3;
        static public void count() {
            cout << x;
            x = Cheese.x -1;
            if (Cheese.x != 0) {
                count();
            }
        }
    }
    void main() {
        Cheese.count();
    }
    ---
    321
    """,
    # Test static member functions returning data members
    """
    class Cheese {
        static public char y = 'a';
        static public char aye() {
            return y;
        }
    }
    void main() {
        cout << Cheese.aye();
    }
    ---
    a
    """,
    """
    class Beez {
        static public int x = 4;
    }
    class Cheese {
        static public int y = 3;
    }
    void main() {
        cout << Beez.x + Cheese.y;
    }
    ---
    7
    """,
    """
    //First 10 fibonacci numbers
    class Leonardo {
        static public int Fib(int n) {
            if (n <= 1) {
                return n;
            }
            return Fib(n - 1) + Fib(n - 2);
        }
    }
    void main() {
        cout << Leonardo.Fib(10);
    }
    ---
    55
    """,
    """
    //Test static member variables
    class Cheese {
        static public int y = 4;
        static public int x = Cheese.y + 1;
        static public int z = x + y;
    }
    void main() {
        cout << Cheese.z;
    }
    ---
    9
    """,
    """
    //Test member qualification
    class Cheese {
        static public int x = 90;
        static public int cheesey() {
            int x = 4;
            return x;
        }
    }
    void main() {
        cout << Cheese.cheesey();
    }
    ---
    4
    """,
        ## Wyatt Additions
    """
    // Returning Classes and Accessing Members
    class Yeet {
        static public Yoink getHim(){
            return Yoink;
        }
    }
    class Yoink{
        static public char me= 'z';
    }
    
    void main() {
        cout<< Yeet.getHim().me;
    }
    ---
    z
    """,
    """
    // Dangling Else WHO
    void main() {
        if(true)
        if(false){}
            else{
            cout << "hey";
            }
    }
    ---
    hey
    """,
        """
    // Else Statement With Block
    void main() {
        bool test = true;
        int y = 1;

        if(!test){
        cout<<"Fail";
        }
        else{
            y =5;
        }
        cout<< y;
    }
    ---
    5
    """,
    """
    //We are Loving Scopes
    void main() {
        int y = 1;
        if( y < 5){
            bool y = false;
            {
                int y = 5;
                {
                    char y = 'a';
                    {
                        string y = "Ayo";
                        cout<< y;
                    }
                    cout<< y;
                }
                cout<< y;
            }
             if(y)
                cout<<"Yoink";  
            else
                cout<<"Yeet";
        }
         cout<< y;
    }
    ---
    Ayoa5Yeet1
    """,
    """
    // Nested Reference to Class Function outside of Class Scope
       class B{

        static public int gimmeInt(){
            return 15;
        }
        static public void eatingInt(int x){
            cout<< x;
        }
    }
    
    void main() {
        B.eatingInt(B.gimmeInt());
    }
    ---
    15
    """,
        """
        // For Loop nested in While Loop
    void main() {
        int x = 10;
        while(x > 0){
            cout<<"Ready";
            for(;x > 0;x -=1){
                cout<<x;
            }
            cout<< "Stop";
        }
        }
    ---
    Ready10987654321Stop
    """,
        """
        // Make sure that you can call main within main, Aldous said in teams
    class B{
        static public int counter= 5;
    }

    void main(){
        if(B.counter > 0){
            B.counter -=1;
            cout<< B.counter;
                main();
        }
        cout<<"End";
    }
    ---
43210End
    """,
    """"
    // Make sure you can shadow main
    void main(){
        int main = 5;
        cout<<main;
    }
    ---
5
    """
]
# MANUAL TESTS
# cin to some integer x
"""
void main() {
    int x;
    cin >> x;
    cout << x; //Ensure the value that prints is the same as your input
}
"""

# cin to some character x
"""
void main() {
    char x;
    cin >> x;
    cout << x; //Ensure the value that prints is the same as your input
}
"""


def main() -> None:
    counter = 0
    for test in tests:
        counter += 1
        counter_str = str(counter)
        # Pad to 3 digits (0's in the beginning)
        counter_str = counter_str.zfill(3)
        with open(f"./tests/test_{counter_str}.kxi", "w") as file:
            file.write(test)
    print("total tests = ", counter)


if __name__ == "__main__":
    main()
