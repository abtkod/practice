from datastructure.node import *


class LinkedList:
    def __init__(self, fixed_dtype=True):        
        self._head = None        
        self._size = 0
        self.__NodeClass = Node if fixed_dtype else BaseNode
    
    def __len__(self):
        return self._size    
    
    def __getitem__(self, index):
        if not (isinstance(index, int) and 0 <= index < self._size):
            raise IndexError('Invalid index')
        n = self._head
        for i in range(index):
            n = n[0]
        return n.value
        
        
    def __setitem__(self, index, value):
        if not (isinstance(index, int) and 0 <= index < self._size):
            raise IndexError('Invalid index')
        n = self._head
        for i in range(index):
            n = n[0]
        n.value = value
    
    def append(self, value):
        self._size += 1
        if self._head is None:
            self._head = self.__NodeClass(value, 1)
            return
        fw = self._head
        while fw[0] is not None:
            fw = fw[0]
        fw[0] = self.__NodeClass(value, 1)        
        
    def pop(self):
        assert self._head is not None, 'Popping from empty list'
        
        self._size -= 1        
        if self._head[0] is None:
            value = self._head.value
            self._head = None
            return value
        
        fw = self._head
        while fw[0][0] is not None:
            fw = fw[0]
        value = fw[0].value
        fw[0] = None
        return value
    
    def __repr__(self):
        rep = {}
        def list_repr(node, rep, level):
            if node is None:                                
                return
            rep[level] = node
            list_repr(node[0], rep, level+1)
        list_repr(self._head, rep, 1)
        return 'LinkedList(%s): %s' % (self._size, rep)
    
    def __str__(self):                
        def list_str(node):
            if node is None:                                
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return "%s"% val + ', ' + list_str(node[0])
        return 'LinkedList: [' + list_str(self._head)[:-2] + ']'


class LinkedListFast(LinkedList):
    # using parent sttribute in BaseNode class
    def __init__(self, fixed_dtype=True):
        super().__init__(fixed_dtype)
        self._tail = None
    
    def append(self, value):
        self._size += 1
        if self._head is None:
            self._head = self._tail = self._LinkedList__NodeClass(value, 1)
            return
        self._tail[0] = self._LinkedList__NodeClass(value, 1)
        self._tail = self._tail[0]
        
    def pop(self):
        assert self._head is not None, 'Popping from empty list'
        
        self._size -= 1        
        if self._head == self._tail:
            value = self._head.value
            self._head = self._head = None
            return value
        
        value = self._tail.value
        self._tail = self._tail._parent
        return value