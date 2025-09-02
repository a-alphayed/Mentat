"""
Claude configuration management for Mentat
Manages the Mentat section in ~/.claude/CLAUDE.md
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from ..utils.logger import get_logger


class ClaudeConfigManager:
    """Manages Mentat section in user's ~/.claude/CLAUDE.md file"""
    
    MENTAT_SECTION_START = "# ═══════════════════════════════════════════════════"
    MENTAT_SECTION_HEADER = "# Mentat Framework Components"
    MENTAT_SECTION_END = "# ═══════════════════════════════════════════════════"
    
    def __init__(self):
        self.logger = get_logger()
        self.claude_dir = Path.home() / ".claude"
        self.claude_md = self.claude_dir / "CLAUDE.md"
        
    def _generate_mentat_section(self) -> str:
        """Generate the Mentat section content based on current installation"""
        
        # Scan for installed components
        commands = self._scan_commands()
        agents = self._scan_agents()
        scripts = self._scan_scripts()
        
        section = f"""
{self.MENTAT_SECTION_START}
{self.MENTAT_SECTION_HEADER}
{self.MENTAT_SECTION_END}

# Mentat = Personal Claude Code customization framework
# Built on SuperClaude v4.0.8 | Add features as needed

# Mentat Commands (Extensible)
{self._format_commands(commands)}

# Mentat Agents
{self._format_agents(agents)}

# Mentat Configuration
# - Config: ~/.mentat/config.json (0600)
# - Dotfiles: ~/dotfiles/ (symlinked)
# - Lock: ~/.mentat/sync.lock (0700)
# - Logs: ~/.mentat/sync.log

# Mentat Security
# - SSH auth with passphrase protection
# - Input validation (emails, usernames, URLs)
# - Atomic permissions (0600 keys, 0700 dirs)
# - No credential storage
# - Sanitized commits

# Mentat Scripts
{self._format_scripts(scripts)}

# Component Count: Commands: {len(commands)} | Agents: {len(agents)} | Scripts: {len(scripts)}
"""
        return section
    
    def _scan_commands(self) -> List[Dict[str, str]]:
        """Scan for installed Mentat commands"""
        commands = []
        # Check both locations: direct commands and mentat subdirectory
        command_dirs = [
            Path.home() / ".claude" / "commands",
            Path.home() / ".claude" / "commands" / "mentat"
        ]
        
        for command_dir in command_dirs:
            if command_dir.exists():
                for cmd_file in command_dir.glob("*.md"):
                    # Check if it's a mentat command (either by prefix or location)
                    is_mentat = (cmd_file.stem.startswith("mentat-") or 
                                command_dir.name == "mentat")
                    
                    if is_mentat:
                        # Parse command file for description
                        if cmd_file.stem.startswith("mentat-"):
                            command_name = f"/mentat:{cmd_file.stem.replace('mentat-', '')}"
                        else:
                            command_name = f"/mentat:{cmd_file.stem}"
                        
                        description = self._get_command_description(cmd_file)
                        commands.append({
                            "name": command_name,
                            "desc": description,
                            "file": cmd_file.name
                        })
        
        return commands
    
    def _scan_agents(self) -> List[Dict[str, str]]:
        """Scan for installed Mentat agents"""
        agents = []
        agent_dir = Path.home() / ".claude" / "agents"
        
        if agent_dir.exists():
            # Look for Mentat category agents
            for agent_file in agent_dir.glob("*.md"):
                if self._is_mentat_agent(agent_file):
                    agent_name = f"@{agent_file.stem.replace('agent-', '')}"
                    description = self._get_agent_description(agent_file)
                    agents.append({
                        "name": agent_name,
                        "desc": description
                    })
        
        return agents
    
    def _scan_scripts(self) -> List[Dict[str, str]]:
        """Scan for installed Mentat scripts"""
        scripts = []
        script_dir = Path.home() / ".claude" / "scripts"
        
        if script_dir.exists():
            # Key Mentat scripts to track
            key_scripts = [
                ("sync-orchestrator.sh", "Core sync engine"),
                ("test-ssh.sh", "SSH diagnostics"),
                ("health-monitor.sh", "Repo health check"),
                ("conflict-resolver.sh", "Merge resolution"),
                ("version-bump.sh", "Semver management"),
            ]
            
            for script_name, description in key_scripts:
                script_path = script_dir / script_name
                if script_path.exists():
                    scripts.append({
                        "name": script_name,
                        "desc": description
                    })
        
        return scripts
    
    def _format_commands(self, commands: List[Dict[str, str]]) -> str:
        """Format commands for the section"""
        if not commands:
            return "# No Mentat commands installed"
        
        lines = []
        for cmd in commands:
            lines.append(f"{cmd['name']:<20} # {cmd['desc']}")
        return "\n".join(lines)
    
    def _format_agents(self, agents: List[Dict[str, str]]) -> str:
        """Format agents for the section"""
        if not agents:
            return "# No Mentat agents installed"
        
        lines = []
        for agent in agents:
            lines.append(f"{agent['name']:<20} # {agent['desc']}")
        return "\n".join(lines)
    
    def _format_scripts(self, scripts: List[Dict[str, str]]) -> str:
        """Format scripts for the section"""
        if not scripts:
            return "# No Mentat scripts installed"
        
        lines = []
        for script in scripts:
            lines.append(f"# - {script['name']:<25} # {script['desc']}")
        return "\n".join(lines)
    
    def _get_command_description(self, cmd_file: Path) -> str:
        """Extract description from command file"""
        try:
            with open(cmd_file, 'r') as f:
                lines = f.readlines()
                for line in lines[:10]:  # Check first 10 lines
                    if line.startswith("# Command:"):
                        # Next non-empty line is usually description
                        continue
                    if line.strip() and not line.startswith("#"):
                        return line.strip()[:50]  # Limit length
        except:
            pass
        return "Mentat command"
    
    def _get_agent_description(self, agent_file: Path) -> str:
        """Extract description from agent file"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
                # Look for description in YAML frontmatter
                if "description:" in content:
                    for line in content.split('\n'):
                        if line.strip().startswith("description:"):
                            desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                            return desc[:50]  # Limit length
        except:
            pass
        return "Mentat agent"
    
    def _is_mentat_agent(self, agent_file: Path) -> bool:
        """Check if agent belongs to Mentat category"""
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
                return "category: mentat" in content or "syncer" in agent_file.name or "mentat" in agent_file.name
        except:
            return False
    
    def _clean_duplicate_sections(self, content: str) -> str:
        """Remove duplicate Mentat sections from content"""
        # Find all Mentat sections - both proper and orphaned
        sections_to_remove = []
        
        # Pattern 1: Proper sections with header
        search_pos = 0
        start_pattern = self.MENTAT_SECTION_START + "\n" + self.MENTAT_SECTION_HEADER
        while True:
            idx = content.find(start_pattern, search_pos)
            if idx == -1:
                break
            sections_to_remove.append((idx, "proper"))
            search_pos = idx + 1
        
        # Pattern 2: Orphaned content blocks (starting with "# Mentat =" or "# Mentat Commands")
        orphan_patterns = [
            "\n# Mentat = Personal Claude Code customization framework",
            "\n# Mentat Commands (Dotfiles",
            "\n# Mentat Commands (Extensible)"
        ]
        
        for pattern in orphan_patterns:
            search_pos = 0
            while True:
                idx = content.find(pattern, search_pos)
                if idx == -1:
                    break
                # Check if this is part of a proper section already found
                is_part_of_proper = any(
                    start <= idx <= start + 500 
                    for start, type in sections_to_remove 
                    if type == "proper"
                )
                if not is_part_of_proper:
                    sections_to_remove.append((idx, "orphan"))
                search_pos = idx + 1
        
        # Sort by position
        sections_to_remove.sort()
        
        # If we have sections to remove (keeping none for fresh start)
        if sections_to_remove:
            self.logger.warning(f"Found {len(sections_to_remove)} Mentat section(s)/fragment(s), cleaning up...")
            
            # Remove all sections/fragments
            cleaned = content
            for start_idx, section_type in reversed(sections_to_remove):
                # Find end of this section/fragment
                component_count_idx = cleaned.find("# Component Count:", start_idx)
                if component_count_idx != -1:
                    end_idx = cleaned.find("\n", component_count_idx) + 1
                else:
                    # Look for next major section or divider
                    end_idx = len(cleaned)
                    search_start = start_idx + 50  # Skip current line
                    
                    # Possible end markers
                    end_markers = [
                        "\n\n# ═══════",  # Next section divider
                        "\n\n# SuperClaude",  # SuperClaude section
                        "\n\n# Core",  # Core framework
                        "\n# Mentat = Personal",  # Another orphan
                        "\n# Mentat Commands"  # Another orphan
                    ]
                    
                    for marker in end_markers:
                        idx = cleaned.find(marker, search_start)
                        if idx != -1 and idx < end_idx:
                            end_idx = idx
                
                # Remove this section/fragment
                cleaned = cleaned[:start_idx] + cleaned[end_idx:]
            
            # Clean up excessive blank lines
            while "\n\n\n\n" in cleaned:
                cleaned = cleaned.replace("\n\n\n\n", "\n\n\n")
            
            # Clean up orphaned dividers (dividers with no content between them)
            import re
            # Pattern: divider followed by optional whitespace and another divider
            divider_pattern = r'# ═══════════════════════════════════════════════════\n\s*\n*# ═══════════════════════════════════════════════════'
            while re.search(divider_pattern, cleaned):
                cleaned = re.sub(divider_pattern, '', cleaned)
            
            # Clean up lone dividers (divider with just whitespace before next section)
            lone_divider = r'\n# ═══════════════════════════════════════════════════\n\s*\n+(?=# ═══════)'
            cleaned = re.sub(lone_divider, '\n\n', cleaned)
            
            return cleaned
        
        return content
    
    def update_claude_md(self) -> bool:
        """Update or add Mentat section in ~/.claude/CLAUDE.md"""
        try:
            # Ensure directory exists
            self.claude_dir.mkdir(exist_ok=True)
            
            # Read existing content or create new
            if self.claude_md.exists():
                with open(self.claude_md, 'r') as f:
                    content = f.read()
            else:
                content = ""
            
            # Clean up any duplicate sections first
            content = self._clean_duplicate_sections(content)
            
            # Generate new Mentat section
            new_section = self._generate_mentat_section()
            
            # Check if Mentat section exists
            if self.MENTAT_SECTION_HEADER in content:
                # Replace existing section
                start_marker = self.MENTAT_SECTION_START + "\n" + self.MENTAT_SECTION_HEADER
                
                # Find start of Mentat section
                start_idx = content.find(start_marker)
                if start_idx != -1:
                    # Find end of section by looking for the Component Count line
                    # which marks the end of each Mentat section
                    component_count_idx = content.find("# Component Count:", start_idx)
                    if component_count_idx != -1:
                        # Find the newline after Component Count line
                        end_of_line = content.find("\n", component_count_idx)
                        if end_of_line != -1:
                            end_idx = end_of_line + 1
                        else:
                            end_idx = len(content)
                    else:
                        # Fallback: look for next non-Mentat section
                        # Skip the immediate closing divider by searching further
                        search_start = start_idx + len(start_marker) + 100  # Skip header block
                        next_section_markers = [
                            "\n\n# ═══════",  # Another major section with blank line
                            "\n\n# SuperClaude",  # SuperClaude section
                            "\n\n# Core Framework",  # Other framework sections
                        ]
                        
                        end_idx = len(content)
                        for marker in next_section_markers:
                            idx = content.find(marker, search_start)
                            if idx != -1 and idx < end_idx:
                                end_idx = idx
                    
                    # Replace the section
                    content = content[:start_idx] + new_section + content[end_idx:]
                    
                    self.logger.info("Updated existing Mentat section in CLAUDE.md")
                else:
                    # Section header exists but not properly formatted, append new
                    content += "\n" + new_section
                    self.logger.info("Added Mentat section to CLAUDE.md")
            else:
                # Add new section at the end
                if content and not content.endswith('\n'):
                    content += '\n'
                content += new_section
                self.logger.info("Added Mentat section to CLAUDE.md")
            
            # Write updated content
            with open(self.claude_md, 'w') as f:
                f.write(content)
            
            # Set appropriate permissions
            self.claude_md.chmod(0o644)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update CLAUDE.md: {e}")
            return False
    
    def remove_mentat_section(self) -> bool:
        """Remove Mentat section from ~/.claude/CLAUDE.md (for uninstall)"""
        try:
            if not self.claude_md.exists():
                return True
            
            with open(self.claude_md, 'r') as f:
                content = f.read()
            
            if self.MENTAT_SECTION_HEADER not in content:
                return True  # Already removed
            
            # Find and remove Mentat section
            start_marker = self.MENTAT_SECTION_START + "\n" + self.MENTAT_SECTION_HEADER
            start_idx = content.find(start_marker)
            
            if start_idx != -1:
                # Find end of section
                next_section_markers = [
                    "\n# ═══════",
                    "\n\n# ",
                ]
                
                end_idx = len(content)
                for marker in next_section_markers:
                    idx = content.find(marker, start_idx + len(start_marker))
                    if idx != -1 and idx < end_idx:
                        end_idx = idx
                
                # Remove the section
                content = content[:start_idx] + content[end_idx:]
                
                # Clean up extra newlines
                while "\n\n\n" in content:
                    content = content.replace("\n\n\n", "\n\n")
                
                # Write updated content
                with open(self.claude_md, 'w') as f:
                    f.write(content)
                
                self.logger.info("Removed Mentat section from CLAUDE.md")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove Mentat section: {e}")
            return False