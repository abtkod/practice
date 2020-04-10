from .node import *

class BinaryTree(Node):
    def __init__(self, val):                
        super().__init__(val, max_child_count=2)
        
    def replace_child(self, cindex, child):
        #overriding Node's replace_child method to ensure every nodes has at most one parent.
        assert 0 <= cindex < len(self._children), 'Invalid child index'
        assert isinstance(child, type(self)), f'New child must be a subclasses of {type(self)}'
        if self._children[cindex] is not None:
            # remove current child
            self.remove_child(cindex)
        self._children[cindex] = child
        # this is the main difference between BinaryTreeNode and Node.
        child._parents = [self]
        
    def access(self, idxlst:list):
        nd = self
        try:            
            for i in idxlst:
                nd = nd[i]
        except TypeError:        
            nd = -1
        return nd
                
    def __repr__(self):
        rep = {}        
        def subtree_repr(node, rep, level):
            if level not in rep.keys():
                rep[level] = list()
            if node is None:                
                rep[level].append(None)
                return
            
            rep[level].append(Node.__repr__(node))            
            for c in node._children:                
                subtree_repr(c, rep, level+1)
        subtree_repr(self, rep, 0)
        if rep[max(rep)].count(None) == len(rep[max(rep)]):
            rep.pop(max(rep))
        return f'{self.__class__.__name__}<depth={max(rep)}>: ' + repr(rep)
    
    def __str__(self):        
        def subtree_str(node):                                
            if node is None:                
                return '_'
            
            val_str = '(' + str(node.value) + '; '            
            for c in node._children:
                val_str += subtree_str(c) + ', '
            val_str = val_str[:-2] + ')'
            return val_str
        return f'{self.__class__.__name__}: ' + subtree_str(self)


class BinarySearchTree:
    def __init__(self, dtype):
        self._dtype = dtype
        self._root = None
        
    def insert(self, val):
        if self._root is None:            
            self._root = BinaryTree(val)
            return self
        assert isinstance(val, self._root._dtype), 'Invalid data type'
        p = self._root
        while True:
            if val <= p.value and p[0] is None:
                p[0] = BinaryTree(val)
                break
            if val > p.value and p[1] is None:
                p[1] = BinaryTree(val)
                break            
            p = p[0] if val <= p.value else p[1]
        return self
    
    def search(self, val):
        if self._root.value == val:
            return ['root']
        ndidx = []
        p = self._root
        while p is not None:
            if p.value == val:
                return ndidx
            if val < p.value:
                ndidx.append(0)
                p = p[0]
            else:
                ndidx.append(1)
                p = p[1]        
        return -1
    
    def access(self, idxlst:list):
        if idxlst == ['root']:
            return self._root
        return self._root.access(idxlst)
    
    def remove(self, val):
        idx = self.search(val)
        if idx == -1:
            return -1
        nd = self.access(idx)
        
        if nd != self._root:
            par_nd = nd._parents[0]
        else:
            # create a dummy Node and then remove it at the end of the function
            par_nd = BinaryTree(val)
            par_nd[0] = nd
        ndidx = 0 if par_nd[0] == nd else 1
                
        if nd.child_count() == 0:
            par_nd.remove_child(ndidx)
            if nd == self._root:                
                self._root = None
            return self
        
        subidx = 1 if nd[1] is not None else 0
        lookupidx = 0 if nd[1] is not None else 1
        par_nd.replace_child(ndidx, nd[subidx])    
        if nd[lookupidx] is not None:
            sub = nd[subidx]
            while sub[lookupidx] is not None:
                sub = sub[lookupidx]
            sub[lookupidx] = nd[lookupidx]
        if nd == self._root:
            self._root = nd[subidx]
        return self
    
    def __repr__(self):
        return repr(self._root)
    
    def __str__(self):
        return str(self._root)


if __name__ == '__main__':    
    BST = BinarySearchTree
    BT = BinaryTree
    root = BT('ROOT')
    root[0] = BT('l')
    root[1] = BT('r')
    root[0][0] = BT('ll')
    root[0][1] = BT('lr')
    root[1][1] = BT('rr')
    root[1][1][1] = BT('rrr')

    print(root)
    print(repr(root))
    print('*'*60)

    print(root[1][1])
    print(repr(root[1][1][1]))
    print('*'*60)

    print(root[1][1][1] == root.access([1,1,1]))
    print('*'*60)

    bst = BST(int)
    print(bst.insert(100).insert(10).insert(20).insert(15).insert(17).insert(16).insert(1).insert(5))
    print(bst.search(11))
    print(bst.search(100))
    print(bst.search(10))
    print(bst.search(15))
    print(bst.access(bst.search(15)))
    print('*' * 60)

    print(bst)
    print(bst.remove(10))