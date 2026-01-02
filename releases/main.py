# pysh_shell.py
import os
import sys
import subprocess
import shutil
import urllib.request
import platform
from colorama import init, Fore

os.system('title PySH CLI v1.0.0')
os.system('cls')

# -----------------------------
# Initialize Colorama for Windows 7
# -----------------------------
init(autoreset=True, convert=True)

PLUGIN_DIR = "plugins"

# -----------------------------
# Utilities
# -----------------------------
def detect_package_manager():
    system = platform.system().lower()
    if system == "windows":
        if platform.version().startswith("6.1") and shutil.which("choco"):
            return "choco"
        if shutil.which("winget"):
            return "winget"
        if shutil.which("choco"):
            return "choco"
    return None

def run_with_symmetric_progress(cmd, prefix="[pkg]"):
    """Symmetric fixed-length progress bar with centered percentage"""
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    bar_length = 30

    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            line = line.strip()
            import re
            match = re.search(r'(\d+)%', line)
            if match:
                progress = int(match.group(1))
                perc_str = f"{progress}%"
                total_hyphens = bar_length - len(perc_str)
                filled_hyphens = int(total_hyphens * progress / 100)
                left_filled = filled_hyphens // 2
                right_filled = filled_hyphens - left_filled
                empty_hyphens = total_hyphens - filled_hyphens
                left_empty = empty_hyphens // 2
                right_empty = empty_hyphens - left_empty
                bar = "[" + "-"*left_filled + perc_str + "-"*right_filled + "-"*left_empty + "-"*right_empty + "]"
                sys.stdout.write(f"\r{prefix} {bar}")
                sys.stdout.flush()
            else:
                sys.stdout.write("\n" + Fore.YELLOW + f"{prefix} {line}\n")
                sys.stdout.flush()
    sys.stdout.write("\n")
    return process.returncode

# -----------------------------
# Plugin functions
# -----------------------------
def install_plugin(url, name):
    os.makedirs(PLUGIN_DIR, exist_ok=True)
    if url.endswith(".py"):
        dest = os.path.join(PLUGIN_DIR, f"{name}.py")
        urllib.request.urlretrieve(url, dest)
        print(Fore.GREEN + f"[pkg] Plugin {name} installed ✅")
    else:
        print(Fore.RED + "[pkg] URL must end with .py for raw plugin")

def install_plugin_git(repo_url, name):
    os.makedirs(PLUGIN_DIR, exist_ok=True)
    dest_dir = os.path.join(PLUGIN_DIR, name)
    subprocess.run(["git", "clone", repo_url, dest_dir])
    print(Fore.GREEN + f"[pkg] Git plugin {name} installed ✅")

def remove_plugin(name):
    path_py = os.path.join(PLUGIN_DIR, f"{name}.py")
    path_dir = os.path.join(PLUGIN_DIR, name)
    if os.path.isfile(path_py):
        os.remove(path_py)
        print(Fore.GREEN + f"[pkg] Plugin {name} removed ✅")
    elif os.path.isdir(path_dir):
        shutil.rmtree(path_dir)
        print(Fore.GREEN + f"[pkg] Plugin {name} removed ✅")
    else:
        print(Fore.RED + f"[pkg] Plugin {name} not found ❌")

def list_plugins():
    if not os.path.exists(PLUGIN_DIR):
        print(Fore.YELLOW + "[pkg] No plugins installed")
        return
    for item in os.listdir(PLUGIN_DIR):
        print(Fore.CYAN + item)

# -----------------------------
# System package functions
# -----------------------------
def install_system_package(name):
    pm = detect_package_manager()
    if not pm:
        print(Fore.RED + "[pkg] No supported system package manager found")
        return
    if pm == "choco":
        cmd = ["choco", "install", name, "-y"]
    elif pm == "winget":
        cmd = ["winget", "install", "--id", name, "--accept-source-agreements", "--accept-package-agreements"]
    print(Fore.YELLOW + f"[pkg] Installing {name} using {pm}...")
    code = run_with_symmetric_progress(cmd)
    if code == 0:
        print(Fore.GREEN + f"[pkg] {name} installed successfully ✅")
    else:
        print(Fore.RED + f"[pkg] {name} installation failed ❌")

def remove_system_package(name):
    pm = detect_package_manager()
    if not pm:
        print(Fore.RED + "[pkg] No supported system package manager found")
        return
    if pm == "choco":
        cmd = ["choco", "uninstall", name, "-y"]
    elif pm == "winget":
        cmd = ["winget", "uninstall", "--id", name]
    print(Fore.YELLOW + f"[pkg] Removing {name} using {pm}...")
    run_with_symmetric_progress(cmd)

# -----------------------------
# Execute system command
# -----------------------------
def execute_system_command(command):
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(Fore.RED + f"[shell] Error: {e}")

# -----------------------------
# Main interactive shell
# -----------------------------
def main_shell():
    print(Fore.GREEN + "PySH CLI [v1.0.0]\nCopyright (c) 2025 Riddhimaan Singh. All rights reserved.\n")
    while True:
        try:
            cwd = os.getcwd()
            # Fixed prompt for Windows 7, no '<-[0m' issue
            cmd_input = input(f"PySH:{cwd}> ").strip()
            if not cmd_input:
                continue
            if cmd_input.lower() in ["exit", "quit"]:
                print(Fore.GREEN + "Exiting PySH CLI...")
                break
            parts = cmd_input.split()
            cmd = parts[0].lower()
            args = parts[1:]

            # Built-in commands
            if cmd == "help":
                print(Fore.YELLOW + "PySH CLI Commands:")
                print("  exit/quit                      Exit CLI")
                print("  help                           Show this help")
                print("  cd <path>                      Change directory")
                print("  dir / ls                        List files")
                print("  mkdir <name>                   Make directory")
                print("  rmdir <name>                   Remove directory")
                print("  install <package_name>         Install system package")
                print("  remove <package_name>          Remove system package")
                print("  install-plugin <url> <name>    Install plugin from URL (.py)")
                print("  install-plugin-git <url> <name> Install plugin from Git repo")
                print("  remove-plugin <name>           Remove plugin")
                print("  list-plugins                   List all installed plugins")
            elif cmd == "cd":
                if args:
                    try:
                        os.chdir(args[0])
                    except FileNotFoundError:
                        print(Fore.RED + "[shell] Directory not found")
                else:
                    print(Fore.YELLOW + "[shell] Usage: cd <path>")
            elif cmd in ["dir", "ls"]:
                for f in os.listdir(os.getcwd()):
                    print(Fore.CYAN + f)
            elif cmd == "mkdir":
                if args:
                    os.makedirs(args[0], exist_ok=True)
                else:
                    print(Fore.YELLOW + "[shell] Usage: mkdir <name>")
            elif cmd == "rmdir":
                if args:
                    try:
                        shutil.rmtree(args[0])
                    except FileNotFoundError:
                        print(Fore.RED + "[shell] Directory not found")
                else:
                    print(Fore.YELLOW + "[shell] Usage: rmdir <name>")
            # Package manager commands
            elif cmd == "install" and args:
                install_system_package(args[0])
            elif cmd == "remove" and args:
                remove_system_package(args[0])
            elif cmd == "install-plugin" and len(args) == 2:
                install_plugin(args[0], args[1])
            elif cmd == "install-plugin-git" and len(args) == 2:
                install_plugin_git(args[0], args[1])
            elif cmd == "remove-plugin" and len(args) == 1:
                remove_plugin(args[0])
            elif cmd == "list-plugins":
                list_plugins()
            else:
                # Execute as system command
                execute_system_command(cmd_input)

        except KeyboardInterrupt:
            print("\n" + Fore.GREEN + "Use 'exit' or 'quit' to leave PySH CLI")

if __name__ == "__main__":
    main_shell()
