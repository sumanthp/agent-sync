package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

func Execute() error {
	if len(os.Args) < 2 {
		printUsage()
		return nil
	}

	command := os.Args[1]
	switch command {
	case "pull":
		return handlePull()
	case "init":
		return handleInit()
	case "help":
		printUsage()
		return nil
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
	}
	return nil
}

func printUsage() {
	fmt.Println("agent-sync - Universal Agent VCS")
	fmt.Println("\nUsage:")
	fmt.Println("  agent-sync <command> [arguments]")
	fmt.Println("\nCommands:")
	fmt.Println("  init          Initialize a new agent-sync project")
	fmt.Println("  pull <target> Pull and compile rules for a specific tool (cursor, claude, copilot, codex, gemini)")
	fmt.Println("  help          Show this help message")
}

func handleInit() error {
	// Create a sample rule
	content := `---
name: sample-rule
description: A sample rule for agent-sync
globs: ["**/*.js"]
---
- Use clean code principles.
- Add comments to complex logic.
`
	err := os.WriteFile("sample-rule.md", []byte(content), 0644)
	if err != nil {
		return err
	}
	fmt.Println("Initialized agent-sync project with sample-rule.md")
	return nil
}

func handlePull() error {
	if len(os.Args) < 3 {
		return fmt.Errorf("usage: agent-sync pull <target>")
	}
	target := os.Args[2]

	// 1. Discover all .md files in the current directory
	// In a real version, we would search recursively or look for a manifest
	files, err := filepath.Glob("*.md")
	if err != nil {
		return err
	}

	if len(files) == 0 {
		fmt.Println("No markdown rules found in the current directory.")
		return nil
	}

	// 2. Call the Python compiler
	// Note: In production, the python script would be bundled or in a fixed location
	args := append([]string{"-m", "compiler.main", target}, files...)
	cmd := exec.Command("python", args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("python compiler failed: %v\nOutput: %s", err, string(output))
	}

	// 3. Parse the JSON output
	var result map[string]string
	err = json.Unmarshal(output, &result)
	if err != nil {
		return fmt.Errorf("failed to parse compiler output: %v\nRaw output: %s", err, string(output))
	}

	// 4. Write the translated files
	for path, content := range result {
		// Ensure directory exists
		dir := filepath.Dir(path)
		if dir != "." {
			err = os.MkdirAll(dir, 0755)
			if err != nil {
				return fmt.Errorf("failed to create directory %s: %v", dir, err)
			}
		}

		err = os.WriteFile(path, []byte(content), 0644)
		if err != nil {
			fmt.Printf("Failed to write %s: %v\n", path, err)
		} else {
			fmt.Printf("Generated %s\n", path)
		}
	}

	fmt.Println("Successfully pulled rules for", target)
	return nil
}
