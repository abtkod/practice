from datastructure.node import *


class Queue:
    def __init__(self, NodeClass=Node):
        assert issubclass(NodeClass, BaseNode), 'Invalid NodeClass'
        self.__NodeClass = NodeClass
        self._first = None
        self._last = None
        self._size = 0        
    
    def __len__(self):
        return self._size        
    
    def push(self, value):
        self._size += 1
        if self._first is None:
            self._first = self._last = self.__NodeClass(value, 1)
            return
        
        self._last[0] = self.__NodeClass(value, 1)
        self._last = self._last[0]        
        
    def pop(self):
        if self._first is None:
            return None
        self._size -= 1
        value = self._first.value
        if self._last == self._first:
            self._first = self._last = None
            return value
        self._first = self._first[0]
        return value
    
    def __repr__(self):
        rep = {}
        def queue_repr(node, rep, level):
            if node is None:                                
                return
            rep[level] = node
            queue_repr(node[0], rep, level+1)
        queue_repr(self._first, rep, 1)
        return 'Queue(%s): %s' % (self._size, rep)
    
    def __str__(self):                
        def queue_str(node):
            if node is None:                                
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return "%s"% val + ' > ' + queue_str(node[0])
        return 'Queue: [' + queue_str(self._first)[:-3] + ']'
