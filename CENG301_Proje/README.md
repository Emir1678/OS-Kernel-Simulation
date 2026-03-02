#  CPU Process Scheduling Simulator

**Student Name:** Mehmet Emir YURT
**Student ID:** 230201026 
**Section:** 1

## 1. Project Overview
In this project, I have designed and implemented a modular CPU Process Scheduling Simulator in **Python 3**. The simulator supports multiple classical scheduling algorithms and generates detailed execution logs, performance statistics, and graphical outputs.

## 2. Implemented Algorithms
The simulator includes the following six algorithms, handling process arrival times and ties (via PID order) deterministically:

1. **FCFS (First-Come First-Served):** Non-preemptive algorithm that executes processes in their arrival order.
2. **SJF (Shortest Job First):** Non-preemptive algorithm that selects the process with the shortest burst time.
3. **SRTF (Shortest Remaining Time First):** Preemptive version of SJF that switches to a shorter task if it arrives.
4. **Round Robin (RR):** Preemptive scheduling using a configurable time quantum.
5. **Priority (Non-Preemptive):** Executes processes based on their priority values; lower values indicate higher priority.
6. **Priority (Preemptive):** Preempts the current process if a higher-priority one arrives.

## 3. Requirements & Dependencies
- **Python Version:** 3.x
- **Standard Libraries:** `argparse`, `sys`, `os`, `copy`
- **External Libraries:** `matplotlib` (used for generating performance graphs).

## 4. How to Run
The simulator is managed via `scheduler.py` using command-line arguments.

### Single Algorithm Execution:
```bash
python scheduler.py --input processes.txt --algo RR --quantum 4

## Comparison Mode(Generate Graphs):
-To run all algorithms and automatically generate comparison graphs in the graphs/ directory:

- **python scheduler.py --input processes.txt --algo COMPARE

## 5. Project Structure:
The source code is organized in a modular and readable form:
scheduler.py: Main entry point and CLI management.

algorithms/: Directory containing separate modules for each scheduling logic.

utils/:

parser.py: Logic for reading processes.txt and defining the Process class.

statistics.py: Calculation of metrics (Waiting, Turnaround, Response) and graph generation.

gantt.py: ASCII Gantt chart generation.

graphs/: Stores generated waiting.png and turnaround.png files.

## 6. Input Files Format:
The input file (processes.txt) uses whitespace-separated fields and supports comments starting with #:
# pid arrival_time burst_time priority
P1 0 8 2
P2 1 4 1

## 7.Results & Discussion:
Best Performing Algorithm
Based on the generated graphs, SRTF typically performed best in terms of minimizing Average Waiting Time and Average Turnaround Time. This is expected as SRTF prioritizes shorter tasks, allowing the system to complete more processes in less time, thereby reducing the average wait.

Observations
Round Robin (RR): I observed that a smaller time quantum leads to a much higher Context Switch Count, which introduces overhead, while a very large quantum makes RR behave like FCFS.

Priority Scheduling: Higher priority tasks finish very quickly, but I observed that lower priority tasks can face "starvation" if high-priority tasks keep arriving.

## 8. Submission Checklist:

[ ] All Python source files (.py)

[ ] processes.txt test file

[ ] graphs/ directory with waiting.png and turnaround.png

[ ] screenshots/ of terminal outputs (Gantt charts and tables)

[ ] execution_log.txt (Detailed timeline log)

## 9. Result & Discussion:

Best Algorithm: SRTF performed best with the lowest Average Waiting Time (6.60) and Turnaround Time (12.20) by prioritizing the shortest remaining tasks.

Context Switches: Round Robin (RR) caused the highest overhead with 13 context switches (Quantum=2), significantly more than other algorithms.

Priority Performance: Both Priority algorithms showed identical results (11.40 wait time), suggesting preemption didn't change the execution order for this specific workload.

FCFS Drawback: FCFS had the highest Average Response Time (11.40) because it lacks preemption or task prioritization.