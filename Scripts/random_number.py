#需要pip安装itertools-recipes

#coding:utf-8

from itertools import permutations

for i in permutations(range(1,5),3):
    k = ''
    for j in i:
        k = k +str(j)
    print(int(k))
