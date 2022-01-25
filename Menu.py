#UNIVERSIDAD SAN CARLOS DE GUATEMALA
#FACULTADE DE INGENIERIA
#ESCUELA DE MECANICA ELECTRICA
#LABORATORIO DE ROBOTIA

#--------------------------------- Gurpo No.4 ------------------------
#Nonbre: Frank Robinson Morales Hernandez       Carne: 201503767
#Nombre: Adolfo Max Rodriguez Pimentesl         Carne: 201444696

import tkinter 
from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox

# ------------ parametros de la Ventana --------------------
ventana = tkinter.Tk()
ventana.title("Modo de Funcionamiento")
ventana.geometry("600x300") 

#----------------- Imange de Fondo ------------------------
img = Image.open('Brazo_Robotico.jpg')
new_img = img.resize((380,256))
render = ImageTk.PhotoImage(new_img)
img1 = Label(ventana, image = render)
img1.image = render
img1.place(x=160, y=0)

#--------- Cracion de Botonoes -------------------------
boton1 = tkinter.Button(ventana, text = "Dectecion por Forma", width = 20, height = 5, command = lambda: formas(50))
boton2 = tkinter.Button(ventana, text = "Deteccion por Color", width = 20, height = 5, command = lambda: colores(60))

boton1.grid(row = 1, column = 1, columnspan = 5, padx = 5, pady = 5)
boton2.grid(row = 2, column = 1, columnspan = 5, padx = 5, pady = 5)

#------------- funciones --------------------------

def formas(valor):
    import Deteccion_Figuras_V_REP
    return

def colores(valor):
    import Deteccion_Colores_V_REP   
    return


ventana.mainloop()