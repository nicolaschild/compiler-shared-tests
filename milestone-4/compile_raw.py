tests = [
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
    "This should print"
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
]


def main() -> None:
    counter = 0
    for test in tests:
        counter += 1
        counter_str = str(counter)
        # Pad to 3 digits (0's in the beginning)
        counter_str = counter_str.zfill(3)
        with open(f"./tests/test_{counter_str}.kxi", "w") as file:
            file.write(test)


if __name__ == "__main__":
    main()
