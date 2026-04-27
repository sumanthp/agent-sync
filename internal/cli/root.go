package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

type Config struct {
	Remotes []string `json:"remotes"`
}

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
	case "remote":
		return handleRemote()
	case "sync":
		return handleSync()
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
	fmt.Println("agentsync-vcs - Universal Agent VCS")
	fmt.Println("\nUsage:")
	fmt.Println("  agentsync-vcs <command> [arguments]")
	fmt.Println("\nCommands:")
	fmt.Println("  init          Initialize a new agentsync-vcs project")
	fmt.Println("  remote add <url>  Add a remote Git repository for rules")
	fmt.Println("  pull <target> Pull and compile rules for a specific tool")
	fmt.Println("  sync          Sync rules from all remotes and compile")
	fmt.Println("  help          Show this help message")
}

func handleInit() error {
	content := `---
name: sample-rule
description: A sample rule for agentsync-vcs
globs: ["**/*.js"]
---
- Use clean code principles.
- Add comments to complex logic.
`
	err := os.WriteFile("sample-rule.md", []byte(content), 0644)
	if err != nil {
		return err
	}
	
	// Create config file
	config := Config{Remotes: []string{}}
	configData, _ := json.MarshalIndent(config, "", "  ")
	err = os.MkdirAll(".agent-sync", 0755)
	if err == nil {
		os.WriteFile(".agent-sync/config.json", configData, 0644)
	}

	fmt.Println("Initialized agentsync-vcs project with sample-rule.md and .agent-sync/config.json")
	return nil
}

func handleRemote() error {
	if len(os.Args) < 4 || os.Args[2] != "add" {
		fmt.Println("Usage: agentsync-vcs remote add <url>")
		return nil
	}
	url := os.Args[3]

	config, err := loadConfig()
	if err != nil {
		config = &Config{}
	}

	for _, r := range config.Remotes {
		if r == url {
			fmt.Println("Remote already exists.")
			return nil
		}
	}

	config.Remotes = append(config.Remotes, url)
	err = saveConfig(config)
	if err != nil {
		return err
	}

	fmt.Printf("Added remote: %s\n", url)
	return nil
}

func handleSync() error {
	config, err := loadConfig()
	if err != nil || len(config.Remotes) == 0 {
		fmt.Println("No remotes configured. Use 'agentsync-vcs remote add <url>' first.")
		return nil
	}

	for _, url := range config.Remotes {
		fmt.Printf("Syncing from %s...\n", url)
		err := syncRemote(url)
		if err != nil {
			fmt.Printf("Failed to sync %s: %v\n", url, err)
		}
	}
	return nil
}

func handlePull() error {
	if len(os.Args) < 3 {
		return fmt.Errorf("usage: agentsync-vcs pull <target>")
	}
	target := os.Args[2]

	// 1. Discover local .md files
	files, _ := filepath.Glob("*.md")

	// 2. Discover cached remote .md files
	cacheDir := getCacheDir()
	remoteFiles := []string{}
	filepath.Walk(cacheDir, func(path string, info os.FileInfo, err error) error {
		if err == nil && !info.IsDir() && strings.HasSuffix(path, ".md") {
			remoteFiles = append(remoteFiles, path)
		}
		return nil
	})

	allFiles := append(files, remoteFiles...)
	if len(allFiles) == 0 {
		fmt.Println("No markdown rules found locally or in cache.")
		return nil
	}

	// 3. Call Python compiler
	args := append([]string{"-m", "agentsync_vcs.main", target}, allFiles...)
	cmd := exec.Command("python", args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("python compiler failed: %v\nOutput: %s", err, string(output))
	}

	// 4. Parse and write
	var result map[string]string
	err = json.Unmarshal(output, &result)
	if err != nil {
		return fmt.Errorf("failed to parse compiler output: %v\nRaw output: %s", err, string(output))
	}

	for path, content := range result {
		dir := filepath.Dir(path)
		if dir != "." {
			os.MkdirAll(dir, 0755)
		}
		os.WriteFile(path, []byte(content), 0644)
		fmt.Printf("Generated %s\n", path)
	}

	fmt.Println("Successfully pulled rules for", target)
	return nil
}

func loadConfig() (*Config, error) {
	data, err := os.ReadFile(".agent-sync/config.json")
	if err != nil {
		return nil, err
	}
	var config Config
	err = json.Unmarshal(data, &config)
	return &config, err
}

func saveConfig(config *Config) error {
	os.MkdirAll(".agent-sync", 0755)
	data, err := json.MarshalIndent(config, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(".agent-sync/config.json", data, 0644)
}

func getCacheDir() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".agent-sync", "cache")
}

func syncRemote(url string) error {
	cacheDir := getCacheDir()
	os.MkdirAll(cacheDir, 0755)

	// Create a unique folder name for the remote
	safeName := strings.ReplaceAll(strings.ReplaceAll(url, "/", "_"), ":", "_")
	repoPath := filepath.Join(cacheDir, safeName)

	if _, err := os.Stat(repoPath); os.IsNotExist(err) {
		// Clone
		cmd := exec.Command("git", "clone", url, repoPath)
		return cmd.Run()
	} else {
		// Pull
		cmd := exec.Command("git", "-C", repoPath, "pull")
		return cmd.Run()
	}
}
