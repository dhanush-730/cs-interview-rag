# Object-Oriented Programming - CS Interview Study Material

## Core OOP Principles

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects" containing data and code.

### The Four Pillars of OOP

1. **Encapsulation**
2. **Abstraction**
3. **Inheritance**
4. **Polymorphism**

---

## Encapsulation

**Encapsulation** is the bundling of data and methods that operate on that data within a single unit (class), restricting direct access to some components.

### Benefits
- Data hiding and protection
- Reduced complexity
- Increased reusability
- Easier maintenance

### Access Modifiers
- **Public**: Accessible from anywhere
- **Private**: Accessible only within the class
- **Protected**: Accessible within class and subclasses
- **Package-private** (Java): Accessible within the same package

### Example Concept
```
class BankAccount:
    - private balance
    - public deposit(amount)
    - public withdraw(amount)
    - public getBalance()
```

---

## Abstraction

**Abstraction** is the process of hiding implementation details and showing only essential features of an object.

### Implementation
1. **Abstract Classes**: Cannot be instantiated, may contain abstract methods
2. **Interfaces**: Define a contract of methods without implementation

### Abstract Class vs Interface
| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Methods | Can have implemented methods | Only abstract methods (pre-Java 8) |
| Variables | Can have instance variables | Only constants (static final) |
| Inheritance | Single inheritance | Multiple interfaces |
| Constructor | Can have constructor | Cannot have constructor |

### When to Use
- **Abstract Class**: When classes share common behavior
- **Interface**: When unrelated classes should implement same methods

---

## Inheritance

**Inheritance** allows a class (child/derived) to inherit properties and methods from another class (parent/base).

### Types of Inheritance
1. **Single Inheritance**: One parent, one child
2. **Multilevel Inheritance**: Chain of inheritance (A → B → C)
3. **Hierarchical Inheritance**: One parent, multiple children
4. **Multiple Inheritance**: Multiple parents (supported via interfaces in Java/C#)
5. **Hybrid Inheritance**: Combination of the above

### The Diamond Problem
Occurs in multiple inheritance when a class inherits from two classes that have a common ancestor.
- Solution in Java: Interfaces with default methods
- Solution in C++: Virtual inheritance

### Method Overriding
Child class provides specific implementation of a method already defined in parent class.
- Same method signature
- Runtime polymorphism
- Use `super` to call parent method

---

## Polymorphism

**Polymorphism** allows objects of different classes to be treated as objects of a common parent class.

### Types of Polymorphism

#### 1. Compile-time Polymorphism (Static)
- **Method Overloading**: Same method name, different parameters
- **Operator Overloading**: Same operator, different operands

#### 2. Runtime Polymorphism (Dynamic)
- **Method Overriding**: Child class overrides parent method
- Achieved through inheritance and interfaces
- Method to call is determined at runtime

### Method Overloading vs Overriding
| Overloading | Overriding |
|-------------|------------|
| Same class | Different classes (inheritance) |
| Different parameters | Same parameters |
| Compile-time | Runtime |
| Return type can differ | Return type must be same/covariant |

---

## SOLID Principles

### S - Single Responsibility Principle
A class should have only one reason to change.

### O - Open/Closed Principle
Software entities should be open for extension but closed for modification.

### L - Liskov Substitution Principle
Objects of a superclass should be replaceable with objects of subclasses without breaking the application.

### I - Interface Segregation Principle
Clients should not be forced to depend on interfaces they don't use.

### D - Dependency Inversion Principle
High-level modules should not depend on low-level modules. Both should depend on abstractions.

---

## Design Patterns

### Creational Patterns
1. **Singleton**: Ensure only one instance of a class exists
2. **Factory Method**: Create objects without specifying exact class
3. **Abstract Factory**: Create families of related objects
4. **Builder**: Construct complex objects step by step
5. **Prototype**: Clone existing objects

### Structural Patterns
1. **Adapter**: Make incompatible interfaces work together
2. **Bridge**: Separate abstraction from implementation
3. **Composite**: Compose objects into tree structures
4. **Decorator**: Add responsibilities to objects dynamically
5. **Facade**: Provide simplified interface to complex system
6. **Proxy**: Provide placeholder for another object

### Behavioral Patterns
1. **Observer**: Notify dependents of state changes
2. **Strategy**: Define family of interchangeable algorithms
3. **Command**: Encapsulate request as object
4. **State**: Alter behavior when internal state changes
5. **Template Method**: Define skeleton algorithm

---

## Composition vs Inheritance

### Inheritance ("is-a" relationship)
- Dog is-a Animal
- Strong coupling
- Compile-time relationship

### Composition ("has-a" relationship)
- Car has-a Engine
- Loose coupling
- Runtime flexibility

### Favor Composition Over Inheritance
- More flexible
- Avoids fragile base class problem
- Better encapsulation
- Supports multiple behaviors

---

## Class Relationships

### Association
General relationship between classes.

### Aggregation
"Has-a" relationship where child can exist independently.
Example: Department has Employees

### Composition
"Has-a" relationship where child cannot exist without parent.
Example: House has Rooms

### Dependency
One class uses another temporarily.
Example: Driver uses Car

---

## Common Interview Questions

1. What is the difference between abstract class and interface?
2. Explain method overloading vs overriding
3. What is the diamond problem and how to solve it?
4. Explain SOLID principles with examples
5. What is dependency injection?
6. Difference between composition and inheritance
7. Explain the Singleton pattern and its thread-safe implementation
8. What is loose coupling and how to achieve it?
9. What are access modifiers and their purposes?
10. Explain polymorphism with real-world examples
