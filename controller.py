import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
from colorama import init, Fore

APP_ID = '1480548c-60f2-40bc-8b34-de8be48a1422'
SCOPES = ['Files.Read']
init()
access_token = generate_access_token(APP_ID, scopes=SCOPES)
headers = {
	'Authorization': 'Bearer ' + access_token['access_token']
}

drive_id= ''
folder_id = ''
invoiceList = None

def empezar(silent):
    global drive_id
    global folder_id
    with open('config.txt') as config:
        c = config.readlines()
        drive_id=c[0].strip("\n")
        folder_id=c[1].strip("\n")
    if not silent: print(Fore.GREEN+"Lectura de configuracion exitosa!")
            


###Lista de facturas en Onedrive
def  folderInfo():
    response_folder_info =requests.get(
        GRAPH_API_ENDPOINT + f'/drives/{drive_id}/items/{folder_id}/children',#list folder
        headers=headers,
        params={'select': 'id,name'}
    )
    #print(response_folder_info.json())
    global invoiceList
    invoiceList=response_folder_info.json().get('value')
    

def downloadInvoice(fileName,path,silent):
    global invoiceList
    counter=0
    if invoiceList is None:
        print("")
    else:
        for file in invoiceList:
            if(fileName in file['name']):
                file_id=file['id']
                path+='\\'+file['name'] 
                response_file_content = requests.get(GRAPH_API_ENDPOINT + f'/me/drive/items/{file_id}/content', headers=headers)
                with open(path, 'wb') as _f:
                    _f.write(response_file_content.content)
                    if silent==False:print(Fore.GREEN+"Descargado con exito: "+fileName)
                break
            counter=counter+1
            if counter==len(invoiceList):
                if silent==False:print(Fore.RED+"Archivo no encontrado: "+fileName)
        
            

def  shareInfo():
    response_drive_info =requests.get(
        GRAPH_API_ENDPOINT + f'/me/drive/sharedWithMe',#list folder
        headers=headers,
        params={'select': 'id,name'}
    )
    print(response_drive_info.json()['value'])

def  driveInfo():
    response_drive_info =requests.get(
        GRAPH_API_ENDPOINT + f'/me/drive',#drive info
        headers=headers,
        params={'select': 'id'}
    )
    print(response_drive_info.json()['id'])
    global drive_id
    drive_id=response_drive_info.json()['id']

def  rootFolderInfo():
    response_folder_info =requests.get(
        GRAPH_API_ENDPOINT + f'/me/drive/root/children',#list folder
        headers=headers,
        params={'select': 'id,name'}
    )
    print (response_folder_info.json()['value'])

def getConfigInfo():
    driveInfo()
    rootFolderInfo()
    shareInfo() 