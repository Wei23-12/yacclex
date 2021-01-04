將yacc.py在Spyder上執行進行以下測試

冪次運算:
calc > 2^3 
8
根號運算:
calc > 4**2 
2.0

for-loop:
calc > i=0
LexToken(NAME,'i',1,0)
LexToken(EQUALS,'=',1,1)
LexToken(NUMBER,0,1,2)

calc > for i<10 i=i+1
LexToken(FOR,'for',1,0)
LexToken(NAME,'i',1,4)
LexToken(SMALL,'<',1,5)
LexToken(NUMBER,10,1,6)
LexToken(NAME,'i',1,9)
LexToken(EQUALS,'=',1,10)
LexToken(NAME,'i',1,11)
LexToken(PLUS,'+',1,12)
LexToken(NUMBER,1,1,13)

calc > i
LexToken(NAME,'i',1,0)
11
[['op', 'arg1', 'arg2', 'result'], ['=', 'i', ' ', 'a']]
 
if-else: 
calc > i=1
LexToken(NAME,'i',1,0)
LexToken(EQUALS,'=',1,1)
LexToken(NUMBER,1,1,2)

calc > if i<10 k=5
LexToken(IF,'if',1,0)
LexToken(NAME,'i',1,3)
LexToken(SMALL,'<',1,4)
LexToken(NUMBER,10,1,5)
LexToken(NAME,'k',1,8)
LexToken(EQUALS,'=',1,9)
LexToken(NUMBER,5,1,10)

calc > k
LexToken(NAME,'k',1,0)
5
[['op', 'arg1', 'arg2', 'result'], ['=', 'k', ' ', 'a']]

calc > i=0
LexToken(NAME,'i',1,0)
LexToken(EQUALS,'=',1,1)
LexToken(NUMBER,0,1,2)

calc > if i>5 k=0 else k=10
LexToken(IF,'if',1,0)
LexToken(NAME,'i',1,3)
LexToken(LARGE,'>',1,4)
LexToken(NUMBER,5,1,5)
LexToken(NAME,'k',1,7)
LexToken(EQUALS,'=',1,8)
LexToken(NUMBER,0,1,9)
LexToken(ELSE,'else',1,11)
LexToken(NAME,'k',1,16)
LexToken(EQUALS,'=',1,17)
LexToken(NUMBER,10,1,18)

calc > k
LexToken(NAME,'k',1,0)
Undefined name 'k'
0
[['op', 'arg1', 'arg2', 'result'], ['=', 'k', ' ', 'a']] 

 
