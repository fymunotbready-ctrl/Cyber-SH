"use client"

import type { CSSProperties } from "react"

type IconProps = { s?: number; c?: string; style?: CSSProperties }

const base = (s = 20) => ({
  width: s,
  height: s,
  viewBox: "0 0 24 24",
  fill: "none" as const,
  strokeWidth: 1.5,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
})

// ─────────────────────────────────────────────
// SF Symbol–style line-icon library (iOS minimalist)
// ─────────────────────────────────────────────
export const Ic = {
  logo: ({ s = 28, c = "currentColor", style }: IconProps) => (
    <svg width={s} height={s} viewBox="0 0 32 32" fill="none" stroke={c} strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" style={style}>
      <polygon points="16,2 28,9.5 28,22.5 16,30 4,22.5 4,9.5" />
      <circle cx="16" cy="16" r="4" />
      <line x1="16" y1="12" x2="16" y2="2" />
      <line x1="16" y1="20" x2="16" y2="30" />
      <line x1="12.5" y1="14.2" x2="4" y2="9.5" />
      <line x1="19.5" y1="17.8" x2="28" y2="22.5" />
      <line x1="19.5" y1="14.2" x2="28" y2="9.5" />
      <line x1="12.5" y1="17.8" x2="4" y2="22.5" />
    </svg>
  ),
  agent: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="3" y="11" width="18" height="11" rx="2.5" />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      <circle cx="12" cy="16.5" r="1.5" fill={c} stroke="none" />
    </svg>
  ),
  sec: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M12 2L4 6.3v5.7c0 5.5 3.8 10.7 8 12 4.2-1.3 8-6.5 8-12V6.3L12 2z" />
      <polyline points="9 12 11 14 15 10" />
    </svg>
  ),
  vibe: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5" />
      <path d="M9 18h6" /><path d="M10 22h4" />
    </svg>
  ),
  code: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <polyline points="16 18 22 12 16 6" /><polyline points="8 6 2 12 8 18" />
    </svg>
  ),
  chat: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  ),
  github: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg width={s} height={s} viewBox="0 0 24 24" fill={c} style={style}>
      <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
    </svg>
  ),
  person: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="8" r="4" /><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
    </svg>
  ),
  settings: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  ),
  theme: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="4" />
      <line x1="12" y1="2" x2="12" y2="4" /><line x1="12" y1="20" x2="12" y2="22" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="2" y1="12" x2="4" y2="12" /><line x1="20" y1="12" x2="22" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  ),
  upgrade: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
    </svg>
  ),
  keyboard: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="2" y="6" width="20" height="12" rx="2" />
      <line x1="6" y1="10" x2="6.01" y2="10" strokeWidth="2.5" /><line x1="10" y1="10" x2="10.01" y2="10" strokeWidth="2.5" />
      <line x1="14" y1="10" x2="14.01" y2="10" strokeWidth="2.5" /><line x1="18" y1="10" x2="18.01" y2="10" strokeWidth="2.5" />
      <line x1="8" y1="14" x2="16" y2="14" strokeWidth="1.5" />
    </svg>
  ),
  help: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="10" />
      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
      <line x1="12" y1="17" x2="12.01" y2="17" strokeWidth="2.5" />
    </svg>
  ),
  logout: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" />
    </svg>
  ),
  chevR: ({ s = 15, c = "currentColor", style }: IconProps) => (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" style={style}>
      <polyline points="9 18 15 12 9 6" />
    </svg>
  ),
  send: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  ),
  close: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2" strokeLinecap="round" style={style}>
      <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  ),
  plus: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2" strokeLinecap="round" style={style}>
      <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  ),
  eye: ({ s = 17, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" />
    </svg>
  ),
  eyeOff: ({ s = 17, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
      <line x1="1" y1="1" x2="23" y2="23" />
    </svg>
  ),
  terminal: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <polyline points="4 17 10 11 4 5" /><line x1="12" y1="19" x2="20" y2="19" />
    </svg>
  ),
  memory: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="2" y="7" width="20" height="10" rx="2" />
      <path d="M6 7V5m4 2V5m4 2V5m4 2V5M6 17v2m4-2v2m4-2v2m4-2v2" />
    </svg>
  ),
  web: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" />
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
    </svg>
  ),
  offline: ({ s = 14, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" />
      <circle cx="12" cy="16" r="1" fill={c} stroke="none" />
    </svg>
  ),
  newChat: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M12 20h9" /><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
    </svg>
  ),
  moon: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  ),
  sun: ({ s = 20, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="4.5" />
      <line x1="12" y1="2.5" x2="12" y2="5" /><line x1="12" y1="19" x2="12" y2="21.5" />
      <line x1="4.2" y1="4.2" x2="5.9" y2="5.9" /><line x1="18.1" y1="18.1" x2="19.8" y2="19.8" />
      <line x1="2.5" y1="12" x2="5" y2="12" /><line x1="19" y1="12" x2="21.5" y2="12" />
      <line x1="4.2" y1="19.8" x2="5.9" y2="18.1" /><line x1="18.1" y1="5.9" x2="19.8" y2="4.2" />
    </svg>
  ),
  check: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={c} strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" style={style}>
      <polyline points="20 6 9 17 4 12" />
    </svg>
  ),
  trash: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    </svg>
  ),
  lock: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 0 1 8 0v4" />
    </svg>
  ),
  lightbulb: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M9 18h6" /><path d="M10 22h4" />
      <path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V18h6v-1.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z" />
    </svg>
  ),
  wrench: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M14.7 6.3a4 4 0 0 0-5.2 5.2L3 18l3 3 6.5-6.5a4 4 0 0 0 5.2-5.2l-2.8 2.8-2.2-2.2 2.8-2.8z" />
    </svg>
  ),
  target: ({ s = 16, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1.5" />
    </svg>
  ),
  search: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="11" cy="11" r="7" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  ),
  flame: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M12 2c1 3 4 4.5 4 8a4 4 0 0 1-8 0c0-1 .3-1.8.8-2.5C9 9 9 7 12 2z" />
      <path d="M8.5 14a3.5 3.5 0 0 0 7 0c0-1.6-1-2.8-1.8-3.6" />
    </svg>
  ),
  book: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    </svg>
  ),
  unlock: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 0 1 7.5-2" />
    </svg>
  ),
  bolt: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <polygon points="13 2 4 14 11 14 10 22 19 10 12 10 13 2" />
    </svg>
  ),
  cap: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M2 9l10-5 10 5-10 5L2 9z" /><path d="M6 11v5c0 1 2.7 2.5 6 2.5s6-1.5 6-2.5v-5" /><line x1="22" y1="9" x2="22" y2="14" />
    </svg>
  ),
  smiley: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="9" /><path d="M8 14s1.5 2 4 2 4-2 4-2" />
      <line x1="9" y1="9" x2="9.01" y2="9" strokeWidth="2.5" /><line x1="15" y1="9" x2="15.01" y2="9" strokeWidth="2.5" />
    </svg>
  ),
  skull: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M12 2a8 8 0 0 0-5 14v3a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-3a8 8 0 0 0-5-14z" />
      <circle cx="9" cy="12" r="1.4" fill={c} stroke="none" /><circle cx="15" cy="12" r="1.4" fill={c} stroke="none" />
    </svg>
  ),
  scale: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <line x1="12" y1="3" x2="12" y2="21" /><line x1="7" y1="21" x2="17" y2="21" /><line x1="5" y1="6" x2="19" y2="6" />
      <path d="M5 6l-3 6h6l-3-6z" /><path d="M19 6l-3 6h6l-3-6z" />
    </svg>
  ),
  robot: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="4" y="8" width="16" height="12" rx="3" /><line x1="12" y1="4" x2="12" y2="8" /><circle cx="12" cy="3.5" r="1.2" />
      <line x1="9" y1="13" x2="9.01" y2="13" strokeWidth="2.5" /><line x1="15" y1="13" x2="15.01" y2="13" strokeWidth="2.5" />
      <line x1="9" y1="17" x2="15" y2="17" />
    </svg>
  ),
  bug: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="8" y="6" width="8" height="14" rx="4" /><path d="M9 6a3 3 0 0 1 6 0" />
      <line x1="3" y1="11" x2="8" y2="11" /><line x1="16" y1="11" x2="21" y2="11" />
      <line x1="3" y1="16" x2="8" y2="16" /><line x1="16" y1="16" x2="21" y2="16" />
    </svg>
  ),
  list: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" />
      <line x1="3" y1="6" x2="3.01" y2="6" strokeWidth="2.5" /><line x1="3" y1="12" x2="3.01" y2="12" strokeWidth="2.5" /><line x1="3" y1="18" x2="3.01" y2="18" strokeWidth="2.5" />
    </svg>
  ),
  sparkles: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3z" />
      <path d="M18 14l.8 2.2L21 17l-2.2.8L18 20l-.8-2.2L15 17l2.2-.8L18 14z" />
    </svg>
  ),
  clock: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="12" cy="12" r="9" /><polyline points="12 7 12 12 15 14" />
    </svg>
  ),
  doc: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" />
      <line x1="8" y1="13" x2="16" y2="13" /><line x1="8" y1="17" x2="13" y2="17" />
    </svg>
  ),
  brain: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-1 5 3 3 0 0 0 1 5 3 3 0 0 0 3 3 2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z" />
      <path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 1 5 3 3 0 0 1-1 5 3 3 0 0 1-3 3 2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" />
    </svg>
  ),
  key: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <circle cx="7.5" cy="15.5" r="4" /><line x1="10.5" y1="12.5" x2="20" y2="3" /><line x1="17" y1="6" x2="20" y2="9" /><line x1="14" y1="9" x2="17" y2="12" />
    </svg>
  ),
  box: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <path d="M21 8l-9-5-9 5v8l9 5 9-5V8z" /><polyline points="3 8 12 13 21 8" /><line x1="12" y1="13" x2="12" y2="21" />
    </svg>
  ),
  number: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <line x1="9" y1="4" x2="7" y2="20" /><line x1="17" y1="4" x2="15" y2="20" /><line x1="4" y1="9" x2="20" y2="9" /><line x1="4" y1="15" x2="20" y2="15" />
    </svg>
  ),
  dice: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="3" y="3" width="18" height="18" rx="3" />
      <line x1="8" y1="8" x2="8.01" y2="8" strokeWidth="2.5" /><line x1="16" y1="8" x2="16.01" y2="8" strokeWidth="2.5" />
      <line x1="12" y1="12" x2="12.01" y2="12" strokeWidth="2.5" /><line x1="8" y1="16" x2="8.01" y2="16" strokeWidth="2.5" /><line x1="16" y1="16" x2="16.01" y2="16" strokeWidth="2.5" />
    </svg>
  ),
  idcard: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <rect x="2" y="5" width="20" height="14" rx="2" /><circle cx="8" cy="11" r="2" /><path d="M5 16c0-1.7 1.3-3 3-3s3 1.3 3 3" /><line x1="14" y1="10" x2="18" y2="10" /><line x1="14" y1="14" x2="18" y2="14" />
    </svg>
  ),
  textformat: ({ s = 18, c = "currentColor", style }: IconProps) => (
    <svg {...base(s)} stroke={c} style={style}>
      <polyline points="4 7 4 4 20 4 20 7" /><line x1="9" y1="20" x2="15" y2="20" /><line x1="12" y1="4" x2="12" y2="20" />
    </svg>
  ),
}

export type IcKey = keyof typeof Ic
