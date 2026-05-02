import yaml
from .base import BaseAdapter
from ..models import AgentRule

class CopilotAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # GitHub Copilot instructions
        if rule.globs:
            # Targeted instruction requiring applyTo
            frontmatter = {
                "name": rule.name,
                "description": rule.description or f"Scope specific rules for {rule.name}",
                "applyTo": rule.globs
            }
            fm_str = yaml.safe_dump(frontmatter, sort_keys=False)
            content = f"---\n{fm_str}---\n{rule.body}"
            safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip()
            file_path = f".github/instructions/{safe_name}.instructions.md"
            return {file_path: content}
        else:
            # Global project instruction
            # Optional frontmatter for name/description can be added even to global
            content = f"\n### {rule.name}\n{rule.body}\n"
            return {".github/copilot-instructions.md": content}
