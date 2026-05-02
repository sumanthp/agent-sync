from .base import BaseAdapter
from ..models import AgentRule

class WindsurfAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Windsurf supports .windsurfrules (root) or .windsurf/rules/*.md
        if rule.type == "global" or (rule.always_apply and not rule.globs):
            content = f"\n### {rule.name}\n{rule.body}\n"
            return {".windsurfrules": content}
            
        content = f"# {rule.name}\n\n"
        if rule.description:
            content += f"**Description:** {rule.description}\n\n"
        if rule.globs:
            content += f"**Globs:** {', '.join(rule.globs)}\n\n"
        
        content += rule.body
        safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
        file_path = f".windsurf/rules/{safe_name}.md"
        return {file_path: content}
