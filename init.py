#!/usr/bin/python3

import time
import os
import controllNr
import emailHelper
import CopySDContent
import datetime

hddPath='/media/pi/Seagate Expansion Drive'
sdCard1='/media/pi/94BA-0FFE/DCIM'
sdCard2='/media/pi/C224-7ACC/DCIM'
controlNrFile=hddPath+'/ConfQuatsch/controllNr'


def secLoop():
    socketError=False
    lastCheck = time.time()/60
    try:
        emailHelper.sendMail('scriptStarted', 'TEST')
    except Exception:
        socketError=True
    cardPathList = []
    pause = 0
    cardPathList.append(sdCard1)
    cardPathList.append(sdCard2)    
    while True:
        sdCards = getSDcardCount(cardPathList)
        if(os.path.isdir(hddPath)):           
            for cards in sdCards:
                print(cards)
                if(os.path.isfile(controlNrFile)):                 
                    controlNr = str(controllNr.generateControlNR(cards))
                    print(controlNr)
                    if(controlNr not in getControllNrFromHDD()):
                        print("__")
                        print("new CR found")
                        reportData = CopySDContent.copyPictures(cards,hddPath)
                        if(not socketError):
                            try:
                                generateMail(reportData['ordnerListe'],reportData['fotoAnzahl'])
                            except Exception:
                                socketError=True
                        controllNr.writeNewControlNR(controlNr,controlNrFile)
        pause=+30
        timeNow = time.time()/60
        if(timeNow-lastCheck>5&socketError):
            lastCheck=time.time()
            socketError = checkSocketError()
        time.sleep(30)

def checkSocketError():
    try:
        emailHelper.sendMail('Socket Test', 'TEST')
    except Exception:
        return True
    return False

def getSDcardCount(cardPathList):
    activeCards=[]
    for cards in cardPathList:
        if os.path.isdir(cards):
            activeCards.append(cards)
    return activeCards

def getControllNrFromHDD():
    file = open(controlNrFile,'r')
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
