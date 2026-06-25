"use client"

import { motion } from "framer-motion"
import { DownloadIcon, BoltIcon } from "./icons"

export function CtaFooter() {
  return (
    <>
      <section id="cta" className="relative z-10 mx-auto max-w-4xl px-5 py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="lg-specular lg-shimmer glass relative overflow-hidden rounded-[2rem] px-8 py-16 text-center"
        >
          <div className="relative z-10">
            <span className="inline-flex items-center gap-2 rounded-full border border-white/[0.12] bg-white/[0.04] px-4 py-1.5 text-xs text-muted">
              <BoltIcon size={14} />
              Free to download · Runs forever offline
            </span>
            <h2 className="mt-6 text-balance text-4xl font-semibold tracking-tight sm:text-5xl">
              Take your AI off the grid.
            </h2>
            <p className="mx-auto mt-4 max-w-md text-pretty text-lg leading-relaxed text-muted">
              Install Cyber-SH and own your intelligence. No accounts, no
              subscriptions, no surveillance.
            </p>
            <a
              href="#"
              className="lg-specular glass glass-tactile mt-9 inline-flex items-center gap-2 rounded-full px-8 py-4 text-sm font-medium text-foreground"
            >
              <DownloadIcon size={18} />
              <span>Download Cyber-SH</span>
            </a>
          </div>
        </motion.div>
      </section>

      <footer className="relative z-10 border-t border-white/[0.08]">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-5 py-8 sm:flex-row">
          <div className="flex items-center gap-2.5">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg border border-white/15 bg-white/[0.04] font-mono text-xs font-bold">
              C
            </span>
            <span className="font-mono text-sm font-bold tracking-[0.08em]">Cyber-SH</span>
          </div>
          <p className="text-sm text-muted">Your Personal Offline AI. Private by design.</p>
          <p className="font-mono text-xs text-muted/70">© {new Date().getFullYear()} Cyber-SH</p>
        </div>
      </footer>
    </>
  )
}
