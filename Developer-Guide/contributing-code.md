# Contributing Code to SuperClaude Framework 🛠️

Welcome to SuperClaude Framework development! This guide provides everything you need to contribute to the meta-programming framework that transforms Claude Code into a structured development platform.

**Project Purpose**: SuperClaude enhances Claude Code through behavioral instruction injection, intelligent agent coordination, and MCP server integration. We're building the next generation of AI-assisted development tools.

**Community Approach**: Open collaboration focused on expanding capabilities, improving user experience, and maintaining high-quality code standards. Every contribution, from bug fixes to new features, helps advance AI-assisted development.

## 🚀 Development Setup

### Prerequisites

**Required:**
- Python 3.8+ with pip
- Git for version control
- Claude Code installed and working
- Node.js 16+ (for MCP server development)

**Recommended:**
- VS Code or PyCharm for development
- Docker for containerized testing
- 8GB RAM for full development environment
- 2GB disk space for repositories and dependencies

**System Check:**
```bash
# Verify prerequisites
python3 --version    # Should be 3.8+
node --version       # Should be 16+
git --version        # Any recent version
claude --version     # Verify Claude Code works
```

### Development Environment Setup

**1. Fork and Clone Repository:**
```bash
# Fork SuperClaude_Framework on GitHub first
git clone https://github.com/YOUR_USERNAME/SuperClaude_Framework.git
cd SuperClaude_Framework
```

**2. Set Up Python Environment:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# For Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

**3. Configure Development Environment:**
```bash
# Set up development configuration
export SUPERCLAUDE_DEV=true
export CLAUDE_CONFIG_DIR=./dev-config

# Create development configuration
mkdir -p dev-config
cp -r SuperClaude/Core/* dev-config/
```

**4. Verify Installation:**
```bash
# Test installation
python -m SuperClaude --version
python -m SuperClaude install --dry-run --install-dir ./dev-config

# Run tests
python -m pytest tests/
python scripts/validate_pypi_ready.py
```

**5. Development Tools Setup:**
```bash
# Install development tools
pip install black pylint mypy pre-commit

# Set up pre-commit hooks
pre-commit install

# Configure IDE (VS Code example)
cp .vscode/settings.json.template .vscode/settings.json
```

## 🏗️ Architecture Overview

### Core Components

**SuperClaude Framework Structure:**
```
SuperClaude_Framework/
├── SuperClaude/                 # Framework components
│   ├── Core/                   # Core behavioral instructions
│   │   ├── FLAGS.md            # Behavioral flags system
│   │   ├── RULES.md            # Development rules
│   │   └── PRINCIPLES.md       # Engineering principles
│   ├── Modes/                  # 6 behavioral modes
│   │   ├── MODE_Brainstorming.md
│   │   ├── MODE_Introspection.md
│   │   └── MODE_*.md
│   ├── MCP/                    # MCP server integrations
│   │   ├── MCP_Context7.md
│   │   ├── MCP_Sequential.md
│   │   └── configs/
│   ├── Commands/               # 21 slash commands
│   │   ├── brainstorm.md
│   │   └── *.md
│   └── Agents/                 # 13 specialized agents
├── setup/                      # Installation system
│   ├── components/             # Component definitions
│   ├── core/                   # Installation logic
│   ├── services/               # System services
│   └── utils/                  # Utilities
├── User-Guide/                 # User documentation
├── Developer-Guide/            # Technical documentation
├── Reference/                  # Reference materials
└── tests/                      # Test suite
```

**Key Architectural Concepts:**
- **Meta-Framework**: Enhances Claude Code through configuration injection
- **Component System**: Modular installation with dependency resolution
- **Behavioral Programming**: AI behavior modification through .md files
- **Intelligent Orchestration**: Dynamic coordination of agents and tools

### V4 Beta Architecture

#### Agents System

**13 Specialized AI Agents:**
- **Architecture**: system-architect, backend-architect, frontend-architect, devops-architect
- **Quality**: security-engineer, performance-engineer, quality-engineer, refactoring-expert
- **Analysis**: root-cause-analyst, requirements-analyst
- **Specialized**: python-expert, technical-writer, learning-guide

**Agent Development Pattern:**
```python
# setup/components/agents.py
class AgentComponent(BaseComponent):
    def get_agent_definitions(self):
        return {
            'agent-id': {
                'triggers': ['keyword1', 'keyword2'],
                'capabilities': ['capability1', 'capability2'],
                'expertise_level': 0.9,
                'collaboration_style': 'strategic_lead'
            }
        }
```

#### Modes System

**6 Behavioral Modes:**
- **Brainstorming**: Interactive discovery and requirements exploration
- **Introspection**: Meta-cognitive analysis and reasoning transparency
- **Task Management**: Hierarchical organization for complex operations
- **Orchestration**: Intelligent tool selection and coordination
- **Token Efficiency**: Compressed communication (30-50% reduction)
- **Standard**: Balanced default behavior

**Mode Development Pattern:**
```markdown
# MODE_CustomMode.md
**Purpose**: Brief description of mode's behavioral changes

## Activation Triggers
- keyword1, keyword2, specific patterns

## Behavioral Changes
- Change 1: Description and impact
- Change 2: Description and impact

## Examples
- Usage scenario with input/output examples
```

#### MCP Integration

**6 MCP Servers:**
- **Context7**: Official library documentation and patterns
- **Sequential**: Multi-step reasoning and systematic analysis
- **Magic**: Modern UI component generation from 21st.dev
- **Playwright**: Browser automation and E2E testing
- **Morphllm**: Pattern-based code transformation
- **Serena**: Semantic understanding and project memory

**MCP Development Pattern:**
```python
# setup/components/mcp.py
class MCPComponent(BaseComponent):
    def get_mcp_servers(self):
        return {
            'server-name': {
                'command': 'node',
                'args': ['/path/to/server'],
                'capabilities': ['capability1', 'capability2'],
                'auto_activation': ['trigger1', 'trigger2']
            }
        }
```

## 📝 Code Contribution Guidelines

### Documentation (Markdown)

**Documentation Standards:**
- **Clarity**: Clear, concise writing accessible to target audience
- **Structure**: Logical organization with consistent heading hierarchy
- **Examples**: Practical code examples for all concepts
- **Accuracy**: Technical accuracy verified through testing
- **Completeness**: Cover all use cases and edge cases

**Markdown Conventions:**
```markdown
# Main Title (H1) - Once per document
## Section (H2) - Major sections
### Subsection (H3) - Detailed topics
#### Detail (H4) - Specific implementation details

**Bold** for emphasis and important concepts
`code` for inline code and commands
```code blocks``` for examples
**Flags**: Use consistent flag notation (--flag-name)
**Commands**: Use consistent command notation (/sc:command)
```

**Code Example Standards:**
```bash
# Good: Complete, runnable examples
/sc:implement "user authentication system"
# → Auto-activates: security-engineer + backend-architect

# Bad: Incomplete or non-functional examples
/sc:implement auth  # Not descriptive enough
```

### Commit Messages

**Commit Message Format:**
```
type(scope): brief description

Detailed explanation if needed, including:
- What changed and why
- Any breaking changes
- Related issue references

Closes #123
```

**Commit Types:**
- **feat**: New feature or enhancement
- **fix**: Bug fix or correction
- **docs**: Documentation changes
- **refactor**: Code restructuring without behavior change
- **test**: Test additions or improvements
- **chore**: Maintenance tasks, dependency updates

**Examples:**
```bash
# Good commit messages
feat(agents): add data-scientist agent with ML capabilities
fix(mcp): resolve Context7 connection timeout issues
docs(modes): update behavioral modes with examples
refactor(components): simplify component registration logic

# Bad commit messages
fix stuff
update files
changes
```

## 🔄 Development Workflow

### 1. Fork & Branch

**Git Workflow:**
```bash
# 1. Fork repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/SuperClaude_Framework.git
cd SuperClaude_Framework

# 3. Add upstream remote
git remote add upstream https://github.com/SuperClaude-Org/SuperClaude_Framework.git

# 4. Create feature branch
git checkout -b feature/your-feature-name
# Examples: feature/data-scientist-agent, fix/mcp-connection-timeout
```

**Branch Naming Conventions:**
- **feature/**: New features (`feature/research-mode`)
- **fix/**: Bug fixes (`fix/installation-error`)
- **docs/**: Documentation (`docs/contributing-guide`)
- **refactor/**: Code restructuring (`refactor/component-system`)

### 2. Develop & Test

**Development Process:**
```bash
# 1. Make changes following coding standards
# 2. Test changes locally
python -m pytest tests/
python scripts/validate_pypi_ready.py

# 3. Test installation
SuperClaude install --dry-run --components your-component

# 4. Run linting and formatting
black .
pylint setup/
mypy setup/

# 5. Update documentation if needed
# 6. Add tests for new functionality
```

**Testing Requirements:**
- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions
- **Installation Tests**: Verify installation process
- **Documentation Tests**: Ensure examples work

### 3. Submit Pull Request

**Pull Request Process:**
```bash
# 1. Commit changes with descriptive messages
git add .
git commit -m "feat(agents): add research agent with citation management"

# 2. Push to your fork
git push origin feature/your-feature-name

# 3. Create Pull Request on GitHub with:
# - Clear title and description
# - Link to related issues
# - Test results and verification
# - Breaking changes documentation
```

**Pull Request Template:**
```markdown
## Description
Brief description of changes and motivation

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Tests pass locally
- [ ] Installation tested
- [ ] Documentation updated
- [ ] Examples verified

## Checklist
- [ ] Code follows project standards
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
```

### 4. Code Review

**Code Review Process:**
1. **Automated Checks**: GitHub Actions run tests and validation
2. **Maintainer Review**: Core team reviews code quality and design
3. **Community Feedback**: Community members provide input
4. **Revision**: Address feedback and make requested changes
5. **Approval**: Final approval and merge by maintainers

**Review Criteria:**
- **Functionality**: Code works as intended
- **Quality**: Follows coding standards and best practices
- **Testing**: Adequate test coverage and validation
- **Documentation**: Clear documentation and examples
- **Impact**: No breaking changes without justification
- **Performance**: No significant performance degradation

**Addressing Feedback:**
```bash
# 1. Make requested changes
# 2. Commit with clear messages
git add .
git commit -m "address review: improve error handling in component loader"

# 3. Push updates
git push origin feature/your-feature-name

# 4. Respond to review comments
# 5. Request re-review when ready
```

## 📦 Release Process

### Version Management

**Semantic Versioning (SemVer):**
- **Major (X.0.0)**: Breaking changes requiring user action
- **Minor (X.Y.0)**: New features, backward compatible
- **Patch (X.Y.Z)**: Bug fixes, backward compatible

**Version Update Process:**
```bash
# 1. Update version in setup.py and __init__.py
# 2. Update CHANGELOG.md with release notes
# 3. Create version tag
git tag -a v4.1.0 -m "Release v4.1.0: Add research agent and enhanced MCP integration"

# 4. Push tag
git push upstream v4.1.0
```

**Release Branches:**
- **master**: Stable releases
- **SuperClaude_V4_Beta**: Beta releases and development
- **hotfix/***: Critical fixes for production

### Release Checklist

**Pre-Release Validation:**
- [ ] All tests pass (`python -m pytest tests/`)
- [ ] Installation validation (`python scripts/validate_pypi_ready.py`)
- [ ] Documentation updated and accurate
- [ ] CHANGELOG.md updated with release notes
- [ ] Version numbers updated consistently
- [ ] Breaking changes documented
- [ ] Migration guides created if needed

**Release Process:**
- [ ] Create release branch from master
- [ ] Final testing on clean environment
- [ ] Generate release notes
- [ ] Create GitHub release with tag
- [ ] Publish to PyPI (`python setup.py sdist bdist_wheel && twine upload dist/*`)
- [ ] Update NPM wrapper package
- [ ] Announce release in community channels

**Post-Release:**
- [ ] Monitor for critical issues
- [ ] Update documentation sites
- [ ] Prepare hotfix procedures if needed
- [ ] Plan next release cycle

## 🚀 Contributing to V4 Components

### Creating New Agents

**Agent Development Process:**
1. **Identify Need**: Clear use case and domain expertise gap
2. **Define Specialization**: Unique capabilities and triggers
3. **Implement Component**: Following agent development pattern
4. **Create Documentation**: Agent description and examples
5. **Test Integration**: Verify activation and coordination

**Agent Implementation Example:**
```python
# setup/components/custom_agent.py
from setup.components.base import BaseComponent

class DataScienceAgentComponent(BaseComponent):
    def get_metadata(self):
        return {
            'name': 'data_science_agent',
            'description': 'Specialized agent for data science and ML workflows',
            'dependencies': ['core']
        }
    
    def install(self, install_dir):
        agent_file = install_dir / 'AGENT_DataScientist.md'
        self._write_agent_definition(agent_file, {
            'expertise': ['data_analysis', 'machine_learning', 'statistical_modeling'],
            'triggers': ['data', 'analytics', 'machine learning', 'statistics'],
            'capabilities': ['data_preprocessing', 'model_development', 'visualization'],
            'collaboration_style': 'analytical_contributor'
        })
```

**Agent Documentation Template:**
```markdown
# Data Scientist Agent 📊

**Purpose**: Advanced data science and machine learning expertise

**Auto-Activation Triggers:**
- Keywords: data, analytics, ML, statistics, pandas, numpy
- File types: .ipynb, .csv, .parquet
- Domain: data science workflows

**Capabilities:**
- Data analysis and preprocessing
- Statistical modeling and hypothesis testing
- Machine learning model development
- Data visualization and reporting

**Examples:**
- Exploratory data analysis workflows
- ML model selection and optimization
- Statistical significance testing
- Data pipeline development
```

### Developing Behavioral Modes

**Mode Development Guidelines:**
1. **Clear Purpose**: Specific behavioral modification goal
2. **Distinct Triggers**: Unique activation patterns
3. **Measurable Impact**: Quantifiable behavioral changes
4. **Documentation**: Complete usage examples
5. **Integration**: Compatibility with existing modes

**Mode Implementation Example:**
```markdown
# MODE_Research.md

**Purpose**: Academic and technical research with systematic methodology

## Activation Triggers
- Research keywords: research, study, investigate, literature
- Academic contexts: citation, peer review, hypothesis
- Manual flags: --research, --academic

## Behavioral Changes
- **Systematic Methodology**: Structure research with clear phases
- **Source Validation**: Verify information credibility and currency
- **Citation Management**: Proper attribution and reference formatting
- **Evidence-Based**: Support claims with verifiable sources

## Examples
Standard: "Tell me about microservices"
Research: "📚 Research Methodology:
          1. Literature review of microservices patterns
          2. Industry case studies and implementations  
          3. Performance benchmarks and trade-offs
          📖 Sources: [Academic papers, industry reports]"
```

### Enhancing Session Lifecycle

**Session Enhancement Areas:**
1. **Memory Management**: Improve context preservation and retrieval
2. **Cross-Session Learning**: Enhance pattern recognition and adaptation
3. **Multi-User Coordination**: Team session coordination features
4. **Performance Optimization**: Memory efficiency and loading speed
5. **Recovery Mechanisms**: Robust session recovery and backup

**Session Development Pattern:**
```python
# Extending session management
class SessionEnhancement:
    def enhance_memory_retention(self, session_context):
        # Implement improved memory compression
        # Add intelligent context pruning
        # Enhance pattern recognition
        pass
    
    def add_collaboration_features(self, session_id):
        # Multi-developer session coordination
        # Shared project context
        # Conflict resolution mechanisms
        pass
```

**Session Contribution Requirements:**
- **Backward Compatibility**: Existing sessions must work unchanged
- **Performance**: No degradation in session load/save times
- **Testing**: Comprehensive session lifecycle testing
- **Documentation**: Clear session enhancement examples

### MCP Server Integration

**MCP Server Development Process:**
1. **Capability Definition**: Clear server purpose and functions
2. **Protocol Implementation**: Standard MCP protocol compliance
3. **SuperClaude Integration**: Auto-activation and coordination
4. **Testing**: Server functionality and integration testing
5. **Documentation**: Usage patterns and examples

**MCP Server Integration Example:**
```python
# setup/components/custom_mcp.py
class DatabaseAnalyzerMCPComponent(BaseComponent):
    def get_metadata(self):
        return {
            'name': 'database_analyzer_mcp',
            'description': 'Database query optimization and schema analysis',
            'dependencies': ['core', 'mcp']
        }
    
    def install(self, install_dir):
        # Add to MCP configuration
        self._add_mcp_server_config({
            'database-analyzer': {
                'command': 'node',
                'args': ['/path/to/database-analyzer-server.js'],
                'capabilities': ['query_optimization', 'schema_analysis'],
                'auto_activation': ['database', 'sql', 'query optimization']
            }
        })
        
        # Create server instruction file
        self._create_mcp_instructions('MCP_DatabaseAnalyzer.md')
```

**MCP Integration Requirements:**
- **Protocol Compliance**: Standard MCP protocol implementation
- **Error Handling**: Robust connection and error recovery
- **Performance**: Acceptable latency and resource usage
- **Documentation**: Clear capability and usage documentation

## 💬 Getting Help

### Development Channels

**Primary Support Channels:**
- **GitHub Issues**: Bug reports, feature requests, technical questions
- **GitHub Discussions**: General questions, ideas, community chat
- **Pull Request Reviews**: Code-specific feedback and guidance
- **Documentation**: Comprehensive guides and examples

**Channel Guidelines:**
- **Issues**: Specific, reproducible problems with detailed information
- **Discussions**: Open-ended questions, ideas, and community interaction
- **Pull Requests**: Code review, implementation feedback, technical guidance

**Response Expectations:**
- **Critical Issues**: 24-48 hours
- **General Questions**: 2-5 days
- **Feature Requests**: Weekly review cycle
- **Pull Requests**: 3-7 days initial review

### Common Development Questions

**Q: How do I test my component changes locally?**
```bash
# Install in development mode
pip install -e ".[dev]"

# Test specific component
SuperClaude install --dry-run --components your-component

# Run test suite
python -m pytest tests/test_your_component.py
```

**Q: Where should I add my custom agent?**
```
# Agent files go in:
SuperClaude/Agents/AGENT_YourAgent.md

# Component definition goes in:
setup/components/your_agent.py

# Tests go in:
tests/test_your_agent.py
```

**Q: How do I handle component dependencies?**
```python
def get_dependencies(self):
    return ['core', 'mcp']  # Required components

def get_metadata(self):
    return {
        'dependencies': ['core', 'mcp'],
        'optional_dependencies': ['agents']
    }
```

**Q: What's the difference between agents and MCP servers?**
- **Agents**: Behavioral specializations within Claude Code
- **MCP Servers**: External tools that extend capabilities
- **Agents** coordinate; **MCP servers** provide enhanced functionality

**Q: How do I contribute documentation?**
1. Find documentation TODOs in relevant files
2. Follow markdown conventions and examples
3. Test all code examples
4. Submit PR with documentation changes

**Q: My MCP server isn't activating automatically. Why?**
Check:
1. Server defined in MCP configuration
2. Auto-activation triggers properly configured
3. Server starts successfully
4. Triggers match user input patterns

## 📄 License

**MIT License**: SuperClaude Framework is licensed under the MIT License, providing maximum freedom for use, modification, and distribution.

**Contribution License Agreement:**
By contributing to SuperClaude Framework, you agree that your contributions will be licensed under the same MIT License. You retain copyright to your contributions while granting the project perpetual rights to use, modify, and distribute your code.

**Third-Party Dependencies:**
Ensure any dependencies you add are compatible with MIT License. Common compatible licenses: MIT, Apache 2.0, BSD. Avoid GPL and other copyleft licenses.

## 🙏 Acknowledgments

**Core Contributors:**
- Framework architecture and implementation
- Community management and support
- Documentation and user experience
- Testing and quality assurance

**Community Impact:**
SuperClaude Framework exists because of the collaborative effort of developers, users, and contributors who believe in advancing AI-assisted development. Every bug report, feature suggestion, documentation improvement, and code contribution makes the framework better for everyone.

**Special Recognition:**
- **Early Adopters**: Testing and feedback during beta development
- **Documentation Contributors**: Improving accessibility and usability
- **Bug Hunters**: Finding and reporting issues that improve stability
- **Feature Contributors**: Adding capabilities that expand framework utility

**Contributing Recognition:**
All contributors are recognized in our GitHub contributors page and release notes. Significant contributions may be highlighted in project announcements and community updates.

**Join the Community:**
Your expertise and perspective make SuperClaude Framework better. Whether you're fixing typos, adding features, or helping other users, every contribution advances the goal of more effective AI-assisted development.

**Thank you for contributing to the future of AI-enhanced development tools! 🚀**