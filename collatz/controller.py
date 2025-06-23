import time
import sys
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
    start = time.time()
    for i in range(graph_depth):
        print(f"Generating Collatz tree depth {i + 1}...")
        children = []
        for parent in parents: # TODO: parallelize this loop
            parent.generate_children()
            children.extend(parent.children)
        parents = children
        run_time = time.time() - start
        print(f"Done in {run_time:.2f} seconds.")
    return root


if __name__ == "__main__":
    graph_depth = 4    # Do not use big values (> 7) when generating visualizations for the entire Collatz tree
    root_sequence = (1, 0)
    root_parent = None
    root = CollatzNumbers(root_parent, root_sequence[0], root_sequence[1], 'ROOT')
    tree = run(graph_depth, root)
    # sys.exit(0)
    # print_to_terminal(tree)
    save_fig_path = "collatz_tree.pdf"
    UniqueDotExporter(root).to_picture(save_fig_path)
