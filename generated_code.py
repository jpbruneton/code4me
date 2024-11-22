def generate_binary_trees(leaf_values: List[int]) -> List[TreeNode]:
    def build_trees(start, end):
        if start > end:
            return [None]
        
        trees = []
        for i in range(start, end + 1):
            left_trees = build_trees(start, i - 1)
            right_trees = build_trees(i + 1, end)
            
            for left in left_trees:
                for right in right_trees:
                    root = TreeNode(leaf_values[i])
                    root.left = left
                    root.right = right
                    trees.append(root)
        
        return trees
    
    return build_trees(0, len(leaf_values) - 1) if leaf_values else []

def build_tree_from_index(leaf_values, start_index, end_index):
    if start_index > end_index:
        return None

    mid = (start_index + end_index) // 2
    node = TreeNode(leaf_values[mid])

    if start_index == end_index:
        return node

    node.left = build_tree_from_index(leaf_values, start_index, mid - 1)
    node.right = build_tree_from_index(leaf_values, mid + 1, end_index)

    return node

def compute_sum(tree):
    if not tree:
        return 0
    return tree.val + compute_sum(tree.left) + compute_sum(tree.right)

def verify_root_value(tree, target_value):
    if not tree:
        return False
    return tree.val == target_value

def run(leaf_values, target_value):
    from binarytree import tree, Node
    
    def generate_trees(nodes):
        if not nodes:
            return [None]
        
        result = []
        for i in range(len(nodes)):
            left_trees = generate_trees(nodes[:i])
            right_trees = generate_trees(nodes[i + 1:])
            
            for left in left_trees:
                for right in right_trees:
                    node = Node(nodes[i])
                    node.left = left
                    node.right = right
                    result.append(node)
        
        return result

    def find_match(root, target):
        if root is None:
            return []
        
        result = []
        if root.value == target:
            result.append(root)
        
        result.extend(find_match(root.left, target))
        result.extend(find_match(root.right, target))
        
        return result

    nodes = generate_trees(leaf_values)
    for node in nodes:
        match = find_match(node, target_value)
        for m in match:
            print(tree(m))

class TreeNode:
    def __init__(self, value: int, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.value = value
        self.left = left
        self.right = right

def generate_binary_trees(leaf_values):
    if not leaf_values:
        return [None]
    
    trees = []
    
    for i in range(len(leaf_values)):
        left_subtrees = generate_binary_trees(leaf_values[:i])
        right_subtrees = generate_binary_trees(leaf_values[i + 1:])
        
        for left in left_subtrees:
            for right in right_subtrees:
                root = TreeNode(leaf_values[i])
                root.left = left
                root.right = right
                trees.append(root)
    
    return trees

def build_tree_from_leaves(leaf_values):
    def helper(leaves):
        if not leaves:
            return [None]
        
        result = []
        for i in range(1, len(leaves)):
            left_trees = helper(leaves[:i])
            right_trees = helper(leaves[i:])
            
            for left in left_trees:
                for right in right_trees:
                    root = TreeNode(leaves[i])
                    root.left = left
                    root.right = right
                    result.append(root)
        
        return result
    
    return helper(leaf_values)

def construct_trees(nodes):
    if not nodes:
        return [None]
    
    trees = []
    for i in range(len(nodes)):
        left_subtrees = construct_trees(nodes[:i])
        right_subtrees = construct_trees(nodes[i+1:])
        
        for left in left_subtrees:
            for right in right_subtrees:
                root = TreeNode(nodes[i].val)
                root.left = left
                root.right = right
                trees.append(root)
    
    return trees

def verify_and_filter_trees(trees: List[TreeNode], target_value: int) -> List[TreeNode]:
    return [tree for tree in trees if tree.val == target_value]

def isSumTree(root):
    if root is None or (root.left is None and root.right is None):
        return True
 
    if isSumTree(root.left) and isSumTree(root.right):
        if root.left is None:
            left_data = 0
        elif root.left.left is None and root.left.right is None:
            left_data = root.left.data
        else:
            left_data = 2 * (root.left.data)
 
        if root.right is None:
            right_data = 0
        elif root.right.left is None and root.right.right is None:
            right_data = root.right.data
        else:
            right_data = 2 * (root.right.data)
 
        return root.data == left_data + right_data
 
    return False

def match_target(root):
    if not root:
        return 0
    left = match_target(root.left)
    right = match_target(root.right)
    root.val += left + right
    return root.val

def run(root, target):
    def traverse(node):
        nonlocal total_count
        if not node:
            return 0
        new_val = node.val + traverse(node.left) + traverse(node.right)
        if new_val == target:
            total_count += 1
        return new_val
    
    total_count = 0
    traverse(root)
    return total_count

