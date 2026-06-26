"use client"

import { useState } from "react"
import { Ic } from "./icons"
import { liquidGlass, glassModal, ACCENT_RGB, BASE_URL, apiFetch } from "./lib"

export function AuthModal({ onClose, onSuccess }: { onClose: () => void; onSuccess: (name: string) => void }) {
  const [email, setEmail] = useState("")
  const [pass, setPass] = useState("")
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState("")
  const [isSignup, setIsSignup] = useState(false)

  // GitHub OAuth — ask the backend for the redirect URL, then send the
  // browser there. Supabase will bounce the user back to your site with
  // a ?code=... param once they approve, which your callback page (or
  // landing logic) should exchange via /auth/github/callback.
  const handleGH = async () => {
    if (!BASE_URL) {
      setErr("Backend not configured. Set NEXT_PUBLIC_CYBERSH_API.")
      return
    }
    setErr("")
    setLoading(true)
    try {
      const redirectTo = typeof window !== "undefined" ? window.location.origin : ""
      const res = await apiFetch(`/auth/github?redirect_to=${encodeURIComponent(redirectTo)}`)
      const data = await res.json()
      if (data.url) {
        window.location.href = data.url
        return
      }
      throw new Error("No redirect URL returned")
    } catch (e) {
      setLoading(false)
      setErr(e instanceof Error ? e.message : "GitHub sign-in failed.")
    }
  }

  // Email/password login or signup against the real backend.
  const handleSubmit = async () => {
    if (!email || !pass) {
      setErr("Please fill in both fields.")
      return
    }
    if (!BASE_URL) {
      setErr("Backend not configured. Set NEXT_PUBLIC_CYBERSH_API.")
      return
    }
    setErr("")
    setLoading(true)
    try {
      const path = isSignup ? "/auth/signup" : "/auth/login"
      const res = await apiFetch(path, {
        method: "POST",
        body: JSON.stringify({ email, password: pass }),
      })
      const data = await res.json()

      if (isSignup) {
        // Signup typically requires email confirmation — no session yet.
        setLoading(false)
        setErr("")
        onSuccess(email.split("@")[0] || "cybersh.ai")
        return
      }

      if (data.access_token) {
        localStorage.setItem("cybersh_access_token", data.access_token)
        localStorage.setItem("cybersh_refresh_token", data.refresh_token || "")
      }
      setLoading(false)
      onSuccess(data.user?.email?.split("@")[0] || email.split("@")[0] || "cybersh.ai")
    } catch (e) {
      setLoading(false)
      setErr(e instanceof Error ? e.message : "Sign in failed. Check your email and password.")
    }
  }

  const inputStyle = {
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
        zIndex: 600,
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
      <div style={{ width: "100%", maxWidth: 420, borderRadius: 22, position: "relative", animation: "cyberSlideUp 0.3s cubic-bezier(0.34,1.56,0.64,1)", ...glassModal }}>
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: 44,
            height: 44,
            background: "linear-gradient(225deg, rgba(var(--tint-rgb),0.1) 0%, rgba(var(--tint-rgb),0.02) 50%, transparent 50%)",
            borderRadius: "0 22px 0 0",
            pointerEvents: "none",
          }}
        />
        <button
          onClick={onClose}
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
            {isSignup ? "Create Account" : "Welcome Back"}
          </h2>
          <p style={{ textAlign: "center", fontSize: 13, color: "rgba(var(--text-rgb),0.4)", marginBottom: 28, lineHeight: 1.5 }}>
            {isSignup ? "Sign up to start using Cyber-SH" : "Sign in to access your Cyber-SH workspace"}
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
            }}
          >
            <Ic.github s={18} />
            {loading ? "Connecting…" : "Continue with GitHub"}
          </button>

          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
            <div style={{ flex: 1, height: 1, background: "rgba(var(--tint-rgb),0.08)" }} />
            <span style={{ fontSize: 12, color: "rgba(var(--tint-rgb),0.28)", letterSpacing: "0.04em" }}>or</span>
            <div style={{ flex: 1, height: 1, background: "rgba(var(--tint-rgb),0.08)" }} />
          </div>

          <label style={{ display: "block", fontSize: 12, fontWeight: 500, color: "rgba(var(--text-rgb),0.55)", marginBottom: 7 }}>Email Address</label>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            style={{ ...inputStyle, marginBottom: 16 }}
            onFocus={(e) => (e.target.style.borderColor = `rgba(${ACCENT_RGB},0.4)`)}
            onBlur={(e) => (e.target.style.borderColor = "rgba(var(--tint-rgb),0.09)")}
          />

          <label style={{ display: "block", fontSize: 12, fontWeight: 500, color: "rgba(var(--text-rgb),0.55)", marginBottom: 7 }}>Password</label>
          <div style={{ position: "relative", marginBottom: err ? 12 : 20 }}>
            <input
              value={pass}
              onChange={(e) => setPass(e.target.value)}
              type={showPw ? "text" : "password"}
              placeholder="••••••••••"
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              style={{ ...inputStyle, padding: "11px 42px 11px 14px" }}
              onFocus={(e) => (e.target.style.borderColor = `rgba(${ACCENT_RGB},0.4)`)}
              onBlur={(e) => (e.target.style.borderColor = "rgba(var(--tint-rgb),0.09)")}
            />
            <button
              onClick={() => setShowPw(!showPw)}
              style={{ position: "absolute", right: 12, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", padding: 2, color: "rgba(var(--tint-rgb),0.3)", display: "flex" }}
            >
              {showPw ? <Ic.eyeOff s={16} /> : <Ic.eye s={16} />}
            </button>
          </div>

          {err && (
            <div style={{ fontSize: 12, color: "#ff453a", marginBottom: 14, padding: "8px 12px", background: "rgba(255,69,58,0.1)", borderRadius: 8, border: "1px solid rgba(255,69,58,0.2)" }}>
              {err}
            </div>
          )}

          <div style={{ textAlign: "right", marginBottom: 20 }}>
            <button style={{ background: "none", border: "none", cursor: "pointer", fontSize: 12, color: `rgba(${ACCENT_RGB},0.8)`, padding: 0 }}>Forgot Password?</button>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="lg-btn"
            style={{ ...liquidGlass(ACCENT_RGB, "md"), width: "100%", borderRadius: 12, opacity: loading ? 0.5 : 1, cursor: loading ? "not-allowed" : "pointer" }}
          >
            {loading ? (isSignup ? "Creating account…" : "Signing in…") : isSignup ? "Sign up" : "Sign in"}
          </button>

          <p style={{ textAlign: "center", fontSize: 13, color: "rgba(var(--tint-rgb),0.3)", marginTop: 20, marginBottom: 0 }}>
            {isSignup ? (
              <>
                Already have an account?{" "}
                <button
                  onClick={() => {
                    setIsSignup(false)
                    setErr("")
                  }}
                  style={{ background: "none", border: "none", cursor: "pointer", fontSize: 13, fontWeight: 600, color: "rgba(var(--text-rgb),0.75)", padding: 0 }}
                >
                  Sign in
                </button>
              </>
            ) : (
              <>
                Don&apos;t have an account yet?{" "}
                <button
                  onClick={() => {
                    setIsSignup(true)
                    setErr("")
                  }}
                  style={{ background: "none", border: "none", cursor: "pointer", fontSize: 13, fontWeight: 600, color: "rgba(var(--text-rgb),0.75)", padding: 0 }}
                >
                  Sign up
                </button>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  )
}
