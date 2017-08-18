#coding:utf-8
#将一个正整数分解质因数

dig_input = int(input('请输入一个数字：'))

l = []

while dig_input != 1:
    for i in range(2,dig_input+1):
        print i
        if dig_input % i == 0:
            l.append(i)
            dig_input = dig_input / i
            break
print l
