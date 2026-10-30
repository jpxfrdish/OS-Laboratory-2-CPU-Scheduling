
from collections import deque

# MODIFIED DATASET
# Used for FCFS, SJF, Priority, and Round Robin
PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 6, "priority": 2},
    {"pid": "P2", "at": 0, "bt": 3, "priority": 4},
    {"pid": "P3", "at": 0, "bt": 8, "priority": 1},
    {"pid": "P4", "at": 0, "bt": 4, "priority": 3}
]

# SEPARATE DATASET FOR SRTF
SRTF_PROCESSES = [
    {"pid": "P1", "at": 0, "bt": 8, "priority": 2},
    {"pid": "P2", "at": 1, "bt": 4, "priority": 1},
    {"pid": "P3", "at": 2, "bt": 2, "priority": 4},
    {"pid": "P4", "at": 3, "bt": 1, "priority": 3}
]


def add_gantt(gantt, pid, start, end):
    if (gantt and gantt[-1][0] == pid
            and gantt[-1][2] == start):
        gantt[-1] = (pid, gantt[-1][1], end)
    else:
        gantt.append((pid, start, end))


def calculate_results(processes, first_start, completion):
    results = []

    for p in processes:
        pid = p["pid"]
        at = p["at"]
        bt = p["bt"]

        ct = completion[pid]
        tat = ct - at
        wt = tat - bt
        rt = first_start[pid] - at

        results.append({
            "pid": pid,
            "ct": ct,
            "tat": tat,
            "wt": wt,
            "rt": rt
        })

    return results


def display(name, gantt, results):
    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    print("Gantt Chart:")
    print(" | ".join(
        f"{pid} [{start}-{end}]"
        for pid, start, end in gantt
    ))

    print("\nProcess Results:")
    print(f"{'PID':<8}{'CT':<8}{'TAT':<8}{'WT':<8}{'RT':<8}")

    for r in results:
        print(
            f"{r['pid']:<8}{r['ct']:<8}"
            f"{r['tat']:<8}{r['wt']:<8}{r['rt']:<8}"
        )

    n = len(results)
    avg_wt = sum(r["wt"] for r in results) / n
    avg_tat = sum(r["tat"] for r in results) / n
    avg_rt = sum(r["rt"] for r in results) / n

    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    print(f"Average Response Time: {avg_rt:.2f}")

    return avg_wt, avg_tat, avg_rt


# 1. FIRST COME FIRST SERVED
def fcfs(processes):
    ps = sorted(
        processes,
        key=lambda p: (p["at"], p["pid"])
    )

    time = 0
    gantt = []
    first_start = {}
    completion = {}

    for p in ps:
        if time < p["at"]:
            time = p["at"]

        pid = p["pid"]
        first_start[pid] = time

        start = time
        time += p["bt"]

        add_gantt(gantt, pid, start, time)
        completion[pid] = time

    results = calculate_results(ps, first_start, completion)
    return display("FCFS", gantt, results)


# 2. NON-PREEMPTIVE SJF
def sjf(processes):
    ps = sorted(
        processes,
        key=lambda p: (p["bt"], p["at"], p["pid"])
    )

    time = 0
    gantt = []
    first_start = {}
    completion = {}

    for p in ps:
        if time < p["at"]:
            time = p["at"]

        pid = p["pid"]
        first_start[pid] = time

        start = time
        time += p["bt"]

        add_gantt(gantt, pid, start, time)
        completion[pid] = time

    results = calculate_results(ps, first_start, completion)
    return display("SJF (Non-Preemptive)", gantt, results)


# 3. NON-PREEMPTIVE PRIORITY SCHEDULING
def priority_scheduling(processes):
    ps = sorted(
        processes,
        key=lambda p: (p["priority"], p["at"], p["pid"])
    )

    time = 0
    gantt = []
    first_start = {}
    completion = {}

    for p in ps:
        if time < p["at"]:
            time = p["at"]

        pid = p["pid"]
        first_start[pid] = time

        start = time
        time += p["bt"]

        add_gantt(gantt, pid, start, time)
        completion[pid] = time

    results = calculate_results(ps, first_start, completion)
    return display("Priority Scheduling", gantt, results)


# 4. ROUND ROBIN
def round_robin(processes, quantum=2):
    ps = sorted(
        processes,
        key=lambda p: (p["at"], p["pid"])
    )

    remaining = {p["pid"]: p["bt"] for p in ps}
    ready_queue = deque(p["pid"] for p in ps)
    lookup = {p["pid"]: p for p in ps}

    time = 0
    gantt = []
    first_start = {}
    completion = {}

    while ready_queue:
        pid = ready_queue.popleft()

        if pid not in first_start:
            first_start[pid] = time

        run_time = min(quantum, remaining[pid])

        start = time
        time += run_time
        remaining[pid] -= run_time

        add_gantt(gantt, pid, start, time)

        if remaining[pid] > 0:
            ready_queue.append(pid)
        else:
            completion[pid] = time

    results = calculate_results(ps, first_start, completion)
    return display(
        f"Round Robin (Quantum = {quantum})",
        gantt,
        results
    )


# 5. SHORTEST REMAINING TIME FIRST
def srtf(processes):
    ps = processes

    remaining = {p["pid"]: p["bt"] for p in ps}
    first_start = {}
    completion = {}
    gantt = []

    time = 0
    completed = 0
    n = len(ps)

    while completed < n:
        available = [
            p for p in ps
            if p["at"] <= time
            and remaining[p["pid"]] > 0
        ]

        if not available:
            time += 1
            continue

        current = min(
            available,
            key=lambda p: (
                remaining[p["pid"]],
                p["at"],
                p["pid"]
            )
        )

        pid = current["pid"]

        if pid not in first_start:
            first_start[pid] = time

        add_gantt(gantt, pid, time, time + 1)

        remaining[pid] -= 1
        time += 1

        if remaining[pid] == 0:
            completion[pid] = time
            completed += 1

    results = calculate_results(ps, first_start, completion)
    return display("SRTF", gantt, results)


# MAIN PROGRAM
if __name__ == "__main__":

    print("CPU SCHEDULING SIMULATOR")
    print("Modified Dataset")

    fcfs(PROCESSES)
    sjf(PROCESSES)
    priority_scheduling(PROCESSES)
    round_robin(PROCESSES, quantum=2)

    # SRTF uses its own separate dataset
    srtf(SRTF_PROCESSES)
