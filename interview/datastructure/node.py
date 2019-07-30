# thanks to: 
# https://www.python-course.eu/python3_properties.php
# http://blog.lerner.co.il/python-attributes/
# https://www.programiz.com/python-programming/property

# this node can store any data types including itself.
class BaseNode(object):
    def __init__(self, val=None, max_child_count=0):
        assert 0 <= max_child_count, 'Invalid value for max_child_count'
        self._dtype = type(val) if val is not None else object
        self._data = val
        self._children = [None] * max_child_count
        self._parents = []
            
    @property
    def value(self):        
        return self._data
    
    @value.setter
    def value(self, val):
        self._data = val
        self._dtype = type(val)
        
    def child_count(self):
        return len(self._children) - self._children.count(None)
    
    def replace_child(self, cindex, child):
        assert 0 <= cindex < len(self._children), 'Invalid child index'
        assert isinstance(child, type(self)), f'New child must be a subclasses of {type(self)}'
        if self._children[cindex] is not None:
            # remove current child
            self.remove_child(cindex)
        self._children[cindex] = child
        child._parents.append(self)
        return self
    
    def remove_child(self, cindex):
        assert 0 <= cindex < len(self._children), 'Invalid child index'
        if self._children[cindex] is None:
            return
        self._children[cindex]._parents.remove(self)
        self._children[cindex] = None
        return self
    
    def max_child_count(self):
        return len(self._children)
            
    def __getitem__(self, cindex):
        assert 0 <= cindex < len(self._children), 'Invalid child index'
        return self._children[cindex]
    
    def __setitem__(self, cindex, child):        
        return self.remove_child(cindex) if child is None else self.replace_child(cindex, child)        
        
    def __call__(self):
        '''
        Let's make objects callable and
        give birth to another node of the same class/data type and the same number of children.
        thanks to: https://www.python-course.eu/python3_classes_and_type.php
        '''
        obj = self.__class__(None, self.max_child_count())        
        obj._dtype = self._dtype
        return obj
    
    def __repr__(self):
        return str({'ntype': type(self), 'dtype':self._dtype, 
                    'parents_count': len(self._parents),                    
                    'children_count':self.child_count(), 
                    'max_children':self.max_child_count(), 
                    'value':self._data})
    
    def __str__(self):
        children_str = [str(c.value) if c is not None else '_' for c in self._children]        
        return '({}; {})'.format(self.value, ', '.join(children_str))


class Node(BaseNode):
    '''
    Consistent nodes. Verifies the same data type and max_child_count across the ancestry!
    
    '''
    def __init__(self, val, max_child_count):        
        super().__init__(val, max_child_count)
    
    @property
    def value(self):        
        return self._data
    
    @value.setter
    def value(self, val):
        assert isinstance(val, self._dtype), f'{type(val)} data-type cannot be stored in a Node of dtype: {self._dtype}'
        self._data = val
        
    def __setitem__(self, cindex, child):
        assert issubclass(child._dtype, self._dtype), 'dtypes do not match! (%s vs. %s)'\
                                                % (child._dtype, self._dtype)
        assert child.max_child_count() == self.max_child_count(), 'Maximum children must be %d'% self.max_child_count()
        super().__setitem__(cindex, child)
        
        
class NodeFlexible(BaseNode):
    '''
    Infinite number of children with no restriction on data types.
    '''
    def __iadd__(self, other):
        '''
        Adds the right node as the child/or expands children list capacity. (overloading += operator)
        '''
        assert isinstance(other, int) or isinstance(other, NodeFlexible), 'Invalid node extension'
        if isinstance(other, int):
            assert other > 0, 'Invalid node extension'
            self._children += [None] * other
        else:
            self._children += [None]
            cidx = len(self._children)-1
            # use BaseNode __setitem__ to add the new node and set parents.
            self[cidx] = other
        return self
        
    def __isub__(self, otherNode):
        '''
        Removes the rights node from the list of children. (overloading -= operator)
        '''
        assert isinstance(otherNode, NodeFlexible), 'Invalid node removal'
        while True:
            try:
                cidx = self._children.index(otherNode)
                self.remove_child(cidx)
            except ValueError:            
                break
        return self
                
    def clean_children(self):
        while None in self._children:
            self._children.remove(None)
