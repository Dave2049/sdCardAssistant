#!/usr/bin/python3
import os
from pathlib import PurePath
import sys

def getRcLocalContent():
    file = open('/etc/rc.local','r')
    lines = file.readlines()
    file.close()
    return lines
    
def getScriptLine(content):
    for line in content:
        if ('python3 /home/pi/git-repos/sdCardAssistant/init.py &' in line):
            return content.index(line)

def getNewContent(index, content):
    if('#' in content[index]):
        content[index] = 'python3 /home/pi/git-repos/sdCardAssistant/init.py &\n'
        print('script activated')
    else:
        content[index] = '# python3 /home/pi/git-repos/sdCardAssistant/init.py &\n'
        print('script deactivated')
    return content

def writeNewContent(newContent):
    file = open('/etc/rc.local','w')
    file.writelines(newContent)
    print('stateChanged')
    file.close()

def main():
    content = getRcLocalContent()
    scriptIndex = getScriptLine(content)
    newContent = getNewContent(int(scriptIndex),content)
    writeNewContent(newContent)

main()
