from sqlbuilder.service import SqlStringBuilderService

if __name__ == '__main__':
    request = {
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
                "type": "SORT",
                "transformObject": {
                    "fields": "`id`, `name`, `age`",
                    "order": "`age`, `name` DESC"
                }
            },
            "D": {
                "key": "D",
                "type": "INPUT",
                "transformObject": {
                    "fields": "`id`, UPPER(`name`) as `name`, `age`"
                }
            },
            "E": {
                "key": "E",
                "type": "OUTPUT",
                "transformObject": {
                    "fields": "*",
                    "limit": 100,
                    "offset": 0
                }
            }
        },
        "edges": [
            {
                "from": "A",
                "to": "B"
            },
            {
                "from": "B",
                "to": "C"
            },
            {
                "from": "C",
                "to": "D"
            },
            {
                "from": "D",
                "to": "E"
            }
        ]
    }

    sql_string_builder_service = SqlStringBuilderService(**request)
    print(sql_string_builder_service.build_sql_string())

