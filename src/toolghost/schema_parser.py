import json
from pathlib import Path
from typing import Dict, Any, List

class SchemaParser:
    @staticmethod
    def load_schema(filepath: str) -> Dict[str, Any]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {filepath}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def extract_parameters(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        params = []
        tools = schema.get("tools", []) or schema.get("functions", [])
        for tool in tools:
            function_def = tool.get("function", tool)
            name = function_def.get("name", "unknown_tool")
            parameters = function_def.get("parameters", {}).get("properties", {})
            for param_name, param_meta in parameters.items():
                params.append({
                    "tool": name,
                    "parameter": param_name,
                    "type": param_meta.get("type", "string"),
                    "description": param_meta.get("description", "")
                })
        return params
