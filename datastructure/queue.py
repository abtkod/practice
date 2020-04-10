from .node import BaseNode, Node, NodeFlexible


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
        return f'{self.__class__.__name__}<%s>: %s' % (self._size, rep)
    
    def __str__(self):                
        def queue_str(node):
            if node is None:                                
                return ''
            val = str(node.value) if type(node.value) != str else "'%s'" % node.value
            return "%s"% val + ' > ' + queue_str(node[0])
        return f'{self.__class__.__name__}<{self._size}>: [{queue_str(self._first)[:-3]}]'


if __name__ == '__main__':    
	q = Queue(NodeFlexible)
	q.push(1)
	q.push('2')
	q.push('three')
	print(repr(q))
	print('-' * 50)
	print(q)
	print(len(q), q.pop())
	print(len(q), q.pop())
	print(len(q))
	print(q)
	print('*'*50)
	q = Queue(Node)
	q.push(1)
	q.push(2)
	q.push(3)
	print(q)
	print(len(q), q.pop())
	print(len(q), q.pop())
	print(len(q))
	print(q)