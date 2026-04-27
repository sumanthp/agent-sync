import yaml
import re
from .models import AgentRule

def parse_markdown_rule(content: str) -> AgentRule:
    """
    Parses a Universal Markdown rule containing YAML frontmatter and Markdown body.
    """
    # Regex to split frontmatter and body
    # Support both --- and --- at the start/end of frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        # Try without leading newline if the file starts exactly with ---
        match = re.match(r'^---\s*(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        
    if not match:
        raise ValueError("Invalid format: Missing YAML frontmatter delimited by ---")
    
    frontmatter_raw = match.group(1)
    body = match.group(2).strip()
    
    frontmatter = yaml.safe_load(frontmatter_raw)
    
    return AgentRule(
        name=frontmatter.get('name', 'unnamed'),
        description=frontmatter.get('description', ''),
        globs=frontmatter.get('globs', []),
        always_apply=frontmatter.get('always_apply', False),
        body=body
    )
