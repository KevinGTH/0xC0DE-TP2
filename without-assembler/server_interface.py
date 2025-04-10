import requests
import tkinter as tk
from tkinter import messagebox

class GiniAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def country_validation(self, data, target_country):
        list_countries = data[1]
        valid_countries_name = set()  # Creo una lista con solo los nombres de los paises de la API
        for entry in list_countries:
            country_name = entry.get('country', {}).get('value','').lower()
            if country_name:  # Me aseguro que solo se agregen paises con nombres distintos de None
                valid_countries_name.add(country_name)
        return target_country.lower() in valid_countries_name

class GUI:
    """Clase para manejar la interfaz gráfica con Tkinter."""
    def __init__(self, api_client, calculator):
        self.api_client = api_client
        self.calculator = calculator
        self.root = tk.Tk()
        self.root.title("Índice GINI")
        self.root.geometry("400x300")
        self.elementos_interfaz()

    def elementos_interfaz(self):
        self.label = tk.Label(self.root, text="Introduce el País:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=25)

        self.button = tk.Button(self.root, text="Buscar", command=self.search)
        self.button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=350, justify="left")
        self.result_label.pack(pady=10)

    def search(self):
        """Busca y muestra el índice GINI del país ingresado."""
        target_country = self.entry.get().strip()
        data = self.api_client.fetch_data()

        if data is None:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la API.")
            return

        if self.api_client.country_validation(data,target_country):
            latest_gini, latest_year = self.calculator.get_latest_gini(data[1], target_country)
            if latest_gini is None:
                self.result_label.config(text=f"No hay datos GINI para {target_country} en el rango solicitado.")
            else:
                int_gini = self.calculator.float_to_int_gini(latest_gini)
                self.result_label.config(
                    text=f"El índice GINI de {target_country} en {latest_year} es: {latest_gini:.2f}\n"
                         f"Valor entero: {int_gini}"
                )
        else:
            self.result_label.config(text=f"Error: El país '{target_country}' no se encontró en los datos de la API.")

    def run(self):
        self.root.mainloop()