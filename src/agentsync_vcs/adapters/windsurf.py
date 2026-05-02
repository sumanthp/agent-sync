from .base import BaseAdapter
from ..models import AgentRule

class WindsurfAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Windsurf modern format is .windsurf/rules/*.md
        # Even global rules are better as modular files in the rules directory.
        
        content = f"# {rule.name}\n\n"
        if rule.description:
            content += f"**Description:** {rule.description}\n\n"
        
        # Windsurf can use XML-style tagging for grouping or just markdown
        if rule.globs:
            content += f"**Globs:** {', '.join(rule.globs)}\n\n"
        
        content += rule.body
        
        safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
        file_path = f".windsurf/rules/{safe_name}.md"
        return {file_path: content}
