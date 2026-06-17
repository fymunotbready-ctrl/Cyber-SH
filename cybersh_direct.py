#!/usr/bin/env python3
# version: 1.2
"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝
  CYBER SH DIRECT — No Server · Pure Python · llama-cpp-python
"""

import sys, os, json, time, shutil, re, subprocess, threading, datetime, textwrap, argparse, glob, readline

# ══════════════════════════════════════════════════════════════
#  AUTO-UPDATER
# ══════════════════════════════════════════════════════════════
REPO_RAW    = "https://raw.githubusercontent.com/neo4-svg/cybersh/main"
VERSION_URL = f"{REPO_RAW}/version.txt"
SCRIPT_URL  = f"{REPO_RAW}/cybersh_direct.py"
REQS_URL    = f"{REPO_RAW}/requirements.txt"

def _http_get(url: str, timeout: int = 10) -> str | None:
    try:
        import urllib.request, ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "cybersh-updater/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None

def _is_online() -> bool:
    import socket
    for host, port in [("github.com", 443), ("8.8.8.8", 53), ("1.1.1.1", 53)]:
        try:
            socket.setdefaulttimeout(3)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port)); s.close()
            return True
        except Exception:
            continue
    return False

def _detect_os() -> dict:
    import platform
    info = {
        "system":  platform.system(),
        "distro":  "",
        "pkg_mgr": None,
        "pip_flag": [],
        "is_venv": sys.prefix != sys.base_prefix,
    }
    if info["system"] == "Linux":
        os_release = {}
        for path in ("/etc/os-release", "/usr/lib/os-release"):
            try:
                with open(path) as f:
                    for line in f:
                        k, _, v = line.strip().partition("=")
                        os_release[k] = v.strip('"')
                break
            except Exception:
                pass
        distro_id = os_release.get("ID", "").lower()
        like      = os_release.get("ID_LIKE", "").lower()
        info["distro"] = os_release.get("PRETTY_NAME", distro_id)
        apt_ids    = {"debian","ubuntu","kali","parrot","linuxmint","pop","elementary","mx","zorin","raspbian"}
        dnf_ids    = {"fedora","rhel","centos","almalinux","rocky","ol","nobara"}
        pacman_ids = {"arch","manjaro","endeavouros","garuda","artix","cachyos"}
        zypper_ids = {"opensuse","suse","opensuse-leap","opensuse-tumbleweed"}
        apk_ids    = {"alpine"}
        all_ids    = {distro_id} | set(like.split())
        if   all_ids & apt_ids:    info["pkg_mgr"] = "apt"
        elif all_ids & dnf_ids:    info["pkg_mgr"] = "dnf"
        elif all_ids & pacman_ids: info["pkg_mgr"] = "pacman"
        elif all_ids & zypper_ids: info["pkg_mgr"] = "zypper"
        elif all_ids & apk_ids:    info["pkg_mgr"] = "apk"
        if not info["is_venv"]:
            info["pip_flag"] = ["--break-system-packages"]
    elif info["system"] == "Darwin":
        info["distro"] = "macOS"; info["pkg_mgr"] = "brew"
    elif info["system"] == "Windows":
        info["distro"] = "Windows"
    return info

def _install_packages(pkgs: list) -> None:
    G="\033[38;5;82m"; C="\033[38;5;51m"; Y="\033[38;5;226m"; D="\033[2m"; R2="\033[0m"
    os_info = _detect_os()
    flag    = os_info["pip_flag"]
    print(f"  {D}OS: {os_info['distro'] or os_info['system']}{R2}")
    for pkg in pkgs:
        print(f"  {C}→{R2} {pkg}", end="", flush=True)
        pip_cmd = [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--upgrade"] + flag
        r = subprocess.run(pip_cmd, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"\r  {G}✓{R2} {pkg}                    "); continue
        # fallback: without flag
        r2 = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--upgrade"],
            capture_output=True, text=True)
        if r2.returncode == 0:
            print(f"\r  {G}✓{R2} {pkg}                    "); continue
        # fallback: system package manager
        pm = os_info["pkg_mgr"]
        if pm:
            pm_cmds = {
                "apt":    ["sudo","apt","install","-y",f"python3-{pkg}"],
                "dnf":    ["sudo","dnf","install","-y",f"python3-{pkg}"],
                "pacman": ["sudo","pacman","-S","--noconfirm",f"python-{pkg}"],
                "zypper": ["sudo","zypper","install","-y",f"python3-{pkg}"],
                "apk":    ["sudo","apk","add",f"py3-{pkg}"],
            }
            r3 = subprocess.run(pm_cmds[pm], capture_output=True, text=True)
            if r3.returncode == 0:
                print(f"\r  {G}✓{R2} {pkg} {D}(via {pm}){R2}              "); continue
        err = (r.stderr or "").strip().split("\n")[-1][:60]
        print(f"\r  {Y}⚠{R2} {pkg} — {D}{err}{R2}")
        print(f"    {D}Manual: pip install {pkg} --break-system-packages{R2}")

def check_and_update(force: bool = False) -> None:
    G="\033[38;5;82m"; C="\033[38;5;51m"; Y="\033[38;5;226m"
    B="\033[1m"; D="\033[2m"; R2="\033[0m"

    this_file = os.path.realpath(os.path.abspath(__file__))

    # read local version from line 2
    local_ver = "0.0.0"
    try:
        with open(this_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("# version:"):
                    local_ver = line.split(":", 1)[1].strip(); break
    except Exception:
        pass

    print(f"\n{C}🔄 Checking for updates…{R2}", end="", flush=True)

    if not force and not _is_online():
        print(f"\r{D}  ↷ No internet — skipping update check.{R2}          \n")
        return

    remote_ver = _http_get(VERSION_URL)
    if not remote_ver:
        print(f"\r{D}  ↷ Could not reach GitHub — skipping.{R2}            \n")
        return

    remote_ver = remote_ver.strip()

    def ver_tuple(v):
        try: return tuple(int(x) for x in v.split("."))
        except: return (0, 0, 0)

    if not force and ver_tuple(remote_ver) <= ver_tuple(local_ver):
        print(f"\r{G}  ✓ Up to date (v{local_ver}){R2}                          \n")
        return

    print(f"\r{Y}  ✦ Update: v{local_ver} → v{remote_ver}{R2}                    ")
    print(f"  {D}Downloading…{R2}", end="", flush=True)

    new_code = _http_get(SCRIPT_URL)
    if not new_code or len(new_code) < 1000:
        print(f"\r\033[38;5;196m  ✗ Download failed — keeping current version.{R2}\n"); return

    # validate python syntax before overwriting
    try:
        import ast as _ast; _ast.parse(new_code)
    except SyntaxError:
        print(f"\r\033[38;5;196m  ✗ Downloaded file invalid — aborting.{R2}\n"); return

    # backup
    backup = this_file + f".backup_v{local_ver}"
    try:
        import shutil as _sh; _sh.copy2(this_file, backup)
        print(f"\r  {D}Backup: {os.path.basename(backup)}{R2}                         ")
    except Exception:
        pass

    # write new file
    try:
        with open(this_file, "w", encoding="utf-8") as f: f.write(new_code)
    except PermissionError:
        print(f"\r\033[38;5;196m  ✗ Permission denied. Try: chmod +w {this_file}{R2}\n"); return
    except Exception as e:
        print(f"\r\033[38;5;196m  ✗ Write error: {e}{R2}\n"); return

    # install/update dependencies
    new_reqs = _http_get(REQS_URL)
    if new_reqs:
        pkgs = [l.strip() for l in new_reqs.splitlines()
                if l.strip() and not l.startswith("#") and not l.startswith("-")]
        if pkgs:
            print(f"  {C}📦 Installing dependencies…{R2}")
            _install_packages(pkgs)

    print(f"\n{G}{B}  ✓ Updated to v{remote_ver} — restarting!{R2}\n")
    time.sleep(1)
    os.execv(sys.executable, [sys.executable, this_file] + sys.argv[1:])

# ══════════════════════════════════════════════════════════════
#  ANSI
# ══════════════════════════════════════════════════════════════
R      = "\033[0m";  BOLD  = "\033[1m";  DIM   = "\033[2m"
NEON_G = "\033[38;5;82m";  NEON_C = "\033[38;5;51m"
NEON_P = "\033[38;5;201m"; NEON_Y = "\033[38;5;226m"
NEON_O = "\033[38;5;208m"; NEON_R = "\033[38;5;196m"
BOLD_C = f"\033[1m{NEON_C}"; BOLD_Y = f"\033[1m{NEON_Y}"
CLEAR  = "\033[2K\r"

# ══════════════════════════════════════════════════════════════
#  RICH INPUT BAR — Claude-style typing experience
# ══════════════════════════════════════════════════════════════
ALL_COMMANDS = [
    "/vibe","/sec","/code","/chat","/agent","/help","/exit","/quit",
    "/clear","/history","/temp","/info","/save","/f","/o","/run","/copy",
    "/recon","/payload","/explain","/cvesearch","/web","/models",
    "/tldr","/howto","/fix","/passgen","/encode","/syswatch",
    "/benchmark","/note","/notes","/tip",
    "/explaincode","/roast","/challenge","/recap","/translate","/weather",
    "/timer","/rename","/regex","/git","/ctf","/diff",
    "/remember","/memories","/memory","/forget",
    "/persona","/summarize","/calc","/goals","/goal",
    "--update","--no-update",
]

class RichInput:
    """Claude-style input bar with autocomplete, history nav, and live char count."""

    def __init__(self):
        self._setup_readline()

    def _setup_readline(self):
        try:
            readline.set_completer(self._completer)
            readline.set_completer_delims(" \t")
            readline.parse_and_bind("tab: complete")
            # history
            hist = os.path.expanduser("~/.cybersh_input_history")
            try:
                readline.read_history_file(hist)
            except FileNotFoundError:
                pass
            readline.set_history_length(500)
            import atexit
            atexit.register(readline.write_history_file, hist)
        except Exception:
            pass

    def _completer(self, text, state):
        options = [c for c in ALL_COMMANDS if c.startswith(text)]
        return options[state] if state < len(options) else None

    def read(self, prompt: str, multiline_hint: bool = True) -> str:
        """Read input with rich prompt. Shift+Enter hint shown. Returns stripped text."""
        try:
            # show char count hint for long inputs
            text = input(prompt)
            return text.strip()
        except (EOFError, KeyboardInterrupt):
            raise KeyboardInterrupt

_rich_input = RichInput()

def rich_prompt(mode_color: str, icon: str, cwd: str) -> str:
    """Render the Claude-style input bar and return user input."""
    w = min(shutil.get_terminal_size((80, 24)).columns, 80)

    # top border
    sys.stdout.write(f"\n{DIM}{'─' * w}{R}\n")

    # prompt line
    prompt = f"{mode_color}{BOLD}{icon} {R}{NEON_C}[{cwd}]{R}{DIM} ▶ {R}"
    try:
        text = _rich_input.read(prompt)
    except KeyboardInterrupt:
        print()
        raise

    return text

# ══════════════════════════════════════════════════════════════
#  EXPERIMENTAL FEATURES
# ══════════════════════════════════════════════════════════════

def cmd_explain_code(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """Paste a code snippet and AI explains every line."""
    if arg:
        code = arg
    else:
        print(f"{NEON_Y}Paste your code (type END on a new line when done):{R}")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END": break
                lines.append(line)
            except EOFError: break
        code = "\n".join(lines)
    if not code: return ""
    return ask(cfg, messages, session_msgs,
        f"Explain this code line by line in plain English. "
        f"Format each explanation as: `line` → what it does.\n\n```\n{code}\n```")

def cmd_roast(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """AI roasts your code — finds bad practices with humor."""
    code = arg
    if not code:
        print(f"{NEON_Y}Paste your code to roast (END to finish):{R}")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END": break
                lines.append(line)
            except EOFError: break
        code = "\n".join(lines)
    if not code: return ""
    return ask(cfg, messages, session_msgs,
        f"Roast this code like a senior dev who's seen it all. "
        f"Be funny but accurate — point out every bad practice, naming issue, "
        f"security hole, and inefficiency. Then at the end give the fixed version.\n\n```\n{code}\n```")

def cmd_challenge(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """AI gives you a coding or hacking challenge to solve."""
    level = arg.lower() if arg else "medium"
    mode  = cfg.get("mode", "chat")
    if mode == "sec":
        topic = "penetration testing or CTF"
    elif mode in ("code", "vibe"):
        topic = "programming"
    else:
        topic = "Linux or general tech"
    return ask(cfg, messages, session_msgs,
        f"Give me a {level} difficulty {topic} challenge. "
        f"Format: 1) Challenge title. 2) Description. 3) What I need to do. "
        f"4) Hints (hidden in a spoiler block using >! syntax). "
        f"5) What a correct solution looks like (also hidden). Make it fun and interesting.")

def cmd_recap(messages: list) -> None:
    """AI-style recap of this session so far."""
    w   = min(shutil.get_terminal_size((80,24)).columns, 70)
    div = f"{NEON_C}{'─'*w}{R}"
    print(f"\n{div}")
    print(f"{NEON_C}{BOLD}  📋 Session Recap{R}")
    print(div)
    count = 0
    for m in messages:
        if m["role"] == "user" and not m["content"].startswith("["):
            count += 1
            preview = textwrap.shorten(m["content"], 65)
            print(f"  {NEON_Y}{count:>2}.{R} {preview}")
    if count == 0:
        print(f"  {DIM}No messages yet.{R}")
    print(f"\n  {DIM}Total exchanges: {count}{R}")
    print(f"{div}\n")

def cmd_translate(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """Translate any text to any language."""
    if not arg:
        print(f"{NEON_Y}Usage: /translate <lang> <text>")
        print(f"Example: /translate arabic Hello how are you{R}\n")
        return ""
    parts = arg.split(maxsplit=1)
    lang  = parts[0]
    text  = parts[1] if len(parts) > 1 else ""
    if not text:
        print(f"{NEON_Y}Usage: /translate <language> <text>{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"Translate this to {lang}. Show only the translation, nothing else:\n{text}")

def cmd_weather_ascii(arg: str) -> None:
    """Fetch weather as ASCII art using wttr.in."""
    loc = arg.strip() or ""
    url = f"https://wttr.in/{loc}?A"
    print(f"\n{NEON_C}🌤 Fetching weather…{R}\n")
    r = subprocess.run(["curl","-s","--max-time","5", url],
                       capture_output=True, text=True)
    if r.returncode == 0 and r.stdout:
        print(r.stdout)
    else:
        print(f"{NEON_R}✗ Could not fetch weather. Check internet.{R}\n")

def cmd_timer(arg: str) -> None:
    """Countdown timer. /timer 5m or /timer 30s or /timer 1h"""
    import time as _time
    if not arg:
        print(f"{NEON_Y}Usage: /timer 30s | /timer 5m | /timer 1h{R}\n"); return
    arg = arg.strip().lower()
    try:
        if arg.endswith("h"):   secs = int(arg[:-1]) * 3600
        elif arg.endswith("m"): secs = int(arg[:-1]) * 60
        elif arg.endswith("s"): secs = int(arg[:-1])
        else:                   secs = int(arg)
    except ValueError:
        print(f"{NEON_R}✗ Invalid time. Use 30s, 5m, or 1h.{R}\n"); return

    total = secs
    print(f"\n{NEON_C}⏱  Timer: {arg}{R}  {DIM}(Ctrl+C to stop){R}\n")
    try:
        while secs > 0:
            h, rem = divmod(secs, 3600)
            m, s   = divmod(rem, 60)
            bar_w  = 30
            filled = int(bar_w * (total - secs) / total)
            bar    = f"{NEON_G}{'█'*filled}{DIM}{'░'*(bar_w-filled)}{R}"
            ts     = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
            sys.stdout.write(f"\r  {bar}  {NEON_Y}{BOLD}{ts}{R}  ")
            sys.stdout.flush()
            _time.sleep(1)
            secs -= 1
        sys.stdout.write(f"\r{CLEAR}")
        print(f"\n{NEON_G}{BOLD}  ✓ TIME'S UP! 🔔{R}\n")
        # terminal bell
        sys.stdout.write("\a"); sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write(f"\r{CLEAR}")
        print(f"\n{NEON_Y}  Timer stopped.{R}\n")

def cmd_ai_rename(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """AI suggests better names for variables, functions, files."""
    if not arg:
        print(f"{NEON_Y}Usage: /rename <name>  — AI suggests better names{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"Suggest 5 better names for this identifier: `{arg}`\n"
        f"Consider: clarity, convention (snake_case for Python, camelCase for JS), "
        f"and what the name implies. Format as a numbered list with a one-line reason for each.")

def cmd_regex(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """AI writes a regex for you."""
    if not arg:
        print(f"{NEON_Y}Usage: /regex <describe what to match>{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"Write a regex pattern for: {arg}\n"
        f"Format: 1) The pattern. 2) Language-specific examples (Python, JS, grep). "
        f"3) Explanation of each part. 4) Test cases showing matches and non-matches.")

def cmd_githelp(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """AI explains or generates git commands."""
    if not arg:
        print(f"{NEON_Y}Usage: /git <what you want to do>{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"Git help: {arg}\n"
        f"Give the exact git command(s) to accomplish this. "
        f"If there are multiple approaches, show the safest one first. "
        f"Add a one-line warning if the command is destructive (rebase, force push, reset --hard etc).")

def cmd_ctf(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """CTF challenge helper — analyze flags, hints, encodings."""
    if not arg:
        print(f"{NEON_Y}Usage: /ctf <paste challenge text or data>{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"CTF challenge analysis:\n{arg}\n\n"
        f"Identify: 1) Challenge category (crypto, forensics, web, pwn, rev, misc). "
        f"2) Any encodings or ciphers present. 3) Tools to use. "
        f"4) Step-by-step approach to solve it. Don't give the flag directly — guide me.")

def cmd_diff_explain(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """Paste a git diff and AI explains what changed and why it matters."""
    diff = arg
    if not diff:
        print(f"{NEON_Y}Paste your git diff (END to finish):{R}")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END": break
                lines.append(line)
            except EOFError: break
        diff = "\n".join(lines)
    if not diff: return ""
    return ask(cfg, messages, session_msgs,
        f"Explain this git diff in plain English:\n```diff\n{diff}\n```\n"
        f"Cover: what changed, why it might have changed, any risks or bugs introduced.")



# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════
CONFIG_PATH = os.path.expanduser("~/.cybersh_direct.json")
DEFAULT_CFG = {
    "model_path":   "",
    "context":      4096,
    "temperature":  0.7,
    "max_tokens":   2048,
    "mode":         "chat",
    "history_file": os.path.expanduser("~/.cybersh_direct_history.json"),
    "max_history":  60,
    "threads":      4,
}

# well-known GGUF download links (free, official)
KNOWN_MODELS = {
    "1": {
        "name":  "Phi-3 Mini (2.2GB) — Microsoft, great for code",
        "file":  "Phi-3-mini-4k-instruct-q4.gguf",
        "url":   "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
    },
    "2": {
        "name":  "TinyLlama 1.1B (638MB) — fastest, lightest",
        "file":  "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "url":   "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    },
    "3": {
        "name":  "Qwen2.5 1.5B (986MB) — smart small model",
        "file":  "qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "url":   "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf",
    },
    "4": {
        "name":  "Mistral 7B (4.1GB) — powerful, best quality",
        "file":  "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "url":   "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    },
    "5": {
        "name":  "Llama 3.2 3B (2.0GB) — Meta, smarter than TinyLlama ★ RECOMMENDED",
        "file":  "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        "url":   "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    },
    "6": {
        "name":  "Qwen2.5 7B (4.7GB) — best for code & reasoning",
        "file":  "qwen2.5-7b-instruct-q4_k_m.gguf",
        "url":   "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf",
    },
    "7": {
        "name":  "DeepSeek-R1 7B (4.7GB) — reasoning model, thinks step-by-step",
        "file":  "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf",
        "url":   "https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF/resolve/main/DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf",
    },
}

def load_cfg() -> dict:
    cfg = DEFAULT_CFG.copy()
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f: cfg.update(json.load(f))
        except: pass
    return cfg

def save_cfg(cfg: dict) -> None:
    with open(CONFIG_PATH, "w") as f: json.dump(cfg, f, indent=2)
    print(f"\n{NEON_G}✓ Config saved → {CONFIG_PATH}{R}")

# ══════════════════════════════════════════════════════════════
#  WEB SEARCH (DuckDuckGo — no API key needed)
# ══════════════════════════════════════════════════════════════
def web_search(query: str, max_results: int = 5) -> str:
    """Search DuckDuckGo and return results as text. No API key needed."""
    try:
        from ddgs import DDGS
    except ImportError:
        return (
            f"{NEON_R}✗ ddgs not installed.{R}\n"
            f"{NEON_Y}Fix:{R} pip install ddgs --break-system-packages"
        )
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    f"[{r.get('title','')}]\n{r.get('href','')}\n{r.get('body','')}"
                )
        if not results:
            return "No results found."
        return "\n\n".join(results)
    except Exception as e:
        return f"Search error: {e}"

# ══════════════════════════════════════════════════════════════
#  MODES
# ══════════════════════════════════════════════════════════════
MODES = {
    "chat": {
        "icon": "💬", "label": "CHAT", "color": NEON_C,
        "system": "You are CYBER SH AI , a sharp helpful local AI. Be concise and direct.",
    },
    "sec": {
        "icon": "🔐", "label": "SEC", "color": NEON_G,
        "system": (
            "You are an elite offensive security expert and bug bounty hunter. "
            "Help with recon, OSINT, XSS, SQLi, SSRF, LFI, RCE, IDOR, API testing, CVE analysis. "
            "Give real working commands and Python tools. Be technical and precise."
        ),
    },
    "vibe": {
        "icon": "🎨", "label": "VIBE", "color": NEON_P,
        "system": (
            "You are an expert vibe coder. Build beautiful impressive projects fast. "
            "Write creative elegant code, suggest UI/UX aesthetics, color schemes, animations."
        ),
    },
    "code": {
        "icon": "⚡", "label": "CODE", "color": NEON_Y,
        "system": (
            "You are an expert software engineer. Write clean production-ready Python and bash. "
            "Add error handling, comments, usage examples."
        ),
    },
    "agent": {
        "icon": "🤖", "label": "AGENT", "color": NEON_O,
        "system": (
            "You are CYBER SH AGENT controlling a Linux computer. "
            "When asked to do things on the computer, use ACTION BLOCKS:\n"
            "ACTION: run_command | <bash command>\n"
            "ACTION: create_file | <filepath> | <content>\n"
            "ACTION: edit_file | <filepath> | <old text> | <new text>\n"
            "ACTION: delete_file | <filepath>\n"
            "ACTION: open_app | <app>\n"
            "ACTION: search_files | <pattern>\n"
            "ACTION: read_file | <filepath>\n"
            "ACTION: make_dir | <path>\n"
            "Always explain what you're doing before each ACTION. User confirms each one."
        ),
    },
}

# ══════════════════════════════════════════════════════════════
#  LLAMA CPP WRAPPER
# ══════════════════════════════════════════════════════════════
_llm_instance = None

def get_llm(cfg: dict):
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance
    try:
        from llama_cpp import Llama
    except ImportError:
        print(f"\n{NEON_R}✗ llama-cpp-python not installed!{R}")
        print(f"{NEON_Y}Fix:{R} pip install llama-cpp-python --break-system-packages")
        sys.exit(1)

    model_path = cfg.get("model_path","").strip()
    if not model_path or not os.path.exists(model_path):
        print(f"\n{NEON_R}✗ No model loaded!{R}")
        print(f"{NEON_Y}Run:{R} python3 {sys.argv[0]} --setup")
        sys.exit(1)

    size_gb = os.path.getsize(model_path) / 1e9
    print(f"\n{NEON_C}Loading {BOLD}{os.path.basename(model_path)}{R} "
          f"{DIM}({size_gb:.1f} GB)…{R}")
    print(f"{DIM}This takes 5-15 seconds on first load…{R}\n")

    # ── Auto-detect GPU every time ────────────────────────────
    n_gpu_layers = 0
    gpu_info     = _detect_gpu()

    if gpu_info["type"] == "nvidia":
        # check if llama-cpp-python was built with CUDA support
        try:
            from llama_cpp import llama_supports_gpu_offload
            cuda_ok = llama_supports_gpu_offload()
        except ImportError:
            cuda_ok = False
        except Exception:
            cuda_ok = True  # older versions don't have this fn but may work

        if cuda_ok:
            n_gpu_layers = -1  # -1 = offload ALL layers to GPU
            print(f"{NEON_G}✓ NVIDIA GPU: {gpu_info['name']} ({gpu_info['vram']}) — CUDA ON ⚡{R}\n")
        else:
            print(f"{NEON_Y}⚠ NVIDIA GPU found ({gpu_info['name']}) but CUDA not enabled.{R}")
            print(f"{DIM}  To enable: CMAKE_ARGS=\"-DGGML_CUDA=on\" pip install llama-cpp-python --force-reinstall --break-system-packages{R}")
            print(f"{DIM}  Running on CPU for now.{R}\n")

    elif gpu_info["type"] == "amd":
        print(f"{NEON_Y}⚠ AMD GPU: {gpu_info['name']} detected.{R}")
        print(f"{DIM}  ROCm support is experimental. Running on CPU.{R}")
        print(f"{DIM}  To try GPU: CMAKE_ARGS=\"-DGGML_HIPBLAS=on\" pip install llama-cpp-python --force-reinstall --break-system-packages{R}\n")

    elif gpu_info["type"] == "intel":
        print(f"{NEON_Y}⚠ Intel GPU: {gpu_info['name']} detected.{R}")
        print(f"{DIM}  Intel Arc/iGPU acceleration not yet supported. Running on CPU.{R}\n")

    else:
        print(f"{DIM}  No GPU detected — running on CPU ({cfg.get('threads',4)} threads){R}\n")

    _llm_instance = Llama(
        model_path   = model_path,
        n_ctx        = cfg["context"],
        n_threads    = cfg.get("threads", 4),
        n_gpu_layers = n_gpu_layers,
        verbose      = False,
    )
    print(f"{NEON_G}✓ Model ready!{R}\n")
    return _llm_instance


def _detect_gpu() -> dict:
    """Detect GPU type, name, and VRAM. Returns dict with type/name/vram."""
    info = {"type": None, "name": "Unknown", "vram": ""}

    # ── NVIDIA — nvidia-smi ───────────────────────────────────
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0 and r.stdout.strip():
            parts = r.stdout.strip().split(",")
            name  = parts[0].strip() if parts else "NVIDIA GPU"
            vram  = f"{int(parts[1].strip())//1024}GB VRAM" if len(parts) > 1 else ""
            return {"type": "nvidia", "name": name, "vram": vram}
    except Exception:
        pass

    # ── AMD — rocm-smi ───────────────────────────────────────
    try:
        r = subprocess.run(["rocm-smi", "--showproductname"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            for line in r.stdout.splitlines():
                if "card" in line.lower() or "gpu" in line.lower() or "rx" in line.lower():
                    name = line.strip().split(":")[-1].strip() or "AMD GPU"
                    return {"type": "amd", "name": name, "vram": ""}
    except Exception:
        pass

    # ── AMD fallback — lspci ─────────────────────────────────
    try:
        r = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                ll = line.lower()
                if "amd" in ll and ("vga" in ll or "display" in ll or "3d" in ll):
                    name = line.split(":")[-1].strip()[:50]
                    return {"type": "amd", "name": name, "vram": ""}
                if "nvidia" in ll and ("vga" in ll or "display" in ll or "3d" in ll):
                    name = line.split(":")[-1].strip()[:50]
                    return {"type": "nvidia", "name": name, "vram": ""}
                if "intel" in ll and ("vga" in ll or "display" in ll or "3d" in ll):
                    name = line.split(":")[-1].strip()[:50]
                    return {"type": "intel", "name": name, "vram": ""}
    except Exception:
        pass

    # ── macOS — system_profiler ──────────────────────────────
    try:
        r = subprocess.run(
            ["system_profiler", "SPDisplaysDataType"],
            capture_output=True, text=True, timeout=8
        )
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                if "Chipset Model:" in line:
                    name = line.split(":", 1)[-1].strip()
                    gpu_type = "nvidia" if "nvidia" in name.lower() \
                               else "amd" if "amd" in name.lower() \
                               else "intel" if "intel" in name.lower() \
                               else "other"
                    return {"type": gpu_type, "name": name, "vram": ""}
    except Exception:
        pass

    return info

def build_prompt(messages: list, model_path: str) -> str:
    """Build prompt string from messages list."""
    mp = model_path.lower()
    parts = []

    # detect model family for correct prompt format
    if "phi-3" in mp or "phi3" in mp:
        for m in messages:
            if m["role"] == "system":
                parts.append(f"<|system|>\n{m['content']}<|end|>")
            elif m["role"] == "user":
                parts.append(f"<|user|>\n{m['content']}<|end|>")
            elif m["role"] == "assistant":
                parts.append(f"<|assistant|>\n{m['content']}<|end|>")
        parts.append("<|assistant|>")

    elif "mistral" in mp or "mixtral" in mp:
        sys_content = ""
        for m in messages:
            if m["role"] == "system": sys_content = m["content"]
        conv = [m for m in messages if m["role"] != "system"]
        for i, m in enumerate(conv):
            if m["role"] == "user":
                prefix = f"[INST] {sys_content}\n" if i == 0 and sys_content else "[INST] "
                parts.append(f"{prefix}{m['content']} [/INST]")
            elif m["role"] == "assistant":
                parts.append(f"{m['content']}</s>")

    elif "qwen" in mp:
        parts.append("<|im_start|>system")
        sys_msg = next((m["content"] for m in messages if m["role"]=="system"), "You are a helpful assistant.")
        parts.append(sys_msg + "<|im_end|>")
        for m in messages:
            if m["role"] == "system": continue
            parts.append(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>")
        parts.append("<|im_start|>assistant")

    else:
        # generic ChatML / TinyLlama
        parts.append("<|system|>")
        sys_msg = next((m["content"] for m in messages if m["role"]=="system"), "You are a helpful assistant.")
        parts.append(sys_msg)
        for m in messages:
            if m["role"] == "system": continue
            tag = "<|user|>" if m["role"] == "user" else "<|assistant|>"
            parts.append(f"{tag}\n{m['content']}")
        parts.append("<|assistant|>")

    return "\n".join(parts)

def stream_local(cfg: dict, messages: list):
    """Stream tokens from local llama-cpp model."""
    llm    = get_llm(cfg)
    prompt = build_prompt(messages, cfg["model_path"])
    stream = llm(
        prompt,
        max_tokens  = cfg.get("max_tokens", 2048),
        temperature = cfg.get("temperature", 0.7),
        stream      = True,
        stop        = ["<|user|>","<|end|>","[INST]","<|im_start|>user"],
    )
    for chunk in stream:
        token = chunk["choices"][0].get("text","")
        if token: yield token

# ══════════════════════════════════════════════════════════════
#  AGENT ENGINE
# ══════════════════════════════════════════════════════════════
ACTION_RE = re.compile(
    r"ACTION:\s*(run_command|create_file|edit_file|delete_file|"
    r"open_app|search_files|read_file|make_dir)\s*\|(.+?)(?=ACTION:|$)",
    re.DOTALL | re.IGNORECASE
)

def parse_actions(text: str) -> list:
    actions = []
    for m in ACTION_RE.finditer(text):
        actions.append({
            "type":  m.group(1).strip().lower(),
            "parts": [p.strip() for p in m.group(2).split("|")],
        })
    return actions

def confirm_action(atype: str, parts: list) -> bool:
    c = min(shutil.get_terminal_size((80,24)).columns, 60)
    print(f"\n{NEON_O}{'─'*c}")
    print(f"  🤖 AGENT ACTION")
    print(f"{'─'*c}{R}")
    labels = {
        "run_command":  (NEON_Y, "RUN",    parts[0][:70]),
        "create_file":  (NEON_G, "CREATE", parts[0]),
        "edit_file":    (NEON_C, "EDIT",   parts[0]),
        "delete_file":  (NEON_R, "DELETE", parts[0]),
        "open_app":     (NEON_P, "OPEN",   parts[0]),
        "search_files": (NEON_C, "SEARCH", parts[0]),
        "read_file":    (NEON_C, "READ",   parts[0]),
        "make_dir":     (NEON_G, "MKDIR",  parts[0]),
    }
    color, label, desc = labels.get(atype, (NEON_C, "ACTION", parts[0]))
    print(f"  {color}{BOLD}[{label}]{R}  {desc}")
    if atype == "delete_file":
        print(f"  {NEON_R}{BOLD}⚠  PERMANENT DELETE{R}")
    if atype == "create_file" and len(parts) > 1:
        print(f"  {DIM}Preview: {parts[1][:80]}…{R}")
    sys.stdout.write(f"\n  {NEON_Y}Approve? [y/N]: {R}")
    try: ans = input().strip().lower()
    except: ans = "n"
    return ans in ("y","yes")

def execute_action(atype: str, parts: list) -> str:
    try:
        if atype == "run_command":
            r = subprocess.run(parts[0], shell=True, capture_output=True,
                               text=True, timeout=30, cwd=os.path.expanduser("~"))
            out = r.stdout.strip()
            if r.stderr.strip(): out += f"\n[stderr] {r.stderr.strip()}"
            return out or "(no output)"

        elif atype == "create_file":
            path = os.path.expanduser(parts[0])
            content = parts[1] if len(parts) > 1 else ""
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            with open(path,"w") as f: f.write(content)
            return f"Created: {path}"

        elif atype == "edit_file":
            path = os.path.expanduser(parts[0])
            old  = parts[1] if len(parts) > 1 else ""
            new  = parts[2] if len(parts) > 2 else ""
            with open(path,"r") as f: c = f.read()
            if old not in c: return f"⚠ Text not found in {path}"
            with open(path,"w") as f: f.write(c.replace(old,new,1))
            return f"Edited: {path}"

        elif atype == "delete_file":
            os.remove(os.path.expanduser(parts[0]))
            return f"Deleted: {parts[0]}"

        elif atype == "open_app":
            subprocess.Popen(parts[0], shell=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Launched: {parts[0]}"

        elif atype == "search_files":
            found = glob.glob(os.path.expanduser(parts[0]), recursive=True)[:20]
            return "\n".join(found) if found else "No matches."

        elif atype == "read_file":
            with open(os.path.expanduser(parts[0]),"r",errors="replace") as f:
                return f.read(6000)

        elif atype == "make_dir":
            os.makedirs(os.path.expanduser(parts[0]), exist_ok=True)
            return f"Created: {parts[0]}"

    except Exception as e:
        return f"✗ Error: {e}"
    return "done"

def process_actions(text: str) -> str:
    actions = parse_actions(text)
    if not actions: return ""
    results = []
    for a in actions:
        if confirm_action(a["type"], a["parts"]):
            print(f"  {NEON_G}⟳ Running…{R}")
            out = execute_action(a["type"], a["parts"])
            print(f"  {NEON_G}✓{R}")
            for line in out.split("\n")[:10]:
                print(f"    {DIM}{line}{R}")
            results.append(f"[{a['type']}] {out[:150]}")
        else:
            print(f"  {NEON_Y}⊘ Skipped{R}")
            results.append(f"[{a['type']}] skipped")
        print()
    return "\n".join(results)

# ══════════════════════════════════════════════════════════════
#  SPINNER
# ══════════════════════════════════════════════════════════════
class Spinner:
    MSGS = ["Cracking the matrix","Routing through proxies","Agent thinking",
            "Vibe coding","Enumerating endpoints","Fuzzing parameters"]
    def __init__(self, label=None):
        import random
        self.label = label or random.choice(self.MSGS)
        self._active = False; self._t = None; self._s = 0.0
    def __enter__(self):
        self._active = True; self._s = time.time()
        self._t = threading.Thread(target=self._spin, daemon=True)
        self._t.start(); return self
    def __exit__(self, *_):
        self._active = False
        if self._t: self._t.join(0.5)
        sys.stdout.write(CLEAR); sys.stdout.flush()
    def _spin(self):
        f = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"; i = 0
        while self._active:
            sys.stdout.write(
                f"\r  {NEON_G}{f[i%len(f)]}{R} {NEON_C}{self.label}{DIM}…{R} "
                f"{DIM}[{time.time()-self._s:.1f}s]{R}"
            )
            sys.stdout.flush(); time.sleep(0.07); i += 1

# ══════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════
def cols(): return shutil.get_terminal_size((80,24)).columns
def div(color=DIM, ch="─"): return f"{color}{ch*cols()}{R}"

def print_banner(cfg: dict) -> None:
    mode = MODES.get(cfg.get("mode","chat"), MODES["chat"])
    mc   = mode["color"]
    now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    model_name = os.path.basename(cfg.get("model_path","no model")).replace(".gguf","")
    print(f"\n{NEON_C}{BOLD}")
    print(r" ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗  ██╗")
    print(r"██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║")
    print(r"██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗███████║")
    print(r"██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══██║")
    print(r"╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║██║  ██║")
    print(r" ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝")
    print(f"  DIRECT — No Server · Pure Python{R}\n")
    print(div())
    print(f"  {NEON_C}MODEL{R} {BOLD}{model_name}{R}  "
          f"{NEON_C}MODE{R} {mc}{BOLD}{mode['icon']} {mode['label']}{R}  "
          f"{NEON_C}TEMP{R} {NEON_Y}{cfg['temperature']}{R}  {DIM}{now}{R}")
    print(div())
    print(f"  {DIM}Modes:{R} {NEON_P}/vibe{R} {NEON_G}/sec{R} "
          f"{NEON_Y}/code{R} {NEON_C}/chat{R} {NEON_O}/agent{R} {NEON_G}/shell{R}  "
          f"{DIM}Files:{R} {NEON_C}/f <path>  /o <path>{R}  "
          f"{DIM}Help:{R} {NEON_C}/help{R}")
    print(div() + "\n")

def startup_selector(cfg: dict) -> None:
    """Show mode selector on startup."""
    print(f"\n{NEON_C}{BOLD}")
    print(r" ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗  ██╗")
    print(r"██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║")
    print(r"██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗███████║")
    print(r"██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══██║")
    print(r"╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║██║  ██║")
    print(r" ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝")
    model_name = os.path.basename(cfg.get("model_path","no model")).replace(".gguf","")
    print(f"  DIRECT  ·  {model_name}{R}\n")
    print(div())
    print(f"\n  {BOLD}Select mode:{R}\n")
    menu = [
        ("1","agent",NEON_O,"🤖","Agent  — AI controls your computer"),
        ("2","sec",  NEON_G,"🔐","Sec    — Bug bounty & pentest expert"),
        ("3","vibe", NEON_P,"🎨","Vibe   — Creative coding & UI/UX"),
        ("4","code", NEON_Y,"⚡","Code   — Clean production code"),
        ("5","chat", NEON_C,"💬","Chat   — General assistant"),
    ]
    for num, key, color, icon, desc in menu:
        cur = f"  {DIM}← current{R}" if key == cfg.get("mode","chat") else ""
        print(f"  {color}{BOLD}[{num}]{R}  {icon}  {color}{desc}{R}{cur}")
    print(f"\n{div()}")
    sys.stdout.write(f"\n  {NEON_Y}Choose [1-5] (Enter = keep current): {R}")
    sys.stdout.flush()
    try: choice = input().strip()
    except: choice = ""
    m = {"1":"agent","2":"sec","3":"vibe","4":"code","5":"chat"}
    if choice in m: cfg["mode"] = m[choice]

def print_help() -> None:
    print(f"\n{div(BOLD_C)}")
    print(f"{BOLD_C}  CYBER SH DIRECT — COMMANDS{R}")
    print(div(BOLD_C))
    sections = [
        ("MODES", [
            ("/agent","🤖 AI controls your computer"),
            ("/sec",  "🔐 Bug bounty expert"),
            ("/vibe", "🎨 Creative vibe coding"),
            ("/code", "⚡ Production code"),
            ("/chat", "💬 General chat"),
        ]),
        ("🧠 MEMORY", [
            ("/remember <anything>",  "AI remembers this forever"),
            ("/remember name is X",   "Remember your name"),
            ("/remember project X Y", "Save a project description"),
            ("/memories",             "Show everything remembered"),
            ("/forget <keyword>",     "Delete a memory"),
        ]),
        ("🎭 PERSONALITY", [
            ("/persona",              "List AI personalities"),
            ("/persona teacher",      "Patient teacher mode"),
            ("/persona hacker",       "Elite hacker mentor"),
            ("/persona coach",        "Motivating life coach"),
            ("/persona roaster",      "Roasts bad ideas (with fixes)"),
            ("/persona sherlock",     "Sherlock Holmes mode"),
        ]),
        ("🎯 PRODUCTIVITY", [
            ("/goals",                "Show today's goals"),
            ("/goals add <goal>",     "Add a daily goal"),
            ("/goals done <n>",       "Mark goal as done"),
            ("/calc <expr>",          "Quick math: /calc 15% of 240"),
            ("/summarize <url>",      "Fetch + summarize any webpage"),
            ("/timer 5m",             "Countdown timer"),
            ("/weather [city]",       "ASCII weather forecast"),
            ("/translate <l> <t>",    "Translate to any language"),
            ("/recap",                "Summary of this session"),
        ]),
        ("FILES", [
            ("/f <path>", "Load file into AI context"),
            ("/o <path>", "Save last response to file"),
            ("/run",      "Execute last code block"),
            ("/copy",     "Copy to clipboard"),
        ]),
        ("SECURITY", [
            ("/recon <target>",    "Bug bounty recon plan"),
            ("/payload <type>",    "Payloads: xss|sqli|ssrf|lfi|rce"),
            ("/explain <cmd>",     "Explain a command"),
            ("/cvesearch <id>",    "Search & analyze CVE/vulnerability"),
        ]),
        ("WEB & MODELS", [
            ("/web <query>",       "Search web, feed results to AI"),
            ("/models",            "Download a new model"),
        ]),
        ("TOOLS", [
            ("/tldr <cmd>",        "Explain any command in plain English"),
            ("/howto <task>",      "Get exact command for any task"),
            ("/fix <error>",       "Paste error, get instant fix"),
            ("/passgen [type]",    "Generate passwords/phrases/API keys"),
            ("/encode <text>",     "Base64/hex/URL/MD5/SHA256 encode"),
            ("/syswatch",          "Live CPU/RAM/disk monitor"),
            ("/benchmark",         "CPU + RAM + disk speed test with score"),
            ("/note <text>",       "Save a quick note"),
            ("/notes list",        "Show all notes"),
            ("/tip",               "Show tip of the day"),
            ("/weather [city]",    "ASCII weather forecast"),
            ("/timer 5m",          "Countdown timer (5m, 30s, 1h)"),
        ]),
        ("CODE & AI LAB", [
            ("/explaincode",       "Paste code → AI explains every line"),
            ("/roast",             "AI roasts your bad code (with fixes)"),
            ("/rename <name>",     "AI suggests better variable/function names"),
            ("/regex <desc>",      "AI writes a regex for you"),
            ("/git <task>",        "AI gives exact git commands"),
            ("/diff",              "Paste git diff → AI explains changes"),
            ("/translate <l> <t>", "Translate text to any language"),
            ("/challenge [level]", "Get a coding/hacking challenge"),
            ("/ctf <data>",        "CTF challenge analyzer"),
            ("/recap",             "Summary of this session"),
        ]),
        ("SESSION", [
            ("/clear",   "Clear history"),
            ("/history", "Show history"),
            ("/temp <n>","Set temperature"),
            ("/info",    "Show model info"),
            ("/save",    "Save config"),
            ("/exit",    "Exit"),
        ]),
    ]
    for section, cmds in sections:
        print(f"\n  {NEON_Y}{BOLD}{section}{R}")
        for cmd, desc in cmds:
            print(f"    {NEON_C}{cmd:<22}{R}{DIM}{desc}{R}")
    print(f"\n{div()}\n")

# ══════════════════════════════════════════════════════════════
#  HISTORY
# ══════════════════════════════════════════════════════════════
def save_history(path: str, history: list, maxh: int) -> None:
    try:
        with open(path,"w") as f: json.dump(history[-maxh:], f, indent=2)
    except: pass

# ══════════════════════════════════════════════════════════════
#  MEMORY SYSTEM — Remembers things between sessions
# ══════════════════════════════════════════════════════════════
MEMORY_PATH = os.path.expanduser("~/.cybersh_memory.json")

def load_memory() -> dict:
    try:
        with open(MEMORY_PATH) as f: return json.load(f)
    except Exception:
        return {"facts": [], "preferences": {}, "projects": {}}

def save_memory(mem: dict) -> None:
    try:
        with open(MEMORY_PATH, "w") as f: json.dump(mem, f, indent=2)
    except Exception: pass

def memory_context(mem: dict) -> str:
    """Build a context string from memory to inject into AI system prompt."""
    if not mem["facts"] and not mem["preferences"] and not mem["projects"]:
        return ""
    parts = ["[MEMORY — things the user told you to remember:]"]
    if mem["facts"]:
        parts.append("Facts: " + " | ".join(mem["facts"][-20:]))
    if mem["preferences"]:
        prefs = ", ".join(f"{k}={v}" for k, v in mem["preferences"].items())
        parts.append(f"Preferences: {prefs}")
    if mem["projects"]:
        for name, info in list(mem["projects"].items())[-5:]:
            parts.append(f"Project '{name}': {info}")
    return "\n".join(parts)

def cmd_remember(arg: str, mem: dict) -> None:
    """Save something to persistent memory."""
    if not arg:
        print(f"{NEON_Y}Usage: /remember <anything>{R}")
        print(f"  Examples:")
        print(f"    /remember my name is Ahmed")
        print(f"    /remember I prefer Python 3.11")
        print(f"    /remember project myapp is a flask REST API\n")
        return
    w   = min(cols(), 60)
    div_line = f"{NEON_C}{'─'*w}{R}"

    # detect project
    if arg.lower().startswith("project "):
        rest  = arg[8:].strip()
        parts = rest.split(" ", 1)
        name  = parts[0]
        info  = parts[1] if len(parts) > 1 else ""
        mem["projects"][name] = info
        save_memory(mem)
        print(f"\n{NEON_G}✓ Project '{name}' remembered.{R}\n")
        return

    # detect preference (key=value or "prefer X")
    if "=" in arg and len(arg.split("=")) == 2:
        k, v = arg.split("=", 1)
        mem["preferences"][k.strip()] = v.strip()
        save_memory(mem)
        print(f"\n{NEON_G}✓ Preference saved: {k.strip()} = {v.strip()}{R}\n")
        return

    # general fact
    ts   = datetime.datetime.now().strftime("%Y-%m-%d")
    fact = f"[{ts}] {arg}"
    mem["facts"].append(fact)
    if len(mem["facts"]) > 100: mem["facts"].pop(0)
    save_memory(mem)
    print(f"\n{NEON_G}✓ Remembered: {arg}{R}\n")

def cmd_memories(mem: dict) -> None:
    """Show everything in memory."""
    w        = min(cols(), 65)
    div_line = f"{NEON_C}{'─'*w}{R}"
    print(f"\n{div_line}")
    print(f"{NEON_C}{BOLD}  🧠 Memory{R}")
    print(div_line)

    if not mem["facts"] and not mem["preferences"] and not mem["projects"]:
        print(f"  {DIM}Nothing remembered yet. Use /remember <anything>{R}")
        print(f"{div_line}\n"); return

    if mem["facts"]:
        print(f"\n  {NEON_Y}Facts:{R}")
        for i, f in enumerate(mem["facts"][-15:], 1):
            print(f"    {DIM}{i:>2}.{R} {f}")

    if mem["preferences"]:
        print(f"\n  {NEON_Y}Preferences:{R}")
        for k, v in mem["preferences"].items():
            print(f"    {NEON_C}{k}{R} = {v}")

    if mem["projects"]:
        print(f"\n  {NEON_Y}Projects:{R}")
        for name, info in mem["projects"].items():
            print(f"    {NEON_C}{name}{R}: {info}")

    print(f"\n  {DIM}Use /forget <text> to remove something{R}")
    print(f"{div_line}\n")

def cmd_forget(arg: str, mem: dict) -> None:
    """Remove something from memory."""
    if not arg:
        print(f"{NEON_Y}Usage: /forget <keyword or project name>{R}\n"); return

    removed = 0
    # check projects
    if arg in mem["projects"]:
        del mem["projects"][arg]
        removed += 1

    # check preferences
    if arg in mem["preferences"]:
        del mem["preferences"][arg]
        removed += 1

    # check facts
    before = len(mem["facts"])
    mem["facts"] = [f for f in mem["facts"] if arg.lower() not in f.lower()]
    removed += before - len(mem["facts"])

    if removed:
        save_memory(mem)
        print(f"\n{NEON_G}✓ Removed {removed} memory item(s) matching '{arg}'{R}\n")
    else:
        print(f"\n{NEON_Y}⚠ Nothing found matching '{arg}'{R}\n")

# ══════════════════════════════════════════════════════════════
#  MOOD / PERSONALITY SYSTEM
# ══════════════════════════════════════════════════════════════
PERSONALITIES = {
    "default":  "You are CYBER SH, a helpful AI assistant. Be concise and direct.",
    "teacher":  "You are a patient teacher. Explain everything simply with analogies, never assume prior knowledge. After explaining, ask if the user understood.",
    "hacker":   "You are an elite hacker mentor. Be direct, technical, use proper security terminology. Challenge the user to think deeper. Occasionally use l33tspeak for emphasis.",
    "coach":    "You are an energetic life and productivity coach. Be encouraging, positive, break problems into small steps. Celebrate every win, no matter how small.",
    "roaster":  "You are a brutally honest senior dev who roasts bad ideas and code with sharp humor — but ALWAYS follows up with the correct approach. Be funny, accurate, and genuinely helpful.",
    "sherlock": "You are Sherlock Holmes. Make deductions from every detail the user gives you. Be dramatic, logical, brilliant. Say 'Elementary.' when something is obvious.",
    "prof":     "You are a university professor — expert, thorough, academic but approachable. Use precise language, cite reasoning, structure answers clearly with examples.",
    "eli5":     "You are explaining everything to a 5-year-old. Use the simplest words possible, fun analogies, and short sentences. Never use jargon.",
    "pirate":   "You are a pirate who happens to be a genius programmer and hacker. Speak like a pirate (Arr, matey, etc.) but give genuinely expert technical advice.",
    "stoic":    "You are a Stoic philosopher AI. Give wise, calm, measured responses. Reference Marcus Aurelius, Epictetus, Seneca where relevant. Focus on what the user can control.",
}

def cmd_persona(arg: str, cfg: dict) -> None:
    """Switch AI personality."""
    w = min(cols(), 60)
    if not arg:
        print(f"\n{NEON_C}{'─'*w}{R}")
        print(f"{NEON_C}{BOLD}  🎭 Personalities{R}")
        print(f"{NEON_C}{'─'*w}{R}")
        for k, v in PERSONALITIES.items():
            cur = f" {NEON_G}← active{R}" if cfg.get("persona","default") == k else ""
            print(f"  {NEON_Y}{k:<12}{R}{DIM}{v[:55]}…{R}{cur}")
        print(f"\n  {DIM}Usage: /persona teacher{R}")
        print(f"{NEON_C}{'─'*w}{R}\n"); return
    if arg not in PERSONALITIES:
        close = [k for k in PERSONALITIES if k.startswith(arg[:3])]
        hint  = f"  Did you mean: {close[0]}?" if close else ""
        print(f"{NEON_R}✗ Unknown persona '{arg}'.{R}{hint}")
        print(f"  Options: {', '.join(PERSONALITIES)}\n"); return
    cfg["persona"] = arg
    desc = PERSONALITIES[arg][:80]
    bw   = min(cols(), 62)
    print(f"\n{NEON_P}{'▓'*bw}")
    print(f"{NEON_P}{BOLD}  🎭 PERSONA → {arg.upper()}{R}")
    print(f"{NEON_P}{'▓'*bw}{R}")
    print(f"  {DIM}{desc}…{R}\n")

# ══════════════════════════════════════════════════════════════
#  SMART SUMMARIZER
# ══════════════════════════════════════════════════════════════
def cmd_summarize_url(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """Fetch a URL and AI summarizes it."""
    if not arg:
        print(f"{NEON_Y}Usage: /summarize <url>{R}\n"); return ""
    print(f"\n{NEON_C}🌐 Fetching {arg}…{R}\n")
    r = subprocess.run(
        ["curl", "-sL", "--max-time", "10",
         "-A", "Mozilla/5.0", arg],
        capture_output=True, text=True
    )
    if not r.stdout:
        print(f"{NEON_R}✗ Could not fetch URL.{R}\n"); return ""
    # strip HTML tags crudely
    text = re.sub(r"<[^>]+>", " ", r.stdout)
    text = re.sub(r"\s+", " ", text).strip()[:4000]
    return ask(cfg, messages, session_msgs,
        f"Summarize this webpage content in bullet points. "
        f"Extract: main topic, key points, any important numbers or dates, and conclusion.\n\n{text}")

# ══════════════════════════════════════════════════════════════
#  QUICK MATH
# ══════════════════════════════════════════════════════════════
def cmd_calc(arg: str) -> None:
    """Safe math evaluator."""
    if not arg:
        print(f"{NEON_Y}Usage: /calc <expression>  e.g. /calc 2**32 or /calc 15% of 240{R}\n"); return
    w   = min(cols(), 50)
    div_line = f"{NEON_C}{'─'*w}{R}"

    # handle "X% of Y"
    pct = re.match(r"(\d+\.?\d*)%\s*of\s*(\d+\.?\d*)", arg.lower())
    if pct:
        a, b = float(pct.group(1)), float(pct.group(2))
        result = a / 100 * b
        print(f"\n  {NEON_C}{a}% of {b}{R} = {NEON_G}{BOLD}{result:,.4g}{R}\n")
        return

    # safe eval — only allow math chars
    safe = re.sub(r"[^0-9+\-*/().% eE]", "", arg)
    try:
        result = eval(safe, {"__builtins__": {}})
        print(f"\n{div_line}")
        print(f"  {NEON_C}{arg}{R} = {NEON_G}{BOLD}{result:,}{R}")
        print(f"{div_line}\n")
    except Exception as e:
        print(f"{NEON_R}✗ Math error: {e}{R}\n")

# ══════════════════════════════════════════════════════════════
#  DAILY GOALS
# ══════════════════════════════════════════════════════════════
GOALS_PATH = os.path.expanduser("~/.cybersh_goals.json")

def load_goals() -> list:
    try:
        with open(GOALS_PATH) as f:
            data = json.load(f)
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            return [g for g in data if g.get("date") == today]
    except Exception: return []

def save_goals(goals: list) -> None:
    try:
        with open(GOALS_PATH, "w") as f: json.dump(goals, f, indent=2)
    except Exception: pass

def cmd_goals(action: str, arg: str) -> None:
    """Daily goal tracker."""
    goals = load_goals()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    w     = min(cols(), 55)
    div_line = f"{NEON_C}{'─'*w}{R}"

    if action in ("add", "") and arg:
        goals.append({"date": today, "text": arg, "done": False})
        save_goals(goals); print(f"{NEON_G}✓ Goal added.{R}\n"); return

    if action in ("done", "check") and arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(goals):
            goals[idx]["done"] = True
            save_goals(goals); print(f"{NEON_G}✓ Marked done!{R}\n")
        return

    if action in ("clear", "reset"):
        save_goals([]); print(f"{NEON_G}✓ Goals cleared.{R}\n"); return

    # show
    print(f"\n{div_line}")
    print(f"{NEON_C}{BOLD}  🎯 Today's Goals — {today}{R}")
    print(div_line)
    if not goals:
        print(f"  {DIM}No goals yet. Add one: /goals add <goal>{R}")
    done = sum(1 for g in goals if g["done"])
    for i, g in enumerate(goals, 1):
        icon  = f"{NEON_G}✓{R}" if g["done"] else f"{NEON_Y}○{R}"
        text  = f"{DIM}{g['text']}{R}" if g["done"] else g["text"]
        print(f"  {icon} {i}. {text}")
    if goals:
        pct = int(100 * done / len(goals))
        bar_w = 25; filled = int(bar_w * pct / 100)
        bar = f"{NEON_G}{'█'*filled}{DIM}{'░'*(bar_w-filled)}{R}"
        print(f"\n  {bar} {NEON_Y}{pct}%{R} ({done}/{len(goals)} done)")
    print(f"\n  {DIM}/goals add <goal> | /goals done <n> | /goals clear{R}")
    print(f"{div_line}\n")



# ══════════════════════════════════════════════════════════════
#  DAILY TIP
# ══════════════════════════════════════════════════════════════
TIPS = [
    "Use `Ctrl+R` to search your bash history interactively.",
    "Use `!!` to repeat the last command. `sudo !!` to run it as root.",
    "Use `cd -` to go back to the previous directory.",
    "Use `grep -r 'text' .` to search inside all files in a folder.",
    "Use `man <command>` to read the full manual for any command.",
    "Use `watch -n 1 <cmd>` to run a command every second and see output live.",
    "Use `curl wttr.in` to check the weather in your terminal.",
    "Use `history | grep <keyword>` to find old commands fast.",
    "Use `tar -xzf file.tar.gz` to extract a .tar.gz file.",
    "Use `df -h` to see disk space in human readable format.",
    "Use `htop` for a beautiful interactive process monitor.",
    "Use `ss -tulpn` to see all open ports and what's using them.",
    "Use `find / -name '*.log' 2>/dev/null` to find all log files.",
    "Use `alias ll='ls -la'` to create a shortcut command.",
    "Use `screen` or `tmux` to keep sessions alive after disconnect.",
    "Use `chmod +x script.sh && ./script.sh` to run a bash script.",
    "Use `curl -O <url>` to download a file from the internet.",
    "Use `zip -r archive.zip folder/` to zip an entire folder.",
    "Use `wc -l file.txt` to count lines in a file.",
    "Use `cut -d',' -f1 file.csv` to extract the first column of a CSV.",
]

def show_tip() -> None:
    import random, hashlib
    # same tip per day, changes daily
    day_seed = datetime.datetime.now().strftime("%Y%m%d")
    idx = int(hashlib.md5(day_seed.encode()).hexdigest(), 16) % len(TIPS)
    tip = TIPS[idx]
    w   = min(cols(), 70)
    print(f"\n{NEON_Y}{'─'*w}")
    print(f"  💡 Tip of the day")
    print(f"{'─'*w}{R}")
    print(f"  {tip}")
    print(f"{NEON_Y}{'─'*w}{R}\n")

def cmd_passgen(arg: str) -> None:
    """Generate passwords, passphrases, or API keys."""
    import random, string, secrets
    w    = min(cols(), 60)
    div  = f"{NEON_C}{'─'*w}{R}"
    kind = arg.lower() if arg else "password"

    print(f"\n{div}")
    print(f"{NEON_C}{BOLD}  🔑 Password Generator{R}")
    print(div)

    if "phrase" in kind or "word" in kind:
        words = ["alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel",
                 "india","juliet","kilo","lima","mike","november","oscar","paper",
                 "router","signal","tango","ultra","victor","whiskey","xray","yankee",
                 "zebra","rocket","flame","storm","pixel","ghost","blade","cipher",
                 "tower","nexus","forge","prism","orbit","quartz","vault","warden"]
        for _ in range(3):
            phrase = "-".join(secrets.choice(words) for _ in range(4))
            num    = secrets.randbelow(9999)
            print(f"  {NEON_G}{phrase}-{num}{R}")
    elif "api" in kind or "key" in kind or "token" in kind:
        for _ in range(3):
            key = secrets.token_hex(32)
            print(f"  {NEON_G}{key}{R}")
    else:
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        for length in (16, 24, 32):
            pwd = "".join(secrets.choice(chars) for _ in range(length))
            print(f"  {NEON_Y}[{length} chars]{R} {NEON_G}{pwd}{R}")

    print(f"\n  {DIM}Usage: /passgen phrase | /passgen api | /passgen (default=password){R}")
    print(f"{div}\n")

def cmd_encode(arg: str) -> None:
    """Encode/decode/hash text in multiple formats."""
    import base64, hashlib, urllib.parse
    if not arg:
        print(f"{NEON_Y}Usage: /encode <text>  or  /encode decode <base64>{R}\n")
        return

    w   = min(cols(), 70)
    div = f"{NEON_C}{'─'*w}{R}"
    print(f"\n{div}")
    print(f"{NEON_C}{BOLD}  🔐 Encode / Hash{R}")
    print(div)

    # decode mode
    if arg.lower().startswith("decode "):
        raw = arg[7:].strip()
        try:
            b64 = base64.b64decode(raw).decode(errors="replace")
            print(f"  {NEON_Y}Base64 decode:{R} {NEON_G}{b64}{R}")
        except Exception:
            print(f"  {NEON_R}✗ Not valid base64{R}")
        try:
            url = urllib.parse.unquote(raw)
            print(f"  {NEON_Y}URL decode:    {R} {NEON_G}{url}{R}")
        except Exception:
            pass
        print(f"{div}\n")
        return

    text = arg.encode()
    b64  = base64.b64encode(text).decode()
    hex_ = text.hex()
    url  = urllib.parse.quote(arg)
    md5  = hashlib.md5(text).hexdigest()
    sha1 = hashlib.sha1(text).hexdigest()
    sha256 = hashlib.sha256(text).hexdigest()

    rows = [
        ("Base64",  b64),
        ("Hex",     hex_),
        ("URL",     url),
        ("MD5",     md5),
        ("SHA1",    sha1),
        ("SHA256",  sha256),
    ]
    for label, val in rows:
        print(f"  {NEON_Y}{label:<10}{R} {NEON_G}{val}{R}")
    print(f"\n  {DIM}Decode: /encode decode <base64>{R}")
    print(f"{div}\n")

def cmd_syswatch() -> None:
    """Live CPU/RAM/Disk monitor — updates every second. Ctrl+C to stop."""
    import time as _time
    print(f"\n{NEON_C}  🖥  SYSWATCH — Live Monitor  {DIM}(Ctrl+C to stop){R}\n")
    try:
        while True:
            # CPU
            try:
                with open("/proc/stat") as f: cpu1 = f.readline().split()
                _time.sleep(0.5)
                with open("/proc/stat") as f: cpu2 = f.readline().split()
                idle1 = int(cpu1[4]); total1 = sum(int(x) for x in cpu1[1:])
                idle2 = int(cpu2[4]); total2 = sum(int(x) for x in cpu2[1:])
                cpu_pct = 100 * (1 - (idle2-idle1)/(total2-total1+0.001))
            except Exception:
                cpu_pct = 0.0

            # RAM
            try:
                meminfo = {}
                with open("/proc/meminfo") as f:
                    for line in f:
                        k, v = line.split(":")
                        meminfo[k.strip()] = int(v.strip().split()[0])
                total_ram  = meminfo.get("MemTotal", 1)
                avail_ram  = meminfo.get("MemAvailable", 0)
                used_ram   = total_ram - avail_ram
                ram_pct    = 100 * used_ram / total_ram
                ram_used_g = used_ram / 1048576
                ram_tot_g  = total_ram / 1048576
            except Exception:
                ram_pct = 0.0; ram_used_g = 0; ram_tot_g = 0

            # Disk
            try:
                st = os.statvfs("/")
                disk_total = st.f_blocks * st.f_frsize
                disk_free  = st.f_bavail * st.f_frsize
                disk_used  = disk_total - disk_free
                disk_pct   = 100 * disk_used / (disk_total + 1)
                disk_used_g = disk_used / 1e9
                disk_tot_g  = disk_total / 1e9
            except Exception:
                disk_pct = 0.0; disk_used_g = 0; disk_tot_g = 0

            def bar(pct, width=30):
                filled = int(width * pct / 100)
                color  = NEON_G if pct < 60 else NEON_Y if pct < 85 else NEON_R
                return f"{color}{'█'*filled}{DIM}{'░'*(width-filled)}{R} {color}{pct:5.1f}%{R}"

            now = datetime.datetime.now().strftime("%H:%M:%S")
            sys.stdout.write(f"\r\033[3A" if True else "")
            print(f"\033[2K  {NEON_C}CPU {R} {bar(cpu_pct)}  {DIM}{now}{R}")
            print(f"\033[2K  {NEON_C}RAM {R} {bar(ram_pct)}  {DIM}{ram_used_g:.1f}/{ram_tot_g:.1f} GB{R}")
            print(f"\033[2K  {NEON_C}DISK{R} {bar(disk_pct)}  {DIM}{disk_used_g:.1f}/{disk_tot_g:.1f} GB{R}")
            _time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{NEON_G}✓ Syswatch stopped.{R}\n")

def cmd_benchmark() -> None:
    """Quick CPU + RAM + disk benchmark."""
    import time as _time, random
    w   = min(cols(), 60)
    div = f"{NEON_C}{'─'*w}{R}"
    print(f"\n{div}")
    print(f"{NEON_C}{BOLD}  ⚡ Benchmark{R}")
    print(div)

    # CPU
    print(f"  {NEON_Y}CPU{R}  — calculating primes…", end="", flush=True)
    t0 = _time.time()
    primes = 0
    for n in range(2, 50000):
        if all(n % i for i in range(2, int(n**0.5)+1)): primes += 1
    cpu_t = _time.time() - t0
    cpu_score = int(3000 / (cpu_t + 0.001))
    bar_w = 20; bar_f = min(bar_w, int(cpu_score / 50))
    color = NEON_G if cpu_score > 1500 else NEON_Y if cpu_score > 800 else NEON_R
    print(f"\r  {NEON_Y}CPU{R}  {color}{'█'*bar_f}{'░'*(bar_w-bar_f)}{R} {cpu_score} pts  {DIM}({cpu_t:.2f}s){R}")

    # RAM
    print(f"  {NEON_Y}RAM{R}  — read/write test…", end="", flush=True)
    t0   = _time.time()
    data = bytearray(50 * 1024 * 1024)  # 50MB
    for i in range(0, len(data), 4096): data[i] = i % 256
    _ = sum(data[::4096])
    ram_t = _time.time() - t0
    ram_score = int(500 / (ram_t + 0.001))
    bar_f = min(bar_w, int(ram_score / 25))
    color = NEON_G if ram_score > 300 else NEON_Y if ram_score > 150 else NEON_R
    print(f"\r  {NEON_Y}RAM{R}  {color}{'█'*bar_f}{'░'*(bar_w-bar_f)}{R} {ram_score} pts  {DIM}({ram_t:.2f}s){R}")

    # Disk
    print(f"  {NEON_Y}DISK{R} — write test…", end="", flush=True)
    tmp = os.path.expanduser("~/.cybersh_bench_tmp")
    t0  = _time.time()
    try:
        with open(tmp, "wb") as f: f.write(os.urandom(20 * 1024 * 1024))
        disk_t = _time.time() - t0
        os.remove(tmp)
        disk_score = int(200 / (disk_t + 0.001))
    except Exception:
        disk_t = 99; disk_score = 0
    bar_f = min(bar_w, int(disk_score / 10))
    color = NEON_G if disk_score > 100 else NEON_Y if disk_score > 50 else NEON_R
    print(f"\r  {NEON_Y}DISK{R} {color}{'█'*bar_f}{'░'*(bar_w-bar_f)}{R} {disk_score} pts  {DIM}({disk_t:.2f}s){R}")

    total = cpu_score + ram_score + disk_score
    grade = "S" if total > 2500 else "A" if total > 1800 else "B" if total > 1200 else "C" if total > 700 else "D"
    grade_color = {
        "S": NEON_G, "A": NEON_G, "B": NEON_Y, "C": NEON_O, "D": NEON_R
    }.get(grade, NEON_C)
    print(div)
    print(f"  {NEON_C}Total score:{R} {BOLD}{total}{R}  Grade: {grade_color}{BOLD}{grade}{R}")
    print(f"{div}\n")

def cmd_fix(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """Paste any error and get an instant fix."""
    error = arg or ""
    if not error:
        print(f"{NEON_Y}Paste the error message:{R} ", end=""); sys.stdout.flush()
        error = input().strip()
    if not error:
        print(f"{NEON_Y}⚠ No error provided.{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"Fix this error — give the exact command or code to solve it:\n\n{error}")

def cmd_howto(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """How do I do X in Linux?"""
    if not arg:
        print(f"{NEON_Y}Usage: /howto <task>{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"How do I {arg} in Linux? Give me the exact command(s) to run. "
        f"Be concise — show the command first, then a one-line explanation.")

def cmd_tldr(arg: str, cfg: dict, messages: list, session_msgs: list) -> str:
    """Explain a command in plain English."""
    if not arg:
        print(f"{NEON_Y}Usage: /tldr <command>{R}\n"); return ""
    return ask(cfg, messages, session_msgs,
        f"Explain the command `{arg}` in plain English — no jargon. "
        f"Format: 1) What it does in one sentence. 2) Common examples with explanations. "
        f"3) Any warnings or things to be careful about.")

def cmd_notes(action: str, arg: str) -> None:
    """Quick note-taking during sessions."""
    notes_file = os.path.expanduser("~/.cybersh_notes.json")
    try:
        with open(notes_file) as f: notes = json.load(f)
    except Exception:
        notes = []

    w   = min(cols(), 60)
    div = f"{NEON_C}{'─'*w}{R}"

    if action in ("add", "note", "") and arg:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        notes.append({"time": ts, "text": arg})
        with open(notes_file, "w") as f: json.dump(notes, f, indent=2)
        print(f"{NEON_G}✓ Note saved.{R}\n")
    elif action in ("list", "show", "ls", ""):
        if not notes:
            print(f"{NEON_Y}No notes yet. Use: /note <text>{R}\n"); return
        print(f"\n{div}")
        print(f"{NEON_C}{BOLD}  📝 Notes{R}")
        print(div)
        for i, n in enumerate(notes[-20:], 1):
            print(f"  {NEON_Y}{i:>2}.{R} {DIM}[{n['time']}]{R} {n['text']}")
        print(f"{div}\n")
    elif action in ("clear", "wipe"):
        with open(notes_file, "w") as f: json.dump([], f)
        print(f"{NEON_G}✓ Notes cleared.{R}\n")
    elif action in ("del", "delete", "rm") and arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(notes):
            removed = notes.pop(idx)
            with open(notes_file, "w") as f: json.dump(notes, f, indent=2)
            print(f"{NEON_G}✓ Deleted: {removed['text'][:50]}{R}\n")
        else:
            print(f"{NEON_R}✗ Note #{arg} not found.{R}\n")
    else:
        # treat whole arg as a note if no subcommand matched
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        text = (action + " " + arg).strip()
        notes.append({"time": ts, "text": text})
        with open(notes_file, "w") as f: json.dump(notes, f, indent=2)
        print(f"{NEON_G}✓ Note saved.{R}\n")

def setup_wizard(cfg: dict) -> None:
    print(f"\n{BOLD_C}{'─'*60}")
    print(f"  CYBER SH DIRECT — Setup Wizard")
    print(f"{'─'*60}{R}\n")

    # check llama-cpp-python
    try:
        import llama_cpp
        print(f"{NEON_G}✓ llama-cpp-python installed{R}")
    except ImportError:
        print(f"{NEON_R}✗ llama-cpp-python not found{R}")
        print(f"\n{NEON_Y}Install it:{R}")
        print(f"  pip install llama-cpp-python --break-system-packages\n")
        ans = input("Install now? [y/N]: ").strip().lower()
        if ans == "y":
            os.system("pip install llama-cpp-python --break-system-packages")
        else:
            print(f"{NEON_R}Cannot continue without llama-cpp-python{R}")
            return

    # model selection
    print(f"\n{NEON_Y}Do you have a .gguf model file already? [y/N]: {R}", end="")
    has_model = input().strip().lower()

    if has_model == "y":
        print(f"{NEON_C}Path to .gguf file: {R}", end="")
        path = input().strip()
        path = os.path.expanduser(path)
        if os.path.exists(path):
            cfg["model_path"] = path
            print(f"{NEON_G}✓ Model set: {path}{R}")
        else:
            print(f"{NEON_R}✗ File not found{R}")
    else:
        print(f"\n{NEON_Y}Available models to download:{R}\n")
        for k, m in KNOWN_MODELS.items():
            print(f"  {NEON_C}[{k}]{R} {m['name']}")
        print(f"\n{NEON_Y}Choose [1-{len(KNOWN_MODELS)}] or Enter to skip: {R}", end="")
        choice = input().strip()
        if choice in KNOWN_MODELS:
            model   = KNOWN_MODELS[choice]
            dl_dir  = os.path.expanduser("~/ollama-models")
            os.makedirs(dl_dir, exist_ok=True)
            dest    = os.path.join(dl_dir, model["file"])
            print(f"\n{NEON_C}Downloading {model['file']}…{R}")
            print(f"{DIM}This may take a while depending on your connection{R}\n")
            ret = os.system(f'wget -c -O "{dest}" "{model["url"]}"')
            if ret == 0 and os.path.exists(dest):
                cfg["model_path"] = dest
                print(f"\n{NEON_G}✓ Downloaded to: {dest}{R}")
            else:
                print(f"{NEON_R}✗ Download failed. Try manually:{R}")
                print(f"  wget -O ~/ollama-models/{model['file']} {model['url']}")

    # threads
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
    print(f"\n{NEON_Y}CPU threads to use [{cpu_count}]: {R}", end="")
    t = input().strip()
    cfg["threads"] = int(t) if t.isdigit() else cpu_count

    # GPU check
    gpu = _detect_gpu()
    if gpu["type"] == "nvidia":
        print(f"\n{NEON_G}✓ NVIDIA GPU detected: {gpu['name']} {gpu['vram']}{R}")
        print(f"{NEON_Y}For GPU acceleration, reinstall llama-cpp-python with CUDA:{R}")
        print(f"  {NEON_C}CMAKE_ARGS=\"-DGGML_CUDA=on\" pip install llama-cpp-python --force-reinstall --break-system-packages{R}")
        print(f"{DIM}(GPU will be used automatically every time you run the tool){R}")
    elif gpu["type"] == "amd":
        print(f"\n{NEON_Y}⚠ AMD GPU detected: {gpu['name']}{R}")
        print(f"{DIM}ROCm support is experimental. CPU will be used by default.{R}")
    elif gpu["type"] == "intel":
        print(f"\n{NEON_Y}⚠ Intel GPU detected: {gpu['name']}{R}")
        print(f"{DIM}Intel GPU acceleration not yet supported. CPU will be used.{R}")
    else:
        print(f"\n{DIM}No dedicated GPU detected — running on CPU (normal){R}")

    save_cfg(cfg)
    print(f"\n{NEON_G}✓ Setup complete!{R}")
    print(f"  Run: {NEON_C}python3 {sys.argv[0]}{R}\n")

# ══════════════════════════════════════════════════════════════
#  CORE ASK
# ══════════════════════════════════════════════════════════════
def ask(cfg: dict, messages: list, session_msgs: list,
        user_input: str, prefix: str = "") -> str:

    full_input = (prefix + "\n\n" + user_input).strip() if prefix else user_input
    messages.append({"role":"user","content":full_input})
    session_msgs.append({"role":"user","content":full_input})

    mode = MODES.get(cfg.get("mode","chat"), MODES["chat"])
    mc   = mode["color"]
    bw   = min(cols(), 62)

    full_response = []; token_count = 0; start = time.time()

    print(f"\n{mc}{'▓'*bw}{R}")
    print(f"{mc}{BOLD}  {mode['icon']} {mode['label']}{R}")
    print(f"{mc}{'▓'*bw}{R}\n")

    try:
        for token in stream_local(cfg, messages):
            sys.stdout.write(token); sys.stdout.flush()
            full_response.append(token); token_count += 1
    except KeyboardInterrupt:
        print(f"\n{NEON_Y}[interrupted]{R}")
    except Exception as e:
        print(f"\n{NEON_R}✗ {e}{R}")
        messages.pop(); session_msgs.pop()
        return ""

    elapsed  = time.time() - start
    response = "".join(full_response)
    messages.append({"role":"assistant","content":response})
    session_msgs.append({"role":"assistant","content":response})
    save_history(cfg["history_file"], session_msgs, cfg["max_history"])

    tok_s = token_count / elapsed if elapsed > 0 else 0
    print(f"\n\n{DIM}  ⏱ {elapsed:.1f}s · {token_count} tokens · {tok_s:.1f} tok/s{R}\n")

    action_results = process_actions(response)
    if action_results:
        messages.append({"role":"user","content":f"[SYSTEM] Results:\n{action_results}"})

    return response

# ══════════════════════════════════════════════════════════════
#  REPL
# ══════════════════════════════════════════════════════════════
def repl(cfg: dict, one_shot: str | None = None) -> None:
    try: import readline
    except: pass

    if not one_shot:
        startup_selector(cfg)
        show_tip()
        print_banner(cfg)

    mem          = load_memory()
    mode         = MODES.get(cfg.get("mode","chat"), MODES["chat"])
    messages     = [{"role":"system","content":""}]   # placeholder, filled below
    session_msgs : list = []
    last_response = ""

    def _build_sys() -> str:
        """Build the full system prompt: persona + mode + memory."""
        m    = MODES.get(cfg.get("mode","chat"), MODES["chat"])
        base = m["system"]
        # inject memory
        ctx = memory_context(mem)
        if ctx:
            base += f"\n\n{ctx}"
        # persona overrides the personality part but keeps mode instructions
        persona = cfg.get("persona","default")
        if persona and persona != "default" and persona in PERSONALITIES:
            base = PERSONALITIES[persona] + "\n\nAdditionally: " + base
        return base

    def rebuild_system() -> None:
        messages[0]["content"] = _build_sys()

    def switch_mode(new_mode: str) -> None:
        nonlocal messages
        cfg["mode"] = new_mode
        m = MODES[new_mode]
        new_msgs = [{"role":"system","content":_build_sys()}]
        messages.clear()
        messages.extend(new_msgs)
        session_msgs.clear()
        bw = min(cols(), 62)
        print(f"\n{m['color']}{BOLD}{'▓'*bw}\n  {m['icon']}  MODE → {m['label']}\n{'▓'*bw}{R}\n")

    # initialise system prompt now that helpers exist
    rebuild_system()

    if one_shot:
        ask(cfg, messages, session_msgs, one_shot)
        return

    while True:
        mode = MODES.get(cfg.get("mode","chat"), MODES["chat"])
        cwd  = os.path.basename(os.getcwd()) or "~"
        try:
            user_input = rich_prompt(mode["color"], mode["icon"], cwd)
        except KeyboardInterrupt:
            print(f"\n{DIM}Stay safe out there.{R}\n"); break

        if not user_input: continue

        if not user_input.startswith("/"):
            last_response = ask(cfg, messages, session_msgs, user_input)
            continue

        parts = user_input.split(maxsplit=1)
        cmd   = parts[0].lower()
        arg   = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("/vibe","/sec","/code","/chat","/agent"):
            switch_mode(cmd[1:])
        elif cmd == "/remember":
            cmd_remember(arg, mem)
            rebuild_system()
        elif cmd in ("/memories", "/memory"):
            cmd_memories(mem)
        elif cmd == "/forget":
            cmd_forget(arg, mem)
            rebuild_system()
        elif cmd == "/persona":
            cmd_persona(arg, cfg)
            rebuild_system()
        elif cmd == "/summarize":
            last_response = cmd_summarize_url(arg, cfg, messages, session_msgs)
        elif cmd == "/calc":
            cmd_calc(arg)
        elif cmd in ("/goals", "/goal"):
            parts2 = arg.split(maxsplit=1)
            action = parts2[0] if parts2 else ""
            arg2   = parts2[1] if len(parts2) > 1 else ""
            if action not in ("done","check","clear","reset","add"):
                cmd_goals("add", arg) if arg else cmd_goals("", "")
            else:
                cmd_goals(action, arg2)
        elif cmd in ("/exit","/quit","/q"):
            print(f"\n{DIM}Stay safe out there.{R}\n"); break
        elif cmd == "/help":     print_help()
        elif cmd == "/save":     save_cfg(cfg)
        elif cmd == "/clear":
            mode = MODES.get(cfg.get("mode","chat"),MODES["chat"])
            messages[:] = [{"role":"system","content":mode["system"]}]
            session_msgs.clear()
            print(f"{NEON_G}✓ Memory wiped.{R}\n")
        elif cmd == "/history":
            for m in messages:
                if m["role"]=="system": continue
                col = NEON_Y if m["role"]=="user" else NEON_G
                lbl = "YOU" if m["role"]=="user" else " AI"
                print(f"  {col}{BOLD}[{lbl}]{R} {textwrap.shorten(m['content'],70)}")
            print()
        elif cmd == "/temp":
            try: cfg["temperature"] = float(arg); print(f"{NEON_G}✓ Temp → {arg}{R}\n")
            except: print(f"{NEON_Y}Usage: /temp <0.0-2.0>{R}\n")
        elif cmd == "/info":
            mp = cfg.get("model_path","none")
            sz = f"{os.path.getsize(mp)/1e9:.1f} GB" if os.path.exists(mp) else "?"
            print(f"\n  {NEON_C}Model:{R}  {os.path.basename(mp)}")
            print(f"  {NEON_C}Size:{R}   {sz}")
            print(f"  {NEON_C}Ctx:{R}    {cfg['context']}")
            print(f"  {NEON_C}Temp:{R}   {cfg['temperature']}")
            print(f"  {NEON_C}Threads:{R}{cfg.get('threads',4)}\n")
        elif cmd == "/f":
            if not arg: print(f"{NEON_Y}Usage: /f <path>{R}\n")
            else:
                try:
                    path = os.path.expanduser(arg)
                    with open(path,"r",errors="replace") as f: content = f.read(50000)
                    ext    = os.path.splitext(arg)[1][1:] or ""
                    prefix = f"[FILE: {arg}]\n```{ext}\n{content}\n```"
                    print(f"{NEON_G}✓ Loaded {arg} ({len(content)} chars){R}")
                    sys.stdout.write(f"{NEON_C}What to do with it? ▶ {R}")
                    follow = input().strip()
                    if follow:
                        last_response = ask(cfg, messages, session_msgs, follow, prefix=prefix)
                except Exception as e: print(f"{NEON_R}✗ {e}{R}\n")
        elif cmd == "/o":
            if not arg: print(f"{NEON_Y}Usage: /o <path>{R}\n")
            elif not last_response: print(f"{NEON_Y}⚠ Nothing to save.{R}\n")
            else:
                try:
                    with open(os.path.expanduser(arg),"w") as f: f.write(last_response)
                    print(f"{NEON_G}✓ Saved → {arg}{R}\n")
                except Exception as e: print(f"{NEON_R}✗ {e}{R}\n")
        elif cmd == "/run":
            matches = re.findall(r"```(?:\w+)?\n(.*?)```", last_response, re.DOTALL)
            code    = matches[-1].strip() if matches else ""
            if not code: print(f"{NEON_Y}⚠ No code block found.{R}\n")
            else:
                print(f"{NEON_Y}Run:{R}\n{DIM}{code[:200]}{R}")
                if input(f"{NEON_R}Execute? [y/N]: {R}").strip().lower() == "y":
                    r = subprocess.run(["bash","-c",code], capture_output=True, text=True)
                    if r.stdout: print(f"{NEON_G}{r.stdout}{R}")
                    if r.stderr: print(f"{NEON_R}{r.stderr}{R}")
        elif cmd == "/copy":
            if not last_response: print(f"{NEON_Y}⚠ Nothing.{R}\n")
            else:
                for c in [["xclip","-selection","clipboard"],["xsel","--clipboard","--input"]]:
                    try:
                        p = subprocess.Popen(c, stdin=subprocess.PIPE)
                        p.communicate(last_response.encode())
                        print(f"{NEON_G}✓ Copied!{R}\n"); break
                    except FileNotFoundError: continue
                else: print(f"{NEON_Y}Install: sudo apt install xclip{R}\n")
        elif cmd == "/recon":
            if not arg: print(f"{NEON_Y}Usage: /recon <target>{R}\n")
            else:
                switch_mode("sec")
                last_response = ask(cfg, messages, session_msgs,
                    f"Full bug bounty recon plan for: {arg}. "
                    f"Cover subdomain enum, ports, tech fingerprinting, wayback, "
                    f"dir fuzzing, API discovery, vuln areas. Real commands only.")
        elif cmd == "/payload":
            switch_mode("sec")
            last_response = ask(cfg, messages, session_msgs,
                f"Generate comprehensive {(arg or 'xss').upper()} payloads for bug bounty: "
                f"basic, encoded, bypass, polyglots. Ready-to-use list.")
        elif cmd == "/explain":
            if not arg: print(f"{NEON_Y}Usage: /explain <cmd>{R}\n")
            else:
                last_response = ask(cfg, messages, session_msgs,
                    f"Explain this command step by step, all flags, security implications:\n`{arg}`")
        elif cmd == "/web":
            if not arg: print(f"{NEON_Y}Usage: /web <query>{R}\n")
            else:
                print(f"\n{NEON_C}🌐 Searching: {arg}…{R}\n")
                results = web_search(arg)
                print(f"{DIM}{results[:600]}…{R}\n")
                sys.stdout.write(f"{NEON_C}Ask AI about results? (Enter to skip): {R}")
                follow = input().strip()
                if follow:
                    last_response = ask(cfg, messages, session_msgs,
                        follow, prefix=f"[WEB SEARCH: {arg}]\n{results}")
                else:
                    last_response = ask(cfg, messages, session_msgs,
                        f"Summarize these search results about '{arg}':\n{results}")
        elif cmd == "/cvesearch":
            if not arg: print(f"{NEON_Y}Usage: /cvesearch <CVE-ID or software>{R}\n")
            else:
                print(f"\n{NEON_C}🔍 Searching CVE info for: {arg}…{R}\n")
                results = web_search(f"{arg} CVE vulnerability exploit POC", max_results=4)
                switch_mode("sec")
                last_response = ask(cfg, messages, session_msgs,
                    f"Analyze this CVE/vulnerability for bug bounty and pentesting:\n{results}\n\n"
                    f"Cover: severity, affected versions, exploit method, detection, mitigation.")
        elif cmd == "/tldr":
            last_response = cmd_tldr(arg, cfg, messages, session_msgs)
        elif cmd == "/howto":
            last_response = cmd_howto(arg, cfg, messages, session_msgs)
        elif cmd == "/fix":
            last_response = cmd_fix(arg, cfg, messages, session_msgs)
        elif cmd == "/passgen":
            cmd_passgen(arg)
        elif cmd == "/encode":
            cmd_encode(arg)
        elif cmd == "/syswatch":
            cmd_syswatch()
        elif cmd == "/benchmark":
            cmd_benchmark()
        elif cmd in ("/note", "/notes"):
            parts2 = arg.split(maxsplit=1)
            action = parts2[0] if parts2 else ""
            arg2   = parts2[1] if len(parts2) > 1 else ""
            # if action is not a subcommand keyword treat whole arg as note text
            if action not in ("list","show","ls","clear","wipe","del","delete","rm"):
                cmd_notes(arg, "")
            else:
                cmd_notes(action, arg2)
        elif cmd == "/tip":
            show_tip()
        elif cmd == "/explaincode":
            last_response = cmd_explain_code(arg, cfg, messages, session_msgs)
        elif cmd == "/roast":
            last_response = cmd_roast(arg, cfg, messages, session_msgs)
        elif cmd == "/challenge":
            last_response = cmd_challenge(arg, cfg, messages, session_msgs)
        elif cmd == "/recap":
            cmd_recap(messages)
        elif cmd == "/translate":
            last_response = cmd_translate(arg, cfg, messages, session_msgs)
        elif cmd == "/weather":
            cmd_weather_ascii(arg)
        elif cmd == "/timer":
            cmd_timer(arg)
        elif cmd == "/rename":
            last_response = cmd_ai_rename(arg, cfg, messages, session_msgs)
        elif cmd == "/regex":
            last_response = cmd_regex(arg, cfg, messages, session_msgs)
        elif cmd == "/git":
            last_response = cmd_githelp(arg, cfg, messages, session_msgs)
        elif cmd == "/ctf":
            last_response = cmd_ctf(arg, cfg, messages, session_msgs)
        elif cmd == "/diff":
            last_response = cmd_diff_explain(arg, cfg, messages, session_msgs)
        elif cmd == "/models":
            print(f"\n{NEON_Y}{BOLD}Available models to download:{R}\n")
            for k, m in KNOWN_MODELS.items():
                print(f"  {NEON_C}[{k}]{R} {m['name']}")
            print(f"\n{NEON_Y}Choose [1-{len(KNOWN_MODELS)}] or Enter to cancel: {R}", end="")
            choice = input().strip()
            if choice in KNOWN_MODELS:
                model  = KNOWN_MODELS[choice]
                dl_dir = os.path.expanduser("~/ollama-models")
                os.makedirs(dl_dir, exist_ok=True)
                dest   = os.path.join(dl_dir, model["file"])
                print(f"\n{NEON_C}Downloading {model['file']}…{R}")
                ret = os.system(f'wget -c -O "{dest}" "{model["url"]}"')
                if ret == 0 and os.path.exists(dest):
                    cfg["model_path"] = dest
                    save_cfg(cfg)
                    print(f"\n{NEON_G}✓ Downloaded! Restart to use new model.{R}\n")
                else:
                    print(f"{NEON_R}✗ Download failed.{R}\n")
        else:
            print(f"{NEON_R}Unknown: {cmd}{R} — /help\n")

# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cybersh",
        description="CYBER SH DIRECT — No server local LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-p","--prompt", help="One-shot prompt")
    parser.add_argument("-f","--file",   help="File context")
    parser.add_argument("-o","--output", help="Save output to file")
    parser.add_argument("-m","--model",  help="Path to .gguf model")
    parser.add_argument("-t","--temp",   type=float)
    parser.add_argument("--mode",        choices=list(MODES.keys()))
    parser.add_argument("--ctx",         type=int)
    parser.add_argument("--threads",     type=int)
    parser.add_argument("--setup",       action="store_true", help="Run setup wizard")
    parser.add_argument("--update",      action="store_true", help="Force update from GitHub")
    parser.add_argument("--no-update",   action="store_true", help="Skip update check")
    parser.add_argument("--version",     action="version", version="CYBER SH DIRECT v1.2")

    args = parser.parse_args()
    cfg  = load_cfg()

    if args.model:   cfg["model_path"]  = args.model
    if args.temp:    cfg["temperature"] = args.temp
    if args.mode:    cfg["mode"]        = args.mode
    if args.ctx:     cfg["context"]     = args.ctx
    if args.threads: cfg["threads"]     = args.threads

    if args.setup:
        setup_wizard(cfg); return

    # auto-update: run on interactive startup unless --no-update
    if not args.no_update and sys.stdin.isatty():
        check_and_update(force=getattr(args, 'update', False))
    elif getattr(args, 'update', False):
        check_and_update(force=True); return

    if not cfg.get("model_path") or not os.path.exists(cfg.get("model_path","")):
        print(f"\n{NEON_Y}No model configured. Running setup…{R}\n")
        setup_wizard(cfg)
        if not cfg.get("model_path"): return

    piped = ""
    if not sys.stdin.isatty(): piped = sys.stdin.read().strip()

    if args.prompt or piped:
        mode     = MODES.get(cfg.get("mode","chat"), MODES["chat"])
        messages = [{"role":"system","content":mode["system"]}]
        sess     = []
        prefix   = ""
        if args.file:
            try:
                with open(os.path.expanduser(args.file),"r",errors="replace") as f:
                    content = f.read(50000)
                ext    = os.path.splitext(args.file)[1][1:] or ""
                prefix = f"[FILE: {args.file}]\n```{ext}\n{content}\n```"
            except Exception as e:
                print(f"{NEON_R}✗ {e}{R}"); sys.exit(1)
        prompt   = args.prompt or ""
        if piped: prompt = f"{prompt}\n\nSTDIN:\n{piped}".strip()
        response = ask(cfg, messages, sess, prompt, prefix=prefix)
        if args.output and response:
            with open(os.path.expanduser(args.output),"w") as f: f.write(response)
            print(f"{NEON_G}✓ Saved → {args.output}{R}")
        return

    repl(cfg)

    if args.model:   cfg["model_path"]  = args.model
    if args.temp:    cfg["temperature"] = args.temp
    if args.mode:    cfg["mode"]        = args.mode
    if args.ctx:     cfg["context"]     = args.ctx
    if args.threads: cfg["threads"]     = args.threads

    if args.setup:
        setup_wizard(cfg); return

    if not cfg.get("model_path") or not os.path.exists(cfg.get("model_path","")):
        print(f"\n{NEON_Y}No model configured. Running setup…{R}\n")
        setup_wizard(cfg)
        if not cfg.get("model_path"): return

    piped = ""
    if not sys.stdin.isatty(): piped = sys.stdin.read().strip()

    if args.prompt or piped:
        mode     = MODES.get(cfg.get("mode","chat"), MODES["chat"])
        messages = [{"role":"system","content":mode["system"]}]
        sess     = []
        prefix   = ""
        if args.file:
            try:
                with open(os.path.expanduser(args.file),"r",errors="replace") as f:
                    content = f.read(50000)
                ext    = os.path.splitext(args.file)[1][1:] or ""
                prefix = f"[FILE: {args.file}]\n```{ext}\n{content}\n```"
            except Exception as e:
                print(f"{NEON_R}✗ {e}{R}"); sys.exit(1)
        prompt   = args.prompt or ""
        if piped: prompt = f"{prompt}\n\nSTDIN:\n{piped}".strip()
        response = ask(cfg, messages, sess, prompt, prefix=prefix)
        if args.output and response:
            with open(os.path.expanduser(args.output),"w") as f: f.write(response)
            print(f"{NEON_G}✓ Saved → {args.output}{R}")
        return

    repl(cfg)

if __name__ == "__main__":
    main()
