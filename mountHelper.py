import os
import subprocess

def getUUIDs():
        devices=os.popen("blkid").readlines()
        uuiDList= []
        for device in devices:
                for attribute in device.split(" "):
                        if("UUID" in attribute and "P" not in attribute):
                              uuidS=attribute.split("=\"")[1]
                              uuid= ''.join( c for c in uuidS if c not in "\"")
                              uuiDList.append(uuid)
        return uuiDList

def matchUUIdAndMP():
        UUIDS = getUUIDs()
        mount = {}
        for uuid in UUIDS:
                if(uuid == "726021E86021B42F"):
                        mount.update({uuid: "/home/pi/mnt/usb"})
                elif(uuid == "94BA-0FFE"):
                        mount.update({uuid: "/home/pi/mnt/sdCard"})
                elif(uuid == "C224-7ACC"):
                        mount.update({uuid: "/home/pi/mnt/sdCard2"})
        return mount


        
def umountALL():
        mounts = matchUUIdAndMP()
        for uuid in mounts:
                os.system("umount UUID=\""+uuid+"\"")
        print("umountComplete")
        
def mount(uuid):
        mounts = matchUUIdAndMP()
        os.system("mount UUID=\""+uuid+"\""+" "+mount[uuid])

def umount(uuid):
        os.system("umount UUID=\""+uuid+"\"")
   
def mountALL():
        mounts = matchUUIdAndMP()
        for uuid in mounts:
                os.system("mount UUID=\""+uuid+"\""+" "+mounts[uuid])
