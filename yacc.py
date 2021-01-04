import ply.lex as lex
import ply.yacc as yacc
import matplotlib.pyplot as plt




reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    
}


tokens = [
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'EQUALS', 'POWER', 'SQUARE',
    'LPAREN', 'RPAREN',
    'EQUAL', 'NOTEQ', 'LARGE', 'SMALL', 'LRGEQ', 'SMLEQ',
] + list(reserved.values())


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MODULO  = r'%'
t_POWER   = r'\^'
t_SQUARE  = r'\*\*'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL   = r'\=\='
t_NOTEQ   = r'\!\='
t_LARGE   = r'\>'
t_SMALL   = r'\<'
t_LRGEQ   = r'\>\='
t_SMLEQ   = r'\<\='



def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    
    return t


# complex tokens
# number token
def t_NUMBER(t):
    r'\d+'  
    t.value = int(t.value)  
    return t



t_ignore = " \t"  


# newline character
def t_newline(t):
    r'\n+'  
    t.lexer.lineno += t.value.count("\n")  



def t_error(t):
    print("Illegal character '%s'" % t.value[0])  
    t.lexer.skip(1) 



lex.lex()




precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS','POWER','SQUARE'),
)


names = {}


def p_statement_if(p):
    '''statement    : IF comparison NAME EQUALS expression
                    | IF comparison NAME EQUALS expression ELSE NAME EQUALS expression '''

    if p[2]:
        names[p[3]] = p[5]
    elif not p[3]:
        if p[6] is not None:
            names[p[7]]=p[9]


def p_statement_for(p):
    '''statement : FOR NAME SMALL NUMBER NAME EQUALS expression PLUS  expression
                 | FOR NAME SMALL NUMBER NAME EQUALS expression MINUS expression '''
                

    t1 = p[7]
    t2 = p[9]
    sum=0

    for i in range(0,p[4]+1):
       if p[8]=='+':
          sum = t1 + t2
          t1 = sum 
       elif p[8]=='-':
          sum = t1 - t2
          t1 = sum

    names[p[5]] = t1



def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]  



def p_statement_expr(p):
    'statement : expression'
    print(p[1])


# comparison
def p_comparison_binop(p):
    '''comparison : expression EQUAL expression
                          | expression NOTEQ expression
                          | expression LARGE expression
                          | expression SMALL expression
                          | expression LRGEQ expression
                          | expression SMLEQ expression'''
    if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]



def p_expression_binop(p):
    '''expression : expression PLUS expression
                          | expression MINUS expression
                          | expression TIMES expression
                          | expression DIVIDE expression
                          | expression MODULO expression
                          | expression POWER  expression
                          | expression SQUARE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]
    elif p[2] == '**':
        p[0] = p[1] ** (1/p[3])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]



def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]



def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]



def p_expression_name(p):
    'expression : NAME'
   
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0



def p_error(p):
    print("Syntax error at '%s'" % p.value)


# TAC 
def find_top_prio(lst):
    top_prio = 1
    count_ops = 0
    for ops in lst:
        if ops in prio_dict:
            count_ops += 1
            if prio_dict[ops] > 1:
                top_prio = prio_dict[ops]

    return top_prio, count_ops



yacc.yacc()

lexer = lex.lex()



while True:
    try:
        s = input('calc > ')  

        lexer.input(s)
        while True:
           tok = lexer.token()
           if not tok:
              break
           print(tok)

        ip_str = s
        ip_lst = list(map(str,ip_str))

    except EOFError:
        break

    yacc.parse(s)  
    
    
    prio_dict = {'-':1,'+':2,'*':3,'/':4,'**':5,'^':6}
    op_lst = []
    op_lst.append(['op','arg1','arg2','result'])

    top_prio, count_ops = find_top_prio(ip_lst)
    ip = ip_lst
    i, res = 0, 0

    while i in range(len(ip)):
      if ip[i] in prio_dict:
        op = ip[i]
        if (prio_dict[op]>=top_prio) and (ip[i+1] in prio_dict):
            res += 1
            op_lst.append([ip[i+1],ip[i+2],' ','t'+str(res)])
            ip[i+1] = 't'+str(res)
            ip.pop(i+2)
            i = 0
            top_prio, count_ops = find_top_prio(ip)
        elif prio_dict[op]>=top_prio:
            res += 1
            op_lst.append([op,ip[i-1],ip[i+1],'t'+str(res)])
            ip[i] = 't'+str(res)
            ip.pop(i-1)
            ip.pop(i)
            i = 0
            top_prio, count_ops = find_top_prio(ip)
      if len(ip) == 1:
        op_lst.append(['=',ip[i],' ','a'])
        print(op_lst)
        
   

      i += 1

