tests = [
"""
    void main   {
    cout << "Hello World!";
}
""",
"""
    void main  {
    int n = 1;
    switch n {
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
"""
""",
void main   {
    int x = 0;
    if  1 < x  {
            cout << "This should not print";
    }   
}
""",
"""
void main   {
    int x = 0;
    if  x < 1  {
            cout << "This should print";
    }
    else {
            cout << "This should not print";
    }
}
""",
"""
void main   {
    int x = 0;
    if  x > 1  {
            cout << "This should not print";
    }
    else {
            cout << "This should print";
    }   
}
""",
"""
void main   {
    int x = 0;
    if  1 > x  {
            cout << "This should print";
    }
    else {
            cout << "This should not print";
    }
}
""",
"""
void main   {
    int x = 0;
    if  x == 0  {
        cout << "This should print";
    }
    else {
        cout << "This should not print";
    }
}
""",
"""
void main   {
    int x = 1;
    if  0 == x  {
        cout << "This should not print";
    }
    else {
        cout << "This should print";
    }
}
""",
"""
void main   {
    int x = 0;
    if  x != 1  {
        cout << "This should print";
    }
    else {
        cout << "This should not print";
    }
}
""",
"""
void main   {
    int x = 1;
    if  1 != x  {
        cout << "This should not print";
    }
    else {
        cout << "This should print";
    }
""",
"""
void main   {
    int x = 0;
    if  x == 0  {
        if  x == 0  {
            cout << "This should print";
        }
    }
}
""",
"""
void main   {
    int x = 0;
    if  x == 0  {
        if  x == 0  {
            if  x == 0  {
                cout << "This should print";
            }
        }
    }
}
""",
"""
void main   {
    int x = 0;
    if  x != 0  {
        cout << "This should not print";
    }
    else {
        if  x == 0  {
            cout << "This should print";
        }
    }
}
""",
"""
void main   {
    int x = 0;
    if  x != 0  {
        cout << "This should not print";
    }
    else {
        if  x != 0  {
            cout << "This should not print";
        }
        else {
            cout << "This should print";
        }
    }
}
""",
"""
void main   {
    int i = 0;
    for  i = 0; i < 5; i = i + 1  {
        cout << i;
    }
}
""",
"""
void main   {
    int i = 0;
    for  ; i < 5; i = i + 1  {
        cout << i;
    }
}
""",
"""
void main   {
    int i = 0;
    for  ; i < 5;  {
        cout << i;
        i = i + 1;
    }
}
""",
"""
void main   {
    int i = 0;
    for  ; i < 5;  {
        cout << i;
        i = i + 1;
        if  i == 3  {
            break;
        }
    }
}
""",
"""
void main   {
    int i = 0;
    for  ; i < 3; i = i + 1  {
        int j = 0;
        for  ; j < 3; j = j + 1  {
            cout << i;
            cout << j;
        }
    }
}
""",
"""
void main   {
    int i = 0;
    for  ; i < 3; i = i + 1  {
        int j = 0;
        for  ; j < 3; j = j + 1  {
            cout << i;
            cout << j;
            if  j == 1  {
                break;
            }
        }
    }
}
""",
"""
void main   {
    int i = 0;
    while  i < 5  {
        cout << i;
        i = i + 1;
    }
}
""",
"""
void main   {
    int i = 0;
    while  i < 3  {
        int j = 0;
        while  j < 3  {
            cout << i;
            cout << j;
            j = j + 1;
        }
        i = i + 1;
    }
}
""",
"""
void main   {
    int i = 0;
    while  i < 3  {
        int j = 0;
        while  j < 3  {
            cout << i;
            cout << j;
            j = j + 1;
            if  j == 1  {
                break;
            }
        }
        i = i + 1;
    }
}
""",
"""
    void main   {
    int x = 1;
    int y = 2;
    int z = x + y;
    cout << z;
    }
""", 
"""
void main   {
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
""",
"""
void main   {
    int x += 1 - 3 * 2 / 2 + 1;
    cout << x + 12; 
}
""",
"""
void main   {
    int x = 1;
    int y = 2;
    int z = 3;
    cout << x + y * z;
}
""",
"""
void main   {
    int x = 1;
    x -= 1;
    cout << x;
}
""",
"""
void main   {
    int x = 1;
    x += 1;
    cout << x;
}
""",
"""
void main   {
    int x = 2;
    x /= 2;
    cout << x;
}
""",
"""
void main   {
    int x = 2;
    x *= 2;
    cout << x;
}
""",
"""
void main   {
    if  !false  {
        cout << "This should print";
    }
}
""",
"""
void main   {
    if  !!true  {
        cout << "This should print";
    }
}
""",
"""
void main   {
    if  true && true  {
        cout << "This should print";
    }
}
""",
"""
void main   {
    if  false && true  {
        cout << "This should not print";
    }
}
""",
"""
void main   {
    if  true || false  {
        cout << "This should print";
    }
}
""",
"""
void main   {
    if  false || false  {
        cout << "This should not print";
    }
}
""",
"""
void main   {
    if  true && true || false  {
        cout << "This should print";
    }
}
""",
"""
void main   {
    if  true && false || false  {
        cout << "This should not print";
    }
}
"""]