"""
Framework Coordinator Hook

Critical priority hook that provides central intelligence for SuperClaude framework coordination.
Enforces ORCHESTRATOR.md auto-activation rules and RULES.md compliance patterns automatically.

Events: PreToolUse, PostToolUse
Responsibilities:
- Parse ORCHESTRATOR.md auto-activation rules
- Analyze context and suggest MCP server activation
- Enforce RULES.md compliance patterns  
- Route based on complexity indicators
"""