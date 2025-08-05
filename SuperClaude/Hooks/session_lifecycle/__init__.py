"""
Session Lifecycle Hook

High priority hook for automatic session management per SESSION_LIFECYCLE.md.
Handles session state transitions and automatic checkpoint creation.

Events: SessionStart, PostToolUse (time-based)
Responsibilities:
- Trigger /sc:load for new projects automatically
- Monitor for automatic checkpoint conditions
- Handle session state transitions
- Performance monitoring integration
"""