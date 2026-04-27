from .base import BaseAdapter
from ..models import AgentRule

class GeminiAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Gemini CLI GEMINI.md
        header = f"\n## Rule: {rule.name}\n"
        if rule.description:
            header += f"**Description:** {rule.description}\n"
        if rule.globs:
            header += f"**Scope:** `{', '.join(rule.globs)}`\n"
        
        content = f"{header}\n{rule.body}\n"
        return {"GEMINI.md": content}
