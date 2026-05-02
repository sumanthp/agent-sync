from pydantic import BaseModel, Field
from typing import List, Optional

SHARED_FILES = [
    "CLAUDE.md", 
    "AGENTS.md", 
    "GEMINI.md", 
    ".github/copilot-instructions.md", 
    "SKILL.md", 
    ".cursorrules", 
    ".windsurfrules", 
    ".trae/project_rules.md"
]

class AgentRule(BaseModel):
    name: str
    description: str
    globs: List[str] = Field(default_factory=list)
    body: str
    always_apply: bool = False
    type: str = "rule" # e.g., "rule", "skill", "global"
