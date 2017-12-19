#!/usr/bin/python3
import os
import pathlib

def generateControlNR(sdCardpathSTR):
    sdCardpath = pathlib.PurePath(sdCardpathSTR)
    if(os.path.isdir(str(sdCardpath))): 
        FolderList = os.listdir(str(sdCardpath))
        imgList= []
        controllNr = 0;
        for folder in FolderList:
            for obj in os.listdir(str(sdCardpath)+"/"+folder) :
                print(folder+":"+obj)
                img = obj.split("DSCF")[1]
                imgList.append(img.split('.')[0]);
        for name in imgList:
            controllNr=controllNr+int(name)
        controllNr = controllNr+len(imgList)
        return controllNr
       
def writeNewControlNR(controlNr,controlNrFile):
    if(os.path.isfile(controlNrFile)):
        file = open(controlNrFile,'r')
        lines = file.readlines()
        file.close
        file = open(controlNrFile,'w')
        if(int(len(lines)) != 0):
            lines.pop(0)
        file.writelines(lines)
        file.close()
        file = open(controlNrFile,'a')
        file.write(str(controlNr)+'\n')
        file.close
