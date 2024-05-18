import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import download_documents as Descargador
import controller
from colorama import init, Fore

excelPath= ''
init()
def inicializar():
    global excelPath
    with open('config.txt') as config:
        c = config.readlines()
        excelPath=c[2].strip("\n")
    controller.empezar(True)
    
def seleccion():
    global excelPath
    df = pd.read_excel(excelPath) 
    print(Fore.YELLOW+"Seleccione la lista de documentos a descargar")
    ListaDescarga = askopenfilename(title="Seleccione lista DT") 
    print("Realizando Proceso de comparacion ID vs Nombre...")
    listafiltrada=filtrarLista(ListaDescarga,df,True)
    path=ListaDescarga.strip(".txt")+"F.txt"
    almacenarListaDescargas(path,listafiltrada,False)
    print("Inicia el proceso de descarga...\n")          
    Descargador.Execute(path,False)

def seleccionAuto(ListaDescarga):
    global excelPath
    df = pd.read_excel(excelPath) 
    listafiltrada=filtrarLista(ListaDescarga,df,True)
    path=ListaDescarga.strip(".txt")+"F.txt"
    almacenarListaDescargas(path,listafiltrada,True)       
    Descargador.Execute(path,True)


def filtrarLista(ListaDescarga,df,silent):
    listafiltrada=[]
    #test=df.groupby("Invoice ID").agg({"File name":lambda x: list(x)[0]})
    #print(test)
    with open(ListaDescarga) as descargables:
        for line in descargables:
            invoice_id=line.strip("\n")
            candidato=df[df["Invoice ID"]==invoice_id].groupby("Invoice ID").agg({"File name":lambda x: list(x)[0]})
#            
            if candidato.values.size==0:
                pass
            else:
                name=candidato.values[0][0]
                if not candidato.isnull().values[0][0]:
                    #print(candidato)
                    name=name+"\n"
                    listafiltrada.append(name)
                elif not silent: print(Fore.RED+"Warning: Se encontro un registro para la factura "+ invoice_id +" en la tabla de referencia, pero no tiene un nombre de archivo asiganado. [DESCARGAOMITIDA]")
    return listafiltrada

def almacenarListaDescargas(path,listafiltrada,silent):
    if silent==False:print(Fore.YELLOW+"Almacenando lista de facturas objetivo por nombre de factura...")
    with open(path, "w") as txt_file:
         for line in listafiltrada:
             txt_file.write(''+line) 
             
def mostrar_menu(opciones):
    print(Fore.WHITE+"Seleccione una opción:")
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')



def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a


def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()


def menu_principal():
    inicializar()
    Tk().withdraw()
    controller.empezar(False)
    #"Texto en negrita de color amarillo")
    opciones = {
        '1': ('Descargar Facturas para DT por Seleccion', accion1),
        '2': ('Consultar info de configuracion', accion2),
        '3': ('Validar Configuracion Actual', accion3),
        '4': ('Cambiar excel de ref', accion4),
        '5': ('Configurar Carpeta Auto', accion5),
        '6': ('Salir', salir)
    }

    generar_menu(opciones, '6')


def accion1():
    seleccion()

def accion2():
    print(Fore.CYAN+'Obteniendo informacion del drive del usuario conectado')
    controller.getConfigInfo()

def accion3():
    print(Fore.YELLOW+'Consultando configuracion actual... ')
    with open('config.txt') as config:
        c = config.readlines()
        print(Fore.CYAN+"Drive ID: "+c[0].strip("\n"))
        print("Folder ID: "+c[1].strip("\n"))
        print("Tabla REF: "+c[2].strip("\n"))
        print("Carpeta Auto: "+c[3].strip("\n"))

def accion4():
    print(Fore.YELLOW+'Seleccione la ubicacion del excel')
    newconfig=[]
    with open('config.txt') as config:
        cfg= config.readlines()
        newconfig.append(cfg[0])
        newconfig.append(cfg[1])
            
    ref =askopenfilename(title="Seleccione el libro excel referencia de busqueda")
    newconfig.append(ref)
    with open('config.txt','w') as c:
        for line in newconfig:
            c.write(line)
    print(Fore.GREEN+"*** Se ha configurado a "+ref+ " como la tabla de referencia ***")

def accion5():
    print(Fore.YELLOW+'Seleccione la ubicacion de la carpeta de descargas de automaticas')
    newconfig=[]
    with open('config.txt') as config:
        cfg= config.readlines()
        newconfig.append(cfg[0])
        newconfig.append(cfg[1])
        newconfig.append(cfg[2])
            
    ref =askdirectory(title="Seleccione carpeta para busqueda de automaticos") 
    newconfig.append(ref)
    with open('config.txt','w') as c:
        for line in newconfig:
            c.write(line)
    print(Fore.GREEN+"*** Se ha configurado a "+ref+ " como la carpeta de busqueda automatica ***")
    
    
def salir():
    print('Saliendo') 


if __name__ == '__main__':
    menu_principal()