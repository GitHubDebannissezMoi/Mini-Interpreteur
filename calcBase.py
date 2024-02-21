# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmÃ©tiques sans variables
# -----------------------------------------------------------------------------
import ply.lex
from genereTreeGraphviz2 import printTreeGraph

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'print' : 'PRINT',
   'while' : 'WHILE',
   'for' : 'FOR',
   'void' : 'VOID',
   'function' : 'FUNCTION',
   'return' : 'RETURN',
   'main' : 'MAIN'
   }

tokens = [
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE',
    'LPAREN','RPAREN','LBRACE','RBRACE',
    'AND','OR','SEMI',
    'NAME','EQUAL','EQUALS','SUP',
    'INF','PLUSPLUS','COMMA'
] + list(reserved.values())

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_AND = r'\&'
t_OR = r'\|'
t_SEMI = r';'
t_EQUAL = r'='
t_EQUALS  = r'=='
t_SUP = r'>'
t_INF = r'<'
t_PLUSPLUS = r'\+\+'
t_COMMA = r'\,'

precedence = (
    ('left','AND','OR'),
    ('nonassoc', 'SUP','INF'),
    ('left','PLUS', 'MINUS' ),
    ('left','TIMES','DIVIDE'),
    ('left','PLUSPLUS')
)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_NAME(t):
    r'[a-z]+'
    t.type = reserved.get(t.value,'NAME')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

names = {}
functionNames = {}
stack = []
scope = {}

# Build the lexer
import ply.lex as lex
lex.lex()

def p_start(t):
    ''' start : bloc function_main'''
    t[0] = ('start',t[1],t[2])
    printTreeGraph(t[0])
    #evalInst(t[1])
    stack.append(t[2][0])
    stack.append(t[2][1])
    manage_stack()

def evalInst(t):
    if type(t)!=tuple : 
        return
    if t[0]=='print' :
        evalInst(t[1])
    if t[0]=='assign' : 
        names[t[1]]=eval(t[2])
    if t[0]=='assignPlus' :
        names[t[1]]+=1
    if t[0]=='bloc' : 
        evalInst(t[1])
        evalInst(t[2])
    if t[0]=='if' :
        if len(t) == 3 : 
            if eval(t[1]) == True :
                evalInst(t[2])
        else :
            if eval(t[1]) == True :
                evalInst(t[2])
            else :
                evalInst(t[3])
    if t[0]=='else' :
        evalInst(t[1])
    if t[0]=='while' :
        while(eval(t[1])) :
            evalInst(t[2])
    if t[0]=='for' :
        evalInst(t[1])
        while(eval(t[2])) :
            evalInst(t[4])
            evalInst(t[3])
    if t[0]=='call' :
        evalInst(functionNames[t[2]][1])
    if t[0]=='return':
        return eval(t[1])  
    if t[0]=='expr':
        while (len(t) > 2) :
            print('CALC>', eval(t[1]))
            t = t[2]
        print('CALC>', eval(t[1]))
           

def manage_stack():
    while len(stack) > 0:
        item = stack.pop()
        if item == "main":
            return

        if type(item) != tuple:
            itemTmp = stack.pop()
            if itemTmp == "print":
                print("CALC>",eval(item))
            elif itemTmp[0] == "assign":
                names[itemTmp[1]] = item
            elif itemTmp[0] == "assignPlus":
                names[itemTmp[1]]+= item
            else :
                item = itemTmp
        add_instructions(item)
        
def add_instructions(t):
    if type(t) is tuple : 
        if t[0] == "call":
            if t[1] == "function":
                stack.append(functionNames[t[2]][3])
            stack.append(functionNames[t[2]][1])
            paramDecla = functionNames[t[2]][2]
            paramCall = t[3]
            while(len(paramDecla) > 2) :
                names[paramDecla[1]] = eval(paramCall[1])
                paramDecla = paramDecla[2]
                paramCall = paramCall[2]
            names[paramDecla[1]] = eval(paramCall[1])
        elif t[0] == "bloc":
            if t[2] != "empty":
                stack.append(t[2])
            stack.append(t[1])
        elif t[0] == "print":
            stack.append(t[0])
            stack.append(t[1])
        elif t[0] == "assign":
            stack.append(tuple([t[0],t[1]]))
            stack.append(t[2])
        elif t[0] == "assignPlus":
            stack.append(tuple([t[0],t[1]]))
            stack.append(1)
        elif t[0] == "expr":
            stack.append(t[1])
        elif t[0] == "return":
            stack.append(eval(t[1]))
        elif t[0] == "if":
            if eval(t[1]) == True:
                stack.append(t[2])
            else :
                if len(t) > 3:
                    stack.append(t[3])
        elif t[0] == "else":
            stack.append(t[1])
        elif t[0] == "while":
            if eval(t[1]) == True:
                stack.append(t)
                stack.append(t[2])
        elif t[0] == "for":
            stack.append(tuple(["boucle",t[2],t[3],t[4]]))
            stack.append(t[1])
        elif t[0] == "boucle":
            if eval(t[1]) == True:
                stack.append(tuple(["boucle",t[1],t[2],t[3]]))
                stack.append(t[2])
                stack.append(t[3])
            
def p_line(t):
    '''bloc : bloc statement
            | statement'''
    if len(t)== 3 :
        t[0] = ('bloc',t[1], t[2])
    else:
        t[0] = ('bloc',t[1], 'empty')
    
def p_if(t):
    '''statement : IF LPAREN expression RPAREN LBRACE bloc RBRACE SEMI
    | IF LPAREN expression RPAREN LBRACE bloc RBRACE condition'''
    if t[8] == ';' : t[0] = ('if',t[3],t[6])
    else : t[0] = ('if',t[3],t[6],t[8])
    
def p_else(t):
    'condition : ELSE LBRACE bloc RBRACE SEMI'
    t[0] = ('else',t[3])
    
def p_while(t):
    'statement : WHILE LPAREN expression RPAREN LBRACE bloc RBRACE SEMI'
    t[0] = ('while',t[3],t[6])
    
def p_for(t):
    '''statement : FOR LPAREN statement expression SEMI expression RPAREN LBRACE bloc RBRACE SEMI
    | FOR LPAREN statement expression SEMI statement RPAREN LBRACE bloc RBRACE SEMI'''
    t[0] = ('for',t[3],t[4],t[6],t[9])
    
def p_statement_void_declaration(t):
    '''statement : VOID NAME LPAREN RPAREN LBRACE bloc RBRACE SEMI
    | VOID NAME LPAREN parameters_function RPAREN LBRACE bloc RBRACE SEMI'''
    if len(t) == 9 : 
        t[0] = ('voidDeclaration',t[1],t[2])
        functionNames[t[2]] = ('void',t[6])
    else : 
        t[0] = ('voidDeclaration',t[1],t[2],t[4])
        functionNames[t[2]] = ('void',t[7],t[4])
    
def p_statement_functions_call(t):
    '''statement : NAME LPAREN RPAREN SEMI
    | NAME LPAREN parameters RPAREN SEMI'''
    if len(t) == 5 : 
        t[0] = ('call',functionNames[t[1]][0],t[1])
    else : 
        t[0] = ('call',functionNames[t[1]][0],t[1],t[3])
    
def p_statement_function_declaration(t):
    '''statement : FUNCTION NAME LPAREN RPAREN LBRACE bloc return_statement RBRACE SEMI
    | FUNCTION NAME LPAREN parameters_function RPAREN LBRACE bloc return_statement RBRACE SEMI'''
    if len(t) == 10 : 
        t[0] = ('functionDeclaration',t[1],t[2],t[7],t[8])
        functionNames[t[2]] = ('function',t[6],t[7])
    else : 
        t[0] = ('functionDeclaration',t[1],t[2],t[4],t[8])
        functionNames[t[2]] = ('function',t[7],t[4],t[8])
    
def p_return_statement_function(t):
    'return_statement : RETURN expression SEMI'
    t[0] = ('return',t[2])
    
def p_parameters_function(t):
    '''parameters_function : NAME COMMA parameters_function
    | NAME'''
    if len(t) == 2 : t[0] = ('param',t[1])
    else : t[0] = ('param',t[1],t[3])
    
def p_parameters(t):
    '''parameters : expression COMMA parameters
    | expression'''
    if len(t) == 2 : t[0] = ('param',t[1])
    else : t[0] = ('param',t[1],t[3])
     
def p_function_main(t):
    'function_main : MAIN LPAREN RPAREN LBRACE bloc RBRACE '
    t[0] = ('main',t[5])
    
def p_statement_assign(t):
    'statement : NAME EQUAL expression SEMI'
    t[0] = ('assign',t[1], t[3])
    
def p_statement_assign_function(t):
    'statement : NAME EQUAL statement'
    t[0] = ('assign',t[1], t[3])

def p_statement_print(t):
    'statement : PRINT LPAREN expression_print RPAREN SEMI'
    t[0] = ('print',t[3])    
    
def p_expression_print(t):
    '''expression_print : expression COMMA expression_print
    | expression'''
    if len(t) == 4 : t[0] = ('expr',t[1],t[3])
    else : t[0] = ('expr',t[1])
    
def p_expression_print_statement(t):
    '''expression_print : statement COMMA expression_print
    | statement'''
    if len(t) == 4 : t[0] = ('expr',t[1],t[3])
    else : t[0] = ('expr',t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression OR expression
                  | expression AND expression
                  | expression INF expression
                  | expression SUP expression
                  | expression DIVIDE expression
                  | expression EQUALS expression'''
    t[0] = (t[2],t[1], t[3])
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]
    
def p_expression_compare_variable(p):
    '''expression : expression INF NAME INF expression
    | expression SUP NAME SUP expression'''
    if p[2] == '<' and p[4] == '<' : p[0] = p[1] < names[p[3]] and names[p[3]] < p[5]
    else : p[0] = p[1] > names[p[3]] and names[p[3]] > p[5]

def p_expression_increment(p):
    'statement : NAME PLUSPLUS SEMI'
    #names[p[1]] += 1
    p[0] = ('assignPlus',p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]
    
def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

def eval (t):
    if type(t) is int : return t
    if type(t) is bool : return t
    if type(t) is tuple : 
       
        if t[0] == '+':     return eval(t[1]) + eval(t[2]) 
        if t[0] == '*':     return eval(t[1]) * eval(t[2])  
        if t[0] == '-':     return eval(t[1]) - eval(t[2]) 
        if t[0] == '/':     return eval(t[1]) / eval(t[2])
        if t[0] == '>':     return eval(t[1]) > eval(t[2])
        if t[0] == '<':     return eval(t[1]) < eval(t[2])
        if t[0] == '&':     return eval(t[1]) and eval(t[2])
        if t[0] == '|':     return eval(t[1]) or eval(t[2])
        if t[0] == '==':    return eval(t[1]) == eval(t[2])
    if type(t) is str :
        return names[t]
    return 'UNK'

#s = "print(1+2);print(5+6);x=2;x++;print(x);if(1+2==3){print(1+2);}else{print(2+3);};"
#s = "void test(x,y){print(x);print(y);};test(1+1,5);"
#s = "function test(x,y){print(x);print(y);return x+y;};test(1,5);"
#s = "x=5;print(1+2,3+5,10+6,x);"
s = "function test(x,y){print(x);print(y);return x+y;};function testdeux(a){print(a);return a+2;}; main(){print(test(1,5););print(x);a=2;for(i=0;i<5;i++;){print(i);};}"
#s = "x=2;while(x<5){x++;print(x);};"
#s = "for(i=0;i<10;i=i+2;){print(i);print(i+1);};"
#s = input('calc > ')
yacc.parse(s)

    