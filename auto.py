import os
import MesaApp as mesa

AutoPath=''
m=mesa
    
def autoseleccion():
    global AutoPath
    global m
    m.inicializar()
    
    with open('config.txt') as config:
        c = config.readlines()
        AutoPath=c[3].strip("\n")

    listdir=os.listdir(AutoPath)

    for ListaDescarga in listdir:
        path=AutoPath+'/'+ListaDescarga
        if os.path.isfile(path):
            m.seleccionAuto(path)

autoseleccion()
