# SuperClaude Context Architecture Guide

## Overview

This guide documents how SuperClaude's Context-Oriented Configuration Framework is structured and how Claude Code interprets these context files to modify its behavior.

**Important**: SuperClaude is NOT standalone software with running processes, execution layers, or performance systems. It is a collection of `.md` instruction files that Claude Code reads to adopt specialized behaviors.

## Table of Contents

1. [Context File Architecture](#context-file-architecture)
2. [The Import System](#the-import-system)
3. [Agent Context Structure](#agent-context-structure)
4. [Command Context Structure](#command-context-structure)
5. [Mode Context Structure](#mode-context-structure)
6. [MCP Server Configuration](#mcp-server-configuration)
7. [How Claude Code Reads Context](#how-claude-code-reads-context)
8. [Extending the Framework](#extending-the-framework)

## Context File Architecture

### Directory Structure

```
~/.claude/                          # Claude Code's configuration directory
├── CLAUDE.md                       # Main context file with imports
├── FLAGS.md                        # Flag definitions and triggers
├── RULES.md                        # Core behavioral rules
├── PRINCIPLES.md                   # Guiding principles
├── agents/                         # Domain specialist contexts
│   ├── backend-architect.md       # Backend expertise
│   ├── frontend-architect.md      # Frontend expertise
│   ├── security-engineer.md       # Security expertise
│   ├── python-expert.md           # Python expertise
│   └── ... (13 total agents)
├── commands/                       # Workflow pattern contexts
│   ├── implement.md                # Implementation patterns
│   ├── analyze.md                  # Analysis patterns
│   ├── brainstorm.md              # Discovery patterns
│   └── ... (21 total commands)
└── modes/                          # Behavioral modification contexts
    ├── MODE_Brainstorming.md      # Collaborative discovery
    ├── MODE_Introspection.md      # Transparent reasoning
    ├── MODE_Task_Management.md    # Task orchestration
    └── ... (6 total modes)
```

### Context File Types

| File Type | Purpose | Activation | Example |
|-----------|---------|------------|---------|
| **Commands** | Define workflow patterns | `/sc:[command]` (context trigger) | User types `/sc:implement` → reads `implement.md` |
| **Agents** | Provide domain expertise | `@agents-[name]` or auto | `@agents-security` → reads `security-engineer.md` |
| **Modes** | Modify interaction style | Flags or triggers | `--brainstorm` → activates brainstorming mode |
| **Core** | Set fundamental rules | Always active | `RULES.md` always loaded |

## The Import System

### How CLAUDE.md Works

The main `CLAUDE.md` file uses an import system to load multiple context files:

```markdown
# CLAUDE.md structure
@import commands/*.md      # Loads all command patterns
@import agents/*.md        # Loads all agent contexts
@import modes/*.md         # Loads all behavioral modes
@import FLAGS.md           # Loads flag definitions
@import RULES.md           # Loads core rules
@import PRINCIPLES.md      # Loads guiding principles
```

### Import Processing

1. Claude Code reads `CLAUDE.md`
2. Encounters `@import` statements
3. Loads referenced files into context
4. Builds complete behavioral framework
5. Applies relevant contexts based on user input

## Agent Context Structure

### Anatomy of an Agent File

Each agent `.md` file follows this structure:

```markdown
---
name: agent-name
description: Brief description
category: specialized|architecture|quality
tools: Read, Write, Edit, Bash, Grep
---

# Agent Name

## Triggers
- Keywords that activate this agent
- File types that trigger activation
- Complexity thresholds

## Behavioral Mindset
Core philosophy and approach

## Focus Areas
- Domain expertise area 1
- Domain expertise area 2

## Key Actions
1. Specific behavior pattern
2. Problem-solving approach
```

### Agent Activation Logic

- **Manual**: User types `@agents-python-expert "task"`
- **Automatic**: Keywords in request trigger agent loading
- **Contextual**: File types or patterns activate relevant agents

## Command Context Structure

### Anatomy of a Command File

```markdown
---
name: command-name
description: Command purpose
category: utility|orchestration|analysis
complexity: basic|enhanced|advanced
mcp-servers: [context7, sequential]
personas: [architect, engineer]
---

# /sc:command-name

## Triggers
- When to use this command
- Context indicators

## Usage
/sc:command-name [target] [--options]

## Workflow Pattern
1. Step 1: Initial action
2. Step 2: Processing
3. Step 3: Validation

## Examples
Practical usage examples
```

### Command Processing

When user types `/sc:implement "feature"` in Claude Code conversation:
1. Claude reads `commands/implement.md`
2. Adopts implementation workflow pattern
3. May auto-activate related agents
4. Follows defined workflow steps

## Mode Context Structure

### Behavioral Modes

Modes modify Claude's interaction style:

```markdown
# MODE_[Name].md

## Activation Triggers
- Flag: --mode-name
- Keywords: [triggers]
- Complexity: threshold

## Behavioral Modifications
- Communication style changes
- Decision-making adjustments
- Output format modifications

## Interaction Patterns
- How to respond
- What to prioritize
```

## MCP Server Configuration

### Configuration Location

MCP servers are configured in `~/.claude.json` (NOT part of SuperClaude context):

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "sequential-thinking-mcp@latest"]
    }
  }
}
```

### MCP Integration

- **MCP Servers**: Actual software providing tools
- **SuperClaude**: Context that tells Claude when to use them
- **Activation**: Flags or keywords trigger MCP usage

## How Claude Code Reads Context

### Context Loading Sequence

```
User Input (in Claude Code): "/sc:analyze src/ --focus security"
                    ↓
1. Parse Command: identify 'analyze' command
                    ↓
2. Load Context: read commands/analyze.md
                    ↓
3. Check Flags: --focus security
                    ↓
4. Auto-Activation: load security-engineer.md
                    ↓
5. Apply Patterns: follow analysis workflow
                    ↓
6. Generate Output: using loaded contexts
```

### Context Priority

1. **Explicit Commands**: `/sc:` commands take precedence
2. **Manual Agents**: `@agents-` override auto-activation
3. **Flags**: Modify behavior of commands/agents
4. **Auto-Activation**: Based on keywords/context
5. **Default Behavior**: Standard Claude Code

## Extending the Framework

### Adding New Commands

1. Create `~/.claude/commands/new-command.md`
2. Define metadata, triggers, and workflow
3. No code changes needed - just context

### Adding New Agents

1. Create `~/.claude/agents/new-specialist.md`
2. Define expertise, triggers, and behaviors
3. Agent available immediately

### Adding New Modes

1. Create `~/.claude/modes/MODE_NewMode.md`
2. Define activation triggers and modifications
3. Mode activates based on triggers

### Best Practices

- **Keep Context Focused**: One concept per file
- **Clear Triggers**: Define when context activates
- **Workflow Patterns**: Provide step-by-step guidance
- **Examples**: Include practical usage examples
- **Metadata**: Use frontmatter for configuration

## Important Clarifications

### What SuperClaude Is NOT

- ❌ **No Execution Engine**: No code runs, no processes execute
- ❌ **No Performance System**: No optimization possible (it's just text)
- ❌ **No Detection Engine**: Claude Code does pattern matching
- ❌ **No Orchestration Layer**: Context files guide, not control
- ❌ **No Quality Gates**: Just instructional patterns

### What SuperClaude IS

- ✅ **Context Files**: `.md` instructions for Claude Code
- ✅ **Behavioral Patterns**: Workflows and approaches
- ✅ **Domain Expertise**: Specialized knowledge contexts
- ✅ **Configuration**: Settings for actual tools (MCP)
- ✅ **Framework**: Structured prompt engineering

## Summary

SuperClaude's architecture is intentionally simple: it's a well-organized collection of context files that Claude Code reads to modify its behavior. The power comes from the careful crafting of these contexts and their systematic organization, not from any executing code or running processes.

The framework's elegance lies in its simplicity - by providing Claude Code with structured instructions through context files, we can achieve sophisticated behavioral modifications without any software complexity.