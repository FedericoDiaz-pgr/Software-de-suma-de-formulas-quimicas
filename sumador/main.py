import json
import os
import sys
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import ImageChops

# Función para obtener la ruta de los archivos en el ejecutable
def resource_path(relative_path):
    """Obtener la ruta de los archivos en el ejecutable."""
    if getattr(sys, 'frozen', False):
        # Ejecutándose en modo congelado
        base_path = sys._MEIPASS
    else:
        # Ejecutándose en modo normal
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Configuración de los pesos de los elementos (no se ha modificado)
element_weights = {
    # Aquí se incluyen los pesos de los elementos químicos...
}

def load_element_weights(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Ruta al archivo JSON
file_path = resource_path("archivo/element_weights.json")
# Cargar los pesos de los elementos desde el archivo
element_weights = load_element_weights(file_path)

def make_dict(result_formula):
    element_dict = {}
    i = 0
    
    while i < len(result_formula):
        element = result_formula[i]
        i += 1
        if i < len(result_formula) and result_formula[i].islower():
            element += result_formula[i]
            i += 1
        
        quantity = ''
        while i < len(result_formula) and result_formula[i].isdigit():
            quantity += result_formula[i]
            i += 1
        
        if quantity == '':
            quantity = 1
        else:
            quantity = int(quantity)
        
        if element in element_dict:
            element_dict[element] += quantity
        else:
            element_dict[element] = quantity
    
    return element_dict

def sumador():
    result_formula = formula_entry.get()
    result = make_dict(result_formula)
    suma = 0

    for key, values in result.items():
        suma += element_weights.get(key, 0) * values

    resultado_label.config(text=f"Total: {suma:.3f} g/mol")

def on_enter(event):
    animate_button_color(boton_sumar_pesos, 0)

def on_leave(event):
    ventana_principal.after_cancel(boton_sumar_pesos.after_id)
    boton_sumar_pesos.config(bg='SystemButtonFace', width=15, height=1)

def animate_button_color(button, color_step):
    if color_step <= 255:
        color = f'#{color_step:02x}{color_step:02x}ff'
        button.config(bg=color)
        button.after_id = ventana_principal.after(10, animate_button_color, button, color_step + 5)

def on_entry_focus_in(event):
    event.widget.config(bg="#DCE775", highlightbackground="#8BC34A")

def on_entry_focus_out(event):
    event.widget.config(bg="white", highlightbackground="gray")

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im




# Configuración de la ventana principal
ventana_principal = Tk()
ventana_principal.config(padx=200, pady=200, bg="#f8efc8")


# Estilo para el Entry
style = ttk.Style()
style.configure("TEntry",
                padding="5 5 5 5",
                relief="flat",
                foreground="black",
                fieldbackground="white",
                borderwidth=2,
                highlightthickness=1,
                highlightcolor="gray")

# Cargar las imágenes y rotarlas usando resource_path
image1 = Image.open(resource_path("images/quimica2.png"))
image1 = trim(image1)
image1 = image1.rotate(-2)  # Rotar la imagen 0 grados (sin rotar)
image1 = image1.resize((165,80))
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open(resource_path("images/cuadrado.jpg"))
image2 = trim(image2)
image2 = image2.resize((100,95))
image2 = ImageTk.PhotoImage(image2)

image3 = Image.open(resource_path("images/medidor.jpg"))
image3 = trim(image3)
image3 = image3.resize((100,130))
image3 = ImageTk.PhotoImage(image3)

image4 = Image.open(resource_path("images/hoh.jpg"))
image4 = trim(image4)
image4 = image4.resize((90,76))
image4 = ImageTk.PhotoImage(image4)

image5 = Image.open(resource_path("images/tubo.jpg"))
image5 = trim(image5)
image5 = image5.resize((70,75))
image5 = ImageTk.PhotoImage(image5)

image6 = Image.open(resource_path("images/gota.jpg"))
image6 = trim(image6)
image6 = image6.resize((100,100))
image6 = ImageTk.PhotoImage(image6)

image7 = Image.open(resource_path("images/molecula.jpg"))
image7 = trim(image7)
image7 = image7.resize((100,115))
image7 = ImageTk.PhotoImage(image7)

# Colocar las imágenes en la ventana
label_image1 = Label(ventana_principal, image=image1, bg="#f8efc8")
label_image1.place(x=-15, y=-75)  # Cambia las coordenadas según sea necesario

label_image2 = Label(ventana_principal, image=image2, bg="#f8efc8")
label_image2.place(x=200, y=125)  # Cambia las coordenadas según sea necesario

label_image3 = Label(ventana_principal, image=image3, bg="#f8efc8")
label_image3.place(x=-120, y=85)  # Cambia las coordenadas según sea necesario

label_image4 = Label(ventana_principal, image=image4, bg="#f8efc8")
label_image4.place(x=-120, y=-145)

label_image5 = Label(ventana_principal, image=image5, bg="#f8efc8")
label_image5.place(x=20, y=200)

label_image6 = Label(ventana_principal, image=image6, bg="#f8efc8")
label_image6.place(x=-190, y=-70)

label_image7 = Label(ventana_principal, image=image7, bg="#f8efc8")
label_image7.place(x=185, y=-150)

# Creación del campo de entrada y el botón
formula_entry = Entry(ventana_principal, highlightthickness=2, highlightbackground="gray", bd=0, relief="flat")
formula_entry.grid(column=0, row=0, pady=20, ipadx=5, ipady=5)

formula_entry.bind("<FocusIn>", on_entry_focus_in)
formula_entry.bind("<FocusOut>", on_entry_focus_out)

boton_sumar_pesos = Button(ventana_principal, text="Calcular", command=sumador, width=15, height=1)
boton_sumar_pesos.grid(column=0, row=1)

# Añadir eventos para animar el botón
boton_sumar_pesos.bind("<Enter>", on_enter)
boton_sumar_pesos.bind("<Leave>", on_leave)

# Etiqueta para mostrar el resultado
resultado_label = Label(ventana_principal, text="", bg="#f8efc8")
resultado_label.grid(column=0, row=2, pady=20)

ventana_principal.mainloop()
