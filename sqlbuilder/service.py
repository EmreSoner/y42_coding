from sqlbuilder.builder_types import BuilderTypes
from sqlbuilder.data_types.linked_list import Node, DoublyLinkedList


class SqlStringBuilderService:
    def __init__(self, nodes: dict, edges: list):
        self.nodes = nodes
        self.edges = edges

    def build_sql_string(self) -> str:
        linked_nodes = self.create_linked_nodes()
        sql_string_list = []
        for node in linked_nodes:
            builder = BuilderTypes(node.data['type']).get_builder()(node)
            sql_string_list.append(builder.get_string())

        return '{} {} {};'.format(
            "WITH",
            ', '.join(sql_string_list),
            'SELECT * FROM {}'.format(linked_nodes.last.data['key'])
        )

    def create_linked_nodes(self) -> DoublyLinkedList:
        prev_node, current_node, head = None, None, None
        for edge in self.edges:
            if not current_node:
                node = Node(self.nodes[edge['from']])
                head = node
            else:
                node = current_node

            node.next_node = Node(self.nodes[edge['to']])
            node.prev_node = prev_node

            prev_node = node
            current_node = node.next_node

        last_node = current_node
        last_node.prev_node = prev_node

        linked_list = DoublyLinkedList(head, current_node)
        return linked_list
