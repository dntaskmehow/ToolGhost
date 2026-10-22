import unittest
import json
import tempfile
from pathlib import Path
from toolghost.schema_parser import SchemaParser

class TestToolGhost(unittest.TestCase):
    def test_schema_parsing(self):
        sample_schema = {
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "execute_query",
                        "parameters": {
                            "properties": {
                                "sql": {"type": "string", "description": "SQL query string"}
                            }
                        }
                    }
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tf:
            json.dump(sample_schema, tf)
            tf_name = tf.name

        try:
            schema = SchemaParser.load_schema(tf_name)
            params = SchemaParser.extract_parameters(schema)
            self.assertEqual(len(params), 1)
            self.assertEqual(params[0]["tool"], "execute_query")
            self.assertEqual(params[0]["parameter"], "sql")
        finally:
            Path(tf_name).unlink(missing_ok=True)

if __name__ == "__main__":
    main()
