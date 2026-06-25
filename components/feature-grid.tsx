"use client"

import { motion } from "framer-motion"
import { ShieldIcon, NeuralIcon, SparkIcon, TerminalIcon } from "./icons"

const features = [
  {
    icon: ShieldIcon,
    title: "Local Privacy",
    desc: "Every prompt, file, and inference stays on your device. No telemetry, no cloud calls — air-gapped by design.",
  },
  {
    icon: NeuralIcon,
    title: "Neural Core Agent",
    desc: "A quantized neural core reasons, plans, and acts autonomously while running on consumer-grade hardware.",
  },
  {
    icon: SparkIcon,
    title: "Vibe Coding Engine",
    desc: "Describe the feel and intent — Cyber-SH writes, refactors, and reviews code that matches your style.",
  },
  {
    icon: TerminalIcon,
    title: "Terminal Execution",
    desc: "Grant scoped permissions and let the agent run commands, tests, and scripts directly in your shell.",
  },
]

export function FeatureGrid() {
  return (
    <section id="features" className="relative z-10 mx-auto max-w-6xl px-5 py-20">
      <div className="mx-auto mb-14 max-w-2xl text-center">
        <motion.h2
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-balance text-4xl font-semibold tracking-tight sm:text-5xl"
        >
          Power that stays private.
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.08 }}
          className="mt-4 text-pretty text-lg leading-relaxed text-muted"
        >
          Four core systems work together to deliver an elite AI experience —
          without ever touching the internet.
        </motion.p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
        {features.map((f, i) => {
          const Icon = f.icon
          return (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.6, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
              className="lg-specular glass glass-tactile rounded-3xl p-7"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/[0.12] bg-white/[0.05] text-foreground">
                <Icon size={22} />
              </div>
              <h3 className="mt-5 text-xl font-semibold tracking-tight text-foreground">
                {f.title}
              </h3>
              <p className="mt-2.5 text-pretty leading-relaxed text-muted">{f.desc}</p>
            </motion.div>
          )
        })}
      </div>
    </section>
  )
}
