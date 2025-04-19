import gini_utils
import requests
from gini_lib_client import MyClient

if __name__ == '__main__':
    API_URL= "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"

    cclient = MyClient()

    #Obtener los datos de la API WorldBank
    response=requests.get(API_URL)

    #Mensaje de conexion con el servidor
    if response:
        print("\nResponse server OK")
    else:
        print("\nResponse server Failed")

    data = response.json()

    print("\nIntroduce el Pais: ")
    target_country=input()

    if (server_interface.country_validation(data, target_country)):
        print(f"\nPaís '{target_country}' encontrado. Buscando índice GINI...")

        latest_gini, latest_year = gini_utils.get_latest_gini(data[1], target_country)
        if latest_gini is None:
            print(f"\nNo hay datos GINI para {target_country} en el rango solicitado.")
        else:
            print(f"\nEl índice GINI de {target_country} en {latest_year} es: {latest_gini:.2f}")

            # Llamado a la funcion de C
            int_gini = cclient.float_to_int_gini(latest_gini)
            print(f"El nuevo valor (int) del índice GINI de {target_country} es: {int_gini}")
    else:
        print(f"\nError: El país '{target_country}' no se encontró en los datos de la API")

    print("\nProceso completado.")








