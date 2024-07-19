from anytree import RenderTree
from anytree.exporter import UniqueDotExporter
from collatz import CollatzNumbers

root = CollatzNumbers(1,0,None)

parents = [root]
for _ in range(12):
    children = []
    for parent in parents:
        parent.generate_children()
        for baby in parent.children:
            children.append(baby)
    # print(' '.join([el.__str__() for el in children]))
    parents = children


for pre, fill, node in RenderTree(root):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(8))

UniqueDotExporter(root).to_picture("tree.png")