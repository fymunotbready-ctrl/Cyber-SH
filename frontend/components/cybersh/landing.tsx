"use client"

import { useState } from "react"
import { BrandLogo } from "./brand-logo"
import { Ic } from "./icons"
import {
  MODES,
  FEATURES,
  glass,
  liquidGlass,
  liquidGlassSm,
  ACCENT_RGB,
  ACCENT_HEX,
  ACCENT_HEX_2,
} from "./lib"

export function Landing({ onGetStarted }: { onGetStarted: () => void }) {
  const [hovered, setHovered] = useState<number | null>(null)

  return (
    <div style={{ minHeight: "100vh", background: "var(--page-bg)", color: "var(--text-color)", overflowX: "hidden" }}>
      {/* ambient background */}
      <div style={{ position: "fixed", inset: 0, pointerEvents: "none", overflow: "hidden" }}>
        <div
          style={{
            position: "absolute",
            top: "-20%",
            left: "50%",
            transform: "translateX(-50%)",
            width: 800,
            height: 800,
            borderRadius: "50%",
            background: `radial-gradient(circle, rgba(${ACCENT_RGB},0.09) 0%, transparent 65%)`,
            filter: "blur(80px)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: "40%",
            left: "-10%",
            width: 500,
            height: 500,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(255,255,255,0.055) 0%, transparent 65%)",
            filter: "blur(80px)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: "20%",
            right: "-5%",
            width: 400,
            height: 400,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(180,180,190,0.04) 0%, transparent 65%)",
            filter: "blur(70px)",
          }}
        />
      </div>

      {/* Nav */}
      <nav
        style={{
          position: "sticky",
          top: 0,
          zIndex: 50,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "16px 24px",
          ...glass(0.04),
          borderTop: "none",
          borderLeft: "none",
          borderRight: "none",
        }}
      >
        <div style={{ display: "flex", alignItems: "center" }}>
          <BrandLogo size={42} withText />
        </div>
        <button
          onClick={onGetStarted}
          className="lg-btn"
          style={liquidGlassSm()}
          onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.88")}
          onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
        >
          Get Started
        </button>
      </nav>

      {/* Hero */}
      <section style={{ maxWidth: 900, margin: "0 auto", padding: "100px 24px 80px", textAlign: "center", position: "relative" }}>
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 7,
            padding: "5px 14px",
            borderRadius: 20,
            fontSize: 11,
            fontWeight: 600,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            marginBottom: 32,
            background: `rgba(${ACCENT_RGB},0.12)`,
            color: ACCENT_HEX,
            border: `1px solid rgba(${ACCENT_RGB},0.25)`,
          }}
        >
          <div style={{ width: 5, height: 5, borderRadius: "50%", background: ACCENT_HEX, boxShadow: `0 0 6px ${ACCENT_HEX}`, animation: "cyberPulse 2s infinite" }} />
          v1.4 — Security Release
        </div>

        <h1 style={{ fontSize: "clamp(42px,7vw,80px)", fontWeight: 700, lineHeight: 1.05, letterSpacing: "-0.03em", margin: "0 0 24px" }}>
          Your Personal
          <br />
          <span style={{ background: `linear-gradient(135deg,${ACCENT_HEX} 0%,${ACCENT_HEX_2} 100%)`, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            AI Assistant
          </span>
        </h1>
        <p style={{ fontSize: 18, lineHeight: 1.7, color: "rgba(var(--text-rgb),0.55)", maxWidth: 520, margin: "0 auto 48px", fontWeight: 400 }}>
          A smart helper that runs right on your own computer. No sign-up, no fees, and no one watching. It remembers you and helps with almost anything.
        </p>

        <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
          <button
            onClick={onGetStarted}
            className="lg-btn"
            style={{ ...liquidGlass(ACCENT_RGB, "lg"), fontSize: 15 }}
            onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.88")}
            onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
          >
            Start Chatting
          </button>
        </div>

        {/* Mode pills */}
        <div style={{ display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap", marginTop: 52 }}>
          {MODES.map((m) => {
            const Icon = m.Icon
            return (
              <div
                key={m.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 7,
                  padding: "7px 14px",
                  borderRadius: 20,
                  fontSize: 12,
                  fontWeight: 500,
                  letterSpacing: "0.02em",
                  background: "rgba(255,255,255,0.055)",
                  backdropFilter: "blur(24px) saturate(180%)",
                  WebkitBackdropFilter: "blur(24px) saturate(180%)",
                  color: "rgba(255,255,255,0.82)",
                  border: "1px solid rgba(255,255,255,0.12)",
                  boxShadow: "inset 0 1px 0 rgba(255,255,255,0.14)",
                }}
              >
                <Icon s={13} c={m.color} />
                {m.label}
              </div>
            )
          })}
        </div>
      </section>

      {/* Features grid */}
      <section style={{ maxWidth: 960, margin: "0 auto 100px", padding: "0 24px" }}>
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, letterSpacing: "-0.02em", marginBottom: 12 }}>Everything in one place</h2>
          <p style={{ fontSize: 15, color: "rgba(var(--text-rgb),0.45)" }}>Simple to use. Set it up once, then it just works.</p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))", gap: 16 }}>
          {FEATURES.map((f, i) => {
            const Icon = f.Icon
            return (
              <div
                key={i}
                onMouseEnter={() => setHovered(i)}
                onMouseLeave={() => setHovered(null)}
                style={{
                  padding: "28px 24px",
                  borderRadius: 20,
                  ...glass(0.04),
                  transition: "all 0.3s",
                  transform: hovered === i ? "translateY(-4px)" : "none",
                  boxShadow: hovered === i ? `0 16px 48px rgba(0,0,0,0.5), 0 0 0 1px ${f.color}33` : "0 8px 32px rgba(0,0,0,0.35)",
                }}
              >
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginBottom: 16,
                    background: `${f.color}18`,
                    border: `1px solid ${f.color}33`,
                  }}
                >
                  <Icon s={22} c={f.color} />
                </div>
                <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 6 }}>{f.title}</div>
                <div style={{ fontSize: 13, lineHeight: 1.65, color: "rgba(var(--text-rgb),0.45)" }}>{f.body}</div>
              </div>
            )
          })}
        </div>
      </section>

      {/* CTA Banner */}
      <section style={{ maxWidth: 760, margin: "0 auto 80px", padding: "0 24px" }}>
        <div
          style={{
            padding: "48px",
            borderRadius: 24,
            textAlign: "center",
            background: `linear-gradient(135deg,rgba(${ACCENT_RGB},0.08),rgba(${ACCENT_RGB},0.03))`,
            border: "1px solid rgba(var(--tint-rgb),0.09)",
            boxShadow: "0 24px 64px rgba(0,0,0,0.4)",
          }}
        >
          <div style={{ marginBottom: 12, display: "inline-flex" }}>
            <Ic.offline s={32} c={ACCENT_HEX} />
          </div>
          <h2 style={{ fontSize: 28, fontWeight: 700, letterSpacing: "-0.02em", marginBottom: 12 }}>Always private</h2>
          <p style={{ fontSize: 15, color: "rgba(var(--text-rgb),0.5)", maxWidth: 400, margin: "0 auto 28px" }}>
            What you type never leaves your computer. Nothing is sent online once you're set up.
          </p>
          <button onClick={onGetStarted} className="lg-btn" style={{ ...liquidGlass(ACCENT_RGB, "lg"), fontSize: 14 }}>
            Try It Now
          </button>
        </div>
      </section>

      <footer style={{ textAlign: "center", padding: "24px", borderTop: "1px solid rgba(var(--tint-rgb),0.06)", fontSize: 12, color: "rgba(var(--tint-rgb),0.25)" }}>
        Made by <span style={{ color: `rgba(${ACCENT_RGB},0.7)` }}>cybersh.ai</span> · MIT License · v1.4
      </footer>
    </div>
  )
}
