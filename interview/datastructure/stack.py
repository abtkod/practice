from datastructure.node import *


class Stack:
    def __init__(self, NodeClass=Node):
        assert issubclass(NodeClass, BaseNode), 'Invalid NodeClass'
        self.__NodeClass = NodeClass
        self._top = None
        self._size = 0        
    
    def __len__(self):
        return self._size    

    
    def push(self, value):
        new_node = self.__NodeClass(value,1)
        if self._top is not None:
            new_node[0] = self._top
        self._top = new_node
        self._size += 1
    
    def pop(self):
        if len(self) == 0:
            return None        
        val = self._top.value        
        self._top = self._top[0] if len(self) > 1 else None
        self._size -= 1
        return val
    
    def __repr__(self):
        rep = {}
        def stack_repr(node, rep, level):
            if node is None:                                
                return
            rep[level] = node
            stack_repr(node[0], rep, level+1)
        stack_repr(self._top, rep, 1)
        return 'Stack<%s>: %s' % (self._size, rep)
    
    def __str__(self):                
        def stack_str(node):
            if node is None:                                
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return val + ' > ' +"%s"% stack_str(node[0])
        return f'{self.__class__.__name__}<{self._size}>: [{stack_str(self._top)[:-3] }]'
