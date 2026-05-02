from .base import BaseAdapter
from ..models import AgentRule

class TraeAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Trae supports .trae/rules/ (Universal) or .trae/skills/ (Modular)
        if rule.type == "skill":
            # Skills require a directory with SKILL.md
            content = f"# Skill: {rule.name}\n"
            if rule.description:
                content += f"**Description:** {rule.description}\n\n"
            content += f"## Instructions\n{rule.body}"
            
            safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
            file_path = f".trae/skills/{safe_name}/SKILL.md"
            return {file_path: content}
            
        # Universal rules go to .trae/rules/*.md
        content = f"# {rule.name}\n\n"
        if rule.description:
            content += f"**Description:** {rule.description}\n\n"
        if rule.globs:
            content += f"**Globs:** {', '.join(rule.globs)}\n\n"
        content += rule.body
        
        safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
        file_path = f".trae/rules/{safe_name}.md"
        return {file_path: content}
