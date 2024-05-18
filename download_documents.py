import os
import errno
import controller
from colorama import init, Fore
transportDocument= ""
init()
def setTransportDocument( transportDocumentID):
    global transportDocument
    transportDocument= transportDocumentID
    return
 
def createDirectory(silent):
    if silent==False:print("*** Creando carpeta ***")
    try:
        global transportDocument
        path=transportDocument.strip("F.txt")
        os.mkdir(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    if silent==False:print(Fore.GREEN+"*** Carpeta Creada Con Exito ***")

def getDownloadables(silent):
    if silent==False:print(Fore.YELLOW+"obtiene la lista de archivos de onedrive y compara con la lista\n"+"de facturas del documento de transporte \n")
    with open(transportDocument) as associatedDocuments:
        controller.folderInfo()
        for line in associatedDocuments:
            if(line != "\n"):
                if silent==False:print(Fore.YELLOW+"obteniendo soporte: "+line)
                downloadInvoice(line.strip('\n'),transportDocument.strip("F.txt"),silent)
    if silent==False:print(Fore.GREEN+"\n*** Proceso Finalizado ***\n")

def downloadInvoice(fileName,path,silent):
    controller.downloadInvoice(fileName,path,silent)
                
def Execute(transportDocumentID,silent):
    setTransportDocument(transportDocumentID)
    createDirectory(silent)
    getDownloadables(silent) 
        