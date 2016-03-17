
import fnmatch

def keyFolder(node,folderList):
    """ For any parameter that is in the given folder
        set a key
    """
    for parm in node.parmsInFolder(folderList):
        if parm.isAutoscoped():
            try:
                val = parm.eval()
                key = hou.Keyframe()
                key.setValue(val)
                parm.setKeyframe(key)
                #key.setFrame(hou.frame()) #not necessary
            # Catch exception if the parameter cannot be changed.
            except hou.PermissionError:
                continue
                
def deleteAllKeyframes(node,folderList):
    """ For any parameter that is in the given folder :
        delete all channels
    """
    for parm in node.parmsInFolder(folderList):
        if parm.isAutoscoped():
            try:
                parm.deleteAllKeyframes()
            # Catch exception if the parameter cannot be changed.
            except hou.PermissionError:
                continue

def revertAllParms(node,folderList):
    """ For any parameter that is in the given folder :
        revert to defaults
    """
    for parm in node.parmsInFolder(folderList):
        if parm.isAutoscoped():
            try:
                parm.revertToDefaults()
            # Catch exception if the parameter cannot be changed.
            except hou.PermissionError:
                continue           
 
def deleteKeyframe(node,folderList):
    """ For any parameter that is in the given folder :
        delete all keyframes at this frame
    """
    for parm in node.parmsInFolder(folderList):
        if parm.isAutoscoped():
            try:
                parm.deleteKeyframeAtFrame(hou.frame())
            # Catch exception if the parameter cannot be changed.
            except:
                pass

def matchFKToIK(rignode,thighBone,shinBone):

    # Bones.
    thigh = rignode.node(thighBone)
    shin = rignode.node(shinBone)
    
    # FK Controls.
    fkthigh = thigh 
    fkshin = shin
    
    # Match the thigh rotations.
    xform = (thigh.worldTransform() \
             * fkthigh.worldTransform().inverted() \
             * fkthigh.parmTransform()).extractRotates(rotate_order='zyx')

    for parm, val in zip(fkthigh.parmTuple('r'), xform):
        parm.getReferencedParm().set(val)

    # Match the shin rotations.
    xform = (shin.worldTransform() \
             * fkshin.worldTransform().inverted() \
             * fkshin.parmTransform()).extractRotates(rotate_order='zyx')

    for parm, val in zip(fkshin.parmTuple('r'), xform):
        parm.getReferencedParm().set(val)
                        
                

def buildLegParms(kwargs):
    node = kwargs['node']
    type = node.type()
    definition = type.definition()
    path = definition.libraryFilePath()
    print path
    
    legBones = []
    for c in node.children():
            if fnmatch.fnmatch(c.name(), "*L_leg_C*") and c.type().name() == "bone":
                print c
                t = c.parmTuple("r")
                template = t.parmTemplate()
                template.setName(c.name() + "_r")
                template.setLabel(c.name() + "_r")
                legBones.append(c)
    
    #legBones.sort() #not good, use sort by arg func instead if in doubt
    
    for leg in legBones:
        print leg.type().name()
        parm = leg.parmTuple("r")
        template = parm.parmTemplate()
        template.setName(leg.name() + "_r")
        template.setLabel(leg.name() + "_r")
        print template
        definition.addParmTuple(template,in_folder=("Animation",))
        #try :
        #    definition.addParmTuple(template,in_folder=("Animation",))
        #except :    
        #    pass

        # definition is NOT written to disk 'cos we're not that brave
        
        
        # extract base name for each bone chain with some splitting
        #path=hou.pwd().parm("elem_subdir").eval()
        #newpath = "/".join(path.split("/")[6:8])
        #return newpath
