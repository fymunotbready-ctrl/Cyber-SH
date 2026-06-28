import type { CSSProperties } from "react"
import { Ic } from "./icons"

// ─────────────────────────────────────────────
// Brand accent — monochrome (Apple-style white/gray)
// ─────────────────────────────────────────────
export const ACCENT_RGB = "255,255,255"
export const ACCENT_HEX = "#ffffff"
export const ACCENT_RGB_2 = "170,170,178" // soft gray (gradient pair)
export const ACCENT_HEX_2 = "#aaaab2"

// ─────────────────────────────────────────────
// Modes
// ─────────────────────────────────────────────
export const MODES = [
  { id: "agent", label: "Agent", desc: "Let the AI do tasks on your computer", color: "#ffffff", Icon: Ic.agent },
  { id: "sec", label: "Security", desc: "Check security and find weak spots", color: "#ffffff", Icon: Ic.sec },
  { id: "vibe", label: "Creative", desc: "Fun help with design and ideas", color: "#ffffff", Icon: Ic.vibe },
  { id: "code", label: "Code", desc: "Write clean, working code", color: "#ffffff", Icon: Ic.code },
  { id: "chat", label: "Chat", desc: "Just talk and ask anything", color: "#ffffff", Icon: Ic.chat },
] as const

export type ModeId = (typeof MODES)[number]["id"]

// ─────────────────────────────────────────────
// Personas — emojis replaced with SF-symbol-style icons
// ─────────────────────────────────────────────
export const PERSONALITIES = [
  { id: "default", label: "Default", Icon: Ic.robot },
  { id: "teacher", label: "Teacher", Icon: Ic.book },
  { id: "hacker", label: "Hacker", Icon: Ic.unlock },
  { id: "coach", label: "Coach", Icon: Ic.bolt },
  { id: "roaster", label: "Roaster", Icon: Ic.flame },
  { id: "sherlock", label: "Sherlock", Icon: Ic.search },
  { id: "prof", label: "Prof", Icon: Ic.cap },
  { id: "eli5", label: "ELI5", Icon: Ic.smiley },
  { id: "pirate", label: "Pirate", Icon: Ic.skull },
  { id: "stoic", label: "Stoic", Icon: Ic.scale },
] as const

export const FEATURES = [
  { Icon: Ic.offline, title: "Works Offline", body: "Runs fully on your own device. No sign-up, no fees, and nothing you say ever leaves your computer.", color: "#ffffff" },
  { Icon: Ic.agent, title: "Gets Things Done", body: "With your okay, it can run commands, create files, and open apps for you.", color: "#ffffff" },
  { Icon: Ic.sec, title: "Security Helper", body: "Find weak spots, check passwords, and get simple step-by-step safety tips.", color: "#ffffff" },
  { Icon: Ic.memory, title: "Remembers You", body: "It keeps your name, projects, and likes so you don't have to repeat yourself.", color: "#ffffff" },
  { Icon: Ic.web, title: "Handy Tools", body: "Built-in helpers for code, writing, and quick everyday tasks — all in one place.", color: "#ffffff" },
  { Icon: Ic.vibe, title: "Many Modes", body: "Switch between writing code, designing, or just chatting with one tap.", color: "#ffffff" },
]

// ─────────────────────────────────────────────
// Shared style tokens (liquid glass)
// ─────────────────────────────────────────────
export const glass = (opacity = 0.06): CSSProperties => ({
  background: `rgba(var(--tint-rgb),${opacity})`,
  backdropFilter: "blur(30px) saturate(190%) brightness(1.04)",
  WebkitBackdropFilter: "blur(30px) saturate(190%) brightness(1.04)",
  border: "1px solid rgba(var(--tint-rgb),0.09)",
  boxShadow: "0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(var(--tint-rgb),0.08)",
  transition: "transform 0.32s cubic-bezier(0.22,1,0.36,1), box-shadow 0.32s cubic-bezier(0.22,1,0.36,1), background 0.25s ease",
})

export const liquidGlass = (tint = ACCENT_RGB, size: "sm" | "md" | "lg" = "md"): CSSProperties => {
  const pad = size === "sm" ? "10px 24px" : size === "lg" ? "16px 38px" : "13px 28px"
  const fontSize = size === "lg" ? 15 : size === "sm" ? 13 : 14
  return {
    padding: pad,
    background: `linear-gradient(160deg,
      rgba(${tint},0.38) 0%,
      rgba(${tint},0.18) 35%,
      rgba(255,255,255,0.06) 65%,
      rgba(${tint},0.10) 100%)`,
    backdropFilter: "blur(32px) saturate(230%) brightness(1.08)",
    WebkitBackdropFilter: "blur(32px) saturate(230%) brightness(1.08)",
    border: "1px solid rgba(255,255,255,0.38)",
    borderTopColor: "rgba(255,255,255,0.72)",
    borderBottomColor: "rgba(0,0,0,0.22)",
    boxShadow: [
      "inset 0 2px 0 rgba(255,255,255,0.70)",
      "inset 1.5px 0 0 rgba(255,255,255,0.22)",
      "inset -1.5px 0 0 rgba(255,255,255,0.10)",
      `inset 0 0 20px rgba(${tint},0.12)`,
      "inset 0 -2px 6px rgba(0,0,0,0.20)",
      `0 6px 28px rgba(${tint},0.30)`,
      "0 2px 12px rgba(0,0,0,0.40)",
      `0 0 0 0.5px rgba(${tint},0.20)`,
    ].join(","),
    color: "#fff",
    cursor: "pointer",
    borderRadius: size === "sm" ? 20 : 16,
    fontSize,
    fontWeight: 600,
    letterSpacing: "0.01em",
    transition: "all 0.22s cubic-bezier(0.34,1.56,0.64,1)",
    position: "relative",
    overflow: "hidden",
    textShadow: "0 1px 2px rgba(0,0,0,0.30)",
  }
}

export const liquidGlassSm = (tint = ACCENT_RGB): CSSProperties => ({
  ...liquidGlass(tint, "sm"),
  borderRadius: 22,
  fontSize: 13,
})

export const glassModal: CSSProperties = {
  background: "var(--panel-bg)",
  backdropFilter: "blur(40px) saturate(200%)",
  WebkitBackdropFilter: "blur(40px) saturate(200%)",
  border: "1px solid rgba(var(--tint-rgb),0.1)",
  boxShadow: "0 24px 80px rgba(0,0,0,0.75), inset 0 1px 0 rgba(var(--tint-rgb),0.08)",
}

// ─────────────────────────────────────────────
// API layer — points at your backend; falls back to a
// local simulation so the UI is fully functional in preview.
// Set NEXT_PUBLIC_CYBERSH_API to wire a real backend later.
// ─────────────────────────────────────────────
export const BASE_URL =
  (typeof process !== "undefined" && process.env.NEXT_PUBLIC_CYBERSH_API) || ""

export async function apiFetch(path: string, opts: RequestInit = {}) {
  if (!BASE_URL) throw new Error("offline")
  const token = typeof window !== "undefined" ? localStorage.getItem("cybersh_access_token") : null
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string, string> || {}),
  }
  if (token) headers["Authorization"] = `Bearer ${token}`

  const res = await fetch(BASE_URL + path, { ...opts, headers })

  if (res.status === 401) {
    // Token missing/expired — drop it and surface a clear, catchable error
    // so calling components can prompt the user to log in again.
    if (typeof window !== "undefined") localStorage.removeItem("cybersh_access_token")
    throw new Error("Please log in to use this feature.")
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error((err as { detail?: string }).detail || `HTTP ${res.status}`)
  }
  return res
}

type ChatMsg = { role: string; content: string }

const PERSONA_VOICE: Record<string, (t: string) => string> = {
  default: (t) => t,
  teacher: (t) => `Let's break this down step by step. ${t}`,
  hacker: (t) => `[root@cybersh]# ${t}`,
  coach: (t) => `You've got this. ${t}`,
  roaster: (t) => `Bold question. Anyway — ${t}`,
  sherlock: (t) => `Observe the details: ${t}`,
  prof: (t) => `Academically speaking, ${t}`,
  eli5: (t) => `Imagine it like this: ${t}`,
  pirate: (t) => `Arr, here be the answer: ${t}`,
  stoic: (t) => `Focus on what you control. ${t}`,
}

function mockReply(messages: ChatMsg[], mode: string, persona: string) {
  const last = messages[messages.length - 1]?.content || ""
  const m = MODES.find((x) => x.id === mode)
  const core =
    `You're in ${m?.label || "Chat"} mode. ` +
    `You said: "${last.slice(0, 80)}". ` +
    `This is a demo reply. Connect your own AI to get real answers. ` +
    `Don't worry — everything you type stays on your device.`
  return (PERSONA_VOICE[persona] || PERSONA_VOICE.default)(core)
}

export async function streamChat(
  messages: ChatMsg[],
  mode: string,
  persona: string,
  onToken: (t: string) => void,
  onDone: () => void,
  onError: (e: string) => void,
) {
  // Try the real backend first.
  if (BASE_URL) {
    try {
      const res = await apiFetch("/api/chat", {
        method: "POST",
        body: JSON.stringify({ messages, mode, persona, stream: true, use_memory: true }),
      })
      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let buf = ""
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const lines = buf.split("\n")
        buf = lines.pop() || ""
        for (const line of lines) {
          if (!line.startsWith("data: ")) continue
          const data = line.slice(6).trim()
          if (data === "[DONE]") {
            onDone()
            return
          }
          try {
            const j = JSON.parse(data)
            if (j.token) onToken(j.token)
            if (j.error) {
              onError(j.error)
              return
            }
          } catch {}
        }
      }
      onDone()
      return
    } catch {
      // fall through to local simulation
    }
  }

  // Local simulated stream.
  const reply = mockReply(messages, mode, persona)
  const words = reply.split(" ")
  let i = 0
  const tick = () => {
    if (i >= words.length) {
      onDone()
      return
    }
    onToken((i === 0 ? "" : " ") + words[i])
    i++
    setTimeout(tick, 28 + Math.random() * 40)
  }
  setTimeout(tick, 250)
}

// ─────────────────────────────────────────────
// Chat history — saved locally on your device (no server)
// ─────────────────────────────────────────────
export type StoredMsg = { id: number; role: "user" | "ai"; text: string; mode: string }
export type ChatSession = { id: string; title: string; updatedAt: number; messages: StoredMsg[] }

const HISTORY_KEY = "cybersh_chat_history"

export function loadHistory(): ChatSession[] {
  if (typeof window === "undefined") return []
  try {
    const raw = localStorage.getItem(HISTORY_KEY)
    if (!raw) return []
    const list = JSON.parse(raw) as ChatSession[]
    return Array.isArray(list) ? list.sort((a, b) => b.updatedAt - a.updatedAt) : []
  } catch {
    return []
  }
}

export function saveHistory(sessions: ChatSession[]) {
  if (typeof window === "undefined") return
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(sessions.slice(0, 50)))
  } catch {}
}

export function titleFromMessages(messages: StoredMsg[]): string {
  const firstUser = messages.find((m) => m.role === "user")
  const base = (firstUser?.text || "New chat").trim().replace(/\s+/g, " ")
  return base.length > 40 ? base.slice(0, 40) + "…" : base
}
