"use client"

import { useEffect, useState } from "react"
import { MenuIcon, CloseIcon } from "./icons"

const links = [
  { label: "Showcase", href: "#showcase" },
  { label: "Features", href: "#features" },
  { label: "Privacy", href: "#features" },
  { label: "Download", href: "#cta" },
]

export function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-500 ${
        scrolled
          ? "border-b border-white/[0.08] backdrop-blur-md"
          : "border-b border-transparent"
      }`}
      style={{ backgroundColor: scrolled ? "rgba(0,0,0,0.7)" : "transparent" }}
    >
      <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <a href="#" className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg border border-white/15 bg-white/[0.04] font-mono text-sm font-bold tracking-tight">
            C
          </span>
          <span className="font-mono text-[15px] font-bold tracking-[0.08em] text-foreground">
            Cyber-SH
          </span>
        </a>

        <div className="hidden items-center gap-1 md:flex">
          {links.map((l) => (
            <a
              key={l.label}
              href={l.href}
              className="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:text-foreground"
            >
              {l.label}
            </a>
          ))}
          <a
            href="#cta"
            className="ml-2 rounded-full border border-white/15 bg-white/[0.06] px-4 py-2 text-sm font-medium text-foreground transition-all hover:bg-white/[0.12]"
          >
            Get Cyber-SH
          </a>
        </div>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-foreground md:hidden"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
        >
          {open ? <CloseIcon size={18} /> : <MenuIcon size={18} />}
        </button>
      </nav>

      {open && (
        <div className="border-t border-white/[0.08] backdrop-blur-md md:hidden" style={{ backgroundColor: "rgba(0,0,0,0.85)" }}>
          <div className="flex flex-col gap-1 px-5 py-4">
            {links.map((l) => (
              <a
                key={l.label}
                href={l.href}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2.5 text-sm text-muted transition-colors hover:bg-white/[0.05] hover:text-foreground"
              >
                {l.label}
              </a>
            ))}
          </div>
        </div>
      )}
    </header>
  )
}
