from datastructure.node import *
from random import randint


class LinkedList:
    '''
    Doubly linked list. Previous pointer is made through parent property of the node object.
    '''
    def __init__(self, NodeClass=Node):        
        assert issubclass(NodeClass, BaseNode), 'Invalid NodeClass'
        self._head = None        
        self._size = 0
        self.__NodeClass = NodeClass
    
    def __len__(self):
        return self._size
    
    def __getitem__(self, index):
        if not (isinstance(index, int) and 0 <= index < self._size):
            raise IndexError('Invalid index')
        n = self._head
        for i in range(index):
            n = n[0]
        return n.value
    
    def __iter__(self):
        current = self._head
        while current:
            yield current.value
            current = current[0]
    
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
    
    def add_multiple(self, values):
        for v in values:
            self.append(v)
    
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
        fw.remove_child(0)
        return value
    
    @classmethod
    def generate(self, n, min_val, max_val):
        ll = self()
        for i in range(n):
            ll.append(randint(min_val, max_val))
        return ll
    
    def __repr__(self):
        rep = {}
        def list_repr(node, rep, level):
            if node is None:
                return
            rep[level] = node
            list_repr(node[0], rep, level+1)
        list_repr(self._head, rep, 1)
        return f'{self.__class__.__name__}<%s>: %s' % (self._size, rep)
    
    def __str__(self):
        def list_str(node):
            if node is None:
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return "%s"% val + ', ' + list_str(node[0])
        return f'{self.__class__.__name__}<{self._size}>: [{list_str(self._head)[:-2]}]'
    

class LinkedListFast(LinkedList):
    '''
    LinkedListFast uses an tail property to improve speed of append and pop.
    '''
    def __init__(self, NodeClass=Node):
        super().__init__(NodeClass)
        self._tail = None
    
    def append(self, value):
        self._size += 1
        if self._head is None:
            self._head = self._tail = self._LinkedList__NodeClass(value, 1)
            return self
        self._tail[0] = self._LinkedList__NodeClass(value, 1)
        self._tail = self._tail[0]
        return self
        
    def pop(self):
        assert self._head is not None, 'Popping from empty list'
        
        self._size -= 1
        if self._head == self._tail:
            value = self._head.value
            self._head = self._tail = None
            return value
        
        value = self._tail.value
        self._tail = self._tail._parents[0]
        self._tail.remove_child(0)
        return value
