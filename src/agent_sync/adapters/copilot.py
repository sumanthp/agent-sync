import yaml
from .base import BaseAdapter
from ..models import AgentRule

class CopilotAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # GitHub Copilot instructions
        if rule.globs:
            # Path-specific instruction
            frontmatter = {
                "applyTo": rule.globs
            }
            fm_str = yaml.safe_dump(frontmatter, sort_keys=False)
            content = f"---\n{fm_str}---\n{rule.body}"
            file_path = f".github/instructions/{rule.name}.instructions.md"
            return {file_path: content}
        else:
            # Global project instruction
            content = f"\n### {rule.name}\n{rule.body}\n"
            return {".github/copilot-instructions.md": content}
