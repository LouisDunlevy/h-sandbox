import os
import sys
import re
import subprocess

def readNukeFile(node):

    nukeFile = node.evalParm("readNukeFile")

    if not os.path.exists(nukeFile):
        
        return ""
    
    lines = open(nukeFile,"r").readlines()

    return "".join(lines)


def getWriteNodes(node):

    writeNodes = []
    comp = re.compile("^Write \{.*?\}",re.MULTILINE|re.DOTALL)

    for result in comp.findall(readNukeFile(node)):

        for line in result.split("\n"):
            
            if line.split()[0] == "name":

                writeNodes.append(line.split()[1])
                writeNodes.append(line.split()[1])

    return writeNodes


def getParseReadNodes(node):

    comp = re.compile("^Read \{.*?\}",re.MULTILINE|re.DOTALL)
    readNodes = []

    for result in comp.findall(readNukeFile(node)):

        name = ""
        path = ""

        for line in result.split("\n"):
            
            splitline = line.split()

            if splitline[0] == "name":

                name = line.split()[1]

            elif splitline[0] == "file":
                
                path = line.split()[1]

        readNodes.append((name,path))

    node.parm("nukeReadFolder").set(0)
    node.parm("nukeReadFolder").set(len(readNodes))

    for idx,readTuple in enumerate(readNodes):

        node.parm("readNodeName%d" % (idx+1)).set(readTuple[0])
        node.parm("readNodeFile%d" % (idx+1)).set(readTuple[1])


def createWriteFile(node):

    lines = readNukeFile(node)
    num = node.evalParm("nukeReadFolder")
    for idx in range(1,num+1):

        name = node.evalParm("readNodeName%d" % (idx))
        path = node.evalParm("readNodeFile%d" % (idx))

        for found in re.findall('^Read \{(.*?name.*?)\}', lines, re.MULTILINE|re.DOTALL):
            
            if name in found:

                new = re.sub("file .*\n","file %s\n" % (path),found,re.MULTILINE|re.DOTALL)
                lines = lines.replace(found,new)
        
                if found in lines:
    
                    lines = re.sub(found,new,lines,re.MULTILINE|re.DOTALL)

    writeNodeIdx = int(node.evalParm("writeNode"))
    writeNode = getWriteNodes(node)[writeNodeIdx *2]
    writeImagePath = node.evalParm("writeImagePath")
    result =re.search("^Write \{(.*?name %s.*?)\}"%(writeNode),lines,re.MULTILINE|re.DOTALL)
        
    if result:

        orginal = result.group(1)
        new = re.sub("file .*\n","file %s\n" % (writeImagePath),result.group(1),re.MULTILINE|re.DOTALL)
        lines = re.sub(orginal,new,lines,re.MULTILINE|re.DOTALL)

    filePath = node.evalParm("writeNukeFile")
    nkfile = open(filePath,"w")
    nkfile.write(lines)
    nkfile.close()

def getSelectedWriteNode(node):

    writeNodeIdx = int(node.evalParm("writeNode"))
    return getWriteNodes(node)[writeNodeIdx *2]


def doLocalRender(node):

    createWriteFile(node)
    start,end,step = node.parmTuple("f").eval()
    filePath = node.evalParm("writeNukeFile")
    writeNode = getSelectedWriteNode(node)
    cmd = "nukePy nukeRender.py --framerange %d %d %d --node %s --scene %s" % (start,end,step,writeNode,filePath)
    process = subprocess.Popen(cmd.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
    while True:

        out = process.stdout.read(1)

        if out == '' and process.poll() != None:

            break

        if out != '':

            sys.stdout.write(out)
            sys.stdout.flush()

    return int(process.returncode)
    



