def synchronized(f):
    def wrapper(self, *args, **kwargs):
        try:
            self.lock.acquire()
            return f(self, *args, **kwargs)
        finally:
            self.lock.release()
    return wrapper

class PlayerStack:    
    class Node:
        def __init__(self, value):
            self.prev = None
            self.next = None
            self.value = value
    
    def __init__(self):
        self._head = None
        self._tail = None
        self._nodes = {}
        
    def update(self, player):
        if player is None:
            raise ValueError("Player can't be None")
            
        node = None
        if player not in self._nodes:
            node = PlayerStack.Node(player)
            self._nodes[player] = node            
        else:
            node = self._nodes[player]
            self._remove_node(node)                    
        
        if self._head is None:
            assert self._tail is None
            self._head = node
            self._tail = node
            return

        self._tail.next = node
        node.prev = self._tail
        self._tail = node

    def _remove_node(self, node):
        if self._head is node:
                self._head = node.next
            
        if self._tail is node:
            self._tail = node.prev

        if node.prev is not None:
            node.prev.next = node.next
            node.prev = None

        if node.next is not None:
            node.next.prev = node.prev
            node.next = None
            
    def remove(self, player):        
        if player not in self._nodes:
            raise ValueError("{} not found on stack".format(repr(player)))
        
        self._remove_node(self._nodes[player])
        del self._nodes[player]
        
        
    def __iter__(self):
        node = self._head
        while node is not None:
            yield node.value
            node = node.next        
    
    def __len__(self):
        return len(self._nodes)
