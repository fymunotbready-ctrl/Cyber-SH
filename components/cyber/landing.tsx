"use client"

import { useState } from "react"
import { Ic } from "./icons"
import { MODES, FEATURES, glass, liquidGlass, liquidGlassSm, BrandLogo } from "./data"

export function Splash({ done }: { done: boolean }) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--page-bg, #1C1C1E)",
        transition: "opacity 0.6s ease, transform 0.6s ease",
        opacity: done ? 0 : 1,
        transform: done ? "scale(1.04)" : "scale(1)",
        pointerEvents: done ? "none" : "auto",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          position: "absolute",
          width: 400,
          height: 400,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(0,212,255,0.12) 0%, transparent 70%)",
          filter: "blur(60px)",
          animation: "cyberPulse 3s ease-in-out infinite",
        }}
      />
      <div style={{ position: "relative", animation: "cyberFloat 2s ease-in-out infinite" }}>
        <BrandLogo size={80} />
      </div>
      <div
        style={{
          marginTop: 20,
          fontSize: 13,
          fontWeight: 500,
          letterSpacing: "0.25em",
          color: "rgba(0,212,255,0.7)",
          textTransform: "uppercase",
          animation: "cyberFadeIn 1s 0.5s both",
        }}
      >
        CYBER — SH
      </div>
      <div
        style={{
          marginTop: 8,
          fontSize: 11,
          color: "rgba(var(--tint-rgb),0.3)",
          letterSpacing: "0.08em",
          animation: "cyberFadeIn 1s 0.8s both",
        }}
      >
        Your personal offline AI
      </div>
    </div>
  )
}

export function Landing({ onGetStarted }: { onGetStarted: () => void }) {
  const [hovered, setHovered] = useState<number | null>(null)
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "var(--page-bg, #1C1C1E)",
        color: "var(--text-color)",
        overflowX: "hidden",
      }}
    >
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
            background: "radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 65%)",
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
            background: "radial-gradient(circle, rgba(94,92,230,0.08) 0%, transparent 65%)",
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
            background: "radial-gradient(circle, rgba(48,209,88,0.06) 0%, transparent 65%)",
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
          padding: "16px 40px",
          ...glass(0.04),
          borderTop: "none",
          borderLeft: "none",
          borderRight: "none",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <BrandLogo size={32} />
          <span style={{ fontSize: 16, fontWeight: 600, letterSpacing: "0.06em", color: "var(--text-color)" }}>
            CYBER<span style={{ color: "#00d4ff" }}>SH</span>
          </span>
        </div>
        <button onClick={onGetStarted} className="lg-btn" style={liquidGlassSm()}>
          Get Started
        </button>
      </nav>

      {/* Hero */}
      <section style={{ maxWidth: 900, margin: "0 auto", padding: "100px 40px 80px", textAlign: "center", position: "relative" }}>
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
            background: "rgba(0,212,255,0.1)",
            color: "#00d4ff",
            border: "1px solid rgba(0,212,255,0.25)",
          }}
        >
          <div
            style={{
              width: 5,
              height: 5,
              borderRadius: "50%",
              background: "#00d4ff",
              boxShadow: "0 0 6px #00d4ff",
              animation: "cyberPulse 2s infinite",
            }}
          />
          v1.4 — Security Release
        </div>

        <h1 style={{ fontSize: "clamp(42px,7vw,80px)", fontWeight: 700, lineHeight: 1.05, letterSpacing: "-0.03em", margin: "0 0 24px" }}>
          Your Personal
          <br />
          <span
            style={{
              background: "linear-gradient(135deg,#00d4ff 0%,#7b5eff 60%,#30d158 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Offline AI
          </span>
        </h1>
        <p style={{ fontSize: 18, lineHeight: 1.7, color: "rgba(var(--text-rgb),0.55)", maxWidth: 520, margin: "0 auto 48px", fontWeight: 400 }}>
          Runs entirely on your computer. No cloud, no subscriptions, no one watching. Five modes. Persistent memory. Full
          security toolkit.
        </p>

        <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
          <button
            onClick={onGetStarted}
            className="lg-btn"
            style={{ ...liquidGlass("0,212,255", "lg"), fontSize: 15, display: "inline-flex", alignItems: "center", gap: 9 }}
          >
            <Ic.chat s={18} c="#fff" />
            Talk 2 Me
          </button>
        </div>

        {/* Mode pills */}
        <div style={{ display: "flex", gap: 8, justifyContent: "center", flexWrap: "wrap", marginTop: 52 }}>
          {MODES.map((m) => (
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
                background: `${m.color}14`,
                color: m.color,
                border: `1px solid ${m.color}33`,
              }}
            >
              <m.Icon s={13} c={m.color} />
              {m.label}
            </div>
          ))}
        </div>
      </section>

      {/* Features grid */}
      <section style={{ maxWidth: 960, margin: "0 auto 100px", padding: "0 40px" }}>
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <h2 style={{ fontSize: 32, fontWeight: 700, letterSpacing: "-0.02em", marginBottom: 12 }}>Everything in one place</h2>
          <p style={{ fontSize: 15, color: "rgba(var(--text-rgb),0.45)" }}>One command. Five modes. No setup after the first run.</p>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))", gap: 16 }}>
          {FEATURES.map((f, i) => (
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
                <f.Icon s={22} c={f.color} />
              </div>
              <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 6 }}>{f.title}</div>
              <div style={{ fontSize: 13, lineHeight: 1.65, color: "rgba(var(--text-rgb),0.45)" }}>{f.body}</div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Banner */}
      <section style={{ maxWidth: 760, margin: "0 auto 80px", padding: "0 40px" }}>
        <div
          style={{
            padding: "48px",
            borderRadius: 24,
            textAlign: "center",
            background: "linear-gradient(135deg,rgba(0,212,255,0.1),rgba(123,94,255,0.1))",
            border: "1px solid rgba(var(--tint-rgb),0.09)",
            boxShadow: "0 24px 64px rgba(0,0,0,0.4)",
          }}
        >
          <div style={{ marginBottom: 12, display: "inline-flex" }}>
            <Ic.offline s={32} c="#00d4ff" />
          </div>
          <h2 style={{ fontSize: 28, fontWeight: 700, letterSpacing: "-0.02em", marginBottom: 12 }}>No cloud. Ever.</h2>
          <p style={{ fontSize: 15, color: "rgba(var(--text-rgb),0.5)", maxWidth: 400, margin: "0 auto 28px" }}>
            Your queries never leave your machine. Not even for model downloads after setup.
          </p>
          <button
            onClick={onGetStarted}
            className="lg-btn"
            style={{ ...liquidGlass("0,212,255", "lg"), fontSize: 14, display: "inline-flex", alignItems: "center", gap: 9 }}
          >
            <Ic.chat s={16} c="#fff" />
            Talk 2 Me
          </button>
        </div>
      </section>

      <footer
        style={{
          textAlign: "center",
          padding: "24px 40px",
          borderTop: "1px solid rgba(var(--tint-rgb),0.06)",
          fontSize: 12,
          color: "rgba(var(--tint-rgb),0.25)",
        }}
      >
        Made by{" "}
        <a href="https://cybersh.ai" style={{ color: "rgba(0,212,255,0.6)", textDecoration: "none" }}>
          cybersh.ai
        </a>{" "}
        · MIT License · v1.4
      </footer>
    </div>
  )
}
