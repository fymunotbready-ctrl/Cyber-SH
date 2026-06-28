"use client"

import { useEffect, useState, type ReactNode } from "react"
import { Ic } from "./icons"
import { PanelModal, SettingRow, Toggle } from "./ui"
import { apiFetch, liquidGlass, ACCENT_RGB, ACCENT_HEX } from "./lib"

// ─── Profile ────────────────────────────────────────────────────────────────
type Profile = { name: string; email: string; job: string; about: string; language: string }

const PROFILE_KEY = "cybersh_profile"

function Field({ label, value, onChange, placeholder, area }: { label: string; value: string; onChange: (v: string) => void; placeholder?: string; area?: boolean }) {
  const base = { width: "100%", marginTop: 8, padding: "10px 14px", borderRadius: 10, background: "rgba(var(--tint-rgb),0.06)", border: "1px solid rgba(var(--tint-rgb),0.1)", color: "var(--text-color)", fontSize: 14, outline: "none" } as const
  return (
    <div style={{ marginBottom: 14 }}>
      <label style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.4)", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>{label}</label>
      {area ? (
        <textarea value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} rows={3} style={{ ...base, resize: "vertical", lineHeight: 1.5 }} />
      ) : (
        <input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} style={base} />
      )}
    </div>
  )
}

export function ProfilePanel({ user, onClose }: { user: { name: string }; onClose: () => void }) {
  const [p, setP] = useState<Profile>({ name: user.name, email: "", job: "", about: "", language: "English" })
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    try {
      const raw = localStorage.getItem(PROFILE_KEY)
      if (raw) setP((prev) => ({ ...prev, ...JSON.parse(raw) }))
    } catch {}
  }, [])

  const set = (k: keyof Profile) => (v: string) => setP((prev) => ({ ...prev, [k]: v }))
  const save = () => {
    try { localStorage.setItem(PROFILE_KEY, JSON.stringify(p)) } catch {}
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <PanelModal title="Your Profile" icon={<Ic.person s={18} c={ACCENT_HEX} />} onClose={onClose}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: 24 }}>
        <div
          style={{
            width: 72,
            height: 72,
            borderRadius: "50%",
            background: "linear-gradient(135deg,rgba(255,255,255,0.28),rgba(255,255,255,0.12))",
            backdropFilter: "blur(24px) saturate(200%)",
            WebkitBackdropFilter: "blur(24px) saturate(200%)",
            border: "1px solid rgba(255,255,255,0.18)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 28,
            fontWeight: 700,
            color: "#fff",
            boxShadow: `0 0 24px rgba(${ACCENT_RGB},0.3)`,
            marginBottom: 12,
          }}
        >
          {(p.name[0] || "?").toUpperCase()}
        </div>
        <div style={{ fontSize: 13, color: "rgba(var(--tint-rgb),0.4)" }}>This info helps the AI talk to you better</div>
      </div>

      <Field label="Your Name" value={p.name} onChange={set("name")} placeholder="What should we call you?" />
      <Field label="Email" value={p.email} onChange={set("email")} placeholder="you@example.com" />
      <Field label="What You Do" value={p.job} onChange={set("job")} placeholder="e.g. Student, Developer, Designer" />
      <Field label="About You" value={p.about} onChange={set("about")} placeholder="A few words about you and what you're working on" area />

      <div style={{ marginBottom: 20 }}>
        <label style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.4)", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>Reply Language</label>
        <select
          value={p.language}
          onChange={(e) => set("language")(e.target.value)}
          style={{ width: "100%", marginTop: 8, padding: "10px 14px", borderRadius: 10, background: "rgba(var(--tint-rgb),0.06)", border: "1px solid rgba(var(--tint-rgb),0.1)", color: "var(--text-color)", fontSize: 14, outline: "none" }}
        >
          {["English", "Spanish", "French", "German", "Hindi", "Arabic", "Chinese", "Portuguese"].map((l) => (
            <option key={l} value={l} style={{ color: "#000" }}>{l}</option>
          ))}
        </select>
      </div>

      <button
        onClick={save}
        className="lg-btn"
        style={{ ...liquidGlass(ACCENT_RGB, "md"), width: "100%", borderRadius: 12, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", gap: 7 }}
      >
        {saved && <Ic.check s={15} c="#fff" />}
        {saved ? "Saved" : "Save Profile"}
      </button>
    </PanelModal>
  )
}

// ─── Settings ───────────────────────────────────────────────────────────────
const SETTINGS_KEY = "cybersh_settings"

function SectionTitle({ children }: { children: ReactNode }) {
  return (
    <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", color: "rgba(var(--tint-rgb),0.3)", margin: "18px 0 4px" }}>
      {children}
    </div>
  )
}

function SelectRow({ label, desc, value, options, onChange }: { label: string; desc?: string; value: string; options: string[]; onChange: (v: string) => void }) {
  return (
    <SettingRow label={label} desc={desc}>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ padding: "7px 10px", borderRadius: 9, background: "rgba(var(--tint-rgb),0.08)", border: "1px solid rgba(var(--tint-rgb),0.12)", color: "var(--text-color)", fontSize: 13, outline: "none", cursor: "pointer", flexShrink: 0 }}
      >
        {options.map((o) => (
          <option key={o} value={o} style={{ color: "#000" }}>{o}</option>
        ))}
      </select>
    </SettingRow>
  )
}

const DEFAULT_SETTINGS = {
  sound: true,
  autoScroll: true,
  sendOnEnter: true,
  timestamps: false,
  compactMode: false,
  saveHistory: true,
  useMemory: true,
  notifications: false,
  telemetry: false,
  replyLength: "Medium",
  replyTone: "Friendly",
  textSize: "Normal",
  defaultMode: "Chat",
}

export function SettingsPanel({ onClose }: { onClose: () => void }) {
  const [s, setS] = useState(DEFAULT_SETTINGS)

  useEffect(() => {
    try {
      const raw = localStorage.getItem(SETTINGS_KEY)
      if (raw) setS((prev) => ({ ...prev, ...JSON.parse(raw) }))
    } catch {}
  }, [])

  const persist = (next: typeof s) => {
    setS(next)
    try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(next)) } catch {}
  }
  const toggle = (k: keyof typeof s) => persist({ ...s, [k]: !s[k] })
  const pick = (k: keyof typeof s) => (v: string) => persist({ ...s, [k]: v })

  return (
    <PanelModal title="Settings" icon={<Ic.settings s={18} c={ACCENT_HEX} />} onClose={onClose}>
      <SectionTitle>How the AI Replies</SectionTitle>
      <SelectRow label="Answer length" desc="How long replies should be" value={s.replyLength} options={["Short", "Medium", "Long"]} onChange={pick("replyLength")} />
      <SelectRow label="Tone" desc="How the AI sounds when it talks" value={s.replyTone} options={["Friendly", "Professional", "Casual", "Direct"]} onChange={pick("replyTone")} />
      <SelectRow label="Start in mode" desc="Which mode opens by default" value={s.defaultMode} options={["Chat", "Code", "Creative", "Security", "Agent"]} onChange={pick("defaultMode")} />
      <SettingRow label="Remember me" desc="Let the AI use what it knows about you">
        <Toggle on={s.useMemory} onToggle={() => toggle("useMemory")} />
      </SettingRow>

      <SectionTitle>Chat</SectionTitle>
      <SettingRow label="Send with Enter" desc="Enter sends, Shift+Enter makes a new line">
        <Toggle on={s.sendOnEnter} onToggle={() => toggle("sendOnEnter")} />
      </SettingRow>
      <SettingRow label="Save my chats" desc="Keep past chats so you can open them later">
        <Toggle on={s.saveHistory} onToggle={() => toggle("saveHistory")} />
      </SettingRow>
      <SettingRow label="Scroll to newest" desc="Always jump to the latest message">
        <Toggle on={s.autoScroll} onToggle={() => toggle("autoScroll")} />
      </SettingRow>
      <SettingRow label="Show times" desc="Put the time next to each message">
        <Toggle on={s.timestamps} onToggle={() => toggle("timestamps")} />
      </SettingRow>
      <SettingRow label="Sound" desc="Play a small sound on send and reply">
        <Toggle on={s.sound} onToggle={() => toggle("sound")} />
      </SettingRow>

      <SectionTitle>Look</SectionTitle>
      <SelectRow label="Text size" desc="Make words bigger or smaller" value={s.textSize} options={["Small", "Normal", "Large"]} onChange={pick("textSize")} />
      <SettingRow label="Tight spacing" desc="Fit more messages on the screen">
        <Toggle on={s.compactMode} onToggle={() => toggle("compactMode")} />
      </SettingRow>

      <SectionTitle>Privacy</SectionTitle>
      <SettingRow label="Notifications" desc="Let the app show you alerts">
        <Toggle on={s.notifications} onToggle={() => toggle("notifications")} />
      </SettingRow>
      <SettingRow label="Share usage data" desc="Send anonymous data to help improve the app">
        <Toggle on={s.telemetry} onToggle={() => toggle("telemetry")} color="#ff453a" />
      </SettingRow>

      <div style={{ marginTop: 20, padding: "12px 14px", borderRadius: 10, background: "rgba(255,255,255,0.05)", backdropFilter: "blur(20px) saturate(180%)", WebkitBackdropFilter: "blur(20px) saturate(180%)", border: "1px solid rgba(255,255,255,0.12)", display: "flex", alignItems: "center", gap: 8 }}>
        <Ic.lock s={14} c="rgba(255,255,255,0.8)" />
        <div style={{ fontSize: 12, color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>Everything stays on your device. Nothing is sent online.</div>
      </div>
    </PanelModal>
  )
}

// ─── Theme ──────────────────────────────────────────────────────────────────
export function ThemePanel({ onClose, mode, setMode }: { onClose: () => void; mode: "dark" | "light"; setMode: (m: "dark" | "light") => void }) {
  const themes = [
    { id: "blue", label: "System Blue", primary: "#0A84FF", secondary: "#0060df" },
    { id: "teal", label: "iOS Teal", primary: "#64D2FF", secondary: "#0a84ff" },
    { id: "green", label: "Matrix Green", primary: "#30d158", secondary: "#20a040" },
    { id: "orange", label: "Flame", primary: "#ff9f0a", secondary: "#cc7000" },
    { id: "pink", label: "Synthwave", primary: "#ff375f", secondary: "#cc1040" },
    { id: "white", label: "Ghost", primary: "rgba(var(--text-rgb),0.9)", secondary: "rgba(200,200,220,0.7)" },
  ]
  const [active, setActive] = useState("blue")
  const appearances = [
    { id: "dark" as const, label: "Dark", Icon: Ic.moon },
    { id: "light" as const, label: "Light", Icon: Ic.sun },
  ]
  return (
    <PanelModal title="Theme" icon={<Ic.theme s={18} c={ACCENT_HEX} />} onClose={onClose}>
      <div style={{ fontSize: 12, fontWeight: 600, color: "rgba(var(--tint-rgb),0.45)", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 10 }}>Appearance</div>
      <div style={{ display: "flex", gap: 6, padding: 5, borderRadius: 14, marginBottom: 22, background: "rgba(var(--tint-rgb),0.05)", border: "1px solid rgba(var(--tint-rgb),0.08)" }}>
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
            }}
          >
            <div style={{ width: 22, height: 22, borderRadius: "50%", flexShrink: 0, background: `linear-gradient(135deg,${t.primary},${t.secondary})`, boxShadow: active === t.id ? `0 0 10px ${t.primary}66` : "none" }} />
            <span style={{ fontSize: 13, fontWeight: 500, color: active === t.id ? t.primary : "rgba(var(--text-rgb),0.65)" }}>{t.label}</span>
          </button>
        ))}
      </div>
      <button onClick={onClose} className="lg-btn" style={{ ...liquidGlass(ACCENT_RGB, "md"), width: "100%", marginTop: 20, borderRadius: 12 }}>
        Apply Theme
      </button>
    </PanelModal>
  )
}

// ─── Shortcuts ──────────────────────────────────────────────────────────────
export function ShortcutsPanel({ onClose }: { onClose: () => void }) {
  const groups = [
    { label: "Chat", shortcuts: [{ keys: ["Enter"], desc: "Send message" }, { keys: ["Shift", "Enter"], desc: "New line" }, { keys: ["Ctrl", "K"], desc: "New conversation" }, { keys: ["Ctrl", "L"], desc: "Clear chat" }] },
    { label: "Modes", shortcuts: [{ keys: ["Ctrl", "1"], desc: "Agent mode" }, { keys: ["Ctrl", "2"], desc: "Security mode" }, { keys: ["Ctrl", "3"], desc: "Creative mode" }, { keys: ["Ctrl", "4"], desc: "Code mode" }, { keys: ["Ctrl", "5"], desc: "Chat mode" }] },
    { label: "App", shortcuts: [{ keys: ["Ctrl", ","], desc: "Open settings" }, { keys: ["Ctrl", "\\"], desc: "Show or hide the side menu" }, { keys: ["Escape"], desc: "Close this window" }] },
  ]
  return (
    <PanelModal title="Keyboard Shortcuts" icon={<Ic.keyboard s={18} c={ACCENT_HEX} />} onClose={onClose}>
      {groups.map((g) => (
        <div key={g.label} style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase", color: "rgba(var(--tint-rgb),0.3)", marginBottom: 10 }}>{g.label}</div>
          {g.shortcuts.map((sc) => (
            <div key={sc.desc} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "9px 0", borderBottom: "1px solid rgba(var(--tint-rgb),0.04)" }}>
              <span style={{ fontSize: 13, color: "rgba(var(--text-rgb),0.65)" }}>{sc.desc}</span>
              <div style={{ display: "flex", gap: 4 }}>
                {sc.keys.map((k) => (
                  <kbd key={k} style={{ padding: "3px 8px", borderRadius: 6, fontSize: 11, fontWeight: 600, background: "rgba(var(--tint-rgb),0.08)", color: "rgba(var(--text-rgb),0.8)", border: "1px solid rgba(var(--tint-rgb),0.12)" }}>
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

// ─── Help ───────────────────────────────────────────────────────────────────
export function HelpPanel({ onClose }: { onClose: () => void }) {
  const [open, setOpen] = useState<number | null>(null)
  const faqs = [
    { q: "Does this work without internet?", a: "Yes. Once it's set up, the app runs fully on your own device. You don't need to be online and nothing you type is sent anywhere." },
    { q: "What do the modes do?", a: "Agent does tasks on your computer. Security helps you stay safe. Creative helps with design and ideas. Code writes code for you. Chat is for everyday questions." },
    { q: "How does it remember things?", a: "It saves your name, projects, and likes right on your device, so you don't have to repeat yourself next time. You can clear this anytime in the Memory panel." },
    { q: "Where are my chats saved?", a: "Your past chats are kept on this device only. Open them anytime from the list on the left, and delete them whenever you want." },
    { q: "How do I get help?", a: "Type /help in any chat for quick tips, or just ask the AI your question in plain words." },
  ]
  return (
    <PanelModal title="Help Center" icon={<Ic.help s={18} c={ACCENT_HEX} />} onClose={onClose}>
      <div style={{ marginBottom: 16, padding: "12px 14px", borderRadius: 10, background: `rgba(${ACCENT_RGB},0.06)`, border: `1px solid rgba(${ACCENT_RGB},0.15)`, display: "flex", alignItems: "center", gap: 8 }}>
        <Ic.chat s={14} c={ACCENT_HEX} />
        <div style={{ fontSize: 13, color: `rgba(${ACCENT_RGB},0.95)`, fontWeight: 500 }}>Type /help inside any chat for in-line assistance</div>
      </div>
      {faqs.map((f, i) => (
        <div key={i} style={{ borderBottom: "1px solid rgba(var(--tint-rgb),0.05)" }}>
          <button
            onClick={() => setOpen(open === i ? null : i)}
            style={{ width: "100%", padding: "13px 0", background: "none", border: "none", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "space-between", color: "rgba(var(--text-rgb),0.85)", textAlign: "left" }}
          >
            <span style={{ fontSize: 13, fontWeight: 500, paddingRight: 12 }}>{f.q}</span>
            <span style={{ transform: open === i ? "rotate(90deg)" : "none", transition: "transform 0.2s", display: "flex" }}>
              <Ic.chevR s={14} c="rgba(var(--tint-rgb),0.3)" />
            </span>
          </button>
          {open === i && <div style={{ padding: "0 0 14px", fontSize: 13, lineHeight: 1.65, color: "rgba(var(--text-rgb),0.5)", animation: "cyberFadeIn 0.2s ease" }}>{f.a}</div>}
        </div>
      ))}
    </PanelModal>
  )
}

// ─── Tools ──────────────────────────────────────────────────────────────────
type Tool = { id: string; Icon: (typeof Ic)[keyof typeof Ic]; label: string; placeholder: string; endpoint: string; method?: string; build?: (v: string) => Record<string, unknown> }

export function ToolsPanel({ onClose }: { onClose: () => void; onSendCommand?: (cmd: string) => void }) {
  const [toolInput, setToolInput] = useState<Record<string, string>>({})
  const [toolResult, setToolResult] = useState<Record<string, string>>({})
  const [toolLoading, setToolLoading] = useState<Record<string, boolean>>({})
  const [activeTab, setActiveTab] = useState<"ai" | "util">("ai")

  const runTool = async (t: Tool, v: string) => {
    setToolLoading((p) => ({ ...p, [t.id]: true }))
    setToolResult((p) => ({ ...p, [t.id]: "" }))
    try {
      const res = await apiFetch(t.endpoint, t.method === "GET" ? {} : { method: "POST", body: JSON.stringify(t.build ? t.build(v) : { text: v }) })
      const data = await res.json()
      setToolResult((p) => ({ ...p, [t.id]: JSON.stringify(data, null, 2) }))
    } catch {
      setToolResult((p) => ({
        ...p,
        [t.id]: `[simulated] ${t.label} on "${v || "(empty)"}"\nConnect a backend via NEXT_PUBLIC_CYBERSH_API to run this tool live.`,
      }))
    }
    setToolLoading((p) => ({ ...p, [t.id]: false }))
  }

  const aiTools: Tool[] = [
    { id: "explain", Icon: Ic.search, label: "Explain Code", placeholder: "Paste code here…", endpoint: "/api/ai/explain-code" },
    { id: "roast", Icon: Ic.flame, label: "Roast Code", placeholder: "Paste code here…", endpoint: "/api/ai/roast" },
    { id: "debug", Icon: Ic.bug, label: "Debug Code", placeholder: "Paste buggy code…", endpoint: "/api/ai/debug", build: (v) => ({ code: v }) },
    { id: "review", Icon: Ic.list, label: "Review Code", placeholder: "Paste code…", endpoint: "/api/ai/review", build: (v) => ({ code: v }) },
    { id: "improve", Icon: Ic.sparkles, label: "Improve Text", placeholder: "Enter text…", endpoint: "/api/ai/improve" },
    { id: "eli5", Icon: Ic.smiley, label: "ELI5", placeholder: "Topic to explain…", endpoint: "/api/ai/eli5", build: (v) => ({ topic: v }) },
    { id: "osint", Icon: Ic.eye, label: "OSINT Checklist", placeholder: "Target (domain/user/email)…", endpoint: "/api/ai/osint", build: (v) => ({ target: v }) },
    { id: "regex", Icon: Ic.bolt, label: "Generate Regex", placeholder: "Describe pattern…", endpoint: "/api/ai/regex", build: (v) => ({ description: v }) },
    { id: "cron", Icon: Ic.clock, label: "Cron Helper", placeholder: "e.g. every day at 3am…", endpoint: "/api/ai/cron", build: (v) => ({ expression: v }) },
    { id: "wordlist", Icon: Ic.doc, label: "Wordlist Gen", placeholder: "Target info (name, DOB…)…", endpoint: "/api/ai/wordlist", build: (v) => ({ info: v }) },
    { id: "think", Icon: Ic.brain, label: "Deep Think", placeholder: "Complex question…", endpoint: "/api/ai/think", build: (v) => ({ question: v }) },
    { id: "debate", Icon: Ic.scale, label: "Debate", placeholder: "Topic to debate…", endpoint: "/api/ai/debate", build: (v) => ({ topic: v }) },
  ]

  const utilTools: Tool[] = [
    { id: "hash", Icon: Ic.key, label: "Hash Identify", placeholder: "Paste a hash…", endpoint: "/api/tools/hash", build: (v) => ({ hash: v }) },
    { id: "pwcheck", Icon: Ic.lock, label: "Password Check", placeholder: "Enter password…", endpoint: "/api/tools/pwcheck", build: (v) => ({ password: v }) },
    { id: "encode", Icon: Ic.box, label: "Encode/Decode", placeholder: "Text to encode…", endpoint: "/api/tools/encode" },
    { id: "calc", Icon: Ic.number, label: "Calculator", placeholder: "e.g. 2**10 or 15% of 200", endpoint: "/api/tools/calc", build: (v) => ({ expression: v }) },
    { id: "ipinfo", Icon: Ic.web, label: "IP Info", placeholder: "IP address or blank for yours…", endpoint: "/api/tools/ipinfo", method: "GET" },
    { id: "passgen", Icon: Ic.dice, label: "Password Gen", placeholder: "Type: password/phrase/token", endpoint: "/api/tools/passgen", method: "GET" },
    { id: "uuid", Icon: Ic.idcard, label: "UUID Gen", placeholder: "(leave blank for 1)", endpoint: "/api/tools/uuid", build: (v) => ({ count: parseInt(v) || 1 }) },
    { id: "slugify", Icon: Ic.textformat, label: "Slugify", placeholder: "Text to slugify…", endpoint: "/api/tools/slugify", method: "GET" },
  ]

  const tools = activeTab === "ai" ? aiTools : utilTools

  return (
    <PanelModal title="Tools" icon={<Ic.wrench s={18} c={ACCENT_HEX} />} onClose={onClose}>
      <div style={{ display: "flex", gap: 4, marginBottom: 18, padding: 3, borderRadius: 10, background: "rgba(var(--tint-rgb),0.05)" }}>
        {([["ai", "AI Tools", Ic.robot], ["util", "Utilities", Ic.wrench]] as const).map(([id, label, TabIcon]) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 7,
              padding: "7px 0",
              borderRadius: 8,
              border: "none",
              cursor: "pointer",
              background: activeTab === id ? `rgba(${ACCENT_RGB},0.18)` : "transparent",
              color: activeTab === id ? ACCENT_HEX : "rgba(var(--text-rgb),0.5)",
              fontSize: 13,
              fontWeight: activeTab === id ? 600 : 400,
            }}
          >
            <TabIcon s={14} c={activeTab === id ? ACCENT_HEX : "rgba(var(--text-rgb),0.5)"} />
            {label}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10, maxHeight: 420, overflowY: "auto" }}>
        {tools.map((t) => {
          const Icon = t.Icon
          return (
            <div key={t.id} style={{ padding: "12px 14px", borderRadius: 12, background: "rgba(var(--tint-rgb),0.03)", border: "1px solid rgba(var(--tint-rgb),0.07)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <Icon s={16} c={ACCENT_HEX} />
                <span style={{ fontSize: 13, fontWeight: 600, color: "rgba(var(--text-rgb),0.8)" }}>{t.label}</span>
              </div>
              <div style={{ display: "flex", gap: 7 }}>
                <input
                  value={toolInput[t.id] || ""}
                  onChange={(e) => setToolInput((p) => ({ ...p, [t.id]: e.target.value }))}
                  placeholder={t.placeholder}
                  onKeyDown={(e) => e.key === "Enter" && runTool(t, toolInput[t.id] || "")}
                  style={{ flex: 1, padding: "7px 11px", borderRadius: 8, fontSize: 12, background: "rgba(var(--tint-rgb),0.05)", border: "1px solid rgba(var(--tint-rgb),0.09)", color: "var(--text-color)", outline: "none" }}
                />
                <button
                  onClick={() => runTool(t, toolInput[t.id] || "")}
                  disabled={toolLoading[t.id]}
                  style={{ padding: "7px 14px", borderRadius: 8, border: "none", cursor: "pointer", background: `rgba(${ACCENT_RGB},${toolLoading[t.id] ? "0.1" : "0.2"})`, color: toolLoading[t.id] ? "rgba(var(--tint-rgb),0.3)" : ACCENT_HEX, fontSize: 12, fontWeight: 600, flexShrink: 0 }}
                >
                  {toolLoading[t.id] ? "…" : "Run"}
                </button>
              </div>
              {toolResult[t.id] && (
                <pre style={{ marginTop: 8, padding: "9px 11px", borderRadius: 8, fontSize: 11, lineHeight: 1.5, background: "rgba(0,0,0,0.3)", border: "1px solid rgba(var(--tint-rgb),0.06)", color: "rgba(var(--text-rgb),0.7)", overflowX: "auto", whiteSpace: "pre-wrap", maxHeight: 160, overflowY: "auto" }}>
                  {toolResult[t.id]}
                </pre>
              )}
            </div>
          )
        })}
      </div>
    </PanelModal>
  )
}

// ─── Memory ─────────────────────────────────────────────────────────────────
type Mem = { facts: string[]; preferences: Record<string, string>; projects: Record<string, string> }

export function MemoryPanel({ onClose }: { onClose: () => void }) {
  const [mem, setMem] = useState<Mem | null>(null)
  const [newFact, setNewFact] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiFetch("/api/memory")
      .then((r) => r.json())
      .then((d) => {
        setMem(d)
        setLoading(false)
      })
      .catch(() => {
        // local starter memory so the panel is functional offline
        setMem({
          facts: ["Prefers concise, technical answers", "Working on the Cyber-SH desktop build"],
          preferences: { theme: "dark", mode: "code" },
          projects: { "cyber-sh": "Offline-first personal AI assistant" },
        })
        setLoading(false)
      })
  }, [])

  const addFact = () => {
    const v = newFact.trim()
    if (!v || !mem) return
    apiFetch("/api/memory", { method: "POST", body: JSON.stringify({ text: v }) }).catch(() => {})
    if (v.includes("=")) {
      const [k, val] = v.split("=")
      setMem({ ...mem, preferences: { ...mem.preferences, [k.trim()]: val.trim() } })
    } else {
      setMem({ ...mem, facts: [...mem.facts, v] })
    }
    setNewFact("")
  }

  const clearAll = () => {
    apiFetch("/api/memory/all", { method: "DELETE" }).catch(() => {})
    setMem({ facts: [], preferences: {}, projects: {} })
  }

  const empty = mem && mem.facts.length === 0 && Object.keys(mem.preferences).length === 0 && Object.keys(mem.projects).length === 0

  return (
    <PanelModal title="Memory" icon={<Ic.memory s={18} c={ACCENT_HEX} />} onClose={onClose}>
      {loading ? (
        <div style={{ textAlign: "center", padding: 30, color: "rgba(var(--tint-rgb),0.3)" }}>Loading…</div>
      ) : !mem ? (
        <div style={{ textAlign: "center", padding: 30, color: "#ff453a" }}>Could not load memory.</div>
      ) : (
        <>
          <div style={{ display: "flex", gap: 7, marginBottom: 18 }}>
            <input
              value={newFact}
              onChange={(e) => setNewFact(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addFact()}
              placeholder="Add a fact, or key=value preference…"
              style={{ flex: 1, padding: "9px 12px", borderRadius: 9, fontSize: 13, background: "rgba(var(--tint-rgb),0.05)", border: "1px solid rgba(var(--tint-rgb),0.09)", color: "var(--text-color)", outline: "none" }}
            />
            <button onClick={addFact} style={{ padding: "9px 16px", borderRadius: 9, border: "none", cursor: "pointer", background: `rgba(${ACCENT_RGB},0.18)`, color: ACCENT_HEX, fontSize: 13, fontWeight: 600 }}>
              Add
            </button>
          </div>

          {mem.facts.length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "rgba(var(--tint-rgb),0.3)", marginBottom: 8 }}>Facts</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 5, maxHeight: 140, overflowY: "auto" }}>
                {[...mem.facts].reverse().map((f, i) => (
                  <div key={i} style={{ padding: "7px 11px", borderRadius: 8, fontSize: 12, background: "rgba(var(--tint-rgb),0.04)", border: "1px solid rgba(var(--tint-rgb),0.06)", color: "rgba(var(--text-rgb),0.65)", lineHeight: 1.4 }}>
                    {f}
                  </div>
                ))}
              </div>
            </div>
          )}

          {Object.keys(mem.preferences).length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "rgba(var(--tint-rgb),0.3)", marginBottom: 8 }}>Preferences</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {Object.entries(mem.preferences).map(([k, v]) => (
                  <div key={k} style={{ padding: "4px 10px", borderRadius: 20, fontSize: 11, background: `rgba(${ACCENT_RGB},0.1)`, border: `1px solid rgba(${ACCENT_RGB},0.2)`, color: ACCENT_HEX }}>
                    {k} = {v}
                  </div>
                ))}
              </div>
            </div>
          )}

          {Object.keys(mem.projects).length > 0 && (
            <div style={{ marginBottom: 14 }}>
              <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "rgba(var(--tint-rgb),0.3)", marginBottom: 8 }}>Projects</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
                {Object.entries(mem.projects).map(([k, v]) => (
                  <div key={k} style={{ padding: "7px 11px", borderRadius: 8, fontSize: 12, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "rgba(var(--text-rgb),0.65)" }}>
                    <strong style={{ color: "rgba(255,255,255,0.85)" }}>{k}</strong>: {v}
                  </div>
                ))}
              </div>
            </div>
          )}

          {empty && <div style={{ textAlign: "center", padding: "20px 0", color: "rgba(var(--tint-rgb),0.25)", fontSize: 13 }}>No memories yet. Add facts or key=value preferences.</div>}

          <button onClick={clearAll} style={{ marginTop: 10, width: "100%", padding: 8, borderRadius: 9, border: "none", cursor: "pointer", background: "rgba(255,69,58,0.08)", color: "#ff453a", fontSize: 12, fontWeight: 500, display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
            <Ic.trash s={13} c="#ff453a" /> Clear All Memory
          </button>
        </>
      )}
    </PanelModal>
  )
}

// ─── Goals ──────────────────────────────────────────────────────────────────
type Goal = { text: string; done: boolean }

export function GoalsPanel({ onClose }: { onClose: () => void }) {
  const [goals, setGoals] = useState<Goal[]>([])
  const [newGoal, setNewGoal] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiFetch("/api/goals")
      .then((r) => r.json())
      .then((d) => {
        setGoals(d.goals || [])
        setLoading(false)
      })
      .catch(() => {
        setGoals([
          { text: "Ship the offline build", done: false },
          { text: "Wire up persistent memory", done: true },
        ])
        setLoading(false)
      })
  }, [])

  const progress = goals.length ? Math.round((goals.filter((g) => g.done).length / goals.length) * 100) : 0

  const addGoal = () => {
    const v = newGoal.trim()
    if (!v) return
    apiFetch("/api/goals", { method: "POST", body: JSON.stringify({ text: v }) }).catch(() => {})
    setGoals((p) => [...p, { text: v, done: false }])
    setNewGoal("")
  }
  const completeGoal = (idx: number) => {
    apiFetch(`/api/goals/${idx + 1}`, { method: "PATCH" }).catch(() => {})
    setGoals((p) => p.map((g, i) => (i === idx ? { ...g, done: true } : g)))
  }
  const clearGoals = () => {
    apiFetch("/api/goals", { method: "DELETE" }).catch(() => {})
    setGoals([])
  }

  return (
    <PanelModal title="Today's Goals" icon={<Ic.target s={18} c={ACCENT_HEX} />} onClose={onClose}>
      {loading ? (
        <div style={{ textAlign: "center", padding: 30, color: "rgba(var(--tint-rgb),0.3)" }}>Loading…</div>
      ) : (
        <>
          {goals.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 12, color: "rgba(var(--tint-rgb),0.4)" }}>
                <span>
                  {goals.filter((g) => g.done).length}/{goals.length} done
                </span>
                <span>{progress}%</span>
              </div>
              <div style={{ height: 5, borderRadius: 3, background: "rgba(var(--tint-rgb),0.08)", overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${progress}%`, borderRadius: 3, background: "linear-gradient(90deg,rgba(255,255,255,0.9),rgba(255,255,255,0.55))", transition: "width 0.4s ease" }} />
              </div>
            </div>
          )}

          <div style={{ display: "flex", gap: 7, marginBottom: 16 }}>
            <input
              value={newGoal}
              onChange={(e) => setNewGoal(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addGoal()}
              placeholder="Add today's goal…"
              style={{ flex: 1, padding: "9px 12px", borderRadius: 9, fontSize: 13, background: "rgba(var(--tint-rgb),0.05)", border: "1px solid rgba(var(--tint-rgb),0.09)", color: "var(--text-color)", outline: "none" }}
            />
            <button onClick={addGoal} style={{ padding: "9px 16px", borderRadius: 9, border: "none", cursor: "pointer", background: `rgba(${ACCENT_RGB},0.18)`, color: ACCENT_HEX, fontSize: 13, fontWeight: 600 }}>
              Add
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
                }}
              >
                <div style={{ width: 18, height: 18, borderRadius: "50%", flexShrink: 0, border: g.done ? "none" : "1.5px solid rgba(var(--tint-rgb),0.25)", background: g.done ? "#30d158" : "transparent", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  {g.done && <Ic.check s={11} c="#fff" />}
                </div>
                <span style={{ fontSize: 13, lineHeight: 1.4, color: g.done ? "rgba(48,209,88,0.8)" : "rgba(var(--text-rgb),0.75)", textDecoration: g.done ? "line-through" : "none" }}>{g.text}</span>
              </div>
            ))}
          </div>

          {goals.length === 0 && <div style={{ textAlign: "center", padding: "20px 0", color: "rgba(var(--tint-rgb),0.25)", fontSize: 13 }}>No goals yet. What do you want to accomplish today?</div>}

          {goals.length > 0 && (
            <button onClick={clearGoals} style={{ marginTop: 12, width: "100%", padding: 8, borderRadius: 9, border: "none", cursor: "pointer", background: "rgba(255,69,58,0.08)", color: "#ff453a", fontSize: 12, fontWeight: 500, display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
              <Ic.trash s={13} c="#ff453a" /> Clear All Goals
            </button>
          )}
        </>
      )}
    </PanelModal>
  )
}
