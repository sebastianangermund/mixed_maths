from anytree import RenderTree
from anytree.exporter import UniqueDotExporter
from collatz import CollatzNumbers


graph_depth = 10
root = CollatzNumbers(27, 2, None, 'root')

parents = [root]
for i in range(graph_depth):
    children = []
    for parent in parents:
        # parent.generate_children()
        parent.generate_odd_even_children()
        for baby in parent.children:
            children.append(baby)
    if not children:
        print('HUH')
        break
    # for child in children:
    #     print(child.name)
    #     if not (child.constant % 2 == 0):
    #         print('counter example found!')
    parents = children


for pre, fill, node in RenderTree(root):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(8))

UniqueDotExporter(root).to_picture("tree.png")
