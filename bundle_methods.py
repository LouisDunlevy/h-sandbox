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
     
     
