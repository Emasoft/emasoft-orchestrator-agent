#!/usr/bin/env python3
"""
Plugin Validator - Validate orchestrator-agent plugin structure

This script validates:
1. Plugin manifest (plugin.json) structure
2. Agent definitions
3. Command definitions
4. Skill structure
5. Hook configuration
6. Script references
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List


class ValidationResult:
    """Validation result tracker."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def error(self, msg: str) -> None:
        """Add error."""
        self.errors.append(f"❌ ERROR: {msg}")

    def warning(self, msg: str) -> None:
        """Add warning."""
        self.warnings.append(f"⚠️  WARNING: {msg}")

    def success(self, msg: str) -> None:
        """Add success."""
        self.passed.append(f"✓ {msg}")

    def print_results(self, verbose: bool = False) -> int:
        """Print validation results."""
        if verbose and self.passed:
            print("\n=== PASSED CHECKS ===")
            for msg in self.passed:
                print(msg)

        if self.warnings:
            print("\n=== WARNINGS ===")
            for msg in self.warnings:
                print(msg)

        if self.errors:
            print("\n=== ERRORS ===")
            for msg in self.errors:
                print(msg)

        # Summary
        print("\n=== SUMMARY ===")
        print(f"Passed: {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")

        # Exit code
        if self.errors:
            return 1
        elif self.warnings:
            return 2
        return 0


def validate_plugin(plugin_dir: Path, _verbose: bool = False) -> ValidationResult:
    """Validate plugin structure."""
    del _verbose  # Parameter kept for API compatibility
    result = ValidationResult()

    # Check plugin directory exists
    if not plugin_dir.exists():
        result.error(f"Plugin directory not found: {plugin_dir}")
        return result

    result.success(f"Plugin directory exists: {plugin_dir}")

    # Check plugin.json
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        result.error("plugin.json not found in .claude-plugin/")
        return result

    result.success("plugin.json exists")

    # Parse plugin.json
    try:
        with open(plugin_json, encoding="utf-8") as f:
            manifest = json.load(f)
        result.success("plugin.json is valid JSON")
    except json.JSONDecodeError as e:
        result.error(f"plugin.json is invalid JSON: {e}")
        return result

    # Validate required fields
    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if field not in manifest:
            result.error(f"plugin.json missing required field: {field}")
        else:
            result.success(f"plugin.json has {field}: {manifest[field]}")

    # Validate manifest schema — Claude Code rejects unknown keys
    known_manifest_fields = {
        "name", "version", "description", "author", "homepage",
        "repository", "license", "keywords", "commands", "agents",
        "skills", "hooks", "mcpServers", "outputStyles", "lspServers",
    }
    for key in manifest.keys():
        if key not in known_manifest_fields:
            result.error(
                f"Unrecognized manifest field '{key}' — Claude Code rejects "
                f"unknown keys and plugin installation will fail"
            )

    # Validate repository field type — must be string URL, not object
    if "repository" in manifest and not isinstance(manifest["repository"], str):
        result.error(
            "Field 'repository' must be a string URL, not an object. "
            "Use \"https://github.com/user/repo\" format."
        )

    # Check directories
    dirs_to_check = ["agents", "commands", "skills", "scripts", "hooks"]
    for dir_name in dirs_to_check:
        dir_path = plugin_dir / dir_name
        if dir_path.exists():
            result.success(f"{dir_name}/ directory exists")
        else:
            result.warning(f"{dir_name}/ directory not found")

    # Validate agents listed in manifest exist
    if "agents" in manifest:
        for agent_path in manifest["agents"]:
            # Remove leading ./ if present
            agent_path_clean = agent_path.lstrip("./")
            full_path = plugin_dir / agent_path_clean
            if full_path.exists():
                result.success(f"Agent file exists: {agent_path}")
            else:
                result.error(f"Agent file not found: {agent_path}")
    else:
        result.warning("No agents listed in plugin.json")

    # Check skills directory structure
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        result.success(f"Found {len(skill_dirs)} skill directories")

        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                result.success(f"Skill has SKILL.md: {skill_dir.name}")
            else:
                result.error(f"Skill missing SKILL.md: {skill_dir.name}")

    # Check commands have frontmatter
    commands_dir = plugin_dir / "commands"
    if commands_dir.exists():
        command_files = list(commands_dir.glob("*.md"))
        result.success(f"Found {len(command_files)} command files")

        for cmd_file in command_files:
            content = cmd_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                result.success(f"Command has frontmatter: {cmd_file.name}")
            else:
                result.error(f"Command missing frontmatter: {cmd_file.name}")

    # Check hooks.json
    hooks_json = plugin_dir / "hooks" / "hooks.json"
    if hooks_json.exists():
        try:
            with open(hooks_json, encoding="utf-8") as f:
                hooks_data = json.load(f)
            result.success("hooks.json is valid JSON")

            # Validate referenced scripts exist
            if "hooks" in hooks_data:
                for _, matchers in hooks_data["hooks"].items():
                    for matcher in matchers:
                        if "hooks" in matcher:
                            for hook in matcher["hooks"]:
                                if "command" in hook:
                                    cmd = hook["command"]
                                    # Replace variable and extract script path
                                    cmd = cmd.replace(
                                        "${CLAUDE_PLUGIN_ROOT}", str(plugin_dir)
                                    )
                                    # Skip interpreter (python3, bash, etc.) and get actual script
                                    parts = cmd.split()
                                    script_part = (
                                        parts[1]
                                        if len(parts) > 1
                                        and parts[0]
                                        in ("python3", "python", "bash", "sh")
                                        else parts[0]
                                    )
                                    # Handle -m module syntax
                                    if (
                                        parts[0] == "python3"
                                        and len(parts) > 1
                                        and parts[1] == "-m"
                                    ):
                                        result.success(
                                            f"Hook uses module: {parts[2] if len(parts) > 2 else 'unknown'}"
                                        )
                                        continue
                                    cmd_path = Path(script_part.split()[0])
                                    if cmd_path.exists():
                                        result.success(
                                            f"Hook script exists: {cmd_path.name}"
                                        )
                                    else:
                                        result.error(
                                            f"Hook script not found: {cmd_path}"
                                        )
        except json.JSONDecodeError as e:
            result.error(f"hooks.json is invalid JSON: {e}")
    else:
        result.warning("hooks.json not found")

    # Check scripts exist
    scripts_dir = plugin_dir / "scripts"
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py"))
        result.success(f"Found {len(scripts)} Python scripts")

        # Check scripts are executable
        for script in scripts:
            content = script.read_text(encoding="utf-8")
            if not content.startswith("#!/usr/bin/env python3"):
                result.warning(f"Script missing shebang: {script.name}")

    return result


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate orchestrator-agent plugin structure"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all passed checks",
    )
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        help="Path to plugin directory (default: current directory's parent)",
    )

    args = parser.parse_args()

    # Determine plugin directory
    if args.plugin_dir:
        plugin_dir = args.plugin_dir
    else:
        # Assume we're running from scripts/ directory
        plugin_dir = Path(__file__).parent.parent

    print(f"Validating plugin: {plugin_dir}")
    print("=" * 60)

    result = validate_plugin(plugin_dir, args.verbose)
    exit_code = result.print_results(args.verbose)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
