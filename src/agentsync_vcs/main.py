import sys
import os
import json
from typing import Dict, List
from .parser import parse_markdown_rule
from .adapters.cursor import CursorAdapter
from .adapters.claude import ClaudeAdapter
from .adapters.copilot import CopilotAdapter
from .adapters.codex import CodexAdapter
from .adapters.gemini import GeminiAdapter
from .adapters.windsurf import WindsurfAdapter
from .adapters.trae import TraeAdapter
from .models import SHARED_FILES

ADAPTERS = {
    "cursor": CursorAdapter(),
    "claude": ClaudeAdapter(),
    "copilot": CopilotAdapter(),
    "codex": CodexAdapter(),
    "gemini": GeminiAdapter(),
    "windsurf": WindsurfAdapter(),
    "trae": TraeAdapter()
}

def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python -m agentsync_vcs.main <target> <file1> <file2> ...")
        sys.exit(1)
    
    target = sys.argv[1].lower()
    files = sys.argv[2:]
    
    if target not in ADAPTERS:
        print(f"Unknown target: {target}")
        sys.exit(1)
    
    adapter = ADAPTERS[target]
    all_translated: Dict[str, str] = {} # {file_path: content}
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rule = parse_markdown_rule(content)
            translated = adapter.translate(rule)
            
            for path, text in translated.items():
                if path in all_translated:
                    # Append if it's a shared file
                    if path in SHARED_FILES:
                        all_translated[path] += "\n" + text
                    else:
                        all_translated[path] = text
                else:
                    all_translated[path] = text
        except Exception as e:
            # We print to stderr so it doesn't mess up the JSON stdout
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
            
    # Output the result as JSON so the Go CLI can read it easily
    print(json.dumps(all_translated))

if __name__ == "__main__":
    main()
