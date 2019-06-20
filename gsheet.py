from googleapiclient import discovery, http
import httplib2
import io

from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import datastore
import os
import gspread

#### pip install gspread oauth2client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "CloudComputing3-78db45442167.json"
datastore_client = datastore.Client()

def addObject(data):
    key = datastore_client.key('Catalog')

    object = datastore.Entity(
        key, exclude_from_indexes=tuple('Description')
    )

    object.update({
        'Type' : data[0],
        'Description' : data[1]
    })
    datastore_client.put(object)

    return object.key

def list_tasks():
    query = datastore_client.query()
    return list(query.fetch())


def insertData(data):
    doc = client.open('T3Spreadsheet')
    sheet = doc.sheet1
    sheet.append_row(data)



def exportExcel():
    def downloadExcel():
        file_id = '1ZIqt_5MoZtUZSXYxOvItJfNjeanIZ012nbrVLb8sxog'
        drive_service = discovery.build('drive', 'v3', http=credentials.authorize(httplib2.Http()))
        request = drive_service.files().export_media(fileId=file_id,
                                                     mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        fh = io.BytesIO()
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(
                "Download %d%%." % int(status.progress() * 100))

        path = os.path.join(os.path.dirname(__file__),'Catalog.xlsx')
        with io.open(path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
    query = datastore_client.query()
    items = list(query.fetch())
    doc = client.open("T3Spreadsheet")
    sheet = doc.sheet1
    for item in items:
        sheet.append_row(list(item.values()))

    downloadExcel()
    sheet.clear()

def addObjects_Message(msg,msg_translated):
#    sheet.clear()
    for m1 in range(0,len(msg)) :
        obj1=list()
        obj1.append(msg[m1])
        obj1.append(msg_translated[m1])
        addObject((obj1))

obj1=list()
obj1.append('Message')
obj1.append('Translated messagee')
addObject(obj1)
#print(obj1[1])
obj2 = list_tasks()[1]
#print(list(obj1.values()))
exportExcel()
