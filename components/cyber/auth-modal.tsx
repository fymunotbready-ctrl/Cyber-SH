"use client"

import { useState } from "react"
import { Ic } from "./icons"
import { liquidGlass, glassModal } from "./data"

export function AuthModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: () => void }) {
  const [email, setEmail] = useState("")
  const [pass, setPass] = useState("")
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState("")

  const handleGH = () => {
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      onSuccess()
    }, 1400)
  }

  const handleSubmit = () => {
    if (!email || !pass) {
      setErr("Please fill in both fields.")
      return
    }
    setErr("")
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      onSuccess()
    }, 1200)
  }

  const fieldStyle = {
    width: "100%",
    padding: "11px 14px",
    borderRadius: 11,
    background: "rgba(var(--tint-rgb),0.05)",
    border: "1px solid rgba(var(--tint-rgb),0.09)",
    color: "var(--text-color)",
    fontSize: 14,
    outline: "none",
    transition: "border 0.2s",
    boxSizing: "border-box" as const,
  }

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 500,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "rgba(4,4,12,0.75)",
        backdropFilter: "blur(8px)",
        WebkitBackdropFilter: "blur(8px)",
        animation: "cyberFadeIn 0.25s ease",
        padding: 20,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <div
        style={{
          width: 420,
          maxWidth: "100%",
          borderRadius: 22,
          position: "relative",
          animation: "cyberSlideUp 0.3s cubic-bezier(0.34,1.56,0.64,1)",
          ...glassModal,
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: 44,
            height: 44,
            background:
              "linear-gradient(225deg, rgba(var(--tint-rgb),0.1) 0%, rgba(var(--tint-rgb),0.02) 50%, transparent 50%)",
            borderRadius: "0 22px 0 0",
            pointerEvents: "none",
          }}
        />
        <button
          onClick={onClose}
          aria-label="Close"
          style={{
            position: "absolute",
            top: 14,
            right: 14,
            width: 28,
            height: 28,
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
            background: "rgba(var(--tint-rgb),0.07)",
            color: "rgba(var(--tint-rgb),0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Ic.close s={13} />
        </button>

        <div style={{ padding: "40px 36px 36px" }}>
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: "50%",
              margin: "0 auto 20px",
              background: "rgba(var(--tint-rgb),0.08)",
              border: "1px solid rgba(var(--tint-rgb),0.1)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Ic.person s={26} c="rgba(var(--tint-rgb),0.5)" />
          </div>

          <h2 style={{ textAlign: "center", fontSize: 22, fontWeight: 700, color: "var(--text-color)", marginBottom: 7, letterSpacing: "-0.01em" }}>
            Welcome Back
          </h2>
          <p style={{ textAlign: "center", fontSize: 13, color: "rgba(var(--text-rgb),0.4)", marginBottom: 28, lineHeight: 1.5 }}>
            Sign in to access your Cyber-SH workspace
          </p>

          <button
            onClick={handleGH}
            disabled={loading}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 10,
              width: "100%",
              padding: "11px 20px",
              borderRadius: 12,
              marginBottom: 20,
              fontSize: 14,
              fontWeight: 600,
              cursor: "pointer",
              background: "rgba(var(--tint-rgb),0.08)",
              color: "var(--text-color)",
              border: "1px solid rgba(var(--tint-rgb),0.12)",
              transition: "all 0.2s",
            }}
          >
            <Ic.github s={18} c="var(--text-color)" />
            {loading ? "Connecting…" : "Continue with GitHub"}
          </button>

          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
            <div style={{ flex: 1, height: 1, background: "rgba(var(--tint-rgb),0.08)" }} />
            <span style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.28)", letterSpacing: "0.04em" }}>or</span>
            <div style={{ flex: 1, height: 1, background: "rgba(var(--tint-rgb),0.08)" }} />
          </div>

          <label style={{ display: "block", fontSize: 12, fontWeight: 500, color: "rgba(var(--text-rgb),0.55)", marginBottom: 7 }}>
            Email Address
          </label>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            style={{ ...fieldStyle, marginBottom: 16 }}
            onFocus={(e) => (e.target.style.borderColor = "rgba(0,212,255,0.4)")}
            onBlur={(e) => (e.target.style.borderColor = "rgba(var(--tint-rgb),0.09)")}
          />

          <label style={{ display: "block", fontSize: 12, fontWeight: 500, color: "rgba(var(--text-rgb),0.55)", marginBottom: 7 }}>
            Password
          </label>
          <div style={{ position: "relative", marginBottom: err ? 12 : 20 }}>
            <input
              value={pass}
              onChange={(e) => setPass(e.target.value)}
              type={showPw ? "text" : "password"}
              placeholder="••••••••••"
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              style={{ ...fieldStyle, padding: "11px 42px 11px 14px" }}
              onFocus={(e) => (e.target.style.borderColor = "rgba(0,212,255,0.4)")}
              onBlur={(e) => (e.target.style.borderColor = "rgba(var(--tint-rgb),0.09)")}
            />
            <button
              onClick={() => setShowPw(!showPw)}
              aria-label={showPw ? "Hide password" : "Show password"}
              style={{
                position: "absolute",
                right: 12,
                top: "50%",
                transform: "translateY(-50%)",
                background: "none",
                border: "none",
                cursor: "pointer",
                padding: 2,
                color: "rgba(var(--tint-rgb),0.3)",
                display: "flex",
              }}
            >
              {showPw ? <Ic.eyeOff s={16} /> : <Ic.eye s={16} />}
            </button>
          </div>

          {err && (
            <div
              style={{
                fontSize: 12,
                color: "#ff453a",
                marginBottom: 14,
                padding: "8px 12px",
                background: "rgba(255,69,58,0.1)",
                borderRadius: 8,
                border: "1px solid rgba(255,69,58,0.2)",
              }}
            >
              {err}
            </div>
          )}

          <div style={{ textAlign: "right", marginBottom: 20 }}>
            <button style={{ background: "none", border: "none", cursor: "pointer", fontSize: 12, color: "rgba(0,212,255,0.7)", padding: 0 }}>
              Forgot Password?
            </button>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="lg-btn"
            style={{
              ...liquidGlass("0,212,255", "md"),
              width: "100%",
              borderRadius: 12,
              opacity: loading ? 0.5 : 1,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>

          <p style={{ textAlign: "center", fontSize: 13, color: "rgba(var(--tint-rgb),0.3)", marginTop: 20, marginBottom: 0 }}>
            {"Don't have an account yet? "}
            <button style={{ background: "none", border: "none", cursor: "pointer", fontSize: 13, fontWeight: 600, color: "rgba(var(--text-rgb),0.75)", padding: 0 }}>
              Sign up
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}
