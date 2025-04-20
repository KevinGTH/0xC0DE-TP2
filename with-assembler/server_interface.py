import requests
import ctypes
from gini_lib_client import MyClient


class GiniAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

        try:
            self.cclient = MyClient()
        except Exception as e:
            print(f"Error al cargar la biblioteca: {e}")
            exit(1)

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


    def float_to_int_gini(self, gini_value):
        #Convierte un valor float a int usando una funcion definida en C
        return self.cclient.float_to_int_gini(gini_value)

    @staticmethod
    def country_validation(data, target_country):
        list_countries = data[1]
        valid_countries_name = set()  # Creo una lista con solo los nombres de los paises de la API
        for entry in list_countries:
            country_name = entry.get('country', {}).get('value','').lower()
            if country_name:  # Me aseguro que solo se agregen paises con nombres distintos de None
                valid_countries_name.add(country_name)
        return target_country.lower() in valid_countries_name

    @staticmethod
    def get_available_years(data, target_country):
        list_years = set()
        for entry in data:
            if entry.get('country',{}).get('value').lower() == target_country.lower():
                list_years.add(entry.get('date'))
        return sorted(list_years)

    @staticmethod
    def get_gini(data_api, target_country, year_str):

        for entry in data_api:
            country = entry.get('country', {}).get('value', '').lower()
            value = entry.get('value')
            date_str = entry.get('date')

            # Busca la coincidencia exacta de país y año
            if country == target_country.lower() and date_str == year_str:
                try:
                    gini = float(value)
                    return gini
                except (ValueError, TypeError):
                    print(f"Warning: Valor GINI no numérico encontrado para {target_country} año {year_str}: {value}")
                    return None

        # Si algo salio mal
        return None
