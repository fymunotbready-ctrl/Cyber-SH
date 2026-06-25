"use client"

import { motion } from "framer-motion"
import { ArrowRightIcon, DownloadIcon, LockIcon } from "./icons"

export function Hero() {
  return (
    <section className="relative z-10 mx-auto flex max-w-5xl flex-col items-center px-5 pt-36 pb-16 text-center sm:pt-44">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/[0.12] bg-white/[0.04] px-4 py-1.5 text-xs text-muted backdrop-blur-xl"
      >
        <LockIcon size={14} />
        <span>100% offline. Your data never leaves your machine.</span>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.05, ease: [0.22, 1, 0.36, 1] }}
        className="text-balance text-5xl font-semibold leading-[1.05] tracking-tight sm:text-6xl md:text-7xl"
      >
        Your Personal
        <br />
        Offline AI.
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.12, ease: [0.22, 1, 0.36, 1] }}
        className="mt-6 max-w-xl text-pretty text-lg leading-relaxed text-muted"
      >
        Cyber-SH runs a powerful neural core entirely on your hardware. No cloud,
        no tracking, no compromise — just a private agent that codes, reasons, and
        executes on your terms.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
        className="mt-10 flex flex-col items-center gap-3 sm:flex-row"
      >
        <a
          href="#cta"
          className="lg-shimmer lg-specular glass glass-tactile group flex items-center gap-2 rounded-full px-7 py-3.5 text-sm font-medium text-foreground"
        >
          <DownloadIcon size={18} />
          <span>Download for Desktop</span>
        </a>
        <a
          href="#showcase"
          className="group flex items-center gap-2 rounded-full border border-white/[0.12] px-7 py-3.5 text-sm font-medium text-muted transition-all hover:border-white/25 hover:text-foreground"
        >
          <span>See it in action</span>
          <ArrowRightIcon size={18} className="transition-transform group-hover:translate-x-0.5" />
        </a>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.32 }}
        className="mt-6 font-mono text-xs tracking-wide text-muted/70"
      >
        macOS · Windows · Linux — runs locally, even on a plane.
      </motion.p>
    </section>
  )
}
