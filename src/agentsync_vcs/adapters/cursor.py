import yaml
from .base import BaseAdapter
from ..models import AgentRule

class CursorAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Cursor .mdc format is preferred for specific rules
        if rule.type == "global" or (rule.always_apply and not rule.globs):
            content = f"\n### {rule.name}\n{rule.body}\n"
            return {".cursorrules": content}
            
        frontmatter = {
            "description": rule.description,
            "globs": rule.globs,
            "alwaysApply": rule.always_apply
        }
        # Use safe_dump for cleaner output
        fm_str = yaml.safe_dump(frontmatter, sort_keys=False)
        content = f"---\n{fm_str}---\n{rule.body}"
        
        # Sanitize rule name for path safety
        safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
        file_path = f".cursor/rules/{safe_name}.mdc"
        return {file_path: content}
