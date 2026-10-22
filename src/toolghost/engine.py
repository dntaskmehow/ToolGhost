import time
import requests
from typing import List, Dict, Any
from pydantic import BaseModel
from .config import ToolGhostConfig
from .schema_parser import SchemaParser

class GhostFinding(BaseModel):
    tool: str
    parameter: str
    payload: Any
    status_code: int
    response_snippet: str
    anomaly_detected: bool
    reason: str

class ToolGhostEngine:
    PAYLOADS = {
        "string": ["../../etc/passwd", "; id;", "'; DROP TABLE users; --", "A" * 5000],
        "integer": [99999999, -1, 0, "admin"],
        "boolean": ["true", None, 1]
    }

    def __init__(self, config: ToolGhostConfig):
        self.config = config
        self.schema = SchemaParser.load_schema(config.schema_file)
        self.parameters = SchemaParser.extract_parameters(self.schema)

    def run(self) -> List[GhostFinding]:
        findings: List[GhostFinding] = []
        session = requests.Session()

        for p_info in self.parameters:
            t_name = p_info["tool"]
            p_name = p_info["parameter"]
            p_type = p_info["type"]

            payloads = self.PAYLOADS.get(p_type, ["test_payload"])

            for payload in payloads:
                body = {
                    "tool": t_name,
                    "arguments": {
                        p_name: payload
                    }
                }

                try:
                    resp = session.post(
                        self.config.target_url,
                        headers=self.config.headers,
                        json=body,
                        timeout=self.config.timeout
                    )
                except Exception:
                    continue

                snippet = resp.text[:150].replace("\n", " ")
                anomaly = False
                reason = "Normal execution behavior."

                if resp.status_code == 500:
                    anomaly = True
                    reason = "Internal Server Error triggered by malformed tool argument."
                elif "root:" in snippet or "uid=" in snippet:
                    anomaly = True
                    reason = "CRITICAL: System execution signature detected in response output!"
                elif resp.status_code == 200 and ("error" not in snippet.lower() and "invalid" not in snippet.lower()):
                    anomaly = True
                    reason = "Tool accepted anomalous/malformed argument without validation."

                if anomaly:
                    findings.append(GhostFinding(
                        tool=t_name,
                        parameter=p_name,
                        payload=str(payload),
                        status_code=resp.status_code,
                        response_snippet=snippet,
                        anomaly_detected=True,
                        reason=reason
                    ))

                time.sleep(0.02)

        return findings
