#!/usr/bin/env python


def unicode():
    print('\033[1;33m ord():\033[0m函数获取字符的整数表示')
    print('\033[1;33m chr():\033[0m函数把编码转换为对应的字符')
    #由于Python的字符串类型是str,在内存中以unicode表示，一个字符对应若干个字节.如果要在网络中传输,或者保存到磁盘上,就需要把str变为以字节为单位的bytes.
    



if __name__=='__main__':
   unicode()
