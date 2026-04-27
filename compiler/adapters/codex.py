from .base import BaseAdapter
from ..models import AgentRule

class CodexAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Codex AGENTS.md
        # Gracefully converting globs to natural language
        header = f"\n## Rule: {rule.name}\n"
        if rule.description:
            header += f"**Description:** {rule.description}\n"
        if rule.globs:
            header += f"**Applies to files matching:** `{', '.join(rule.globs)}`\n"
            header += "\n**Instructions when working on these files:**\n"
        
        content = f"{header}\n{rule.body}\n"
        return {"AGENTS.md": content}
