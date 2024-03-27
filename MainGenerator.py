import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import ttk, filedialog, Label, Entry, Text, Frame, Canvas
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os
import numpy as np
import time
import random


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generadores de Números Pseudoaleatorios")

        # Botones para seleccionar generador
        ttk.Button(self.root, text="Cuadrados Medios", command=self.open_cuadrados_medios).pack(pady=10)
        ttk.Button(self.root, text="Congruencial Lineal", command=self.open_congruencial_lineal).pack(pady=10)
        ttk.Button(self.root, text="Distribucion Uniforme", command=self.open_distribucion_uniforme).pack(pady=10)
        ttk.Button(self.root, text="Distribucion Normal", command=self.open_distribucion_normal).pack(pady=10)
        ttk.Button(self.root, text="Generar Ni", command=self.open_generar_ni).pack(pady=10)


    def open_cuadrados_medios(self):
        # Cerrar la ventana actual y abrir la interfaz para el generador de cuadrados medios
        self.root.destroy()
        root_cm = tk.Tk()  # Crear una nueva instancia de Tk
        CuadradosMediosApp(root_cm)  # Pasar la instancia de Tk como argumento

    def open_congruencial_lineal(self):
        # Cerrar la ventana actual y abrir la interfaz para el generador congruencial lineal
        self.root.destroy()
        root_cl = tk.Tk()  # Crear una nueva instancia de Tk
        CongruencialLinealApp(root_cl)  # Pasar la instancia de Tk como argumento

    def open_distribucion_uniforme(self):
        # Cerrar la ventana actual y abrir la interfaz para el generador distribución uniforme
        self.root.destroy()
        root_du = tk.Tk()  # Crear una nueva instancia de Tk
        DistribucionUniforme(root_du)  # Pasar la instancia de Tk como argumento

    def open_distribucion_normal(self):
        # Cerrar la ventana actual y abrir la interfaz para el generador distribución normal
        self.root.destroy()
        root_dn = tk.Tk()  # Crear una nueva instancia de Tk
        NormalDistributionGenerator(root_dn)  # Pasar la instancia de Tk como argumento

    def open_generar_ni(self):
        # Cerrar la ventana actual y abrir la interfaz para generar Ni
        self.root.destroy()
        root_gn = tk.Tk()  # Crear una nueva instancia de Tk
        GeneratorNi(root_gn)  # Pasar la instancia de Tk como argumento


class CuadradosMediosApp:
    """
    Aplicación para generar números pseudoaleatorios utilizando el método de los cuadrados medios.
    """

    def __init__(self, root):

        self.root = root
        self.root.title("Generador Pseudoaleatorio - Cuadrados Medios")

        # Variables
        self.seed_var = tk.StringVar()
        self.num_var = tk.IntVar()

        # Interfaz gráfica
        self.create_widgets()

        # Consolas
        self.create_consoles()

    def create_widgets(self):
        """
        Se crean los widgets de la interfaz gráfica.
        """
        # Labels
        ttk.Label(self.root, text="Semilla (n>=3)").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(self.root, text="Número de Iteraciones").grid(row=1, column=0, padx=10, pady=10)

        # Entry Widgets
        ttk.Entry(self.root, textvariable=self.seed_var).grid(row=0, column=1, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.num_var).grid(row=1, column=1, padx=10, pady=10)

        # Button
        ttk.Button(self.root, text="Generar", command=self.generate_numbers).grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(self.root, text="Volver al Menú Principal", command=self.go_back_to_main_menu).grid(row=3, column=0, columnspan=2, pady=20)

    def create_consoles(self):
        """
        Se crean las consolas para mostrar los valores de Ri y Xi generados.
        """
        # Consola para Ri
        ttk.Label(self.root, text="Números Ri Generados", font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=2, sticky="ew")
        self.console_ri = tk.Text(self.root, height=10, width=50)
        self.console_ri.grid(row=5, column=0, padx=10, pady=10)

        # Consola para Xi
        ttk.Label(self.root, text="Números Xi Generados", font=('Arial', 12, 'bold')).grid(row=4, column=1, columnspan=2, sticky="ew")
        self.console_xi = tk.Text(self.root, height=10, width=50)
        self.console_xi.grid(row=5, column=1, padx=10, pady=10)

    def generate_numbers(self):
        """
        Se generan los números pseudoaleatorios utilizando el método de los cuadrados medios.
        """

        #Se obtienen los valores de las variables ingresadas por el usuario como lo es la semilla y el numero de iteraciones
        seed = self.seed_var.get()
        num_iterations = self.num_var.get()

        #Se verifica que la longitud de la semilla sea mayor o igual a 3
        if len(seed) < 3:
            tk.messagebox.showerror("Error", "La semilla debe tener al menos 3 dígitos.")
            return

        ri_values = []
        xi_values = []
        generated_numbers = set()

        #Se elevan los valores Xi al cuadrado
        for _ in range(num_iterations):
            seed_squared = int(seed) ** 2
            seed_str = str(seed_squared).zfill(2 * len(seed))

            # Se obtienen los números centrales
            num_digits = len(seed)
            half_length = len(seed_str) // 2
            start_index = half_length - num_digits // 2
            end_index = half_length + num_digits // 2

            # Se ajusta la longitud para no perder la integridad
            if end_index - start_index < num_digits:
                seed_str = seed_str.zfill(2 * num_digits)

            xi_str = seed_str[start_index:end_index]

            # Se normaliza el número para estar en el intervalo [0, 1]
            ri = int(xi_str) / (10 ** num_digits)

            # Se verifica si se ha generado antes el mismo número
            if ri in generated_numbers:  
                tk.messagebox.showwarning("Advertencia", "Se detectó una secuencia repetitiva. Deteniendo la generación de números.")
                break

            #Se agrega el numero pseudoaleatorio ri a la lista de ri_values
            ri_values.append(ri)
            #Se agrega el numero pseudoaleatorio ri a la lista de verificacion de duplicados, esto con el fin de observar los periodos de numeros
            generated_numbers.add(ri)

            #Se agrega el numero pseudoaleatorio xi a la lista de xi_values
            xi_values.append(int(xi_str))
            
            #Se actualiza la semilla
            seed = xi_str

        # Se muestran los resultados en consolas
        self.show_results_in_console(ri_values, self.console_ri)
        self.show_results_in_console(xi_values, self.console_xi)

        # Se guardan los resultados en un archivo CSV
        self.save_to_csv(ri_values)

        # Se grafican los resultados
        self.plot_results(ri_values)

    def go_back_to_main_menu(self):
        self.root.destroy()
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()

    def show_results_in_console(self, values, console):
        """
        Se muestran los valores generados en la consola correspondiente.
        """
        console.delete(1.0, tk.END)  # Se limpia la consola antes de mostrar nuevos valores
        for value in values:
            console.insert(tk.END, f"{value}\n")  # Se agrega el valor a la consola

    def save_to_csv(self, data):
        """
        Se guardan los números pseudoaleatorios generados en un archivo CSV.

        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'numeros_ri_cuadrados_medios.csv')

        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for ri in data:
                writer.writerow([ri])

    def plot_results(self, data):
        """
        Se grafican los números pseudoaleatorios generados.

        """
        fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
        ax.plot(data, marker='o', linestyle='-', color='b')
        ax.set_title("Números Ri Pseudoaleatorios Generados")
        ax.set_xlabel("Iteración")
        ax.set_ylabel("Valor")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=6, column=0, columnspan=2, padx=10, pady=10)  # Se usa la fila 5

class CongruencialLinealApp:

    """
    Aplicación para generar números pseudoaleatorios utilizando el método de los congruencias.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Generador Pseudoaleatorio")

        # Variables
        self.k_var = tk.IntVar()
        self.c_var = tk.IntVar()
        self.g_var = tk.IntVar()
        self.seed_var = tk.IntVar()
        self.num_var = tk.IntVar()

        # Interfaz gráfica
        self.create_widgets()


    #Crear lso widgets de la interfaz 
    def create_widgets(self):
        # Labels
        ttk.Label(self.root, text="Semilla").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(self.root, text="Parámetro 'k'").grid(row=1, column=0, padx=10, pady=10)
        ttk.Label(self.root, text="Parámetro 'c'").grid(row=2, column=0, padx=10, pady=10)
        ttk.Label(self.root, text="Parámetro 'g'").grid(row=3, column=0, padx=10, pady=10)
        ttk.Label(self.root, text="Número de Iteraciones").grid(row=4, column=0, padx=10, pady=10)

        # Entry Widgets
        ttk.Entry(self.root, textvariable=self.seed_var).grid(row=0, column=1, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.k_var).grid(row=1, column=1, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.c_var).grid(row=2, column=1, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.g_var).grid(row=3, column=1, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.num_var).grid(row=4, column=1, padx=10, pady=10)

        # Button
        ttk.Button(self.root, text="Generar", command=self.generate_numbers).grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(self.root, text="Volver al Menú Principal", command=self.go_back_to_main_menu).grid(row=6, column=0, columnspan=2, pady=20)
        # Text Widgets for Xi and Ri
        self.text_output_xi = self.create_console("Números Xi Generados", row=7, column=0)
        self.text_output_ri = self.create_console("Números Ri Generados", row=7, column=1)


    def create_console(self, title, row, column):
        """
        Se crea una consola para mostrar los valores Xi y Ri.
        """
        ttk.Label(self.root, text=title, font=('Arial', 12, 'bold')).grid(row=row, column=column, columnspan=2, sticky="ew")
        text_widget = ScrolledText(self.root, width=1, height=10)  # Usamos un ancho inicial mínimo
        text_widget.grid(row=row+1, column=column, columnspan=2, padx=10, pady=10)
        return text_widget

    """
        Se generan los números pseudoaleatorios utilizando el método de congruencias.
        """
    #Se obtienen los valores ingresados por el usuario respecto a los parametros 
    def generate_numbers(self):
        k = self.k_var.get()
        c = self.c_var.get()
        g = self.g_var.get()
        seed = self.seed_var.get()
        num_iterations = self.num_var.get()

        #Se declaran arreglos para guardar el resultado de las iteraciones y de igual manera variables para el periodo de los numeros
        xi_values = []
        ri_values = []
        period_detected = False
        period_start_index = 0
        
        # Método congruencial lineal, se calculan algunos parametros
        for i in range(num_iterations):
            a = 1 + 2 * k
            m = 2 ** g
            seed = (a * seed + c) % m 
            xi_values.append(seed)

            # Calcular el valor de Ri
            ri_value = seed / (m - 1)
            if abs(ri_value - 1) < 1e-10 or abs(ri_value) < 1e-10:
                continue
            
            #Se truncan los valores para las pruebas
            ri_truncated = int(ri_value * 10**5) / 10**5
            ri_values.append(ri_truncated)

            # Mostrar valores de Xi y Ri en los cuadros de texto respectivos
            self.text_output_xi.insert(tk.END, f"Iteración {i+1} - Xi: {seed}\n")
            self.text_output_ri.insert(tk.END, f"Iteración {i+1} - Ri: {ri_truncated}\n")
            self.text_output_xi.see(tk.END) 
            self.text_output_ri.see(tk.END)  


            # Verificar si se ha detectado un período
            if seed in xi_values[:i]:
                period_detected = True
                break

            # Calcular el ancho máximo necesario para ambos cuadros de texto
            max_width_xi = max(len(f"Iteración {i+1} - Xi: {seed}") for i, seed in enumerate(xi_values))
            max_width_ri = max(len(f"Iteración {i+1} - Ri: {ri_truncated}") for i, ri_truncated in enumerate(ri_values))

            # Ajustar el ancho de los cuadros de texto
            self.text_output_xi.configure(width=max_width_xi + 20)  
            self.text_output_ri.configure(width=max_width_ri + 2)

        #Si se detecta un periodo, se guarda el conjunto de numeros antes de repetir la secuencia nuevamente 
        if period_detected:
            period_length = len(xi_values) - period_start_index
            print("Período detectado desde la iteración", period_start_index, "hasta la iteración", len(xi_values))
            print("Longitud del período:", period_length)
            period_values = xi_values 
            period_ri_values = ri_values[:len(ri_values)]

            # Guardar el período en un archivo CSV
            self.save_to_csv(period_ri_values, "numeros_ri_congruencia_periodo.csv")

            # Graficar el período
            self.plot_results(period_ri_values)
        else:
            # Mostrar resultados en consola
            print("No se detectó un período en las primeras", num_iterations, "iteraciones.")

        # Guardar los resultados en un archivo CSV
        self.save_to_csv(ri_values, "numeros_ri_congruencia.csv")

        # Graficar los resultados
        self.plot_results(ri_values)

    #Volver al menu inicial
        
    def go_back_to_main_menu(self):
        self.root.destroy()
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()

    #Funcion para guardar resultados en archivo csv
    def save_to_csv(self, data, filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, filename)

        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for ri in data:
                writer.writerow([ri])

    #Graficar los resultados
    def plot_results(self, data):
        fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
        ax.plot(data, marker='o', linestyle='-', color='b')
        ax.set_title("Números Pseudoaleatorios Generados")
        ax.set_xlabel("Iteración")
        ax.set_ylabel("Valor")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=9, column=0, columnspan=2, padx=10, pady=10)



class DistribucionUniforme:

    def __init__(self, root):
        self.root = root
        self.root.title("Generador de números pseudoaleatorios - Distribución Uniforme")

        self.min_label = Label(root, text="Valor mínimo (a):")
        self.min_label.grid(row=1, column=0, padx=5, pady=5)
        self.min_entry = Entry(root)
        self.min_entry.grid(row=1, column=1, padx=5, pady=5)

        self.max_label = Label(root, text="Valor máximo (b):")
        self.max_label.grid(row=2, column=0, padx=5, pady=5)
        self.max_entry = Entry(root)
        self.max_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.generate_button = ttk.Button(root, text="Generar números", command=self.generate_random_numbers)
        self.generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.min_xi_label = Label(root, text="Mínimo generado (Xi):")
        self.min_xi_label.grid(row=5, column=0, padx=5, pady=5)
        self.min_xi_value = Label(root, text="")
        self.min_xi_value.grid(row=5, column=1, padx=5, pady=5)

        self.max_xi_label = Label(root, text="Máximo generado (Xi):")
        self.max_xi_label.grid(row=6, column=0, padx=5, pady=5)
        self.max_xi_value = Label(root, text="")
        self.max_xi_value.grid(row=6, column=1, padx=5, pady=5)

        self.result_text = Text(root, height=10, width=50)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.histogram_frame = Frame(root)
        self.histogram_frame.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.xi_values = []

    def generate_random_numbers(self):
        try:
            # Obtener los valores mínimo y máximo (a y b)
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())

            # Generar 10,000 datos Xi dentro de los rangos ingresados
            self.xi_values = [random.uniform(min_val, max_val) for _ in range(1000000)]

            # Calcular el mínimo y el máximo de los datos Xi generados
            min_generated = min(self.xi_values)
            max_generated = max(self.xi_values)

            # Mostrar los valores mínimo y máximo de los Xi en la interfaz gráfica
            self.min_xi_value.config(text=str(min_generated))
            self.max_xi_value.config(text=str(max_generated))


            # Leer un archivo CSV para obtener los valores Ri
            file_path = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
            if file_path:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    ri_values = [float(value) for row in reader for value in row if value.strip()]

                # Aplicar la fórmula Ni = a + (b - a) * Ri a cada Xi
                n_values = [min_generated + (max_generated - min_generated) * ri for ri in ri_values]

                # Crear histograma
                plt.figure(figsize=(6, 4))
                plt.hist(n_values, bins=20, color='skyblue', edgecolor='black')
                plt.xlabel('Valores Ni')
                plt.ylabel('Frecuencia')
                plt.title('Histograma de valores Ni')
                plt.grid(True)
                
                # Mostrar histograma en la interfaz gráfica
                self.plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.histogram_frame)
                self.plot_canvas.draw()
                self.plot_canvas.get_tk_widget().pack(fill='both', expand=True)

                # Mostrar en la consola
                self.result_text.delete('1.0', 'end')  # Limpiar el contenido anterior
                self.result_text.insert('end', "Números Ni generados a partir de los datos Xi y Ri:\n")
                for ni in n_values:
                    truncated_ni = round(ni, 5)  # Truncar a 5 decimales
                    self.result_text.insert('end', str(truncated_ni) + '\n')

                # Guardar en un archivo CSV
                nombre_archivo = "numeros_ni_DistUniforme.csv"
                with open(nombre_archivo, 'w', newline='') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv, delimiter=';')
                    for numero in n_values:
                        escritor_csv.writerow(['{:.5f}'.format(numero).replace('.', ',')])

                self.result_text.insert('end', f"\nMínimo generado (Xi): {min_generated}\nMáximo generado (Xi): {max_generated}")
        except Exception as e:
            self.result_text.delete('1.0', 'end')  # Limpiar el contenido anterior
            self.result_text.insert('end', f"Error: {str(e)}")


import tkinter as tk
from tkinter import filedialog
import csv
import numpy as np
import matplotlib.pyplot as plt
import time
import random

class NormalDistributionGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Números Pseudoaleatorios con Distribución Normal")
        
        self.min_label = tk.Label(root, text="Mínimo (Xi):")
        self.min_label.grid(row=0, column=0, padx=10, pady=10)
        self.min_entry = tk.Entry(root)
        self.min_entry.grid(row=0, column=1, padx=10, pady=10)

        self.max_label = tk.Label(root, text="Máximo (Xi):")
        self.max_label.grid(row=1, column=0, padx=10, pady=10)
        self.max_entry = tk.Entry(root)
        self.max_entry.grid(row=1, column=1, padx=10, pady=10)

        self.info_text = tk.Text(root, height=10, width=50)
        self.info_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.load_button = tk.Button(root, text="Cargar archivo Ri", command=self.load_file)
        self.load_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.generate_button = tk.Button(root, text="Generar", command=self.generate_numbers)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Seleccione el archivo Ri", filetypes=[("Archivos CSV", "*.csv")])
        if file_path:
            self.ri_data = self.read_csv(file_path)
            self.result_label.config(text=f"Archivo Ri cargado correctamente: {len(self.ri_data)} valores.")

    def read_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        return [float(val) for row in data for val in row]

    def generate_numbers(self):
        try:
            min_xi = float(self.min_entry.get())
            max_xi = float(self.max_entry.get())
            if not hasattr(self, 'ri_data'):
                self.result_label.config(text="Error: Cargue primero el archivo Ri.")
                return

            current_time = int(time.time())
            random.seed(current_time)
            self.xi_values = [random.random() for _ in range(10000)]

            mean_xi = np.mean(self.xi_values)
            stddev_xi = np.std(self.xi_values)

            current_time = int(time.time())
            np.random.seed(current_time)
            ni_data = np.random.normal(mean_xi, stddev_xi, len(self.ri_data))

            # Calcular los intervalos a partir de los datos generados
            intervals = plt.hist(ni_data, bins=20, edgecolor='black')[1]
            min_ni = np.min(ni_data)
            max_ni = np.max(ni_data)
            
            # Actualizar el cuadro de texto con los datos
            info_text_content = f'Media de Xi: {mean_xi:.2f}\n'
            info_text_content += f'Desviación Estándar de Xi: {stddev_xi:.2f}\n'
            info_text_content += f'Mínimo de Xi: {min_xi}\n'
            info_text_content += f'Máximo de Xi: {max_xi}\n'
            info_text_content += '\nIntervalos:\n'
            for i in range(len(intervals) - 1):
                info_text_content += f'{intervals[i]:.2f}-{intervals[i+1]:.2f}\n'
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info_text_content.strip())

            plt.hist(ni_data, bins=20, edgecolor='black')
            plt.title('Distribución Normal de Ni')
            plt.xlabel('Ni')
            plt.ylabel('Frecuencia')
            plt.grid(True)
            plt.show()

        except ValueError:
            self.result_label.config(text="Error: Ingrese valores válidos para mínimo y máximo.")




class GeneratorNi: 
    def __init__(self, root):
        self.root = root
        self.root.title("Convertir Números Pseudoaleatorios a Números Aleatorios Acumulados")

        # Variables
        self.a_var = tk.DoubleVar()
        self.b_var = tk.DoubleVar()

        # Interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Labels y campos de entrada para a y b
        ttk.Label(self.root, text="Valor de a:").pack()
        ttk.Entry(self.root, textvariable=self.a_var).pack()

        ttk.Label(self.root, text="Valor de b:").pack()
        ttk.Entry(self.root, textvariable=self.b_var).pack()

        # Botón para seleccionar el archivo CSV y convertir los números
        ttk.Button(self.root, text="Seleccionar archivo", command=self.convertir_numeros).pack()

    def convertir_numeros(self):
        a = self.a_var.get()
        b = self.b_var.get()

        # Abrir el diálogo para seleccionar el archivo CSV
        archivo_csv = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))

        if archivo_csv:
            try:
                # Leer los números pseudoaleatorios del archivo CSV
                with open(archivo_csv, 'r') as archivo:
                    lector_csv = csv.reader(archivo)
                    numeros_pseudoaleatorios = [float(row[0]) for row in lector_csv]

                # Calcular los números aleatorios acumulados (Ni)
                numeros_acumulados = [a + (b - a) * numero for numero in numeros_pseudoaleatorios]

                # Guardar los números aleatorios acumulados en un archivo CSV
                nombre_archivo = "numeros_ni_final.csv"
                with open(nombre_archivo, 'w', newline='') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv, delimiter=';')
                    for numero in numeros_acumulados:
                        escritor_csv.writerow(['{:.5f}'.format(numero).replace('.', ',')])

                # Mostrar los resultados en la interfaz gráfica
                messagebox.showinfo("Información", "Números Aleatorios Acumulados (Ni) generados y guardados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar el archivo CSV: {e}")

    

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    app = MainApp(root)
    root.mainloop()
