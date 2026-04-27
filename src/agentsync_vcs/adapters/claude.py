from .base import BaseAdapter
from ..models import AgentRule

class ClaudeAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Claude Code CLAUDE.md
        # Returns a content block that should be part of CLAUDE.md
        header = f"\n## Rule: {rule.name}\n"
        if rule.description:
            header += f"**Description:** {rule.description}\n"
        if rule.globs:
            header += f"**Globs:** {', '.join(rule.globs)}\n"
        
        content = f"{header}\n{rule.body}\n"
        return {"CLAUDE.md": content}
