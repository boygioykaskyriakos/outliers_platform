from queue import Queue
from generic_functions.read_data_from_csv import read_data_from_csv

"""
Algorithm that implements a binary tree in inorder traversal form and then swaps the nodes based on depth
"""


class Node:
    """
    Binary Node
    """
    def __init__(self, data, depth):
        """
        This class is a binary Node with attributes data, depth, left_child and right_child
        :param data: int: the node's data
        :param depth: int : node's depth
        """
        self.data = data
        self.depth = depth
        self.left_child = None
        self.right_child = None


class SwapNodesBinaryTreeInOrderTraversal:
    """
    This class implements a a Binary Tree in InOrder traversal form and swaps the nodes based on its depth
    """
    def __init__(self, root, data, swaps):
        """
        :param root: Node: root Node of the class
        :param data: list[Nodes]: Nodes of the tree
        :param swaps: list[int]: depths that swaps will occur
        """
        self.root = root
        self.data = data
        self.swaps = swaps
        self.depths = {self.root.depth}

    def create_tree(self):
        """
        the method that will create the initial tree of the class based on the self.data
        :return:
        """
        n = 0
        q = Queue()
        q.put(self.root)

        while n < len(self.data):
            current_node = q.get()

            left_node = None if self.data[n][0] == -1 else Node(self.data[n][0], depth=current_node.depth + 1)
            right_node = None if self.data[n][1] == -1 else Node(self.data[n][1], depth=current_node.depth + 1)

            current_node.left_child = left_node
            current_node.right_child = right_node

            if current_node.left_child is not None and current_node.left_child.data != -1:
                q.put(current_node.left_child)
                self.depths.add(current_node.depth + 1)
            if current_node.right_child is not None and current_node.right_child.data != -1:
                q.put(current_node.right_child)
                self.depths.add(current_node.depth + 1)

            n += 1

    def swap_nodes_without_recursion(self, k_swaps):
        _results = []
        stack_q = []
        current_node = self.root

        while True:
            if current_node is not None:
                if current_node.depth in k_swaps:
                    temp_child_left = current_node.left_child
                    current_node.left_child = current_node.right_child
                    current_node.right_child = temp_child_left

                stack_q.append(current_node)
                current_node = current_node.left_child

            elif stack_q:
                current_node = stack_q.pop()
                _results.append(current_node.data)
                current_node = current_node.right_child
            else:
                break

        return _results

    def run(self):
        all_results = []
        self.create_tree()

        # without recursion
        for swap in self.swaps:
            k_swaps = [x for x in self.depths if x % swap == 0]
            all_results.append(self.swap_nodes_without_recursion(k_swaps))

        return all_results


if __name__ == "__main__":
    # indexes = [
    #     [2, 3],
    #     [4, 5],
    #     [6, -1],
    #     [-1, 7],
    #     [8, 9],
    #     [10, 11],
    #     [12, 13],
    #     [-1, 14],
    #     [-1, -1],
    #     [15, -1],
    #     [16, 17],
    #     [-1, -1],
    #     [-1, -1],
    #     [-1, -1],
    #     [-1, -1],
    #     [-1, -1],
    #     [-1, -1]
    # ]
    # queries = [2, 3]

    indexes, queries = read_data_from_csv("test_files/test_1024")

    root_node = Node(1, depth=1)
    tree_obj = SwapNodesBinaryTreeInOrderTraversal(root=root_node, data=indexes, swaps=queries)
    results = tree_obj.run()

    for result in results:
        print(result)