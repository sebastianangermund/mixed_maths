import time
from anytree import RenderTree
from anytree.exporter import UniqueDotExporter
from collatz import CollatzNumbers


def print_to_terminal(root):
    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8))


def run(graph_depth, root):
    """Run the entire Collatz generation."""
    parents = [root]
    for i in range(graph_depth):
        children = []
        for parent in parents: # TODO: parallelize this loop
            parent.generate_children()
            children.extend(parent.children)
        if not children:
            print('HUH')
            break
        parents = children
    return root


if __name__ == "__main__":
    start = time.time()
    graph_depth = 24    # Do not use big values (> 7) when generating visualizations for the entire Collatz tree
    root_sequence = (1, 0)
    root_parent = None
    root = CollatzNumbers(root_parent, root_sequence[0], root_sequence[1], 'ROOT')
    tree = run(graph_depth, root)
    run_time = time.time() - start
    print(f"Collatz tree generation took {run_time:.2f} seconds.")
    # print_to_terminal(tree)
    # save_fig_path = "collatz_tree.pdf"
    # UniqueDotExporter(root).to_picture(save_fig_path)
