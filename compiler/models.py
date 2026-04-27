from pydantic import BaseModel, Field
from typing import List, Optional

class AgentRule(BaseModel):
    name: str
    description: str
    globs: List[str] = Field(default_factory=list)
    body: str
    always_apply: bool = False
