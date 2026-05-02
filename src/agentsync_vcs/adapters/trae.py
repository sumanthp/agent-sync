from .base import BaseAdapter
from ..models import AgentRule

class TraeAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Trae supports .trae/project_rules.md or .trae/skills/*.md
        content = f"# {rule.name}\n\n"
        if rule.description:
            content += f"**Description:** {rule.description}\n\n"
        
        content += rule.body
        
        if rule.type == "skill":
            safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
            file_path = f".trae/skills/{safe_name}.md"
            return {file_path: content}
            
        return {".trae/project_rules.md": f"\n{content}\n"}
