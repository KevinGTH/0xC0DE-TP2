import tkinter as tk
from tkinter import messagebox

class GUI:
    """Clase para manejar la interfaz gráfica con Tkinter."""
    def __init__(self, api_client):
        self.api_client = api_client
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
        target_country = self.entry.get().strip()
        data = self.api_client.fetch_data()

        if data is None:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la API.")
            return

        if self.api_client.country_validation(data,target_country):
            latest_gini, latest_year = self.api_client.get_latest_gini(data[1], target_country)
            if latest_gini is None:
                self.result_label.config(text=f"No hay datos GINI para {target_country} en el rango solicitado.")
            else:
                int_gini = self.api_client.float_to_int_gini(latest_gini)
                self.result_label.config(
                    text=f"El índice GINI de {target_country} en {latest_year} es: {latest_gini:.2f}\n"
                         f"Valor entero: {int_gini}"
                )
        else:
            self.result_label.config(text=f"Error: El país '{target_country}' no se encontró en los datos de la API.")

    def run(self):
        self.root.mainloop()