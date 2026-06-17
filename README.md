<div align="center">

```
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝
```

**CYBER SH — Your Personal Offline AI Assistant**  
Runs entirely on your own computer. No cloud. No subscriptions. No one watching.

![Version](https://img.shields.io/badge/version-1.2-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows%20WSL-lightgrey)

</div>

---

## 🌐 Do I Need Internet?

**Most features work 100% offline.** Internet is only used when you specifically ask for it:

| Feature | Needs Internet? |
|---------|----------------|
| AI chat, all modes | ❌ No |
| Memory, personas, goals | ❌ No |
| Code help, file analysis | ❌ No |
| Security tools, payloads | ❌ No |
| `/web` — web search | ✅ Yes |
| `/weather` — weather | ✅ Yes |
| `/summarize` — read a URL | ✅ Yes |
| `/cvesearch` — CVE lookup | ✅ Yes |
| Auto-update on startup | ✅ Yes (skipped automatically if offline) |

> **Privacy note:** When you use `/web` or any internet feature, your search goes directly from **your computer** to the search service. It never passes through any third-party server or CYBER SH infrastructure. Your queries are yours alone.

---

## 🔄 Updates — Nothing You Need to Do

CYBER SH **updates itself automatically every time you run it.**

- On startup it silently checks GitHub for a newer version
- If there is one, it downloads the new code, backs up your old file, installs any new packages, and restarts — all in seconds
- If you are offline, it simply skips the check and continues normally
- **You never need to run any update command manually — ever**

> Your AI models, chat memory, notes, goals, and config are **never touched by updates.** Only the script file itself gets replaced.

---

## ⚡ GPU — Automatic Every Time

CYBER SH automatically detects your GPU **every single time** you launch it. No config needed.

| GPU | What happens |
|-----|-------------|
| **NVIDIA** + CUDA installed | ✅ Full GPU acceleration — faster responses |
| **NVIDIA** without CUDA | Shows you one command to enable it, runs on CPU until then |
| **AMD** | Detected and shown, runs on CPU (ROCm experimental) |
| **Intel Arc / iGPU** | Detected and shown, runs on CPU |
| **No GPU** | Runs on CPU normally |

**To enable NVIDIA GPU acceleration (one time only):**
```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --break-system-packages
```
After that, every run will automatically use your GPU with no extra steps.

**Example of what you see on startup:**
```
✓ NVIDIA GPU: RTX 3060 (12GB VRAM) — CUDA ON ⚡
```

---

## ⚠️ Official Version Notice

> **The only official, safe, and maintained version of CYBER SH is published at:**  
> 👉 **[github.com/neo4-svg/cybersh](https://github.com/neo4-svg/cybersh)**
>
> Any version described as "unofficial", "uncensored", "cracked", or "modified" distributed anywhere else — on any forum, website, or file sharing platform — is **not authorized.** These versions may contain malware, backdoors, or stolen code and are a legal violation of the MIT license.
>
> **Found an unofficial version?** Please report it immediately:  
> 👉 [Open an issue here](https://github.com/neo4-svg/cybersh/issues) and include the link. We will act on every report.

---

## 🚀 Installation — Do This Once

> **You only do this once.** After setup, just run one command every time to launch.

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/neo4-svg/cybersh.git
cd cybersh
```

> This downloads everything to your computer. No extra downloads needed after this.

---

### Step 2 — Run setup

```bash
python3 cybersh_direct.py --setup
```

**The setup automatically:**
- Detects your operating system and GPU
- Installs the AI engine (`llama-cpp-python`)
- Installs web search support (`ddgs`)
- Lets you pick and download an AI model
- Saves your configuration

> ✅ You do not need to install anything separately. Setup handles everything.

---

### Step 3 — Launch it

```bash
python3 cybersh_direct.py
```

**That is it.** Every time you want to use CYBER SH, just run this one command from the `cybersh` folder. It will:
- Check for updates automatically
- Detect your GPU automatically
- Load your AI model
- Remember everything from your last session

---

## 🤖 Picking an AI Model

During setup, pick the model that fits your machine:

| # | Model | Size | RAM needed | Best for |
|---|-------|------|------------|----------|
| 1 | Phi-3 Mini | 2.2GB | 4GB+ | Code |
| 2 | TinyLlama 1.1B | 638MB | 2GB+ | Very low RAM machines |
| 3 | Qwen2.5 1.5B | 986MB | 3GB+ | Smart but lightweight |
| 4 | Mistral 7B | 4.1GB | 16GB+ | Best quality, needs good PC |
| **5** | **Llama 3.2 3B ★** | **2.0GB** | **7GB+** | **Best choice for most people** |
| 6 | Qwen2.5 7B | 4.7GB | 12GB+ | Great for code and reasoning |
| 7 | DeepSeek-R1 7B | 4.7GB | 12GB+ | Thinks step by step |

**Not sure which to pick?** Choose **[5] Llama 3.2 3B** — works great on most laptops.

You can download and switch models anytime inside the app with `/models`.

---

## 💻 Supported Systems

**Linux — all major distros:**
- Kali Linux, Parrot OS
- Ubuntu, Debian, Linux Mint, Pop!_OS
- Fedora, RHEL, AlmaLinux, Rocky Linux
- Arch Linux, Manjaro, EndeavourOS
- openSUSE, Alpine

**macOS** — works natively

**Windows** — via WSL2:
```powershell
# Run in PowerShell as Administrator:
wsl --install
# Then open WSL terminal and follow the Linux steps above
```

---

## ✨ Features

### Choose a mode when you start

```
[1] 🤖 Agent  — AI controls your computer (runs commands, creates files, opens apps)
[2] 🔐 Sec    — Security expert for bug bounty, pentesting, CVE analysis
[3] 🎨 Vibe   — Creative coding, beautiful UI, design ideas
[4] ⚡ Code   — Clean production code with error handling and comments
[5] 💬 Chat   — General assistant, ask it anything
```

Switch modes any time by typing `/agent`, `/sec`, `/vibe`, `/code`, or `/chat`.

---

### 🧠 Memory — AI remembers you between sessions

The AI remembers things you tell it, even after you close and reopen the tool:

```
/remember my name is Ahmed
/remember I work with Python 3.11
/remember project myapp is a Flask REST API

/memories          → show everything the AI knows about you
/forget python     → remove something from memory
```

---

### 🎭 AI Personalities

Change how the AI talks and thinks:

```
/persona teacher    → explains everything simply, like a patient teacher
/persona hacker     → talks like an elite security expert
/persona coach      → motivates you and breaks things into steps
/persona roaster    → roasts your bad code with humor (then fixes it)
/persona sherlock   → thinks and deduces like Sherlock Holmes
/persona prof       → formal university professor style
/persona eli5       → explains like you are 5 years old
/persona pirate     → pirate who is somehow a genius programmer
/persona stoic      → calm, wise, Marcus Aurelius energy
```

---

### 🌐 Internet features

These use your internet connection directly — no middleman server:

```
/web latest AI news 2026
→ searches DuckDuckGo and AI summarizes the results

/weather Washington D.C
→ shows ASCII weather forecast for Washington D.C

/weather Baghdad
→ shows weather for Baghdad

/summarize https://example.com/article
→ fetches the page and gives you a bullet point summary

/cvesearch CVE-2024-1234
→ searches for vulnerability info and gives full security analysis

/cvesearch apache log4j
→ finds known CVEs and explains them
```

---

### 🔐 Security tools

```
/recon example.com
→ full bug bounty recon plan: subdomains, ports, tech stack, fuzzing

/payload xss
→ ready-to-use XSS payloads: basic, encoded, polyglots, filter bypasses

/payload sqli
→ SQL injection payloads

/cvesearch CVE-2024-1234
→ severity, affected versions, exploit method, mitigation steps

/explain "nmap -sV -T4 192.168.1.1"
→ explains every flag and what the command does

/ctf aGVsbG8gd29ybGQ=
→ analyzes CTF challenge data, identifies encodings, guides you to solve it
```

---

### ⚡ Code tools

```
/explaincode
→ paste any code, AI explains every single line in plain English

/roast
→ AI finds every bad practice in your code with humor, then gives the fixed version

/fix ModuleNotFoundError: No module named 'requests'
→ paste any error message, get the exact fix

/howto zip a folder
→ get the exact Linux command for any task

/tldr chmod 755
→ plain English explanation of any Linux command

/regex match all email addresses
→ AI writes the regex pattern with examples and test cases

/git undo last commit without losing changes
→ exact git commands for anything you want to do

/diff
→ paste a git diff, AI tells you what changed and any risks

/rename user_data_processing_function
→ AI suggests 5 better names with reasons

/challenge hard
→ get a coding or hacking challenge to practice
```

---

### 🎯 Productivity tools

```
/goals
→ show today's goals with a progress bar

/goals add finish the login page
→ add a goal for today

/goals done 1
→ mark goal 1 as complete

/calc 15% of 240
→ quick math (/calc 2**32 also works)

/timer 25m
→ countdown timer with live progress bar (also: /timer 30s, /timer 1h)

/note remember to test the API endpoint
→ save a quick note to disk, persists between sessions

/notes list
→ show all your saved notes

/passgen
→ generate 3 strong passwords (16, 24, 32 chars)

/passgen phrase
→ generate passphrases like: ghost-vault-cipher-7291

/passgen api
→ generate a random 64-character API key

/encode hello world
→ shows Base64 + Hex + URL + MD5 + SHA1 + SHA256 all at once

/encode decode aGVsbG8gd29ybGQ=
→ decode Base64 back to text

/benchmark
→ tests CPU, RAM, and disk speed — gives a score and grade (S/A/B/C/D)

/syswatch
→ live CPU / RAM / disk monitor that updates every second (Ctrl+C to stop)

/translate arabic How are you today
→ translates any text to any language

/recap
→ summary of everything you asked this session

/tip
→ shows a useful Linux tip (changes every day)
```

---

### 📁 File tools

```
/f ~/myproject/app.py
→ loads a file so the AI can read and help with it

/o ~/output/fixed_script.py
→ saves the last AI response to a file

/run
→ runs the last code block the AI wrote (asks your confirmation first)

/copy
→ copies the last AI response to your clipboard
```

---

## 📋 Version History

| Version | What was added |
|---------|---------------|
| **v1.2** | Full GPU auto-detection (NVIDIA/AMD/Intel) · auto-updater with OS detection · memory system · 9 AI personas · daily goals · `/calc` · `/summarize` · `/timer` · `/weather` · `/passgen` · `/encode` · `/benchmark` · `/syswatch` · `/explaincode` · `/roast` · `/regex` · `/git` · `/diff` · `/ctf` · `/rename` · `/challenge` · `/translate` · `/recap` · tab autocomplete · arrow key history |
| **v1.1** | Web search (`/web`, `/cvesearch`) · 7 downloadable models · in-app model downloader |
| **v1.0** | Initial release — 5 modes · agent engine · file loading · chat history |

---

## 🐛 Troubleshooting

**Setup fails with build error:**
```bash
# Debian / Ubuntu / Kali
sudo apt install python3-dev build-essential -y

# Fedora
sudo dnf install python3-devel gcc gcc-c++ -y

# Arch
sudo pacman -S python base-devel --noconfirm
```

**No space for the model:**
```bash
df -h /home
mkdir -p ~/models
# When setup asks where to save the model, type: ~/models
```

**Model not found after setup:**
```bash
python3 cybersh_direct.py --setup
```

**`/web` not working:**
```bash
pip install ddgs --break-system-packages
```

**NVIDIA GPU not accelerating:**
```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --break-system-packages
# GPU will be used automatically every run after this
```

---

## 📁 What Updates Touch — What They Don't

| File | Location | Safe from updates? |
|------|----------|--------------------|
| `cybersh_direct.py` | your cybersh folder | 🔄 Replaced with new version |
| AI models | `~/ollama-models/` | ✅ Never touched |
| Your memories | `~/.cybersh_memory.json` | ✅ Never touched |
| Your config | `~/.cybersh_direct.json` | ✅ Never touched |
| Your notes | `~/.cybersh_notes.json` | ✅ Never touched |
| Your goals | `~/.cybersh_goals.json` | ✅ Never touched |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for full details.

Redistribution of modified versions must include the original license and credit the original author. Versions marketed as "uncensored", "cracked", or "unofficial" without proper attribution are a license violation and should be [reported here](https://github.com/neo4-svg/cybersh/issues).

---

<div align="center">

Made by <a href="https://github.com/neo4-svg">neo4-svg</a>

[⭐ Star this repo](https://github.com/neo4-svg/cybersh) · [🐛 Report a bug](https://github.com/neo4-svg/cybersh/issues) · [🚨 Report an unofficial version](https://github.com/neo4-svg/cybersh/issues)

</div>
