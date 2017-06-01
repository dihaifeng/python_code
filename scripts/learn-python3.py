#-*- coding:utf-8 -*-

def mov(n,a,b,c):
    if n == 1:
        print(a,'->',c)
    else:
        mov(n-1,a,c,b)
        mov(1,a,b,c)
        mov(n-1,b,a,c)
num = input("num:")
mov(int(num),'A','B','C')
