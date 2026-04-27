import sys
import os
import json
import argparse
import glob
import subprocess
import shutil
from pathlib import Path
from .main import ADAPTERS, parse_markdown_rule

def get_cache_dir():
    return Path.home() / ".agent-sync" / "cache"

def load_config():
    config_path = Path(".agent-sync/config.json")
    if not config_path.exists():
        return {"remotes": []}
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config):
    os.makedirs(".agent-sync", exist_ok=True)
    with open(".agent-sync/config.json", 'w') as f:
        json.dump(config, f, indent=2)

def handle_init():
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

def handle_remote_add(url):
    config = load_config()
    if url in config["remotes"]:
        print("Remote already exists.")
        return
    config["remotes"].append(url)
    save_config(config)
    print(f"Added remote: {url}")

def sync_remote(url):
    cache_dir = get_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    safe_name = url.replace("/", "_").replace(":", "_")
    repo_path = cache_dir / safe_name
    
    if not repo_path.exists():
        subprocess.run(["git", "clone", url, str(repo_path)], check=True)
    else:
        subprocess.run(["git", "-C", str(repo_path), "pull"], check=True)

def handle_sync():
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

def handle_pull(target):
    if target not in ADAPTERS:
        print(f"Unknown target: {target}")
        return

    # 1. Discover local files
    files = glob.glob("*.md")
    
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
    all_translated = {}
    
    shared_files = ["CLAUDE.md", "AGENTS.md", "GEMINI.md", ".github/copilot-instructions.md"]

    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            rule = parse_markdown_rule(content)
            translated = adapter.translate(rule)
            
            for path, text in translated.items():
                if path in all_translated and path in shared_files:
                    all_translated[path] += "\n" + text
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

def main():
    parser = argparse.ArgumentParser(prog="agentsync-vcs")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init")
    
    remote_parser = subparsers.add_parser("remote")
    remote_sub = remote_parser.add_subparsers(dest="subcommand")
    add_parser = remote_sub.add_parser("add")
    add_parser.add_argument("url")

    subparsers.add_parser("sync")
    
    pull_parser = subparsers.add_parser("pull")
    pull_parser.add_argument("target")

    args = parser.parse_args()

    if args.command == "init":
        handle_init()
    elif args.command == "remote":
        if args.subcommand == "add":
            handle_remote_add(args.url)
    elif args.command == "sync":
        handle_sync()
    elif args.command == "pull":
        handle_pull(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
