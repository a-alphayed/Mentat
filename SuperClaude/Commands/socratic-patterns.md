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

### Chain of Responsibility Discovery
```
/sc:socratic-patterns "if (canHandle(request)) { process(); } else { next.handle(request); }" --category behavioral
# Guides discovery through questioning:
# "What happens when this object can't handle the request?"
# "How does the request find someone who can handle it?"
# "What would you do to add a new type of handler?"
```

### Iterator Pattern Recognition
```
/sc:socratic-patterns [collection-traversal-code] --focus structure
# Leads to Iterator pattern discovery:
# "How do you access elements without knowing the internal structure?"
# "What stays the same when you change from Array to LinkedList?"
# "Who's responsible for knowing the current position?"
```

### Mediator Pattern Exploration
```
/sc:socratic-patterns [ui-component-communication] --category behavioral
# Discovers Mediator through questioning:
# "How do these components communicate without knowing about each other?"
# "What happens when you add a new component to the dialog?"
# "Who coordinates the interactions between all these parts?"
```

### Flyweight Pattern Discovery
```
/sc:socratic-patterns [text-editor-character-rendering] --focus structure
# Guides to Flyweight recognition:
# "What data is shared vs unique for each character?"
# "How do you handle thousands of characters efficiently?"
# "What would happen if each character object stored its position?"
```

### Proxy Pattern Recognition
```
/sc:socratic-patterns [remote-object-access] --category structural
# Leads to Proxy pattern discovery:
# "How do you control access to this expensive resource?"
# "What's the difference between the proxy and the real object?"
# "When would you use this instead of accessing directly?"
```

### Memento Pattern Exploration  
```
/sc:socratic-patterns [undo-functionality] --focus behavioral
# Discovers Memento through questioning:
# "How do you save state without exposing internal structure?"
# "Who's responsible for managing the saved states?"
# "How do you restore without breaking encapsulation?"
```

### Interpreter Pattern Discovery
```
/sc:socratic-patterns [expression-evaluator] --category behavioral
# Guides to Interpreter recognition:
# "How do you represent each grammar rule as an object?"
# "What happens when you add a new operation to the language?"
# "How does the parse tree get evaluated?"
```

### Visitor Pattern Recognition
```
/sc:socratic-patterns [tree-operations] --focus behavioral
# Leads to Visitor pattern discovery:
# "How do you add new operations without changing the tree nodes?"
# "What's the relationship between the visitor and the elements?"
# "How does double dispatch work here?"
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
- **Bridge**: "How is abstraction separated from implementation?"
- **Composite**: "How are individual and composite objects treated uniformly?"
- **Decorator**: "How is additional behavior added without changing structure?"
- **Facade**: "How is complex subsystem complexity hidden behind simple interface?"
- **Flyweight**: "How is memory usage minimized when working with large numbers of similar objects?"
- **Proxy**: "How is access to another object controlled or enhanced?"

### Behavioral Patterns - Object Interaction
- **Chain of Responsibility**: "How is a request passed along a chain until handled?"
- **Command**: "How are requests encapsulated as objects?"
- **Interpreter**: "How is a language or notation interpreted and executed?"
- **Iterator**: "How is sequential access provided to elements without exposing structure?"
- **Mediator**: "How do objects interact without referring to each other explicitly?"
- **Memento**: "How is object state captured and restored without violating encapsulation?"
- **Observer**: "How are multiple objects notified of state changes?"
- **State**: "How does object behavior change based on internal state?"
- **Strategy**: "How are algorithms made interchangeable?"
- **Template Method**: "How is algorithm structure defined with variable steps?"
- **Visitor**: "How are operations added to objects without modifying their structure?"

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

### Pattern-Specific Discovery Questions

#### Missing Structural Patterns
```yaml
flyweight_discovery:
  context: "Large numbers of similar objects with performance concerns"
  key_questions:
    - "What data is intrinsic (shared) vs extrinsic (unique) to each object?"
    - "How do you handle thousands of similar objects without consuming too much memory?"
    - "What happens if you store all state inside each object instance?"
    - "How do you separate what varies from what stays constant?"

proxy_discovery:
  context: "Controlled access to another object or resource"
  key_questions:
    - "How do you control or enhance access to the real object?"
    - "What's the difference between the proxy and the actual object?"
    - "When would someone use this instead of direct access?"
    - "How do you maintain the same interface while adding behavior?"
```

#### Missing Behavioral Patterns
```yaml
chain_of_responsibility_discovery:
  context: "Request handling along a chain until processed"
  key_questions:
    - "What happens when this handler can't process the request?"
    - "How does the request find the right handler?"
    - "How would you add a new type of handler to the chain?"
    - "Who decides the order of processing?"

interpreter_discovery:
  context: "Language or expression evaluation systems"
  key_questions:
    - "How is each grammar rule represented as code?"
    - "What happens when you add a new operation to the language?"
    - "How do you build and evaluate the parse tree?"
    - "Who's responsible for understanding each part of the expression?"

iterator_discovery:
  context: "Sequential access to collection elements"
  key_questions:
    - "How do you access elements without knowing internal structure?"
    - "What stays the same when changing from Array to LinkedList?"
    - "Who maintains the current position in traversal?"
    - "How do you support multiple simultaneous traversals?"

mediator_discovery:
  context: "Complex interactions between multiple objects"
  key_questions:
    - "How do these objects communicate without knowing each other?"
    - "What happens when you add a new component to the system?"
    - "Who coordinates all the interactions?"
    - "How do you avoid tight coupling between components?"

memento_discovery:
  context: "State capture and restoration (like undo/redo)"
  key_questions:
    - "How do you save state without exposing internal structure?"
    - "Who's responsible for managing saved states?"
    - "How do you restore previous state without breaking encapsulation?"
    - "What happens when the object structure changes?"

visitor_discovery:
  context: "Operations on object structures without modification"
  key_questions:
    - "How do you add new operations without changing existing classes?"
    - "What's the relationship between visitor and elements?"
    - "How does the object structure collaborate with operations?"
    - "What happens when you need different types of traversal?"
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