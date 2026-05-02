import time
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from agentsync_vcs.cli import handle_pull
from agentsync_vcs.main import ADAPTERS

def generate_benchmark_data(count: int, target_dir: str):
    """Generates a large number of rule files for stress testing."""
    for i in range(count):
        content = f"""---
name: rule-{i}
description: Benchmark rule number {i}
globs: ["src/module-{i}/**/*.py"]
---
# Rule {i}
- Standard instruction for module {i}
- Ensure performance is maintained.
"""
        with open(os.path.join(target_dir, f"rule-{i}.md"), 'w') as f:
            f.write(content)

class BenchmarkAgentSync(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def run_benchmark(self, rule_count: int, target: str):
        generate_benchmark_data(rule_count, ".")
        
        start_time = time.time()
        handle_pull(target)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"\n[BENCHMARK] Target: {target} | Rules: {rule_count} | Duration: {duration:.4f}s")
        return duration

    def test_scalability_100_rules(self):
        """Standard industry benchmark: 100 rules should compile in under 1 second."""
        for target in ["cursor", "claude"]:
            duration = self.run_benchmark(100, target)
            self.assertLess(duration, 1.0, f"{target} took too long for 100 rules")

    def test_stress_500_rules(self):
        """Stress test: 500 rules to check for memory leaks or exponential slowdown."""
        duration = self.run_benchmark(500, "claude")
        self.assertLess(duration, 3.0, "Stress test failed performance threshold")

if __name__ == "__main__":
    unittest.main()
