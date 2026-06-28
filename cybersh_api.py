"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║  ██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ███████╗███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ╚════██║██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ███████║██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝
  CYBER SH — FastAPI Web Backend  (v1.5)

  v1.5 Changes:
  - USER DATA ISOLATION: all memory/history/sessions/goals/notes scoped per user_id
  - DATA LEAK FIX: no shared global file paths; each user gets ~/.cybersh/<user_id>/
  - MULTI-LANGUAGE SUPPORT: 30+ UI + system prompt languages via ?lang= or X-Language header
  - EXTENDED SETTINGS: language, theme, font size, response style, AI creativity, chat density
  - CHAT HISTORY: full per-user conversation log with search and export
  - AI ADAPTIVE LEARNING: auto-extracts learnable facts from conversations into per-user memory
  - REMOVED: /api/upgrade endpoint
"""

from __future__ import annotations

import ast
import base64
import datetime
import glob
import hashlib
import json
import math
import os
import re
import secrets
import string
import subprocess
import sys
import textwrap
import time
import urllib.parse
import urllib.request
import ssl
import uuid as _uuid
from typing import Any, Generator

from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq
from auth import setup_auth_routes, get_optional_user

# ─────────────────────────────────────────────
#  APP
# ─────────────────────────────────────────────
app = FastAPI(
    title="Cyber-SH API",
    description="Web backend for Cyber-SH — AI security & dev toolkit",
    version="1.5.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_auth_routes(app)

# ─────────────────────────────────────────────
#  USER DATA ISOLATION — per-user directory tree
#  FIX: was using single global ~/.cybersh_memory.json etc.
#  Now each user gets their own ~/.cybersh/<user_id>/ directory.
#  Anonymous (unauthenticated) sessions get an "anon" bucket —
#  acceptable for single-device use, but multi-user MUST authenticate.
# ─────────────────────────────────────────────

CYBERSH_ROOT = os.path.expanduser("~/.cybersh")


def _user_dir(user_id: str) -> str:
    """Return (and create) the per-user data directory. Sanitise user_id."""
    safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", user_id)[:64] or "anon"
    path = os.path.join(CYBERSH_ROOT, safe_id)
    os.makedirs(path, exist_ok=True)
    return path


def _user_paths(user_id: str) -> dict[str, str]:
    d = _user_dir(user_id)
    return {
        "config":   os.path.join(d, "config.json"),
        "memory":   os.path.join(d, "memory.json"),
        "goals":    os.path.join(d, "goals.json"),
        "notes":    os.path.join(d, "notes.json"),
        "history":  os.path.join(d, "chat_history.json"),
        "sessions": os.path.join(d, "sessions"),
    }


def _resolve_user(
    authorization: str | None = None,
    x_user_id: str | None = None,
) -> str:
    """
    Resolve the effective user_id from:
      1. JWT via Authorization: Bearer  (verified with Supabase)
      2. X-User-Id header              (dev/fallback only)
      3. 'anon'                        (unauthenticated)
    """
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
        try:
            from auth import _get_supabase
            result = _get_supabase().auth.get_user(token)
            if result and result.user:
                return result.user.id
            # token was accepted but user object is empty
            return "anon"
        except Exception as exc:
            # Store reason so /api/whoami can surface it
            _resolve_user._last_error = str(exc)
    if x_user_id:
        return x_user_id
    return "anon"

_resolve_user._last_error: str = ""


# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────

DEFAULT_CFG: dict[str, Any] = {
    "groq_model": "llama-3.3-70b-versatile",
    "context": 4096,
    "temperature": 0.7,
    "max_tokens": 2048,
    "mode": "chat",
    "max_history": 60,
    "threads": 4,
    # New v1.5 settings
    "language": "en",
    "theme": "cyberpunk",
    "font_size": "md",
    "response_style": "balanced",   # concise | balanced | detailed
    "chat_density": "comfortable",  # compact | comfortable | spacious
    "show_tips": True,
    "stream_tokens": True,
    "auto_learn": True,             # AI learns from conversations
    "persona": "default",
}

THEMES = ["cyberpunk", "dark", "matrix", "midnight", "dracula", "nord", "solarized"]
FONT_SIZES = {"sm": "13px", "md": "15px", "lg": "17px", "xl": "20px"}
RESPONSE_STYLES = {
    "concise":  "Be very concise. Short answers only. No fluff.",
    "balanced": "Balance brevity with completeness.",
    "detailed": "Be thorough and detailed. Include examples, edge cases, and alternatives.",
}
CHAT_DENSITIES = ["compact", "comfortable", "spacious"]


# ─────────────────────────────────────────────
#  LANGUAGE SUPPORT
# ─────────────────────────────────────────────

SUPPORTED_LANGUAGES: dict[str, str] = {
    "en": "English",
    "ar": "Arabic / العربية",
    "zh": "Chinese (Simplified) / 中文",
    "zh-tw": "Chinese (Traditional) / 繁體中文",
    "fr": "French / Français",
    "de": "German / Deutsch",
    "es": "Spanish / Español",
    "pt": "Portuguese / Português",
    "ru": "Russian / Русский",
    "ja": "Japanese / 日本語",
    "ko": "Korean / 한국어",
    "hi": "Hindi / हिन्दी",
    "ur": "Urdu / اردو",
    "fa": "Persian / فارسی",
    "tr": "Turkish / Türkçe",
    "it": "Italian / Italiano",
    "nl": "Dutch / Nederlands",
    "pl": "Polish / Polski",
    "sv": "Swedish / Svenska",
    "no": "Norwegian / Norsk",
    "da": "Danish / Dansk",
    "fi": "Finnish / Suomi",
    "he": "Hebrew / עברית",
    "id": "Indonesian / Bahasa Indonesia",
    "ms": "Malay / Bahasa Melayu",
    "th": "Thai / ภาษาไทย",
    "vi": "Vietnamese / Tiếng Việt",
    "uk": "Ukrainian / Українська",
    "cs": "Czech / Čeština",
    "ro": "Romanian / Română",
    "hu": "Hungarian / Magyar",
    "el": "Greek / Ελληνικά",
}

RTL_LANGUAGES = {"ar", "he", "fa", "ur"}


def _lang_instruction(lang: str) -> str:
    if lang == "en" or lang not in SUPPORTED_LANGUAGES:
        return ""
    name = SUPPORTED_LANGUAGES[lang]
    return f"\n\nIMPORTANT: Always respond in {name}. The user's language is {name}."


# ─────────────────────────────────────────────
#  MODES & PERSONALITIES
# ─────────────────────────────────────────────

MODES: dict[str, dict] = {
    "chat": {
        "icon": "💬", "label": "CHAT",
        "system": "You are CYBER SH AI, a sharp helpful assistant. Be concise and direct.",
    },
    "sec": {
        "icon": "🔐", "label": "SEC",
        "system": (
            "You are an elite offensive security expert and bug bounty hunter. "
            "Help with recon, OSINT, XSS, SQLi, SSRF, LFI, RCE, IDOR, API testing, CVE analysis. "
            "Give real working commands and Python tools. Be technical and precise."
        ),
    },
    "vibe": {
        "icon": "🎨", "label": "VIBE",
        "system": (
            "You are an expert vibe coder. Build beautiful impressive projects fast. "
            "Write creative elegant code, suggest UI/UX aesthetics, color schemes, animations."
        ),
    },
    "code": {
        "icon": "⚡", "label": "CODE",
        "system": (
            "You are an elite software engineer — write production-grade code. "
            "Add proper error handling, type hints, comments only where they add real value. "
            "Prefer clear correct code over clever code."
        ),
    },
    "agent": {
        "icon": "🤖", "label": "AGENT",
        "system": (
            "You are CYBER SH AGENT, an AI assistant for Linux/terminal tasks. "
            "When asked to do things, explain what commands to run and why. "
            "Be safe: always warn before suggesting destructive operations."
        ),
    },
}

PERSONALITIES: dict[str, str] = {
    "default":  "You are CYBER SH, a helpful AI assistant. Be concise and direct.",
    "teacher":  "You are a patient teacher. Explain everything simply with analogies, never assume prior knowledge.",
    "hacker":   "You are an elite hacker mentor. Be direct, technical, use proper security terminology. Challenge the user to think deeper.",
    "coach":    "You are an energetic life and productivity coach. Be encouraging, positive, break problems into small steps.",
    "roaster":  "You are a brutally honest senior dev who roasts bad ideas and code with sharp humor — but ALWAYS follows up with the correct approach.",
    "sherlock": "You are Sherlock Holmes. Make deductions from every detail. Be dramatic, logical, brilliant. Say 'Elementary.' when obvious.",
    "prof":     "You are a university professor — expert, thorough, academic but approachable. Use precise language, structure answers clearly.",
    "eli5":     "You are explaining everything to a 5-year-old. Use the simplest words possible, fun analogies, and short sentences.",
    "pirate":   "You are a pirate who happens to be a genius programmer and hacker. Speak like a pirate but give genuinely expert technical advice.",
    "stoic":    "You are a Stoic philosopher AI. Give wise, calm, measured responses. Reference Marcus Aurelius, Epictetus, Seneca where relevant.",
}

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

GROQ_AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B — best quality (recommended)",
    "llama-3.1-8b-instant":    "Llama 3.1 8B — fastest responses",
    "mixtral-8x7b-32768":      "Mixtral 8x7B — great for code",
    "gemma2-9b-it":            "Gemma 2 9B — Google model",
}

# ─────────────────────────────────────────────
#  GROQ CLIENT
# ─────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL   = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
_groq_client: Groq | None = None


def get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is not None:
        return _groq_client
    if not GROQ_API_KEY:
        raise HTTPException(500, "GROQ_API_KEY environment variable not set.")
    _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client


def stream_llm(cfg: dict, messages: list) -> Generator[str, None, None]:
    client = get_groq_client()
    model = cfg.get("groq_model", GROQ_MODEL)
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=cfg.get("max_tokens", 2048),
        temperature=cfg.get("temperature", 0.7),
        stream=True,
    )
    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token


# ─────────────────────────────────────────────
#  SUPABASE STATE HELPERS  (generic get / set)
#  All authenticated user data lives in one table:
#
#  user_state (
#    user_id  TEXT PRIMARY KEY,
#    memory   JSONB DEFAULT '{}',
#    config   JSONB DEFAULT '{}',
#    goals    JSONB DEFAULT '[]',
#    notes    JSONB DEFAULT '[]',
#    history  JSONB DEFAULT '[]',
#    sessions JSONB DEFAULT '{}'
#  )
#
#  Anonymous users always fall back to local files.
# ─────────────────────────────────────────────

def _sb_get(user_id: str, field: str, default):
    """Fetch one JSONB field from user_state. Returns default on any error."""
    try:
        from auth import _get_supabase
        result = (
            _get_supabase()
            .table("user_state")
            .select(field)
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        if result.data and len(result.data) > 0:
            val = result.data[0].get(field)
            if val is not None:
                return val
    except Exception:
        pass
    return default() if callable(default) else default


def _sb_set(user_id: str, field: str, value) -> None:
    """Upsert one JSONB field in user_state. Best-effort — never raises."""
    try:
        from auth import _get_supabase
        _get_supabase().table("user_state").upsert(
            {"user_id": user_id, field: value},
            on_conflict="user_id",
        ).execute()
    except Exception:
        pass


# ─────────────────────────────────────────────
#  CONFIG HELPERS  (per-user, Supabase-backed)
# ─────────────────────────────────────────────

def load_cfg(user_id: str = "anon") -> dict:
    cfg = DEFAULT_CFG.copy()
    if user_id == "anon":
        path = _user_paths(user_id)["config"]
        if os.path.exists(path):
            try:
                with open(path) as f:
                    cfg.update(json.load(f))
            except Exception:
                pass
        return cfg
    saved = _sb_get(user_id, "config", dict)
    if saved:
        cfg.update(saved)
    return cfg


def save_cfg(cfg: dict, user_id: str = "anon") -> None:
    if user_id == "anon":
        path = _user_paths(user_id)["config"]
        with open(path, "w") as f:
            json.dump(cfg, f, indent=2)
        return
    _sb_set(user_id, "config", cfg)


# ─────────────────────────────────────────────
#  MEMORY HELPERS  (per-user, Supabase-backed)
# ─────────────────────────────────────────────

_MEMORY_EMPTY: dict[str, Any] = {"facts": [], "preferences": {}, "projects": {}, "learned": []}


def load_memory(user_id: str = "anon") -> dict:
    if user_id == "anon":
        path = _user_paths(user_id)["memory"]
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return _MEMORY_EMPTY.copy()
    return _sb_get(user_id, "memory", _MEMORY_EMPTY.copy)


def save_memory(mem: dict, user_id: str = "anon") -> None:
    if user_id == "anon":
        path = _user_paths(user_id)["memory"]
        with open(path, "w") as f:
            json.dump(mem, f, indent=2)
        return
    _sb_set(user_id, "memory", mem)


def memory_context(mem: dict) -> str:
    if not mem.get("facts") and not mem.get("preferences") and not mem.get("projects") and not mem.get("learned"):
        return ""
    parts = ["[MEMORY — things the user told you to remember:]"]
    if mem.get("facts"):
        parts.append("Facts: " + " | ".join(mem["facts"][-20:]))
    if mem.get("preferences"):
        prefs = ", ".join(f"{k}={v}" for k, v in mem["preferences"].items())
        parts.append(f"Preferences: {prefs}")
    if mem.get("projects"):
        for name, info in list(mem["projects"].items())[-5:]:
            parts.append(f"Project '{name}': {info}")
    if mem.get("learned"):
        parts.append("Learned about user: " + " | ".join(mem["learned"][-15:]))
    return "\n".join(parts)


# ─────────────────────────────────────────────
#  AI ADAPTIVE LEARNING
#  Extracts learnable facts from a conversation turn and stores
#  them in the user's memory automatically — making each user's
#  AI progressively more personalised.
# ─────────────────────────────────────────────

_LEARN_SYSTEM = """You are a memory extraction assistant.
Given the last user message and assistant reply, extract any NEW facts worth remembering about the user.
Focus on: preferences, technical skills, projects, tools they use, goals, personal context.
Output ONLY a JSON array of short strings (max 10 words each). Max 3 items. Empty array [] if nothing worth learning.
Example: ["prefers Python over JavaScript", "working on a bug bounty project", "uses Kali Linux on ThinkPad"]
Output ONLY valid JSON. No markdown, no explanation."""


def _auto_learn(user_msg: str, ai_reply: str, user_id: str) -> None:
    """Background extraction of learnable facts from a conversation turn."""
    try:
        cfg = load_cfg(user_id)
        if not cfg.get("auto_learn", True):
            return
        client = get_groq_client()
        prompt = f"User said: {user_msg[:500]}\n\nAssistant replied: {ai_reply[:500]}"
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # fast cheap model for extraction
            messages=[
                {"role": "system", "content": _LEARN_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.2,
            stream=False,
        )
        raw = resp.choices[0].message.content.strip()
        # strip markdown fences if present
        raw = re.sub(r"```[a-z]*", "", raw).strip("`").strip()
        facts = json.loads(raw)
        if not isinstance(facts, list):
            return
        mem = load_memory(user_id)
        existing = set(mem.get("learned", []))
        for fact in facts:
            if isinstance(fact, str) and fact.strip() and fact not in existing:
                mem.setdefault("learned", []).append(fact.strip())
                existing.add(fact)
        # cap at 100 learned facts
        mem["learned"] = mem["learned"][-100:]
        save_memory(mem, user_id)
    except Exception:
        pass   # learning is best-effort; never break the main chat


# ─────────────────────────────────────────────
#  CHAT HISTORY  (per-user, Supabase-backed)
# ─────────────────────────────────────────────

def load_history(user_id: str = "anon") -> list:
    if user_id == "anon":
        path = _user_paths(user_id)["history"]
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return []
    return _sb_get(user_id, "history", list)


def save_history(history: list, user_id: str = "anon") -> None:
    if user_id == "anon":
        path = _user_paths(user_id)["history"]
        with open(path, "w") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return
    _sb_set(user_id, "history", history)


def append_to_history(user_msg: str, ai_reply: str, mode: str, user_id: str) -> None:
    history = load_history(user_id)
    history.append({
        "id": str(_uuid.uuid4())[:8],
        "ts": datetime.datetime.now().isoformat(),
        "mode": mode,
        "user": user_msg,
        "assistant": ai_reply,
    })
    # keep last 500 turns per user
    if len(history) > 500:
        history = history[-500:]
    save_history(history, user_id)


# ─────────────────────────────────────────────
#  GOALS / NOTES HELPERS  (per-user, Supabase-backed)
# ─────────────────────────────────────────────

def load_goals(user_id: str = "anon") -> list:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if user_id == "anon":
        path = _user_paths(user_id)["goals"]
        try:
            with open(path) as f:
                data = json.load(f)
            return [g for g in data if g.get("date") == today]
        except Exception:
            return []
    data = _sb_get(user_id, "goals", list)
    return [g for g in data if g.get("date") == today]


def save_goals(goals: list, user_id: str = "anon") -> None:
    if user_id == "anon":
        path = _user_paths(user_id)["goals"]
        with open(path, "w") as f:
            json.dump(goals, f, indent=2)
        return
    # Preserve goals from other days; replace only today's
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    all_goals = _sb_get(user_id, "goals", list)
    other_days = [g for g in all_goals if g.get("date") != today]
    _sb_set(user_id, "goals", other_days + goals)


def load_notes(user_id: str = "anon") -> list:
    if user_id == "anon":
        path = _user_paths(user_id)["notes"]
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return []
    return _sb_get(user_id, "notes", list)


def save_notes(notes: list, user_id: str = "anon") -> None:
    if user_id == "anon":
        path = _user_paths(user_id)["notes"]
        with open(path, "w") as f:
            json.dump(notes, f, indent=2)
        return
    _sb_set(user_id, "notes", notes)


# ─────────────────────────────────────────────
#  SESSIONS  (per-user, Supabase-backed)
#  Anon  → local ~/.cybersh/anon/sessions/*.json
#  Auth  → user_state.sessions JSONB  {filename: session_data}
# ─────────────────────────────────────────────

def _sessions_dir(user_id: str) -> str:
    d = _user_paths(user_id)["sessions"]
    os.makedirs(d, exist_ok=True)
    return d


def get_safe_session_path(filename: str, user_id: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_\-]+\.json$", filename):
        raise HTTPException(400, "Invalid filename format.")
    sessions_dir = _sessions_dir(user_id)
    target = os.path.abspath(os.path.join(sessions_dir, filename))
    if not target.startswith(sessions_dir + os.sep):
        raise HTTPException(403, "Access Denied: Path Traversal Detected.")
    return target


def _load_all_sessions(user_id: str) -> dict:
    """Return {filename: session_data} for all saved sessions."""
    if user_id == "anon":
        sessions_dir = _sessions_dir(user_id)
        files = sorted(glob.glob(os.path.join(sessions_dir, "*.json")), reverse=True)
        result = {}
        for fpath in files[:50]:
            try:
                with open(fpath, encoding="utf-8") as f:
                    result[os.path.basename(fpath)] = json.load(f)
            except Exception:
                pass
        return result
    return _sb_get(user_id, "sessions", dict)


def _save_session_entry(filename: str, data: dict, user_id: str) -> None:
    if user_id == "anon":
        path = get_safe_session_path(filename, user_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return
    sessions = _sb_get(user_id, "sessions", dict)
    sessions[filename] = data
    _sb_set(user_id, "sessions", sessions)


def _delete_session_entry(filename: str, user_id: str) -> bool:
    if user_id == "anon":
        path = get_safe_session_path(filename, user_id)
        if not os.path.exists(path):
            return False
        os.remove(path)
        return True
    sessions = _sb_get(user_id, "sessions", dict)
    if filename not in sessions:
        return False
    del sessions[filename]
    _sb_set(user_id, "sessions", sessions)
    return True


# ─────────────────────────────────────────────
#  SYSTEM PROMPT BUILDER
# ─────────────────────────────────────────────

def build_system_prompt(cfg: dict, mem: dict | None = None) -> str:
    mode = MODES.get(cfg.get("mode", "chat"), MODES["chat"])
    base = mode["system"]

    persona = cfg.get("persona", "default")
    if persona and persona != "default" and persona in PERSONALITIES:
        base = PERSONALITIES[persona] + "\n\nAdditionally: " + base

    style = cfg.get("response_style", "balanced")
    style_instr = RESPONSE_STYLES.get(style, "")
    if style_instr:
        base += f"\n\nResponse style: {style_instr}"

    lang = cfg.get("language", "en")
    base += _lang_instruction(lang)

    if mem:
        ctx = memory_context(mem)
        if ctx:
            base += "\n\n" + ctx

    return base


def ai_complete(
    prompt: str,
    mode: str | None = None,
    persona: str | None = None,
    isolated: bool = False,
    user_id: str = "anon",
) -> str:
    cfg = load_cfg(user_id)
    if mode:
        cfg["mode"] = mode
    if persona:
        cfg["persona"] = persona

    if isolated:
        system_content = "You are a precise, focused assistant. Output only what is asked for."
    else:
        mem = load_memory(user_id)
        system_content = build_system_prompt(cfg, mem)

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt},
    ]
    try:
        return "".join(stream_llm(cfg, messages)).strip()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"AI completion failed: {e}")


# ─────────────────────────────────────────────
#  HTTP HELPER
# ─────────────────────────────────────────────

def http_get(url: str, timeout: int = 10) -> str | None:
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers={"User-Agent": "cybersh-api/1.5"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


# ─────────────────────────────────────────────
#  SAFE MATH EVAL
# ─────────────────────────────────────────────

def safe_math_eval(expr: str) -> float | int:
    allowed_operators = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a ** b,
        ast.USub: lambda a: -a,
        ast.UAdd: lambda a: a
    }

    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise TypeError("Invalid constant type")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        else:
            raise ValueError(f"Unsupported node: {type(node).__name__}")

    try:
        clean_expr = expr.strip().replace(" ", "")
        tree = ast.parse(clean_expr, mode='eval')
        return _eval(tree.body)
    except Exception:
        raise ValueError("Failed to evaluate expression securely.")


# ─────────────────────────────────────────────
#  REQUEST MODELS
# ─────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    mode: str = "chat"
    persona: str = "default"
    temperature: float = 0.7
    stream: bool = True
    use_memory: bool = True
    save_history: bool = True   # NEW: persist turn to history


class ConfigUpdateRequest(BaseModel):
    model_path: str | None = None
    temperature: float | None = None
    context: int | None = None
    threads: int | None = None
    mode: str | None = None
    persona: str | None = None
    # New v1.5 settings
    language: str | None = None
    theme: str | None = None
    font_size: str | None = None
    response_style: str | None = None
    chat_density: str | None = None
    show_tips: bool | None = None
    stream_tokens: bool | None = None
    auto_learn: bool | None = None
    groq_model: str | None = None


class MemoryAddRequest(BaseModel):
    text: str

class MemoryDeleteRequest(BaseModel):
    keyword: str

class GoalAddRequest(BaseModel):
    text: str

class NoteAddRequest(BaseModel):
    text: str

class SessionSaveRequest(BaseModel):
    name: str
    messages: list[ChatMessage]
    mode: str = "chat"

class AIBasicRequest(BaseModel):
    text: str
    mode: str | None = None
    persona: str | None = None

class AIExplainCodeRequest(AIBasicRequest): pass
class AIRoastRequest(AIBasicRequest): pass

class AIChallengeRequest(BaseModel):
    level: str = "medium"
    mode: str | None = None
    persona: str | None = None

class AITranslateRequest(BaseModel):
    language: str
    text: str

class AIRenameRequest(BaseModel):
    identifier: str
    mode: str | None = None
    persona: str | None = None

class AIRegexRequest(BaseModel):
    description: str
    mode: str | None = None
    persona: str | None = None

class AIGitHelpRequest(BaseModel):
    query: str
    mode: str | None = None
    persona: str | None = None

class AICTFRequest(BaseModel):
    text: str
    mode: str | None = None
    persona: str | None = None

class AIDiffExplainRequest(BaseModel):
    diff: str
    mode: str | None = None
    persona: str | None = None

class AISummarizeUrlRequest(BaseModel):
    url: str
    mode: str | None = None
    persona: str | None = None

class AIFixRequest(BaseModel):
    error: str
    mode: str | None = None
    persona: str | None = None

class AIHowtoRequest(BaseModel):
    task: str
    mode: str | None = None
    persona: str | None = None

class AITldrRequest(BaseModel):
    command: str
    mode: str | None = None
    persona: str | None = None

class AIDebugRequest(BaseModel):
    code: str
    mode: str | None = None
    persona: str | None = None

class AIReviewRequest(BaseModel):
    code: str
    mode: str | None = None
    persona: str | None = None

class AITemplateRequest(BaseModel):
    project_type: str
    mode: str | None = None
    persona: str | None = None

class AIGitLogRequest(BaseModel):
    target: str = ""
    repo_path: str | None = None
    limit: int = 20
    mode: str | None = None
    persona: str | None = None

class AIOsintRequest(BaseModel):
    target: str
    mode: str | None = None
    persona: str | None = None

class AIWordlistRequest(BaseModel):
    info: str
    mode: str | None = None
    persona: str | None = None

class AIThinkRequest(BaseModel):
    question: str
    mode: str | None = None
    persona: str | None = None

class AIDebateRequest(BaseModel):
    topic: str
    mode: str | None = None
    persona: str | None = None

class AIImproveRequest(BaseModel):
    text: str
    mode: str | None = None
    persona: str | None = None

class AIEli5Request(BaseModel):
    topic: str
    mode: str | None = None
    persona: str | None = None

class AICronRequest(BaseModel):
    expression: str
    mode: str | None = None
    persona: str | None = None

class AIQuizRequest(BaseModel):
    topic: str
    mode: str | None = None
    persona: str | None = None

class AINameBrainstormRequest(BaseModel):
    description: str
    mode: str | None = None
    persona: str | None = None

class AICheatsheetRequest(BaseModel):
    topic: str
    mode: str | None = None
    persona: str | None = None

class RecapRequest(BaseModel):
    messages: list[ChatMessage]

class ToolConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

class ToolEncodeRequest(BaseModel):
    text: str
    decode: bool = False

class ToolHashRequest(BaseModel):
    hash: str

class ToolUUIDRequest(BaseModel):
    count: int = 1
    namespace: str | None = None

class ToolJSONRequest(BaseModel):
    text: str
    minify: bool = False

class ToolBaseRequest(BaseModel):
    number: str
    from_base: int | None = None

class ToolColorRequest(BaseModel):
    color: str

class ToolCalcRequest(BaseModel):
    expression: str

class ToolPwCheckRequest(BaseModel):
    password: str


# ─────────────────────────────────────────────
#  USER IDENTITY HELPER  (extracts user_id from headers)
# ─────────────────────────────────────────────

def _uid(
    authorization: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
) -> str:
    return _resolve_user(authorization, x_user_id)


# ─────────────────────────────────────────────
#  ROUTES — SYSTEM
# ─────────────────────────────────────────────

@app.get("/api/status")
def status(user_id: str = Depends(_uid)):
    cfg = load_cfg(user_id)
    groq_ready = bool(GROQ_API_KEY)
    return {
        "version": "1.5",
        "model_loaded": groq_ready,
        "model_name": cfg.get("groq_model", GROQ_MODEL),
        "model_size": "cloud",
        "backend": "groq",
        "mode": cfg.get("mode", "chat"),
        "temperature": cfg.get("temperature", 0.7),
        "language": cfg.get("language", "en"),
        "theme": cfg.get("theme", "cyberpunk"),
    }


@app.get("/api/whoami")
def whoami(
    authorization: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """
    Debug endpoint — shows exactly how the server resolved your identity.
    Call this from your frontend (with the same headers you send to /api/chat)
    to confirm auth is working.
    """
    user_id = _resolve_user(authorization, x_user_id)
    auth_error = _resolve_user._last_error or None
    _resolve_user._last_error = ""  # clear after reading

    supabase_configured = bool(
        os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_ANON_KEY")
    )

    return {
        "user_id": user_id,
        "authenticated": user_id != "anon",
        "auth_header_received": bool(authorization),
        "auth_header_format_ok": bool(
            authorization and authorization.lower().startswith("bearer ")
        ),
        "x_user_id_header": x_user_id,
        "supabase_configured": supabase_configured,
        "auth_error": auth_error,
        "hint": (
            "Auth is working correctly."
            if user_id != "anon"
            else (
                "No auth header sent — frontend must include: "
                "Authorization: Bearer <access_token>"
                if not authorization
                else f"Token was sent but auth failed: {auth_error or 'unknown error'}"
            )
        ),
    }


@app.get("/api/modes")
def get_modes():
    return {k: {"icon": v["icon"], "label": v["label"]} for k, v in MODES.items()}


@app.get("/api/personas")
def get_personas():
    return {k: v[:100] + "…" for k, v in PERSONALITIES.items()}


@app.get("/api/tip")
def get_tip(user_id: str = Depends(_uid)):
    cfg = load_cfg(user_id)
    if not cfg.get("show_tips", True):
        return {"tip": None}
    day_seed = datetime.datetime.now().strftime("%Y%m%d")
    idx = int(hashlib.md5(day_seed.encode()).hexdigest(), 16) % len(TIPS)
    return {"tip": TIPS[idx]}


@app.get("/api/config")
def get_config(user_id: str = Depends(_uid)):
    return load_cfg(user_id)


@app.patch("/api/config")
def update_config(req: ConfigUpdateRequest, user_id: str = Depends(_uid)):
    cfg = load_cfg(user_id)
    if req.model_path is not None:
        cfg["groq_model"] = req.model_path
    if req.groq_model is not None:
        if req.groq_model not in GROQ_AVAILABLE_MODELS:
            raise HTTPException(400, f"Unknown model: {req.groq_model}")
        cfg["groq_model"] = req.groq_model
    if req.temperature is not None:
        cfg["temperature"] = max(0.0, min(2.0, req.temperature))
    if req.context is not None:
        cfg["context"] = req.context
    if req.threads is not None:
        cfg["threads"] = req.threads
    if req.mode is not None:
        if req.mode not in MODES:
            raise HTTPException(400, f"Unknown mode: {req.mode}")
        cfg["mode"] = req.mode
    if req.persona is not None:
        if req.persona not in PERSONALITIES:
            raise HTTPException(400, f"Unknown persona: {req.persona}")
        cfg["persona"] = req.persona
    # v1.5 settings
    if req.language is not None:
        if req.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(400, f"Unsupported language: {req.language}. See /api/languages")
        cfg["language"] = req.language
    if req.theme is not None:
        if req.theme not in THEMES:
            raise HTTPException(400, f"Unknown theme. Options: {THEMES}")
        cfg["theme"] = req.theme
    if req.font_size is not None:
        if req.font_size not in FONT_SIZES:
            raise HTTPException(400, f"Unknown font_size. Options: {list(FONT_SIZES.keys())}")
        cfg["font_size"] = req.font_size
    if req.response_style is not None:
        if req.response_style not in RESPONSE_STYLES:
            raise HTTPException(400, f"Unknown response_style. Options: {list(RESPONSE_STYLES.keys())}")
        cfg["response_style"] = req.response_style
    if req.chat_density is not None:
        if req.chat_density not in CHAT_DENSITIES:
            raise HTTPException(400, f"Unknown chat_density. Options: {CHAT_DENSITIES}")
        cfg["chat_density"] = req.chat_density
    if req.show_tips is not None:
        cfg["show_tips"] = req.show_tips
    if req.stream_tokens is not None:
        cfg["stream_tokens"] = req.stream_tokens
    if req.auto_learn is not None:
        cfg["auto_learn"] = req.auto_learn
    save_cfg(cfg, user_id)
    return {"ok": True, "config": cfg}


@app.get("/api/models")
def get_models():
    return GROQ_AVAILABLE_MODELS


@app.get("/api/languages")
def get_languages():
    return {
        "languages": SUPPORTED_LANGUAGES,
        "rtl": list(RTL_LANGUAGES),
    }


@app.get("/api/settings/options")
def settings_options():
    """Return all available setting values — use this to populate settings UI."""
    return {
        "themes": THEMES,
        "font_sizes": FONT_SIZES,
        "response_styles": list(RESPONSE_STYLES.keys()),
        "chat_densities": CHAT_DENSITIES,
        "groq_models": GROQ_AVAILABLE_MODELS,
        "modes": {k: {"icon": v["icon"], "label": v["label"]} for k, v in MODES.items()},
        "personas": list(PERSONALITIES.keys()),
        "languages": SUPPORTED_LANGUAGES,
        "rtl_languages": list(RTL_LANGUAGES),
    }


# ─────────────────────────────────────────────
#  ROUTES — AI CHAT
# ─────────────────────────────────────────────

@app.post("/api/chat")
def chat(req: ChatRequest, user_id: str = Depends(_uid)):
    cfg = load_cfg(user_id)
    cfg["mode"] = req.mode
    cfg["temperature"] = req.temperature
    if req.persona:
        cfg["persona"] = req.persona

    mem = load_memory(user_id) if req.use_memory else None
    system_content = build_system_prompt(cfg, mem)

    messages = [{"role": "system", "content": system_content}]
    for m in req.messages:
        messages.append({"role": m.role, "content": m.content})

    # identify the last user message for history & learning
    last_user_msg = next(
        (m.content for m in reversed(req.messages) if m.role == "user"), ""
    )

    if req.stream:
        collected: list[str] = []

        def event_stream():
            try:
                for token in stream_llm(cfg, messages):
                    collected.append(token)
                    data = json.dumps({"token": token})
                    yield f"data: {data}\n\n"
                # after streaming completes, persist history + trigger learning
                ai_reply = "".join(collected)
                if req.save_history and last_user_msg:
                    append_to_history(last_user_msg, ai_reply, req.mode, user_id)
                    _auto_learn(last_user_msg, ai_reply, user_id)
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': 'Streaming error.'})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")
    else:
        response = "".join(stream_llm(cfg, messages))
        if req.save_history and last_user_msg:
            append_to_history(last_user_msg, response, req.mode, user_id)
            _auto_learn(last_user_msg, response, user_id)
        return {"response": response, "mode": req.mode}


# ─────────────────────────────────────────────
#  ROUTES — CHAT HISTORY  (NEW)
# ─────────────────────────────────────────────

@app.get("/api/history")
def get_history(
    limit: int = Query(50, le=500),
    offset: int = Query(0, ge=0),
    mode: str | None = Query(None),
    user_id: str = Depends(_uid),
):
    """Return paginated per-user chat history."""
    history = load_history(user_id)
    if mode:
        history = [h for h in history if h.get("mode") == mode]
    total = len(history)
    # newest first
    page = list(reversed(history))[offset: offset + limit]
    return {"total": total, "offset": offset, "limit": limit, "history": page}


@app.get("/api/history/search")
def search_history(
    q: str = Query(..., min_length=1),
    user_id: str = Depends(_uid),
):
    """Full-text search over user's chat history."""
    history = load_history(user_id)
    results = []
    for turn in reversed(history):
        if q.lower() in turn.get("user", "").lower() or q.lower() in turn.get("assistant", "").lower():
            results.append(turn)
        if len(results) >= 30:
            break
    return {"query": q, "count": len(results), "results": results}


@app.delete("/api/history")
def clear_history(user_id: str = Depends(_uid)):
    """Wipe all chat history for this user."""
    save_history([], user_id)
    return {"ok": True}


@app.delete("/api/history/{turn_id}")
def delete_history_turn(turn_id: str, user_id: str = Depends(_uid)):
    """Delete a single history turn by id."""
    history = load_history(user_id)
    before = len(history)
    history = [h for h in history if h.get("id") != turn_id]
    if len(history) == before:
        raise HTTPException(404, "Turn not found.")
    save_history(history, user_id)
    return {"ok": True, "deleted": turn_id}


# ─────────────────────────────────────────────
#  ROUTES — MEMORY
# ─────────────────────────────────────────────

@app.get("/api/memory")
def get_memory(user_id: str = Depends(_uid)):
    return load_memory(user_id)


@app.post("/api/memory")
def add_memory(req: MemoryAddRequest, user_id: str = Depends(_uid)):
    mem = load_memory(user_id)
    arg = req.text.strip()

    if arg.lower().startswith("project "):
        rest = arg[8:].strip().split(" ", 1)
        name = rest[0]
        info = rest[1] if len(rest) > 1 else ""
        mem["projects"][name] = info
        save_memory(mem, user_id)
        return {"ok": True, "type": "project", "name": name}

    if "=" in arg and len(arg.split("=")) == 2:
        k, v = arg.split("=", 1)
        mem["preferences"][k.strip()] = v.strip()
        save_memory(mem, user_id)
        return {"ok": True, "type": "preference", "key": k.strip(), "value": v.strip()}

    ts = datetime.datetime.now().strftime("%Y-%m-%d")
    fact = f"[{ts}] {arg}"
    mem["facts"].append(fact)
    if len(mem["facts"]) > 100:
        mem["facts"].pop(0)
    save_memory(mem, user_id)
    return {"ok": True, "type": "fact", "fact": fact}


@app.delete("/api/memory")
def delete_memory(req: MemoryDeleteRequest, user_id: str = Depends(_uid)):
    mem = load_memory(user_id)
    keyword = req.keyword
    removed = 0
    if keyword in mem.get("projects", {}):
        del mem["projects"][keyword]; removed += 1
    if keyword in mem.get("preferences", {}):
        del mem["preferences"][keyword]; removed += 1
    before = len(mem.get("facts", []))
    mem["facts"] = [f for f in mem.get("facts", []) if keyword.lower() not in f.lower()]
    removed += before - len(mem["facts"])
    save_memory(mem, user_id)
    return {"ok": True, "removed": removed, "keyword": keyword}


@app.delete("/api/memory/learned")
def clear_learned_memory(user_id: str = Depends(_uid)):
    """Clear only the auto-learned facts (keeps manual memory intact)."""
    mem = load_memory(user_id)
    mem["learned"] = []
    save_memory(mem, user_id)
    return {"ok": True}


@app.delete("/api/memory/all")
def clear_memory(user_id: str = Depends(_uid)):
    save_memory({"facts": [], "preferences": {}, "projects": {}, "learned": []}, user_id)
    return {"ok": True}


# ─────────────────────────────────────────────
#  ROUTES — GOALS
# ─────────────────────────────────────────────

@app.get("/api/goals")
def get_goals(user_id: str = Depends(_uid)):
    goals = load_goals(user_id)
    done = sum(1 for g in goals if g.get("done"))
    return {
        "goals": goals, "total": len(goals), "done": done,
        "progress_pct": int(100 * done / len(goals)) if goals else 0,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }


@app.post("/api/goals")
def add_goal(req: GoalAddRequest, user_id: str = Depends(_uid)):
    goals = load_goals(user_id)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    goals.append({"date": today, "text": req.text.strip(), "done": False})
    save_goals(goals, user_id)
    return {"ok": True, "goals": goals}


@app.patch("/api/goals/{index}")
def complete_goal(index: int, user_id: str = Depends(_uid)):
    goals = load_goals(user_id)
    if index < 1 or index > len(goals):
        raise HTTPException(404, "Goal not found.")
    goals[index - 1]["done"] = True
    save_goals(goals, user_id)
    return {"ok": True, "goals": goals}


@app.delete("/api/goals")
def clear_goals(user_id: str = Depends(_uid)):
    save_goals([], user_id)
    return {"ok": True}


# ─────────────────────────────────────────────
#  ROUTES — NOTES
# ─────────────────────────────────────────────

@app.get("/api/notes")
def get_notes(user_id: str = Depends(_uid)):
    return {"notes": load_notes(user_id)}


@app.post("/api/notes")
def add_note(req: NoteAddRequest, user_id: str = Depends(_uid)):
    notes = load_notes(user_id)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    notes.append({"time": ts, "text": req.text.strip()})
    save_notes(notes, user_id)
    return {"ok": True, "notes": notes}


@app.delete("/api/notes/{index}")
def delete_note(index: int, user_id: str = Depends(_uid)):
    notes = load_notes(user_id)
    if index < 1 or index > len(notes):
        raise HTTPException(404, "Note not found.")
    removed = notes.pop(index - 1)
    save_notes(notes, user_id)
    return {"ok": True, "removed": removed}


@app.delete("/api/notes")
def clear_notes(user_id: str = Depends(_uid)):
    save_notes([], user_id)
    return {"ok": True}


# ─────────────────────────────────────────────
#  ROUTES — SESSIONS
# ─────────────────────────────────────────────

@app.get("/api/sessions")
def list_sessions(user_id: str = Depends(_uid)):
    all_sessions = _load_all_sessions(user_id)
    sessions = []
    for i, (filename, d) in enumerate(
        sorted(all_sessions.items(), reverse=True)[:50], 1
    ):
        sessions.append({
            "index": i,
            "name": d.get("name", "?"),
            "saved_at": d.get("saved_at", "?"),
            "mode": d.get("mode", "chat"),
            "turns": d.get("turns", 0),
            "filename": filename,
        })
    return {"sessions": sessions}


@app.post("/api/sessions")
def save_session(req: SessionSaveRequest, user_id: str = Depends(_uid)):
    convo = [m.dict() for m in req.messages if m.role in ("user", "assistant")]
    if not convo:
        raise HTTPException(400, "No valid messages to save.")
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", req.name)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{safe_name}__{ts}.json"
    data = {
        "name": req.name, "saved_at": ts, "mode": req.mode,
        "messages": convo,
        "turns": sum(1 for m in convo if m["role"] == "user"),
    }
    _save_session_entry(filename, data, user_id)
    return {"ok": True, "filename": filename, "turns": data["turns"]}


@app.get("/api/sessions/{filename}")
def load_session(filename: str, user_id: str = Depends(_uid)):
    all_sessions = _load_all_sessions(user_id)
    if filename not in all_sessions:
        raise HTTPException(404, "Session not found.")
    return all_sessions[filename]


@app.delete("/api/sessions/{filename}")
def delete_session(filename: str, user_id: str = Depends(_uid)):
    if not _delete_session_entry(filename, user_id):
        raise HTTPException(404, "Session not found.")
    return {"ok": True, "deleted": filename}


@app.get("/api/sessions/search/{keyword}")
def search_sessions(keyword: str, user_id: str = Depends(_uid)):
    all_sessions = _load_all_sessions(user_id)
    found = []
    for filename, data in sorted(all_sessions.items(), reverse=True):
        hits = []
        for msg in data.get("messages", []):
            content = msg.get("content", "")
            if keyword.lower() in content.lower():
                idx = content.lower().find(keyword.lower())
                start = max(0, idx - 40)
                end = min(len(content), idx + 80)
                snip = content[start:end].replace("\n", " ").strip()
                hits.append({"role": msg["role"], "snippet": f"…{snip}…"})
        if hits:
            found.append({
                "name": data.get("name", "?"), "saved_at": data.get("saved_at", "?"),
                "filename": filename, "hits": hits[:3], "total_hits": len(hits),
            })
    return {"keyword": keyword, "results": found, "count": len(found)}


# ─────────────────────────────────────────────
#  ROUTES — RECAP
# ─────────────────────────────────────────────

@app.post("/api/recap")
def recap(req: RecapRequest, user_id: str = Depends(_uid)):
    if not req.messages:
        raise HTTPException(400, "No messages to recap.")
    convo = "\n".join(
        f"{m.role.upper()}: {m.content}"
        for m in req.messages if m.role in ("user", "assistant")
    )
    result = ai_complete(
        f"Give a concise bullet-point summary of this conversation. "
        f"List: key topics, decisions made, code/commands discussed, any open questions.\n\n{convo}",
        user_id=user_id,
    )
    return {"recap": result}


# ─────────────────────────────────────────────
#  ROUTES — AI FEATURES
# ─────────────────────────────────────────────

@app.post("/api/ai/explain-code")
def ai_explain_code(req: AIExplainCodeRequest, user_id: str = Depends(_uid)):
    if not req.text.strip():
        raise HTTPException(400, "No code provided.")
    result = ai_complete(
        f"Explain this code line by line in plain English.\n\n```\n{req.text}\n```",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/roast")
def ai_roast(req: AIRoastRequest, user_id: str = Depends(_uid)):
    if not req.text.strip():
        raise HTTPException(400, "No code provided.")
    result = ai_complete(
        f"Roast this code like a senior dev. Be funny but accurate. "
        f"Then give the fixed version.\n\n```\n{req.text}\n```",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/challenge")
def ai_challenge(req: AIChallengeRequest, user_id: str = Depends(_uid)):
    cfg = load_cfg(user_id)
    mode = req.mode or cfg.get("mode", "chat")
    if mode == "sec":
        topic = "penetration testing or CTF"
    elif mode in ("code", "vibe"):
        topic = "programming"
    else:
        topic = "Linux or general tech"
    result = ai_complete(
        f"Give me a {req.level} difficulty {topic} challenge with hints hidden in spoiler blocks.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result, "level": req.level}


@app.post("/api/ai/translate")
def ai_translate(req: AITranslateRequest, user_id: str = Depends(_uid)):
    if not req.text.strip():
        raise HTTPException(400, "No text provided.")
    cfg = load_cfg(user_id)
    messages = [
        {"role": "system", "content": "You are a translation engine. Output ONLY the translated text."},
        {"role": "user", "content": f"Translate to {req.language}:\n{req.text}"},
    ]
    try:
        result = "".join(stream_llm(cfg, messages)).strip()
    except Exception as e:
        raise HTTPException(500, f"Translation failed: {e}")
    return {"result": result, "language": req.language}


@app.post("/api/ai/rename")
def ai_rename(req: AIRenameRequest, user_id: str = Depends(_uid)):
    if not req.identifier.strip():
        raise HTTPException(400, "No identifier provided.")
    result = ai_complete(
        f"Suggest 5 better names for `{req.identifier}` with reasons.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/regex")
def ai_regex(req: AIRegexRequest, user_id: str = Depends(_uid)):
    if not req.description.strip():
        raise HTTPException(400, "No description provided.")
    result = ai_complete(
        f"Write a regex for: {req.description}. Include Python/JS/grep examples and test cases.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/githelp")
def ai_githelp(req: AIGitHelpRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Git help: {req.query}. Give the exact commands with explanations.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/ctf")
def ai_ctf(req: AICTFRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"CTF challenge analysis: {req.text}. Identify vulnerabilities, suggest tools and approach.",
        mode=req.mode or "sec", persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/diff-explain")
def ai_diff_explain(req: AIDiffExplainRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Explain this git diff in plain English:\n\n{req.diff}",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/summarize-url")
def ai_summarize_url(req: AISummarizeUrlRequest, user_id: str = Depends(_uid)):
    content = http_get(req.url)
    if not content:
        raise HTTPException(400, "Could not fetch URL.")
    snippet = content[:3000]
    result = ai_complete(
        f"Summarize this web page content:\n\n{snippet}",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/fix")
def ai_fix(req: AIFixRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Fix this error and explain what caused it:\n\n{req.error}",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/howto")
def ai_howto(req: AIHowtoRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"How to {req.task}? Give step-by-step instructions with exact commands.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/tldr")
def ai_tldr(req: AITldrRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"TL;DR for the command `{req.command}`: what does it do, common flags, examples.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/debug")
def ai_debug(req: AIDebugRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Debug this code. Find all bugs, explain each one, provide fixed version:\n\n```\n{req.code}\n```",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/review")
def ai_review(req: AIReviewRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Code review. Check for: bugs, security issues, performance, style, maintainability.\n\n```\n{req.code}\n```",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/template")
def ai_template(req: AITemplateRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Generate a project template for: {req.project_type}. Include folder structure, key files, and starter code.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/osint")
def ai_osint(req: AIOsintRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"OSINT guide for target: {req.target}. List passive recon tools, queries, and techniques.",
        mode=req.mode or "sec", persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/wordlist")
def ai_wordlist(req: AIWordlistRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Generate a targeted wordlist for: {req.info}. Include common patterns, variations, company-specific terms.",
        mode=req.mode or "sec", persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/think")
def ai_think(req: AIThinkRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Think through this step by step. Consider all angles, edge cases, and second-order effects:\n\n{req.question}",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/debate")
def ai_debate(req: AIDebateRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Debate both sides of: {req.topic}. Give strong arguments for and against. Conclude with your assessment.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/improve")
def ai_improve(req: AIImproveRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Improve this text — better clarity, flow, and impact. Show before/after:\n\n{req.text}",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/eli5")
def ai_eli5(req: AIEli5Request, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Explain {req.topic} like I'm 5 years old. Use simple words and fun analogies.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/cron")
def ai_cron(req: AICronRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Explain this cron expression: `{req.expression}`. When does it run? Give next 5 execution times.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/quiz")
def ai_quiz(req: AIQuizRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Create a 5-question multiple-choice quiz about {req.topic}. Include answers at the end.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/namebrainstorm")
def ai_namebrainstorm(req: AINameBrainstormRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Brainstorm 10 creative names for: {req.description}. Consider memorability, domain availability, and brand fit.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


@app.post("/api/ai/cheatsheet")
def ai_cheatsheet(req: AICheatsheetRequest, user_id: str = Depends(_uid)):
    result = ai_complete(
        f"Create a concise cheat sheet for {req.topic}. Use tables and code blocks. Cover the 20% of commands used 80% of the time.",
        mode=req.mode, persona=req.persona, user_id=user_id,
    )
    return {"result": result}


# ─────────────────────────────────────────────
#  ROUTES — TOOLS  (stateless — no user_id needed)
# ─────────────────────────────────────────────

@app.post("/api/tools/encode")
def tool_encode(req: ToolEncodeRequest):
    try:
        if req.decode:
            result = base64.b64decode(req.text.encode()).decode("utf-8", errors="replace")
        else:
            result = base64.b64encode(req.text.encode()).decode()
        return {"result": result, "operation": "decode" if req.decode else "encode"}
    except Exception as e:
        raise HTTPException(400, f"Encoding/decoding failed: {e}")


@app.post("/api/tools/hash")
def tool_hash(req: ToolHashRequest):
    text = req.hash.encode()
    return {
        "md5":    hashlib.md5(text).hexdigest(),
        "sha1":   hashlib.sha1(text).hexdigest(),
        "sha256": hashlib.sha256(text).hexdigest(),
        "sha512": hashlib.sha512(text).hexdigest(),
    }


@app.post("/api/tools/uuid")
def tool_uuid(req: ToolUUIDRequest):
    count = max(1, min(req.count, 50))
    return {"uuids": [str(_uuid.uuid4()) for _ in range(count)]}


@app.post("/api/tools/json")
def tool_json(req: ToolJSONRequest):
    try:
        parsed = json.loads(req.text)
        if req.minify:
            return {"result": json.dumps(parsed, separators=(",", ":")), "valid": True}
        return {"result": json.dumps(parsed, indent=2), "valid": True}
    except Exception as e:
        return {"valid": False, "error": str(e)}


@app.post("/api/tools/calc")
def tool_calc(req: ToolCalcRequest):
    try:
        result = safe_math_eval(req.expression)
        return {"expression": req.expression, "result": result}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/api/tools/pwcheck")
def tool_pwcheck(req: ToolPwCheckRequest):
    pw = req.password
    checks = {
        "length": len(pw) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", pw)),
        "lowercase": bool(re.search(r"[a-z]", pw)),
        "digits": bool(re.search(r"\d", pw)),
        "symbols": bool(re.search(r"[^a-zA-Z0-9]", pw)),
    }
    score = sum(checks.values())
    ratings = {5: "Strong 💪", 4: "Good 👍", 3: "Fair ⚠️", 2: "Weak ❌", 1: "Very Weak ❌", 0: "Terrible ❌"}
    return {"score": score, "rating": ratings.get(score, "Unknown"), "checks": checks}


@app.get("/api/tools/clock")
def tool_clock():
    now = datetime.datetime.utcnow()
    return {
        "utc": now.isoformat() + "Z",
        "unix": int(now.timestamp()),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
    }


@app.get("/api/tools/speedtest")
def tool_speedtest():
    urls = [
        "https://raw.githubusercontent.com/sindresorhus/github-markdown-css/main/github-markdown.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    ]
    results = []
    for url in urls:
        try:
            start = time.time()
            ctx = ssl.create_default_context()
            req = urllib.request.Request(url, headers={"User-Agent": "cybersh/1.5"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                size = len(r.read())
            elapsed = time.time() - start
            mbps = (size * 8) / (elapsed * 1_000_000)
            results.append({"url": url, "size_kb": round(size/1024, 1), "time_s": round(elapsed, 2), "mbps": round(mbps, 2)})
        except Exception:
            results.append({"url": url, "error": "Failed"})
    return {"results": results}


@app.get("/api/tools/ipinfo")
def tool_ipinfo(ip: str = Query(...)):
    data = http_get(f"https://ipinfo.io/{ip}/json")
    if not data:
        raise HTTPException(503, "IP info service unavailable.")
    try:
        return json.loads(data)
    except Exception:
        raise HTTPException(500, "Failed to parse IP info.")


@app.get("/api/tools/weather")
def tool_weather(city: str = Query(...)):
    data = http_get(f"https://wttr.in/{urllib.parse.quote(city)}?format=j1")
    if not data:
        raise HTTPException(503, "Weather service unavailable.")
    try:
        return json.loads(data)
    except Exception:
        raise HTTPException(500, "Failed to parse weather data.")


@app.get("/api/tools/syswatch")
def tool_syswatch():
    cpu_pct = ram_pct = ram_used_gb = ram_total_gb = disk_pct = disk_used_gb = disk_total_gb = 0.0
    try:
        with open("/proc/loadavg") as f:
            loadavg = float(f.read().split()[0])
        cpu_count = os.cpu_count() or 1
        cpu_pct = min(100.0, (loadavg / cpu_count) * 100)
    except Exception:
        pass
    try:
        with open("/proc/meminfo") as f:
            lines = {l.split(":")[0].strip(): int(l.split(":")[1].strip().split()[0]) for l in f if ":" in l}
        total = lines.get("MemTotal", 0)
        avail = lines.get("MemAvailable", 0)
        used = total - avail
        ram_pct = 100 * used / (total + 1)
        ram_used_gb = used / 1e6
        ram_total_gb = total / 1e6
    except Exception:
        pass
    try:
        s = os.statvfs("/")
        disk_total = s.f_blocks * s.f_frsize
        disk_used  = (s.f_blocks - s.f_bfree) * s.f_frsize
        disk_pct   = 100 * disk_used / (disk_total + 1)
        disk_used_gb  = disk_used / 1e9
        disk_total_gb = disk_total / 1e9
    except Exception:
        pass
    return {
        "cpu_percent": round(cpu_pct, 1),
        "ram": {"percent": round(ram_pct, 1), "used_gb": round(ram_used_gb, 1), "total_gb": round(ram_total_gb, 1)},
        "disk": {"percent": round(disk_pct, 1), "used_gb": round(disk_used_gb, 1), "total_gb": round(disk_total_gb, 1)},
        "timestamp": datetime.datetime.now().isoformat(),
    }


@app.get("/api/tools/timer/parse")
def tool_timer_parse(duration: str = Query(...)):
    arg = duration.strip().lower()
    try:
        if arg.endswith("h"):
            secs = int(arg[:-1]) * 3600
        elif arg.endswith("m"):
            secs = int(arg[:-1]) * 60
        elif arg.endswith("s"):
            secs = int(arg[:-1])
        else:
            secs = int(arg)
    except ValueError:
        raise HTTPException(400, "Invalid duration. Use 30s, 5m, or 1h.")
    return {"duration": duration, "total_seconds": secs}


@app.post("/api/tools/slugify")
def tool_slugify(text: str = Query(...)):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return {"slug": slug}


# ─────────────────────────────────────────────
#  API INFO
# ─────────────────────────────────────────────

@app.get("/api")
def api_info():
    return {
        "name": "Cyber-SH API",
        "version": "1.5",
        "docs": "/docs",
        "new_in_1_5": [
            "User data isolation — all data scoped per authenticated user",
            "30+ language support via /api/languages and ?lang= or X-Language header",
            "Extended settings via /api/settings/options",
            "Per-user chat history via /api/history",
            "AI adaptive learning — auto-extracts facts per user",
            "Removed /api/upgrade endpoint",
        ],
    }


# ─────────────────────────────────────────────
#  FRONTEND
# ─────────────────────────────────────────────
from fastapi.staticfiles import StaticFiles
if os.path.isdir("out"):
    app.mount("/", StaticFiles(directory="out", html=True), name="frontend")


# ─────────────────────────────────────────────
#  ENTRYPOINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cybersh_api:app", host="0.0.0.0", port=8000, reload=True)