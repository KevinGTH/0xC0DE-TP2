import sys
from server_interface import GiniAPIClient

NUM_ITERATIONS = 100000
TEST_VALUE = 12.32

# Función Python pura
def float_to_int_py(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def run_python():
    print(f"Ejecutando versión Python con {NUM_ITERATIONS:,} iteraciones.")
    for _ in range(NUM_ITERATIONS):
        float_to_int_py(TEST_VALUE)

def run_c():
    print(f"Ejecutando versión C (ctypes) con {NUM_ITERATIONS:,} iteraciones")
    client = GiniAPIClient("http://dummy.url")  #No es necesario poner una url real
    float_to_int_c_func = client.float_to_int_gini
    for _ in range(NUM_ITERATIONS):
        float_to_int_c_func(TEST_VALUE)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso incorrecto. Esperado:\n  python3 measure_perf.py [python|c]")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "python":
        run_python()
    elif mode == "c":
        run_c()
    else:
        print(f" Argumento no reconocido: {mode}")
        print("Uso correcto: python3 measure_perf.py [python|c]")
        sys.exit(1)
