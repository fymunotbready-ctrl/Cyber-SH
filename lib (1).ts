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
  { id: "agent", label: "Agent", desc: "AI controls your system", color: "#ffffff", Icon: Ic.agent },
  { id: "sec", label: "Sec", desc: "Security & pentesting", color: "#ffffff", Icon: Ic.sec },
  { id: "vibe", label: "Vibe", desc: "Creative coding & design", color: "#ffffff", Icon: Ic.vibe },
  { id: "code", label: "Code", desc: "Production-ready code", color: "#ffffff", Icon: Ic.code },
  { id: "chat", label: "Chat", desc: "General AI assistant", color: "#ffffff", Icon: Ic.chat },
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
  { Icon: Ic.offline, title: "100% Offline", body: "Runs entirely on your hardware. No API keys, no subscriptions, no data leaving your machine.", color: "#ffffff" },
  { Icon: Ic.agent, title: "Agent Mode", body: "I can execute terminal commands, create and edit files, open apps — with your permission.", color: "#ffffff" },
  { Icon: Ic.sec, title: "Security Suite", body: "CVE lookup, recon plans, payload generation, OSINT checklists, hash identification.", color: "#ffffff" },
  { Icon: Ic.memory, title: "Persistent Memory", body: "I remember your name, projects, and preferences across sessions using local JSON storage.", color: "#ffffff" },
  { Icon: Ic.web, title: "Web Tools", body: "/web, /weather, /summarize, /cvesearch — internet features that route directly to each service.", color: "#ffffff" },
  { Icon: Ic.vibe, title: "Vibe & Code Modes", body: "Generate beautiful UIs or clean production code. Switch modes any time with a single keystroke.", color: "#ffffff" },
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
  const res = await fetch(BASE_URL + path, {
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
    ...opts,
  })
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
    `Running in ${m?.label || "Chat"} mode. ` +
    `I received: "${last.slice(0, 80)}". ` +
    `This is a local simulation — connect a backend via NEXT_PUBLIC_CYBERSH_API to get live responses. ` +
    `Everything you see here stays on your device.`
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
