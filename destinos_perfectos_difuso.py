import tkinter as tk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Función para centrar la ventana en la pantalla
def centrar_ventana(root, ancho, alto):
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema Difuso - Destinos Perfectos")
centrar_ventana(root, 400, 300)

# Variables difusas
preferencias = ctrl.Antecedent(np.arange(0, 11, 1), 'preferencias')
tipo_viaje = ctrl.Antecedent(np.arange(0, 11, 1), 'tipo_viaje')
presupuesto = ctrl.Antecedent(np.arange(0, 11, 1), 'presupuesto')
destino = ctrl.Consequent(np.arange(0, 11, 1), 'destino')

# Definición de funciones de pertenencia
preferencias['playa'] = fuzz.trimf(preferencias.universe, [0, 0, 5])
preferencias['cultura'] = fuzz.trimf(preferencias.universe, [0, 5, 10])
preferencias['aventura'] = fuzz.trimf(preferencias.universe, [5, 10, 10])

tipo_viaje['individual'] = fuzz.trimf(tipo_viaje.universe, [0, 0, 5])
tipo_viaje['familiar'] = fuzz.trimf(tipo_viaje.universe, [0, 5, 10])
tipo_viaje['grupal'] = fuzz.trimf(tipo_viaje.universe, [5, 10, 10])

presupuesto['bajo'] = fuzz.trimf(presupuesto.universe, [0, 0, 5])
presupuesto['medio'] = fuzz.trimf(presupuesto.universe, [0, 5, 10])
presupuesto['alto'] = fuzz.trimf(presupuesto.universe, [5, 10, 10])

destino['economico'] = fuzz.trimf(destino.universe, [0, 0, 5])
destino['medio'] = fuzz.trimf(destino.universe, [0, 5, 10])
destino['lujoso'] = fuzz.trimf(destino.universe, [5, 10, 10])

# Definir las reglas difusas
rule1 = ctrl.Rule(preferencias['playa'] & tipo_viaje['individual'] & presupuesto['bajo'], destino['economico'])
rule2 = ctrl.Rule(preferencias['cultura'] & tipo_viaje['familiar'] & presupuesto['medio'], destino['medio'])
rule3 = ctrl.Rule(preferencias['aventura'] & tipo_viaje['grupal'] & presupuesto['alto'], destino['lujoso'])

# Reglas adicionales para más combinaciones
rule4 = ctrl.Rule(preferencias['cultura'] & tipo_viaje['individual'] & presupuesto['alto'], destino['lujoso'])
rule5 = ctrl.Rule(preferencias['playa'] & tipo_viaje['familiar'] & presupuesto['medio'], destino['medio'])
rule6 = ctrl.Rule(preferencias['aventura'] & tipo_viaje['individual'] & presupuesto['bajo'], destino['economico'])

controlador_destinos = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
simulador = ctrl.ControlSystemSimulation(controlador_destinos)

# Función para mostrar la gráfica de la variable 'destino'
def mostrar_grafica():
    destino.view(sim=simulador)
    plt.show()

# Función para ejecutar el sistema difuso
def calcular_destino():
    try:
        # Obtener los valores de las entradas
        pref = float(entry_preferencias.get())
        tipo = float(entry_tipo_viaje.get())
        pres = float(entry_presupuesto.get())
        
        # Asignar valores a las entradas del simulador
        simulador.input['preferencias'] = pref
        simulador.input['tipo_viaje'] = tipo
        simulador.input['presupuesto'] = pres
        
        # Ejecutar simulación
        simulador.compute()
        
        # Obtener el resultado
        if 'destino' in simulador.output:
            destino_recomendado = simulador.output['destino']
        else:
            messagebox.showwarning("Advertencia", "No se pudo calcular un destino para los valores dados. Intenta con diferentes entradas.")
            return
        
        # Determinar la categoría del destino
        if destino_recomendado <= 3.33:
            categoria = "económico"
        elif destino_recomendado <= 6.66:
            categoria = "medio"
        else:
            categoria = "lujoso"
        
        # Mostrar el resultado en un mensaje emergente
        messagebox.showinfo("Recomendación", f"El destino recomendado tiene una puntuación de: {destino_recomendado:.2f}\nCategoría del destino: {categoria}")
        
        # Mostrar la gráfica
        mostrar_grafica()
    
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores válidos para todas las entradas.")

# Etiquetas y cuadros de entrada
label_preferencias = tk.Label(root, text="Preferencias (0-10):")
label_preferencias.pack(pady=10)
entry_preferencias = tk.Entry(root)
entry_preferencias.pack()

label_tipo_viaje = tk.Label(root, text="Tipo de viaje (0-10):")
label_tipo_viaje.pack(pady=10)
entry_tipo_viaje = tk.Entry(root)
entry_tipo_viaje.pack()

label_presupuesto = tk.Label(root, text="Presupuesto (0-10):")
label_presupuesto.pack(pady=10)
entry_presupuesto = tk.Entry(root)
entry_presupuesto.pack()

# Botón para ejecutar el cálculo
btn_calcular = tk.Button(root, text="Calcular Destino", command=calcular_destino)
btn_calcular.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
