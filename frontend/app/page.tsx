"use client"

import { useEffect, useState } from "react"
import { Splash } from "@/components/cybersh/splash"
import { Landing } from "@/components/cybersh/landing"
import { Dashboard } from "@/components/cybersh/dashboard"
import { AuthModal } from "@/components/cybersh/auth-modal"

type Screen = "splash" | "landing" | "dashboard"
type Mode = "dark" | "light"

export default function Page() {
  const [screen, setScreen] = useState<Screen>("splash")
  const [splashFading, setSplashFading] = useState(false)
  const [showAuth, setShowAuth] = useState(false)
  const [user, setUser] = useState<{ name: string } | null>(null)
  const [mode, setMode] = useState<Mode>("dark")

  // Splash → Landing sequence
  useEffect(() => {
    const t1 = setTimeout(() => setSplashFading(true), 2900)
    const t2 = setTimeout(() => setScreen("landing"), 3600)
    return () => {
      clearTimeout(t1)
      clearTimeout(t2)
    }
  }, [])

  // GitHub OAuth callback — Supabase redirects back here with ?code=...
  // after the user approves on GitHub. Exchange it for a session.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const code = params.get("code")
    if (!code) return

    const BASE_URL = process.env.NEXT_PUBLIC_CYBERSH_API || ""
    if (!BASE_URL) return

    ;(async () => {
      try {
        const res = await fetch(`${BASE_URL}/auth/github/callback`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, redirect_to: window.location.origin }),
        })
        const data = await res.json()
        if (data.access_token) {
          localStorage.setItem("cybersh_access_token", data.access_token)
          localStorage.setItem("cybersh_refresh_token", data.refresh_token || "")
        }
        // Clean the ?code=... out of the URL bar
        window.history.replaceState({}, "", window.location.pathname)
        handleAuthSuccess(data.user?.email?.split("@")[0] || data.user?.user_metadata?.user_name || "cybersh.ai")
      } catch {
        window.history.replaceState({}, "", window.location.pathname)
      }
    })()
  }, [])

  const handleAuthSuccess = (name: string) => {
    setUser({ name: name || "cybersh.ai" })
    setShowAuth(false)
    setScreen("dashboard")
  }

  const isDark = mode === "dark"

  return (
    <>
      {/* Dynamic iOS dark/light theme tokens + liquid-glass animation system */}
      <style>{`
        :root {
          --page-bg: ${isDark ? "#000000" : "#f5f5f7"};
          --panel-bg: ${isDark ? "rgba(14,14,16,0.72)" : "rgba(255,255,255,0.78)"};
          --sidebar-bg: ${isDark ? "rgba(8,8,10,0.8)" : "rgba(255,255,255,0.85)"};
          --text-color: ${isDark ? "#ffffff" : "#1d1d1f"};
          --text-rgb: ${isDark ? "255,255,255" : "29,29,31"};
          --tint-rgb: ${isDark ? "255,255,255" : "0,0,0"};
          --muted-rgb: ${isDark ? "134,134,139" : "110,110,115"};
          --accent-rgb: 255,255,255;
        }
        :root { --ease-ios: cubic-bezier(0.34,1.56,0.64,1); --ease-smooth: cubic-bezier(0.22,1,0.36,1); }
        * { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
        html { -webkit-text-size-adjust: 100%; }
        html, body { background: var(--page-bg, #1C1C1E) !important; transition: background 0.3s var(--ease-smooth); overscroll-behavior: none; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(var(--tint-rgb),0.12); border-radius: 6px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(var(--tint-rgb),0.22); }
        * { scrollbar-width: thin; scrollbar-color: rgba(var(--tint-rgb),0.12) transparent; }
        input::placeholder, textarea::placeholder { color: rgba(var(--text-rgb),0.25); }

        /* buttery, touch-friendly interactions everywhere */
        button, a, [role="button"], summary, label[for], input[type="checkbox"], input[type="radio"] {
          -webkit-tap-highlight-color: transparent !important;
          outline: none !important;
          -webkit-user-select: none; user-select: none;
          touch-action: manipulation;
        }
        button:focus, a:focus, button:focus-visible, a:focus-visible { outline: none !important; box-shadow: none !important; }
        button, a, [role="button"] {
          transition: transform 0.32s var(--ease-ios), opacity 0.22s ease, filter 0.22s ease, background 0.25s ease, box-shadow 0.3s var(--ease-smooth), border-color 0.25s ease;
          will-change: transform;
        }
        /* gentle, springy press feedback for tappable controls */
        button:active, [role="button"]:active { transform: scale(0.955); filter: brightness(0.96); }
        @media (hover: hover) {
          button:not(:disabled):hover, [role="button"]:hover { filter: brightness(1.06); }
        }
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
        }

        @keyframes cyberPulse { 0%,100% { opacity: 1 } 50% { opacity: 0.35 } }
        @keyframes cyberFloat { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-8px) } }
        @keyframes cyberFadeIn { from { opacity: 0 } to { opacity: 1 } }
        @keyframes cyberSlideUp { from { opacity: 0; transform: translateY(24px) scale(0.96) } to { opacity: 1; transform: none } }
        @keyframes cyberDot { 0%,80%,100% { transform: scale(0.6); opacity: 0.4 } 40% { transform: scale(1); opacity: 1 } }
        @keyframes lgShimmer { 0% { transform: translateX(-120%) skewX(-20deg) } 100% { transform: translateX(260%) skewX(-20deg) } }

        /* intro animations */
        @keyframes logoReveal {
          0%   { opacity: 0; transform: scale(0.6) translateY(14px); filter: blur(14px) brightness(1.4); }
          55%  { opacity: 1; filter: blur(0px) brightness(1.12); }
          100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0px) brightness(1); }
        }
        /* springy pop-up entrance for the intro mark */
        @keyframes logoPop {
          0%   { opacity: 0; transform: scale(0.2) translateY(46px) rotate(-7deg); filter: blur(20px) brightness(1.7); }
          45%  { opacity: 1; transform: scale(1.14) translateY(-7px) rotate(1.6deg); filter: blur(0px) brightness(1.2); }
          68%  { transform: scale(0.95) translateY(3px) rotate(-0.7deg); }
          84%  { transform: scale(1.035) translateY(-1px) rotate(0.25deg); }
          100% { opacity: 1; transform: scale(1) translateY(0) rotate(0deg); filter: blur(0px) brightness(1); }
        }
        @keyframes ringBurst {
          0%   { transform: scale(0.35); opacity: 0; }
          30%  { opacity: 0.85; }
          100% { transform: scale(2.6); opacity: 0; }
        }
        @keyframes cyberRing { 0%,100% { transform: scale(0.92); opacity: 0.7 } 50% { transform: scale(1.12); opacity: 1 } }
        @keyframes loadSweep { 0% { transform: translateX(-130%) } 100% { transform: translateX(360%) } }

        .lg-btn { position: relative; overflow: hidden; }
        .lg-btn::before {
          content: ''; position: absolute; top: 0; left: 0; right: 0; height: 44%;
          background: linear-gradient(180deg, rgba(255,255,255,0.34) 0%, rgba(255,255,255,0) 100%);
          border-radius: inherit; pointer-events: none; z-index: 1;
        }
        .lg-btn::after {
          content: ''; position: absolute; top: -10%; left: 0; width: 38%; height: 120%;
          background: linear-gradient(105deg, transparent 20%, rgba(255,255,255,0.30) 50%, transparent 80%);
          animation: lgShimmer 3.8s ease-in-out infinite; pointer-events: none; z-index: 2;
        }
        .lg-btn:hover { transform: translateY(-2px) scale(1.035); filter: brightness(1.14); }
        .lg-btn:active { transform: translateY(0px) scale(0.95); filter: brightness(0.92); }
      `}</style>

      {screen === "splash" && <Splash done={splashFading} />}
      {screen === "landing" && <Landing onGetStarted={() => setShowAuth(true)} />}
      {screen === "dashboard" && user && (
        <Dashboard
          user={user}
          onLogout={() => {
            setUser(null)
            setScreen("landing")
          }}
          mode={mode}
          setMode={setMode}
        />
      )}
      {showAuth && <AuthModal onClose={() => setShowAuth(false)} onSuccess={handleAuthSuccess} />}
    </>
  )
}
