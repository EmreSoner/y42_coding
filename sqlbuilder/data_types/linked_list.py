

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next_node = None
        self.prev_node = None


class DoublyLinkedList:
    def __init__(self, head, last):
        self.head = head
        self.last = last

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next_node
