import unittest

from sqlbuilder.service import SqlStringBuilderService


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.request = {
            "nodes": {
                "A": {
                    "key": "A",
                    "type": "INPUT",
                    "transformObject": {
                        "tableName": "users",
                        "fields": "`id`, `name`, `age`"
                    }
                },
                "B": {
                    "key": "B",
                    "type": "FILTER",
                    "transformObject": {
                        "fields": "`id`, `name`, `age`",
                        "operations": [
                            {
                                "join_operator": "AND",
                                "field": "`age`",
                                "operator": ">",
                                "value": "18"
                            },
                            {
                                "join_operator": "OR",
                                "field": "`id`",
                                "operator": ">",
                                "value": "5"
                            }
                        ]
                    }
                },
                "C": {
                    "key": "C",
                    "type": "OUTPUT",
                    "transformObject": {
                        "fields": "*",
                        "limit": 100,
                        "offset": 0
                    }
                },
            },
            "edges": [
                {
                    "from": "A",
                    "to": "B"
                },
                {
                    "from": "B",
                    "to": "C"
                }
            ]
        }

    def test_sql_builder_output(self):
        sql_sample = """WITH A as (
            SELECT `id`, `name`, `age` FROM `users`   
        ), B as (
            SELECT `id`, `name`, `age` FROM `A` WHERE `age` > 18 OR `id` > 5  
        ), C as (
            SELECT * FROM `B` LIMIT 100 OFFSET 0
        ) SELECT * FROM C;"""

        sql_string_builder_service = SqlStringBuilderService(**self.request)
        self.assertEqual(sql_string_builder_service.build_sql_string().replace(' ', ''), sql_sample.replace(' ', ''))


if __name__ == '__main__':
    unittest.main()
