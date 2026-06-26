"use client"

import { useEffect, useRef, useState, useCallback } from "react"
import { BrandLogo } from "./brand-logo"
import { Ic } from "./icons"
import { ModeTag, TypingDots, ProfileMenu } from "./ui"
import { MODES, PERSONALITIES, glass, glassModal, streamChat, ACCENT_RGB, ACCENT_HEX, type ModeId } from "./lib"
import { ProfilePanel, SettingsPanel, ThemePanel, ShortcutsPanel, HelpPanel, ToolsPanel, MemoryPanel, GoalsPanel } from "./panels"

type Msg = { id: number; role: "user" | "ai"; text: string; mode: string; streaming?: boolean }
type PanelKey = "profile" | "settings" | "theme" | "shortcuts" | "help" | "tools" | "memory" | "goals"

const DAILY_TIP = "Press Ctrl+K to start a fresh conversation without losing your modes."

export function Dashboard({
  user,
  onLogout,
  mode,
  setMode,
}: {
  user: { name: string }
  onLogout: () => void
  mode: "dark" | "light"
  setMode: (m: "dark" | "light") => void
}) {
  const [activeMode, setActiveMode] = useState<ModeId>("chat")
  const [persona, setPersona] = useState("default")
  const [messages, setMessages] = useState<Msg[]>([
    { id: 1, role: "ai", text: "Welcome to Cyber-SH. Choose a mode, pick a persona, or just start chatting.", mode: "chat" },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [showProfile, setShowProfile] = useState(false)
  const [activePanel, setActivePanel] = useState<PanelKey | null>(null)
  const [sessions] = useState<string[]>(["Recon plan — acme.dev", "Refactor auth module", "Landing page copy"])
  const [isMobile, setIsMobile] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [showPersonaMenu, setShowPersonaMenu] = useState(false)
  const profileRef = useRef<HTMLDivElement>(null)
  const endRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const currentMode = MODES.find((m) => m.id === activeMode)!
  const currentPersona = PERSONALITIES.find((p) => p.id === persona) || PERSONALITIES[0]
  const CurrentModeIcon = currentMode.Icon
  const PersonaIcon = currentPersona.Icon

  useEffect(() => {
    const onResize = () => {
      const mobile = window.innerWidth < 768
      setIsMobile(mobile)
      setSidebarOpen(!mobile)
    }
    onResize()
    window.addEventListener("resize", onResize)
    return () => window.removeEventListener("resize", onResize)
  }, [])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  useEffect(() => {
    const h = (e: MouseEvent) => {
      if (profileRef.current && !profileRef.current.contains(e.target as Node)) setShowProfile(false)
    }
    document.addEventListener("mousedown", h)
    return () => document.removeEventListener("mousedown", h)
  }, [])

  const closeSidebarOnMobile = () => {
    if (isMobile) setSidebarOpen(false)
  }

  const send = useCallback(() => {
    if (!input.trim() || loading) return
    const txt = input.trim()
    const userMsg: Msg = { id: Date.now(), role: "user", text: txt, mode: activeMode }
    setMessages((p) => [...p, userMsg])
    setInput("")
    setLoading(true)

    const history = [...messages, userMsg]
      .filter((m) => m.role === "user" || m.role === "ai")
      .slice(-20)
      .map((m) => ({ role: m.role === "ai" ? "assistant" : m.role, content: m.text }))

    const aiId = Date.now() + 1
    setMessages((p) => [...p, { id: aiId, role: "ai", text: "", mode: activeMode, streaming: true }])

    streamChat(
      history,
      activeMode,
      persona,
      (token) => setMessages((p) => p.map((m) => (m.id === aiId ? { ...m, text: m.text + token } : m))),
      () => {
        setMessages((p) => p.map((m) => (m.id === aiId ? { ...m, streaming: false } : m)))
        setLoading(false)
        inputRef.current?.focus()
      },
      (errMsg) => {
        setMessages((p) => p.map((m) => (m.id === aiId ? { ...m, text: `API Error: ${errMsg}`, streaming: false } : m)))
        setLoading(false)
      },
    )
  }, [input, loading, activeMode, persona, messages])

  const handleLogout = () => {
    setShowProfile(false)
    onLogout()
  }

  const quickTools: { key: PanelKey; label: string; Icon: typeof Ic.wrench }[] = [
    { key: "tools", label: "Tools", Icon: Ic.wrench },
    { key: "memory", label: "Memory", Icon: Ic.memory },
    { key: "goals", label: "Goals", Icon: Ic.target },
  ]

  return (
    <div style={{ display: "flex", height: "100dvh", background: "var(--page-bg)", color: "var(--text-color)", overflow: "hidden", position: "relative" }}>
      {/* ambient */}
      <div style={{ position: "fixed", inset: 0, pointerEvents: "none", overflow: "hidden" }}>
        <div style={{ position: "absolute", top: "-15%", left: "30%", width: 600, height: 600, borderRadius: "50%", background: `radial-gradient(circle,rgba(${ACCENT_RGB},0.05) 0%,transparent 70%)`, filter: "blur(80px)" }} />
        <div style={{ position: "absolute", bottom: "10%", right: "10%", width: 400, height: 400, borderRadius: "50%", background: "radial-gradient(circle,rgba(255,255,255,0.04) 0%,transparent 70%)", filter: "blur(60px)" }} />
      </div>

      {isMobile && sidebarOpen && (
        <div onClick={() => setSidebarOpen(false)} style={{ position: "fixed", inset: 0, zIndex: 40, background: "rgba(0,0,0,0.55)", backdropFilter: "blur(4px)", WebkitBackdropFilter: "blur(4px)", animation: "cyberFadeIn 0.25s ease" }} />
      )}

      {/* Sidebar */}
      <aside
        style={{
          width: 260,
          flexShrink: 0,
          display: "flex",
          flexDirection: "column",
          padding: "20px 12px",
          gap: 4,
          zIndex: 50,
          ...(isMobile
            ? {
                position: "fixed",
                top: 0,
                left: 0,
                height: "100dvh",
                transform: sidebarOpen ? "translateX(0)" : "translateX(-100%)",
                transition: "transform 0.3s cubic-bezier(0.4,0,0.2,1)",
                background: "var(--sidebar-bg)",
                backdropFilter: "blur(32px)",
                WebkitBackdropFilter: "blur(32px)",
                borderRight: "1px solid rgba(var(--tint-rgb),0.08)",
                boxShadow: sidebarOpen ? "4px 0 40px rgba(0,0,0,0.6)" : "none",
              }
            : { position: "relative", ...glass(0.03), borderTop: "none", borderBottom: "none", borderLeft: "none" }),
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 9, padding: "8px 12px 20px" }}>
          <BrandLogo size={34} withText />
          <div style={{ marginLeft: "auto", width: 6, height: 6, borderRadius: "50%", background: "#30d158", boxShadow: "0 0 8px #30d158", animation: "cyberPulse 2.5s ease-in-out infinite" }} />
          {isMobile && (
            <button onClick={() => setSidebarOpen(false)} style={{ marginLeft: 4, background: "none", border: "none", cursor: "pointer", color: "rgba(var(--tint-rgb),0.4)", padding: 4, display: "flex" }}>
              <Ic.close s={18} />
            </button>
          )}
        </div>

        <button
          onClick={() => {
            setMessages([{ id: Date.now(), role: "ai", text: "New conversation started. How can I help?", mode: activeMode }])
            closeSidebarOnMobile()
          }}
          style={{ display: "flex", alignItems: "center", gap: 9, padding: "9px 12px", borderRadius: 10, border: "1px solid rgba(var(--tint-rgb),0.09)", background: "rgba(var(--tint-rgb),0.04)", color: "rgba(var(--text-rgb),0.65)", cursor: "pointer", fontSize: 13, fontWeight: 500, marginBottom: 8 }}
        >
          <Ic.plus s={15} /> New Conversation
        </button>

        <div style={{ fontSize: 10, fontWeight: 600, letterSpacing: "0.12em", color: "rgba(var(--tint-rgb),0.25)", textTransform: "uppercase", padding: "8px 12px 4px" }}>Modes</div>
        {MODES.map((m) => {
          const Icon = m.Icon
          const active = activeMode === m.id
          return (
            <button
              key={m.id}
              onClick={() => {
                setActiveMode(m.id)
                closeSidebarOnMobile()
              }}
              style={{ display: "flex", alignItems: "center", gap: 9, padding: "9px 12px", borderRadius: 10, border: "none", cursor: "pointer", textAlign: "left", background: active ? `${m.color}18` : "transparent", color: active ? m.color : "rgba(var(--text-rgb),0.55)", position: "relative" }}
            >
              {active && <div style={{ position: "absolute", left: 0, top: "20%", bottom: "20%", width: 2.5, borderRadius: 2, background: m.color, boxShadow: `0 0 8px ${m.color}` }} />}
              <Icon s={16} c={active ? m.color : "rgba(var(--text-rgb),0.45)"} />
              <div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{m.label}</div>
                <div style={{ fontSize: 11, opacity: 0.55, lineHeight: 1.3 }}>{m.desc}</div>
              </div>
            </button>
          )
        })}

        <div style={{ marginTop: 16, fontSize: 10, fontWeight: 600, letterSpacing: "0.12em", color: "rgba(var(--tint-rgb),0.25)", textTransform: "uppercase", padding: "8px 12px 4px" }}>Recent Sessions</div>
        {sessions.map((s, i) => (
          <button key={i} onClick={closeSidebarOnMobile} style={{ display: "flex", alignItems: "center", gap: 8, padding: "7px 12px", borderRadius: 9, border: "none", cursor: "pointer", background: "transparent", color: "rgba(var(--text-rgb),0.4)", fontSize: 12, textAlign: "left" }}>
            <Ic.chat s={13} c="rgba(var(--tint-rgb),0.3)" />
            <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{s}</span>
          </button>
        ))}

        <div style={{ marginTop: "auto", padding: "12px 12px 0", display: "flex", flexDirection: "column", gap: 6 }}>
          <div style={{ padding: "9px 11px", borderRadius: 10, background: "rgba(255,255,255,0.06)", backdropFilter: "blur(20px) saturate(180%)", WebkitBackdropFilter: "blur(20px) saturate(180%)", border: "1px solid rgba(255,255,255,0.12)", marginBottom: 2 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 10, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "rgba(255,255,255,0.7)", marginBottom: 3 }}>
              <Ic.lightbulb s={11} c="rgba(255,255,255,0.7)" /> Daily Tip
            </div>
            <div style={{ fontSize: 11, color: "rgba(var(--text-rgb),0.45)", lineHeight: 1.5 }}>{DAILY_TIP}</div>
          </div>

          <div style={{ display: "flex", gap: 5 }}>
            {quickTools.map((q) => (
              <button
                key={q.key}
                onClick={() => {
                  setActivePanel(q.key)
                  closeSidebarOnMobile()
                }}
                style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", gap: 5, padding: "7px 0", borderRadius: 9, border: "1px solid rgba(var(--tint-rgb),0.09)", background: "rgba(var(--tint-rgb),0.04)", color: "rgba(var(--text-rgb),0.5)", cursor: "pointer", fontSize: 11, fontWeight: 500 }}
              >
                <q.Icon s={13} c="rgba(var(--text-rgb),0.5)" /> {q.label}
              </button>
            ))}
          </div>

          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 6, padding: "9px 12px", borderRadius: 10, background: "rgba(255,255,255,0.06)", backdropFilter: "blur(20px) saturate(180%)", WebkitBackdropFilter: "blur(20px) saturate(180%)", border: "1px solid rgba(255,255,255,0.12)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <Ic.offline s={14} c="rgba(255,255,255,0.85)" />
              <span style={{ fontSize: 11, fontWeight: 500, color: "rgba(255,255,255,0.85)" }}>Offline</span>
            </div>
            <span style={{ fontSize: 10, color: "rgba(var(--tint-rgb),0.3)" }}>local-model</span>
          </div>
        </div>
      </aside>

      {/* Main */}
      <main style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", position: "relative", minWidth: 0 }}>
        <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: isMobile ? "12px 16px" : "14px 24px", flexShrink: 0, borderBottom: "1px solid rgba(var(--tint-rgb),0.06)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: isMobile ? 8 : 12 }}>
            {isMobile && (
              <button onClick={() => setSidebarOpen(true)} style={{ background: "none", border: "none", cursor: "pointer", padding: 6, color: "rgba(var(--tint-rgb),0.7)", display: "flex", flexDirection: "column", gap: 4, alignItems: "center", justifyContent: "center", borderRadius: 8 }}>
                <div style={{ width: 18, height: 2, background: "currentColor", borderRadius: 2 }} />
                <div style={{ width: 18, height: 2, background: "currentColor", borderRadius: 2 }} />
                <div style={{ width: 12, height: 2, background: "currentColor", borderRadius: 2 }} />
              </button>
            )}
            <div style={{ display: "flex", alignItems: "center", gap: 8, padding: isMobile ? "5px 10px" : "6px 14px", borderRadius: 10, background: `${currentMode.color}12`, border: `1px solid ${currentMode.color}2a` }}>
              <CurrentModeIcon s={15} c={currentMode.color} />
              <span style={{ fontSize: isMobile ? 12 : 13, fontWeight: 600, color: currentMode.color }}>{currentMode.label} Mode</span>
            </div>
            {!isMobile && <span style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.25)" }}>{currentMode.desc}</span>}

            <div style={{ position: "relative" }}>
              <button
                onClick={() => setShowPersonaMenu((p) => !p)}
                style={{ display: "flex", alignItems: "center", gap: 5, padding: "5px 10px", borderRadius: 10, border: "1px solid rgba(var(--tint-rgb),0.1)", background: "rgba(var(--tint-rgb),0.04)", color: "rgba(var(--text-rgb),0.65)", cursor: "pointer", fontSize: 12, fontWeight: 500 }}
              >
                <PersonaIcon s={14} c="rgba(var(--text-rgb),0.7)" />
                {!isMobile && <span>{currentPersona.label}</span>}
                <Ic.chevR s={11} c="rgba(var(--tint-rgb),0.3)" />
              </button>
              {showPersonaMenu && (
                <div style={{ position: "absolute", top: "calc(100% + 6px)", left: 0, width: 180, borderRadius: 14, overflow: "hidden", zIndex: 200, ...glassModal }}>
                  <div style={{ padding: 6, maxHeight: 320, overflowY: "auto" }}>
                    {PERSONALITIES.map((p) => {
                      const PIcon = p.Icon
                      const sel = persona === p.id
                      return (
                        <button
                          key={p.id}
                          onClick={() => {
                            setPersona(p.id)
                            setShowPersonaMenu(false)
                          }}
                          style={{ display: "flex", alignItems: "center", gap: 9, width: "100%", padding: "8px 10px", borderRadius: 9, border: "none", cursor: "pointer", background: sel ? `rgba(${ACCENT_RGB},0.1)` : "transparent", color: sel ? ACCENT_HEX : "rgba(var(--text-rgb),0.75)", textAlign: "left", fontSize: 13 }}
                        >
                          <PIcon s={15} c={sel ? ACCENT_HEX : "rgba(var(--text-rgb),0.6)"} />
                          <span style={{ fontWeight: sel ? 600 : 400 }}>{p.label}</span>
                        </button>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: isMobile ? 8 : 10, position: "relative" }} ref={profileRef}>
            {!isMobile && (
              <button
                onClick={() => setMessages((p) => [...p, { id: Date.now(), role: "ai", text: "New session started.", mode: activeMode }])}
                style={{ display: "flex", alignItems: "center", gap: 6, padding: "7px 14px", borderRadius: 10, border: "1px solid rgba(var(--tint-rgb),0.1)", background: "rgba(var(--tint-rgb),0.05)", color: "rgba(var(--text-rgb),0.7)", cursor: "pointer", fontSize: 13, fontWeight: 500 }}
              >
                <Ic.newChat s={14} /> New Chat
              </button>
            )}

            <button
              onClick={() => setShowProfile(!showProfile)}
              style={{ width: 40, height: 40, borderRadius: "50%", background: `linear-gradient(155deg,rgba(255,255,255,0.32),rgba(255,255,255,0.14))`, backdropFilter: "blur(24px) saturate(220%)", WebkitBackdropFilter: "blur(24px) saturate(220%)", border: showProfile ? "1.5px solid rgba(var(--tint-rgb),0.5)" : "1.5px solid rgba(var(--tint-rgb),0.25)", boxShadow: `inset 0 1.5px 0 rgba(var(--tint-rgb),0.5), 0 4px 14px rgba(${ACCENT_RGB},0.25)`, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, fontWeight: 700, color: "#fff" }}
            >
              {user.name[0].toUpperCase()}
            </button>

            {showProfile && <ProfileMenu user={user} onClose={() => setShowProfile(false)} onLogout={handleLogout} onOpenPanel={(p) => setActivePanel(p as PanelKey)} />}
          </div>
        </header>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: isMobile ? 16 : 24, display: "flex", flexDirection: "column", gap: 16 }}>
          {messages.map((msg) => (
            <div key={msg.id} style={{ display: "flex", flexDirection: msg.role === "user" ? "row-reverse" : "row", gap: 10, alignItems: "flex-end", maxWidth: isMobile ? "90%" : "80%", alignSelf: msg.role === "user" ? "flex-end" : "flex-start" }}>
              {msg.role === "ai" && (
                <div style={{ width: 30, height: 30, borderRadius: "50%", flexShrink: 0, background: `linear-gradient(135deg,rgba(255,255,255,0.2),rgba(255,255,255,0.08))`, border: `1px solid rgba(255,255,255,0.25)`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <BrandLogo size={18} />
                </div>
              )}
              <div
                style={{
                  padding: "12px 16px",
                  borderRadius: msg.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                  background: msg.role === "user" ? `linear-gradient(135deg,rgba(255,255,255,0.16),rgba(255,255,255,0.07))` : "rgba(var(--tint-rgb),0.05)",
                  border: msg.role === "user" ? `1px solid rgba(${ACCENT_RGB},0.2)` : "1px solid rgba(var(--tint-rgb),0.07)",
                  backdropFilter: "blur(10px)",
                  WebkitBackdropFilter: "blur(10px)",
                }}
              >
                {msg.role === "ai" && (
                  <div style={{ marginBottom: 6 }}>
                    <ModeTag mode={msg.mode} />
                  </div>
                )}
                <div style={{ fontSize: 14, lineHeight: 1.65, color: msg.role === "user" ? "rgba(var(--text-rgb),0.9)" : "rgba(var(--text-rgb),0.8)", whiteSpace: "pre-wrap" }}>
                  {msg.text}
                  {msg.streaming && msg.text === "" ? "…" : ""}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div style={{ display: "flex", gap: 10, alignItems: "flex-end", maxWidth: "80%" }}>
              <div style={{ width: 30, height: 30, borderRadius: "50%", flexShrink: 0, background: `linear-gradient(135deg,rgba(255,255,255,0.2),rgba(255,255,255,0.08))`, border: `1px solid rgba(255,255,255,0.25)`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <BrandLogo size={18} />
              </div>
              <div style={{ padding: "12px 18px", borderRadius: "18px 18px 18px 4px", background: "rgba(var(--tint-rgb),0.05)", border: "1px solid rgba(var(--tint-rgb),0.07)" }}>
                <TypingDots />
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Input */}
        <div style={{ padding: isMobile ? "12px 16px 20px" : "16px 24px 20px", flexShrink: 0 }}>
          <div style={{ display: "flex", alignItems: "flex-end", gap: 10, padding: "12px 12px 12px 18px", borderRadius: 18, ...glass(0.06) }}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  send()
                }
              }}
              placeholder={`Message in ${currentMode.label} mode · ${currentPersona.label}…`}
              rows={1}
              style={{ flex: 1, background: "none", border: "none", outline: "none", color: "var(--text-color)", fontSize: 14, lineHeight: 1.6, resize: "none", maxHeight: 140, overflowY: "auto" }}
            />
            <button
              onClick={send}
              disabled={!input.trim() || loading}
              style={{
                width: 42,
                height: 42,
                borderRadius: 12,
                flexShrink: 0,
                ...(input.trim() && !loading
                  ? {
                      background: `linear-gradient(155deg,${currentMode.color}44,${currentMode.color}18)`,
                      backdropFilter: "blur(20px) saturate(200%)",
                      WebkitBackdropFilter: "blur(20px) saturate(200%)",
                      border: "1px solid rgba(var(--tint-rgb),0.28)",
                      boxShadow: `inset 0 1.5px 0 rgba(var(--tint-rgb),0.5), 0 4px 16px ${currentMode.color}33`,
                      cursor: "pointer",
                    }
                  : { background: "rgba(var(--tint-rgb),0.05)", border: "1px solid rgba(var(--tint-rgb),0.08)", cursor: "default" }),
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                transition: "all 0.25s",
              }}
            >
              <Ic.send s={15} c={input.trim() && !loading ? "#fff" : "rgba(var(--tint-rgb),0.3)"} />
            </button>
          </div>
          <div style={{ textAlign: "center", marginTop: 8, fontSize: 11, color: "rgba(var(--tint-rgb),0.18)" }}>cybersh.ai · local model · 100% offline</div>
        </div>
      </main>

      {/* Panels */}
      {activePanel === "profile" && <ProfilePanel user={user} onClose={() => setActivePanel(null)} />}
      {activePanel === "settings" && <SettingsPanel onClose={() => setActivePanel(null)} />}
      {activePanel === "theme" && <ThemePanel onClose={() => setActivePanel(null)} mode={mode} setMode={setMode} />}
      {activePanel === "shortcuts" && <ShortcutsPanel onClose={() => setActivePanel(null)} />}
      {activePanel === "help" && <HelpPanel onClose={() => setActivePanel(null)} />}
      {activePanel === "tools" && <ToolsPanel onClose={() => setActivePanel(null)} onSendCommand={(cmd) => { setInput(cmd); setActivePanel(null); inputRef.current?.focus() }} />}
      {activePanel === "memory" && <MemoryPanel onClose={() => setActivePanel(null)} />}
      {activePanel === "goals" && <GoalsPanel onClose={() => setActivePanel(null)} />}
    </div>
  )
}
