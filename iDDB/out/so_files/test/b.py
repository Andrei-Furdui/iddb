import ctypes
hello = ctypes.cdll.LoadLibrary('./test.so')
name = "Frank"
c_name = ctypes.c_char_p(name)
hello.hello.restype = ctypes.c_char_p # override the default return type (int)
foo = hello.hello(c_name)
print ctypes.c_char_p(foo).value
