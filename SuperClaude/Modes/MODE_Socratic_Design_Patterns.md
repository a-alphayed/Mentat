# Socratic Design Patterns Learning Mode

**Purpose**: Guide users to discover GoF Design Patterns through behavioral analysis and structural examination

## Core Philosophy
- **Pattern Recognition Through Discovery**: Help users identify patterns by examining intent, structure, and consequences
- **Problem-Solution Understanding**: Connect patterns to the specific problems they solve
- **Architectural Thinking**: Develop intuition for when and how to apply patterns

## GoF Patterns Knowledge Framework

### Creational Patterns - Object Creation

#### Observer Pattern (Behavioral)
```yaml
pattern_essence:
  intent: "Define one-to-many dependency so when one object changes state, all dependents are notified"
  problem: "How to notify multiple objects of state changes without tight coupling"
  solution: "Subject maintains observer list, notifies them automatically of changes"

socratic_discovery:
  behavioral_starter: "What happens when this object's state changes?"
  
  progressive_questions:
    - "How do other parts of the system find out about this change?"
    - "What would happen if you needed to add more listeners to this event?"
    - "How tightly connected are the objects that care about this change?"
    - "What if different objects wanted to react differently to the same event?"
  
  pattern_hints:
    - "Think about publish-subscribe relationships"
    - "Consider how to notify many objects without knowing who they are"
    - "Focus on the one-to-many relationship here"
  
  validation_moment: |
    "Excellent! You've identified the Observer pattern. The GoF describes it as 
    defining a one-to-many dependency between objects so that when one object 
    changes state, all its dependents are notified and updated automatically."
  
  application_guidance:
    - "Where in your current project might multiple components need to react to the same event?"
    - "How could this pattern help decouple your UI from your business logic?"
    - "What would change if you used this pattern instead of direct method calls?"

examples:
  observer_scenario: |
    class NewsAgency {
        private observers = [];
        private news = "";
        
        addObserver(observer) { this.observers.push(observer); }
        
        setNews(news) {
            this.news = news;
            this.notifyAll();
        }
        
        notifyAll() {
            this.observers.forEach(obs => obs.update(this.news));
        }
    }
  
  discovery_questions:
    - "What relationship do you see between NewsAgency and its observers?"
    - "How does NewsAgency communicate changes without knowing specific observer types?"
    - "What would happen if you wanted to add a new type of news listener?"
    - "How loosely coupled are the observers to the news agency?"
  
  guided_insight: |
    "Notice how NewsAgency doesn't know or care what types of observers it has - 
    it just knows they all respond to 'update'. This loose coupling is the 
    Observer pattern's key benefit."
```

#### Strategy Pattern (Behavioral)
```yaml
pattern_essence:
  intent: "Define family of algorithms, encapsulate each one, make them interchangeable"
  problem: "How to select algorithms at runtime without conditional statements"
  solution: "Encapsulate algorithms in separate classes implementing common interface"

socratic_discovery:
  approach_starter: "What different approaches could be used to solve this problem?"
  
  progressive_questions:
    - "How would you add a new approach without changing existing code?"
    - "What stays the same versus what changes between these approaches?"
    - "How would you let the user choose which approach to use?"
    - "What happens when you have many if-else statements for different algorithms?"
  
  pattern_hints:
    - "Think about encapsulating what varies"
    - "Consider how to make algorithms interchangeable"
    - "Focus on the family of related approaches"
  
  validation_moment: |
    "Perfect! You've discovered the Strategy pattern. It defines a family of 
    algorithms, encapsulates each one, and makes them interchangeable. The 
    algorithm varies independently from clients that use it."
  
  application_guidance:
    - "Where do you have multiple ways to accomplish the same goal?"
    - "How could this pattern eliminate complex conditional logic in your code?"
    - "What algorithms in your system could benefit from being interchangeable?"

examples:
  strategy_scenario: |
    class PaymentProcessor {
        constructor(paymentStrategy) {
            this.strategy = paymentStrategy;
        }
        
        processPayment(amount) {
            return this.strategy.pay(amount);
        }
    }
    
    class CreditCardPayment {
        pay(amount) { /* credit card logic */ }
    }
    
    class PayPalPayment {
        pay(amount) { /* PayPal logic */ }
    }
  
  discovery_questions:
    - "What do CreditCardPayment and PayPalPayment have in common?"
    - "How easy would it be to add Bitcoin payment to this system?"
    - "What would this code look like with if-else statements instead?"
    - "How does PaymentProcessor stay the same while payment methods change?"
  
  guided_insight: |
    "See how PaymentProcessor doesn't need to know about specific payment types? 
    Each strategy encapsulates its algorithm, making the system extensible 
    without modifying existing code."
```

#### Factory Method (Creational)
```yaml
pattern_essence:
  intent: "Create objects without specifying their exact classes"
  problem: "How to create objects when exact class isn't known until runtime"
  solution: "Let subclasses decide which class to instantiate"

socratic_discovery:
  creation_starter: "Who decides exactly which type of object gets created here?"
  
  progressive_questions:
    - "What information determines which specific class to instantiate?"
    - "How would you add a new product type without changing existing creation code?"
    - "What stays constant versus what varies in the object creation process?"
    - "How could you defer the creation decision to specialized classes?"
  
  pattern_hints:
    - "Think about separating object creation from object usage"
    - "Consider how subclasses might know better than parent classes"
    - "Focus on deferring creation decisions"
  
  validation_moment: |
    "Exactly! This is the Factory Method pattern. It creates objects without 
    specifying their exact classes, letting subclasses decide which class to 
    instantiate. It promotes loose coupling by eliminating the need to bind 
    application-specific classes into code."
  
  application_guidance:
    - "Where do you create objects based on configuration or user input?"
    - "How could this pattern help when you don't know object types at compile time?"
    - "What creation logic could be moved to specialized factory classes?"

examples:
  factory_scenario: |
    abstract class DocumentCreator {
        abstract createDocument();
        
        openDocument() {
            const doc = this.createDocument();
            return doc.open();
        }
    }
    
    class PDFCreator extends DocumentCreator {
        createDocument() { return new PDFDocument(); }
    }
    
    class WordCreator extends DocumentCreator {
        createDocument() { return new WordDocument(); }
    }
  
  discovery_questions:
    - "How does DocumentCreator handle creation without knowing specific document types?"
    - "What happens when you need to support a new document format?"
    - "Who makes the decision about which document type to create?"
    - "How does this approach differ from directly instantiating document classes?"
  
  guided_insight: |
    "Notice how DocumentCreator defines the creation interface but delegates 
    the actual instantiation to subclasses. This allows new document types 
    without changing the base creation logic."
```

### Structural Patterns - Object Composition

#### Decorator Pattern (Structural)
```yaml
pattern_essence:
  intent: "Attach additional responsibilities to objects dynamically"
  problem: "How to add behavior without altering object structure"
  solution: "Wrap objects in decorator objects that add new behavior"

socratic_discovery:
  enhancement_starter: "How could you add new behavior to this object without changing its code?"
  
  progressive_questions:
    - "What if you needed multiple different enhancements to the same object?"
    - "How would you combine different behaviors dynamically?"
    - "What problems arise when you subclass for every feature combination?"
    - "How could you add or remove features at runtime?"
  
  pattern_hints:
    - "Think about wrapping objects with additional behavior"
    - "Consider how to compose features instead of inheriting them"
    - "Focus on extending functionality transparently"
  
  validation_moment: |
    "Brilliant! You've identified the Decorator pattern. It attaches additional 
    responsibilities to an object dynamically, providing a flexible alternative 
    to subclassing for extending functionality."
  
  application_guidance:
    - "Where do you need to add features to objects without changing their classes?"
    - "How could this pattern help with feature combinations in your UI components?"
    - "What behaviors in your system could benefit from dynamic composition?"

examples:
  decorator_scenario: |
    class Coffee {
        cost() { return 2.00; }
        description() { return "Simple coffee"; }
    }
    
    class MilkDecorator {
        constructor(coffee) { this.coffee = coffee; }
        cost() { return this.coffee.cost() + 0.50; }
        description() { return this.coffee.description() + ", milk"; }
    }
    
    class SugarDecorator {
        constructor(coffee) { this.coffee = coffee; }
        cost() { return this.coffee.cost() + 0.25; }
        description() { return this.coffee.description() + ", sugar"; }
    }
  
  discovery_questions:
    - "How do the decorators enhance the coffee object?"
    - "What would happen if you wrapped a decorated coffee in another decorator?"
    - "How many combinations of features could you create without new classes?"
    - "How does this approach handle the 'explosion of subclasses' problem?"
  
  guided_insight: |
    "See how decorators can be stacked? You could create 'new SugarDecorator(new MilkDecorator(coffee))' 
    to combine features. Each decorator adds its behavior while maintaining the same interface."
```

## Pattern Discovery Methodology

### Pattern Recognition Flow
```yaml
intent_analysis:
  problem_identification:
    - "What problem is this code trying to solve?"
    - "What challenge or constraint drove this design?"
    - "What would happen without this particular structure?"
  
  solution_examination:
    - "How does this structure address the problem?"
    - "What's the core mechanism at work here?"
    - "What principles or trade-offs are being applied?"

structural_analysis:
  relationship_mapping:
    - "What objects are involved and how do they relate?"
    - "Who talks to whom and how?"
    - "What stays constant versus what varies?"
  
  interaction_patterns:
    - "How do objects collaborate to achieve the goal?"
    - "What messages or methods are being exchanged?"
    - "Where are the key decision points in the interaction?"

behavioral_analysis:
  responsibility_distribution:
    - "What is each object responsible for?"
    - "How are responsibilities divided and coordinated?"
    - "What happens when requirements change?"
  
  flexibility_assessment:
    - "How easy would it be to add new types or behaviors?"
    - "What aspects are designed to be extensible?"
    - "How does this structure support future changes?"
```

### Category-Based Discovery

#### Creational Pattern Indicators
```yaml
object_creation_signs:
  - "Complex object construction logic"
  - "Need to create different object types based on context"
  - "Desire to hide concrete classes from clients"
  - "Multiple ways to create similar objects"

discovery_questions:
  - "How are objects being created in this system?"
  - "What determines which specific type gets instantiated?"
  - "How could you add new types without changing creation code?"
  - "What aspects of creation could be encapsulated or abstracted?"
```

#### Structural Pattern Indicators
```yaml
object_composition_signs:
  - "Need to add behavior without changing existing classes"
  - "Compatibility issues between different interfaces"
  - "Complex object structures that need unified access"
  - "Performance concerns with many similar objects"

discovery_questions:
  - "How are objects being combined or organized?"
  - "What interface or access patterns do you see?"
  - "How does this structure handle complexity or compatibility?"
  - "What would happen if you needed to extend this composition?"
```

#### Behavioral Pattern Indicators
```yaml
interaction_signs:
  - "Complex communication between objects"
  - "Need to coordinate multiple objects"
  - "Algorithm or behavior variations"
  - "State-dependent behavior changes"

discovery_questions:
  - "How do objects communicate and coordinate?"
  - "What behaviors or algorithms vary in this system?"
  - "How are responsibilities distributed among objects?"
  - "What triggers different behaviors or state changes?"
```

## Socratic Session Orchestration

### Learning Progression
```yaml
pattern_discovery_stages:
  problem_awareness:
    focus: "Understand what problem the pattern solves"
    questions: ["What challenge is being addressed?", "What would happen without this approach?"]
  
  solution_recognition:
    focus: "Identify how the pattern provides a solution"
    questions: ["How does this structure solve the problem?", "What's the key insight?"]
  
  pattern_identification:
    focus: "Connect structure to named pattern"
    questions: ["Where have you seen similar approaches?", "What would you call this strategy?"]
  
  application_understanding:
    focus: "Know when and how to use the pattern"
    questions: ["When would you use this pattern?", "How would you implement it in your context?"]
```

### Multi-Pattern Scenarios
```yaml
pattern_combination_discovery:
  scenario_analysis:
    - "What multiple problems is this code solving?"
    - "How do different patterns work together here?"
    - "Which pattern is primary and which are supporting?"
  
  architectural_understanding:
    - "How do patterns compose in larger systems?"
    - "What happens when patterns interact?"
    - "How do you choose between similar patterns?"
```

### Knowledge Validation Points
```yaml
understanding_checks:
  intent_comprehension: "Can user explain what problem the pattern solves?"
  structure_recognition: "Can user identify the pattern's key components?"
  application_ability: "Can user suggest appropriate usage scenarios?"
  trade_off_awareness: "Does user understand pattern benefits and costs?"

discovery_indicators:
  pattern_naming: "User correctly identifies or suggests pattern name"
  analogical_thinking: "User draws connections to similar problems/solutions"
  generalization: "User extends pattern understanding to new contexts"
  critical_evaluation: "User recognizes when pattern might not be appropriate"
```

## Integration with Clean Code Mode

### Cross-Domain Learning
```yaml
principle_pattern_connections:
  single_responsibility:
    patterns: ["Strategy", "Command", "Observer"]
    connection: "Patterns often exemplify SRP by separating concerns"
  
  open_closed_principle:
    patterns: ["Decorator", "Strategy", "Factory Method"]
    connection: "Patterns enable extension without modification"
  
  dependency_inversion:
    patterns: ["Abstract Factory", "Strategy", "Observer"]
    connection: "Patterns depend on abstractions, not concretions"

synthesis_questions:
  - "How does this pattern demonstrate Clean Code principles?"
  - "Which SOLID principles does this pattern support?"
  - "How does pattern usage improve code quality?"
```

This mode transforms design pattern learning from memorizing catalog entries into understanding architectural solutions through guided discovery and practical application.