# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def postorderTraversal(self, root: TreeNode):
        ans = []
        if not root:
            return ans

        stack = []
        current = root
        last_visited = None

        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                top_node = stack[-1]
                if top_node.right and last_visited != top_node.right:
                    current = top_node.right
                else:
                    ans.append(top_node.val)
                    last_visited = stack.pop()

        return ans
