path=hou.pwd().parm("elem_subdir").eval()
newpath = "/".join(path.split("/")[0:5])
return newpath




def opColor(kwargs):
    inst = kwargs['node']
    read = inst.parm('read').eval()
    inst.setColor( hou.Color((0.75*read,0.5*(1-read),0)) )




def show_cleanup(kwargs):
    node = kwargs['node']
    parms = node.parmsInFolder(("Management","Version Cleanup",)) # FOLDER LAYOUT HAS CHANGED
    if len(parms) <= 1:
       node.parm("cleanuphide").set(True)
    else:
       node.parm("cleanuphide").set(False)


def makeFetch(kwargs):
    ### we don't have a custom fetch node so we make some spare parms and link them
    node = kwargs['node']
    name = node.parm("name").eval()
    
    parentNode = kwargs["parentNode"] if "parentNode" in kwargs else hou.node("/out")
    fetchnode = parentNode.createNode("fetch",name)

    ### start making spare parms and linking
    nodepath_template = fetchnode.parm("source").parmTemplate()
    #change parm name
    nodepath_template.setName("sopnode")
    nodepath_template.setLabel("OUT Geom Node")
    fetchnode.addSpareParmTuple(nodepath_template)
    fetchnode.parm("sopnode").set(node.path())
    ### link source to referenced geom node
    rop_node = node.node("ropnet/geom_out")
    fetchnode.parm("source").set(rop_node.path())

    ### link the version number to a new spare parm, should probably link other useful parms like static etc
    version_template = node.parm("ver").parmTemplate()
    fetchnode.addSpareParmTuple(version_template)
    fetchnode.parm("ver").setExpression("ch("+ "\"" + node.path() + "/ver\")" )

    ### perhaps link all parms in Bake folder
    #sopParmTemplateGroup = node.parmTemplateGroup()
    #fetchnode.setParmTemplateGroup(sopParmTemplateGroup)

    
    # Channel link all the hbatch parms on the fetch back to the SOP.
    for parm in fetchnode.parms():
        parm_name = parm.name()
        if not parm_name.startswith("hbatch_") or not node.parm(parm_name):
            continue
        op = "ch"
        if parm.parmTemplate().type() == hou.parmTemplateType.String:
            op = "chs"
        expression = "%s(\"%s/%s\")" % (op, node.path(), parm_name)
        parm.setExpression(expression)
    
    if kwargs.get("selectNode", True):
        fetchnode.setSelected(True, clear_all_selected=True)

    return fetchnode

# Alias to createFetchNode, which is used by the Global ROP Dependencies ROP
# to create fetch nodes on request.
createFetchNode = makeFetch

def makeBatch(kwargs,fetchnode):
    node = kwargs['node']
    name = node.parm("name").eval()
    batchname = name + "_batch"
    batchnode = fetchnode.createOutputNode("lfl::main::out_batch::2.0",batchname)
    try :
        batchnode.setName(batchname)
    except hou.OperationFailed :
        print "rop nodes already exist, continuing anyway"
    batchnode.setFirstInput(fetchnode)
    sopparms = node.parmsInFolder(("Write","Batch","Houdini Phase",))
    ropparms = batchnode.parmsInFolder(("Houdini Phases",))
    i = 0
    for parm in ropparms :
        if (i < len(sopparms)) :
            sopparmPath = sopparms[i].path()
            parm.setExpression("ch("+ "\"" + sopparmPath + "\"" + ")")
        i += 1


def staticVsAnim(kwargs):
    node = kwargs['node']
    static = node.parm("static").eval()
    if static == 0 :
        node.parm("frame").setExpression("$F")
        node.parm("trange").set("normal")
    if static == 1 :
        node.parm("frame").deleteAllKeyframes()
        node.parm("trange").set("off")

def writeUserLog(kwargs):
    # need to make sop render dir first
    node = kwargs['node']
    text = node.parm("log").eval()
    filename = node.parm("userLogFile").eval()
    file = open(filename,"w")
    file.write(text)
    file.close()


def returnUsers(kwargs):
    import os
    import re

    node = kwargs['node']    
    #dir = hou.pwd().parm("shotbasedir").eval()
    dir = node.parm("shotbasedir").eval()
    files = [f for f in os.listdir(dir) if re.match(r'td_*', f)]
    list = []
    i = 0
    for f in files :
        name = "FX : "
        name += f 
        list += [f,name]
        i += 1
    return list


def refreshVersionList(kwargs): # slightly simpler version
    import os
    import re

    node = kwargs['node']    
    name = node.parm("name").eval()
    basedir = node.parm("baseOutputDir").eval()
    searchdir = "/".join(basedir.split("/")[0:-1])
    dirsThatMatchThisNode = [f for f in os.listdir(searchdir) if re.match(name, f)]

    # we always want to remove existing buttons so we do this later
    #if len(dirsThatMatchThisNode) == 0:
    #    return

    dirsThatMatchThisNode.sort(reverse=True)

    # first we remove any previous existing cleanup buttons
    # we ignore the first parm, as it is the let_me_clean toggle, which remains.
    # We have to re-get the parms each time we delete, as they are reordered under the hood!

    n = len(node.parmsInFolder(("Management","Version Cleanup",)))
    if n > 1:
        for i in range(n-1): # don't remove let_me_clean toggle!
            parms = node.parmsInFolder(("Management","Version Cleanup",)) ### FOLDER LAYOUT HAS CHANGED
            node.removeSpareParmTuple(parms[1].tuple())  # again, always skip the [0] as it is let_me_clean toggle

    if len(dirsThatMatchThisNode) == 0:
        return

    # now construct delete buttons and callback scripts for each of these dirs.
    thisnode = kwargs['node'].path()
    for dir in dirsThatMatchThisNode:
        
        buttonName = dir.translate(None,"!@#$.") + "Button"
        dirToDelete = kwargs['node'].evalParm('elem_subdir') + "/" + dir
        dirSize = directorySize(dirToDelete)

        # callback script for delete button does three things. Delete the files, delete the label, delete the button.
        callback =  "import subprocess,os\n"
        del_cmd = "[\'rm\',\'-r\',\'%s\']"%dirToDelete
        callback += "subprocess.Popen(%s,preexec_fn=os.setsid,close_fds=True)\n"%del_cmd
        callback += "\nhou.node(\"%s\").removeSpareParmTuple(hou.parm(\"%s/%s\").tuple())"%(thisnode,thisnode,buttonName)
        callback += "\nhou.phm().show_cleanup(kwargs)"
        #butn = hou.ButtonParmTemplate(buttonName,"Delete Version : %s " %dir,
        butn = hou.ButtonParmTemplate(buttonName,"Delete Version : %s : %s" %(dir, dirSize),
            script_callback_language=hou.scriptLanguage.Python,
            script_callback= callback,
            disable_when = "{ let_me_clean == 0 }")
        ### FOLDER LAYOUT HAS CHANGED
        kwargs['node'].addSpareParmTuple(butn,in_folder=("Management","Version Cleanup",),create_missing_folders=True)

def directorySize(dir):

    import os

    folder = dir
    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
    return human(folder_size)

def human(size):

    B = "B"
    KB = "KB" 
    MB = "MB"
    GB = "GB"
    TB = "TB"
    UNITS = [B, KB, MB, GB, TB]
    HUMANFMT = "%f %s"
    HUMANRADIX = 1024.

    for u in UNITS[:-1]:
        if size < HUMANRADIX : return HUMANFMT % (size, u)
        size /= HUMANRADIX

    return HUMANFMT % (size,  UNITS[-1])

def switch_frame(kwargs):
    """Switches the frame parameter depending on the Valid Frame Range."""
    
    valid_frange = int(kwargs['script_value'])
    
    node = kwargs['node']
    frame_parm = node.parm('frame')
    frame_val = frame_parm.eval()    
    
    if valid_frange == 2:
        frame_parm.setExpression("$F")
    else:
        frame_parm.setExpression("$RFSTART")
