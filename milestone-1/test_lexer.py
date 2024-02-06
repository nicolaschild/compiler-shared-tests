# type: ignore
from lex.lexer import lexer_main as lex

"""
Unit Tests to test the individual tokens
"""

def test_token_INTLIT() -> None:
    input = """
123
00321
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "INTLIT"
    assert tokens[1].type == "INTLIT"

def test_token_CHARLIT() -> None:
    # Arrange
    input = """
'a'
'\\n'
'\\r'
'\\t'
'\\''
'0'
    """
    # Act
    tokens = lex(input, True, None)
    # Assert
    for token in tokens:
        assert token.type == "CHARLIT"

# 1/29/24 adding tests for new CHARLIT specification
def test_token_CHARLIT_DOUBLE_QUOTE() -> None:
    # Arrange
    input = """
'"'
"""
    # Act
    tokens = lex(input, True, None)
    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == "CHARLIT"
    assert tokens[0].value == '"'

def test_token_STRINGLIT() -> None:
    # Arrange
    input = """
"Hello World 1234"
"\\n"
"\\r"
"\\t"
"\\""
    """
    # Act
    tokens = lex(input, True, None)
    # Assert
    assert len(tokens) == 5
    for token in tokens:
        assert token.type == "STRINGLIT"

# 1/29/24 adding tests for new STRINGLIT specification
def test_token_STRINGLIT_SINGLE_QUOTE() -> None:
    # Arrange
    input = """
"Hello '''''''' SIRE!"
"""
    # Act
    tokens = lex(input, True, None)
    # Assert
    assert len(tokens) == 1
    assert tokens[0].type == "STRINGLIT"
    assert tokens[0].value == "Hello '''''''' SIRE!"


def test_token_COLON() -> None:
    input = """
:
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "COLON"

def test_token_SEMICOLON() -> None:
    input = """
;
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "SEMICOLON"

def test_token_LCURLY() -> None:
    input = """
{
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "LCURLY"

def test_token_RCURLY() -> None:
    input = """
}
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "RCURLY"

def test_token_LSQUARE() -> None:
    input = """
[
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "LSQUARE"

def test_token_RSQUARE() -> None:
    input = """
]
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "RSQUARE"

def test_token_LPAREN() -> None:
    input = """
(
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "LPAREN"

def test_token_RPAREN() -> None:
    input = """
)
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "RPAREN"

def test_token_EQ() -> None:
    input = """
=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "EQ"

def test_token_EQEQ() -> None:
    input = """
==
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "EQEQ"

def test_token_NOTEQ() -> None:
    input = """
!=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "NOTEQ"
    
def test_token_GEQ() -> None:
    input = """
>=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "GEQ"

def test_token_LEQ() -> None:
    input = """
<=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "LEQ"

def test_token_GT() -> None:
    input = """
>
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "GT"

def test_token_LT() -> None:
    input = """
<
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "LT"
    
def test_token_AND() -> None:
    input = """
&&
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "AND"

def test_token_OR() -> None:
    input = """
||
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "OR"

def test_token_NOT() -> None:
    input = """
!
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "NOT"

def test_token_PLUS() -> None:
    input = """
+
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "PLUS"

def test_token_MINUS() -> None:
    input = """
-
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "MINUS"

def test_token_TIMES() -> None:
    input = """
*
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "TIMES"

def test_token_DIVIDE() -> None:
    input = """
/
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "DIVIDE"

def test_token_PLUSEQ() -> None:
    input = """
+=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "PLUSEQ"

def test_token_MINUSEQ() -> None:
    input = """
-=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "MINUSEQ"

def test_token_TIMESEQ() -> None:
    input = """
*=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "TIMESEQ"

def test_token_DIVIDEEQ() -> None:
    input = """
/=
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "DIVIDEEQ"

def test_token_INSERT() -> None:
    input = """
<<
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "INSERT"

def test_token_EXTRACT() -> None:
    input = """
>>
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "EXTRACT"

def test_token_DOT() -> None:
    input = """
.
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "DOT"

def test_token_COMMA() -> None:
    input = """
,
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "COMMA"

def test_token_COMMENT() -> None:
    input = """
//This is a comment
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "COMMENT"

def test_token_COMMENT_EOF() -> None:
    input = """
//This is a comment"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "COMMENT"

def test_token_WHITESPACE() -> None:
    #Should just ignore whitespace
    input = """  
  






    """
    tokens = lex(input, True, None)
    assert len(tokens) == 0

def test_token_ID() -> None:
    input = """
char a;
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "CHAR"
    assert tokens[1].type == "ID"

def test_token_ID_VALID_START_WITH_UNDERSCORE() -> None:
    input = """
char _a;
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "CHAR"
    assert tokens[1].type == "ID"

def test_token_ID_INVALID_START_WITH_NUMBER() -> None:
    input = """
char 1a;
    """
    tokens = lex(input, True, None)
    assert tokens[0].type == "CHAR"
    assert tokens != "ID"
    #TODO: CHECK THIS BEHAVIOR

def test_token_UNKNOWN() -> None:
    input = """
?@#$%^&|"'`~
"""
    tokens = lex(input, True, None)
    for token in tokens:
        assert token.type == "UNKNOWN"

#Reserved keywords
def test_token_BOOL() -> None:
    input = """
bool a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "BOOL"
    assert tokens[1].type == "ID"

def test_reserved_BREAK() -> None:
    input = """
break;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "BREAK"

def test_reserved_CASE() -> None:
    input = """
case 1:
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "CASE"
    assert tokens[1].type == "INTLIT"
    assert tokens[2].type == "COLON"


def test_reserved_CLASS() -> None:
    input = """
class A {
}
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "CLASS"
    assert tokens[1].type == "ID"
    assert tokens[2].type == "LCURLY"
    assert tokens[3].type == "RCURLY"

def test_reserved_CHAR() -> None:
    input = """
char a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "CHAR"
    assert tokens[1].type == "ID"
    assert tokens[2].type == "SEMICOLON"

def test_reserved_CIN() -> None:
    input = """
cin >> a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "CIN"
    assert tokens[1].type == "EXTRACT"
    assert tokens[2].type == "ID"
    assert tokens[3].type == "SEMICOLON"

def test_reserved_COUT() -> None:
    input = """
cout << a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "COUT"
    assert tokens[1].type == "INSERT"
    assert tokens[2].type == "ID"
    assert tokens[3].type == "SEMICOLON"

def test_reserved_DEFAULT() -> None:
    input = """
default:
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "DEFAULT"
    assert tokens[1].type == "COLON"

def test_reserved_ELSE() -> None:
    input = """
else {
}
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "ELSE"
    assert tokens[1].type == "LCURLY"
    assert tokens[2].type == "RCURLY"

def test_reserved_FALSE() -> None:
    input = """
false;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "FALSE"
    assert tokens[1].type == "SEMICOLON"

def test_reserved_FOR() -> None:
    input = """
for () {
}
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "FOR"
    assert tokens[1].type == "LPAREN"
    assert tokens[2].type == "RPAREN"
    assert tokens[3].type == "LCURLY"
    assert tokens[4].type == "RCURLY"

def test_reserved_IF() -> None:
    input = """
if () {
}
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "IF"
    assert tokens[1].type == "LPAREN"
    assert tokens[2].type == "RPAREN"
    assert tokens[3].type == "LCURLY"
    assert tokens[4].type == "RCURLY"

def test_reserved_INT() -> None:
    input = """
int a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "INT"
    assert tokens[1].type == "ID"
    assert tokens[2].type == "SEMICOLON"
    

def test_reserved_NEW() -> None:
    input = """
new int[10];
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "NEW"
    assert tokens[1].type == "INT"
    assert tokens[2].type == "LSQUARE"
    assert tokens[3].type == "INTLIT"
    assert tokens[4].type == "RSQUARE"
    assert tokens[5].type == "SEMICOLON"

def test_reserved_NULL() -> None:
    input = """
null;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "NULL"
    assert tokens[1].type == "SEMICOLON"

def test_reserved_PUBLIC() -> None:
    input = """
public:
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "PUBLIC"
    assert tokens[1].type == "COLON"

def test_reserved_RETURN() -> None:
    input = """
return;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "RETURN"
    assert tokens[1].type == "SEMICOLON"

def test_reserved_STATIC() -> None:
    input = """
static int a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "STATIC"
    assert tokens[1].type == "INT"
    assert tokens[2].type == "ID"
    assert tokens[3].type == "SEMICOLON"

def test_reserved_STRING() -> None:
    input = """
string a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "STRING"
    assert tokens[1].type == "ID"
    assert tokens[2].type == "SEMICOLON"

def test_reserved_SWITCH() -> None:
    input = """
switch () {
}
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "SWITCH"
    assert tokens[1].type == "LPAREN"
    assert tokens[2].type == "RPAREN"
    assert tokens[3].type == "LCURLY"
    assert tokens[4].type == "RCURLY"

def test_reserved_THIS() -> None:
    input = """
this;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "THIS"
    assert tokens[1].type == "SEMICOLON"

def test_reserved_TRUE() -> None:
    input = """
true;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "TRUE"
    assert tokens[1].type == "SEMICOLON"

def test_reserved_VOID() -> None:
    input = """
void a;
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "VOID"
    assert tokens[1].type == "ID"
    assert tokens[2].type == "SEMICOLON"

def test_reserved_WHILE() -> None:
    input = """
while () {
}
"""
    tokens = lex(input, True, None)
    assert tokens[0].type == "WHILE"
    assert tokens[1].type == "LPAREN"
    assert tokens[2].type == "RPAREN"
    assert tokens[3].type == "LCURLY"
    assert tokens[4].type == "RCURLY"


def test_line_numbers() -> None:
    input = """while (true) {
    //INFINITE LOOOOOOP
}
for (int i = 0; i < 10; i++) {
    cout << i << endl;
}
char a;
char b;
string c = "This should be on line 9";

//I am a comment, KXI is my passion
return 0;
"""
    tokens = lex(input, True, None)
    assert tokens[0].lineno == 1
    assert tokens[1].lineno == 1
    assert tokens[2].lineno == 1
    assert tokens[3].lineno == 1
    assert tokens[4].lineno == 1
    assert tokens[5].lineno == 2
    assert tokens[6].lineno == 3
    #Find the for token and assert line number is 4
    for token in tokens:
        if token.type == "FOR":
            assert token.lineno == 4
            break
        if token.value == "This should be on line 9":
            assert token.lineno == 9
            assert token.type == "STRINGLIT"
            break
        if token.type == "RETURN":
            assert token.lineno == 12
            break

#Check type cast for INTLIT, CHARLIT, STRINGLIT
def test_token_type_cast_INTLIT() -> None:
    input = """
int a = 123;
"""
    tokens = lex(input, True, None)
    assert tokens[3].type == "INTLIT"
    assert isinstance(tokens[3].value, int)

def test_token_type_cast_CHARLIT() -> None:
    input = """
char a = 'a';
"""
    tokens = lex(input, True, None)
    assert tokens[3].type == "CHARLIT"
    assert isinstance(tokens[3].value, str)
    assert len(tokens[3].value) == 1

def test_token_type_cast_STRINGLIT() -> None:
    input = """
string a = "Hello World";
"""
    tokens = lex(input, True, None)
    assert tokens[3].type == "STRINGLIT"
    assert isinstance(tokens[3].value, str)
    assert len(tokens[3].value) == 11
