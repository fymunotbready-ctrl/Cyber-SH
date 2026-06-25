import type { CSSProperties } from "react"
import { Ic, type IconComponent } from "./icons"

export type Mode = {
  id: string
  label: string
  desc: string
  color: string
  Icon: IconComponent
}

export const MODES: Mode[] = [
  { id: "agent", label: "Agent", desc: "AI controls your system", color: "#5e5ce6", Icon: Ic.agent },
  { id: "sec", label: "Sec", desc: "Security & pentesting", color: "#30d158", Icon: Ic.sec },
  { id: "vibe", label: "Vibe", desc: "Creative coding & design", color: "#ff6961", Icon: Ic.vibe },
  { id: "code", label: "Code", desc: "Production-ready code", color: "#ffd60a", Icon: Ic.code },
  { id: "chat", label: "Chat", desc: "General AI assistant", color: "#00d4ff", Icon: Ic.chat },
]

export type Persona = { id: string; label: string; Icon: IconComponent }

export const PERSONALITIES: Persona[] = [
  { id: "default", label: "Default", Icon: Ic.cpu },
  { id: "teacher", label: "Teacher", Icon: Ic.book },
  { id: "hacker", label: "Hacker", Icon: Ic.unlock },
  { id: "coach", label: "Coach", Icon: Ic.bolt },
  { id: "roaster", label: "Roaster", Icon: Ic.flame },
  { id: "sherlock", label: "Sherlock", Icon: Ic.search },
  { id: "prof", label: "Prof", Icon: Ic.cap },
  { id: "eli5", label: "ELI5", Icon: Ic.face },
  { id: "pirate", label: "Pirate", Icon: Ic.flag },
  { id: "stoic", label: "Stoic", Icon: Ic.scale },
]

export const FEATURES: { Icon: IconComponent; title: string; body: string; color: string }[] = [
  {
    Icon: Ic.offline,
    title: "100% Offline",
    body: "Runs entirely on your hardware. No API keys, no subscriptions, no data leaving your machine.",
    color: "#30d158",
  },
  {
    Icon: Ic.agent,
    title: "Agent Mode",
    body: "I can execute terminal commands, create and edit files, open apps — with your permission.",
    color: "#5e5ce6",
  },
  {
    Icon: Ic.sec,
    title: "Security Suite",
    body: "CVE lookup, recon plans, payload generation, OSINT checklists, hash identification.",
    color: "#ff453a",
  },
  {
    Icon: Ic.memory,
    title: "Persistent Memory",
    body: "I remember your name, projects, and preferences across sessions using local JSON storage.",
    color: "#ffd60a",
  },
  {
    Icon: Ic.web,
    title: "Web Tools",
    body: "/web, /weather, /summarize, /cvesearch — internet features that route directly to each service.",
    color: "#00d4ff",
  },
  {
    Icon: Ic.vibe,
    title: "Vibe & Code Modes",
    body: "Generate beautiful UIs or clean production code. Switch modes any time with a single keystroke.",
    color: "#ff6961",
  },
]

/* ── Shared glass style tokens ── */
export const glass = (opacity = 0.06): CSSProperties => ({
  background: `rgba(var(--tint-rgb),${opacity})`,
  backdropFilter: "blur(24px) saturate(180%)",
  WebkitBackdropFilter: "blur(24px) saturate(180%)",
  border: "1px solid rgba(var(--tint-rgb),0.09)",
  boxShadow: "0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(var(--tint-rgb),0.07)",
})

export const liquidGlass = (tint = "0,212,255", size: "sm" | "md" | "lg" = "md"): CSSProperties => {
  const pad = size === "sm" ? "8px 22px" : size === "lg" ? "15px 36px" : "11px 26px"
  const fontSize = size === "lg" ? 15 : size === "sm" ? 13 : 14
  return {
    padding: pad,
    background: `linear-gradient(160deg,
      rgba(${tint},0.38) 0%,
      rgba(${tint},0.18) 35%,
      rgba(255,255,255,0.06) 65%,
      rgba(${tint},0.10) 100%)`,
    backdropFilter: "blur(28px) saturate(220%) brightness(1.08)",
    WebkitBackdropFilter: "blur(28px) saturate(220%) brightness(1.08)",
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

export const liquidGlassSm = (tint = "0,212,255"): CSSProperties => ({
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

/* ── Brand mark — crisp themeable hexagon glyph (no external asset) ── */
export function BrandLogo({ size = 28, glow = true }: { size?: number; glow?: boolean }) {
  return (
    <span
      style={{
        display: "inline-flex",
        color: "#00d4ff",
        filter: glow ? "drop-shadow(0 0 8px rgba(0,212,255,0.6))" : "none",
      }}
    >
      <Ic.logo s={size} c="#00d4ff" />
    </span>
  )
}
