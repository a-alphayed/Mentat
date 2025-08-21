# SuperClaude Flags Guide 🏁

**Most flags activate automatically** - Claude Code reads behavioral instructions to engage appropriate contexts based on keywords and patterns in your requests.

## Essential Flags (90% of Use Cases)

### Auto-Activation Flags
| Flag | When Activated | What It Does |
|------|---------------|--------------|
| `--think` | 5+ files OR complex analysis | Standard structured analysis |
| `--magic` | UI components, frontend | Modern UI generation |
| `--loop` | "improve", "polish", "refine" | Iterative enhancement cycles |
| `--safe-mode` | Production, >15 files | Maximum validation |
| `--uc` | High context usage | Ultra-compressed output |
| `--validate` | Risk detected | Pre-execution validation |

### MCP Server Flags
| Flag | Server | Purpose | API Key Required |
|------|---------|---------|------------------|
| `--c7` | Context7 | Official docs, framework patterns | No |
| `--seq` | Sequential | Multi-step reasoning, debugging | No |
| `--magic` | Magic | UI component generation | Yes |
| `--play` | Playwright | Browser testing, E2E validation | No |
| `--morph` | Morphllm | Bulk transformations, pattern edits | Yes |
| `--serena` | Serena | Project memory, symbol operations | No |

### Control Flags
| Flag | Purpose | Example |
|------|---------|---------|
| `--all-mcp` | Enable all MCP servers | Maximum capability tasks |
| `--no-mcp` | Native tools only | Quick operations, testing |
| `--scope [file\|module\|project]` | Define analysis boundary | Limit operation scope |
| `--focus [security\|performance\|quality]` | Target specific domain | Specialized analysis |

## Common Patterns

### Frontend Development
```bash
/sc:implement "responsive dashboard" --magic --c7
/sc:test ui-components/ --magic --play
/sc:improve legacy-ui/ --magic --morph --validate
```

### Backend Development
```bash
/sc:analyze api/ --focus performance --seq --think
/sc:analyze system/ --think-hard --c7 --scope system
/sc:analyze . --focus security --ultrathink --validate
```

### Large Projects
```bash
/sc:improve large-codebase/ --delegate --morph --uc
/sc:analyze . --ultrathink --all-mcp --safe-mode
/sc:analyze . --focus performance --think-hard --loop
```

## Manual Override
```bash
# Force specific behavior
/sc:analyze . --no-mcp                     # Native tools only
/sc:implement feature --ultrathink         # Maximum analysis depth
/sc:troubleshoot issue --uc                # Ultra-compressed output
```

## Flag Interactions

### Compatible Combinations
- `--think` + `--c7`: Analysis with documentation
- `--magic` + `--play`: UI generation with testing
- `--serena` + `--morph`: Project memory with transformations
- `--safe-mode` + `--validate`: Maximum safety

### Conflicting Flags
- `--all-mcp` vs individual MCP flags (use one or the other)
- `--no-mcp` vs any MCP flags (no-mcp wins)

## Troubleshooting

### Common Issues
- **Too many tools**: Use `--no-mcp` to test without MCP servers
- **Operation too slow**: Add `--uc` to compress output
- **Validation blocking**: Use `--validate` instead of `--safe-mode` in development

### Quick Fixes
```bash
/sc:analyze . --help                         # Should show available flags
/sc:analyze . --no-mcp                       # Native execution only
/sc:analyze . --verbose                      # Shows decision logic
```

## Related Resources
- [Commands Guide](commands.md) - Commands that use these flags
- [MCP Servers Guide](mcp-servers.md) - Understanding MCP flag activation