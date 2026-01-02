# 🚀 System Guardian Console

**System Guardian Console** is a Python-based monitoring and security tool that helps you keep track of your system’s health, clean temporary files, manage backups, and scan for malware. Built for Python 3.8+, it works on both Windows and Linux.

---

## Features

* Real-time system monitoring (CPU, RAM, Disk, Battery, Temperatures)
* Network and process monitoring
* Scheduled cleanups and task automation
* File and directory analysis
* Malware scanning using MD5 signatures and heuristics
* File quarantine for suspicious files
* Backup and reporting functionality
* Clipboard viewer
* Weather information (via Open-Meteo API)
* Configurable alerts for CPU, RAM, and Disk usage

---

## Installation

1. Ensure Python 3.8+ is installed.
2. Install dependencies:

```bash
pip install psutil colorama requests pyperclip
```

3. Clone the repository:

```bash
git clone https://github.com/yourusername/system-guardian-console.git
cd system-guardian-console
```

---

## Usage

Run the console:

```bash
python3 guardian.py
```

You’ll see a live system monitor. Use commands at the prompt:

```
help
```

Some common commands:

* `clean` — Clean temp files
* `viewlog` / `deletelog` / `logsummary` — Manage cleaning logs
* `backup <dir>` — Backup a directory
* `scheduleclean <minutes>` — Schedule automated cleanups
* `topprocs` — Show top CPU/RAM processes
* `scan <dir>` — Scan a directory for malware
* `heuristics <dir>` — Run heuristic checks for suspicious files
* `quarantine <file>` — Quarantine a suspicious file
* `updatesigs <file>` — Load malware signature file
* `netstatus` / `netconns` — View network status and connections
* `diskinfo` — Check disk usage
* `weather <city>` — Show current weather

Type `help` for the full command list.

---

## Configuration

* Set monitoring intervals and thresholds:

```python
cfg = {
    "interval": 3,          # Monitor refresh interval in seconds
    "cpu_threshold": 85,    # CPU usage alert %
    "mem_threshold": 80,    # RAM usage alert %
    "disk_threshold": 90    # Disk usage alert %
}
```

* Add paths to clean or monitor dynamically using `addpath <dir>`.

---

## Supported Platforms

* Windows
* Linux

---

## Notes

* Make sure you have the necessary permissions for cleaning system directories.
* Malware scanning uses MD5 signature matching and basic heuristics — it is for learning and personal use, not a replacement for antivirus software.
* Always back up important data before running cleanups or quarantine operations.

---

## License

MIT License © Riddhimaan Singh
