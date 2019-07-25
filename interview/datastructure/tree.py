from datastructure.node import *

class BinaryTreeNode(Node):
    def __init__(self, val):                
        Node.__init__(self, val, max_child_count=2)
                
    def __repr__(self):
        rep = {}        
        def subtree_repr(node, rep, level):
            if level not in rep.keys():
                rep[level] = list()
            if node is None:                
                rep[level].append('null')
                return
            
            rep[level].append(Node.__repr__(node))            
            for c in node._children:                
                subtree_repr(c, rep, level+1)
        subtree_repr(self, rep, 0)
        return 'tree: ' + repr(rep)
    
    def __str__(self):        
        def subtree_str(node):                                
            if node is None:                
                return '_'
            
            val_str = '(' + str(node.value) + '; '            
            for c in node._children:
                val_str += subtree_str(c) + ', '
            val_str = val_str[:-2] + ')'
            return val_str
        return subtree_str(self)