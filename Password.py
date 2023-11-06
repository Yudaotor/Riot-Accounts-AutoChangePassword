import string
import random

# 密码段各段长度默认值
UL = 1  # 大写字母长度
LL = 7  # 小写字母长度
DL = 5  # 数字长度
SL = 1  # 符号长度

# 符号池
symbols = "@!#&"

class Password:
    '''
    随机密码: 
    格式：
        第一段：大写字母， 默认1位
        第二段：小写字母， 默认7位
        第三段：数字， 默认5位
        第四段：符号， 默认1位， 符号池：@、!、#、&
    示例：
        Abcdefgh12345@
    '''
    def __init__(self, ul=UL, ll=LL, dl=DL, sl=SL):
        p1 = "".join(random.choices(string.ascii_uppercase, k=ul))
        p2 = "".join(random.choices(string.ascii_lowercase, k=ll))
        p3 = "".join(random.choices(string.digits, k=dl))
        p4 = "".join(random.choices(symbols, k=sl))
        self.value = p1+p2+p3+p4
