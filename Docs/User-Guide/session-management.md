# SuperClaude Session Management Guide

## ✅ Important Note
Sessions are conversation-scoped, not persistent between Claude Code conversations.

## Understanding Session Context

### What "Sessions" Actually Are

**Reality Check**: Claude Code conversations are independent. Each new conversation starts fresh. "Session management" in SuperClaude refers to commands that help Claude understand and work with your project context during a single conversation.

### What /sc:load and /sc:save Actually Do

- **`/sc:load`**: Tells Claude to analyze and understand a project structure within the current conversation
- **`/sc:save`**: Creates a summary or checkpoint of work done in the current conversation
- **`/sc:reflect`**: Reviews what has been discussed/done in the current conversation

**Important**: These commands DO NOT persist data between Claude Code conversations. Each conversation is isolated.

## How Context Works in Claude Code

### Within a Conversation

During a single Claude Code conversation:
- Claude maintains context of what you've discussed
- Can refer back to earlier parts of the conversation
- Understands the project structure you've shown
- Remembers decisions made in this conversation

### Between Conversations

When you start a new Claude Code conversation:
- Previous conversation context is lost
- Must re-explain project context
- Previous decisions aren't remembered
- Must reload any necessary understanding

## Session Commands Explained

### /sc:load - Project Context Loading

**What it does**: Analyzes project structure and creates mental model
**What it doesn't do**: Store anything persistently

```bash
/sc:load src/
# Claude analyzes the src/ directory structure
# Builds understanding for THIS conversation only
```

**Use cases**:
- Starting work on an existing project
- Helping Claude understand codebase structure
- Establishing context for subsequent commands

### /sc:save - Conversation Summary

**What it does**: Creates a summary of work done
**What it doesn't do**: Actually save for next conversation

```bash
/sc:save "refactoring-complete"
# Claude summarizes what was accomplished
# Useful for you to copy/paste to notes
# Does NOT persist for next conversation
```

**Use cases**:
- Creating documentation of work done
- Generating summary for your records
- Checkpoint before major changes

### /sc:reflect - Conversation Review

**What it does**: Reviews current conversation progress
**What it doesn't do**: Access previous conversations

```bash
/sc:reflect
# Claude reviews what's been discussed
# Summarizes decisions and progress
# Only covers current conversation
```

**Use cases**:
- Mid-conversation status check
- Reviewing decisions made
- Planning next steps

## Working Effectively Without Persistence

### Starting New Conversations

When starting a new Claude Code conversation for continued work:

1. **Provide Context Again**
   ```bash
   /sc:load project-directory/
   # Re-establishes project understanding
   ```

2. **Summarize Previous Work**
   ```
   "We previously refactored the auth system. Now we need to..."
   ```

3. **Reference Key Decisions**
   ```
   "We're using JWT tokens with refresh tokens, as decided earlier"
   ```

### Creating Your Own Persistence

Since Claude doesn't persist between conversations, create your own:

1. **Project Notes File**
   ```markdown
   # project-notes.md
   
   ## Session 1 (Date)
   - Implemented user authentication
   - Decided on JWT with refresh tokens
   - Created user model with email validation
   
   ## Session 2 (Date)
   - Added password reset functionality
   - Integrated email service
   ```

2. **Copy Important Summaries**
   ```bash
   /sc:save "session-end"
   # Copy the output to your notes
   ```

3. **Document Key Decisions**
   ```bash
   /sc:reflect
   # Copy important decisions to your documentation
   ```

## MCP Servers and "Memory"

### Serena MCP Server

If Serena MCP is configured, it may provide some project analysis capabilities, but:
- Still doesn't persist between Claude conversations
- Operates within MCP server constraints
- Not true persistent memory

### What MCP Servers Can Do

- Provide tools for file analysis
- Help with project navigation
- Enhance Claude's capabilities
- But NOT store conversation history

## Best Practices

### For Single Conversation

1. **Load Context Early**
   ```bash
   /sc:load .
   # Start with full project context
   ```

2. **Work Systematically**
   ```bash
   /sc:workflow "plan the session"
   # Organize your work
   ```

3. **Save Summaries**
   ```bash
   /sc:save "checkpoint-1"
   # Create summaries as you go
   ```

### For Multiple Conversations

1. **Maintain External Notes**
   - Keep a project journal
   - Document decisions
   - Track progress

2. **Create Context Files**
   ```markdown
   # .claude-context.md
   Project context for Claude Code sessions
   - Architecture: microservices
   - Database: PostgreSQL
   - Auth: JWT with refresh tokens
   ```

3. **Start Consistently**
   ```bash
   # At start of each conversation:
   /sc:load .
   "Please read .claude-context.md for project decisions"
   ```

## Common Misconceptions

### ❌ Myth: Sessions Persist
**Reality**: Each Claude conversation is independent

### ❌ Myth: /sc:save Stores Data
**Reality**: It creates a summary for you to copy

### ❌ Myth: /sc:load Remembers Previous Work
**Reality**: It analyzes current files only

### ❌ Myth: Serena Provides Memory
**Reality**: MCP tools work within conversation scope

## Troubleshooting

### "Claude doesn't remember our previous conversation"
**Expected behavior**: Claude Code conversations don't persist
**Solution**: Provide context at start of new conversation

### "/sc:load isn't loading previous session"
**Expected behavior**: It loads project files, not session history
**Solution**: Maintain your own project notes

### "/sc:save doesn't actually save"
**Expected behavior**: Creates summary text only
**Solution**: Copy output to your own notes

## Summary

SuperClaude's "session management" commands are tools for managing context within a single Claude Code conversation. They help Claude understand your project and track progress during the current conversation, but do not provide persistence between conversations. 

For true continuity across multiple conversations, maintain your own documentation and provide context at the start of each new conversation. Think of these commands as conversation helpers, not database operations.