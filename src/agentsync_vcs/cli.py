import sys
import os
import json
import argparse
import glob
import subprocess
import shutil
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from .main import ADAPTERS, parse_markdown_rule
from .models import SHARED_FILES

def validate_url(url: str) -> bool:
    """Basic validation for git URLs (HTTPS or SSH)."""
    https_pattern = r'^https?://[a-zA-Z0-9.-]+(/[a-zA-Z0-9._/-]*)?(\.git)?$'
    ssh_pattern = r'^git@[a-zA-Z0-9.-]+:[a-zA-Z0-9._/-]+(\.git)?$'
    return bool(re.match(https_pattern, url) or re.match(ssh_pattern, url))

def get_cache_dir() -> Path:
    return Path.home() / ".agent-sync" / "cache"

def load_config() -> Dict[str, Any]:
    config_path = Path(".agent-sync/config.json")
    if not config_path.exists():
        return {"remotes": []}
    with open(config_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Warning: .agent-sync/config.json is malformed. Resetting config.")
            return {"remotes": []}

def save_config(config: Dict[str, Any]) -> None:
    os.makedirs(".agent-sync", exist_ok=True)
    with open(".agent-sync/config.json", 'w') as f:
        json.dump(config, f, indent=2)

def handle_init() -> None:
    content = """---
name: sample-rule
description: A sample rule for agent-sync
globs: ["**/*.js"]
---
- Use clean code principles.
- Add comments to complex logic.
"""
    with open("sample-rule.md", 'w') as f:
        f.write(content)
    
    save_config({"remotes": []})
    print("Initialized agent-sync project with sample-rule.md and .agent-sync/config.json")

def handle_remote_add(url: str) -> None:
    if not validate_url(url):
        print(f"Error: Invalid git URL: {url}")
        return
        
    config = load_config()
    if url in config["remotes"]:
        print("Remote already exists.")
        return
    config["remotes"].append(url)
    save_config(config)
    print(f"Added remote: {url}")

def handle_remote_list() -> None:
    config = load_config()
    remotes = config.get("remotes", [])
    if not remotes:
        print("No remotes configured.")
        return
    print("Configured remotes:")
    for url in remotes:
        print(f"  - {url}")

def handle_remote_remove(url: str) -> None:
    config = load_config()
    if url not in config["remotes"]:
        print(f"Remote not found: {url}")
        return
    config["remotes"].remove(url)
    save_config(config)
    print(f"Removed remote: {url}")

def sync_remote(url: str) -> None:
    if not validate_url(url):
        raise ValueError(f"Invalid git URL: {url}")
        
    cache_dir = get_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize name for filesystem
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', url)
    repo_path = cache_dir / safe_name
    
    if not repo_path.exists():
        subprocess.run(["git", "clone", url, str(repo_path)], check=True)
    else:
        subprocess.run(["git", "-C", str(repo_path), "pull"], check=True)

def handle_sync() -> None:
    config = load_config()
    if not config["remotes"]:
        print("No remotes configured. Use 'agent-sync remote add <url>' first.")
        return
    
    for url in config["remotes"]:
        print(f"Syncing from {url}...")
        try:
            sync_remote(url)
        except Exception as e:
            print(f"Failed to sync {url}: {e}")

def handle_pull(target: str) -> None:
    if target not in ADAPTERS:
        print(f"Unknown target: {target}")
        return

    # 1. Discover local files (excluding generated ones)
    all_local = glob.glob("*.md")
    files = [f for f in all_local if f not in SHARED_FILES]
    
    # 2. Discover cached files
    cache_dir = get_cache_dir()
    remote_files = []
    if cache_dir.exists():
        for path in cache_dir.rglob("*.md"):
            remote_files.append(str(path))
            
    all_files = files + remote_files
    if not all_files:
        print("No markdown rules found locally or in cache.")
        return

    adapter = ADAPTERS[target]
    all_translated: Dict[str, str] = {}
    
    # Pre-calculate shared files for faster lookup in loop
    shared_set = set(SHARED_FILES)

    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            rule = parse_markdown_rule(content)
            translated = adapter.translate(rule)
            
            for path, text in translated.items():
                if path in shared_set:
                    if path in all_translated:
                        all_translated[path] += "\n" + text
                    else:
                        all_translated[path] = text
                else:
                    all_translated[path] = text
        except Exception as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)

    for path, content in all_translated.items():
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {path}")
    
    print(f"Successfully pulled rules for {target}")

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agentsync-vcs",
        description="Universal Version Control System for AI Agent behaviors.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agentsync-vcs init
  agentsync-vcs remote add https://github.com/org/rules.git
  agentsync-vcs remote list
  agentsync-vcs sync
  agentsync-vcs pull cursor
  agentsync-vcs pull claude
  agentsync-vcs pull windsurf
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init
    subparsers.add_parser(
        "init", 
        help="Initialize a new project with a sample rule and config"
    )
    
    # Help
    subparsers.add_parser(
        "help", 
        help="Show this help message and exit"
    )
    
    # Remote
    remote_parser = subparsers.add_parser(
        "remote", 
        help="Manage remote rule repositories"
    )
    remote_sub = remote_parser.add_subparsers(dest="subcommand", help="Remote sub-commands")
    
    add_parser = remote_sub.add_parser(
        "add", 
        help="Add a new remote repository"
    )
    add_parser.add_argument("url", help="URL of the git repository")

    remote_sub.add_parser(
        "list", 
        help="List configured remote repositories"
    )

    remove_parser = remote_sub.add_parser(
        "remove", 
        help="Remove a configured remote repository"
    )
    remove_parser.add_argument("url", help="URL of the git repository to remove")

    # Sync
    subparsers.add_parser(
        "sync", 
        help="Sync rules from all configured remote repositories"
    )
    
    # Pull
    pull_parser = subparsers.add_parser(
        "pull", 
        help="Compile rules and pull them into a target agent's format"
    )
    pull_parser.add_argument(
        "target", 
        choices=list(ADAPTERS.keys()),
        help=f"Target agent format (available: {', '.join(ADAPTERS.keys())})"
    )

    args = parser.parse_args()

    if args.command == "init":
        handle_init()
    elif args.command == "remote":
        if args.subcommand == "add":
            handle_remote_add(args.url)
        elif args.subcommand == "list":
            handle_remote_list()
        elif args.subcommand == "remove":
            handle_remote_remove(args.url)
        else:
            remote_parser.print_help()
    elif args.command == "sync":
        handle_sync()
    elif args.command == "pull":
        handle_pull(args.target)
    elif args.command == "help":
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
