import sys
import os
import json
from .parser import parse_markdown_rule
from .adapters.cursor import CursorAdapter
from .adapters.claude import ClaudeAdapter
from .adapters.copilot import CopilotAdapter
from .adapters.codex import CodexAdapter
from .adapters.gemini import GeminiAdapter

ADAPTERS = {
    "cursor": CursorAdapter(),
    "claude": ClaudeAdapter(),
    "copilot": CopilotAdapter(),
    "codex": CodexAdapter(),
    "gemini": GeminiAdapter()
}

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m compiler.main <target> <file1> <file2> ...")
        sys.exit(1)
    
    target = sys.argv[1].lower()
    files = sys.argv[2:]
    
    if target not in ADAPTERS:
        print(f"Unknown target: {target}")
        sys.exit(1)
    
    adapter = ADAPTERS[target]
    all_translated = {} # {file_path: content}
    
    for file_path in files:
        if not os.path.exists(file_path):
            # Try relative to CWD if not absolute
            pass
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rule = parse_markdown_rule(content)
            translated = adapter.translate(rule)
            
            for path, text in translated.items():
                if path in all_translated:
                    # Append if it's a shared file like CLAUDE.md or AGENTS.md
                    if path in ["CLAUDE.md", "AGENTS.md", "GEMINI.md", ".github/copilot-instructions.md"]:
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
