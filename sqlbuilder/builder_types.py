from enum import Enum

from sqlbuilder.exceptions import ImproperlyConfigured


class SQLStringBuilder:
    def __init__(self, node):
        self.node = node

    def get_string(self) -> str:
        raise NotImplementedError

    def get_transform_object(self) -> dict:
        return self.node.data['transformObject']

    @staticmethod
    def get_base_string() -> str:
        sql_string = """{key} as (
            SELECT {fields} FROM `{table_name}` {filter} {sort} {output}
        )"""

        return sql_string

    def get_base_transform_data(self, transform_object) -> dict:
        return {
            'key': self.node.data['key'],
            'fields': transform_object['fields'],
            'table_name': transform_object.get('tableName', self.node.prev_node and self.node.prev_node.data['key']),
        }


class InputBuilder(SQLStringBuilder):
    keys = [{'name': 'tableName', 'type': str}, {'name': 'fields', 'type': list}]

    def get_string(self) -> str:
        base_string = self.get_base_string()
        transform_object = self.get_transform_object()

        transform_data = dict(**{
            'filter': '',
            'sort': '',
            'output': ''
        }, **self.get_base_transform_data(transform_object))

        return base_string.format(**transform_data)


class FilterBuilder(SQLStringBuilder):
    def get_string(self) -> str:
        base_string = self.get_base_string()
        transform_object = self.get_transform_object()

        operations = transform_object['operations']
        first_filter = operations.pop(0)
        filter_string = "WHERE {field} {operator} {value}".format(**first_filter)
        for filter_data in operations:
            filter_string += " {join_operator} {field} {operator} {value}".format(**filter_data)

        transform_data = dict(**{
            'filter': filter_string,
            'sort': '',
            'output': ''
        }, **self.get_base_transform_data(transform_object))

        return base_string.format(**transform_data)


class SortBuilder(SQLStringBuilder):
    def get_string(self):
        base_string = self.get_base_string()
        transform_object = self.get_transform_object()

        transform_data = dict(**{
            'filter': '',
            'sort': 'ORDER BY {}'.format(transform_object['order']),
            'output': ''
        }, **self.get_base_transform_data(transform_object))

        return base_string.format(**transform_data)


class OutputBuilder(SQLStringBuilder):
    def get_string(self):
        base_string = self.get_base_string()
        transform_object = self.get_transform_object()

        transform_data = dict(**{
            'filter': '',
            'sort': '',
            'output': 'LIMIT {limit} OFFSET {offset}'.format(**transform_object)
        }, **self.get_base_transform_data(transform_object))

        return base_string.format(**transform_data)


class BuilderTypes(Enum):
    INPUT = 'INPUT'
    FILTER = 'FILTER'
    SORT = 'SORT'
    OUTPUT = 'OUTPUT'

    def builder_mapping(self):
        return {
            self.INPUT: InputBuilder,
            self.FILTER: FilterBuilder,
            self.SORT: SortBuilder,
            self.OUTPUT: OutputBuilder
        }

    def get_builder(self):
        try:
            return self.builder_mapping()[self]
        except KeyError:
            raise ImproperlyConfigured()
