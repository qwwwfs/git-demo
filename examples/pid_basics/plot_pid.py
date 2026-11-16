"""Plot verified CSV output from the independent desktop PID demo.

Not a real balancing-robot measurement. Usage:
    pip install matplotlib
    python examples/pid_basics/plot_pid.py
"""
from pathlib import Path
import csv

import matplotlib.pyplot as plt

base = Path(__file__).resolve().parent
csv_path = base / "results" / "pid_step.csv"
with csv_path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

t = [float(r["time_s"]) for r in rows]
target = [float(r["target"]) for r in rows]
measured = [float(r["measurement"]) for r in rows]

plt.plot(t, target, linestyle="--", label="target")
plt.plot(t, measured, label="first-order plant output")
plt.xlabel("time (s)")
plt.ylabel("response")
plt.title("PID teaching example (not robot measurement)")
plt.legend()
plt.tight_layout()
plt.savefig(base / "results" / "pid_step.png", dpi=150)
print(base / "results" / "pid_step.png")
