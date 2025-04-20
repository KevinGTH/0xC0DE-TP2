import tkinter as tk
from tkinter import messagebox,ttk

class GUI:
    def __init__(self, api_client):
        #Ventana Principal
        self.api_client = api_client
        self.root = tk.Tk()
        self.root.title("Visor Índice GINI")
        self.root.geometry("600x300") #

        self.current_country = tk.StringVar()
        self.selected_year = tk.StringVar()
        self.available_years = []
        self.current_api_data = None # Para almacenar temporalmente los datos
        self.result_label=None
        self.list_year=None
        self.select_country=None
        self.button_find_years=None

        #Crear interfaz
        self.create_frame_country()
        self.create_frame_year()
        self.create_frame_results()

    def run(self):
        self.root.mainloop()

    def create_frame_country(self):
        frame_country = tk.Frame(self.root)
        frame_country.pack(pady=10, padx=10, fill=tk.X)
        label_country = tk.Label(frame_country, text="Introduce el País:")
        label_country.pack(side=tk.LEFT, padx=5)
        # Asociamos el texto escrito con el argumento del pais solicitado a la API
        self.select_country = tk.Entry(frame_country, textvariable=self.current_country, width=30)
        self.select_country.pack(side=tk.LEFT)
        # Frame para comenzar la busqueda
        self.button_find_years = tk.Button(frame_country, text="Seleccionar", command=self.find_country_and_years)
        self.button_find_years.pack(side=tk.LEFT)
        # También asociamos la tecla "Enter" y comenzamos la busqueda
        self.select_country.bind("<Return>", self.find_country_and_years)

    def create_frame_year(self):
        # Frame para seleccionar el año
        frame_year = tk.Frame(self.root)
        frame_year.pack(pady=10, padx=10, fill=tk.X)
        label_year = tk.Label(frame_year, text="Seleccionar año:")
        label_year.pack(side=tk.LEFT, padx=5)
        self.list_year = ttk.Combobox(frame_year, textvariable=self.selected_year, state="disabled", width=10)
        self.list_year.pack(side=tk.LEFT, padx=5)
        self.list_year.bind("<<ComboboxSelected>>", self.show_gini_for_year) #La variable toma valor al seleccionar el año

    def create_frame_results(self):
        # Frame para mostrar resultados
        frame_result = tk.Frame(self.root)
        frame_result.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.result_label = tk.Label(frame_result, wraplength=400, justify="left", anchor="nw")
        self.result_label.pack(pady=10, fill=tk.BOTH, expand=True)

    def fetch_and_validate_country(self,country):
        if not country:
            messagebox.showwarning("Entrada Vacía", "Por favor, introduce un nombre de país.")
            return None
        self.result_label.config(text=f"Buscando datos del país {country}...")
        self.root.update_idletasks()  # Forzar actualización de la GUI
        data = self.api_client.fetch_data()
        if self.api_client.country_validation(data, country):
            return data
        self.result_label.config(text=f"Error: El país '{country}' no se encontró en los datos de la API.")
        return None

    def find_country_and_years(self, event=None): # event=None para que funcione con el botón y Enter
        target_country = self.current_country.get().strip()
        data = self.fetch_and_validate_country(target_country)
        if data:
            self.current_api_data = data[1]
            self.available_years = self.api_client.get_available_years(data[1], target_country)
            self.list_year['values'] = self.available_years
            self.list_year.config(state="readonly")
            self.result_label.config(text=f"Seleccione uno de los años disponibles del país '{target_country.capitalize()}'.")
            self.selected_year.set(self.available_years[0] if self.available_years else "")

    def show_gini_for_year(self, event=None):
        gini_value = self.api_client.get_gini(self.current_api_data, self.current_country.get(), self.selected_year.get())
        if gini_value is None:
            self.result_label.config(
                text=f"No hay registro del índice GINI para el país '{self.current_country.get().capitalize()}' en el año {self.selected_year.get()}.")
        else:
            int_gini = self.api_client.float_to_int_gini(gini_value)
            self.result_label.config(text=f"Índice GINI del país '{self.current_country.get().capitalize()}' en el año {self.selected_year.get()}:\n"
                                          f"Valor: {gini_value:.2f}\n"
                                          f"Valor entero (truncado+1) con C: {str(int_gini)}")
