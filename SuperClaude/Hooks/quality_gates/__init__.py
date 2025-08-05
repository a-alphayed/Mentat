"""
Quality Gates Hook

High priority hook for systematic enforcement of 8-step validation cycle.
Provides automatic quality validation after Write/Edit operations.

Events: PostToolUse (after Write/Edit operations)
Responsibilities:
- Trigger 8-step validation cycle automatically
- Monitor quality metrics and thresholds
- Provide evidence collection and documentation
- Integration with SuperClaude quality standards
"""