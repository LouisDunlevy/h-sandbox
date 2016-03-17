#get nodes
nodes = nuke.allNodes()
print nodes

### get nuke string
for n in nodes:
if n.Class() == 'Read':
print n.name()
print n.knob('inFile').value()

#extend this to extract versions
for n in nodes:
if n.Class() == 'Read':
print n.name()
curr = n.knob('inFile').value()
ver = curr.split('_')[-3]
take = curr.split('_')[-2]
print curr
print ver
print take

#now lets get the versions
for n in nodes:
if n.Class() == 'Read':
curr = n.knob('inFile').value()
ver = curr.split('_')[-3]
take = curr.split('_')[-2]
fpath = curr.rpartition('/')[0].rpartition('/')[0]+'/'
versbits = curr.replace(fpath, '')
searcher = versbits.split('_v')[0]+'_'
print n.name()
for a in os.listdir(fpath):
if searcher in a:
print a.split('_v')[-1].split('_')[0], a.split('_t')[-1].split('_')[0]

#now let's get the highest version
for n in nodes:
if n.Class() == 'Read':
curr = n.knob('inFile').value()
ver = curr.split('_')[-3]
take = curr.split('_')[-2]
fpath = curr.rpartition('/')[0].rpartition('/')[0]+'/'
versbits = curr.replace(fpath, '')
searcher = versbits.split('_v')[0]+'_'
print n.name()
version = []
for a in os.listdir(fpath):
if searcher in a:
version.append(int(a.split('_v')[-1].split('_')[0]))
print max(version)

#now lets add that versions’ highest take
for n in nodes:
if n.Class() == 'Read':
curr = n.knob('inFile').value()
ver = curr.split('_')[-3]
take = curr.split('_')[-2]
fpath = curr.rpartition('/')[0].rpartition('/')[0]+'/'
versbits = curr.replace(fpath, '')
searcher = versbits.split('_v')[0]+'_'
print n.name()
version = []
for a in os.listdir(fpath):
if searcher in a:
version.append(int(a.split('_v')[-1].split('_')[0]))
newver = max(version)
takes = []
for a in os.listdir(fpath):
if '_v'+str(newver) in a and searcher in a:
takes.append(int(a.split('_t')[-1].split('_')[0]))
newtake = max(takes)
print newver, newtake

#final step, lets update the path and throw it back to the node

for n in nodes:
if n.Class() == 'Read':
curr = n.knob('file').value()
ver = curr.split('_')[-3]
take = curr.split('_')[-2]
fpath = curr.rpartition('/')[0].rpartition('/')[0]+'/'
versbits = curr.replace(fpath, '')
searcher = versbits.split('_v')[0]+'_'
print n.name()
version = []
for a in os.listdir(fpath):
if searcher in a:
version.append(int(a.split('_v')[-1].split('_')[0]))
newver = max(version)
takes = []
for a in os.listdir(fpath):
if '_v'+str(newver) in a and searcher in a:
takes.append(int(a.split('_t')[-1].split('_')[0]))
newtake = max(takes)
print ver
print take
print curr
new = curr.replace(ver, 'v%02d'%newver)
new =new.replace(take, 't%02d'%newtake)
n.knob('file').setValue(new)
n.knob('on_error').setValue(3)
n.knob("reload").execute()


