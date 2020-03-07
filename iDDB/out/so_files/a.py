from ctypes import *

so_file = './database_manipulation.so'
cfactorial = CDLL(so_file)


c_return = cfactorial.mesaj();
print (str(c_return))


