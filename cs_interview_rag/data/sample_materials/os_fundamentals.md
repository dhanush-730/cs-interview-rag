# Operating Systems - CS Interview Study Material

## Process Management

### What is a Process?
A **process** is a program in execution. It includes:
- Program code (text section)
- Current activity (program counter, registers)
- Stack (temporary data)
- Data section (global variables)
- Heap (dynamically allocated memory)

### Process States
1. **New**: Process is being created
2. **Ready**: Process is waiting to be assigned to a processor
3. **Running**: Instructions are being executed
4. **Waiting**: Process is waiting for an event
5. **Terminated**: Process has finished execution

### Process Control Block (PCB)
Data structure containing:
- Process ID (PID)
- Process state
- Program counter
- CPU registers
- Memory management info
- I/O status information
- Scheduling information

---

## Threads

### What is a Thread?
A **thread** is the smallest unit of CPU execution. A process can have multiple threads sharing:
- Code section
- Data section
- OS resources (open files, signals)

Each thread has its own:
- Thread ID
- Program counter
- Register set
- Stack

### Process vs Thread
| Process | Thread |
|---------|--------|
| Heavy weight | Light weight |
| Own memory space | Shares memory with other threads |
| More isolation | Less isolation |
| Expensive context switch | Cheaper context switch |
| IPC needed for communication | Can directly communicate |

### Multithreading Models
1. **Many-to-One**: Many user threads → one kernel thread
2. **One-to-One**: Each user thread → one kernel thread
3. **Many-to-Many**: Many user threads → many kernel threads

---

## CPU Scheduling

### Scheduling Criteria
- **CPU Utilization**: Keep CPU as busy as possible
- **Throughput**: Number of processes completed per time unit
- **Turnaround Time**: Time from submission to completion
- **Waiting Time**: Time spent in ready queue
- **Response Time**: Time from request to first response

### Scheduling Algorithms

#### 1. First-Come, First-Served (FCFS)
- Non-preemptive
- Simple but may cause convoy effect
- Not optimal for time-sharing systems

#### 2. Shortest Job First (SJF)
- Optimal for minimizing average waiting time
- Can be preemptive (SRTF) or non-preemptive
- Requires knowing burst time in advance

#### 3. Priority Scheduling
- Each process has a priority
- May cause starvation (solved by aging)
- Can be preemptive or non-preemptive

#### 4. Round Robin (RR)
- Time quantum for each process
- Preemptive FCFS
- Good for time-sharing systems
- Performance depends on quantum size

#### 5. Multilevel Queue
- Multiple queues with different priorities
- Each queue can have its own scheduling algorithm

#### 6. Multilevel Feedback Queue
- Processes can move between queues
- Based on CPU burst characteristics

---

## Process Synchronization

### Race Condition
When multiple processes access shared data concurrently, and the outcome depends on the execution order.

### Critical Section Problem
Requirements for solution:
1. **Mutual Exclusion**: Only one process in critical section
2. **Progress**: If no process is in CS, selection cannot be postponed indefinitely
3. **Bounded Waiting**: Limit on number of times others can enter CS

### Synchronization Mechanisms

#### 1. Mutex (Mutual Exclusion)
- Lock before entering critical section
- Unlock after leaving
- Only one process can hold the lock

#### 2. Semaphore
- **Binary Semaphore**: Similar to mutex (0 or 1)
- **Counting Semaphore**: Can have integer values
- Operations: wait() and signal()

#### 3. Monitor
- High-level synchronization construct
- Encapsulates shared data and operations
- Only one process can be active in monitor

### Classical Synchronization Problems
1. **Producer-Consumer**: Bounded buffer problem
2. **Readers-Writers**: Multiple readers, single writer
3. **Dining Philosophers**: Resource allocation

---

## Deadlock

### Conditions for Deadlock
All four must hold simultaneously:
1. **Mutual Exclusion**: Resource held exclusively
2. **Hold and Wait**: Process holds resources while waiting for others
3. **No Preemption**: Resources cannot be forcibly taken
4. **Circular Wait**: Circular chain of waiting processes

### Deadlock Handling

#### 1. Prevention
Break one of the four conditions:
- Mutual Exclusion: Not possible for some resources
- Hold and Wait: Request all resources at start
- No Preemption: Allow preemption
- Circular Wait: Order resource requests

#### 2. Avoidance
- Use resource allocation graph
- Banker's Algorithm: Ensure safe state before allocation

#### 3. Detection
- Periodically check for cycles
- Use wait-for graph

#### 4. Recovery
- Process termination
- Resource preemption

---

## Memory Management

### Memory Allocation Strategies
1. **First Fit**: Allocate first hole big enough
2. **Best Fit**: Allocate smallest hole big enough
3. **Worst Fit**: Allocate largest hole

### Fragmentation
- **External**: Free memory scattered in small blocks
- **Internal**: Allocated memory larger than needed

### Paging
- Divide physical memory into fixed-size frames
- Divide logical memory into pages of same size
- Page table maps pages to frames
- No external fragmentation

### Segmentation
- Divide memory into variable-size segments
- Each segment has base and limit
- Supports user view of memory

---

## Virtual Memory

### Concept
Allow execution of processes not completely in memory.

### Demand Paging
- Load pages only when needed
- Page fault when accessing non-resident page

### Page Replacement Algorithms
1. **FIFO**: Replace oldest page
2. **Optimal**: Replace page not used for longest time
3. **LRU (Least Recently Used)**: Replace least recently used page
4. **LFU (Least Frequently Used)**: Replace least frequently used page

### Thrashing
Occurs when process spends more time paging than executing.
- Cause: Too many processes, not enough memory
- Solution: Working set model, page fault frequency

---

## File Systems

### File Allocation Methods
1. **Contiguous**: Files stored in consecutive blocks
2. **Linked**: Each block points to next block
3. **Indexed**: Index block contains pointers to all blocks

### Directory Structure
1. **Single-Level**: All files in one directory
2. **Two-Level**: Separate directory for each user
3. **Tree-Structured**: Hierarchy of directories
4. **Acyclic-Graph**: Shared subdirectories
5. **General Graph**: Links allowed (may have cycles)

---

## Common Interview Questions

1. Difference between process and thread?
2. Explain context switching
3. What is a deadlock? How to prevent it?
4. Compare different CPU scheduling algorithms
5. Explain virtual memory and demand paging
6. What is thrashing and how to avoid it?
7. Difference between paging and segmentation
8. Explain semaphore vs mutex
9. What is a race condition?
10. Describe page replacement algorithms
