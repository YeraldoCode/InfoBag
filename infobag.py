import requests
from bs4 import BeautifulSoup
import tkinter as tk 
from tkinter import messagebox

ventana = tk.Tk()
ventana.geometry('900x400')
ventana.title('InfoBag by Yera')

def on_entry_click(event):
    if entrada_simbolo.get()== "Ingrese simbolo del stock":
        entrada_simbolo.delete(0, tk.END)
        entrada_simbolo.config(fg='#000000')

#funcion para exttraer datos
def obtener_info():
    simbolo = entrada_simbolo.get()
    url = 'https://finance.yahoo.com/quote/'+simbolo
    if simbolo == "Ingrese simbolo del stock" or not simbolo:
        messagebox.showwarning("Error", "Ingrese un simbolo de stock")
        return

    url = 'https://finance.yahoo.com/quote/' + simbolo
    encabezados = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'}
    html = requests.get(url, headers= encabezados)

    #crear sopa
    soup = BeautifulSoup(html.content, 'lxml')

    # Extraer el elemento con el atributo data-testid específico
    info_encabezado = soup.find(attrs={"data-testid": "quote-hdr"})
    titulo_simbolo = info_encabezado.find('h1')
    precio_actual = info_encabezado.find('span', attrs={"data-testid": "qsp-price"})

    #extraer tabla
    tablas = soup.find('ul', class_='yf-gn3zu3').find_all('li')

    for li in tablas:
        nombre = li.find_all('span')[0].get_text()
        valor = li.find_all('span')[1].get_text()
        print(nombre + '- '+ valor)


#caja de texto para ingresar simbolo
entrada_simbolo = tk.Entry(ventana, width=20, font=('Arial', 14), fg= 'grey')
entrada_simbolo.insert(0, 'Ingrese simbolo del stock')
entrada_simbolo.bind('<FocusIn>', on_entry_click)
entrada_simbolo.pack(pady=20)

#boton para obtener info
boton_info = tk.Button(ventana, text='Buscar', width=20, font=('Arial', 14), relief='flat', command=obtener_info)
boton_info.pack(pady=3)


#frame para resultadosh
frame_interior = tk.Frame(ventana)
frame_interior.pack(fill='both', padx=10, pady=10, expand=True)

frame_interior.grid_columnconfigure(0, weight=1)
frame_interior.grid_columnconfigure(1, weight=1)
frame_interior.grid_columnconfigure(2, weight=1)
frame_interior.grid_columnconfigure(3, weight=1)



#loop principal de la ventana 
ventana.mainloop()
