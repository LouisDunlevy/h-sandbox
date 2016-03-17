#RENAMER 

import re

def rename(kwargs):
    print "running"
    node = kwargs['node']
    selectedNodes = hou.selectedNodes()
    src = node.evalParm('src')
    dest = node.evalParm('dest')
    for n in selectedNodes:
        print n
        name = n.name()
        if src in name :
            newname = re.sub(src,dest,name)
            print "name is :" + name
            print "new name :" + re.sub(src,dest,name)
            #n.setName(name.replace(src,dest))
            #n.setName(re.sub(src,dest,name))
            n.setName(newname)



#CREATE A PRIMITIVE GROUP FOR EACH POLYGON ON A GEOMETRY

node = hou.pwd()
geo = node.geometry()
for primm in geo.iterPrims():
   grpName = geo.createPrimGroup('Gurupu_' + str(primm.number()))
   grpName.add(primm)
#CHANGE A CERTAIN PARAMETER IN ALL MANTRA NODES

# change a certain parameter in all Mantra nodes
parent = hou.node("/obj/ROPSr node in parent.children():
   node_type_name = node.type().name()
   if node_type_name == 'mantra':
      # Get the value of a parameter and store it in a variable
      param = node.parm("matte_objects    # set the value of the parameter to a different value
      param.set("enduranceer")
 

There are times when you want to perform an operation on nodes whose names contain a particular pattern. In this case, all nodes with ‘thrusterA’ in their names are acted upon.

#Change the forced matte parameter of node with 'thrusterA' pattern to 'endurance_render'

parent = hou.node("/obj/ROPString = 'thrusterA'
temp = 'endurance_render'
for child in parent.children():
   if sstring in child.name():
      param = child.parm("matte_objects    if param is None:
         pass
      else: 
         print searchStr
         print replStr
         param.set(temp)
#THIS TWO PART CODE ALLOWS YOU TO COPY BUNDLES FROM ONE HOUDINI SCENE TO THE OTHER

# write bundle names, filter and pattern to file
import hou
namedumpfile = '/u/toa/Desktop/b_name.txt'
patterndumpfile = '/u/toa/Desktop/b_pattern.txt'
filterdumpfile = '/u/toa/Desktop/b_filter.txt'
a = file(namedumpfile, 'w')
b = file(patterndumpfile, 'w')
c = file(filterdumpfile, 'w')

# write bundle names, filter and pattern
for bdl in hou.nodeBundles():
   a.write(str(bdl.name()))
   a.write("\n")
   a.close

   b.write(str(bdl.pattern()))
   b.write("\n")
   b.close

   c.write(str(bdl.filter()))
   c.write("\n")
   c.close
# Read bundle names, filter and pattern from file

namedumpfile = '/u/toa/Desktop/b_name.txt'
patterndumpfile = '/u/toa/Desktop/b_pattern.txt'
filterdumpfile = '/u/toa/Desktop/b_filter.txt'
import hou
a = file(namedumpfile, 'r')
b = file(patterndumpfile, 'r')
c = file(filterdumpfile, 'r')
global need
for lin in b:
   for line in a:
     need = hou.addNodeBundle(line.rstrip())
     need.setPattern(lin.rstrip())
     break
#REPLACE A SUBSET OF STRINGS IN A SPECIFIC PARAMETER

'''
matchStr is the value to be replaced and replaceStr is the replacement
make sure the nodes you want to change are selected
'''

def forceObjects():

   for node in hou.selectedNodes():
      param = node.parm("forceobject    searchStr = param.evalAsString()
 
      matchStr = "thrusterDelayedBB"
      replaceStr = "thrusterDelayedBC"

      #Change the values here
      if matchStr in searchStr:
         replStr = searchStr.replace(matchStr,replaceStr)
         #Replace the string
         param.set(replStr)


def forceLights():

   for node in hou.selectedNodes():
      param = node.parm("forcelights    searchStr = param.evalAsString()

      #Change the values here
      matchStr = "thrusterDelayedCA"
      replaceStr = "thrusterDelayedBA"

      if matchStr in searchStr:
         replStr = searchStr.replace(matchStr,replaceStr)
         #Replace the string
         param.set(replStr)


forceObjects()
forceLights()
When it comes to batch/distributed rendering on the render farm, there are times when I want full control over the individual jobs just so I can easily delete/troubleshoot a job that stalls on the render farm. The following code allows me the control of sending each job as individual render tasks to the render farm rather than sending multiple jobs as a single render task.

#RENAME ALL SELECTED ‘ALFHOU’ NODES TO THE NAME OF THEIR ANCESTORS PREFIXED WITH ALFHOU

import hou
for node in hou.selectedNodes():
   ans = node.inputAncestors()
   suff = ans[0].name()
   node.setName("alfhou_" + str(suff))
#APPEND AN ALFOU NODE TO THE SELECTED NODES AND RENAME THEM SUFFIXED WITH ITS ANCESTORS NAME

import hou
parent = hou.node("/obj/ROPSr node in hou.selectedNodes():
    alfu = parent.createNode("alfhou")
    alfu.setFirstInput(node)
    alfu.moveToGoodPosition()
    ans = alfu.inputAncestors()
    suffix = ans[0].name()
    alfu.setName("alfhou_" + str(suffix))
#REPLACE A CHARACTER IN ALL SELECTED NODE NAMES

import hou
for node in hou.selectedNodes():
   name = node.name()
   str = "D"
   rep = "A"
   if str in name:
     newN = name.replace(str,rep)
     node.setName(newN)
#WRITE A SET OF NODES TO DISK AS CODE

import hou
dumpfile='/u/toa/Desktop/nodeAsCode.txt'
a = file(dumpfile,'w')
for node in hou.selectedNodes():
   acode = node.asCode()
   a.write(acode)
   a.close
It is quite easy to do channel referencing in Houdini but that does not work when you want to copy and paste ramp parameter values. The following code allows you to do that and saves you a bit more time so you can get your work into dailies faster!

#COPY RAMP PARAMETERS

import hou

#Change path to source and destination nodes here
sourceNode = hou.node("/obj/Rnd/color1stNode = hou.node("/obj/Rnd/color2urceParm = sourceNode.parm("rampstParm = destNode.parm("rampdedestParm.set(sourceParm.eval())
