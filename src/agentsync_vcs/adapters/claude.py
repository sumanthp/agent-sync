from .base import BaseAdapter
from ..models import AgentRule

class ClaudeAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Claude Code CLAUDE.md and SKILL.md
        header = f"\n## Rule: {rule.name}\n"
        if rule.description:
            header += f"**Description:** {rule.description}\n"
        if rule.globs:
            header += f"**Globs:** {', '.join(rule.globs)}\n"
        
        content = f"{header}\n{rule.body}\n"
        
        if rule.type == "skill":
            return {"SKILL.md": content}
        return {"CLAUDE.md": content}
