---
name: orch-claude-code-action-integration
description: Set up Claude Code in GitHub Actions for automated PR reviews, @claude mention responses, and issue triage.
agent: deploy-agent
context: fork
---

# Claude Code Action Integration

## When to Use This Skill

Use this skill when you need to:
- Set up automated PR reviews using Claude Code in GitHub Actions
- Configure Claude-powered issue triage automation
- Enable @claude mention responses in GitHub issues/PRs
- Integrate Claude Code into CI/CD pipelines

## Trigger Conditions

- User asks to "set up automated code review"
- User wants "Claude to review PRs automatically"
- User asks about "GitHub Actions with Claude"
- User needs "@claude mention integration"
- User wants "automated issue triage"

---

## Overview

The `claude-code-action` is Anthropic's official GitHub Action for running Claude Code in CI/CD workflows. This skill provides ready-to-use workflow templates for common integration patterns.

## Available Templates

| Template | Purpose | Location |
|----------|---------|----------|
| **claude-pr-review.yml** | Automatic PR code review | `templates/workflows/` |
| **claude-mention.yml** | @claude mention responses | `templates/workflows/` |
| **claude-issue-triage.yml** | Automated issue triage | `templates/workflows/` |

---

## Quick Start

### Step 1: Choose a Template

Select the workflow template that matches your use case from `templates/workflows/`.

### Step 2: Copy to Repository

Copy the YAML file to your repository's `.github/workflows/` directory:

```bash
# Example: Set up PR review
cp claude-pr-review.yml /path/to/repo/.github/workflows/
```

### Step 3: Configure Secrets

Add required secrets in your repository settings:

1. Go to **Settings > Secrets and variables > Actions**
2. Add `ANTHROPIC_API_KEY` with your Anthropic API key

### Step 4: Configure Permissions

1. Go to **Settings > Actions > General**
2. Under "Workflow permissions", select "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"

---

## Template Details

### PR Review Workflow

**File**: `templates/workflows/claude-pr-review.yml`

**Triggers**:
- Pull request opened
- New commits pushed to PR
- PR marked ready for review
- PR reopened

**Features**:
- Comprehensive code review (quality, bugs, security, performance)
- Inline comments on specific code issues
- Summary comment with overall assessment
- Concurrency control (one review per PR at a time)
- Draft PR handling (skips drafts)

**Review Categories**:
1. Code Quality - patterns, naming, organization, DRY
2. Potential Bugs - null handling, edge cases, race conditions
3. Security - injection, XSS, auth issues
4. Performance - complexity, queries, caching
5. Testing - coverage, edge cases, clarity

### Mention Response Workflow

**File**: `templates/workflows/claude-mention.yml`

**Triggers**:
- @claude mentioned in issue comment
- @claude mentioned in PR comment

**Features**:
- Responds to direct questions
- Provides code explanations
- Suggests fixes for reported issues
- Answers architecture questions

### Issue Triage Workflow

**File**: `templates/workflows/claude-issue-triage.yml`

**Triggers**:
- New issue opened

**Features**:
- Automatic label assignment
- Priority assessment
- Initial response to reporter
- Related issue linking

---

## Customization

### Changing the Model

Edit the `claude_args` section in any workflow:

```yaml
claude_args: |
  --model "claude-sonnet-4-20250514"  # or claude-opus-4-5-20251101
```

### Restricting Tools

Modify the `--allowedTools` argument to limit what Claude can do:

```yaml
--allowedTools "Read,Glob,Grep"  # Read-only, no bash
```

### Custom Prompts

Edit the `prompt` section to customize Claude's behavior for your project's specific needs.

---

## Troubleshooting

### Workflow Not Triggering

1. Check workflow file is in `.github/workflows/`
2. Verify YAML syntax is valid
3. Ensure trigger conditions match your action

### Authentication Errors

1. Verify `ANTHROPIC_API_KEY` secret is set
2. Check API key has not expired
3. Ensure key has required permissions

### Permission Denied Errors

1. Enable "Read and write permissions" in repository settings
2. Add required permissions block to workflow

### Timeout Issues

1. Increase `timeout-minutes` in workflow
2. Consider using a faster model for large repos

---

## References

- [claude-code-action GitHub](https://github.com/anthropics/claude-code-action)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## Best Practices

1. **Start with PR Review** - Most common and valuable integration
2. **Use Sonnet for Speed** - Faster reviews, lower cost
3. **Limit Tools** - Only allow necessary tools for security
4. **Test on Draft PRs** - Test workflow before enabling widely
5. **Monitor Costs** - Watch API usage with track_progress enabled
