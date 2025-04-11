# client.py

from msl.loadlib import Client64

class MyClient(Client64):
    """Call a function in 'libgini32.so' via the 'MyServer' wrapper."""

    def __init__(self):
        # Specify the name of the Python module to execute on the 32-bit server (i.e., 'my_server')
        super(MyClient, self).__init__(module32='gini_lib_server')

    def float_to_int_gini(self, gini_float):
        # The Client64 class has a 'request32' method to send a request to the 32-bit server
        # Send the 'gini_float' arguments to the 'float_to_int_gini' method in MyServer
        return self.request32('add', gini_float)

