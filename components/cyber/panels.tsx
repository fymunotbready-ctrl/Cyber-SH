"use client"

import { useEffect, useState } from "react"
import { Ic, type IconComponent } from "./icons"
import { liquidGlass } from "./data"
import { apiFetch } from "./api"
import { PanelModal, SettingRow, Toggle } from "./ui"

/* ── Profile ── */
export function ProfilePanel({ user, onClose }: { user: { name: string }; onClose: () => void }) {
  const [name, setName] = useState(user.name)
  const [saved, setSaved] = useState(false)
  const save = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }
  const inputStyle = {
    width: "100%",
    marginTop: 8,
    padding: "10px 14px",
    borderRadius: 10,
    background: "rgba(var(--tint-rgb),0.06)",
    border: "1px solid rgba(var(--tint-rgb),0.1)",
    color: "var(--text-color)",
    fontSize: 14,
    outline: "none",
  } as const
  const labelStyle = {
    fontSize: 12,
    color: "rgba(var(--tint-rgb),0.4)",
    fontWeight: 600,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
  } as const
  return (
    <PanelModal title="Profile" icon={<Ic.person s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: 24 }}>
        <div
          style={{
            width: 72,
            height: 72,
            borderRadius: "50%",
            background: "linear-gradient(135deg,#00d4ff,#7b5eff)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 28,
            fontWeight: 700,
            color: "#fff",
            boxShadow: "0 0 24px rgba(0,212,255,0.3)",
            marginBottom: 12,
          }}
        >
          {name[0]?.toUpperCase()}
        </div>
        <div style={{ fontSize: 13, color: "rgba(var(--tint-rgb),0.4)" }}>cybersh.ai</div>
      </div>
      <div style={{ marginBottom: 14 }}>
        <label style={labelStyle}>Display Name</label>
        <input value={name} onChange={(e) => setName(e.target.value)} style={inputStyle} />
      </div>
      <div style={{ marginBottom: 20 }}>
        <label style={labelStyle}>Version</label>
        <div
          style={{
            marginTop: 8,
            padding: "10px 14px",
            borderRadius: 10,
            background: "rgba(var(--tint-rgb),0.04)",
            border: "1px solid rgba(var(--tint-rgb),0.07)",
            fontSize: 13,
            color: "rgba(var(--tint-rgb),0.5)",
          }}
        >
          Cyber-SH v1.4 — Offline Build
        </div>
      </div>
      <button
        onClick={save}
        className="lg-btn"
        style={{
          ...liquidGlass(saved ? "48,209,88" : "0,212,255", "md"),
          width: "100%",
          borderRadius: 12,
          color: saved ? "#30d158" : "#fff",
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 7,
        }}
      >
        {saved && <Ic.check s={15} c="#30d158" />}
        {saved ? "Saved" : "Save Changes"}
      </button>
    </PanelModal>
  )
}

/* ── Settings ── */
export function SettingsPanel({ onClose }: { onClose: () => void }) {
  const [s, setS] = useState({
    sound: true,
    autoScroll: true,
    sendOnEnter: true,
    timestamps: false,
    compactMode: false,
    telemetry: false,
  })
  const toggle = (k: keyof typeof s) => setS((p) => ({ ...p, [k]: !p[k] }))
  return (
    <PanelModal title="Settings" icon={<Ic.settings s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      <SettingRow label="Sound effects" desc="Play sounds on send/receive">
        <Toggle on={s.sound} onToggle={() => toggle("sound")} />
      </SettingRow>
      <SettingRow label="Auto-scroll" desc="Jump to latest message automatically">
        <Toggle on={s.autoScroll} onToggle={() => toggle("autoScroll")} />
      </SettingRow>
      <SettingRow label="Send on Enter" desc="Press Enter to send, Shift+Enter for newline">
        <Toggle on={s.sendOnEnter} onToggle={() => toggle("sendOnEnter")} />
      </SettingRow>
      <SettingRow label="Show timestamps" desc="Display time on each message">
        <Toggle on={s.timestamps} onToggle={() => toggle("timestamps")} />
      </SettingRow>
      <SettingRow label="Compact mode" desc="Reduce spacing between messages">
        <Toggle on={s.compactMode} onToggle={() => toggle("compactMode")} />
      </SettingRow>
      <SettingRow label="Usage telemetry" desc="Anonymous crash & usage data">
        <Toggle on={s.telemetry} onToggle={() => toggle("telemetry")} color="#ff453a" />
      </SettingRow>
      <div
        style={{
          marginTop: 20,
          padding: "12px 14px",
          borderRadius: 10,
          background: "rgba(48,209,88,0.06)",
          border: "1px solid rgba(48,209,88,0.15)",
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <Ic.lock s={14} c="#30d158" />
        <div style={{ fontSize: 12, color: "#30d158", fontWeight: 500 }}>
          All data stays on your device. Zero network calls.
        </div>
      </div>
    </PanelModal>
  )
}

/* ── Theme ── */
export function ThemePanel({
  onClose,
  mode,
  setMode,
}: {
  onClose: () => void
  mode: "dark" | "light"
  setMode: (m: "dark" | "light") => void
}) {
  const themes = [
    { id: "cyan", label: "Cyber Cyan", primary: "#00d4ff", secondary: "#0090d4" },
    { id: "purple", label: "Neon Purple", primary: "#7b5eff", secondary: "#5e3ed4" },
    { id: "green", label: "Matrix Green", primary: "#30d158", secondary: "#20a040" },
    { id: "orange", label: "Flame", primary: "#ff9f0a", secondary: "#cc7000" },
    { id: "pink", label: "Synthwave", primary: "#ff375f", secondary: "#cc1040" },
    { id: "white", label: "Ghost", primary: "rgba(var(--text-rgb),0.9)", secondary: "rgba(200,200,220,0.7)" },
  ]
  const [active, setActive] = useState("cyan")
  const appearances: { id: "dark" | "light"; label: string; Icon: IconComponent }[] = [
    { id: "dark", label: "Dark", Icon: Ic.moon },
    { id: "light", label: "Light", Icon: Ic.sun },
  ]
  return (
    <PanelModal title="Theme" icon={<Ic.theme s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      <div
        style={{
          fontSize: 12,
          fontWeight: 600,
          color: "rgba(var(--tint-rgb),0.45)",
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          marginBottom: 10,
        }}
      >
        Appearance
      </div>
      <div
        style={{
          display: "flex",
          gap: 6,
          padding: 5,
          borderRadius: 14,
          marginBottom: 22,
          background: "rgba(var(--tint-rgb),0.05)",
          border: "1px solid rgba(var(--tint-rgb),0.08)",
        }}
      >
        {appearances.map((a) => (
          <button
            key={a.id}
            onClick={() => setMode(a.id)}
            style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 7,
              padding: "10px 0",
              borderRadius: 10,
              border: "none",
              cursor: "pointer",
              background: mode === a.id ? "rgba(var(--tint-rgb),0.12)" : "transparent",
              boxShadow: mode === a.id ? "inset 0 0 0 1px rgba(var(--tint-rgb),0.12)" : "none",
              color: mode === a.id ? "var(--text-color)" : "rgba(var(--tint-rgb),0.45)",
              fontSize: 13,
              fontWeight: 600,
              transition: "all 0.2s",
            }}
          >
            <a.Icon s={15} c={mode === a.id ? "var(--text-color)" : "rgba(var(--tint-rgb),0.45)"} />
            {a.label}
          </button>
        ))}
      </div>
      <p style={{ fontSize: 13, color: "rgba(var(--tint-rgb),0.4)", marginBottom: 18 }}>Choose your accent color.</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        {themes.map((t) => (
          <button
            key={t.id}
            onClick={() => setActive(t.id)}
            style={{
              padding: "14px 16px",
              borderRadius: 14,
              cursor: "pointer",
              background: active === t.id ? `${t.primary}18` : "rgba(var(--tint-rgb),0.04)",
              border: active === t.id ? `1.5px solid ${t.primary}60` : "1.5px solid rgba(var(--tint-rgb),0.07)",
              display: "flex",
              alignItems: "center",
              gap: 10,
              transition: "all 0.2s",
            }}
          >
            <div
              style={{
                width: 22,
                height: 22,
                borderRadius: "50%",
                flexShrink: 0,
                background: `linear-gradient(135deg,${t.primary},${t.secondary})`,
                boxShadow: active === t.id ? `0 0 10px ${t.primary}66` : "none",
              }}
            />
            <span style={{ fontSize: 13, fontWeight: 500, color: active === t.id ? t.primary : "rgba(var(--text-rgb),0.65)" }}>
              {t.label}
            </span>
          </button>
        ))}
      </div>
      <button
        onClick={onClose}
        className="lg-btn"
        style={{ ...liquidGlass("0,212,255", "md"), width: "100%", marginTop: 20, borderRadius: 12 }}
      >
        Apply Theme
      </button>
    </PanelModal>
  )
}

/* ── Upgrade ── */
export function UpgradePanel({ onClose }: { onClose: () => void }) {
  const plans = [
    { name: "Free", price: "$0", color: "rgba(var(--tint-rgb),0.5)", features: ["5 modes", "Local models only", "Basic memory"] },
    {
      name: "Pro",
      price: "$9",
      color: "#00d4ff",
      features: ["All 5 modes", "Priority model updates", "Persistent memory", "Web tools"],
      popular: true,
    },
    {
      name: "Elite",
      price: "$19",
      color: "#7b5eff",
      features: ["Everything in Pro", "Multi-agent workflows", "Custom model import", "API access"],
    },
  ]
  return (
    <PanelModal title="Upgrade" icon={<Ic.upgrade s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      <p style={{ fontSize: 13, color: "rgba(var(--tint-rgb),0.4)", marginBottom: 18 }}>
        All tiers run fully offline. Cloud is never required.
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {plans.map((p) => (
          <div
            key={p.name}
            style={{
              padding: "16px 18px",
              borderRadius: 14,
              background: p.popular ? `${p.color}10` : "rgba(var(--tint-rgb),0.03)",
              border: p.popular ? `1.5px solid ${p.color}44` : "1.5px solid rgba(var(--tint-rgb),0.07)",
              position: "relative",
            }}
          >
            {p.popular && (
              <div
                style={{
                  position: "absolute",
                  top: -10,
                  right: 16,
                  padding: "2px 10px",
                  borderRadius: 20,
                  fontSize: 10,
                  fontWeight: 700,
                  background: p.color,
                  color: "#000",
                  letterSpacing: "0.06em",
                }}
              >
                POPULAR
              </div>
            )}
            <div style={{ display: "flex", alignItems: "baseline", gap: 6, marginBottom: 10 }}>
              <span style={{ fontSize: 18, fontWeight: 700, color: p.color }}>{p.name}</span>
              <span style={{ fontSize: 22, fontWeight: 700, color: "var(--text-color)" }}>{p.price}</span>
              <span style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.3)" }}>/mo</span>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
              {p.features.map((f) => (
                <div
                  key={f}
                  style={{ fontSize: 13, color: "rgba(var(--text-rgb),0.6)", display: "flex", alignItems: "center", gap: 7 }}
                >
                  <Ic.check s={12} c={p.color} /> {f}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </PanelModal>
  )
}

/* ── Keyboard shortcuts ── */
export function ShortcutsPanel({ onClose }: { onClose: () => void }) {
  const groups = [
    {
      label: "Chat",
      shortcuts: [
        { keys: ["Enter"], desc: "Send message" },
        { keys: ["Shift", "Enter"], desc: "New line" },
        { keys: ["Ctrl", "K"], desc: "New conversation" },
        { keys: ["Ctrl", "L"], desc: "Clear chat" },
      ],
    },
    {
      label: "Modes",
      shortcuts: [
        { keys: ["Ctrl", "1"], desc: "Agent mode" },
        { keys: ["Ctrl", "2"], desc: "Sec mode" },
        { keys: ["Ctrl", "3"], desc: "Vibe mode" },
        { keys: ["Ctrl", "4"], desc: "Code mode" },
        { keys: ["Ctrl", "5"], desc: "Chat mode" },
      ],
    },
    {
      label: "App",
      shortcuts: [
        { keys: ["Ctrl", ","], desc: "Open settings" },
        { keys: ["Ctrl", "\\"], desc: "Toggle sidebar" },
        { keys: ["Escape"], desc: "Close panel" },
      ],
    },
  ]
  return (
    <PanelModal title="Keyboard Shortcuts" icon={<Ic.keyboard s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      {groups.map((g) => (
        <div key={g.label} style={{ marginBottom: 20 }}>
          <div
            style={{
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
              color: "rgba(var(--tint-rgb),0.3)",
              marginBottom: 10,
            }}
          >
            {g.label}
          </div>
          {g.shortcuts.map((sc) => (
            <div
              key={sc.desc}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "9px 0",
                borderBottom: "1px solid rgba(var(--tint-rgb),0.04)",
              }}
            >
              <span style={{ fontSize: 13, color: "rgba(var(--text-rgb),0.65)" }}>{sc.desc}</span>
              <div style={{ display: "flex", gap: 4 }}>
                {sc.keys.map((k) => (
                  <kbd
                    key={k}
                    style={{
                      padding: "3px 8px",
                      borderRadius: 6,
                      fontSize: 11,
                      fontWeight: 600,
                      background: "rgba(var(--tint-rgb),0.08)",
                      color: "rgba(var(--text-rgb),0.8)",
                      border: "1px solid rgba(var(--tint-rgb),0.12)",
                    }}
                  >
                    {k}
                  </kbd>
                ))}
              </div>
            </div>
          ))}
        </div>
      ))}
    </PanelModal>
  )
}

/* ── Help ── */
export function HelpPanel({ onClose }: { onClose: () => void }) {
  const [open, setOpen] = useState<number | null>(null)
  const faqs = [
    { q: "How do I run Cyber-SH offline?", a: "After the first setup, Cyber-SH runs 100% on your device. No internet connection needed. All model weights are stored locally." },
    { q: "What are the different modes?", a: "Agent: executes system commands. Sec: security & pentesting tools. Vibe: creative UI/design help. Code: production-ready code. Chat: general assistant." },
    { q: "How does persistent memory work?", a: "Cyber-SH saves your name, project context and preferences to a local JSON file. Nothing is ever sent to a server." },
    { q: "Can I import custom models?", a: "Yes on the Elite plan. Drop any GGUF-format model into the /models directory and restart the app to use it." },
    { q: "How do I report a bug?", a: "Open an issue on the GitHub repo or use the feedback command inside any chat: just type /feedback followed by your report." },
  ]
  return (
    <PanelModal title="Help Center" icon={<Ic.help s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      <div
        style={{
          marginBottom: 16,
          padding: "12px 14px",
          borderRadius: 10,
          background: "rgba(0,212,255,0.06)",
          border: "1px solid rgba(0,212,255,0.15)",
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <Ic.chat s={14} c="rgba(0,212,255,0.9)" />
        <div style={{ fontSize: 13, color: "rgba(0,212,255,0.9)", fontWeight: 500 }}>
          Type /help inside any chat for in-line assistance
        </div>
      </div>
      {faqs.map((f, i) => (
        <div key={i} style={{ borderBottom: "1px solid rgba(var(--tint-rgb),0.05)" }}>
          <button
            onClick={() => setOpen(open === i ? null : i)}
            style={{
              width: "100%",
              padding: "13px 0",
              background: "none",
              border: "none",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              color: "rgba(var(--text-rgb),0.85)",
              textAlign: "left",
            }}
          >
            <span style={{ fontSize: 13, fontWeight: 500, paddingRight: 12 }}>{f.q}</span>
            <span style={{ transform: open === i ? "rotate(90deg)" : "none", transition: "transform 0.2s", display: "inline-flex" }}>
              <Ic.chevR s={14} c="rgba(var(--tint-rgb),0.3)" />
            </span>
          </button>
          {open === i && (
            <div
              style={{
                padding: "0 0 14px",
                fontSize: 13,
                lineHeight: 1.65,
                color: "rgba(var(--text-rgb),0.5)",
                animation: "cyberFadeIn 0.2s ease",
              }}
            >
              {f.a}
            </div>
          )}
        </div>
      ))}
    </PanelModal>
  )
}

/* ── Tools ── */
type Tool = { id: string; Icon: IconComponent; label: string; placeholder: string; action: (v: string) => void }

export function ToolsPanel({
  onClose,
}: {
  onClose: () => void
  onSendCommand?: (cmd: string) => void
}) {
  const [toolInput, setToolInput] = useState<Record<string, string>>({})
  const [toolResult, setToolResult] = useState<Record<string, string>>({})
  const [toolLoading, setToolLoading] = useState<Record<string, boolean>>({})

  const runTool = async (id: string, endpoint: string, body: object, method: "GET" | "POST" = "POST") => {
    setToolLoading((p) => ({ ...p, [id]: true }))
    setToolResult((p) => ({ ...p, [id]: "" }))
    try {
      const res = await apiFetch(endpoint, method === "GET" ? {} : { method: "POST", body: JSON.stringify(body) })
      const data = await res.json()
      setToolResult((p) => ({ ...p, [id]: JSON.stringify(data, null, 2) }))
    } catch (e) {
      setToolResult((p) => ({ ...p, [id]: `Error: ${e instanceof Error ? e.message : String(e)}` }))
    }
    setToolLoading((p) => ({ ...p, [id]: false }))
  }

  const aiTools: Tool[] = [
    { id: "explain", Icon: Ic.search, label: "Explain Code", placeholder: "Paste code here…", action: (v) => runTool("explain", "/api/ai/explain-code", { text: v }) },
    { id: "roast", Icon: Ic.flame, label: "Roast Code", placeholder: "Paste code here…", action: (v) => runTool("roast", "/api/ai/roast", { text: v }) },
    { id: "debug", Icon: Ic.bug, label: "Debug Code", placeholder: "Paste buggy code…", action: (v) => runTool("debug", "/api/ai/debug", { code: v }) },
    { id: "review", Icon: Ic.clipboard, label: "Review Code", placeholder: "Paste code…", action: (v) => runTool("review", "/api/ai/review", { code: v }) },
    { id: "improve", Icon: Ic.sparkles, label: "Improve Text", placeholder: "Enter text…", action: (v) => runTool("improve", "/api/ai/improve", { text: v }) },
    { id: "eli5", Icon: Ic.face, label: "ELI5", placeholder: "Topic to explain…", action: (v) => runTool("eli5", "/api/ai/eli5", { topic: v }) },
    { id: "osint", Icon: Ic.search, label: "OSINT Checklist", placeholder: "Target (domain/user/email)…", action: (v) => runTool("osint", "/api/ai/osint", { target: v }) },
    { id: "regex", Icon: Ic.bolt, label: "Generate Regex", placeholder: "Describe pattern…", action: (v) => runTool("regex", "/api/ai/regex", { description: v }) },
    { id: "cron", Icon: Ic.clock, label: "Cron Helper", placeholder: "e.g. every day at 3am…", action: (v) => runTool("cron", "/api/ai/cron", { expression: v }) },
    { id: "wordlist", Icon: Ic.list, label: "Wordlist Gen", placeholder: "Target info (name, DOB…)…", action: (v) => runTool("wordlist", "/api/ai/wordlist", { info: v }) },
    { id: "think", Icon: Ic.brain, label: "Deep Think", placeholder: "Complex question…", action: (v) => runTool("think", "/api/ai/think", { question: v }) },
    { id: "debate", Icon: Ic.scale, label: "Debate", placeholder: "Topic to debate…", action: (v) => runTool("debate", "/api/ai/debate", { topic: v }) },
  ]

  const utilTools: Tool[] = [
    { id: "hash", Icon: Ic.key, label: "Hash Identify", placeholder: "Paste a hash…", action: (v) => runTool("hash", "/api/tools/hash", { hash: v }) },
    { id: "pwcheck", Icon: Ic.lock, label: "Password Check", placeholder: "Enter password…", action: (v) => runTool("pwcheck", "/api/tools/pwcheck", { password: v }) },
    { id: "encode", Icon: Ic.box, label: "Encode/Decode", placeholder: "Text to encode…", action: (v) => runTool("encode", "/api/tools/encode", { text: v }) },
    { id: "calc", Icon: Ic.calc, label: "Calculator", placeholder: "e.g. 2**10 or 15% of 200", action: (v) => runTool("calc", "/api/tools/calc", { expression: v }) },
    { id: "ipinfo", Icon: Ic.web, label: "IP Info", placeholder: "IP address or blank for yours…", action: (v) => runTool("ipinfo", `/api/tools/ipinfo?ip=${encodeURIComponent(v)}`, {}, "GET") },
    { id: "passgen", Icon: Ic.dice, label: "Password Gen", placeholder: "Type: password/phrase/token", action: (v) => runTool("passgen", `/api/tools/passgen?kind=${encodeURIComponent(v || "password")}`, {}, "GET") },
    { id: "uuid", Icon: Ic.id, label: "UUID Gen", placeholder: "(leave blank for 1)", action: (v) => runTool("uuid", "/api/tools/uuid", { count: Number.parseInt(v) || 1 }) },
    { id: "slugify", Icon: Ic.type, label: "Slugify", placeholder: "Text to slugify…", action: (v) => runTool("slugify", `/api/tools/slugify?text=${encodeURIComponent(v)}`, {}, "GET") },
  ]

  const [activeTab, setActiveTab] = useState<"ai" | "util">("ai")
  const tools = activeTab === "ai" ? aiTools : utilTools
  const tabs: { id: "ai" | "util"; label: string; Icon: IconComponent }[] = [
    { id: "ai", label: "AI Tools", Icon: Ic.cpu },
    { id: "util", label: "Utilities", Icon: Ic.wrench },
  ]

  return (
    <PanelModal title="Tools" icon={<Ic.wrench s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      <div style={{ display: "flex", gap: 4, marginBottom: 18, padding: 3, borderRadius: 10, background: "rgba(var(--tint-rgb),0.05)" }}>
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 6,
              padding: "7px 0",
              borderRadius: 8,
              border: "none",
              cursor: "pointer",
              background: activeTab === t.id ? "rgba(0,212,255,0.18)" : "transparent",
              color: activeTab === t.id ? "#00d4ff" : "rgba(var(--text-rgb),0.5)",
              fontSize: 13,
              fontWeight: activeTab === t.id ? 600 : 400,
              transition: "all 0.2s",
            }}
          >
            <t.Icon s={14} c={activeTab === t.id ? "#00d4ff" : "rgba(var(--text-rgb),0.5)"} />
            {t.label}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10, maxHeight: 420, overflowY: "auto" }}>
        {tools.map((t) => (
          <div
            key={t.id}
            style={{
              padding: "12px 14px",
              borderRadius: 12,
              background: "rgba(var(--tint-rgb),0.03)",
              border: "1px solid rgba(var(--tint-rgb),0.07)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 7, marginBottom: 8 }}>
              <t.Icon s={16} c="rgba(0,212,255,0.85)" />
              <span style={{ fontSize: 13, fontWeight: 600, color: "rgba(var(--text-rgb),0.8)" }}>{t.label}</span>
            </div>
            <div style={{ display: "flex", gap: 7 }}>
              <input
                value={toolInput[t.id] || ""}
                onChange={(e) => setToolInput((p) => ({ ...p, [t.id]: e.target.value }))}
                placeholder={t.placeholder}
                onKeyDown={(e) => e.key === "Enter" && t.action(toolInput[t.id] || "")}
                style={{
                  flex: 1,
                  padding: "7px 11px",
                  borderRadius: 8,
                  fontSize: 12,
                  background: "rgba(var(--tint-rgb),0.05)",
                  border: "1px solid rgba(var(--tint-rgb),0.09)",
                  color: "var(--text-color)",
                  outline: "none",
                }}
              />
              <button
                onClick={() => t.action(toolInput[t.id] || "")}
                disabled={toolLoading[t.id]}
                style={{
                  padding: "7px 14px",
                  borderRadius: 8,
                  border: "none",
                  cursor: "pointer",
                  background: `rgba(0,212,255,${toolLoading[t.id] ? "0.1" : "0.2"})`,
                  color: toolLoading[t.id] ? "rgba(var(--tint-rgb),0.3)" : "#00d4ff",
                  fontSize: 12,
                  fontWeight: 600,
                  flexShrink: 0,
                  transition: "all 0.2s",
                }}
              >
                {toolLoading[t.id] ? "…" : "Run"}
              </button>
            </div>
            {toolResult[t.id] && (
              <pre
                style={{
                  marginTop: 8,
                  padding: "9px 11px",
                  borderRadius: 8,
                  fontSize: 11,
                  lineHeight: 1.5,
                  background: "rgba(0,0,0,0.3)",
                  border: "1px solid rgba(var(--tint-rgb),0.06)",
                  color: "rgba(var(--text-rgb),0.7)",
                  overflowX: "auto",
                  whiteSpace: "pre-wrap",
                  maxHeight: 160,
                  overflowY: "auto",
                }}
              >
                {toolResult[t.id]}
              </pre>
            )}
          </div>
        ))}
      </div>
    </PanelModal>
  )
}

/* ── Memory ── */
type MemoryData = { facts?: string[]; preferences?: Record<string, string>; projects?: Record<string, string> }

export function MemoryPanel({ onClose }: { onClose: () => void }) {
  const [mem, setMem] = useState<MemoryData | null>(null)
  const [newFact, setNewFact] = useState("")
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    apiFetch("/api/memory")
      .then((r) => r.json())
      .then((d) => {
        setMem(d)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const addFact = async () => {
    if (!newFact.trim()) return
    setSaving(true)
    try {
      await apiFetch("/api/memory", { method: "POST", body: JSON.stringify({ text: newFact.trim() }) })
      apiFetch("/api/memory")
        .then((r) => r.json())
        .then(setMem)
      setNewFact("")
    } catch {
      /* offline */
    }
    setSaving(false)
  }

  const clearAll = async () => {
    if (!confirm("Clear all memory?")) return
    await apiFetch("/api/memory/all", { method: "DELETE" }).catch(() => {})
    setMem({ facts: [], preferences: {}, projects: {} })
  }

  const sectionTitle = {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "rgba(var(--tint-rgb),0.3)",
    marginBottom: 8,
  } as const

  return (
    <PanelModal title="Memory" icon={<Ic.brain s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      {loading ? (
        <div style={{ textAlign: "center", padding: 30, color: "rgba(var(--tint-rgb),0.3)" }}>Loading…</div>
      ) : !mem ? (
        <div style={{ textAlign: "center", padding: 30, color: "#ff453a" }}>Could not reach backend.</div>
      ) : (
        <>
          <div style={{ display: "flex", gap: 7, marginBottom: 18 }}>
            <input
              value={newFact}
              onChange={(e) => setNewFact(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addFact()}
              placeholder="Add a fact, key=value pref, or 'project name info'…"
              style={{
                flex: 1,
                padding: "9px 12px",
                borderRadius: 9,
                fontSize: 13,
                background: "rgba(var(--tint-rgb),0.05)",
                border: "1px solid rgba(var(--tint-rgb),0.09)",
                color: "var(--text-color)",
                outline: "none",
              }}
            />
            <button
              onClick={addFact}
              disabled={saving}
              style={{
                padding: "9px 16px",
                borderRadius: 9,
                border: "none",
                cursor: "pointer",
                background: "rgba(0,212,255,0.18)",
                color: "#00d4ff",
                fontSize: 13,
                fontWeight: 600,
              }}
            >
              {saving ? "…" : "Add"}
            </button>
          </div>

          {mem.facts && mem.facts.length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div style={sectionTitle}>Facts</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 5, maxHeight: 140, overflowY: "auto" }}>
                {[...mem.facts].reverse().map((f, i) => (
                  <div
                    key={i}
                    style={{
                      padding: "7px 11px",
                      borderRadius: 8,
                      fontSize: 12,
                      background: "rgba(var(--tint-rgb),0.04)",
                      border: "1px solid rgba(var(--tint-rgb),0.06)",
                      color: "rgba(var(--text-rgb),0.65)",
                      lineHeight: 1.4,
                    }}
                  >
                    {f}
                  </div>
                ))}
              </div>
            </div>
          )}

          {mem.preferences && Object.keys(mem.preferences).length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div style={sectionTitle}>Preferences</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {Object.entries(mem.preferences).map(([k, v]) => (
                  <div
                    key={k}
                    style={{
                      padding: "4px 10px",
                      borderRadius: 20,
                      fontSize: 11,
                      background: "rgba(0,212,255,0.1)",
                      border: "1px solid rgba(0,212,255,0.2)",
                      color: "#00d4ff",
                    }}
                  >
                    {k} = {v}
                  </div>
                ))}
              </div>
            </div>
          )}

          {mem.projects && Object.keys(mem.projects).length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div style={sectionTitle}>Projects</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
                {Object.entries(mem.projects).map(([k, v]) => (
                  <div
                    key={k}
                    style={{
                      padding: "7px 11px",
                      borderRadius: 8,
                      fontSize: 12,
                      background: "rgba(123,94,255,0.07)",
                      border: "1px solid rgba(123,94,255,0.15)",
                      color: "rgba(var(--text-rgb),0.65)",
                    }}
                  >
                    <strong style={{ color: "#7b5eff" }}>{k}</strong>: {v}
                  </div>
                ))}
              </div>
            </div>
          )}

          {(!mem.facts || mem.facts.length === 0) &&
            (!mem.preferences || Object.keys(mem.preferences).length === 0) &&
            (!mem.projects || Object.keys(mem.projects).length === 0) && (
              <div style={{ textAlign: "center", padding: "20px 0", color: "rgba(var(--tint-rgb),0.25)", fontSize: 13 }}>
                No memories yet. Add facts, key=value preferences, or project descriptions.
              </div>
            )}

          <button
            onClick={clearAll}
            style={{
              marginTop: 10,
              width: "100%",
              padding: 8,
              borderRadius: 9,
              border: "none",
              cursor: "pointer",
              background: "rgba(255,69,58,0.08)",
              color: "#ff453a",
              fontSize: 12,
              fontWeight: 500,
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 6,
            }}
          >
            <Ic.trash s={13} c="#ff453a" /> Clear All Memory
          </button>
        </>
      )}
    </PanelModal>
  )
}

/* ── Goals ── */
type Goal = { text: string; done: boolean }

export function GoalsPanel({ onClose }: { onClose: () => void }) {
  const [goals, setGoals] = useState<Goal[]>([])
  const [newGoal, setNewGoal] = useState("")
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [progress, setProgress] = useState(0)

  const fetchGoals = () => {
    apiFetch("/api/goals")
      .then((r) => r.json())
      .then((d) => {
        setGoals(d.goals || [])
        setProgress(d.progress_pct || 0)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => {
    fetchGoals()
  }, [])

  const addGoal = async () => {
    if (!newGoal.trim()) return
    setSaving(true)
    await apiFetch("/api/goals", { method: "POST", body: JSON.stringify({ text: newGoal.trim() }) }).catch(() => {})
    setNewGoal("")
    fetchGoals()
    setSaving(false)
  }

  const completeGoal = async (idx: number) => {
    await apiFetch(`/api/goals/${idx + 1}`, { method: "PATCH" }).catch(() => {})
    fetchGoals()
  }

  const clearGoals = async () => {
    await apiFetch("/api/goals", { method: "DELETE" }).catch(() => {})
    setGoals([])
    setProgress(0)
  }

  return (
    <PanelModal title="Today's Goals" icon={<Ic.target s={17} c="rgba(var(--text-rgb),0.7)" />} onClose={onClose}>
      {loading ? (
        <div style={{ textAlign: "center", padding: 30, color: "rgba(var(--tint-rgb),0.3)" }}>Loading…</div>
      ) : (
        <>
          {goals.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: 6,
                  fontSize: 12,
                  color: "rgba(var(--tint-rgb),0.4)",
                }}
              >
                <span>
                  {goals.filter((g) => g.done).length}/{goals.length} done
                </span>
                <span>{progress}%</span>
              </div>
              <div style={{ height: 5, borderRadius: 3, background: "rgba(var(--tint-rgb),0.08)", overflow: "hidden" }}>
                <div
                  style={{
                    height: "100%",
                    width: `${progress}%`,
                    borderRadius: 3,
                    background: "linear-gradient(90deg,#00d4ff,#7b5eff)",
                    transition: "width 0.4s ease",
                  }}
                />
              </div>
            </div>
          )}

          <div style={{ display: "flex", gap: 7, marginBottom: 16 }}>
            <input
              value={newGoal}
              onChange={(e) => setNewGoal(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addGoal()}
              placeholder="Add today's goal…"
              style={{
                flex: 1,
                padding: "9px 12px",
                borderRadius: 9,
                fontSize: 13,
                background: "rgba(var(--tint-rgb),0.05)",
                border: "1px solid rgba(var(--tint-rgb),0.09)",
                color: "var(--text-color)",
                outline: "none",
              }}
            />
            <button
              onClick={addGoal}
              disabled={saving}
              style={{
                padding: "9px 16px",
                borderRadius: 9,
                border: "none",
                cursor: "pointer",
                background: "rgba(0,212,255,0.18)",
                color: "#00d4ff",
                fontSize: 13,
                fontWeight: 600,
              }}
            >
              {saving ? "…" : "Add"}
            </button>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 7, maxHeight: 280, overflowY: "auto" }}>
            {goals.map((g, i) => (
              <div
                key={i}
                onClick={() => !g.done && completeGoal(i)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  padding: "10px 13px",
                  borderRadius: 10,
                  cursor: g.done ? "default" : "pointer",
                  background: g.done ? "rgba(48,209,88,0.07)" : "rgba(var(--tint-rgb),0.04)",
                  border: g.done ? "1px solid rgba(48,209,88,0.2)" : "1px solid rgba(var(--tint-rgb),0.07)",
                  transition: "all 0.2s",
                }}
              >
                <div
                  style={{
                    width: 18,
                    height: 18,
                    borderRadius: "50%",
                    flexShrink: 0,
                    border: g.done ? "none" : "1.5px solid rgba(var(--tint-rgb),0.25)",
                    background: g.done ? "#30d158" : "transparent",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  {g.done && <Ic.check s={11} c="#fff" />}
                </div>
                <span
                  style={{
                    fontSize: 13,
                    lineHeight: 1.4,
                    color: g.done ? "rgba(48,209,88,0.7)" : "rgba(var(--text-rgb),0.75)",
                    textDecoration: g.done ? "line-through" : "none",
                  }}
                >
                  {g.text}
                </span>
              </div>
            ))}
          </div>

          {goals.length === 0 && (
            <div style={{ textAlign: "center", padding: "20px 0", color: "rgba(var(--tint-rgb),0.25)", fontSize: 13 }}>
              No goals yet. What do you want to accomplish today?
            </div>
          )}

          {goals.length > 0 && (
            <button
              onClick={clearGoals}
              style={{
                marginTop: 12,
                width: "100%",
                padding: 8,
                borderRadius: 9,
                border: "none",
                cursor: "pointer",
                background: "rgba(255,69,58,0.08)",
                color: "#ff453a",
                fontSize: 12,
                fontWeight: 500,
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 6,
              }}
            >
              <Ic.trash s={13} c="#ff453a" /> Clear All Goals
            </button>
          )}
        </>
      )}
    </PanelModal>
  )
}
