# SuperClaude v4 Beta 🚀
[![Website Preview](https://img.shields.io/badge/Visit-Website-blue?logo=google-chrome)](https://superclaude-org.github.io/SuperClaude_Website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/SuperClaude.svg)](https://pypi.org/project/SuperClaude/)
[![Version](https://img.shields.io/badge/version-4.0.0--beta.1-blue.svg)](https://github.com/SuperClaude-Org/SuperClaude_Framework)
[![GitHub issues](https://img.shields.io/github/issues/SuperClaude-Org/SuperClaude_Framework)](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/CONTRIBUTING.md)
[![Contributors](https://img.shields.io/github/contributors/SuperClaude-Org/SuperClaude_Framework)](https://github.com/SuperClaude-Org/SuperClaude_Framework/graphs/contributors)
[![Website](https://img.shields.io/website?url=https://superclaude-org.github.io/SuperClaude_Website/)](https://superclaude-org.github.io/SuperClaude_Website/)

An intelligent framework that transforms Claude Code into a comprehensive development environment with specialized agents, behavioral modes, and advanced MCP integration.

**📢 Status**: V4 Beta is here! Major architecture overhaul with new behavioral modes, session lifecycle, and comprehensive agent system.

## What is SuperClaude V4? 🤔

SuperClaude V4 represents a complete evolution of the development framework, now featuring:
- 🛠️ **21 specialized commands** for comprehensive development workflows
- 🤖 **13 specialized agents** with domain expertise and intelligent routing
- 🧠 **4 Behavioral Modes** for different types of work (Brainstorming, Introspection, Task Management, Token Efficiency)
- 🔧 **6 MCP servers** including the powerful new Morphllm and Serena agents
- 💾 **Session Lifecycle** with persistent context via /sc:load and /sc:save
- 🎣 **Hooks System** for extensibility and customization
- ⚡ **SuperClaude-Lite** for lightweight usage

This is a complete rethink of how AI-assisted development should work - more intelligent, more capable, and more adaptable to your workflow! 🎯

## Current Status 📊

✅ **What's New in V4:**
- Complete architecture redesign with behavioral modes
- Session persistence with intelligent context management
- 13 specialized agents replacing the old persona system
- Advanced MCP integration with Morphllm and Serena
- Hooks system for extensibility (now implemented!)
- SuperClaude-Lite for resource-constrained environments

✅ **What's Working Well:**
- All 21 commands with enhanced capabilities
- Full MCP server integration suite
- Session lifecycle with /sc:load and /sc:save
- Behavioral modes with automatic activation
- Intelligent agent routing and coordination

⚠️ **Beta Limitations:**
- Some advanced features still being refined
- Documentation being updated for new features
- Performance optimizations ongoing

## Key Features ✨

### 21 Specialized Commands 🛠️
Enhanced command suite for comprehensive development workflows:

**Development**: `/sc:implement`, `/sc:build`, `/sc:design`  
**Analysis**: `/sc:analyze`, `/sc:troubleshoot`, `/sc:explain`  
**Quality**: `/sc:improve`, `/sc:test`, `/sc:cleanup`  
**Session**: `/sc:load`, `/sc:save`, `/sc:brainstorm`, `/sc:reflect`  
**Workflow**: `/sc:task`, `/sc:spawn`, `/sc:workflow`, `/sc:select-tool`  
**Others**: `/sc:document`, `/sc:git`, `/sc:estimate`, `/sc:index`

### 13 Specialized Agents 🤖
AI specialists with deep domain expertise and intelligent coordination:
- 🏗️ **architect** - System design and architecture
- 🎨 **frontend** - UI/UX and modern frontend development
- ⚙️ **backend** - APIs, infrastructure, and server-side logic
- 🔍 **analyzer** - Debugging and system analysis
- 🛡️ **security** - Security assessment and vulnerability analysis
- ✍️ **scribe** - Technical documentation and writing
- ⚡ **performance** - Optimization and performance engineering
- 🧪 **qa** - Quality assurance and testing strategies
- 📊 **data** - Data analysis and processing
- 🤖 **devops** - Infrastructure and deployment automation
- 🔧 **sre** - Site reliability and system operations
- 💼 **product** - Product strategy and requirements
- 🎯 **specialist** - Adaptive expertise for unique domains

*These agents feature intelligent routing, context awareness, and collaborative problem-solving capabilities.*

### 4 Behavioral Modes 🧠
Revolutionary behavioral system that adapts SuperClaude's approach:

#### Brainstorming Mode
- **Purpose**: Interactive requirements discovery and ideation
- **Triggers**: Ambiguous requests, exploration keywords, uncertainty indicators
- **Features**: Socratic dialogue, collaborative discovery, automated brief generation

#### Introspection Mode  
- **Purpose**: Meta-cognitive analysis and framework troubleshooting
- **Triggers**: Self-analysis requests, complex problem solving, error recovery
- **Features**: Reasoning analysis, decision validation, pattern recognition

#### Task Management Mode
- **Purpose**: Multi-layer orchestration with wave systems and delegation
- **Triggers**: Multi-step operations, complex builds, system-wide changes
- **Features**: Wave orchestration, sub-agent delegation, performance analytics

#### Token Efficiency Mode
- **Purpose**: Intelligent optimization with symbol systems and compression
- **Triggers**: Resource constraints, large contexts, performance needs
- **Features**: 30-50% token reduction, quality preservation, adaptive compression

### 6 MCP Server Integration 🔧
Comprehensive external tool ecosystem:
- **Context7** - Official library documentation and patterns
- **Sequential** - Multi-step analysis and complex reasoning
- **Magic** - Modern UI component generation
- **Playwright** - Browser automation and E2E testing
- **Morphllm** - Intelligent file editing with Fast Apply capability
- **Serena** - Semantic code analysis and project-wide operations

### Session Lifecycle System 💾
Persistent development context with intelligent management:
- **`/sc:load`** - Initialize projects with full context restoration
- **`/sc:save`** - Create checkpoints and preserve session state
- **Automatic Checkpoints** - Task completion, time-based, risk-based triggers
- **Cross-Session Learning** - Accumulated insights and pattern recognition

### Hooks System 🎣
Extensible architecture for customization:
- **Framework Coordinator** - Cross-component orchestration
- **Performance Monitor** - Real-time metrics and optimization
- **Quality Gates** - 8-step validation pipeline
- **Session Lifecycle** - Event-driven session management

### SuperClaude-Lite ⚡
Lightweight variant for resource-constrained environments:
- Streamlined feature set
- Reduced resource requirements
- Core functionality preservation
- Easy upgrade path to full SuperClaude

## ⚠️ Upgrading from v3? Important!

SuperClaude V4 is a major architectural upgrade. Clean installation recommended:

1. **Backup Important Data** - Save any custom configurations
2. **Clean Previous Installation**:
   ```bash
   python3 -m SuperClaude uninstall  # If available
   rm -rf ~/.claude/SuperClaude/
   rm -rf ~/.claude/shared/
   ```
3. **Install V4 Beta** - Follow installation instructions below

### 🔄 **Key Changes for v3 Users**
- **New Commands**: `/sc:brainstorm`, `/sc:reflect`, `/sc:save`, `/sc:select-tool`
- **Session Management**: Use `/sc:load` to initialize projects, `/sc:save` for persistence
- **Agent System**: Enhanced from personas to full agent coordination
- **Behavioral Modes**: Automatic activation based on context and needs

## Installation 📦

SuperClaude V4 Beta installation with enhanced capabilities:

### Step 1: Install the Package

**Option A: From PyPI (Recommended)**
```bash
uv add SuperClaude
```

**Option B: From Source**
```bash
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework.git
cd SuperClaude_Framework
uv sync
```

### 🔧 UV / UVX Setup Guide

SuperClaude V4 fully supports installation via [`uv`](https://github.com/astral-sh/uv) for optimal performance.

### 🌀 Install with `uv`

Make sure `uv` is installed:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

> Or follow instructions from: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

Once `uv` is available:

```bash
uv venv
source .venv/bin/activate
uv pip install SuperClaude
```

### ⚡ Install with `uvx` (Cross-platform CLI)

```bash
uvx pip install SuperClaude
```

### ✅ SuperClaude-Lite Installation

For lightweight usage:

```bash
python3 -m SuperClaude install --lite
```

---
**Missing Python?** Install Python 3.8+ first:
```bash
# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip

# macOS  
brew install python3

# Windows
# Download from https://python.org/downloads/
```

### Step 2: Run the V4 Installer

Enhanced installer with behavioral modes and session lifecycle:

```bash
# V4 Beta setup (recommended for most users)
python3 -m SuperClaude install

# Interactive selection with V4 features
python3 -m SuperClaude install --interactive

# Minimal install (core framework only)
python3 -m SuperClaude install --minimal

# Full developer setup (all V4 features)
python3 -m SuperClaude install --profile developer

# SuperClaude-Lite installation
python3 -m SuperClaude install --lite

# See all V4 options
python3 -m SuperClaude install --help
```

### Simple bash Command Usage 
```bash
# V4 Beta setup
SuperClaude install

# Interactive V4 installation
SuperClaude install --interactive

# Lightweight installation
SuperClaude install --lite

# Full V4 developer setup
SuperClaude install --profile developer
```

**That's it! 🎉** The V4 installer configures everything: behavioral modes, MCP servers, session lifecycle, and hooks system.

## How V4 Works 🔄

SuperClaude V4 transforms Claude Code through intelligent architecture:

1. **Behavioral Modes** - Adaptive behavior based on context and task requirements
2. **Agent Coordination** - 13 specialized agents with intelligent routing and collaboration
3. **Session Lifecycle** - Persistent context with /sc:load and /sc:save commands
4. **MCP Integration** - 6 powerful servers for extended capabilities
5. **Hooks System** - Extensible architecture for customization and monitoring
6. **Quality Gates** - 8-step validation pipeline ensuring excellence

The system intelligently adapts to your workflow, automatically activating appropriate modes and agents. 🧠

## V4 Architecture Highlights 🏗️

### Behavioral Intelligence
- **Automatic Mode Detection** - Context-aware behavioral adaptation
- **Cross-Mode Coordination** - Seamless integration between behavioral patterns
- **Progressive Enhancement** - Capabilities scale with complexity

### Agent Orchestration
- **Intelligent Routing** - Smart agent selection based on domain expertise
- **Collaborative Problem-Solving** - Multi-agent coordination for complex tasks
- **Context Preservation** - Agents maintain awareness across interactions

### Session Management
- **Persistent Context** - Full project state preservation across sessions
- **Intelligent Checkpointing** - Automatic saves based on risk and completion
- **Cross-Session Learning** - Accumulated insights and pattern recognition

## Configuration ⚙️

V4 configuration with enhanced behavioral controls:
- `~/.claude/settings.json` - Main V4 configuration with modes and agents
- `~/.claude/*.md` - Behavioral mode configurations
- `~/.claude/agents/` - Agent-specific customizations
- `~/.serena/` - Session lifecycle and memory management

Most users can use defaults - V4 intelligently adapts to your workflow! 🎛️

## Documentation 📖

Comprehensive V4 guides and documentation:

- 📚 [**V4 User Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/superclaude-user-guide.md) - Complete V4 overview and getting started
- 🛠️ [**Commands Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/commands-guide.md) - All 21 commands with V4 enhancements
- 🧠 [**Behavioral Modes Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/behavioral-modes-guide.md) - Understanding the 4 behavioral modes
- 🤖 [**Agent System Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/agent-system-guide.md) - Working with 13 specialized agents
- 💾 [**Session Lifecycle Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/session-lifecycle-guide.md) - /sc:load and /sc:save workflows
- 🎣 [**Hooks System Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/hooks-guide.md) - Extending and customizing V4
- 🏳️ [**Flags Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/flags-guide.md) - V4 command flags and behavioral controls
- 📦 [**Installation Guide**](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/Docs/installation-guide.md) - Detailed V4 installation and setup

## Contributing 🤝

V4 opens new contribution opportunities:
- 🐛 **Bug Reports** - Help us refine the beta
- 📝 **Documentation** - V4 features need clear explanation
- 🧪 **Testing** - Beta testing across different environments
- 🎣 **Hooks Development** - Extend the hooks system
- 🤖 **Agent Enhancement** - Improve specialized agent capabilities
- 🧠 **Behavioral Modes** - Contribute to mode intelligence

The V4 architecture is modular and extensible - many ways to contribute!

## Project Structure 📁

```
SuperClaude/
├── setup.py                    # PyPI setup for V4
├── SuperClaude/                # V4 Framework files  
│   ├── Core/                   # Behavioral mode documentation
│   ├── Commands/               # 21 specialized command definitions
│   ├── Agents/                 # 13 agent specifications
│   ├── Modes/                  # 4 behavioral mode configurations
│   ├── MCP/                    # 6 MCP server integrations
│   ├── Hooks/                  # Extensible hooks system
│   └── Config/                 # V4 configuration management
├── SuperClaude-Lite/           # Lightweight variant
├── setup/                      # V4 installation system
└── profiles/                   # Installation profiles with V4 features
```

## V4 Architecture Notes 🏗️

The V4beta architecture focuses on:
- **Behavioral Intelligence** - Context-aware adaptive behavior
- **Agent Orchestration** - Sophisticated multi-agent coordination
- **Session Persistence** - Continuous learning and context preservation
- **Extensibility** - Hooks system for customization and enhancement
- **Performance** - Token efficiency and resource optimization
- **Quality** - 8-step validation gates ensuring excellence

V4 represents a fundamental evolution in AI-assisted development frameworks.

## FAQ 🙋

**Q: What's new in V4 compared to V3?**  
A: Complete architecture overhaul with behavioral modes, session lifecycle, 13 agents, 6 MCP servers, and hooks system.

**Q: Is the hooks system back?**  
A: Yes! Completely redesigned and implemented with extensible architecture.

**Q: Should I upgrade from V3?**  
A: V4 beta offers significant improvements, but clean installation recommended for stability.

**Q: What is SuperClaude-Lite?**  
A: Lightweight variant with core functionality for resource-constrained environments.

**Q: How stable is V4 beta?**  
A: Core functionality is solid, with some advanced features still being refined. Great for development and testing!

## SuperClaude Contributors

[![Contributors](https://contrib.rocks/image?repo=SuperClaude-Org/SuperClaude_Framework)](https://github.com/SuperClaude-Org/SuperClaude_Framework/graphs/contributors)

## License

MIT - [See LICENSE file for details](https://opensource.org/licenses/MIT)

## Star History

<a href="https://www.star-history.com/#SuperClaude-Org/SuperClaude_Framework&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Date" />
 </picture>
</a>
---

*V4 Beta: The future of AI-assisted development is here. Experience intelligent, adaptive, and powerful development workflows! 🚀*

---