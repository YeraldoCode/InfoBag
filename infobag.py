import requests
from bs4 import BeautifulSoup
import tkinter as tk 
from tkinter import messagebox

ventana = tk.Tk()
ventana.geometry('900x400')
ventana.title('InfoBag by Yera')

paleta_dia = {
    'ventana_bg': '#E3F2FD',
    'frame_bg': '#F9FAFB',
    'boton_bg': '#007BFF',
    'boton_fg': 'white',
    'texto_etiquetas_fg': '#333333',
    'etiqueta_bg': '#DDEAF6',
    'valor_bg': '#FFFFFF',
    'valor_fg': '#333333'
}

# Paleta de colores para noche
paleta_noche = {
    'ventana_bg': '#1C1C1E',
    'frame_bg': '#2C2C2E',
    'boton_bg': '#0A84FF',
    'boton_fg': 'white',
    'texto_etiquetas_fg': '#F5F5F5',
    'etiqueta_bg': '#4D4D4D',
    'valor_bg': '#000000',
    'valor_fg': '#FFFFFF'
}

#establecer modo noche
modo_noche = False


def aplicar_paleta(paleta):
    ventana.config(bg=paleta['ventana_bg'])
    frame_interior.config(bg=paleta['frame_bg'])
    boton_info.config(bg=paleta['boton_bg'], fg=paleta['boton_fg'])
    entrada_simbolo.config(bg=paleta['valor_bg'], fg=paleta['valor_fg'])

    #actualizar widgets 
    for widget in frame_interior.winfo_children():
        if isinstance(widget, tk.Label):
            if 'valor' in widget.winfo_name():
                widget.config(bg=paleta['valor_bg'], fg=paleta['valor_fg'])
            else:
                widget.config(bg=paleta['etiqueta_bg'], fg=paleta['texto_etiquetas_fg'])


def alternar_modo():
    global modo_noche
    if var.get() == 1:
        modo_noche = True
        aplicar_paleta(paleta_noche)
    else:
        modo_noche = False
        aplicar_paleta(paleta_dia)

def on_entry_click(event):
    if entrada_simbolo.get()== "Ingrese simbolo del stock":
        entrada_simbolo.delete(0, tk.END)
        entrada_simbolo.config(fg=paleta_dia['texto_etiquetas_fg'] if not modo_noche else paleta_noche['texto_etiquetas_fg'])

#funcion para exttraer datos
def obtener_info():
    simbolo = entrada_simbolo.get()
    url = 'https://finance.yahoo.com/quote/'+simbolo
    if simbolo == "Ingrese simbolo del stock" or not simbolo:
        messagebox.showwarning("Error", "Ingrese un simbolo de stock")
        return

    url = 'https://finance.yahoo.com/quote/' + simbolo
    encabezados = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'}


    try:
        html = requests.get(url, headers= encabezados)




        #crear sopa
        soup = BeautifulSoup(html.content, 'lxml')

        # Extraer el elemento con el atributo data-testid específico
        info_encabezado = soup.find(attrs={"data-testid": "quote-hdr"})
        titulo_simbolo = info_encabezado.find('h1').text
        precio_actual = info_encabezado.find('span', attrs={"data-testid": "qsp-price"}).text

        #limpiar frame anterior 
        for widget in frame_interior.winfo_children():
            widget.destroy()

        #mostrar encabezado con nombre y precio de stock 
        color_texto = paleta_dia['texto_etiquetas_fg'] if not modo_noche else paleta_noche['texto_etiquetas_fg']
        color_encabezado = paleta_dia['etiqueta_bg'] if not modo_noche else paleta_noche['etiqueta_bg']
        encabezado = f"{titulo_simbolo} - {precio_actual}"
        encabezado_etiqueta = tk.Label(frame_interior, text=encabezado, font=('Arial',16, 'bold'), bg =color_encabezado, fg=color_texto)
        encabezado_etiqueta.grid(row=0, column=0, columnspan=4, pady=10, sticky='n')

            
        #extraer tabla
        tablas = soup.find('ul', class_='yf-gn3zu3').find_all('li')

        for indice_li, li in enumerate(tablas):
            nombre = li.find_all('span')[0].get_text()
            valor = li.find_all('span')[1].get_text()
            fila = (indice_li//2) + 1
            columna = indice_li % 2
            agregar_a_tabla(nombre, valor, fila, columna)


    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error al obtener la informacion del stock : {e}")

#funcion para agregar registros 
def agregar_a_tabla(nombre, valor, fila, columna):
    color_etiqueta = paleta_dia['etiqueta_bg'] if not modo_noche else paleta_noche ['etiqueta_bg']
    color_valor = paleta_dia['valor_bg'] if not modo_noche else paleta_noche ['valor_bg']
    color_valor_texto = paleta_dia['valor_fg'] if not modo_noche else paleta_noche ['valor_fg']
    color_textos = paleta_dia['texto_etiquetas_fg'] if not modo_noche else paleta_noche['texto_etiquetas_fg']

    etiqueta_widget=tk.Label(frame_interior, text=f"{nombre}", font=('Arial', 10), anchor='w', name=f'etiqueta_{fila}_{columna}', bg=color_etiqueta, fg=color_textos) 
    etiqueta_widget.grid(row=fila, column=columna * 2, sticky='w', padx=10, pady=2)

    valor_widget=tk.Label(frame_interior, text=f"{valor}", font=('Arial', 10), anchor='w', name=f'valor_{fila}_{columna}', bg=color_valor, fg=color_valor_texto)
    valor_widget.grid(row=fila, column=columna * 2 + 1, sticky ='w', padx=10, pady=2)

#caja de texto para ingresar simbolo
entrada_simbolo = tk.Entry(ventana, width=20, font=('Arial', 14), fg= 'grey')
entrada_simbolo.insert(0, 'Ingrese simbolo del stock')
entrada_simbolo.bind('<FocusIn>', on_entry_click)
entrada_simbolo.pack(pady=20)

#boton para obtener info
boton_info = tk.Button(ventana, text='Buscar', width=20, font=('Arial', 14), relief='flat', command=obtener_info)
boton_info.pack(pady=3)

#variable para manejar checkbutton
var = tk.IntVar()

#checkbutton para activar modo noche 
check = tk.Checkbutton(ventana, text='Modo Noche', variable=var, onvalue=1, offvalue=0, command=alternar_modo)
check.place(relx=0.9, rely=0.05, anchor='ne')


#frame para resultadosh
frame_interior = tk.Frame(ventana)
frame_interior.pack(fill='both', padx=10, pady=10, expand=True)

frame_interior.grid_columnconfigure(0, weight=1)
frame_interior.grid_columnconfigure(1, weight=1)
frame_interior.grid_columnconfigure(2, weight=1)
frame_interior.grid_columnconfigure(3, weight=1)

#iniciar con paleta dia 
aplicar_paleta(paleta_dia)

#loop principal de la ventana 
ventana.mainloop()
