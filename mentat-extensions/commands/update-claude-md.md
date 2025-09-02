# Command: /mentat:update-claude-md

> "Updating CLAUDE.md with current Mentat components"

## Command Metadata

- **Trigger**: `/mentat:update-claude-md`
- **Description**: Update ~/.claude/CLAUDE.md with current Mentat components
- **Category**: Maintenance
- **Requires**: Mentat installed
- **Time Estimate**: 1-2 seconds

## Purpose

Updates the Mentat section in your personal ~/.claude/CLAUDE.md file to reflect currently installed components. Use this after adding new features or commands to Mentat.

## Workflow

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add the setup module to path
sys.path.insert(0, str(Path.home() / ".claude" / "setup"))

try:
    from setup.utils.claude_config import ClaudeConfigManager
    from setup.utils.logger import get_logger
    
    logger = get_logger()
    manager = ClaudeConfigManager()
    
    logger.info("Scanning for installed Mentat components...")
    
    # Update the CLAUDE.md file
    if manager.update_claude_md():
        logger.success("Successfully updated CLAUDE.md with current components")
        
        # Show what was found
        commands = manager._scan_commands()
        agents = manager._scan_agents()
        scripts = manager._scan_scripts()
        
        print(f"\n📊 Component Summary:")
        print(f"   Commands: {len(commands)}")
        print(f"   Agents: {len(agents)}")
        print(f"   Scripts: {len(scripts)}")
        
        if commands:
            print("\n📜 Commands:")
            for cmd in commands:
                print(f"   • {cmd['name']}")
        
        if agents:
            print("\n🤖 Agents:")
            for agent in agents:
                print(f"   • {agent['name']}")
        
        if scripts:
            print("\n🔧 Scripts:")
            for script in scripts:
                print(f"   • {script['name']}")
        
        print(f"\n✅ CLAUDE.md updated at: ~/.claude/CLAUDE.md")
    else:
        logger.error("Failed to update CLAUDE.md")
        logger.info("You may need to manually update ~/.claude/CLAUDE.md")
        
except ImportError as e:
    print(f"❌ Error: Required modules not found: {e}")
    print("Make sure Mentat is properly installed")
except Exception as e:
    print(f"❌ Error updating CLAUDE.md: {e}")
```

## Examples

### Update after adding a new command
```bash
# After creating a new command in mentat-extensions/commands/
/mentat:update-claude-md

# Output:
# Scanning for installed Mentat components...
# ✅ Successfully updated CLAUDE.md with current components
# 
# 📊 Component Summary:
#    Commands: 6
#    Agents: 2
#    Scripts: 5
```

### Update after installing new features
```bash
# After running mentat install with new features
/mentat:update-claude-md

# Shows all currently installed components
```

## Success Output

```
╔════════════════════════════════════════╗
║     CLAUDE.MD UPDATE COMPLETE          ║
╠════════════════════════════════════════╣
║ 📊 Components Found:                   ║
║   • Commands: 6                        ║
║   • Agents: 2                          ║
║   • Scripts: 5                         ║
║                                        ║
║ ✅ Updated: ~/.claude/CLAUDE.md         ║
╚════════════════════════════════════════╝
```

## Integration

This command integrates with:
- **ClaudeConfigManager**: Scans and updates the CLAUDE.md
- **Installation system**: Reflects actual installed components
- **Extension workflow**: Use after adding new features

## Notes

- Automatically called during `mentat install`
- Safe to run multiple times
- Preserves other sections in CLAUDE.md
- Only updates the Mentat Framework Components section