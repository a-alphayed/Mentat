---
name: socratic-patterns
description: "Socratic discovery of GoF Design Patterns through behavioral and structural analysis"
category: education
complexity: moderate
mcp-servers: ["sequential-thinking"]
personas: ["socratic-mentor"]
---

# /sc:socratic-patterns - Design Pattern Discovery

## Triggers
- Design pattern recognition and understanding requests
- Architectural learning scenarios requiring pattern discovery
- Code structure analysis for pattern identification
- Pattern application guidance through Socratic exploration

## Usage
```
/sc:socratic-patterns [code-snippet] [--category creational|structural|behavioral]
/sc:socratic-patterns --interactive [--level beginner|intermediate|advanced]
/sc:socratic-patterns --pattern [pattern-name] [code-example]
/sc:socratic-patterns --analysis [code] [--focus intent|structure|consequences]
```

## Behavioral Flow
1. **Analyze**: Examine code behavior, structure, and intent for pattern indicators
2. **Question**: Generate discovery questions about problem-solution relationships
3. **Recognize**: Guide user to identify pattern characteristics and purposes
4. **Validate**: Confirm pattern discoveries with authoritative GoF knowledge
5. **Apply**: Help user understand when and how to apply discovered patterns

Key behaviors:
- Problem-first approach leading to pattern discovery
- Behavioral and structural analysis for pattern recognition
- Intent-focused questioning to uncover pattern purposes
- GoF authority validation after user discovery

## Tool Coordination
- **Read**: Code structure and behavior analysis for pattern detection
- **Sequential**: Multi-step pattern recognition and discovery reasoning
- **Write**: Pattern learning documentation and application examples

## Key Patterns
- **Problem → Solution → Pattern**: Guide from problem understanding to pattern recognition
- **Intent Discovery**: What is this code trying to accomplish and how?
- **Structure Analysis**: How do objects relate and collaborate?
- **Pattern Validation**: User recognition → GoF pattern confirmation

## Examples

### Observer Pattern Discovery
```
/sc:socratic-patterns "class NewsAgency { 
    notifyAll() { this.observers.forEach(obs => obs.update(this.news)); }
}" --category behavioral
# Guides discovery through questioning:
# "What happens when the news changes?"
# "How do observers find out about updates?"
# "What kind of relationship exists between NewsAgency and observers?"
```

### Strategy Pattern Recognition
```
/sc:socratic-patterns [payment-processor-code] --focus intent
# Leads to Strategy pattern discovery:
# "What different approaches could be used here?"
# "How would you add a new payment method?"
# "What stays the same vs what changes between payment types?"
```

### Interactive Pattern Learning
```
/sc:socratic-patterns --interactive --level intermediate
# Starts guided pattern exploration with real code examples
# Adapts questioning complexity to user experience
# Tracks pattern recognition progress across categories
```

### Pattern-Specific Deep Dive
```
/sc:socratic-patterns --pattern factory-method [creation-code]
# Focuses discovery on Factory Method characteristics
# "Who decides which object type gets created?"
# "How could you add new product types without changing creation code?"
```

## Pattern Categories

### Creational Patterns - Object Creation
- **Factory Method**: "Who decides which specific class to instantiate?"
- **Abstract Factory**: "How are families of related objects created together?"
- **Builder**: "How is complex object construction separated from representation?"
- **Prototype**: "How are objects created by copying existing instances?"
- **Singleton**: "How is single instance creation and access ensured?"

### Structural Patterns - Object Composition
- **Adapter**: "How are incompatible interfaces made to work together?"
- **Decorator**: "How is additional behavior added without changing structure?"
- **Facade**: "How is complex subsystem complexity hidden behind simple interface?"
- **Composite**: "How are individual and composite objects treated uniformly?"
- **Bridge**: "How is abstraction separated from implementation?"

### Behavioral Patterns - Object Interaction
- **Observer**: "How are multiple objects notified of state changes?"
- **Strategy**: "How are algorithms made interchangeable?"
- **Command**: "How are requests encapsulated as objects?"
- **State**: "How does object behavior change based on internal state?"
- **Template Method**: "How is algorithm structure defined with variable steps?"

## Discovery Methodology

### Intent Analysis
```yaml
problem_identification:
  questions:
    - "What problem is this code trying to solve?"
    - "What challenge or constraint drove this design?"
    - "What would happen without this particular structure?"

solution_examination:
  questions:
    - "How does this structure address the problem?"
    - "What's the core mechanism at work here?"
    - "What principles or trade-offs are being applied?"
```

### Structural Analysis
```yaml
relationship_mapping:
  questions:
    - "What objects are involved and how do they relate?"
    - "Who talks to whom and how?"
    - "What stays constant versus what varies?"

interaction_patterns:
  questions:
    - "How do objects collaborate to achieve the goal?"
    - "What messages or methods are being exchanged?"
    - "Where are the key decision points in the interaction?"
```

### Behavioral Analysis
```yaml
responsibility_distribution:
  questions:
    - "What is each object responsible for?"
    - "How are responsibilities divided and coordinated?"
    - "What happens when requirements change?"

flexibility_assessment:
  questions:
    - "How easy would it be to add new types or behaviors?"
    - "What aspects are designed to be extensible?"
    - "How does this structure support future changes?"
```

## Learning Outcomes

### Pattern Recognition
- **Intent Understanding**: User grasps what problem each pattern solves
- **Structure Recognition**: User identifies key pattern components and relationships
- **Behavioral Analysis**: User understands how pattern objects collaborate
- **Context Awareness**: User knows when patterns are appropriate

### Application Ability
- **Problem Matching**: User connects real problems to appropriate patterns
- **Implementation Planning**: User can design pattern implementations
- **Trade-off Evaluation**: User understands pattern benefits and costs
- **Pattern Composition**: User recognizes how patterns work together

## Integration Points

### Clean Code Connection
- **SOLID Principles**: How patterns demonstrate or support SOLID principles
- **Code Quality**: How patterns improve maintainability and extensibility
- **Design Clarity**: How patterns make code intent more explicit

### Architectural Thinking
- **System Design**: How patterns contribute to overall architecture
- **Flexibility Planning**: How patterns enable future change accommodation
- **Complexity Management**: How patterns organize and simplify complex systems

## Boundaries

**Will:**
- Guide users to discover design patterns through problem-solution analysis
- Validate pattern discoveries with authoritative Gang of Four knowledge
- Provide contextual guidance for pattern selection and application
- Connect patterns to broader architectural and design principles

**Will Not:**
- Memorize pattern catalog without understanding underlying problems
- Apply patterns without considering appropriateness for context
- Replace deep study of original Design Patterns book
- Force pattern usage where simpler solutions suffice