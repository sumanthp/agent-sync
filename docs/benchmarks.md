# Performance Benchmarks

`agentsync-vcs` is designed for enterprise-scale repositories. We maintain a high-performance translation engine optimized for speed and low resource consumption.

## Benchmark Results

All benchmarks were conducted on a standard development machine (12th Gen Intel i7, 32GB RAM).

| Metric | Target: Cursor | Target: Claude | Industry Standard | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Scalability (100 Rules)** | ~0.25s | ~0.15s | < 1.0s | ✅ Pass |
| **Stress Test (500 Rules)** | ~1.50s | ~1.15s | < 3.0s | ✅ Pass |

## Key Optimizations
- **O(1) File Lookup**: Uses set-based hashing for shared file detection.
- **Efficient Parsing**: Regex-based frontmatter extraction avoids full markdown AST parsing where not needed.
- **Minimized I/O**: Intelligently groups and merges rules before writing to disk.

## How to Run Benchmarks
To verify performance on your own hardware, run:
```bash
python tests/benchmark_performance.py
```

This will generate synthetic rule sets and measure the duration of the `pull` command across multiple targets.
