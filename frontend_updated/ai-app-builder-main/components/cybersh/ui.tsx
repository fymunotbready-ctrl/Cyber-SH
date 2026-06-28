"use client"

import type { ReactNode } from "react"
import { Ic } from "./icons"
import { MODES, glassModal, ACCENT_HEX } from "./lib"

export function ModeTag({ mode }: { mode: string }) {
  const m = MODES.find((x) => x.id === mode)
  if (!m) return null
  const Icon = m.Icon
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 4,
        padding: "1px 8px",
        borderRadius: 6,
        fontSize: 10,
        fontWeight: 600,
        letterSpacing: "0.04em",
        background: `${m.color}22`,
        color: m.color,
        border: `1px solid ${m.color}44`,
      }}
    >
      <Icon s={10} c={m.color} /> {m.label.toUpperCase()}
    </span>
  )
}

export function TypingDots() {
  return (
    <div style={{ display: "flex", gap: 4, alignItems: "center", padding: "4px 0" }}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            width: 6,
            height: 6,
            borderRadius: "50%",
            background: "rgba(var(--accent-rgb),0.6)",
            animation: `cyberDot 1.2s ${i * 0.2}s ease-in-out infinite`,
          }}
        />
      ))}
    </div>
  )
}

type PanelKey = "profile" | "settings" | "theme" | "shortcuts" | "help"

export function ProfileMenu({
  user,
  onClose,
  onLogout,
  onOpenPanel,
}: {
  user: { name: string }
  onClose: () => void
  onLogout: () => void
  onOpenPanel: (p: PanelKey) => void
}) {
  const items: (
    | { Icon: typeof Ic.person; label: string; action: () => void; hasArrow?: boolean; danger?: boolean }
    | null
  )[] = [
    { Icon: Ic.person, label: "Profile", action: () => { onClose(); onOpenPanel("profile") } },
    { Icon: Ic.settings, label: "Settings", action: () => { onClose(); onOpenPanel("settings") } },
    { Icon: Ic.theme, label: "Theme", action: () => { onClose(); onOpenPanel("theme") }, hasArrow: true },
    null,
    { Icon: Ic.keyboard, label: "Keyboard shortcuts", action: () => { onClose(); onOpenPanel("shortcuts") } },
    { Icon: Ic.help, label: "Help center", action: () => { onClose(); onOpenPanel("help") } },
    { Icon: Ic.logout, label: "Log out", action: onLogout, danger: true },
  ]
  return (
    <div style={{ position: "absolute", top: 52, right: 0, width: 230, borderRadius: 16, overflow: "hidden", zIndex: 200, ...glassModal }}>
      <div style={{ padding: "6px 6px" }}>
        {items.map((item, i) =>
          item === null ? (
            <div key={i} style={{ height: 1, background: "rgba(var(--tint-rgb),0.07)", margin: "4px 10px" }} />
          ) : (
            <button
              key={i}
              onClick={item.action}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 11,
                width: "100%",
                padding: "10px 12px",
                borderRadius: 10,
                border: "none",
                cursor: "pointer",
                background: "transparent",
                textAlign: "left",
                color: item.danger ? "#ff453a" : "rgba(var(--text-rgb),0.85)",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.7")}
              onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
            >
              <item.Icon s={17} c={item.danger ? "#ff453a" : "rgba(var(--text-rgb),0.7)"} />
              <span style={{ fontSize: 14, fontWeight: 400, flex: 1 }}>{item.label}</span>
              {item.hasArrow && <Ic.chevR s={13} c="rgba(var(--tint-rgb),0.3)" />}
            </button>
          ),
        )}
      </div>
    </div>
  )
}

export function PanelModal({ title, icon, onClose, children }: { title: string; icon?: ReactNode; onClose: () => void; children: ReactNode }) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 500,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "rgba(0,0,0,0.6)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        animation: "cyberFadeIn 0.2s ease",
        padding: 20,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 460,
          borderRadius: 22,
          overflow: "hidden",
          ...glassModal,
          animation: "cyberSlideUp 0.25s ease",
          maxHeight: "85vh",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "20px 24px 16px",
            borderBottom: "1px solid rgba(var(--tint-rgb),0.07)",
          }}
        >
          <span style={{ display: "flex", alignItems: "center", gap: 9, fontSize: 16, fontWeight: 700, color: "var(--text-color)" }}>
            {icon}
            {title}
          </span>
          <button
            onClick={onClose}
            style={{
              background: "rgba(var(--tint-rgb),0.07)",
              border: "none",
              cursor: "pointer",
              width: 30,
              height: 30,
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "rgba(var(--tint-rgb),0.6)",
            }}
          >
            <Ic.close s={14} />
          </button>
        </div>
        <div style={{ overflowY: "auto", padding: "20px 24px 24px", flex: 1 }}>{children}</div>
      </div>
    </div>
  )
}

export function SettingRow({ label, desc, children }: { label: string; desc?: string; children: ReactNode }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "14px 0",
        borderBottom: "1px solid rgba(var(--tint-rgb),0.05)",
      }}
    >
      <div>
        <div style={{ fontSize: 14, fontWeight: 500, color: "rgba(var(--text-rgb),0.9)" }}>{label}</div>
        {desc && <div style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.35)", marginTop: 2 }}>{desc}</div>}
      </div>
      {children}
    </div>
  )
}

export function Toggle({ on, onToggle, color = ACCENT_HEX }: { on: boolean; onToggle: () => void; color?: string }) {
  return (
    <div
      onClick={onToggle}
      style={{
        width: 44,
        height: 26,
        borderRadius: 13,
        cursor: "pointer",
        background: on ? color : "rgba(var(--tint-rgb),0.12)",
        transition: "background 0.25s",
        position: "relative",
        flexShrink: 0,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 3,
          left: on ? 21 : 3,
          width: 20,
          height: 20,
          borderRadius: "50%",
          background: "#fff",
          boxShadow: on ? `0 0 8px ${color}88` : "0 1px 4px rgba(0,0,0,0.4)",
          transition: "left 0.25s cubic-bezier(0.4,0,0.2,1)",
        }}
      />
    </div>
  )
}
