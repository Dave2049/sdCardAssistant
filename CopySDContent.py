
'''
Created on 30.05.2017
TODO: create Folder per day nicht den Ordner nach erstellungsDatum pruefen sondern einzelne Bilder.nochmal nach exists uberproefen. Pruefen ob auf SD karte und in Ordnern gleich viele Bilder. 
@author: David

'''
import os
import time
from _datetime import datetime
import shutil
import pathlib
from pathlib import PurePath
from copy import copy
from _tracemalloc import start

fotoDestination = 'Default'

    
def getFotoDestination(creationDate):
    if(creationDate.weekday() == 4):
        fotoDestination = 'Choosen'
    else:
        fotoDestination = 'Default'
    return fotoDestination
    
    
def createFolderByDate(folder, dest, author, typeV,cardPath,hddPath):
    folderPath = cardPath.joinpath(folder);
    dateStamp = datetime.fromtimestamp(os.path.getmtime(str(folderPath)))
    creationYear = dateStamp.strftime('%Y')
    convertetCreationDate = dateStamp.strftime('%Y-%m-%d')
    extDiskPath = hddPath
    
    secFolder = typeV;
    
    if(author):
        firstPath = PurePath(extDiskPath).joinpath(author).joinpath(secFolder)
    else:
        firstPath = PurePath(extDiskPath).joinpath(secFolder)
    
    if(dest.__eq__('Default')):
            newPhotoFolderPath = firstPath.joinpath(creationYear).joinpath(convertetCreationDate)
    else:
            newPhotoFolderPath = firstPath.joinpath(dest).joinpath(creationYear).joinpath(convertetCreationDate)
        
    if not os.path.isdir(str(newPhotoFolderPath)):
            os.makedirs(str(newPhotoFolderPath))
    return newPhotoFolderPath                

def getFileType(photo):
    if(".RAF" in photo or ".JPG" in photo):
        return "Fotos"
    else:
        return "Video"

def getIndexOfType(typeM,folderList):
    for folder in folderList:
        if(typeM in str(folder)):
            return folderList.index(folder)

def containsMOV(photoList):
    for foto in photoList:
        if("Video" in getFileType(foto)):
            return True
    return False

def containsPIC(photoList):
    for foto in photoList:
        if("Fotos" in getFileType(foto)):
            return True
    return False


def organizeFolderList(folder,dest,author,photoList,folderList,cardPath,hddPath):   
     folderNewPic = PurePath(createFolderByDate(folder, dest,author,"Fotos",cardPath,hddPath))
     folderNewMOV = PurePath(createFolderByDate(folder, dest,author,"Video",cardPath,hddPath))        
     if(containsPIC(photoList) and folderNewPic not in folderList):
        folderList.append(folderNewPic)
     if(containsMOV(photoList) and folderNewMOV not in folderList):
        folderList.append(folderNewMOV)
     return folderList


def copyPictures(cardPathString,hddPathString):
    cardPath = PurePath(cardPathString)
    print(cardPathString)
    hddPath= PurePath(hddPathString)
    photoFolders = os.listdir(cardPathString)
    startI = time.time()
    folderList = []
    copyCount = 0
    completeFotoCount = getPhotoCount(photoFolders,cardPath)
    author = ""
    finalFotoList=[]
    mediaArt =""

    
    for folder in photoFolders:
        photoList = os.listdir(str(cardPath.joinpath(folder)))
        lastPhoto = pathlib.Path(cardPath.joinpath(folder).joinpath(photoList[-1]))
        dest = getFotoDestination(datetime.fromtimestamp(lastPhoto.stat().st_mtime))   
        folderList = organizeFolderList(folder,dest,author,photoList,folderList,cardPath,hddPath)
        for photo in photoList:
            curPhoto = pathlib.Path(cardPath.joinpath(folder).joinpath(photo))
            newDest = getFotoDestination(datetime.fromtimestamp(curPhoto.stat().st_mtime))
            if(newDest is not dest):
                folderList = organizeFolderList(folder, newDest, author, photoList, folderList, cardPath, hddPath)
                dest = newDest
            if(getFileType(photo).__eq__("Fotos")):
                mediaArt="Fotos"
                if("Video" in str(folderList[-1])):
                    folderList.insert(-3, folderList[-1])
                    folderList.pop(-1)
            elif("Fotos" in str(folderList[-1])):
                mediaArt="Video" 
                index = getIndexOfType('Video',folderList)
                folderList.insert(-3, folderList[-1])
                folderList.pop(-1)
                
            cPhotoPath = pathlib.Path(cardPath.joinpath(folder).joinpath(photo))
            creationDateStamp = cPhotoPath.stat().st_mtime
            
            if(not checkPhotoDay(creationDateStamp, folderList[-1])):
                folderNEW = PurePath(createFolderByPhotoDate(creationDateStamp,author,dest,mediaArt,hddPath))
                photoPath = folderNEW.joinpath(photo)
                if(os.path.isfile(str(photoPath))):
                    continue
                folderList.append(folderNEW)
                datetime.fromtimestamp(creationDateStamp)
            else:
                folderNEW = ""
            photoPath = folderList[-1].joinpath(photo)
            if(not os.path.isfile(str(photoPath))):
                shutil.copy(str(cardPath.joinpath(folder).joinpath(photo)), str(folderList[-1]))
                copyCount += 1
                if(folderNEW not in finalFotoList):
                    finalFotoList.append(folderNEW)
    reportData = {"ordnerListe":finalFotoList , "fotoAnzahl": copyCount}
    return reportData
     

def getPhotoCount(photoFolder, cardPath):
    count = 0
    for folder in photoFolder:
        photoList = os.listdir(str(cardPath.joinpath(folder)))
        count += len(photoList)
    return count

def checkPhotoDay(creationDateStamp, folder):
    oldFolder = PurePath(folder).name
    creationDate = datetime.fromtimestamp(creationDateStamp).strftime('%Y-%m-%d')
    if(str(creationDate).__eq__(oldFolder)):
        return True
    return False


def createFolderByPhotoDate(creationDateStamp, author,dest, art, hddPath):
    creationDate = datetime.fromtimestamp(creationDateStamp).strftime('%Y-%m-%d')
    creationYear = datetime.fromtimestamp(creationDateStamp).strftime('%Y')
    extDiskPath = hddPath
    secFolder = art
    if(author):
        firstPath = PurePath(extDiskPath).joinpath(author).joinpath(secFolder)
    else:
        firstPath = PurePath(extDiskPath).joinpath(secFolder)
        if(dest.__eq__('Default')):
            newPhotoFolderPath = firstPath.joinpath(creationYear).joinpath(creationDate)
        else:
            newPhotoFolderPath = firstPath.joinpath(dest).joinpath(creationYear).joinpath(creationDate)
   
    if not os.path.isdir(str(newPhotoFolderPath)):
        os.makedirs(str(newPhotoFolderPath))
    return newPhotoFolderPath

