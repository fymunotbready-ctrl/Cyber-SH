#!/usr/bin/env python3
"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝
  CYBER SH DIRECT — No Server · Pure Python · llama-cpp-python
"""

import sys, os, json, time, shutil, re, subprocess, threading, datetime, textwrap, argparse, glob

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
        from duckduckgo_search import DDGS
    except ImportError:
        return (
            f"{NEON_R}✗ duckduckgo-search not installed.{R}\n"
            f"{NEON_Y}Fix:{R} pip install duckduckgo-search --break-system-packages"
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

    # Auto-detect GPU layers
    n_gpu_layers = 0
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            n_gpu_layers = -1  # -1 = offload all layers to GPU
            print(f"{NEON_G}✓ NVIDIA GPU detected — using GPU acceleration!{R}\n")
    except FileNotFoundError:
        pass  # No nvidia-smi, stay on CPU

    _llm_instance = Llama(
        model_path   = model_path,
        n_ctx        = cfg["context"],
        n_threads    = cfg.get("threads", 4),
        n_gpu_layers = n_gpu_layers,
        verbose      = False,
    )
    print(f"{NEON_G}✓ Model ready!{R}\n")
    return _llm_instance

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
          f"{NEON_Y}/code{R} {NEON_C}/chat{R} {NEON_O}/agent{R}  "
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
#  SETUP WIZARD
# ══════════════════════════════════════════════════════════════
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
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\n{NEON_G}✓ NVIDIA GPU detected!{R}")
            print(f"{NEON_Y}For GPU acceleration, reinstall llama-cpp-python with CUDA:{R}")
            print(f"  {NEON_C}CMAKE_ARGS=\"-DGGML_CUDA=on\" pip install llama-cpp-python --force-reinstall --break-system-packages{R}")
            print(f"{DIM}(Skip this if already done — GPU will be used automatically){R}")
    except FileNotFoundError:
        print(f"\n{DIM}No NVIDIA GPU detected — using CPU (normal){R}")

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
        print_banner(cfg)

    mode         = MODES.get(cfg.get("mode","chat"), MODES["chat"])
    messages     = [{"role":"system","content":mode["system"]}]
    session_msgs : list = []
    last_response = ""

    def switch_mode(new_mode: str) -> None:
        nonlocal messages
        cfg["mode"] = new_mode
        m = MODES[new_mode]
        messages = [{"role":"system","content":m["system"]}]
        session_msgs.clear()
        bw = min(cols(), 62)
        print(f"\n{m['color']}{BOLD}{'▓'*bw}\n  {m['icon']}  MODE → {m['label']}\n{'▓'*bw}{R}\n")

    if one_shot:
        ask(cfg, messages, session_msgs, one_shot)
        return

    while True:
        mode = MODES.get(cfg.get("mode","chat"), MODES["chat"])
        cwd  = os.path.basename(os.getcwd()) or "~"
        try:
            sys.stdout.write(f"{mode['color']}{BOLD}{mode['icon']}[{cwd}] ▶ {R}")
            sys.stdout.flush()
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
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
    parser.add_argument("--version",     action="version", version="CYBER SH DIRECT v1.0")

    args = parser.parse_args()
    cfg  = load_cfg()

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
