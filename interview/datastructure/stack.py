from datastructure.node import *


class Stack:
    def __init__(self):        
        self.__NodeClass = BaseNode
        self._top = None
        self._size = 0        
    
    def __len__(self):
        return self._size    

    
    def push(self, value):
        new_node = self.__NodeClass(value,1)        
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
    
    def __str__(self):                
        def stack_str(node):
            if node is None:                                
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return val + ' > ' +"%s"% stack_str(node[0])
        return 'Stack: [' + stack_str(self._top)[:-3] + ']'


class Stack2(Stack):
    # using parent attribute of each node to give Stack flexibility of being either fixed-typed container or not
    def __init__(self, fixed_dtype=True):
        super().__init__()        
        self._Stack__NodeClass = Node if fixed_dtype else BaseNode
    
    def push(self, value):
        prev_top = self._top        
        self._top = self._Stack__NodeClass(value,1)
        if prev_top is not None:
            prev_top[0] = self._top
        self._size += 1
    
    def pop(self):
        if len(self) == 0:
            return None        
        val = self._top.value        
        self._top = self._top._parent
        if self._top is not None:
            self._top[0] = None
        self._size -= 1
        return val
    
    def __str__(self):                
        def stack_str(node):
            if node is None:                                
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return val + ' > ' +"%s"% stack_str(node._parent)
        return 'Stack: [' + stack_str(self._top)[:-3] + ']'