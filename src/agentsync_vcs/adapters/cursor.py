import yaml
from .base import BaseAdapter
from ..models import AgentRule

class CursorAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Cursor .mdc format
        frontmatter = {
            "description": rule.description,
            "globs": rule.globs,
            "alwaysApply": rule.always_apply
        }
        # Use safe_dump for cleaner output
        fm_str = yaml.safe_dump(frontmatter, sort_keys=False)
        content = f"---\n{fm_str}---\n{rule.body}"
        file_path = f".cursor/rules/{rule.name}.mdc"
        return {file_path: content}
