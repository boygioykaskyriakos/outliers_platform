# Python3 program to construct tree from
# inorder traversal

# Helper class that allocates a new node
# with the given data and None left and
# right pointers.


class newNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


# Prototypes of a utility function to get
# the maximum value in inorder[start..end]

# Recursive function to construct binary of
# size len from Inorder traversal inorder[].
# Initial values of start and end should be
# 0 and len -1.


def buildTree(inorder, start, end):
    if start > end:
        return None

    # Find index of the maximum element
    # from Binary Tree
    i = Max(inorder, start, end)

    # Pick the maximum value and make it root
    root = newNode(inorder[i])

    # If this is the only element in
    # inorder[start..end], then return it
    if start == end:
        return root

    # Using index in Inorder traversal,
    # construct left and right subtress
    root.left = buildTree(inorder, start, i - 1)
    root.right = buildTree(inorder, i + 1, end)

    return root


# UTILITY FUNCTIONS

# Function to find index of the maximum
# value in arr[start...end]
def Max(arr, strt, end):
    i, Max = 0, arr[strt]
    maxind = strt
    for i in range(strt + 1, end + 1):
        if arr[i] > Max:
            Max = arr[i]
            maxind = i
    return maxind


# This funtcion is here just to test buildTree()
def printInorder(node):
    if node == None:
        return

    # first recur on left child
    printInorder(node.left)

    # then print the data of node
    print(node.data, end=" ")

    # now recur on right child
    printInorder(node.right)


# Driver Code
if __name__ == '__main__':
    # Assume that inorder traversal of
    # following tree is given
    #	 40
    # / \
    # 10	 30
    # /		 \
    # 5		 28

    # inorder = [5, 10, 40, 30, 28]
    inorder = [
        [2, 3],
        [4, -1],
        [5, -1],
        [6, -1],
        [7, 8],
        [-1, 9],
        [-1, -1],
        [10, 11],
        [-1, -1],
        [-1, -1],
        [-1, -1]
    ]
    Len = len(inorder)
    root = buildTree(inorder, 0, Len - 1)

    # Let us test the built tree by
    # printing Insorder traversal
    print("Inorder traversal of the",
          "constructed tree is ")
    printInorder(root)

# This code is contributed by PranchalK
