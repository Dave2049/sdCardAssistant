#!/usr/bin/python3

import time
import os
import controllNr
import emailHelper
import CopySDContent
import datetime

def secLoop():
    emailHelper.sendMail('scriptStarted', 'TEST')
    print('start')
    while True:
        if os.path.isdir('/mnt/usb/Fotos'):           
            if os.path.isdir('/mnt/sdCard/DCIM'):            
                if os.path.isfile('/mnt/usb/ConfQuatsch/controllNr'):                 
                    controlNr = str(controllNr.generateControlNR())
                    if controlNr not in getControllNrFromHDD():
                        emailHelper.sendMail('check succed', 'DEBUG')
                        reportData = CopySDContent.copyPictures()
                        print("EvrythingCopied")
                        generateMail(reportData['ordnerListe'],reportData['fotoAnzahl'])
                        controllNr.writeNewControlNR(controlNr)
                    else:
                        emailHelper.sendMail('Already Copied', 'DEBUG')
                        print("already Copy")
                else:
                    emailHelper.sendMail('Controll NR Not found', 'DEBUG')
                    print("Control NR File npt found")
            else:
                emailHelper.sendMail('NO SD', 'DEBUG')
                print("No SD")
        else:
            emailHelper.sendMail('NO HDD', 'DEBUG')
            print("No HDD")
        time.sleep(10)

def getControllNrFromHDD():
    file = open('/mnt/usb/ConfQuatsch/controllNr','r')
    return file.read()

def getStringsFromFolderList(folderList):
    listString = " "
    for folder in folderList:
        listString+=str(folder)+"--"
    return listString

def generateMail(folderList, fotoCount):
    timeStamp = time.time()
    timerTitel = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:')
    Titel ="SDCard Report "+str(timerTitel)
    Message="Hey David, \ndeine Fotos wurden Kopiert. \nFolgende Ordner wurden verwenden: "+ getStringsFromFolderList(folderList) +".\n"+ str(fotoCount)+" Fotos wurden kopiert."
    emailHelper.sendMail(Titel, Message)     

secLoop()
