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
    
    try:
        frontmatter = yaml.safe_load(frontmatter_raw)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")
        
    if not isinstance(frontmatter, dict):
        raise ValueError("Invalid format: Frontmatter must be a YAML dictionary")
    
    return AgentRule(
        name=str(frontmatter.get('name', 'unnamed')),
        description=str(frontmatter.get('description', '')),
        globs=frontmatter.get('globs', []) if isinstance(frontmatter.get('globs'), list) else [],
        always_apply=bool(frontmatter.get('always_apply', False)),
        type=str(frontmatter.get('type', 'rule')),
        body=body
    )
