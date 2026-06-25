"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { ChatIcon, CodeIcon, TerminalIcon, LayersIcon, CpuIcon, ArrowRightIcon } from "./icons"

const tabs = [
  { id: "chat", label: "Chat", icon: ChatIcon },
  { id: "code", label: "Vibe Coding", icon: CodeIcon },
  { id: "terminal", label: "Terminal", icon: TerminalIcon },
  { id: "memory", label: "Memory", icon: LayersIcon },
]

const conversation = [
  { role: "user", text: "Refactor my auth module to use the offline keychain and add 2FA." },
  {
    role: "ai",
    text: "On it. Running fully local — no data leaves this device. I'll restructure auth.py, wire in the keychain, and scaffold TOTP-based 2FA.",
  },
  { role: "user", text: "Great. Run the test suite when you're done." },
]

export function Showcase() {
  const [active, setActive] = useState("chat")

  return (
    <section id="showcase" className="relative z-10 mx-auto max-w-6xl px-5 py-16">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        className="lg-specular glass rounded-3xl p-2.5 shadow-2xl"
      >
        <div className="rounded-[1.4rem] border border-white/[0.06] bg-black/40">
          {/* window bar */}
          <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-white/15" />
              <span className="h-3 w-3 rounded-full bg-white/15" />
              <span className="h-3 w-3 rounded-full bg-white/15" />
            </div>
            <div className="flex items-center gap-2 font-mono text-xs text-muted">
              <CpuIcon size={14} />
              <span>cyber-sh · local · neural-core-7B</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted">
              <span
                className="h-2 w-2 rounded-full bg-emerald-400"
                style={{ animation: "pulseDot 2s ease-in-out infinite" }}
              />
              <span className="hidden sm:inline">Online · Offline</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-[200px_1fr]">
            {/* sidebar tabs */}
            <div className="flex gap-2 overflow-x-auto border-b border-white/[0.08] p-3 md:flex-col md:overflow-visible md:border-b-0 md:border-r">
              {tabs.map((t) => {
                const Icon = t.icon
                const isActive = active === t.id
                return (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => setActive(t.id)}
                    className={`flex shrink-0 items-center gap-2.5 rounded-xl px-3.5 py-2.5 text-sm transition-all ${
                      isActive
                        ? "border border-white/[0.12] bg-white/[0.07] text-foreground"
                        : "border border-transparent text-muted hover:text-foreground"
                    }`}
                  >
                    <Icon size={18} />
                    <span>{t.label}</span>
                  </button>
                )
              })}
              <div className="mt-auto hidden rounded-xl border border-white/[0.08] bg-white/[0.03] p-3 md:block">
                <p className="font-mono text-[11px] text-muted">MODEL LOAD</p>
                <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
                  <div className="h-full w-[82%] rounded-full bg-white/60" />
                </div>
                <p className="mt-2 font-mono text-[11px] text-muted">6.4 GB · GPU offload</p>
              </div>
            </div>

            {/* main panel */}
            <div className="flex min-h-[320px] flex-col p-4 sm:p-6">
              <div className="flex-1 space-y-4">
                {conversation.map((m, i) => (
                  <div
                    key={i}
                    className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                        m.role === "user"
                          ? "border border-white/[0.1] bg-white/[0.07] text-foreground"
                          : "lg-specular glass text-foreground/90"
                      }`}
                    >
                      {m.role === "ai" && (
                        <span className="mb-1 block font-mono text-[11px] tracking-wide text-muted">
                          CYBER-SH
                        </span>
                      )}
                      {m.text}
                    </div>
                  </div>
                ))}
              </div>

              {/* input */}
              <div className="mt-4 flex items-center gap-2 rounded-2xl border border-white/[0.12] bg-white/[0.04] px-4 py-2.5 transition-colors focus-within:border-white/25">
                <CodeIcon size={18} className="text-muted" />
                <input
                  type="text"
                  placeholder="Ask Cyber-SH anything — it runs entirely offline…"
                  className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted/70 focus:outline-none"
                />
                <button
                  type="button"
                  aria-label="Send message"
                  className="lg-specular glass glass-tactile flex h-9 w-9 items-center justify-center rounded-xl text-foreground"
                >
                  <ArrowRightIcon size={18} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  )
}
