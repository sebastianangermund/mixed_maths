from anytree import RenderTree
from anytree.exporter import UniqueDotExporter
from collatz import CollatzNumbers


def print_to_terminal(root):
    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8))


def run_collatz_general(graph_depth, root):
    """Run the entire Collatz generation."""
    parents = [root]
    for i in range(graph_depth):
        children = []
        for parent in parents:
            parent.generate_children()
            for baby in parent.children:
                children.append(baby)
        if not children:
            print('HUH')
            break
        parents = children
    return root


def run_collatz_odd_even(graph_depth, root):
    """Run the specific odd-even Collatz generation."""
    parents = [root]
    for i in range(graph_depth):
        children = []
        for parent in parents:
            parent.generate_odd_even_children()
            for baby in parent.children:
                children.append(baby)
        if not children:
            print('HUH')
            break
        parents = children
    return root


if __name__ == "__main__":
    graph_depth = 10    # Do not use big values (> 6) when generating the entire Collatz tree
    root_sequence = (1, 0)
    root_parent = None
    root = CollatzNumbers(root_sequence[0], root_sequence[1], root_parent, 'root')
    tree = run_collatz_odd_even(graph_depth, root)
    print_to_terminal(root)
    save_fig_path = "collatz_tree.pdf"
    UniqueDotExporter(root).to_picture(save_fig_path)
