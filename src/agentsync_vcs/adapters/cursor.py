import yaml
from .base import BaseAdapter
from ..models import AgentRule

class CursorAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Cursor .mdc format is the modern standard
        # Even for "global" rules, we prefer .mdc in the rules directory
        # with alwaysApply: true for better token efficiency and modularity.
        
        frontmatter = {
            "description": rule.description or f"Instructions for {rule.name}",
            "globs": rule.globs,
            "alwaysApply": rule.always_apply or (rule.type == "global")
        }
        
        # Use safe_dump for cleaner output
        fm_str = yaml.safe_dump(frontmatter, sort_keys=False)
        content = f"---\n{fm_str}---\n{rule.body}"
        
        # Sanitize rule name for path safety
        safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
        file_path = f".cursor/rules/{safe_name}.mdc"
        return {file_path: content}
