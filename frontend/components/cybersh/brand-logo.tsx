"use client"

import { ACCENT_RGB } from "./lib"

export function BrandLogo({
  size = 34,
  withText = false,
}: {
  size?: number
  withText?: boolean
}) {
  return (
    <span
      aria-label="Cyber SH"
      role="img"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: Math.round(size * 0.32),
        lineHeight: 0,
        filter: `drop-shadow(0 0 6px rgba(${ACCENT_RGB},0.35)) drop-shadow(0 2px 6px rgba(0,0,0,0.5))`,
      }}
    >
      <img
        src="/cyber-sh-mark.png"
        alt=""
        style={{ height: size, width: "auto", display: "block" }}
      />
      {withText && (
        <img
          src="/cyber-sh-text.png"
          alt=""
          style={{ height: Math.round(size * 0.5), width: "auto", display: "block" }}
        />
      )}
    </span>
  )
}
