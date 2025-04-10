import requests
import ctypes


class GiniAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url
        try:
            self.gini_lib = ctypes.CDLL("./libgini.so")
            self.gini_lib.float_to_int_gini.argtypes = [ctypes.c_double]
            self.gini_lib.float_to_int_gini.restype = ctypes.c_int
        except Exception as e:
            print(f"Error al cargar la biblioteca: {e}")
            exit(1)

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def country_validation(data, target_country):
        list_countries = data[1]
        valid_countries_name = set()  # Creo una lista con solo los nombres de los paises de la API
        for entry in list_countries:
            country_name = entry.get('country', {}).get('value','').lower()
            if country_name:  # Me aseguro que solo se agregen paises con nombres distintos de None
                valid_countries_name.add(country_name)
        return target_country.lower() in valid_countries_name

    def get_latest_gini(self, data, target_country):
        # Inicializo las variables
        latest_year = -1
        latest_gini = None

        for entry in data:
            # Sacamos valor de país, fecha y gini de forma segura
            country = entry.get('country', {}).get('value')
            date_str = entry.get('date')
            value = entry.get('value')

            # En caso de existir, buscamos el pais seleccionado y obtenemos sus datos
            if (not country or country.lower() != target_country.lower() or value is None):
                continue

            # Verificacion del tipo de dato obtenido
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

    def float_to_int_gini(self, gini_value):
        """Convierte un valor GINI de float a int usando la función de C."""
        return self.gini_lib.float_to_int_gini(gini_value)

