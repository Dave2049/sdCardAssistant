import pyudev

context = pyudev.Context()

def printUUID():
        for devive in context.list_devices(subsystem="block", DEVTYPE="partition"):
                if(device.get(ID_USB_DRIVER) == 'usb-storage'):
                    print '{0} {1}'.format(device.device_node, devive.get('ID_FS_UUID'))
printUUID()
