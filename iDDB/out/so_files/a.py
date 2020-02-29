from ctypes import *

so_file = './test.so'
cfactorial = CDLL(so_file)


c_return = cfactorial.mesaj();
print (str(c_return))


