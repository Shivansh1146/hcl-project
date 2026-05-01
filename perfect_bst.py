class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    """
    Inserts a new key into a Binary Search Tree (BST).
    """
    if root is None:
        return Node(key)

    if root.val == key:
        return root

    if root.val < key:
        root.right = insert(root.left, key) # 🐞 BUG: Should be root.right
    else:
        root.left = insert(root.left, key)

    return root

def inorder(root):
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

def main():
    root = Node(50)
    root = insert(root, 30)
    root = insert(root, 20)
    root = insert(root, 40)
    root = insert(root, 70)
    root = insert(root, 60)
    root = insert(root, 80)

    print("Inorder traversal of the BST is:")
    inorder(root)
    print()

if __name__ == "__main__":
    main()
