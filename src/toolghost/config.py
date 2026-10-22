from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ToolGhostConfig(BaseModel):
    target_url: str
    headers: Dict[str, str] = Field(default_factory=dict)
    schema_file: str
    timeout: float = 15.0
