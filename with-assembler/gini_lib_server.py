# server.py
from ctypes import c_double, c_int
from msl.loadlib import Server32

class MyServer(Server32):
    """Wrapper around a 32-bit C library 'libgini32.so' that has an 'float_to_int_gini' function."""

    def __init__(self, host, port, **kwargs):
        # Load the 'libgini32' shared-library file using ctypes.CDLL
        super(MyServer, self).__init__('libgini.so', 'cdll', host, port)

        # The Server32 class has a 'lib' property that is a reference to the ctypes.CDLL object

        # Definir los tipos de la función de C
        self.lib.float_to_int_gini.argtypes = [c_double]  # argumento: double
        self.lib.float_to_int_gini.restype = c_int        # retorna: int

    def add(self, gini_float):
        # The shared library's 'float_to_int_gini' function takes one double as input and returns an int
        return self.lib.float_to_int_gini(gini_float)
