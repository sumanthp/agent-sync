import unittest
import os
import shutil
import tempfile
from pathlib import Path
from agentsync_vcs.cli import handle_init, handle_pull
from agentsync_vcs.main import ADAPTERS

class TestAgentSyncVCS(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_init(self):
        handle_init()
        self.assertTrue(os.path.exists("sample-rule.md"))
        self.assertTrue(os.path.exists(".agent-sync/config.json"))
        
        with open("sample-rule.md", 'r') as f:
            content = f.read()
            self.assertIn("name: sample-rule", content)

    def test_adapter_translations(self):
        # Sample rule content
        rule_md = """---
name: test-rule
description: A test rule
globs: ["**/*.py"]
---
- Use type hints.
"""
        with open("test-rule.md", 'w') as f:
            f.write(rule_md)

        # Test each adapter
        for target in ADAPTERS.keys():
            handle_pull(target)
            
            if target == "cursor":
                self.assertTrue(os.path.exists(".cursor/rules/test-rule.mdc"))
            elif target == "claude":
                self.assertTrue(os.path.exists("CLAUDE.md"))
            elif target == "copilot":
                # Copilot can generate either global or specific instructions based on globs
                has_global = os.path.exists(".github/copilot-instructions.md")
                has_specific = os.path.exists(f".github/instructions/test-rule.instructions.md")
                self.assertTrue(has_global or has_specific)
            elif target == "gemini":
                self.assertTrue(os.path.exists("GEMINI.md"))
            elif target == "codex":
                self.assertTrue(os.path.exists("AGENTS.md"))
            elif target == "windsurf":
                # Windsurf can generate either .windsurfrules or .windsurf/rules/*.md
                has_global = os.path.exists(".windsurfrules")
                has_specific = os.path.exists(".windsurf/rules/test-rule.md")
                self.assertTrue(has_global or has_specific)
            elif target == "trae":
                # Trae can generate either .trae/project_rules.md or .trae/skills/*.md
                has_project = os.path.exists(".trae/project_rules.md")
                has_specific = os.path.exists(".trae/skills/test-rule.md")
                self.assertTrue(has_project or has_specific)

    def test_pull_merging(self):
        # Create two rules
        rule1 = "---\nname: r1\nglobs: []\n---\n- Rule 1"
        rule2 = "---\nname: r2\nglobs: []\n---\n- Rule 2"
        
        with open("r1.md", 'w') as f: f.write(rule1)
        with open("r2.md", 'w') as f: f.write(rule2)
        
        handle_pull("claude")
        
        with open("CLAUDE.md", 'r') as f:
            content = f.read()
            self.assertIn("Rule 1", content)
            self.assertIn("Rule 2", content)

    def test_claude_skill_generation(self):
        # Create a skill rule
        skill_rule = """---
name: my-skill
type: skill
description: A custom skill
---
- Skill behavior
"""
        with open("skill.md", 'w') as f:
            f.write(skill_rule)
            
        handle_pull("claude")
        
        self.assertTrue(os.path.exists("SKILL.md"))
        with open("SKILL.md", 'r') as f:
            content = f.read()
            self.assertIn("my-skill", content)
            self.assertIn("Skill behavior", content)

    def test_cursor_global_generation(self):
        # Create a global rule
        global_rule = """---
name: global-rule
type: global
description: A global rule
---
- Global behavior
"""
        with open("global.md", 'w') as f:
            f.write(global_rule)
            
        handle_pull("cursor")
        
        self.assertTrue(os.path.exists(".cursorrules"))
        with open(".cursorrules", 'r') as f:
            content = f.read()
            self.assertIn("global-rule", content)
            self.assertIn("Global behavior", content)

    def test_windsurf_rule_categorization(self):
        # 1. Global rule for Windsurf
        global_rule = "---\nname: w-global\ntype: global\n---\nGlobal Windsurf"
        with open("w1.md", 'w') as f: f.write(global_rule)
        
        # 2. Specific rule for Windsurf
        spec_rule = "---\nname: w-spec\nglobs: [\"*.py\"]\n---\nSpec Windsurf"
        with open("w2.md", 'w') as f: f.write(spec_rule)
        
        handle_pull("windsurf")
        
        self.assertTrue(os.path.exists(".windsurfrules"))
        self.assertTrue(os.path.exists(".windsurf/rules/w-spec.md"))
        
        with open(".windsurfrules", 'r') as f:
            self.assertIn("Global Windsurf", f.read())

    def test_trae_skill_and_merging(self):
        # 1. Skill for Trae
        skill = "---\nname: t-skill\ntype: skill\n---\nTrae Skill"
        with open("t1.md", 'w') as f: f.write(skill)
        
        # 2. Project rule for Trae
        rule = "---\nname: t-rule\n---\nTrae Rule"
        with open("t2.md", 'w') as f: f.write(rule)
        
        handle_pull("trae")
        
        self.assertTrue(os.path.exists(".trae/skills/t-skill.md"))
        self.assertTrue(os.path.exists(".trae/project_rules.md"))
        
        with open(".trae/project_rules.md", 'r') as f:
            content = f.read()
            self.assertIn("Trae Rule", content)

    def test_real_world_scenarios(self):
        # 1. Complex Architecture Rule
        arch_rule = """---
name: arch-standard
description: High-level architecture standards
type: global
always_apply: true
---
# Architecture Standards

- Use **Domain Driven Design** (DDD).
- All services must implement the `BaseService` interface:
  ```python
  class BaseService(ABC):
      @abstractmethod
      def execute(self, context: dict) -> Result:
          pass
  ```
- No direct database access from the UI layer.
"""
        # 2. Complex API Skill
        api_skill = """---
name: api-expert
description: Specialized skill for building REST APIs
type: skill
globs: ["src/api/**/*.py"]
---
## API Expert Skill

1. **Validation**: Use Pydantic for all request/response models.
2. **Security**: Ensure OAuth2 scopes are checked:
   - `read:items`
   - `write:items`
3. **Docs**: Auto-generate OpenAPI specs.
"""
        
        with open("arch.md", 'w', encoding='utf-8') as f: f.write(arch_rule)
        with open("api.md", 'w', encoding='utf-8') as f: f.write(api_skill)
        
        # Test Claude (Merging and Skill separation)
        handle_pull("claude")
        
        self.assertTrue(os.path.exists("CLAUDE.md"))
        self.assertTrue(os.path.exists("SKILL.md"))
        
        with open("CLAUDE.md", 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("# Architecture Standards", content)
            self.assertIn("class BaseService(ABC):", content)
            self.assertIn("**Domain Driven Design**", content)
            
        with open("SKILL.md", 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("## API Expert Skill", content)
            self.assertIn("`read:items`", content)

        # Test Cursor (MDC and Global)
        handle_pull("cursor")
        self.assertTrue(os.path.exists(".cursorrules"))
        self.assertTrue(os.path.exists(".cursor/rules/api-expert.mdc"))
        
        with open(".cursorrules", 'r', encoding='utf-8') as f:
            self.assertIn("class BaseService(ABC):", f.read())

if __name__ == "__main__":
    unittest.main()
