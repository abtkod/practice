# thanks to: 
# https://www.python-course.eu/python3_properties.php
# http://blog.lerner.co.il/python-attributes/
# https://www.programiz.com/python-programming/property

# this node can store any data types including itself.
class BaseNode(object):
    def __init__(self, val=object(), max_child_count=0):
        self._dtype = type(val)
        self._data = val
        self._children = [None] * max_child_count
        self._parent = None
            
    @property
    def value(self):        
        return self._data
    
    @value.setter
    def value(self, val):
        self._data = val
        self._dtype = type(val)
        
    def child_count(self):
        return len(self._children) - self._children.count(None)
    
    def max_child_count(self):
        return len(self._children)
        
    def get_child(self, child_index):
        assert 0 <= child_index < len(self._children), 'Invalid child index'
        return self._children[child_index]
    
    def __getitem__(self, cindex):
        return self.get_child(cindex)
    
    def __setitem__(self, cindex, child):
        if child is None:
            self._children[cindex] = None
            return
        assert isinstance(child, type(self)), 'Children must be the same subclass as parent'
        assert 0 <= cindex < len(self._children), 'Invalid child index'                
        if self._children[cindex] is not None:
            # setting child's parent as None
            self._children[cindex]._parent = None        
        self._children[cindex] = child
        child._parent = self
    
    def __repr__(self):
        return str({'child_count':self.child_count(), 'max_children':self.max_child_count(), 
                'value':self._data, 'dtype':self._dtype})
    
    def __str__(self):
        children_str = [str(c.value) if c is not None else '_' for c in self._children]        
        return '({}; {})'.format(self.value, ', '.join(children_str))


class Node(BaseNode):
    @property
    def value(self):        
        return self._data
    
    @value.setter
    def value(self, val):        
        if not isinstance(val, self._dtype):
            raise TypeError('{} data-type cannot be stored in this Node({})'.format(type(val), self._dtype))
        self._data = val
        
    def __setitem__(self, cindex, child):
        if child is None:
            self._children[cindex] = None
            return
        assert isinstance(child, type(self)), 'Children must be the same subclass as parent'
        assert 0 <= cindex < len(self._children), 'Invalid child index'
        assert issubclass(child._dtype, self._dtype), 'dtypes do not match! (%s vs. %s)'\
                                                % (child._dtype, self._dtype)
        assert child.max_child_count() == self.max_child_count(), 'Maximum children must be %d'% self.max_child_count()
        if self._children[cindex] is not None:
            # setting child's parent as None            
            self._children[cindex]._parent = None        
        self._children[cindex] = child
        child._parent = self