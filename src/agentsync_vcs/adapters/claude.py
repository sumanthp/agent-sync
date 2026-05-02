import yaml
from .base import BaseAdapter
from ..models import AgentRule

class ClaudeAdapter(BaseAdapter):
    def translate(self, rule: AgentRule) -> dict:
        # Claude Code CLAUDE.md (Project Rules) and .claude/skills/ (Project Skills)
        if rule.type == "skill":
            # Official Agent Skills structure: .claude/skills/<name>/SKILL.md
            frontmatter = {
                "name": rule.name,
                "description": rule.description or f"Modular skill for {rule.name}"
            }
            # Use safe_dump to ensure valid YAML
            fm_str = yaml.safe_dump(frontmatter, sort_keys=False)
            content = f"---\n{fm_str}---\n\n# {rule.name}\n{rule.body}"
            
            # Sanitize rule name for path safety
            safe_name = "".join(c for c in rule.name if c.isalnum() or c in ("-", "_")).strip().lower()
            file_path = f".claude/skills/{safe_name}/SKILL.md"
            return {file_path: content}
            
        # Standard rules go to CLAUDE.md
        header = f"\n## Rule: {rule.name}\n"
        if rule.description:
            header += f"**Description:** {rule.description}\n"
        if rule.globs:
            header += f"**Globs:** {', '.join(rule.globs)}\n"
        
        content = f"{header}\n{rule.body}\n"
        return {"CLAUDE.md": content}
