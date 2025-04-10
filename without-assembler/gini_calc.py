import ctypes

class GiniCalculator:
    """Clase para procesar los datos del índice GINI."""
    def __init__(self):
        try:
            self.gini_lib = ctypes.CDLL("./libgini.so")
            self.gini_lib.float_to_int_gini.argtypes = [ctypes.c_double]
            self.gini_lib.float_to_int_gini.restype = ctypes.c_int
        except Exception as e:
            print(f"Error al cargar la biblioteca: {e}")
            exit(1)

    def get_latest_gini(self, data, target_country):
        """Obtiene el último índice GINI disponible para un país."""
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

