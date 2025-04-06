import ctypes
import requests

def get_latest_gini(data, target_country):
    latest_year = -1
    latest_gini = None

    for entry in data:
        # Sacamos valor de país, fecha y gini de forma segura
        country = entry.get('country', {}).get('value')
        date_str = entry.get('date')
        value = entry.get('value')

        # Filtrar entradas sin país, sin valor o con value==None
        if (not country or
            country.lower() != target_country.lower() or
            value is None):
            continue

        try:
            year = int(date_str)
            gini = float(value)
        except (ValueError, TypeError):
            # si date_str no es entero o value no es float
            continue

        # Actualizamos si encontramos un año más reciente
        if year > latest_year:
            latest_year = year
            latest_gini = gini

    if latest_gini is None:
        return None, None

    return latest_gini, latest_year



API_URL= "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"

try:
    #Cargar libreria de C
    gini_lib= ctypes.CDLL("./libgini.so")

    # Definir los tipos de los argumentos y del valor de retorno de la función C
    gini_lib.float_to_int_gini.argtypes = [ctypes.c_double]      #Argumento del programa
    gini_lib.float_to_int_gini.restype = ctypes.c_int            #Tipo de retorno del programa

except AttributeError as e:
    print(f"Error: No se encontró la función 'float_to_int_gini' en la biblioteca.")
    exit(1)

#Obtener los datos de la API WorldBank
response=requests.get(API_URL)

if response:
    print("\nResponse server OK")
else:
    print("\nResponse server Failed")

data = response.json()

print("\nIntroduce el Pais: ")
target_country=input()

latest_gini, latest_year= get_latest_gini(data[1],target_country)
if latest_gini is None:
    print(f"No hay datos GINI para {target_country} en el rango solicitado.")
else:
    print(f"\nEl índice GINI de {target_country} en {latest_year} es: {latest_gini:.2f}")

    #Llamado a la funcion de C
    int_gini = gini_lib.float_to_int_gini(latest_gini)
    print(f"El nuevo valor (int) del índice GINI de {target_country} es: {int_gini}")

print("\nProceso completado.")








